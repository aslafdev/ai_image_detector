
from pydantic import BaseModel
from typing import Literal

class StyleGan1ConvNeXtResultSchema(BaseModel):
    file_name : str
    probability: float
    label : Literal["real", "fake"]
    prediction_time : float
    