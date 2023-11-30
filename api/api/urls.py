from __future__ import annotations

from django.urls import URLResolver, include, path

# https://www.webhallen.com/
urlpatterns: list[URLResolver] = [path("", include("webhallen.urls"))]
