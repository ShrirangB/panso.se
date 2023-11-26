from __future__ import annotations

from django.urls import URLPattern, path

from core.webhallen.views import (
    api_product,
    api_products,
    api_products_hugo,
    api_sitemaps_categories,
    api_sitemaps_home,
    api_sitemaps_root,
    api_sitemaps_sections,
    testboi,
)

urlpatterns: list[URLPattern] = [
    path("api/v1/webhallen/products", api_products),
    path("api/v1/webhallen/products/hugo", api_products_hugo),
    path("api/v1/webhallen/products/<str:product_id>", api_product),
    path("api/v1/webhallen/sitemaps/root", api_sitemaps_root),
    path("api/v1/webhallen/sitemaps/home", api_sitemaps_home),
    path("api/v1/webhallen/sitemaps/sections", api_sitemaps_sections),
    path("api/v1/webhallen/sitemaps/categories", api_sitemaps_categories),
    path("testboi", testboi),
]
