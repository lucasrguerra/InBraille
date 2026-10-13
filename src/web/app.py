"""Composition root: build the FastAPI app and wire the dependencies together."""
from fastapi import FastAPI

from src.modeling.model_builder import BrailleModelBuilder
from src.modeling.stl_service import StlService
from src.rendering.vtk_mesh_engine import VtkMeshEngine
from src.rendering.vtk_stl_serializer import VtkStlSerializer
from src.web.api_routes import build_api_router
from src.web.page_routes import build_page_router
from src.web.security import BodyLimitMiddleware, RateLimiter, SecurityHeadersMiddleware


def create_app() -> FastAPI:
    # Infrastructure implementations of the modeling ports.
    mesh_engine = VtkMeshEngine()
    mesh_serializer = VtkStlSerializer()

    # Use cases.
    stl_service = StlService(BrailleModelBuilder(mesh_engine), mesh_serializer)

    # Interactive docs and the OpenAPI schema are not needed in production.
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(RateLimiter)
    app.add_middleware(BodyLimitMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.include_router(build_page_router())
    app.include_router(build_api_router(stl_service))
    return app
