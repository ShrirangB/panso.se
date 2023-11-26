from __future__ import annotations

import json

from loguru import logger
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

from core.webhallen.models import SitemapRoot


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
            logger.info(f"{loc} was removed from the sitemap")
            SitemapRoot.objects.filter(url=loc).update(active=False)
            continue

        obj, created = SitemapRoot.objects.update_or_create(loc=loc, defaults={"active": True})
        if created:
            logger.info(f"Found new sitemap root! {loc}")

        obj.save()
