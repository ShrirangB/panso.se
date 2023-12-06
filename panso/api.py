from ninja import NinjaAPI

from webhallen.api import router as webhallen_router

api = NinjaAPI(
    title="Panso API",
    version="1.0.0",
    description="API for Panso.se",
    urls_namespace="api-v1",
)

api.add_router("webhallen/", webhallen_router)
