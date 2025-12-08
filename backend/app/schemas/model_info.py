
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from typing import List, Type

class ModelStatus(str, Enum):
    NOT_LOADED = "not_loaded"
    LOADING = "loading"
    LOADED = "loaded"
    ERROR = "error"


@dataclass
class ExistingModel:
    id: str
    name: str
    model_class: Type[BaseModel]    


#model dla forntu 
class ModelInfoOut(BaseModel):
    id: str
    name: str
    status : ModelStatus
    features: List[str]

    