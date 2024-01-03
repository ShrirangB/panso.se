from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from amd.models import Processor

if TYPE_CHECKING:
    from django.http import HttpRequest


@admin.register(Processor)
class NoDeleteModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions.

    We only want to add processors and prevent any modifications or deletions.
    """

    def has_delete_permission(  # noqa: PLR6301
        self: NoDeleteModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: NoDeleteModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False
