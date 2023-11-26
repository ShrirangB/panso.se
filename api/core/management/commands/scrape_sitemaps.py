from __future__ import annotations

import json

from loguru import logger
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

from core.webhallen.models import (
    SitemapCampaign,
    SitemapCampaignList,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapProduct,
    SitemapRoot,
    SitemapSection,
)


def scrape_sitemap_root() -> None:
    """Scrape the root sitemap."""
    sitemap = "https://www.webhallen.com/sitemap.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_sitemaps()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]

        already_exists_in_db: bool = SitemapRoot.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.xml")
            SitemapRoot.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapRoot.objects.update_or_create(loc=loc, defaults={"active": True})
        if created:
            logger.info(f"Found new sitemap sitemap.xml! {loc}")

        obj.save()


def scrape_sitemap_home() -> None:
    """Scrape sitemap.home.xml."""
    sitemap = "https://www.webhallen.com/sitemap.home.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapHome.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.home.xml")
            SitemapHome.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapHome.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.home.xml! {loc}")

        obj.save()


def scrape_sitemap_section() -> None:
    """Scrape sitemap.section.xml."""
    sitemap = "https://www.webhallen.com/sitemap.section.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapSection.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.section.xml")
            SitemapSection.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapSection.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.section.xml! {loc}")

        obj.save()


def scrape_sitemap_category() -> None:
    """Scrape sitemap.category.xml."""
    sitemap = "https://www.webhallen.com/sitemap.category.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapCategory.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.category.xml")
            SitemapCategory.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapCategory.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.category.xml! {loc}")

        obj.save()


def scrape_sitemap_campaign() -> None:
    """Scrape sitemap.campaign.xml."""
    sitemap = "https://www.webhallen.com/sitemap.campaign.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapCampaign.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.campaign.xml")
            SitemapCampaign.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapCampaign.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.campaign.xml! {loc}")

        obj.save()


def scrape_sitemap_campaign_list() -> None:
    """Scrape sitemap.campaignList.xml."""
    sitemap = "https://www.webhallen.com/sitemap.campaignList.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapCampaignList.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.campaignList.xml")
            SitemapCampaignList.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapCampaignList.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.campaignList.xml! {loc}")

        obj.save()


def scrape_sitemap_info_pages() -> None:
    """Scrape sitemap.infoPages.xml."""
    sitemap = "https://www.webhallen.com/sitemap.infoPages.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapInfoPages.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.infoPages.xml")
            SitemapInfoPages.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapInfoPages.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.infoPages.xml! {loc}")

        obj.save()


def scrape_sitemap_products() -> None:
    """Scrape sitemap.product.xml."""
    sitemap = "https://www.webhallen.com/sitemap.product.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    urls_in_sitemap: list[str] = [url["loc"] for url in urls_json]

    for url in urls_json:
        loc: str = url["loc"]
        priority: float = url["priority"]

        already_exists_in_db: bool = SitemapProduct.objects.filter(loc=loc).exists()
        if loc not in urls_in_sitemap and already_exists_in_db:
            logger.info(f"{loc} was removed from the sitemap.product.xml")
            SitemapProduct.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapProduct.objects.update_or_create(
            loc=loc,
            defaults={
                "active": True,
                "priority": priority,
            },
        )
        if created:
            logger.info(f"Found new sitemap in sitemap.product.xml! {loc}")

        obj.save()
