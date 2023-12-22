from __future__ import annotations

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path
from django.views.decorators.cache import cache_page

from intel.management.commands.scrape_cpus import get_html, process_html
from panso.api import api
from panso.sitemaps import StaticViewSitemap, WebhallenJSONSitemap


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    for data in get_html():
        process_html(processor_data=data)
        break
    return JsonResponse({"status": "ok"}, status=200, safe=False)


sitemaps: dict[str, type[Sitemap]] = {
    "static": StaticViewSitemap,
    "webhallen": WebhallenJSONSitemap,
}

# TODO: Cache views
urlpatterns: list = [
    # path(route="admin/", view=admin.site.urls),     # TODO: Re-add admin page.
    path(route="", view=include(arg="products.urls")),
    path(route="api/v1/", view=api.urls),  # type: ignore  # noqa: PGH003
    path(route="webhallen/", view=include(arg="webhallen.urls")),
    path(route="intel/", view=include(arg="intel.urls")),
    path(
        route="sitemap.xml",
        view=cache_page(timeout=86400)(sitemaps_views.index),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        route="sitemap-<section>.xml",
        view=cache_page(timeout=86400)(sitemaps_views.sitemap),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(route="testboi/", view=testboi),
    ]
