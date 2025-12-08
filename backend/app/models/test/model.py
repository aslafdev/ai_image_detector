# models/dummy.py

import time
from models.base import BaseModel
from typing import List

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

    @staticmethod
    def features() -> List[str]:
        return ["Symulacja"]

    def preprocess(self, image):
        return image

    def predict(self, image):
        pass

    def predict_ex(self, image):
        pass