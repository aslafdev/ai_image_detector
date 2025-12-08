import asyncio
import gc
import torch
import psutil
import os
from typing import Dict, List, Type,Tuple
from fastapi.concurrency import run_in_threadpool

from models.base import BaseModel
from schemas.model_info import ModelStatus, ModelInfoOut, ExistingModel
from schemas.model_results import TableCell, PredictionResult,CellType, ValueType



class ModelManagerError(Exception):
    """Bazowa klasa błędów managera."""
    pass

class ModelNotFoundError(ModelManagerError):
    pass

class ModelMemoryLimitError(ModelManagerError):
    pass

class ModelNotLoadedError(ModelManagerError):
    pass

class ModelLoadingError(ModelManagerError):
    pass




class ModelManager:
    def __init__(self, existing_models: List[ExistingModel], max_loaded_models: int = 3):
        self.max_loaded_models = max_loaded_models
        
        self.registry_info: Dict[str, ExistingModel] = {
            m.id: m for m in existing_models
        }
        
        self.registry_classes: Dict[str, Type[BaseModel]] = {
            m.id: m.model_class for m in existing_models
        }

        self.loaded_models: Dict[str, BaseModel] = {}
        
        self.model_states: Dict[str, ModelStatus] = {
            k: ModelStatus.NOT_LOADED for k in self.registry_classes.keys()
        }
        
        self.lock = asyncio.Lock()

    def _log_memory(self, tag: str):
        """Pomocnicza funkcja do logowania zużycia RAM/VRAM."""
        # RAM (Pamięć operacyjna procesu)
        process = psutil.Process(os.getpid())
        ram_mb = process.memory_info().rss / 1024 / 1024
        
        # VRAM (Pamięć karty graficznej - jeśli dostępna)
        vram_msg = ""
        if torch.cuda.is_available():
            # Allocated: To, co faktycznie zajmują tensory
            allocated = torch.cuda.memory_allocated() / 1024 / 1024
            # Reserved: To, co PyTorch zarezerwował od systemu (cache)
            reserved = torch.cuda.memory_reserved() / 1024 / 1024
            vram_msg = f" | VRAM Alloc: {allocated:.2f}MB, Res: {reserved:.2f}MB"
            
        print(f"[{tag}] RAM: {ram_mb:.2f}MB{vram_msg}")

    def get_available_models(self) -> List[ModelInfoOut]:
        results = []
        for model_conf in self.registry_info.values():
            
            # Pobieramy samą klasę
            model_class = self.registry_classes[model_conf.id]
            
            # Wywołujemy metodę bezpośrednio na klasie!
            headers_list = model_class.features()

            results.append(ModelInfoOut(
                id=model_conf.id,
                name=model_conf.name,
                status=self.model_states.get(model_conf.id, ModelStatus.NOT_LOADED),
                features=headers_list 
            ))
        return results
    
    def get_loaded_models(self) -> List[ModelInfoOut]:
        return [
            ModelInfoOut(
                id=m_id,
                name=self.registry_info[m_id].name,
                status=ModelStatus.LOADED,
                features=self.registry_classes[m_id].features()
            )
            for m_id in self.loaded_models.keys()
        ]

    async def load_model(self, model_id: str):
        if model_id not in self.registry_classes:
            raise ModelNotFoundError(f"Model '{model_id}' nie istnieje w rejestrze.")

        async with self.lock:
            # 1. Sprawdź czy już załadowany
            if self.model_states[model_id] == ModelStatus.LOADED:
                print(f"Model {model_id} already loaded.")
                return 

            # 2. Limit pamięci
            if len(self.loaded_models) >= self.max_loaded_models:
                raise ModelMemoryLimitError(
                    f"Limit pamięci osiągnięty ({self.max_loaded_models} modeli). Odładuj inny model."
                )

            # 3. Rozpocznij procedurę
            print(f"--- Rozpoczynam ładowanie: {model_id} ---")
            self._log_memory(f"START LOAD {model_id}")
            
            self.model_states[model_id] = ModelStatus.LOADING
            
            try:
                model_class = self.registry_classes[model_id]
                model_instance = model_class()

                await run_in_threadpool(model_instance.load)

                self.loaded_models[model_id] = model_instance
                self.model_states[model_id] = ModelStatus.LOADED
                
                self._log_memory(f"END LOAD {model_id}")
                print(f"Model {model_id} załadowany pomyślnie.")
            
            except Exception as e:
                self.model_states[model_id] = ModelStatus.ERROR
                print(f"Krytyczny błąd ładowania {model_id}: {e}")
                
                # --- SPRZĄTANIE PO BŁĘDZIE ---
                if 'model_instance' in locals():
                    del model_instance
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                self._log_memory(f"ERROR CLEANUP {model_id}")
                # -----------------------------

                raise ModelLoadingError(f"Błąd wewnętrzny modelu: {str(e)}")

    async def unload_model(self, model_id: str):
        if model_id not in self.registry_classes:
            raise ModelNotFoundError(f"Model '{model_id}' nie istnieje.")

        async with self.lock:
            if model_id in self.loaded_models:
                print(f"--- Usuwanie modelu: {model_id} ---")
                self._log_memory(f"START UNLOAD {model_id}")

                # 1. Usunięcie referencji
                del self.loaded_models[model_id]
                self.model_states[model_id] = ModelStatus.NOT_LOADED
                
                # 2. Czyszczenie pamięci
                gc.collect() 
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                self._log_memory(f"END UNLOAD {model_id}")
                print(f"Model {model_id} odładowany.")
            else:
                pass

    async def predict(self, model_id: str, image) -> Tuple[List[TableCell], float]:
          
            if model_id not in self.loaded_models:
                raise ModelNotLoadedError(f"Model {model_id} nie jest załadowany.")
            
            try:
                model = self.loaded_models[model_id]

                return await run_in_threadpool(model.predict, image)
                
            except Exception as e:
                raise e
                
           