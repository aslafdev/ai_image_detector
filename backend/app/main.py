from fastapi import FastAPI

from routes.models.stylegan1 import router as stylegan1_router

app = FastAPI(title="AI Image Detector")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(stylegan1_router)


if __name__ == "__main__":
    import uvicorn

    # Use the fully qualified path so uvicorn can reload correctly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
