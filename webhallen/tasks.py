from __future__ import annotations

import re
from functools import lru_cache

import httpx
import orjson
from celery import shared_task
from django.db import models, transaction
from rich import print
from rich.console import Console
from rich.progress import track
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser
from tenacity import retry, stop_after_attempt, wait_random_exponential

from webhallen.models import (
    SitemapArticle,
    SitemapCampaign,
    SitemapCampaignList,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapManufacturer,
    SitemapProduct,
    SitemapRoot,
    SitemapSection,
    WebhallenJSON,
    WebhallenSection,
)

err_console = Console(stderr=True)


@retry(stop=stop_after_attempt(3))
def scrape_sitemap_root() -> None:
    """Scrape the root sitemap."""
    sitemap = "https://www.webhallen.com/sitemap.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_sitemaps()
    urls_json = orjson.loads(urls_json)
    sitemap_objects: list[SitemapRoot] = [SitemapRoot(loc=url["loc"], active=True) for url in urls_json]
    with transaction.atomic():
        SitemapRoot.objects.bulk_create(sitemap_objects)
    print(f"Done scraping sitemap.xml, {len(sitemap_objects)} sitemaps found")


@retry(stop=stop_after_attempt(3))
def scrape_sitemap(url: str, model_class: type[models.Model], model_name: str) -> None:
    """Scrape a sitemap.xml and store the data in the specified model."""
    sm = SiteMapParser(url)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = orjson.loads(urls_json)

    sitemap_objects: list[models.Model] = [
        model_class(loc=url["loc"], active=True, priority=url["priority"]) for url in urls_json
    ]

    with transaction.atomic():
        model_class.objects.bulk_create(
            sitemap_objects,
            update_fields=["active", "priority"],
            ignore_conflicts=True,
        )

    print(f"Done scraping {model_name}, {len(sitemap_objects)} urls found")


# TODO: Remove Rich and use logging instead
err_console = Console(stderr=True)


@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=30))
def scrape_product(product_id: str, product_url: str) -> dict:
    """Scrape a single product from Webhallen API and return the JSON.

    Args:
        product_id: The product ID.
        product_url: URL to API. This contains the JSON.

    Raises:
        e: If the response is a HTTP error.
        httpx.HTTPError: If the request is 404 but the response is not 404.
        httpx.HTTPError: If the JSON is empty.

    Returns:
        The JSON response.
    """
    try:
        response: httpx.Response = httpx.get(product_url)
    except httpx.HTTPError as e:
        err_console.print(f"Error getting product {product_id}: {e}")
        raise e from None

    if response.text.startswith("<!DOCTYPE html>"):
        msg: str = f"Probably 404? https://www.webhallen.com/api/v1/product/{product_id}"
        err_console.print(msg)
        raise httpx.HTTPError(msg)

    product_json = response.json()
    if not product_json:
        msg: str = f"Empty JSON response for https://www.webhallen.com/api/v1/product/{product_id}"
        err_console.print(f"Error getting product {product_id}: {msg}")
        raise httpx.HTTPError(msg)

    return dict(product_json)


@shared_task(
    bind=True,
    name="scrape_webhallen_products",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="webhallen",
)
def scrape_products() -> None:
    """Scrape products from Webhallen sitemap and save them to the database."""
    # TODO: Use Celery jobs to scrape products in parallel
    # TODO: Use Celery Beat to scrape products every 24 hours
    sitemap = "https://www.webhallen.com/sitemap.product.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = orjson.loads(urls_json)

    print(f"Got {len(urls_json)} products from Webhallen sitemap")
    for url in track(urls_json, description="Scraping products...", total=len(urls_json)):
        loc: str = url["loc"]

        product_id: str | None = match.group() if (match := re.search(r"\d+", loc)) else None
        if not product_id:
            err_console.print(f"Could not get product ID from {loc}")
            continue

        product_url: str = f"https://www.webhallen.com/api/v1/product/{product_id}"
        print(f"GET {product_url}")

        product_json: dict = scrape_product(product_id, product_url)

        # Add our own metadata
        metadata: dict[str, str] = {
            "product_id": product_id,
            "product_url": product_url,
        }
        product_json["metadata"] = metadata

        product, created = WebhallenJSON.objects.get_or_create(
            product_id=product_id,
            defaults={"product_json": product_json},
        )

        if created:
            print(f"Created {product_id}")
        product.save()

    print("Done!")


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
        section_name: str = section.name or ""
        if section_url.startswith(f"https://www.webhallen.com/se/section/{section_id}-"):
            print(f"{section_id} - {section_name}")
            print(f"\t{section_url}")
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

    print(f"\t{icon_url}")
    return icon_url


def mark_sections_inactive() -> None:
    """Mark all sections as inactive."""
    sections = WebhallenSection.objects.all()
    for section in sections:
        section.active = False
    WebhallenSection.objects.bulk_update(sections, ["active"])


@shared_task(
    bind=True,
    name="create_webhallen_sections",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="webhallen",
)
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


@shared_task(
    bind=True,
    name="scrape_sitemaps",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="webhallen",
)
def scrape_sitemaps() -> None:
    """Scrape all sitemaps."""
    # TODO: Should we use Celery jobs instead of loop?
    sitemaps = [
        ("https://www.webhallen.com/sitemap.product.xml", SitemapProduct, "sitemap.product.xml"),
        ("https://www.webhallen.com/sitemap.manufacturer.xml", SitemapManufacturer, "sitemap.manufacturer.xml"),
        ("https://www.webhallen.com/sitemap.article.xml", SitemapArticle, "sitemap.article.xml"),
        ("https://www.webhallen.com/sitemap.infoPages.xml", SitemapInfoPages, "sitemap.infoPages.xml"),
        ("https://www.webhallen.com/sitemap.home.xml", SitemapHome, "sitemap.home.xml"),
        ("https://www.webhallen.com/sitemap.section.xml", SitemapSection, "sitemap.section.xml"),
        ("https://www.webhallen.com/sitemap.category.xml", SitemapCategory, "sitemap.category.xml"),
        ("https://www.webhallen.com/sitemap.campaign.xml", SitemapCampaign, "sitemap.campaign.xml"),
        ("https://www.webhallen.com/sitemap.campaignList.xml", SitemapCampaignList, "sitemap.campaignList.xml"),
    ]

    for url, model_class, model_name in sitemaps:
        scrape_sitemap(url=url, model_class=model_class, model_name=model_name)

    scrape_sitemap_root()  # Needs to be standalone because it doesn't have priority
