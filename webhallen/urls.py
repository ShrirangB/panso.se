from __future__ import annotations

from django.urls import URLPattern, path

from . import views

app_name: str = "webhallen"

urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
]
