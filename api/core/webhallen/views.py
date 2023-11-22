from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from loguru import logger

from core.webhallen.models import Webhallen


@require_http_methods(["GET"])
@cache_page(60 * 60 * 24)
def list_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    logger.info("Webhallen list view called")

    products = Webhallen.objects.all()
    products_data: list = []
    for product in products:
        product_json = product.product_json
        products_data.append(product_json["product"])

    return JsonResponse(products_data, safe=False)


@require_http_methods(["GET"])
def list_product(request: HttpRequest, product_id: str) -> JsonResponse:  # noqa: ARG001
    """Return Webhallen product as JSON."""
    logger.info(f"Webhallen product view called for {product_id}")

    # Get product from database or 404
    try:
        product = Webhallen.objects.get(product_id=product_id)
    except Webhallen.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    product_json = product.product_json
    product_data = product_json["product"]

    return JsonResponse(product_data, safe=False)
