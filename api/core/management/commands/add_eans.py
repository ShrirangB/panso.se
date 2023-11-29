from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from rich import print
from rich.console import Console
from rich.progress import track

from core.models import Eans
from core.stores.webhallen.models import WebhallenJSON

err_console = Console(stderr=True)


def create_eans() -> None:
    """Loop through all JSON objects and create eans."""
    products = WebhallenJSON.objects.all()
    for json in track(products, description="Processing...", total=products.count()):
        product_json = dict(json.product_json)
        product_json: dict = product_json.get("product", {})
        if not product_json:
            err_console.print(f"Error getting product JSON for {json.product_id}")
            continue

        name: str = product_json.get("name", "No name")
        eans: dict = product_json.get("eans", {})
        if not eans:
            err_console.print(f"Error getting eans JSON for {json.product_id}")
            continue

        for ean in eans:
            obj, created = Eans.objects.update_or_create(
                ean=ean,
                defaults={
                    "name": name,
                    "list_of_webhallen_ids_with_ean": f"{json.product_id}",
                },
            )
            if created:
                print(f"Found new ean! {ean} - {name}")
            obj.save()


class Command(BaseCommand):
    """Loop through all JSON objects and create eans."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            create_eans()
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while creating eans"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
