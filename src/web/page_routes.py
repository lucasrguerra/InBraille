"""HTTP routes that serve the HTML pages and static frontend assets."""
from pathlib import Path

from fastapi import APIRouter
import fastapi.responses as responses

from src.config import Settings


# The frontend files are not fingerprinted, so browsers must revalidate them (cheap 304 via ETag)
# instead of heuristically caching a previous release after a deploy.
REVALIDATE = {"Cache-Control": "no-cache"}


def build_page_router() -> APIRouter:
    router = APIRouter()

    @router.api_route("/", methods=["GET", "HEAD"])
    @router.api_route("/en", methods=["GET", "HEAD"])
    @router.api_route("/zh", methods=["GET", "HEAD"])
    def home():
        try:
            return responses.FileResponse(Settings.TEMPLATE_HTML, media_type="text/html; charset=utf-8", headers=REVALIDATE)
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get(f"/{Settings.GOOGLE_VERIFICATION_FILE}")
    def google_site_verification():
        return responses.FileResponse(Settings.GOOGLE_VERIFICATION_HTML, media_type="text/html; charset=utf-8")

    @router.get("/robots.txt")
    def robots_txt():
        return responses.FileResponse(Settings.ROBOTS_TXT, media_type="text/plain; charset=utf-8")

    @router.get("/sitemap.xml")
    def sitemap_xml():
        return responses.FileResponse(Settings.SITEMAP_XML, media_type="application/xml; charset=utf-8")

    @router.get("/public/{file_path:path}")
    def static(file_path: str):
        # Resolve and confine the path so "..", encoded slashes and symlinks cannot escape STATIC_DIR.
        root = Path(Settings.STATIC_DIR).resolve()
        target = (root / file_path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            return responses.Response(content="File not found", status_code=404)

        media_types = {
            ".css": "text/css",
            ".js": "text/javascript",
            ".woff2": "font/woff2",
            ".woff": "font/woff",
            ".ttf": "font/ttf",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".ico": "image/x-icon",
            ".json": "application/json",
            ".webmanifest": "application/manifest+json",
        }
        return responses.FileResponse(target, media_type=media_types.get(target.suffix), headers=REVALIDATE)

    return router
