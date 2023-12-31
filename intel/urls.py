from __future__ import annotations

from django.urls import URLPattern, path

from . import views

app_name: str = "intel"

urlpatterns: list[URLPattern] = [
    path(route="", view=views.index, name="index"),
    path(route="processors/<int:processor_id>", view=views.processor, name="processor"),
]
