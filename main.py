from fastapi import FastAPI

from app.core_config.config import Settings
settings = Settings()
app = FastAPI(title=settings.service_name)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "env": settings.env,
        "service": settings.service_name
    }