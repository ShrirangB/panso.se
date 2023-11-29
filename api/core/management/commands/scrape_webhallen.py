from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand, CommandError

from core.stores.webhallen.tasks import scrape_products

if TYPE_CHECKING:
    import argparse


class Command(BaseCommand):
    """Scrape Webhallen products and save to the database."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def add_arguments(self: BaseCommand, parser: argparse.ArgumentParser) -> None:  # noqa: PLR6301
        """Add arguments to the command."""
        parser.add_argument(
            "--reason",
            type=str,
            default="No reason given",
            help="Reason for scraping the products.",
        )

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            scrape_reason: str = options["reason"]
            scrape_products(scrape_reason)
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while scraping Webhallen products"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
