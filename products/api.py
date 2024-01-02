"""We use Django Ninja to create a REST API for the data we have scraped from Intel's website.

See https://django-ninja.dev/ for more information.

API endpoints:
- /api/v1/eans
- /api/v1/eans/{ean}
"""

from __future__ import annotations

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from products.models import Eans

router = Router()

# TODO(TheLovinator): #30 We should add more OpenAPI documentation for each endpoint.
# https://github.com/TheLovinator1/panso.se/issues/30


@router.get(
    path="/eans",
    summary="Return all EANs.",
    description="Return all EANs as JSON.  \n\n **Note:** This will return a JSON array of 12k+ EANs so don't try to load this via the Swagger UI.",  # noqa: E501
)
def list_eans(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all EANs."""
    eans = list(Eans.objects.values("ean", "name"))
    return JsonResponse(data=eans, safe=False)


@router.get(path="/eans/{ean}")
def get_ean(request: HttpRequest, ean: str) -> JsonResponse:  # noqa: ARG001
    """Return EAN."""
    try:
        _ean: Eans = get_object_or_404(Eans, ean=ean)
        ean_data: dict[str, str] = {
            "ean": str(_ean.ean),
            "name": str(_ean.name),
        }
        return JsonResponse(data=ean_data, safe=False)
    except Http404:
        return JsonResponse(data={"error": f"EAN with ID {ean} not found."}, status=404)
    except Exception as e:  # noqa: BLE001
        return JsonResponse(data={"error": str(e)}, status=500)
