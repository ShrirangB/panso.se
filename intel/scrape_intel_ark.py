"""Scrape Intel ARK and create/update a database entry for each processor."""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import batched
from typing import TYPE_CHECKING, Any

import dateparser
import hishel
from django.db import Error, transaction
from rich import print
from rich.console import Console
from rich.progress import track
from selectolax.lexbor import LexborHTMLParser, LexborNode

from data_converters import (
    bandwidth_to_bandwidth,
    bit_to_bit,
    bool_to_bool,
    bytes_to_bytes,
    dollar_to_cents,
    float_to_float,
    hertz_an_hertz,
    temp_to_temp,
    watt_to_watt,
)
from intel._product_ids import product_ids
from intel.data_mappings import (
    bandwidth_bois,
    bit_bois,
    byte_bois,
    float_bois,
    hertz_bois,
    int_bois,
    mapping,
    temp_bois,
    watt_bois,
)
from intel.models import Processor

if TYPE_CHECKING:
    from collections.abc import Callable, Generator
    from datetime import datetime

    from httpx import Response


storage = hishel.FileStorage(ttl=60 * 60 * 24 * 7)  # 1 week
err_console = Console(stderr=True)


@dataclass(frozen=True)
class ProcessorData:
    """Data about a processor."""

    html: str
    ids: str


def get_html() -> Generator[ProcessorData, Any, None]:
    """Get the HTML from Intel ARK so we can parse it."""
    for batch in list(batched(product_ids, 100)):
        ids: str = ",".join(batch)
        url: str = f"https://www.intel.com/content/www/us/en/products/compare.html?productIds={ids}"
        print(f"Visiting {url}")
        with hishel.CacheClient(storage=storage) as client:
            response: Response = client.get(url=url, timeout=60)
            processor_data: ProcessorData = ProcessorData(html=response.text, ids=ids)
            yield processor_data


def get_recommended_customer_price(node_attributes: dict[str, str | None]) -> int | None:
    """Get the recommended customer price.

    Args:
        node_attributes: The attributes of the node.

    Returns:
        int: The recommended customer price.
    """
    if "class" in node_attributes:
        # TODO(TheLovinator): #34 Fix this for $294.00-$304.00
        # https://github.com/TheLovinator1/panso.se/issues/34
        class_value: str | None = node_attributes["class"]
        price_regex = r"\$\d+.\d+"
        if class_value and class_value.startswith("$") and re.match(pattern=price_regex, string=class_value):
            price: int | None = dollar_to_cents(d=class_value)
            return price
    return None


def get_data_from_html(html: str, _id: str) -> list[LexborNode] | None:
    """Get the data from the HTML.

    Args:
        html: The HTML from Intel ARK.
        _id: The ID of the processor.

    Returns:
        list[LexborNode]: The data from the HTML.
    """
    parser: LexborHTMLParser = LexborHTMLParser(html=html)
    selector: str = f'[data-product-id="{_id}"]'
    data: list[LexborNode] = parser.css(selector)
    if not data:
        print(f"Could not find {_id}")
        return None
    return data


def get_esu_date(node: LexborNode) -> datetime | None:
    """Get the ESU date.

    Extended Security Updates (ESU) date is the date when the processor will no longer receive security updates.

    Args:
        node: The node.

    Returns:
        datetime: The ESU date.
    """
    date_string: str | None = node.text(strip=True) or None
    if date_string:
        parsed_date: datetime | None = dateparser.parse(
            date_string=date_string,
            languages=["en"],
            settings={"PREFER_DAY_OF_MONTH": "first"},
        )
        if parsed_date:
            return parsed_date
    return None


def convert_and_set_value(
    data_key: str,
    data_dict: dict,
    node: LexborNode,
    conversion_function: Callable[[str], Any],
    defaults: dict,
) -> dict:
    """Convert and set a value.

    Args:
        data_key: Data key on the product page.
        data_dict: Our dictionary with data keys. (e.g. float_bois. Can be found above.)
        node: The node.
        conversion_function: The function to convert the value.
        defaults: The defaults. This is the data we will add to the database.

    Returns:
        dict: The defaults but with the new value.
    """
    if data_key in data_dict:
        key: str = data_dict[data_key]
        value: str | None = node.text(strip=True) or None
        if value:
            defaults[key] = conversion_function(value)
    return defaults


def get_data_keys(node: LexborNode, _id: str, defaults: dict) -> dict:
    """Get the data keys.

    Args:
        node: The node.
        _id: The ID of the processor.
        defaults: The defaults.

    Returns:
        dict: The defaults.
    """
    # TODO(TheLovinator): #36 Add OnDemandAvailableUpgrade
    # https://github.com/TheLovinator1/panso.se/issues/36

    # TODO(TheLovinator): #38 We should check if we are missing any data keys on the product page or if we have empty values in our model. # noqa: E501
    # https://github.com/TheLovinator1/panso.se/issues/38
    if "data-key" not in node.attributes:
        return defaults

    node_attributes: dict[str, str | None] = node.attributes
    data_key: str | None = node_attributes["data-key"]

    if not data_key:
        err_console.print(f"Could not find data-key for {_id}")
        return defaults

    if data_key == "ESUDate":
        defaults["end_of_servicing_updates_date"] = get_esu_date(node=node)

    # Get string values
    if data_key in mapping:
        key: str = mapping[data_key]
        value: str | None = node.text(strip=True) or None
        if value:
            defaults[key] = value
        return defaults

    # Placeholder so we don't get errors that we have unused imports.
    _: tuple = (bandwidth_bois, bit_bois, byte_bois, hertz_bois, int_bois, mapping, temp_bois, watt_bois, float_bois)

    # Run these functions on each boi
    conversion_functions: dict[str, Callable] = {
        "float_bois": float_to_float,
        "temp_bois": temp_to_temp,
        "bandwidth_bois": bandwidth_to_bandwidth,
        "byte_bois": bytes_to_bytes,
        "bool_bois": bool_to_bool,
        "watt_bois": watt_to_watt,
        "hertz_bois": hertz_an_hertz,
        "bit_bois": bit_to_bit,
    }

    for data_dict_name, conversion_function in conversion_functions.items():
        defaults = convert_and_set_value(
            data_key=data_key,
            data_dict=globals()[data_dict_name],
            node=node,
            conversion_function=conversion_function,
            defaults=defaults,
        )

    # Get int values
    if data_key in int_bois:
        key: str = int_bois[data_key]
        value: str | None = node.text(strip=True) or None
        if value:
            defaults[key] = int(value)

    return defaults


def remove_shit(defaults: dict) -> dict:
    """Remove unnecessary things from a string."""
    for key, value in defaults.items():
        if value and isinstance(value, str):
            defaults[key] = value.replace("®", "")
            defaults[key] = value.replace("™", "")
            defaults[key] = value.replace("©", "")
            defaults[key] = value.replace("  ", " ")
            defaults[key] = value.strip()

    return defaults


def get_processor_name(node: LexborNode) -> str | None:
    """Get the processor name from the product page."""
    arkproductlink: LexborNode | None = node.css_first('[data-component="arkproductlink"]')
    if arkproductlink:
        name: str = arkproductlink.text(strip=True)
        return name.replace("Processor", "")
    return None


def process_html(processor_data: ProcessorData) -> None:
    """Process the HTML from Intel ARK.

    Args:
        processor_data: The data about the processor.
    """
    for _id in track(sequence=processor_data.ids.split(sep=","), description="Processing HTML..."):
        print(f"Processing {_id}")

        # This is the data we will add to the database.
        defaults: dict = {}

        # Get the data from the HTML
        data: list[LexborNode] | None = get_data_from_html(html=processor_data.html, _id=_id)
        if not data:
            continue

        for node in data:
            if not node.attributes:
                err_console.print(f"Could not find attributes for {_id}")
                continue

            defaults["name"] = get_processor_name(node=node)
            defaults["recommended_customer_price"] = get_recommended_customer_price(node_attributes=node.attributes)

            defaults = get_data_keys(node=node, _id=_id, defaults=defaults)

            defaults = remove_shit(defaults=defaults)

            # Add the data to the database
            try:
                with transaction.atomic():
                    processor, created = Processor.objects.update_or_create(product_id=_id, defaults=defaults)
                    if created:
                        # TODO(TheLovinator): #37 Send email/Discord message
                        # https://github.com/TheLovinator1/panso.se/issues/37
                        print(f"Added {processor}")
            except Error as e:
                print(f"Could not add {_id}")
                print(e)
                continue
