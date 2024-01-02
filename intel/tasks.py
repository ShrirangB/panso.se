"""Celery tasks for the intel app.

Tasks:
    scrape_intel_ark: Scrape https://www.intel.com/content/www/us/en/products/compare.html.
    get_data_from_ark: Get the data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.
"""

from __future__ import annotations

from celery import shared_task
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from rich import print
from rich.pretty import pprint

from intel.models import ArkFilterData
from intel.scrape_intel_ark import get_html, process_html


@shared_task(
    bind=True,
    name="scrape_intel_ark",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="intel_ark",
)
def scrape_intel_ark() -> None:
    """Scrape https://www.intel.com/content/www/us/en/products/compare.html."""
    print("Scraping Intel ARK")
    for data in get_html():
        process_html(processor_data=data)


@shared_task(
    bind=True,
    name="get_data_from_ark",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="intel_ark",
)
def get_data_from_ark() -> None:
    """Get the data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""
    with sync_playwright() as p:
        browser: Browser = p.firefox.launch()
        context: BrowserContext = browser.new_context()
        page: Page = context.new_page()
        page.goto("https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html")
        result = page.evaluate("window.arkFiltersData")
        browser.close()

    if result:
        ArkFilterData.objects.update_or_create(pk=1, defaults={"json_data": result})
        pprint(result)
        print("Added data to database")
    else:
        print("Result is empty")
