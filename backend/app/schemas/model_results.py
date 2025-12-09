from pydantic import BaseModel
from typing import Literal, Union, List, Optional

CellType = Literal["text", "tag", "percent", "number"]
ValueType = Union[str, float, int, bool]

class TableCell(BaseModel):
    value: ValueType
    label: str           # <--- WAŻNE: To będzie nagłówek kolumny (np. "Decyzja")
    type: CellType
    

class PredictionResult(BaseModel):
    filename: str
    cells: List[TableCell]          
    prediction_time: float 
    
