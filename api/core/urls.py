from __future__ import annotations

from django.urls import URLPattern, path

from .views import index_view
from .webhallen.urls import urlpatterns as webhallen_urlpatterns

# /
urlpatterns: list[URLPattern] = [path("", index_view, name="index")]

# /webhallen/
urlpatterns += webhallen_urlpatterns
