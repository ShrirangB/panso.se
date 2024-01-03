from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

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

if TYPE_CHECKING:
    from django.db import models
    from django.http import HttpRequest


@admin.register(
    SitemapArticle,
    SitemapCampaign,
    SitemapCampaignList,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapManufacturer,
    SitemapProduct,
    SitemapSection,
)
class SitemapModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions for Webhallen Sitemaps.

    We only want to add things and prevent any modifications or deletions.
    """

    list_display = (
        "loc",
        "priority",
        "active",
    )

    def has_delete_permission(  # noqa: PLR6301
        self: SitemapModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: SitemapModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False


@admin.register(SitemapRoot)
class SitemapRootModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions for Webhallen Sitemaps but without priority.

    We only want to add things and prevent any modifications or deletions.
    """

    list_display = (
        "loc",
        "active",
    )

    def has_delete_permission(  # noqa: PLR6301
        self: SitemapRootModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: SitemapRootModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False


@admin.register(WebhallenJSON)
class ProductModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions for WebhallenJSON.

    We only want to add things and prevent any modifications or deletions.
    """

    list_display: tuple = ("product_id", "created", "updated")
    list_display_links: tuple = ("product_id",)
    ordering: tuple = ("-product_id",)

    def has_delete_permission(  # noqa: PLR6301
        self: ProductModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: ProductModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False


@admin.register(WebhallenSection)
class WebhallenSectionModelAdmin(admin.ModelAdmin):
    """ModelAdmin with read-only permissions for Webhallen Sections.

    We only want to add things and prevent any modifications or deletions.
    """

    list_display: tuple = (
        "section_id",
        "meta_title",
        "active",
        "icon",
        "icon_url",
        "name",
        "url",
    )
    list_display_links: tuple = ("section_id",)

    # Sort by section_id (1 -> 19)
    ordering: tuple = ("section_id",)

    def has_delete_permission(  # noqa: PLR6301
        self: WebhallenSectionModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(  # noqa: PLR6301
        self: WebhallenSectionModelAdmin,
        request: HttpRequest,  # noqa: ARG002
        obj: models.Model | None = None,  # noqa: ARG002
    ) -> bool:
        """Disable change permission."""
        return False
