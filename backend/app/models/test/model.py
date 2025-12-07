# models/dummy.py

import time
from models.base import BaseModel

class DummySlowModel(BaseModel):
    def __init__(self):
        self._is_loaded = False

    def load(self):
        print("DUMMY: Rozpoczynam symulację ładowania wag (10 sekund)...")
        # To jest symulacja ciężkiej operacji I/O lub alokacji GPU.
        # Blokujemy wątek na 10 sekund.
        time.sleep(20) 
        self._is_loaded = True
        print("DUMMY: Załadowano!")
        return self

    @property
    def columns(self) -> dict[str, str]:
        return {
            "filename": "Plik", 
            "prediction": "Decyzja", 
            "score": "Pewność", 
            "prediction_time": "Czas (s)"
        }

    def preprocess(self, image):
        return image

    def predict(self, image):
        pass

    def predict_ex(self, image):
        pass