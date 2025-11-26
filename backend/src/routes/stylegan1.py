from functools import lru_cache
from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from src.models.convnext.model import ConvNeXtBinaryModel_StyleGan1


router = APIRouter(prefix="/stylegan1", tags=["stylegan1"])


@lru_cache(maxsize=1)
def get_model() -> ConvNeXtBinaryModel_StyleGan1:
    # Load weights once per process
    return ConvNeXtBinaryModel_StyleGan1().load()


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        image = Image.open(BytesIO(content)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")

    model = get_model()
    prob = model.predict(image)

    return {
        "probability": prob,
        "label": "fake" if prob >= 0.5 else "real",
    }
