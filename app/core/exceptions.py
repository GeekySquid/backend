# app/core/exceptions.py
from fastapi import HTTPException, status

class StockAPIException(HTTPException):
    """Base exception for Stock API"""
    pass

class InvalidSymbolError(StockAPIException):
    """Invalid stock symbol"""
    def __init__(self, symbol: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol: {symbol}. Must be 1-5 uppercase letters."
        )

class DataFetchError(StockAPIException):
    """Error fetching stock data"""
    def __init__(self, message: str = "Failed to fetch stock data"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=message
        )

class ModelLoadError(StockAPIException):
    """Error loading ML model"""
    def __init__(self, model_name: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to load model: {model_name}"
        )

class PredictionError(StockAPIException):
    """Error during prediction"""
    def __init__(self, message: str = "Prediction failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )

class RateLimitExceeded(StockAPIException):
    """Rate limit exceeded"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
