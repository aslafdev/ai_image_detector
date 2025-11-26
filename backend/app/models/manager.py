from functools import lru_cache
from typing import Callable

from app.models.base import BaseModel
from app.models.convnext.model import ConvNeXtBinaryModel_StyleGan1

ModelBuilder = Callable[[], BaseModel]

_MODEL_BUILDERS: dict[str, ModelBuilder] = {
    "stylegan1": ConvNeXtBinaryModel_StyleGan1,
}


@lru_cache(maxsize=None)
def get_model(name: str) -> BaseModel:
    """Lazily load and cache models by name."""
    builder = _MODEL_BUILDERS.get(name)
    if builder is None:
        raise ValueError(f"Unknown model '{name}'")
    return builder().load()


def available_models() -> list[str]:
    return list(_MODEL_BUILDERS.keys())
