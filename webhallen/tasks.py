from __future__ import annotations

import json
import re
from datetime import datetime

import httpx
from rich import print
from rich.console import Console
from rich.progress import track
from simple_history.utils import update_change_reason
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser
from tenacity import retry, stop_after_attempt, wait_random_exponential
from zoneinfo import ZoneInfo

from webhallen.models import WebhallenJSON

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
        msg: str = f"Probably 404? https://www.webhallen.com/api/product/{product_id}"
        err_console.print(msg)
        raise httpx.HTTPError(msg)

    product_json = response.json()
    if not product_json:
        msg: str = f"Empty JSON response for https://www.webhallen.com/api/product/{product_id}"
        err_console.print(f"Error getting product {product_id}: {msg}")
        raise httpx.HTTPError(msg)

    return dict(product_json)


def scrape_products() -> None:
    """Scrape products from Webhallen sitemap and save them to the database."""
    sitemap = "https://www.webhallen.com/sitemap.product.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    print(f"Got {len(urls_json)} products from Webhallen sitemap")
    for url in track(urls_json, description="Scraping products...", total=len(urls_json)):
        loc: str = url["loc"]

        product_id: str | None = match.group() if (match := re.search(r"\d+", loc)) else None
        if not product_id:
            err_console.print(f"Could not get product ID from {loc}")
            continue

        product_url: str = f"https://www.webhallen.com/api/product/{product_id}"
        print(f"GET {product_url}")

        product_json: dict = scrape_product(product_id, product_url)

        # Add our own metadata
        metadata: dict[str, str] = {
            "product_id": product_id,
            "product_url": product_url,
        }
        product_json["metadata"] = metadata

        product, created = WebhallenJSON.objects.get_or_create(
            product_id=product_id, defaults={"product_json": product_json}
        )

        if created:
            print(f"Created {product_id}")
        product.save()

        current_datetime: datetime = datetime.now(tz=ZoneInfo("Europe/Stockholm"))
        iso8601_format: str = current_datetime.isoformat()
        update_change_reason(product, f"Daily scrape {iso8601_format}")

    print("Done!")
