"""Application settings. The port can be overridden with the PORT env var."""
import os


# Base dir is always resolved relative to this file, not the working directory.
# This prevents breakage when the app is launched from a different cwd (e.g. Docker).
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings:
    PORT = int(os.getenv("PORT", "3000"))
    TEMPLATES_DIR = os.path.join(_BASE_DIR, "templates")
    STATIC_DIR = os.path.join(_BASE_DIR, "public")
