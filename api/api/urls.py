from __future__ import annotations

from django.contrib import admin
from django.http import HttpRequest, HttpResponse  # Django Ninja needs these so # noqa: TCH002
from django.shortcuts import render
from django.urls import path
from ninja import NinjaAPI

from core.webhallen.api import router as webhallen_router

api = NinjaAPI()
api.add_router("webhallen", webhallen_router, tags=["webhallen"])


@api.get("/", include_in_schema=False)
def index_view(request: HttpRequest) -> HttpResponse:
    """Return /."""
    return render(request, "core/index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),  # type: ignore  # noqa: PGH003
]
