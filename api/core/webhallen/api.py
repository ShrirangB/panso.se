from __future__ import annotations

from typing import ClassVar, cast

from django.http import HttpRequest  # noqa: TCH002 # Needed for NinjaAPI
from ninja import Router, Schema
from ninja.errors import HttpError

from core.webhallen.description import list_product_description
from core.webhallen.models import Webhallen

router = Router()


class WebhallenSchema(Schema):
    """Schema for Webhallen."""

    class Meta:
        """Meta class for Webhallen."""

        model = Webhallen
        fields: ClassVar[list[str]] = ["product_id", "product_json", "created", "updated"]


# TODO: Add the history
@router.get(
    "/products",
    response=WebhallenSchema,
    openapi_extra={
        "summary": "List all products from Webhallen.",
        "tags": ["webhallen"],
        "description": list_product_description,
        "x-code-samples": [
            {
                "lang": "Python",
                "source": """import requests""",
            },
        ],
        "externalDocs": {
            "description": "GitHub",
            "url": "https://www.webhallen.com/api/",
        },
        "servers": [
            {
                "url": "https://www.webhallen.com/api/product/",
                "description": "Webhallen API",
            },
            {
                "url": "https://api.panso.se/api/webhallen/products/",
                "description": "Panso API",
            },
        ],
    },
)
def list_products(request: HttpRequest) -> WebhallenSchema:  # noqa: ARG001
    """List all products from Webhallen."""
    products = Webhallen.objects.all()
    if not products:
        raise HttpError(404, "No products found")
    return cast(WebhallenSchema, products)
