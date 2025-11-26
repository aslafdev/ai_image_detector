from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from time import time
from app.models.manager import get_model


router = APIRouter(prefix="/stylegan1", tags=["stylegan1"])


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        image = Image.open(BytesIO(content)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")

    model = get_model("stylegan1")
    start_time = time()
    prob = model.predict(image)
    end_time = time()
    elapsed_time = end_time - start_time

    return {
        "name": file.filename,
        "probability": prob,
        "label": "real" if prob >= 0.5 else "fake",
        "elapsed_time": elapsed_time,
    }
