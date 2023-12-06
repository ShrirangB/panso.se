from __future__ import annotations

from django.contrib import admin
from django.urls import URLResolver, include, path

from panso.api import api

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # type: ignore  # noqa: PGH003
    path("", include("pages.urls")),
    path("webhallen/", include("webhallen.urls")),
]
