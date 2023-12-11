from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from rich import print
from rich.pretty import pprint

from intel.models import ArkFilterData


def get_data_from_ark() -> dict[str, dict[str, dict[str, str]]]:
    """Get the data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.

    Returns:
        dict[str, dict[str, dict[str, str]]]: The filters from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.
    """
    with sync_playwright() as p:
        browser: Browser = p.firefox.launch()
        context: BrowserContext = browser.new_context()
        page: Page = context.new_page()
        page.goto("https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html")
        result = page.evaluate("window.arkFiltersData")
        browser.close()
    return result


class Command(BaseCommand):
    """Scrape the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            result = get_data_from_ark()
            if result:
                ArkFilterData.objects.update_or_create(pk=1, defaults={"json_data": result})
                pprint(result)
                print("Added data to database")
            else:
                print("Result is empty")
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while creating eans"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
