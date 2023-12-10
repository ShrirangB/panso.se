from __future__ import annotations

from django.urls import URLPattern, path
from django.views.generic.base import RedirectView

from . import views

app_name: str = "products"

urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
    path("robots.txt", views.robots_txt, name="robots-txt"),
    path("favicon.ico", RedirectView.as_view(url="/static/products/favicon.ico", permanent=True)),
    path("icon-512.png", RedirectView.as_view(url="/static/products/icon-512.png", permanent=True)),
    path("icon-192.png", RedirectView.as_view(url="/static/products/icon-192.png", permanent=True)),
    path("bot-ip-list.txt", views.bot_ip_list, name="bot-ip-list"),
]
