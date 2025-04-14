from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.service_name)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "env": settings.env,
        "service": settings.service_name
    }