# app/routers/models.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.dependencies import get_manager
from services.model_manager import (
    ModelManager, 
    ModelNotFoundError, 
    ModelMemoryLimitError, 
    ModelLoadingError,
    ModelNotLoadedError
)
from schemas.model_info import ModelInfoOut
from schemas.model_results import PredictionResult, TableCell
from fastapi import UploadFile, File

from PIL import Image
import io
import time


router = APIRouter(prefix='/models', tags=['models'])


@router.get("/loaded", response_model=List[ModelInfoOut])
def list_loaded_models(
    manager: ModelManager = Depends(get_manager)
):
    """Zwraca tylko modele znajdujące się w pamięci (RAM/VRAM)."""
    return manager.get_loaded_models()


@router.get("/", response_model=List[ModelInfoOut])
def list_all_models(
    manager: ModelManager = Depends(get_manager)
):
    """Zwraca listę wszystkich dostępnych modeli (do budowania menu)."""
    return manager.get_available_models()


@router.post("/{model_id}/load")
async def load_model(
    model_id: str, 
    manager: ModelManager = Depends(get_manager)
):
    try:
        await manager.load_model(model_id)
        return {"status": "ok", "message": f"Model {model_id} loaded"}
        
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except ModelMemoryLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=str(e)
        )
    except ModelLoadingError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.post("/{model_id}/unload")
async def unload_model(
    model_id: str, 
    manager: ModelManager = Depends(get_manager)
):
    try:
        await manager.unload_model(model_id)
        return {"status": "ok", "message": f"Model {model_id} unloaded"}
        
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error unloading model: {str(e)}"
        )

@router.post("/{model_id}/predict", response_model=PredictionResult)
async def predict(
    model_id: str,
    file: UploadFile = File(...),
    manager: ModelManager = Depends(get_manager)
):

    content = await file.read()
    image = Image.open(io.BytesIO(content)).convert("RGB")
    image.filename = file.filename
    model_cells, prediction_time = await manager.predict(model_id, image)


    return PredictionResult(
        filename=file.filename,
        cells=model_cells ,              # To przyszło z modelu
        prediction_time=prediction_time 
    )