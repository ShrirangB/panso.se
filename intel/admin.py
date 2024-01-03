from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from intel.models import ArkFilterData, Processor

if TYPE_CHECKING:
    from django.http import HttpRequest


@admin.register(Processor)
class ProcessorModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions.

    We only want to add processors and prevent any modifications or deletions.
    """

    list_display: tuple = (
        "name",
        "product_collection",
        "lithography",
        "total_cores",
        "total_threads",
        "max_turbo_frequency",
        "created",
        "updated",
    )

    def has_delete_permission(  # noqa: PLR6301
        self: ProcessorModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: ProcessorModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False


@admin.register(ArkFilterData)
class ArkFilterDataModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions.

    We only want to add processors and prevent any modifications or deletions.
    """

    # TODO(TheLovinator): #53 Try to find out how to make JSON look nicer in the admin
    # https://github.com/TheLovinator1/panso.se/issues/53
    def has_delete_permission(  # noqa: PLR6301
        self: ArkFilterDataModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: ArkFilterDataModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: Processor | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False
