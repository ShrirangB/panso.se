"""URLs for the intel app.

URLs:
    - /intel/
        - List of all processors.
    - /intel/processors/{processor_id}
        - The processor detail page.
"""

from __future__ import annotations

from cacheops import cached_view_as
from django.urls import URLPattern, path

from intel.models import Processor

from . import views

app_name: str = "intel"

urlpatterns: list[URLPattern] = [
    path(route="", view=cached_view_as(Processor)(views.ProcessorsListView.as_view()), name="index"),
    path(
        route="processors/<int:processor_id>",
        view=views.processor,
        name="detail",
    ),
]
