from __future__ import annotations

import json
import re

import httpx
from loguru import logger
from simple_history.utils import update_change_reason
from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

from core.stores.webhallen.models import WebhallenJSON


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
        logger.error(f"Error getting product {product_id}: {e}")
        return {}
    if response.is_error:
        logger.error(f"Error getting product {product_id}: {response.status_code}\n{response.text}")
        return {}

    if response.text.startswith("<!DOCTYPE html>"):
        logger.error(f"Probably 404? https://www.webhallen.com/api/product/{product_id}")
        return {}

    product_json = response.json()
    if not product_json:
        logger.error(f"Error getting product JSON {product_id}: {response.status_code}\n{response.text}")
        return {}

    # Add our own metadata
    metadata: dict[str, str] = {
        "product_id": product_id,
        "product_url": product_url,
    }
    product_json["metadata"] = metadata

    return product_json


def _get_product_id(url: str) -> str | None:
    match: re.Match[str] | None = re.search(r"\d+", url)
    if match:
        return match.group()
    return None


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
            logger.error(f"Could not get product ID from {product_url}")
            continue

        yield get_product_json(product_id)


def scrape_products(scrape_reason: str = "No reason given") -> None:
    """Scrape products from Webhallen and save to the Django database.

    Args:
        scrape_reason: Reason for scraping the products.
    """
    # Get the product JSON
    products = get_products_from_sitemap()

    # Save the products
    for product in products:
        if not product:
            continue

        # Get product ID from metadata
        product_id = product["metadata"]["product_id"]
        if not product_id:
            logger.error(f"Could not get product ID from {product}")
            continue

        obj: WebhallenJSON
        obj, _ = WebhallenJSON.objects.update_or_create(
            product_id=product_id,
            defaults={
                "product_json": product,
            },
        )

        obj.save()
        update_change_reason(obj, f"Scraped Webhallen product JSON: {scrape_reason}")

    logger.info("Done scraping Webhallen products")
