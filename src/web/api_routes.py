"""HTTP API routes: text/braille translation and STL generation."""
from io import BytesIO

from fastapi import APIRouter, HTTPException
import fastapi.responses as responses

from src.translation import translator
from src.modeling.options import ModelOptions
from src.modeling.stl_service import StlService
from src.web.schemas import Text, Braille, ToSTLRequest


def _clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def _build_options(request: ToSTLRequest) -> ModelOptions:
    unique_plate = request.unique_plate if request.unique_plate else False
    symbols_per_line = _clamp(request.symbols_per_line if request.symbols_per_line else 22, 8, 50)
    text_alignment = request.text_alignment if request.text_alignment else "left"
    rounded = request.rounded if request.rounded else False
    points_only = request.points_only if request.points_only else False
    resolution = _clamp(request.resolution if request.resolution else 20, 15, 50)
    plate_thickness = _clamp(request.plate_thickness if request.plate_thickness else 2, 2, 100)

    return ModelOptions(
        resolution=resolution,
        plate_thickness=plate_thickness,
        unique_plate=unique_plate,
        symbols_per_line=symbols_per_line,
        text_alignment=text_alignment,
        rounded=rounded,
        points_only=points_only,
    )


def build_api_router(stl_service: StlService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.post("/encode")
    def braille_encode(request: Text):
        try:
            alphabet = request.alphabet if request.alphabet else "North American"
            return {"encoded": translator.encode(request.text, alphabet)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/decode")
    def braille_decode(request: Braille):
        try:
            alphabet = request.alphabet if request.alphabet else "North American"
            return {"decoded": translator.decode(request.braille, alphabet)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/to-stl")
    def to_stl(request: ToSTLRequest):
        try:
            options = _build_options(request)
            stl_bytes = stl_service.generate(request.braille, options)

            return responses.StreamingResponse(
                BytesIO(stl_bytes),
                media_type="application/vnd.ms-pkistl",
                headers={"Content-Disposition": "attachment; filename=output.stl"},
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
