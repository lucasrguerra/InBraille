import uvicorn

from src.config import Settings
from src.web.app import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=Settings.PORT, log_level="info")
