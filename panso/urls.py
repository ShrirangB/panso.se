from __future__ import annotations

from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path

from panso.api import api
from panso.sitemaps import StaticViewSitemap
from products.management.commands.add_eans import create_eans


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    create_eans()
    return JsonResponse({"status": "ok"})


sitemaps: dict[str, type[StaticViewSitemap]] = {
    "pages": StaticViewSitemap,
}

# TODO: Cache views
urlpatterns: list = [
    path("admin/", admin.site.urls),
    path("testboi", testboi, name="testboi"),
    path("api/", api.urls),  # type: ignore  # noqa: PGH003
    path("", include("pages.urls")),
    path("webhallen/", include("webhallen.urls")),
    path(
        "sitemap.xml",
        sitemaps_views.index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        sitemaps_views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
