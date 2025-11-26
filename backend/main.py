import uvicorn

from src.app import app
from src.config.dirs import TORCH_WEIGHTS_DIR



print(TORCH_WEIGHTS_DIR)


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)