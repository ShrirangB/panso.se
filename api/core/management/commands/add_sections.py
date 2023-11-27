from __future__ import annotations

from functools import lru_cache

from django.core.management.base import BaseCommand, CommandError
from loguru import logger

from core.webhallen.models import WebhallenJSON, WebhallenSection


@lru_cache(maxsize=20)
def get_section_url(section_id: str | None) -> str | None:
    """Return section URL."""
    if not section_id:
        logger.error(f"Error getting section URL for {section_id}")
        return None

    sections = WebhallenSection.objects.all()
    for section in sections:
        section_url: str | None = section.url
        if not section_url:
            continue
        if section_url.startswith(f"https://www.webhallen.com/se/section/{section_id}-"):
            logger.debug(f"Found section URL for {section_id}")
            return section_url

    section_id_presentkort = 19
    if section_id == section_id_presentkort:
        # Has no URL so we use something close
        return "https://www.webhallen.com/se/info/28-Kop-presentkort"

    logger.error(f"Error getting section URL for {section_id}")
    return None


@lru_cache(maxsize=20)
def get_section_icon_url(icon: str | None, name: str | None) -> str | None:
    """Return section icon URL.

    Args:
        icon: Section icon name
        name: Section name

    Returns:
        str: URL to section icon
    """
    # TODO: Save icon to disk and return URL?
    icon_hex_color: str = "1A1A1D"
    if not icon:
        if name != "Presentkort":
            logger.error(f"Error getting section icon URL for {name}")
        return None
    icon_url: str = f"https://cdn.webhallen.com/api/dynimg/category/{icon}/{icon_hex_color}"

    logger.debug(f"Found section icon URL for {name}")
    return icon_url


def create_sections() -> None:
    """Loop through all JSON objects and create sections."""
    old_sections = WebhallenSection.objects.all()

    for json in WebhallenJSON.objects.all():
        product_json = dict(json.product_json)
        product_json: dict = product_json.get("product", {})
        if not product_json:
            logger.error(f"Error getting product JSON {json.product_id}")
            continue

        section: dict = product_json.get("section", {})
        if not section:
            logger.error(f"Error getting section JSON {json.product_id}")
            continue

        # 3
        section_id: str | None = section.get("id")
        # Datorer och Tillbehör
        meta_title: str | None = product_json.get("metaTitle")
        # True
        active: bool | None = section.get("active")
        # Datorer och Tillbehör
        name: str | None = section.get("name")
        # https://www.webhallen.com/se/section/3-datorer-och-tillbehor
        url: str | None = get_section_url(section_id=section_id)
        # datorer_tillbehor
        icon: str | None = section.get("icon")
        # https://cdn.webhallen.com/api/dynimg/category/datorer_tillbehor/1A1A1D
        icon_url: str | None = get_section_icon_url(icon=icon, name=name)

        # Only update if meta_title, active, name, url, icon or icon_url has changed since last time
        old_section: WebhallenSection | None = old_sections.filter(section_id=section_id).first()
        if old_section and (  # noqa: PLR0916
            old_section.meta_title == meta_title
            and old_section.active == active
            and old_section.name == name
            and old_section.url == url
            and old_section.icon == icon
            and old_section.icon_url == icon_url
        ):
            continue

        obj: WebhallenSection
        created: bool
        obj, created = WebhallenSection.objects.update_or_create(
            section_id=section_id,
            defaults={
                "url": url,
                "meta_title": meta_title,
                "active": active,
                "icon": icon,
                "icon_url": icon_url,
                "name": name,
            },
        )

        if created:
            logger.info(f"Found new section! {name} - {url}")

        obj.save()


class Command(BaseCommand):
    """Loop through all JSON objects and create sections."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            create_sections()
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while creating sections"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
