"""This module contains the views for the webhallen application.

Paths:
    /webhallen/ index page.

See:
    https://docs.djangoproject.com/en/5.0/topics/http/views/
"""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.template import Template, loader

from webhallen.models import WebhallenSection


def index(request: HttpRequest) -> HttpResponse:
    """/webhallen/ index page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="webhallen/index.html")
    sections = WebhallenSection.objects.all()
    sections = sorted(sections, key=lambda section: section.section_id)

    context: dict[str, list[WebhallenSection]] = {"sections": sections}
    return HttpResponse(content=template.render(context, request))
