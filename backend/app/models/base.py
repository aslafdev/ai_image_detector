
from abc import ABC, abstractmethod
from typing import List

class BaseModel(ABC):
    @abstractmethod
    def load(self):
        pass
    
    @staticmethod
    @abstractmethod
    def features() -> List[str]:
        pass

    @abstractmethod
    def preprocess(self, image):
        pass


    @abstractmethod
    def predict(self, image):
        pass 


        

        
    

    
