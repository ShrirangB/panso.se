from __future__ import annotations

import datetime

from loguru import logger


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
