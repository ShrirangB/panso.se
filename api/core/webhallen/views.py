from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from loguru import logger

from core.management.commands.rewrite_webhallen import convert_json_to_model
from core.webhallen.models import WebhallenJSON, WebhallenProduct


@require_http_methods(["GET"])
def list_products(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    logger.info("Webhallen list view called")

    products = WebhallenJSON.objects.all()
    products_data: list = []
    for product in products:
        product_json = product.product_json
        products_data.append(product_json["product"])

    return JsonResponse(products_data, safe=False)


@require_http_methods(["GET"])
def list_products_hugo(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all Webhallen products as JSON."""
    products = WebhallenProduct.objects.all()
    products_data: list = []
    for product in products:
        product_json = {
            "product_id": product.product_id,
            "minimum_rank_level": product.minimum_rank_level,
            "images_zoom": product.images_zoom,
            "images_large": product.images_large,
            "images_thumb": product.images_thumb,
            "name": product.name,
            "price": product.price,
            "vat": product.vat,
            "price_end_at": product.price_end_at,
            "price_nearly_over": product.price_nearly_over,
            "price_flash_sale": product.price_flash_sale,
            "price_type": product.price_type,
            "regular_price": product.regular_price,
            "regular_price_type": product.regular_price_type,
            "regular_price_end_at": product.regular_price_end_at,
            "regular_price_nearly_over": product.regular_price_nearly_over,
            "regular_price_flash_sale": product.regular_price_flash_sale,
            "lowest_price": product.lowest_price,
            "lowest_price_type": product.lowest_price_type,
            "lowest_price_end_at": product.lowest_price_end_at,
            "lowest_price_nearly_over": product.lowest_price_nearly_over,
            "lowest_price_flash_sale": product.lowest_price_flash_sale,
            "level_one_price": product.level_one_price,
            "level_one_price_type": product.level_one_price_type,
            "level_one_price_end_at": product.level_one_price_end_at,
            "level_one_price_nearly_over": product.level_one_price_nearly_over,
            "level_one_price_flash_sale": product.level_one_price_flash_sale,
            "description": product.description,
            "meta_title": product.meta_title,
            "meta_description": product.meta_description,
            "canonical_url": product.canonical_url,
            "release_date": product.release_date,
            "section_id": product.section_id,
            "is_digital": product.is_digital,
            "discontinued": product.discontinued,
            "category_tree": product.category_tree,
            "main_category_path": product.main_category_path,
            "manufacturer": product.manufacturer,
            "part_numbers": product.part_numbers,
            "eans": product.eans,
            "thumbnail": product.thumbnail,
            "average_rating": product.average_rating,
            "average_rating_type": product.average_rating_type,
            "energy_marking_rating": product.energy_marking_rating,
            "energy_marking_label": product.energy_marking_label,
            "package_size_id": product.package_size_id,
            "status_codes": product.status_codes,
            "long_delivery_notice": product.long_delivery_notice,
            "categories": product.categories,
            "phone_subscription": product.phone_subscription,
            "highlighted_review_id": product.highlighted_review_id,
            "highlighted_review_text": product.highlighted_review_text,
            "highlighted_review_rating": product.highlighted_review_rating,
            "highlighted_review_upvotes": product.highlighted_review_upvotes,
            "highlighted_review_downvotes": product.highlighted_review_downvotes,
            "highlighted_review_verified": product.highlighted_review_verified,
            "highlighted_review_created": product.highlighted_review_created,
            "highlighted_review_is_anonymous": product.highlighted_review_is_anonymous,
            "highlighted_review_is_employee": product.highlighted_review_is_employee,
            "highlighted_review_product_id": product.highlighted_review_product_id,
            "highlighted_review_user_id": product.highlighted_review_user_id,
            "highlighted_review_is_hype": product.highlighted_review_is_hype,
            "is_fyndware": product.is_fyndware,
            "fyndware_of": product.fyndware_of,
            "fyndware_of_description": product.fyndware_of_description,
            "fyndware_class": product.fyndware_class,
            "main_title": product.main_title,
            "sub_title": product.sub_title,
            "is_shippable": product.is_shippable,
            "is_collectable": product.is_collectable,
            "excluded_shipping_methods": product.excluded_shipping_methods,
            "insurance_id": product.insurance_id,
            "possible_delivery_methods": product.possible_delivery_methods,
        }
        # Loop through the dict and remove all None values
        for key, value in list(product_json.items()):
            if value is None:
                del product_json[key]

        products_data.append(product_json)

    return JsonResponse(products_data, safe=False)


@require_http_methods(["GET"])
def list_product(request: HttpRequest, product_id: str) -> JsonResponse:  # noqa: ARG001
    """Return Webhallen product as JSON."""
    logger.info(f"Webhallen product view called for {product_id}")

    # Get product from database or 404
    try:
        product = WebhallenJSON.objects.get(product_id=product_id)
    except WebhallenJSON.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    product_json = product.product_json
    product_data = product_json["product"]

    return JsonResponse(product_data, safe=False)


@require_http_methods(["GET"])
def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    convert_json_to_model()
    return JsonResponse({"status": "ok"})