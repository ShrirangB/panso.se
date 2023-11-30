from __future__ import annotations

from functools import lru_cache

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from rich import print
from rich.console import Console
from rich.progress import track

from core.stores.webhallen.models import WebhallenJSON, WebhallenSection

err_console = Console(stderr=True)


@lru_cache(maxsize=20)
def get_section_url(section_id: str | None) -> str | None:
    """Return section URL."""
    if not section_id:
        err_console.print(f"Error getting section URL for {section_id}")
        return None

    sections = WebhallenSection.objects.all()
    for section in sections:
        section_url: str | None = section.url
        if not section_url:
            continue
        if section_url.startswith(f"https://www.webhallen.com/se/section/{section_id}-"):
            print(f"Found section URL for {section_id}")
            return section_url

    section_id_presentkort = 19
    if section_id == section_id_presentkort:
        # Has no URL so we use something close
        return "https://www.webhallen.com/se/info/28-Kop-presentkort"

    err_console.print(f"Error getting section URL for {section_id}")
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
            err_console.print(f"Error getting section icon URL for {name}")
        return None
    icon_url: str = f"https://cdn.webhallen.com/api/dynimg/category/{icon}/{icon_hex_color}"

    print(f"Found section icon URL for {name}")
    return icon_url


def mark_sections_inactive() -> None:
    """Mark all sections as inactive."""
    sections = WebhallenSection.objects.all()
    for section in sections:
        section.active = False
    WebhallenSection.objects.bulk_update(sections, ["active"])


def create_sections() -> None:
    """Loop through all JSON objects and create sections."""
    mark_sections_inactive()

    new_sections = []
    products = WebhallenJSON.objects.all()
    for json in track(products, description="Processing...", total=products.count()):
        product_json: dict = dict(json.product_json).get("product", {})
        if not product_json:
            err_console.print(f"Error getting product JSON {json.product_id}")
            continue

        section: dict = product_json.get("section", {})
        if not section:
            err_console.print(f"Error getting section JSON {json.product_id}")
            continue

        section_id: str | None = section.get("id")
        meta_title: str | None = product_json.get("metaTitle")
        active: bool | None = section.get("active")
        name: str | None = section.get("name")
        url: str | None = get_section_url(section_id=section_id)
        icon: str | None = section.get("icon")
        icon_url: str | None = get_section_icon_url(icon=icon, name=name)

        new_sections.append(
            WebhallenSection(
                section_id=section_id,
                url=url,
                meta_title=meta_title,
                active=active,
                icon=icon,
                icon_url=icon_url,
                name=name,
            ),
        )

    with transaction.atomic():
        sections: list[WebhallenSection] = WebhallenSection.objects.bulk_create(
            new_sections,
            update_fields=["url", "meta_title", "active", "icon", "icon_url", "name"],
            ignore_conflicts=True,
        )
        print(f"Created {len(sections)} sections" if sections else "No sections created")


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
