# app/routes/health.py

from fastapi import APIRouter
from datetime import datetime
import os

from app.core.config import settings
from app.core.cache import cache
from app.models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
    - API status
    - Version
    - Models loaded status
    - Cache size
    """
    # Check if models exist
    lstm_model_exists = os.path.exists("app/models/lstm_model.pth")
    xgb_model_exists = os.path.exists("app/models/xgb_model.pkl")
    models_loaded = lstm_model_exists and xgb_model_exists
    
    return HealthResponse(
        status="healthy" if models_loaded else "degraded",
        version=settings.APP_VERSION,
        timestamp=datetime.now(),
        models_loaded=models_loaded,
        cache_size=cache.size()
    )

@router.get("/health/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    lstm_model_exists = os.path.exists("app/models/lstm_model.pth")
    xgb_model_exists = os.path.exists("app/models/xgb_model.pkl")
    
    if lstm_model_exists and xgb_model_exists:
        return {"status": "ready"}
    return {"status": "not ready"}, 503

@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}
