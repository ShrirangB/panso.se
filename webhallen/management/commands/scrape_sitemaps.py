from __future__ import annotations

import json

from django.core.management.base import BaseCommand, CommandError
from django.db import models, transaction
from rich import print
from rich.console import Console
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser
from tenacity import retry, stop_after_attempt

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
)

err_console = Console(stderr=True)


@retry(stop=stop_after_attempt(3))
def scrape_sitemap_root() -> None:
    """Scrape the root sitemap."""
    sitemap = "https://www.webhallen.com/sitemap.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_sitemaps()
    urls_json = json.loads(urls_json)
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
    urls_json = json.loads(urls_json)

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


class Command(BaseCommand):
    """Scrape Webhallen products and save to the database."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            scrape_sitemap("https://www.webhallen.com/sitemap.product.xml", SitemapProduct, "sitemap.product.xml")
            scrape_sitemap(
                "https://www.webhallen.com/sitemap.manufacturer.xml",
                SitemapManufacturer,
                "sitemap.manufacturer.xml",
            )
            scrape_sitemap("https://www.webhallen.com/sitemap.article.xml", SitemapArticle, "sitemap.article.xml")
            scrape_sitemap("https://www.webhallen.com/sitemap.infoPages.xml", SitemapInfoPages, "sitemap.infoPages.xml")
            scrape_sitemap("https://www.webhallen.com/sitemap.home.xml", SitemapHome, "sitemap.home.xml")
            scrape_sitemap("https://www.webhallen.com/sitemap.section.xml", SitemapSection, "sitemap.section.xml")
            scrape_sitemap("https://www.webhallen.com/sitemap.category.xml", SitemapCategory, "sitemap.category.xml")
            scrape_sitemap("https://www.webhallen.com/sitemap.campaign.xml", SitemapCampaign, "sitemap.campaign.xml")
            scrape_sitemap(
                "https://www.webhallen.com/sitemap.campaignList.xml",
                SitemapCampaignList,
                "sitemap.campaignList.xml",
            )
            scrape_sitemap_root()  # Needs to be standalone because it doesn't have priority
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while scraping Webhallen products"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
