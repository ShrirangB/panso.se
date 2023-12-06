from __future__ import annotations

from typing import TYPE_CHECKING

import orjson
from ninja import NinjaAPI
from ninja.parser import Parser

from webhallen.api import router as webhallen_router

if TYPE_CHECKING:
    from django.http import HttpRequest
    from ninja.types import DictStrAny


class ORJSONParser(Parser):
    """Use orjson instead of json for parsing.

    Args:
        Parser: _description_
    """

    def parse_body(self: ORJSONParser, request: HttpRequest) -> DictStrAny:  # noqa: PLR6301
        """Deserialize the body of the request using orjson."""
        return orjson.loads(request.body)


api = NinjaAPI(
    title="Panso API",
    version="1.0.0",
    description="API for Panso.se",
    urls_namespace="api-v1",
    parser=ORJSONParser(),
)

api.add_router("webhallen/", webhallen_router)
