"""Where all the URL routes are defined.

Contains the following routes:
    - /admin/
        - Admin page
    - /
        - Home page
    - /api/v1/
        - API endpoints
    - /webhallen/
        - Things scraped from https://www.webhallen.com/
    - /intel/
        - Things scraped from https://ark.intel.com/
    - /sitemap.xml
        - Our main sitemap, contains links to all other sitemaps.
    - /sitemap-webhallen.xml
        - Sitemap for Webhallen. Add more sections in panso/sitemaps.py
    - /testboi/
        - So we can test stuff without creating a new URL route.
See:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from __future__ import annotations

import os

from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path
from django.views.decorators.cache import cache_page

from intel.scrape_intel_ark import get_html, process_html
from panso.api import api
from panso.sitemaps import StaticViewSitemap, WebhallenJSONSitemap


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    for data in get_html():
        process_html(processor_data=data)

    return JsonResponse(data={"status": "ok"}, status=200, safe=False)


sitemaps: dict[str, type[Sitemap]] = {
    "static": StaticViewSitemap,
    "webhallen": WebhallenJSONSitemap,
}

admin_page_path: str = os.getenv(key="ADMIN_PAGE_PATH", default="admin/")

# Remove leading slash if present
admin_page_path = admin_page_path.lstrip("/")

# Add trailing slash if missing
if not admin_page_path.endswith("/"):
    admin_page_path = admin_page_path + "/"

# TODO(TheLovinator): #33 Cache more views.
# https://github.com/TheLovinator1/panso.se/issues/33
urlpatterns: list = [
    # /admin/
    # Admin page
    path(route=admin_page_path, view=admin.site.urls),
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
    # Debug toolbar
    path("__debug__/", include("debug_toolbar.urls")),
]
