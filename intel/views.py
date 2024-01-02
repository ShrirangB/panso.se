"""This module contains the views for the Intel application.

Paths:
    /intel/
        List of all the Intel processors.
    /intel/processors/{processor_id}
        Information about a specific Intel processor.

See:
    https://docs.djangoproject.com/en/5.0/topics/http/views/
"""

from __future__ import annotations

from functools import lru_cache
from typing import ClassVar

from cacheops import cached_view_as
from django.http import HttpRequest, HttpResponse
from django.template import Template, loader
from django.views.generic import ListView
from django_filters import CharFilter, FilterSet, NumberFilter

from intel.models import Processor


class ProcessorsListView(ListView):
    """A list of all the Intel processors."""

    model = Processor
    template_name = "intel/index.html"
    context_object_name = "processors"
    paginate_by = 100


@cached_view_as(Processor)
def index(request: HttpRequest) -> HttpResponse:
    """/intel/ page.

    Args:
        request: The request.

    Returns:
        HttpResponse: The response.
    """
    # TODO(TheLovinator): Make name clickable to go to /intel/processors/{processor_id}  # noqa: TD003
    # TODO(TheLovinator): If the filter is empty we should rewrite the URL to /intel/processors  # noqa: TD003
    # TODO(TheLovinator): If a filter is empty we should remove it from the URL (e.g. /intel/processors?name=foo&lithography=) -> /intel/processors?name=foo # noqa: E501, TD003
    # Table filtering for django-filter
    f = ProcessorFilter(
        request.GET,
        queryset=Processor.objects.all(),
    )

    template: Template = loader.get_template(template_name="intel/index.html")
    return HttpResponse(content=template.render({"filter": f}, request=request))


class ProcessorFilter(FilterSet):
    """The django-filter filter for the Processor model."""

    # TODO(TheLovinator): Make this look nicer with Bootstrap  # noqa: TD003
    # TODO(TheLovinator): Make each filter a dropdown menu with the available options  # noqa: TD003
    # TODO(TheLovinator): Make the filter labels translatable  # noqa: TD003
    # TODO(TheLovinator): Make the filter labels clickable to filter by that label  # noqa: TD003

    name = CharFilter(lookup_expr="icontains", label="Name")
    lithography = NumberFilter(lookup_expr="exact", label="Lithography")
    total_cores = NumberFilter(lookup_expr="exact", label="Total cores")
    performance_cores = NumberFilter(lookup_expr="exact", label="Performance cores")
    efficiency_cores = NumberFilter(lookup_expr="exact", label="Efficiency cores")

    class Meta:
        """Meta class for the ProcessorFilter."""

        model = Processor
        fields: ClassVar[list[str]] = [
            "name",
            "lithography",
            "total_cores",
            "performance_cores",
            "efficiency_cores",
        ]


@lru_cache(maxsize=128)
def render_field(verbose_name: str, help_text: str, field: str) -> str:
    """Render a field.

    Args:
        verbose_name: The verbose name of the field.
        help_text: The help text of the field.
        field: The field.

    Returns:
        str: The rendered field.
    """
    return f"""
    <!-- {verbose_name} -->
    <div class="col-md-6" id="{verbose_name.replace(' ', '-').replace('(', '').replace(')', '').lower()}">
        <h4 class="custom-tooltip" data-bs-toggle="tooltip" data-bs-placement="top" title="{help_text}" id="{verbose_name.replace(' ', '-').replace('(', '').replace(')', '').lower()}-label">
            {verbose_name}
        </h4>
        <p class="mb-3" id="{verbose_name.replace(' ', '-').replace('(', '').replace(')', '').lower()}-value">{field}</p>
    </div>
    """  # noqa: E501


@lru_cache(maxsize=128)
def generate_cpu_information_html(processor: Processor) -> str:  # noqa: C901
    """Generate HTML for CPU information.

    Args:
        processor: The Processor instance.

    Returns:
        str: The HTML.
    """
    # Get all fields from the Processor model
    fields = Processor._meta.get_fields()  # noqa: SLF001

    # List to store rendered fields
    rendered_fields = []

    for field in fields:
        verbose_name: str = str(field.verbose_name)  # type: ignore  # noqa: PGH003
        help_text: str = str(field.help_text)  # type: ignore  # noqa: PGH003
        field_value: str = str(getattr(processor, field.name))

        if not field_value or field_value == "None":
            continue

        excluded_names: list[str] = ["created", "updated", "id", "history"]
        if verbose_name in excluded_names:
            continue

        hertz_list: list[str] = ["base_frequency", "max_frequency", "max_turbo_frequency", "max_memory_speed"]
        if field.name in hertz_list:
            # Convert from hertz to gigahertz
            field_value = f"{int(field_value) / 1000000000} GHz"

        size_list: list[str] = ["l1_cache", "l2_cache", "l3_cache", "max_memory_size"]
        if field.name in size_list:
            # Convert from bytes to terabytes if larger than 1000 GB
            if int(field_value) >= 1_000_000_000_000:  # noqa: PLR2004
                field_value = f"{int(field_value) / 1_000_000_000_000} TB"
            # Convert from bytes to gigabytes if larger than 1 GB
            elif int(field_value) >= 1_000_000_000:  # noqa: PLR2004
                field_value = f"{int(field_value) / 1_000_000_000} GB"
            # Convert from bytes to megabytes if smaller than 1 GB
            elif int(field_value) < 1_000_000_000:  # noqa: PLR2004
                field_value = f"{int(field_value) / 1_000_000} MB"
            # Remove .0
            field_value = field_value.replace(".0", "")

        watt_list: list[str] = ["tdp"]
        if field.name in watt_list:
            # Convert to watts
            field_value = f"{int(field_value)} W"

        temperature_list: list[str] = [
            "digital_thermal_sensor_temperature_max",
            "t_case",
            "thermal_velocity_boost_temperature",
            "operating_temperature_max",
            "operating_temperature_min",
        ]
        if field.name in temperature_list:
            int_field_value = int(float(field_value))
            # Convert to degrees Celsius and Fahrenheit
            field_value = f"{int(int_field_value)} °C ({int(int_field_value) * 1.8 + 32} °F)"

        # Replace True with Yes and False with No
        if field_value == "True":
            field_value = "Yes"
        elif field_value == "False":
            field_value = "No"

        # Render the field
        rendered_field: str = render_field(verbose_name=verbose_name, help_text=help_text, field=field_value)

        # Append the rendered field to the list
        rendered_fields.append(rendered_field)

    return f"""
    <div class="row">
        {''.join(rendered_fields)}
    </div>
    """


@cached_view_as(Processor)
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
    context = {"processor": processor, "cpu_information": generate_cpu_information_html(processor)}
    return HttpResponse(content=template.render(context, request))
