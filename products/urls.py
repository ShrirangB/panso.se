"""URL Configuration for /.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/


URLs:
    - /
        - The home page.
    - /privacy
        - The privacy policy page.
    - /terms
        - The license page. Can be found by clicking "CC BY-SA 4.0" in the footer.
    - /contact
        - The contact page.
    - /api
        - The API documentation page.
    - /robots.txt
        - The robots.txt page.
    - /favicon.ico
        - The favicon.ico icon.
    - /icon-512.png
        - The 512x512 logo. Used for manifest.webmanifest.
    - /icon-192.png
        - The 192x192 logo. Used for manifest.webmanifest.
    - /bot-ip-list.txt
        - The list of IP addresses for web crawlers. Used for Cloudflare Verified Bots.
"""

from __future__ import annotations

from django.urls import URLPattern, path
from django.views.generic.base import RedirectView

from . import views

app_name: str = "products"


# TODO(TheLovinator): #33 We should cache the views.
# https://github.com/TheLovinator1/panso.se/issues/33

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
