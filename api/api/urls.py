from __future__ import annotations

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from core.views import index
from core.webhallen.api import router as webhallen_router

api = NinjaAPI()
api.add_router("webhallen", webhallen_router, tags=["webhallen"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # type: ignore  # noqa: PGH003
    path("", index),
]
