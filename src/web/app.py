"""Composition root: build the FastAPI app and wire the dependencies together."""
from fastapi import FastAPI

from src.modeling.model_builder import BrailleModelBuilder
from src.modeling.stl_service import StlService
from src.rendering.vtk_mesh_engine import VtkMeshEngine
from src.rendering.vtk_stl_serializer import VtkStlSerializer
from src.web.api_routes import build_api_router
from src.web.page_routes import build_page_router


def create_app() -> FastAPI:
    # Infrastructure implementations of the modeling ports.
    mesh_engine = VtkMeshEngine()
    mesh_serializer = VtkStlSerializer()

    # Use cases.
    stl_service = StlService(BrailleModelBuilder(mesh_engine), mesh_serializer)

    app = FastAPI()
    app.include_router(build_page_router())
    app.include_router(build_api_router(stl_service))
    return app
