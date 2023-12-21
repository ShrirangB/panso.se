from __future__ import annotations

from django.urls import URLPattern, path
from django.views.generic.base import RedirectView

from . import views

app_name: str = "products"

urlpatterns: list[URLPattern] = [
    path(route="", view=views.index, name="index"),
    path(route="privacy", view=views.privacy, name="privacy"),
    path(route="terms", view=views.terms, name="terms"),
    path(route="contact", view=views.contact, name="contact"),
    path(route="api", view=views.api_view, name="api"),
    path(route="robots.txt", view=views.robots_txt, name="robots-txt"),
    path(route="favicon.ico", view=RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path(route="icon-512.png", view=RedirectView.as_view(url="/static/icon-512.png", permanent=True)),
    path(route="icon-192.png", view=RedirectView.as_view(url="/static/icon-192.png", permanent=True)),
    path(route="bot-ip-list.txt", view=views.bot_ip_list, name="bot-ip-list"),
]
