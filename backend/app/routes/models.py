# app/routers/models.py

from typing  import List
from fastapi import APIRouter, Depends, HTTPException
from services.dependencies import get_manager  
from services.model_manager import ModelManager
from schemas.model_info import ModelInfoOut, ModelStatus

router = APIRouter(prefix = '/models', tags=['models'])


@router.get("/loaded", response_model=List[ModelInfoOut])
def list_loaded_models(
    manager: ModelManager = Depends(get_manager)
):
    return manager.get_loaded_models()



@router.get("/", response_model=List[ModelInfoOut])
def list_all_models(
    manager: ModelManager = Depends(get_manager)
):
   
    return manager.get_available_models()


@router.post("/{model_id}/load")
async def load_model(
    model_id: str, 
    manager: ModelManager = Depends(get_manager)
):
    # manager tutaj to ta sama instancja co wyżej, więc stan jest zachowany
    await manager.load_model(model_id)
    return {"status": "ok"}