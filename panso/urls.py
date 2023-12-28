from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path
from django.views.decorators.cache import cache_page

from amd.scraping.processors import get_processor_data
from panso.api import api
from panso.sitemaps import StaticViewSitemap, WebhallenJSONSitemap


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    get_processor_data()

    return JsonResponse(data={"status": "ok"}, status=200, safe=False)


sitemaps: dict[str, type[Sitemap]] = {
    "static": StaticViewSitemap,
    "webhallen": WebhallenJSONSitemap,
}

# TODO: Cache more views.
urlpatterns: list = [
    # /admin/
    # Admin page
    # path(route="admin/", view=admin.site.urls),     # TODO: Re-add admin page.
    # /
    # Home page
    path(
        route="",
        view=include(arg="products.urls"),
    ),
    # /testboi/
    # Testing stuff
    path(
        route="testboi/",
        view=testboi,
    ),
    # /api/v1/
    # API endpoints
    path(
        route="api/v1/",
        view=api.urls,  # type: ignore  # noqa: PGH003
    ),
    # /webhallen/
    # Things scraped from https://www.webhallen.com/
    path(
        route="webhallen/",
        view=include(arg="webhallen.urls"),
    ),
    # /intel/
    # Things scraped from https://ark.intel.com/
    path(
        route="intel/",
        view=include(arg="intel.urls"),
    ),
    # /sitemap.xml
    # Sitemap
    path(
        route="sitemap.xml",
        view=cache_page(timeout=86400)(sitemaps_views.index),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    # /sitemap-webhallen.xml
    # Sitemap for other sections. Add more sections in panso/sitemaps.py
    path(
        route="sitemap-<section>.xml",
        view=cache_page(timeout=86400)(sitemaps_views.sitemap),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
