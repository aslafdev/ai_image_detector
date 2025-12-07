
from typing import List

from models.test.model import DummySlowModel
from services.model_manager import ModelManager, ExistingModel

from models.convnext.model import ConvNeXtBinaryModel_StyleGan1
# Tu będziesz dopisywać kolejne, np:
# from models.resnet import ResNetModel

available_models = [
    ExistingModel(
        id="stylegan1", 
        name="StyleGAN 1 Detector", 
        model_class=ConvNeXtBinaryModel_StyleGan1
    ),
    ExistingModel(
        id="dummy_slow",
        name="Symulacja (Wolne Ładowanie)",
        model_class=DummySlowModel
    )
]

global_model_manager = ModelManager(
    existing_models=available_models,
    max_loaded_models=2  
)


def get_manager() -> ModelManager:
    return global_model_manager