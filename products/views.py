"""The views for the main panso.se application.

URLs:
    - index /
        - The index page.
    - privacy /privacy
        - The privacy policy page.
    - terms /terms
        - The license page. Can be found by clicking "CC BY-SA 4.0" in the footer.
    - contact /contact
        - The contact page.
    - api_view /api
        - The API documentation page.
    - robots_txt /robots.txt
        - The robots.txt page.
    - get_ip /bot-ip-list.txt
        - The list of IP addresses for web crawlers. Used for Cloudflare Verified Bots.
    - about /about
        - The about page.
"""

from __future__ import annotations

from functools import lru_cache

import httpx
from cacheops import cached_view
from django.http import HttpRequest, HttpResponse
from django.template import Template, loader


@cached_view
def index(request: HttpRequest) -> HttpResponse:
    """/ index page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="index.html")
    canonical_url: str = "https://panso.se/"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context=context, request=request))


robots_txt_content = """User-agent: *
Allow: /

Sitemap: https://panso.se/sitemap.xml
"""


@cached_view
def robots_txt(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    """robots.txt page."""
    return HttpResponse(robots_txt_content, content_type="text/plain")


@lru_cache(maxsize=1)
def get_ip() -> str:
    """Get the IP address of the current server."""
    try:
        ip: str = httpx.get(url="https://checkip.amazonaws.com", timeout=5).text.strip()
    except httpx.HTTPError:
        ip = ""
    return ip


@cached_view
def bot_ip_list(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    """bot-ip-list page for Cloudflare verification."""
    ip: str = get_ip()
    return HttpResponse(content=ip, content_type="text/plain")


@cached_view
def contact(request: HttpRequest) -> HttpResponse:
    """/contact page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="contact.html")
    canonical_url: str = "https://panso.se/contact"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context, request))


@cached_view
def privacy(request: HttpRequest) -> HttpResponse:
    """/privacy page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="privacy.html")
    canonical_url: str = "https://panso.se/privacy"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context, request))


@cached_view
def terms(request: HttpRequest) -> HttpResponse:
    """/terms page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="terms.html")
    canonical_url: str = "https://panso.se/terms"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context, request))


@cached_view
def api_view(request: HttpRequest) -> HttpResponse:
    """/api page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="api.html")
    canonical_url: str = "https://panso.se/api"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context, request))
