"""This module contains the views for the webhallen application.

Paths:
    /webhallen/ index page.

See:
    https://docs.djangoproject.com/en/5.0/topics/http/views/
"""

from __future__ import annotations

from cacheops import cached_view
from django.http import HttpRequest, HttpResponse
from django.template import Template, loader

from webhallen.models import WebhallenSection


@cached_view
def index(request: HttpRequest) -> HttpResponse:
    """/webhallen/ index page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="webhallen/index.html")
    sections = WebhallenSection.objects.all()
    sections_sorted: list[WebhallenSection] = sorted(sections, key=lambda section: section.section_id)
    canonical_url: str = "https://panso.se/webhallen/"
    context: dict[str, list[WebhallenSection] | str] = {"sections": sections_sorted, "canonical_url": canonical_url}
    return HttpResponse(content=template.render(context=context, request=request))
