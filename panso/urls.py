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

from cacheops import cached_view, cached_view_as
from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpRequest, JsonResponse
from django.urls import include, path
from django.utils.text import slugify

from intel.models import Processor
from panso.api import api
from panso.sitemaps import IntelProcessorSitemap, StaticViewSitemap, WebhallenJSONSitemap
from webhallen.models.json import WebhallenJSON


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    # Update the slug field using the slugify function
    processors_to_update: list[Processor] = []
    for processor in Processor.objects.filter(slug="fname"):
        processor_name: str = processor.name or "Unknown processor"
        processor.slug = slugify(processor_name)
        processors_to_update.append(processor)

    Processor.objects.bulk_update(processors_to_update, fields=["slug"])

    return JsonResponse(data={"status": "ok"}, status=200, safe=False)


sitemaps: dict[str, type[Sitemap]] = {
    "static": StaticViewSitemap,
    "webhallen": WebhallenJSONSitemap,
    "intel": IntelProcessorSitemap,
}

admin_page_path: str = os.getenv(key="ADMIN_PAGE_PATH", default="admin/")

# Remove leading slash if present
admin_page_path = admin_page_path.lstrip("/")

# Add trailing slash if missing
if not admin_page_path.endswith("/"):
    admin_page_path = admin_page_path + "/"

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
        view=cached_view()(sitemaps_views.index),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    # /sitemap-webhallen.xml
    # Sitemap for other sections. Add more sections in panso/sitemaps.py
    path(
        route="sitemap-<section>.xml",
        view=cached_view_as(WebhallenJSON, Processor)(sitemaps_views.sitemap),
        kwargs={"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Debug toolbar
    path("__debug__/", include("debug_toolbar.urls")),
]
