from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from webhallen.models import (
    SitemapArticle,
    SitemapCampaign,
    SitemapCampaignList,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapManufacturer,
    SitemapProduct,
    SitemapRoot,
    SitemapSection,
    WebhallenJSON,
    WebhallenSection,
)

if TYPE_CHECKING:
    from datetime import datetime

    from django.db import models

router = Router()


@router.get("/products")
def api_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    products_data = list(
        WebhallenJSON.objects.values_list("product_json__product", flat=True).filter(
            product_json__product__isnull=False,
        ),
    )
    return JsonResponse(products_data, safe=False)


@router.get("/products/{product_id}")
def api_product(request: HttpRequest, product_id: str) -> JsonResponse:  # noqa: ARG001
    """Return Webhallen product as JSON."""
    try:
        product: WebhallenJSON = get_object_or_404(WebhallenJSON, product_id=product_id)
        product_json = product.product_json
        product_data = product_json.get("product", {})
        return JsonResponse(product_data, safe=False)
    except Http404:
        return JsonResponse({"error": f"Product with ID {product_id} not found."}, status=404)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=500)


@router.get("/sitemaps/root")
def api_sitemaps_root(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.xml."""
    sitemaps_data = list(SitemapRoot.objects.values("loc", "active", "created", "updated"))
    return JsonResponse(sitemaps_data, safe=False)


def get_sitemap_data(model: type[models.Model]) -> list[dict[str, str | datetime]]:
    """Return all URLs from https://www.webhallen.com/sitemap.{sitemap}.xml.

    Args:
        model: Sitemap model.

    Returns:
        list[dict[str, str | datetime]]: Sitemap data.
    """
    return list(model.objects.values("loc", "priority", "active", "created", "updated"))


@router.get("/sitemaps/home")
def api_sitemaps_home(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.home.xml."""
    return JsonResponse(get_sitemap_data(SitemapHome), safe=False)


@router.get("/sitemaps/sections")
def api_sitemaps_sections(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.section.xml."""
    return JsonResponse(get_sitemap_data(SitemapSection), safe=False)


@router.get("/sitemaps/categories")
def api_sitemaps_categories(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.category.xml."""
    return JsonResponse(get_sitemap_data(SitemapCategory), safe=False)


@router.get("/sitemaps/campaigns")
def api_sitemaps_campaigns(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaign.xml."""
    return JsonResponse(get_sitemap_data(SitemapCampaign), safe=False)


@router.get("/sitemaps/campaign-lists")
def api_sitemaps_campaign_lists(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaignList.xml."""
    return JsonResponse(get_sitemap_data(SitemapCampaignList), safe=False)


@router.get("/sitemaps/info-pages")
def api_sitemaps_info_pages(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.infoPages.xml."""
    return JsonResponse(get_sitemap_data(SitemapInfoPages), safe=False)


@router.get("/sitemaps/products")
def api_sitemaps_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.products.xml."""
    return JsonResponse(get_sitemap_data(SitemapProduct), safe=False)


@router.get("/sitemaps/manufacturers")
def api_sitemaps_manufacturers(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.manufacturer.xml."""
    return JsonResponse(get_sitemap_data(SitemapManufacturer), safe=False)


@router.get("/sitemaps/articles")
def api_sitemaps_articles(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.article.xml."""
    return JsonResponse(get_sitemap_data(SitemapArticle), safe=False)


@router.get("/sections")
def api_list_sections(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all sections."""
    sections_data = list(
        WebhallenSection.objects.values(
            "section_id",
            "url",
            "meta_title",
            "active",
            "icon",
            "icon_url",
            "name",
        ),
    )
    return JsonResponse(sections_data, safe=False)
