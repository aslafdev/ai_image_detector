import asyncio
import gc
import torch
from typing import Dict, List, Type
from dataclasses import dataclass
from fastapi.concurrency import run_in_threadpool

# Twoje importy
from models.base import BaseModel
from schemas.model_info import ModelStatus, ModelInfoOut



class ModelManagerError(Exception):
    """Bazowa klasa błędów managera."""
    pass

class ModelNotFoundError(ModelManagerError):
    """Gdy pytamy o ID, którego nie ma w rejestrze."""
    pass

class ModelMemoryLimitError(ModelManagerError):
    """Gdy brakuje miejsca na załadowanie modelu."""
    pass

class ModelNotLoadedError(ModelManagerError):
    """Gdy próbujemy użyć modelu, który nie jest załadowany."""
    pass

class ModelLoadingError(ModelManagerError):
    """Gdy wystąpił błąd wewnątrz metody .load() modelu."""
    pass


@dataclass
class ExistingModel:
    id: str
    name: str
    model_class: Type[BaseModel]

class ModelManager:
    def __init__(self, existing_models: List[ExistingModel], max_loaded_models: int = 3):
        self.max_loaded_models = max_loaded_models
        
        # Przechowujemy konfigurację (nazwę itp) osobno, a klasy osobno
        self.registry_info: Dict[str, ExistingModel] = {
            m.id: m for m in existing_models
        }
        
        # Rejestr samych klas do instancjonowania
        self.registry_classes: Dict[str, Type[BaseModel]] = {
            m.id: m.model_class for m in existing_models
        }

        self.loaded_models: Dict[str, BaseModel] = {}
        
        self.model_states: Dict[str, ModelStatus] = {
            k: ModelStatus.NOT_LOADED for k in self.registry_classes.keys()
        }
        
        self.lock = asyncio.Lock()


    def get_available_models(self) -> List[ModelInfoOut]:
        """
        Zwraca listę WSZYSTKICH zdefiniowanych modeli w systemie (załadowanych i nie).
        Idealne dla Frontendu do zbudowania menu/routera.
        """
        return [
            ModelInfoOut(
                id=model.id,
                name=model.name,
                status=self.model_states.get(model.id, ModelStatus.NOT_LOADED)
            )
            # Iterujemy po wartościach rejestru (czyli obiektach ExistingModel)
            for model in self.registry_info.values()
        ]
    

    def get_loaded_models(self) -> List[ModelInfoOut]:
        """Zwraca listę TYLKO aktualnie załadowanych modeli."""
        return [
            ModelInfoOut(
                id=m_id,
                name=self.registry_info[m_id].name,
                status=ModelStatus.LOADED  # Skoro jest w loaded_models, to na pewno jest LOADED
            )
            for m_id in self.loaded_models.keys()
        ]

    async def load_model(self, model_id: str):
        if model_id not in self.registry_classes:
            raise ModelNotFoundError(f"Model '{model_id}' nie istnieje w rejestrze.")

        async with self.lock:
            # 1. Sprawdź czy już załadowany (Idempotency)
            if self.model_states[model_id] == ModelStatus.LOADED:
                print("Model already in memory, skipping load.")
                return 

            # Używamy self.max_loaded_models (bez podkreślenia, zgodnie z __init__)
            if len(self.loaded_models) >= self.max_loaded_models:
                raise ModelMemoryLimitError(
                    f"Limit pamięci osiągnięty ({self.max_loaded_models} modeli). Odładuj inny model."
                )

            # 3. Rozpocznij procedurę
            self.model_states[model_id] = ModelStatus.LOADING
            
            try:
                model_class = self.registry_classes[model_id]
                model_instance = model_class()

                # Ciężka operacja w wątku
                await run_in_threadpool(model_instance.load)

                self.loaded_models[model_id] = model_instance
                self.model_states[model_id] = ModelStatus.LOADED
                print(f"Model {model_id} załadowany pomyślnie.")
            
            except Exception as e:
                self.model_states[model_id] = ModelStatus.ERROR
                print(f"Krytyczny błąd ładowania {model_id}: {e}")
                # Opakowujemy nieznany błąd w nasz wyjątek
                raise ModelLoadingError(f"Błąd wewnętrzny modelu: {str(e)}")

    async def unload_model(self, model_id: str):
        if model_id not in self.registry_classes:
            raise ModelNotFoundError(f"Model '{model_id}' nie istnieje.")

        async with self.lock:
            if model_id in self.loaded_models:
                del self.loaded_models[model_id]
                self.model_states[model_id] = ModelStatus.NOT_LOADED
                
                # Czyszczenie pamięci
                gc.collect() 
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                print(f"Model {model_id} odładowany.")
            else:
                # Opcjonalnie: można to ignorować (idempotency)
                pass