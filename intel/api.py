from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from ninja import Router

from intel.models import ArkFilterData

router = Router()


@router.get(
    "/filter",
    summary="Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.",
    description="Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.",
)
def return_filter_data(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""
    try:
        filters = ArkFilterData.objects.get(pk=1)
        return JsonResponse(filters.json_data, safe=False)
    except ArkFilterData.DoesNotExist:
        return JsonResponse([], safe=False)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=500)
