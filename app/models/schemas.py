# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class PredictionRequest(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL"
            }
        }

class PredictionResponse(BaseModel):
    symbol: str
    predicted_price: float
    signal: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)
    model_version: str
    cached: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "predicted_price": 175.32,
                "signal": "BUY",
                "confidence": 0.87,
                "timestamp": "2026-02-27T10:30:00",
                "model_version": "v2.1",
                "cached": False
            }
        }

class BatchPredictionRequest(BaseModel):
    symbols: List[str] = Field(..., max_length=10, description="List of stock symbols (max 10)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbols": ["AAPL", "GOOGL", "MSFT"]
            }
        }

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total: int
    successful: int
    failed: int

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    models_loaded: bool
    cache_size: int

class MetricsResponse(BaseModel):
    total_predictions: int
    cache_hit_rate: float
    average_response_time: float
    model_version: str
    uptime: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "InvalidSymbolError",
                "detail": "Invalid stock symbol: ABC123",
                "timestamp": "2026-02-27T10:30:00"
            }
        }
