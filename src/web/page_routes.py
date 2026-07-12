"""HTTP routes that serve the HTML pages and static frontend assets."""
from fastapi import APIRouter
import fastapi.responses as responses

from src.config import Settings


def build_page_router() -> APIRouter:
    router = APIRouter()

    @router.get("/")
    def home_pt_br():
        try:
            html_content = open(f"{Settings.TEMPLATES_DIR}/index_pt_br.html", "r", encoding="utf-8").read()
            return responses.HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get("/en")
    def home_en():
        try:
            html_content = open(f"{Settings.TEMPLATES_DIR}/index_en.html", "r", encoding="utf-8").read()
            return responses.HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get("/zh")
    def home_zh():
        try:
            html_content = open(f"{Settings.TEMPLATES_DIR}/index_zh.html", "r", encoding="utf-8").read()
            return responses.HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
        except Exception:
            return responses.Response(content="Internal Server Error", status_code=404)

    @router.get("/public/{file_path}")
    def static(file_path: str):
        try:
            path = f"{Settings.STATIC_DIR}/{file_path}"
            if file_path == "style.css":
                content = open(path, "r", encoding="utf-8").read()
                return responses.HTMLResponse(content=content, media_type="text/css; charset=utf-8")
            elif file_path in ("script.js", "preview.js"):
                content = open(path, "r", encoding="utf-8").read()
                return responses.HTMLResponse(content=content, media_type="text/javascript; charset=utf-8")
            else:
                return responses.FileResponse(path)
        except Exception:
            return responses.Response(content="File not found", status_code=404)

    return router
