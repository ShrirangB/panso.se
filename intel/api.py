from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from ninja import Router

from intel.models import ArkFilterData, Processor

router = Router()


@router.get(
    "/filter",
    summary="Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.",
    description="Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html.",
)
def return_filter_data(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return the filter data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""
    try:
        filters: ArkFilterData = ArkFilterData.objects.get(pk=1)
        return JsonResponse(filters.json_data, safe=False)
    except ArkFilterData.DoesNotExist:
        return JsonResponse([], safe=False)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=500)


@router.get(
    "/processors",
    summary="Return a list of ids for all processors.",
    description="Return a list of ids for all processors. You can use this to get the data for all processors with the /processors/{id} endpoint.",  # noqa: E501
)
def return_processor_ids(request: HttpRequest) -> JsonResponse:  # noqa: ARG001
    """Return a list of ids for all processors."""
    try:
        processors = Processor.objects.values_list("product_id", "name")
        processors = [{"id": p[0], "name": p[1]} for p in processors]
        return JsonResponse(processors, safe=False)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=500)
