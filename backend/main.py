import uvicorn

from app.app import app
from app.config.dirs import TORCH_WEIGHTS_DIR


if __name__ == "__main__":
    # Run the FastAPI app defined in app/app.py; using the correct module path avoids
    # ModuleNotFoundError when uvicorn imports the application.
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)
