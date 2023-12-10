from __future__ import annotations

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from products.models import Eans

router = Router()


@router.get(
    "/eans",
    summary="Return all EANs.",
    description="Return all EANs as JSON.  \n\n **Note:** This will return a JSON array of 12k+ EANs so don't try to load this via the Swagger UI.",  # noqa: E501
)
def list_eans(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return all EANs."""
    eans = list(Eans.objects.values("ean", "name", "created", "updated"))
    return JsonResponse(eans, safe=False)


@router.get("/eans/{ean}")
def get_ean(request: HttpRequest, ean: str) -> JsonResponse:  # noqa: ARG001
    """Return EAN."""
    try:
        _ean: Eans = get_object_or_404(Eans, ean=ean)
        ean_data: dict[str, str] = {
            "ean": str(_ean.ean),
            "name": str(_ean.name),
            "created": str(_ean.created),
            "updated": str(_ean.updated),
        }
        return JsonResponse(ean_data, safe=False)
    except Http404:
        return JsonResponse({"error": f"EAN with ID {ean} not found."}, status=404)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=500)
