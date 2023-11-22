from __future__ import annotations

from django.urls import URLPattern, path

from core.webhallen.views import list_product, list_products

urlpatterns: list[URLPattern] = [
    # /api/v1/webhallen/products/ - GET - Return all Webhallen products as JSON
    path("api/v1/webhallen/products", list_products),
    # /api/v1/webhallen/products/<product_id> - GET - Return Webhallen product as JSON
    path("api/v1/webhallen/products/<str:product_id>", list_product),
]
