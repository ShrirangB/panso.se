from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import path

if TYPE_CHECKING:
    from django.urls import URLPattern


from webhallen.views import (
    api_list_sections,
    api_product,
    api_products,
    api_products_hugo,
    api_sitemaps_articles,
    api_sitemaps_campaign_lists,
    api_sitemaps_campaigns,
    api_sitemaps_categories,
    api_sitemaps_home,
    api_sitemaps_info_pages,
    api_sitemaps_manufacturers,
    api_sitemaps_products,
    api_sitemaps_root,
    api_sitemaps_sections,
    testboi,
)

urlpatterns: list[URLPattern] = [
    path("api/v1/webhallen/products", api_products),
    path("api/v1/webhallen/products/hugo", api_products_hugo),
    path("api/v1/webhallen/products/<str:product_id>", api_product),
    path("api/v1/webhallen/sections", api_list_sections),
    # Sitemaps
    path("api/v1/webhallen/sitemaps/root", api_sitemaps_root),
    path("api/v1/webhallen/sitemaps/home", api_sitemaps_home),
    path("api/v1/webhallen/sitemaps/sections", api_sitemaps_sections),
    path("api/v1/webhallen/sitemaps/categories", api_sitemaps_categories),
    path("api/v1/webhallen/sitemaps/campaigns", api_sitemaps_campaigns),
    path("api/v1/webhallen/sitemaps/campaign_lists", api_sitemaps_campaign_lists),
    path("api/v1/webhallen/sitemaps/info_pages", api_sitemaps_info_pages),
    path("api/v1/webhallen/sitemaps/products", api_sitemaps_products),
    path("api/v1/webhallen/sitemaps/manufacturers", api_sitemaps_manufacturers),
    path("api/v1/webhallen/sitemaps/articles", api_sitemaps_articles),
    # Debug
    path("testboi", testboi),
]