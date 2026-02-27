# app/routes/metrics.py

from fastapi import APIRouter
from datetime import datetime
import time

from app.core.config import settings
from app.core.cache import cache
from app.models.schemas import MetricsResponse

router = APIRouter()

# Track metrics (in-memory, replace with database in production)
_metrics = {
    "total_predictions": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "total_requests": 0,
    "total_response_time": 0.0,
    "start_time": time.time()
}

def increment_prediction():
    """Increment prediction counter"""
    _metrics["total_predictions"] += 1

def increment_cache_hit():
    """Increment cache hit counter"""
    _metrics["cache_hits"] += 1

def increment_cache_miss():
    """Increment cache miss counter"""
    _metrics["cache_misses"] += 1

def record_response_time(duration: float):
    """Record response time"""
    _metrics["total_requests"] += 1
    _metrics["total_response_time"] += duration

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get API metrics
    
    Returns:
    - Total predictions made
    - Cache hit rate
    - Average response time
    - Model version
    - Uptime
    """
    total_cache_requests = _metrics["cache_hits"] + _metrics["cache_misses"]
    cache_hit_rate = (
        _metrics["cache_hits"] / total_cache_requests 
        if total_cache_requests > 0 else 0.0
    )
    
    avg_response_time = (
        _metrics["total_response_time"] / _metrics["total_requests"]
        if _metrics["total_requests"] > 0 else 0.0
    )
    
    uptime_seconds = time.time() - _metrics["start_time"]
    uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
    
    return MetricsResponse(
        total_predictions=_metrics["total_predictions"],
        cache_hit_rate=round(cache_hit_rate, 4),
        average_response_time=round(avg_response_time * 1000, 2),  # ms
        model_version=settings.MODEL_VERSION,
        uptime=uptime_str
    )

@router.post("/metrics/reset")
async def reset_metrics():
    """Reset metrics (admin only in production)"""
    _metrics["total_predictions"] = 0
    _metrics["cache_hits"] = 0
    _metrics["cache_misses"] = 0
    _metrics["total_requests"] = 0
    _metrics["total_response_time"] = 0.0
    _metrics["start_time"] = time.time()
    
    return {"message": "Metrics reset successfully"}
