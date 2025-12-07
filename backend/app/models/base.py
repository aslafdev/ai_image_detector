
from abc import ABC, abstractmethod
from typing import Dict
from schemas.model_results import TableRow

class BaseModel(ABC):
    @abstractmethod
    def load(self):
        pass
    

    @property
    @abstractmethod
    def columns(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def preprocess(self, image):
        pass


    @abstractmethod
    def predict(self, image)-> TableRow:
        pass 


        

        
    

    
