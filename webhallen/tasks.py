from __future__ import annotations

import json
import re

import httpx
from rich import print
from rich.console import Console
from rich.progress import track
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

from webhallen.models import WebhallenJSON

err_console = Console(stderr=True)


def get_product_json(product_id: str) -> dict:
    """Get Webhallen product JSON.

    Args:
        product_id (str): Webhallen product ID

    Returns:
        dict: Webhallen product JSON or empty dict if error
    """
    product_url: str = f"https://www.webhallen.com/api/product/{product_id}"

    try:
        response: httpx.Response = httpx.get(product_url)
    except httpx.HTTPError as e:
        err_console.print(f"Error getting product {product_id}: {e}")
        return {}
    if response.is_error:
        err_console.print(f"Error getting product {product_id}: {response.status_code}\n{response.text}")
        return {}

    if response.text.startswith("<!DOCTYPE html>"):
        err_console.print(f"Probably 404? https://www.webhallen.com/api/product/{product_id}")
        return {}

    product_json = response.json()
    if not product_json:
        err_console.print(f"Error getting product JSON {product_id}: {response.status_code}\n{response.text}")
        return {}

    # Add our own metadata
    metadata: dict[str, str] = {
        "product_id": product_id,
        "product_url": product_url,
    }
    product_json["metadata"] = metadata

    return product_json


def _get_product_id(url: str) -> str | None:
    return match.group() if (match := re.search(r"\d+", url)) else None


def get_products_from_sitemap():  # noqa: ANN201
    """Generator for Webhallen products.

    Returns:
        dict: Webhallen product JSON
    """
    sitemap = "https://www.webhallen.com/sitemap.product.xml"
    sm = SiteMapParser(sitemap)
    json_exporter = JSONExporter(sm)
    urls_json = json_exporter.export_urls()
    urls_json = json.loads(urls_json)

    for url in urls_json:
        product_url: str = url["loc"]
        product_id = _get_product_id(product_url)
        if not product_id:
            err_console.print(f"Could not get product ID from {product_url}")
            continue

        yield get_product_json(product_id)


def scrape_products() -> None:
    """Scrape products from Webhallen and save to the Django database."""
    # Prepare the list of WebhallenJSON objects
    webhallen_json_list = []

    # Get the product JSON
    products = get_products_from_sitemap()
    products = list(products)
    for product in track(products, description="Scraping products...", total=len(products)):
        if not product:
            continue

        # Get product ID from metadata
        try:
            product_id = product["metadata"]["product_id"]
            if not product_id:
                err_console.print(f"Could not get product ID from {product}")
                continue
        except KeyError:
            err_console.print(f"Could not get product ID from {product}")
            continue

        webhallen_json = WebhallenJSON(
            product_id=product_id,
            product_json=product,
        )
        webhallen_json_list.append(webhallen_json)

    # Bulk create the WebhallenJSON objects
    WebhallenJSON.objects.bulk_create(webhallen_json_list)

    print("Done scraping Webhallen products")
