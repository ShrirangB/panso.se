from __future__ import annotations

import datetime


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
