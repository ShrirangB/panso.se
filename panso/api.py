from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import orjson
from ninja import NinjaAPI
from ninja.openapi.docs import DocsBase, Redoc, Swagger
from ninja.parser import Parser

from intel.api import router as intel_router
from products.api import router as panso_router
from webhallen.api import router as webhallen_router

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from ninja.types import DictStrAny


class ORJSONParser(Parser):
    """Use orjson instead of json for parsing.

    Args:
        Parser: _description_
    """

    def parse_body(self: ORJSONParser, request: HttpRequest) -> DictStrAny:  # noqa: PLR6301
        """Deserialize the body of the request using orjson."""
        return orjson.loads(request.body)


class MixedDocs(DocsBase):
    """Use both Swagger and Redoc for docs."""

    def __init__(self: MixedDocs) -> None:
        """Initialize the MixedDocs class."""
        super().__init__()
        self.swagger = Swagger()
        self.redoc = Redoc()

    def render_page(self: MixedDocs, request: HttpRequest, api: NinjaAPI, **kwargs) -> HttpResponse:  # noqa: ANN003
        """Render the docs page.

        Args:
            self: Both Swagger and Redoc
            request: The request
            api: The NinjaAPI instance
            **kwargs: The keyword arguments

        Returns:
            HttpResponse: The rendered docs page
        """
        engine_name: Literal["swagger", "redoc"] = kwargs.pop("engine")
        engine: Swagger = {
            "swagger": self.swagger,
            "redoc": self.redoc,
        }.get(engine_name, self.swagger)
        return engine.render_page(request, api, **kwargs)


api = NinjaAPI(
    title="Panso API",
    version="1.0.0",
    description="API for Panso.se",
    urls_namespace="api-v1",
    parser=ORJSONParser(),
    docs_url="/docs/<engine>",
    docs=MixedDocs(),
)

api.add_router("webhallen/", webhallen_router, tags=["Webhallen"])
api.add_router("", panso_router, tags=["Panso"])
api.add_router("intel/", intel_router, tags=["Intel"])
