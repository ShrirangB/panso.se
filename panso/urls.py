from __future__ import annotations

from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path

from intel.management.commands.scrape_cpus import get_html, get_names
from panso.api import api
from panso.sitemaps import StaticViewSitemap


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    for data in get_html():
        get_names(processor_data=data)
    return JsonResponse({"status": "ok"}, status=200, safe=False)


sitemaps: dict[str, type[StaticViewSitemap]] = {
    "products": StaticViewSitemap,
}

# TODO: Cache views
urlpatterns: list = [
    path(route="admin/", view=admin.site.urls),
    path(route="testboi", view=testboi, name="testboi"),
    path(route="api/", view=api.urls),  # type: ignore  # noqa: PGH003
    path(route="", view=include(arg="products.urls")),
    path(route="webhallen/", view=include(arg="webhallen.urls")),
    path(
        route="sitemap.xml",
        view=sitemaps_views.index,
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        route="sitemap-<section>.xml",
        view=sitemaps_views.sitemap,
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
