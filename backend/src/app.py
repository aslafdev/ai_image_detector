from fastapi import FastAPI

app = FastAPI(title="AI Image Detector")



@app.get("/health")
def health_check():
    return {"status": "ok"}
