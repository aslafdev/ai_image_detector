
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def load(self, weight_path: str | None = None):
        """Load model weights."""
        pass

    @abstractmethod
    def preprocess(self, image):
        
        pass

    @abstractmethod
    def predict(self, image):
       
        pass
