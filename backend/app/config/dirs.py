from pathlib import Path 



ROOT_DIR = Path(__file__).parent.parent.parent


STORAGE_DIR = ROOT_DIR/'storage'
TORCH_WEIGHTS_DIR = STORAGE_DIR/'torch'/'weights'

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
TORCH_WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)