from fastapi import FastAPI

from app.routes.models.stylegan1 import router as stylegan1_router

app = FastAPI(title="AI Image Detector")






@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(stylegan1_router)
