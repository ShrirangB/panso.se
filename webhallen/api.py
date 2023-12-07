from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from loguru import logger
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

router = Router()


@router.get("/products")
def api_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    products = WebhallenJSON.objects.all()
    products_data: list = []
    for product in products:
        product_json = product.product_json
        if "product" not in product_json:
            logger.error(f"Product {product.product_id} has no product key")
            continue

        products_data.append(product_json["product"])

    return JsonResponse(products_data, safe=False)


@router.get("/products/{product_id}")
def api_product(request: HttpRequest, product_id: str) -> JsonResponse:  # noqa: ARG001
    """Return Webhallen product as JSON."""
    try:
        product = WebhallenJSON.objects.get(product_id=product_id)
    except WebhallenJSON.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    product_json = product.product_json
    product_data = product_json["product"]

    return JsonResponse(product_data, safe=False)


@router.get("/sitemaps/root")
def api_sitemaps_root(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.xml."""
    sitemaps = SitemapRoot.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/home")
def api_sitemaps_home(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.home.xml."""
    sitemaps = SitemapHome.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/sections")
def api_sitemaps_sections(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.section.xml."""
    sitemaps = SitemapSection.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/categories")
def api_sitemaps_categories(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.category.xml."""
    sitemaps = SitemapCategory.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/campaigns")
def api_sitemaps_campaigns(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaign.xml."""
    sitemaps = SitemapCampaign.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/campaign-lists")
def api_sitemaps_campaign_lists(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.campaignList.xml."""
    sitemaps = SitemapCampaignList.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/info-pages")
def api_sitemaps_info_pages(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.infoPages.xml."""
    sitemaps = SitemapInfoPages.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/products")
def api_sitemaps_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.products.xml."""
    sitemaps = SitemapProduct.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)

    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/manufacturers")
def api_sitemaps_manufacturers(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.manufacturer.xml."""
    sitemaps = SitemapManufacturer.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "priority": sitemap.priority,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)
    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sitemaps/articles")
def api_sitemaps_articles(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all URLs from https://www.webhallen.com/sitemap.article.xml."""
    sitemaps = SitemapArticle.objects.all()
    sitemaps_data: list = []
    for sitemap in sitemaps:
        sitemap_data = {
            "loc": sitemap.loc,
            "active": sitemap.active,
            "created": sitemap.created,
            "updated": sitemap.updated,
        }
        sitemaps_data.append(sitemap_data)
    return JsonResponse(sitemaps_data, safe=False)


@router.get("/sections")
def api_list_sections(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all sections."""
    sections = WebhallenSection.objects.all()
    sections_data: list = []
    for section in sections:
        section_data = {
            "section_id": section.section_id,
            "url": section.url,
            "meta_title": section.meta_title,
            "active": section.active,
            "icon": section.icon,
            "icon_url": section.icon_url,
            "name": section.name,
        }
        sections_data.append(section_data)

    return JsonResponse(sections_data, safe=False)
