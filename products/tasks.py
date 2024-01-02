"""Celery tasks for our main panso.se application.

Tasks:
    - create_eans
        Loop through all JSON objects and create eans.
"""

from __future__ import annotations

from celery import shared_task
from rich import print
from rich.progress import track

from products.models import Eans
from webhallen.models import WebhallenJSON


@shared_task(
    bind=True,
    name="create_eans",
    max_retries=7,
    retry_backoff=5,
    soft_time_limit=60,
    queue="webhallen",
)
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
