from __future__ import annotations

from django.urls import URLPattern, path

from core.webhallen.views import list_product, list_products, list_products_hugo, testboi

urlpatterns: list[URLPattern] = [
    # /api/v1/webhallen/products/ - GET - Return all Webhallen products as JSON
    path("api/v1/webhallen/products", list_products),
    # /api/v1/webhallen/products/hugo/ - GET - Return all Webhallen products as JSON
    path("api/v1/webhallen/products/hugo", list_products_hugo),
    # /api/v1/webhallen/products/<product_id> - GET - Return Webhallen product as JSON
    path("api/v1/webhallen/products/<str:product_id>", list_product),
    path("testboi", testboi),
]
