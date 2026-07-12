"""Application settings. The port can be overridden with the PORT env var."""
import os


class Settings:
    PORT = int(os.getenv("PORT", "3000"))
    TEMPLATES_DIR = "templates"
    STATIC_DIR = "public"
