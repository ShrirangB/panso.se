from __future__ import annotations

from typing import Any

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from intel.models import ArkFilterData, Processor

router = Router()


@router.get(
    path="/filter",
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
        return JsonResponse(data={"error": str(e)}, status=500)


@router.get(
    path="/processors",
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
        return JsonResponse(data={"error": str(e)}, status=500)


@router.get(
    path="/processors/{product_id}",
    summary="Return the data for a specific processor.",
    description="Return the data for a specific processor.",
)
def return_processor_data(request: HttpRequest, product_id: int) -> JsonResponse:  # noqa: ARG001
    """Return the data for a specific processor."""
    try:
        processor: Processor = get_object_or_404(Processor, product_id=product_id)
        processor_data: dict[str, Any] = processor.__dict__
        excluded_fields: list[str] = ["created", "modified", "history", "_state"]
        processor_data = {key: value for key, value in processor_data.items() if key not in excluded_fields}
        return JsonResponse(data=processor_data, safe=False)

    except Processor.DoesNotExist:
        return JsonResponse(data=[], safe=False)
    except Exception as e:  # noqa: BLE001
        return JsonResponse(data={"error": str(e)}, status=500)
