from __future__ import annotations

import datetime

from django.core.management.base import BaseCommand, CommandError
from loguru import logger

from core.stores.webhallen.models import WebhallenJSON, WebhallenProduct


def make_datetime_from_timestamp(date_string: str | None) -> datetime.datetime | None:
    """Convert a date to a datetime.

    Args:
        date_string: Datetime as string. For example: "2024-02-22T01:13:46"

    Returns:
        datetime.datetime: Datetime or None if timestamp is empty or fucked
    """
    if not date_string:
        return None

    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").astimezone(tz=datetime.UTC)


def convert_timestamp_to_datetime(timestamp: int | None, date_format: str | None) -> str:  # noqa: PLR0911
    """Convert a timestamp to a datetime.

    Example:
        timestamp=1704059999, format="Y" -> 2023
        timestamp=1686110400, format="Y-m-d" -> 2023-06-07

    Args:
        timestamp: Unix timestamp
        date_format: Format shown on website

    Returns:
        The parsed date
    """
    if not timestamp or timestamp == 0:
        return ""

    if not date_format:
        return ""

    if timestamp == -62169966000:  # noqa: PLR2004
        # Seems to be 0000-00-00 00:00:00?
        return ""

    if date_format == "Y":
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC).strftime("%Y")

    if date_format == "Y-m-d":
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC).strftime("%Y-%m-%d")

    if date_format == "M Y":
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC).strftime("%B %Y")

    if date_format == "Q \\k\\v\\a\\r\\t\\a\\l\\e\\t Y":
        # TODO: Implement this
        logger.error("For example: 2:a kvartalet 2018 ")
    logger.error(f"Unknown date format: {date_format}")
    return ""


def make_thumbnail_url(url: str | None) -> str | None:
    """Make a thumbnail URL from a URL.

    Args:
        url (str): URL

    Returns:
        str: Thumbnail URL
    """
    if url:
        return f"https://www.webhallen.com{url}"
    return None


def get_image_list_zoom(product_json: dict) -> str | None:
    """Get a list of zoom images.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of zoom images
    """
    images: list = product_json.get("images", [])
    images_list_zoom: str | None = ""
    for image in images:
        image: dict
        zoom_url: str | None = image.get("zoom")
        if zoom_url:
            images_list_zoom += f"https://www.webhallen.com{zoom_url},"
    return images_list_zoom.rstrip(",") or None


def get_image_list_large(product_json: dict) -> str | None:
    """Get a list of large images.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of large images
    """
    images: list = product_json.get("images", [])
    images_list_large: str | None = ""
    for image in images:
        image: dict
        large_url: str | None = image.get("large")
        if large_url:
            images_list_large += f"https://www.webhallen.com{large_url},"
    return images_list_large.rstrip(",") or None


def get_image_list_thumb(product_json: dict) -> str | None:
    """Get a list of thumbnail images.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of thumbnail images
    """
    images: list = product_json.get("images", [])
    images_list_thumb: str | None = ""
    for image in images:
        image: dict
        thumb_url: str | None = image.get("thumb")
        if thumb_url:
            images_list_thumb += f"https://www.webhallen.com{thumb_url},"
    return images_list_thumb.rstrip(",") or None


def get_status_codes(product_json: dict) -> str | None:
    """Get a list of status codes.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of status codes
    """
    status_codes_list: list = product_json.get("statusCodes", [])
    status_codes: str | None = ""
    for status_code in status_codes_list:
        status_codes += f"{status_code},"
    return status_codes.rstrip(",") or None


def get_part_numbers(product_json: dict) -> str | None:
    """Get a list of part numbers.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of part numbers
    """
    part_numbers_list: list = product_json.get("partNumbers", [])
    part_numbers: str | None = ""
    for part_number in part_numbers_list:
        part_numbers += f"{part_number},"
    return part_numbers.rstrip(",") or None


def get_eans(product_json: dict) -> str | None:
    """Get a list of EANs.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of EANs
    """
    eans_list: list = product_json.get("eans", [])
    eans: str | None = ""
    for ean in eans_list:
        eans += f"{ean},"
    return eans.rstrip(",") or None


def get_main_category_path(product_json: dict) -> str | None:
    """Get a list of main category paths.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of main category paths
    """
    main_category_path_list: list = product_json.get("mainCategoryPath", [])
    main_category_path: str | None = ""
    for main_category in main_category_path_list:
        main_category_path += f"{main_category.get('id')},"
    return main_category_path.rstrip(",") or None


def get_possible_delivery_methods(product_json: dict) -> str | None:
    """Get a list of possible delivery methods.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of possible delivery methods
    """
    possible_delivery_methods_list: list = product_json.get("possible_delivery_methods", [])
    possible_delivery_methods: str | None = ""
    for possible_delivery_method in possible_delivery_methods_list:
        possible_delivery_methods += f"{possible_delivery_method},"
    return possible_delivery_methods.rstrip(",") or None


def get_categories(product_json: dict) -> str | None:
    """Get a list of categories.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of categories
    """
    categories_list: list = product_json.get("categories", [])
    categories: str | None = ""
    for category in categories_list:
        categories += f"{category.get('id')},"
    return categories.rstrip(",") or None


def get_manufacturer(product_json: dict) -> str | None:
    """Get a list of manufacturers.

    Args:
        product_json: Product JSON

    Returns:
        str: Comma separated list of manufacturers
    """
    manufacturer_json: dict = product_json.get("manufacturer", {})
    manufacturer: int | None = None
    if manufacturer_json:
        manufacturer: int | None = manufacturer_json.get("id")
    return manufacturer


def convert_json_to_model() -> None:  # noqa: C901, PLR0912, PLR0915
    """Convert Webhallen product JSON to a Django model."""
    for json in WebhallenJSON.objects.all():
        product_json = dict(json.product_json)
        product_json: dict = product_json.get("product", {})
        if not product_json:
            logger.error(f"Error getting product JSON {json.product_id}")
            continue

        product_id: int | None = product_json.get("id")
        if not product_id:
            logger.error(f"Error getting product ID {json.product_id}")
            continue

        images_list_zoom: str | None = get_image_list_zoom(product_json)
        images_list_large: str | None = get_image_list_large(product_json)
        images_list_thumb: str | None = get_image_list_thumb(product_json)
        status_codes: str | None = get_status_codes(product_json)
        part_numbers: str | None = get_part_numbers(product_json)
        eans: str | None = get_eans(product_json)
        main_category_path: str | None = get_main_category_path(product_json)
        possible_delivery_methods: str | None = get_possible_delivery_methods(product_json)
        categories: str | None = get_categories(product_json)
        manufacturer: str | None = get_manufacturer(product_json)

        defaults: dict = {
            "minimum_rank_level": product_json.get("minimumRankLevel"),
            "images_zoom": images_list_zoom,
            "images_large": images_list_large,
            "images_thumb": images_list_thumb,
            "name": product_json.get("name"),
            "description": product_json.get("description"),
            "meta_title": product_json.get("metaTitle"),
            "meta_description": product_json.get("metaDescription"),
            "canonical_url": product_json.get("canonicalUrl"),
            "is_digital": product_json.get("isDigital"),
            "discontinued": product_json.get("discontinued"),
            "category_tree": product_json.get("categoryTree"),
            "main_category_path": main_category_path,
            "manufacturer": manufacturer,
            "part_numbers": part_numbers,
            "eans": eans,
            "thumbnail": make_thumbnail_url(product_json.get("thumbnail")),
            "package_size_id": product_json.get("packageSizeId"),
            "status_codes": status_codes,
            "long_delivery_notice": product_json.get("longDeliveryNotice"),
            "categories": categories,
            "phone_subscription": product_json.get("phoneSubscription"),
            "is_fyndware": product_json.get("isFyndware"),
            "main_title": product_json.get("mainTitle"),
            "sub_title": product_json.get("subTitle"),
            "is_shippable": product_json.get("isShippable"),
            "is_collectable": product_json.get("isCollectable"),
            "possible_delivery_methods": possible_delivery_methods,
        }

        lowest_price: dict = product_json.get("lowestPrice", {})
        if lowest_price:
            defaults["lowest_price"] = lowest_price.get("price")
            defaults["lowest_price_type"] = lowest_price.get("type")
            defaults["lowest_price_end_at"] = make_datetime_from_timestamp(lowest_price.get("endAt"))
            defaults["lowest_price_nearly_over"] = lowest_price.get("nearlyOver", False)
            defaults["lowest_price_flash_sale"] = lowest_price.get("flashSale", False)

        regular_price: dict = product_json.get("regularPrice", {})
        if regular_price:
            defaults["regular_price"] = regular_price.get("price")
            defaults["regular_price_type"] = regular_price.get("type")
            defaults["regular_price_end_at"] = make_datetime_from_timestamp(regular_price.get("endAt"))
            defaults["regular_price_nearly_over"] = regular_price.get("nearlyOver", False)
            defaults["regular_price_flash_sale"] = regular_price.get("flashSale", False)

        level_one_price: dict = product_json.get("levelOnePrice", {})
        if level_one_price:
            defaults["level_one_price"] = level_one_price.get("price")
            defaults["level_one_price_type"] = level_one_price.get("type")
            defaults["level_one_price_end_at"] = make_datetime_from_timestamp(level_one_price.get("endAt"))
            defaults["level_one_price_nearly_over"] = level_one_price.get("nearlyOver", False)
            defaults["level_one_price_flash_sale"] = level_one_price.get("flashSale", False)

        review_highlight: dict = product_json.get("reviewHighlight", {})
        if review_highlight:
            review_highlight_product: dict = review_highlight.get("product", {})
            review_highlight_user: dict = review_highlight.get("user", {})
            if review_highlight_user:
                defaults["highlighted_review_user_id"] = review_highlight_user.get("id")
            elif review_highlight.get("isAnonymous"):
                defaults["highlighted_review_user_id"] = "Anonymous"

            defaults["highlighted_review_id"] = review_highlight.get("id")
            defaults["highlighted_review_text"] = review_highlight.get("text")
            defaults["highlighted_review_rating"] = review_highlight.get("rating")
            defaults["highlighted_review_upvotes"] = review_highlight.get("upvotes")
            defaults["highlighted_review_downvotes"] = review_highlight.get("downvotes")
            defaults["highlighted_review_verified"] = review_highlight.get("verified", False)
            defaults["highlighted_review_created"] = make_datetime_from_timestamp(review_highlight.get("created"))
            defaults["highlighted_review_is_anonymous"] = review_highlight.get("isAnonymous", False)
            defaults["highlighted_review_is_employee"] = review_highlight.get("isEmployee", False)
            defaults["highlighted_review_product_id"] = review_highlight_product.get("id")

            defaults["highlighted_review_is_hype"] = review_highlight.get("isHype", False)

        energy_marking: dict = product_json.get("energyMarking", {})
        if energy_marking:
            defaults["energy_marking_rating"] = energy_marking.get("rating")
            defaults["energy_marking_label"] = energy_marking.get("label")

        average_rating: dict = product_json.get("averageRating", {})
        if average_rating:
            defaults["average_rating"] = average_rating.get("rating")
            defaults["average_rating_type"] = average_rating.get("type")

        meta: dict = product_json.get("meta", {})
        if meta:
            defaults["excluded_shipping_methods"] = ",".join(meta.get("excluded_shipping_methods", []))

        fyndware_of: dict = product_json.get("fyndwareOf", {})
        if fyndware_of:
            defaults["fyndware_of"] = fyndware_of.get("id")
            defaults["fyndware_of_description"] = fyndware_of.get("description")

        fyndware_class: dict = product_json.get("fyndwareClass", {})
        if fyndware_class:
            defaults["fyndware_class"] = fyndware_class.get("id")

        price: dict = product_json.get("price", {})
        if price:
            defaults["price"] = price.get("price")
            defaults["vat"] = price.get("vat")
            defaults["price_type"] = price.get("type")
            defaults["price_end_at"] = make_datetime_from_timestamp(price.get("endAt"))
            defaults["price_nearly_over"] = price.get("nearlyOver", False)
            defaults["price_flash_sale"] = price.get("flashSale", False)

        release: dict = product_json.get("release", {})
        if release:
            defaults["release_date"] = convert_timestamp_to_datetime(release.get("timestamp"), release.get("format"))

        insurance: dict = product_json.get("insurance", {})
        if insurance:
            defaults["insurance_id"] = insurance.get("id")

        section: dict = product_json.get("section", {})
        if section:
            defaults["section_id"] = section.get("id")

        obj: WebhallenProduct
        obj, _ = WebhallenProduct.objects.update_or_create(product_id=product_id, defaults=defaults)

        obj.save()


class Command(BaseCommand):
    """Convert our JSON data a Django model."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            convert_json_to_model()
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while converting JSON to model"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e


if __name__ == "__main__":
    convert_json_to_model()
