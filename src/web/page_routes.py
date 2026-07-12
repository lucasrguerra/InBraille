"""HTTP routes that serve the HTML pages and static frontend assets."""
from fastapi import APIRouter
import fastapi.responses as responses

from src.config import Settings


def build_page_router() -> APIRouter:
    router = APIRouter()

    @router.get("/")
    @router.get("/en")
    @router.get("/zh")
    def home():
        try:
            return responses.FileResponse(Settings.TEMPLATE_HTML, media_type="text/html; charset=utf-8")
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get("/public/{file_path:path}")
    def static(file_path: str):
        try:
            path = f"{Settings.STATIC_DIR}/{file_path}"
            if file_path.endswith(".css"):
                return responses.FileResponse(path, media_type="text/css")
            elif file_path.endswith(".js"):
                return responses.FileResponse(path, media_type="text/javascript")
            else:
                return responses.FileResponse(path)
        except Exception:
            return responses.Response(content="File not found", status_code=404)

    return router
