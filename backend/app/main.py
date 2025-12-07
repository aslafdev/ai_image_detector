from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importujemy nasz router z pliku routers/models.py
# Upewnij się, że w routers/models.py masz linię: router = APIRouter()
from routes import models 

app = FastAPI(
    title="AI Model Manager",
    description="API do zarządzania modelami sieci neuronowych",
    version="1.0.0"
)

origins = [
    "http://localhost:8080",  # Domyślny port Vue 2/CLI
    "http://localhost:5173",  # Domyślny port Vue 3/Vite
    "http://127.0.0.1:8080",
    "*"                       # Opcjonalnie: odblokuj wszystko na czas devu
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # Pozwalamy na POST, GET, DELETE, itd.
    allow_headers=["*"],
)

app.include_router(models.router)

@app.get("/")
def root():
    return {"message": "AI Model Manager API is running!"}


if __name__ == "__main__":
    import uvicorn

    # Use the fully qualified path so uvicorn can reload correctly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
