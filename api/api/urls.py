from __future__ import annotations

from django.contrib import admin
from django.urls import URLResolver, include, path

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
