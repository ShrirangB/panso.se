from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from rich import print
from rich.progress import track

from products.models import Eans
from webhallen.models import WebhallenJSON


def create_eans() -> None:
    """Loop through all JSON objects and create eans."""
    eans_to_create: list[Eans] = []
    products = WebhallenJSON.objects.all()
    for json in track(products, description="Processing...", total=products.count()):
        product_json = dict(json.product_json)
        if not product_json:
            print(f"Product JSON is empty for {json.product_id}")
            continue
        product: dict = product_json.get("product", {})
        eans: dict = product.get("eans", {})
        if not eans:
            continue

        name = product.get("name", "")
        if not name:
            print(f"No name for {json.product_id}")
            continue

        eans_to_create.extend([Eans(ean=ean, name=name) for ean in eans])
        print(f"Created {len(eans_to_create)} EANs so far")

    Eans.objects.bulk_create(eans_to_create, update_fields=["name"], ignore_conflicts=True)
    print(f"Created {len(eans_to_create)} EANs")


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
