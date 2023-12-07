from __future__ import annotations

from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import include, path

from panso.api import api


def testboi(request: HttpRequest) -> JsonResponse:  # noqa: D103, ARG001
    return JsonResponse({"status": "ok"})


urlpatterns: list = [
    path("admin/", admin.site.urls),
    path("testboi", testboi, name="testboi"),
    path("api/", api.urls),  # type: ignore  # noqa: PGH003
    path("", include("pages.urls")),
    path("webhallen/", include("webhallen.urls")),
]
