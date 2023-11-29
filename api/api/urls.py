from __future__ import annotations

from django.urls import URLResolver, include, path

urlpatterns: list[URLResolver] = [path("", include("core.urls"))]
