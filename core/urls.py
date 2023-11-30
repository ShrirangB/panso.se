from __future__ import annotations

from django.contrib import admin
from django.urls import URLResolver, path

from core.api import api

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # type: ignore  # noqa: PGH003
]
