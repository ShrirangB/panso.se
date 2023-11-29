from __future__ import annotations

from typing import TYPE_CHECKING

from .stores.webhallen.urls import urlpatterns as webhallen_urlpatterns

if TYPE_CHECKING:
    from django.urls import URLPattern

# /webhallen/
urlpatterns: list[URLPattern] = webhallen_urlpatterns
