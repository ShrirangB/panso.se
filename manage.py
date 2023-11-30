#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415
    except ImportError as exc:
        msg = "Couldn't import Django. Have you run `poetry install`?"
        raise ImportError(msg) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
