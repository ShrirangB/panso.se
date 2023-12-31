from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar

import django_tables2 as tables
from django.http import HttpRequest, HttpResponse
from django.template import Template, loader
from django_filters import CharFilter, FilterSet, NumberFilter
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

from intel.models import Processor


class ProcessorTable(tables.Table):
    """The django-tables2 table for the Processor model."""

    class Meta:
        model = Processor
        template_name: str = "django_tables2/bootstrap5.html"
        fields: ClassVar[list[str]] = [
            "name",
            "lithography",
            "total_cores",
            "tdp",
            "performance_cores",
            "efficiency_cores",
        ]


def index(request: HttpRequest) -> HttpResponse:
    """/intel/ page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    # TODO: Make name clickable to go to /intel/processors/{processor_id}
    # TODO: If the filter is empty we should rewrite the URL to /intel/processors
    # TODO: If a filter is empty we should remove it from the URL (e.g. /intel/processors?name=foo&lithography=) -> /intel/processors?name=foo # noqa: E501
    # Table filtering for django-filter
    f = ProcessorFilter(request.GET, queryset=Processor.objects.all())
    table = ProcessorTable(f.qs)
    RequestConfig(request).configure(table)

    # Table exporting for django-tables2
    export_format: str | None = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        current_date: str = datetime.now(tz=timezone.utc).strftime("%Y%m%d")  # 20231222
        return exporter.response(f"Intel.processors.{current_date}-panso.se.{export_format}")

    template: Template = loader.get_template(template_name="intel/index.html")
    return HttpResponse(content=template.render({"table": table, "filter": f}, request=request))


class ProcessorFilter(FilterSet):
    """The django-filter filter for the Processor model."""

    # TODO: Make this look nicer with Bootstrap
    # TODO: Make each filter a dropdown menu with the available options
    # TODO: Make the filter labels translatable
    # TODO: Make the filter labels clickable to filter by that label

    name = CharFilter(lookup_expr="icontains", label="Name")
    lithography = NumberFilter(lookup_expr="exact", label="Lithography")
    total_cores = NumberFilter(lookup_expr="exact", label="Total cores")
    performance_cores = NumberFilter(lookup_expr="exact", label="Performance cores")
    efficiency_cores = NumberFilter(lookup_expr="exact", label="Efficiency cores")

    class Meta:
        model = Processor
        fields: ClassVar[list[str]] = [
            "name",
            "lithography",
            "total_cores",
            "performance_cores",
            "efficiency_cores",
        ]


def processor(request: HttpRequest, processor_id: int) -> HttpResponse:
    """/intel/processors/{processor_id} page.

    Args:
        request: The request.
        processor_id: The processor ID.

    Returns:
        HttpResponse: The response.
    """
    template: Template = loader.get_template(template_name="intel/processor.html")
    processor = Processor.objects.get(pk=processor_id)
    context = {"processor": processor}
    return HttpResponse(content=template.render(context, request))
