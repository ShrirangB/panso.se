import argparse

from django.core.management.base import BaseCommand, CommandError

from core.webhallen.tasks import scrape_products


class Command(BaseCommand):
    """Scrape Webhallen products and save to the database.

    Args:
        BaseCommand: The base class from which all management commands ultimately
        derive.

    Raises:
        CommandError: If there is an error with the command.
    """

    help = "Closes the specified poll for voting"  # noqa: A003
    output_transaction = True
    requires_migrations_checks = True

    def add_arguments(self: BaseCommand, parser: argparse.ArgumentParser) -> None:  # noqa: PLR6301
        """Add arguments to the command.

        Args:
            self: The command object.
            parser: The parser object.
        """
        parser.add_argument(
            "--reason",
            type=str,
            default="No reason given",
            help="Reason for scraping the products.",
        )

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command.

        Args:
            self: The command object.
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Raises:
            CommandError: If there is an error with the command or got ctrl-c.
        """
        try:
            scrape_reason: str = options["reason"]
            scrape_products(scrape_reason)
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while scraping Webhallen products"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
