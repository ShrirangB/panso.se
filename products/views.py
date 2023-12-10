from __future__ import annotations

from functools import lru_cache

import httpx
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET
from loguru import logger


def index(request: HttpRequest) -> HttpResponse:
    """/ index page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template = loader.get_template(template_name="products/index.html")
    context = {}
    return HttpResponse(content=template.render(context, request))


robots_txt_content = """User-agent: *
Allow: /

Sitemap: https://panso.se/sitemap.xml
"""


@require_GET
def robots_txt(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    """robots.txt page."""
    return HttpResponse(robots_txt_content, content_type="text/plain")


@lru_cache(maxsize=1)
def get_ip() -> str:
    """Get the IP address of the current server."""
    try:
        ip: str = httpx.get("https://checkip.amazonaws.com", timeout=5).text.strip()
    except httpx.HTTPError:
        ip = ""

    logger.info(ip)
    return ip


@require_GET
def bot_ip_list(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    """bot-ip-list page for Cloudflare verification."""
    ip: str = get_ip()
    return HttpResponse(content=ip, content_type="text/plain")
