from pydantic import BaseModel
from typing import Literal, Any, Dict, List


CellType = Literal["tag", "percent", "text", "number"]

class TableCell(BaseModel):
    value: Any          # Surowa wartość (do CSV/eksportu), np. 0.98
    type: CellType      # Jak to narysować?


class TableRow(BaseModel):
    filename: TableCell
    decision: TableCell 
    score: TableCell 
    prediction_time: TableCell
    
    extra_metrics: Dict[str, TableCell] = {}

class Table(BaseModel):
    header: Dict[str,str] 
    table: List[TableRow]
