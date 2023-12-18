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


@router.get(
    path="/products",
    summary="Return all Webhallen products as JSON.",
    description="Return all Webhallen products as JSON.\n\n **Note:** This will return 130 MB+ of JSON so don't try to load this via the Swagger UI.",  # noqa: E501
)
def api_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    products_data = list(
        WebhallenJSON.objects.values_list("product_json__product", flat=True).filter(
            product_json__product__isnull=False,
        ),
    )
    return JsonResponse(data=products_data, safe=False)


@router.get(path="/products/{product_id}")
def api_product(request: HttpRequest, product_id: str) -> JsonResponse:  # noqa: ARG001
    """Return Webhallen product as JSON."""
    try:
        product: WebhallenJSON = get_object_or_404(WebhallenJSON, product_id=product_id)
        product_json = product.product_json
        product_data = product_json.get("product", {})
        return JsonResponse(product_data, safe=False)
    except Http404:
        return JsonResponse(data={"error": f"Product with ID {product_id} not found."}, status=404)
    except Exception as e:  # noqa: BLE001
        return JsonResponse(data={"error": str(e)}, status=500)


@router.get(path="/sitemaps/root")
def api_sitemaps_root(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.xml."""
    sitemaps_data = list(SitemapRoot.objects.values("loc", "active", "created", "updated"))
    return JsonResponse(data=sitemaps_data, safe=False)


def get_sitemap_data(model: type[models.Model]) -> list[dict[str, str | datetime]]:
    """Return all URLs from https://www.webhallen.com/sitemap.{sitemap}.xml.

    Args:
        model: Sitemap model.

    Returns:
        list[dict[str, str | datetime]]: Sitemap data.
    """
    return list(model.objects.values("loc", "priority", "active", "created", "updated"))


@router.get(path="/sitemaps/home")
def api_sitemaps_home(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.home.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapHome), safe=False)


@router.get(path="/sitemaps/sections")
def api_sitemaps_sections(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.section.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapSection), safe=False)


@router.get(path="/sitemaps/categories")
def api_sitemaps_categories(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.category.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapCategory), safe=False)


@router.get(path="/sitemaps/campaigns")
def api_sitemaps_campaigns(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaign.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapCampaign), safe=False)


@router.get(path="/sitemaps/campaign-lists")
def api_sitemaps_campaign_lists(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaignList.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapCampaignList), safe=False)


@router.get(path="/sitemaps/info-pages")
def api_sitemaps_info_pages(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.infoPages.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapInfoPages), safe=False)


@router.get(path="/sitemaps/products")
def api_sitemaps_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.products.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapProduct), safe=False)


@router.get(path="/sitemaps/manufacturers")
def api_sitemaps_manufacturers(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.manufacturer.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapManufacturer), safe=False)


@router.get(path="/sitemaps/articles")
def api_sitemaps_articles(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.article.xml."""
    return JsonResponse(data=get_sitemap_data(model=SitemapArticle), safe=False)


@router.get(path="/sections")
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
    return JsonResponse(data=sections_data, safe=False)
