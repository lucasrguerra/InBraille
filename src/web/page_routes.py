"""HTTP routes that serve the HTML pages and static frontend assets."""
from pathlib import Path

from fastapi import APIRouter
import fastapi.responses as responses

from src.config import Settings


def build_page_router() -> APIRouter:
    router = APIRouter()

    @router.api_route("/", methods=["GET", "HEAD"])
    @router.api_route("/en", methods=["GET", "HEAD"])
    @router.api_route("/zh", methods=["GET", "HEAD"])
    def home():
        try:
            return responses.FileResponse(Settings.TEMPLATE_HTML, media_type="text/html; charset=utf-8")
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get(f"/{Settings.GOOGLE_VERIFICATION_FILE}")
    def google_site_verification():
        return responses.FileResponse(Settings.GOOGLE_VERIFICATION_HTML, media_type="text/html; charset=utf-8")

    @router.get("/public/{file_path:path}")
    def static(file_path: str):
        # Resolve and confine the path so "..", encoded slashes and symlinks cannot escape STATIC_DIR.
        root = Path(Settings.STATIC_DIR).resolve()
        target = (root / file_path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            return responses.Response(content="File not found", status_code=404)

        media_types = {".css": "text/css", ".js": "text/javascript"}
        return responses.FileResponse(target, media_type=media_types.get(target.suffix))

    return router
