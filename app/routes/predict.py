# app/routes/predict.py

from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
import json
from datetime import datetime
import numpy as np
import pandas as pd

from app.core.config import settings
from app.core.logging import logger
from app.core.cache import cache
from app.core.validators import validate_stock_symbol, validate_symbols_batch
from app.core.exceptions import DataFetchError, ModelLoadError, PredictionError
from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from app.services.data_service import get_stock_data
from app.services.lstm_service import load_lstm_model, predict_price
from app.services.xgb_service import load_xgb_model, predict_signal

router = APIRouter()

# Load models at startup
try:
    lstm_model = load_lstm_model()
    xgb_model = load_xgb_model()
    logger.info("Models loaded successfully")
except Exception as e:
    logger.error(f"Failed to load models: {e}")
    lstm_model = None
    xgb_model = None


def get_prediction_from_cache(symbol: str):
    """Get prediction from cache if available"""
    if not settings.CACHE_ENABLED:
        return None
    
    cache_key = f"prediction:{symbol}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        logger.info(f"Cache hit for symbol: {symbol}")
        return cached_data
    
    return None


def save_prediction_to_cache(symbol: str, prediction: dict):
    """Save prediction to cache"""
    if not settings.CACHE_ENABLED:
        return
    
    cache_key = f"prediction:{symbol}"
    cache.set(cache_key, prediction, ttl=settings.CACHE_TTL)
    logger.info(f"Cached prediction for symbol: {symbol}")


async def make_prediction(symbol: str) -> PredictionResponse:
    """Core prediction logic"""
    # Validate symbol
    symbol = validate_stock_symbol(symbol)
    
    # Check cache
    cached_prediction = get_prediction_from_cache(symbol)
    if cached_prediction:
        cached_prediction["cached"] = True
        return PredictionResponse(**cached_prediction)
    
    # Check if models are loaded
    if lstm_model is None or xgb_model is None:
        raise ModelLoadError("LSTM or XGBoost")
    
    try:
        # Fetch stock data
        logger.info(f"Fetching data for symbol: {symbol}")
        df = get_stock_data(symbol)
        
        # Make predictions
        logger.info(f"Making predictions for symbol: {symbol}")
        predicted_price = predict_price(lstm_model, df)
        signal, confidence = predict_signal(xgb_model, df, symbol)
        
        # Create response
        prediction = PredictionResponse(
            symbol=symbol,
            predicted_price=float(predicted_price),
            signal=signal,
            confidence=float(confidence),
            timestamp=datetime.now(),
            model_version=settings.MODEL_VERSION,
            cached=False
        )
        
        # Save to cache
        save_prediction_to_cache(symbol, prediction.dict())
        
        logger.info(
            f"Prediction successful for {symbol}",
            extra={
                "predicted_price": predicted_price,
                "signal": signal,
                "confidence": confidence
            }
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Prediction failed for {symbol}: {str(e)}")
        if "API limit" in str(e) or "invalid symbol" in str(e).lower():
            raise DataFetchError(str(e))
        raise PredictionError(f"Failed to generate prediction: {str(e)}")


@router.get("/predict", response_model=PredictionResponse)
async def predict(symbol: str):
    """
    Get stock prediction for a single symbol using LIVE DATA
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
    
    Returns:
    - Predicted next-day closing price
    - Trading signal (BUY/SELL)
    - Confidence score (0-1)
    - Timestamp and model version
    """
    return await make_prediction(symbol)


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """
    Get stock predictions for multiple symbols (max 10)
    
    - **symbols**: List of stock ticker symbols
    
    Returns:
    - List of predictions
    - Success/failure counts
    """
    # Validate symbols
    symbols = validate_symbols_batch(request.symbols)
    
    predictions = []
    successful = 0
    failed = 0
    
    for symbol in symbols:
        try:
            prediction = await make_prediction(symbol)
            predictions.append(prediction)
            successful += 1
        except Exception as e:
            logger.error(f"Batch prediction failed for {symbol}: {str(e)}")
            failed += 1
            # Add error placeholder
            predictions.append(
                PredictionResponse(
                    symbol=symbol,
                    predicted_price=0.0,
                    signal="ERROR",
                    confidence=0.0,
                    timestamp=datetime.now(),
                    model_version=settings.MODEL_VERSION,
                    cached=False
                )
            )
    
    return BatchPredictionResponse(
        predictions=predictions,
        total=len(symbols),
        successful=successful,
        failed=failed
    )


@router.get("/predict/demo", response_model=PredictionResponse)
async def predict_demo(symbol: str):
    """
    DEMO ENDPOINT - Get stock prediction using mock data (for testing/demo purposes)
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
    
    This endpoint uses pre-generated mock data and doesn't call external APIs.
    Perfect for demonstrations when API limits are reached.
    
    Returns:
    - Predicted next-day closing price
    - Trading signal (BUY/SELL)
    - Confidence score (0-1)
    - Timestamp and model version
    """
    # Validate symbol
    symbol = validate_stock_symbol(symbol)
    
    # Check if models are loaded
    if lstm_model is None or xgb_model is None:
        raise ModelLoadError("LSTM or XGBoost")
    
    logger.info(f"Demo prediction for symbol: {symbol}")
    
    # Generate mock stock data (100 days)
    np.random.seed(hash(symbol) % 10000)
    dates = pd.date_range(end=datetime.now(), periods=100)
    base_price = np.random.uniform(50, 500)
    
    # Create realistic price movement
    returns = np.random.normal(0.001, 0.02, 100)
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'close': prices,
        'open': prices * np.random.uniform(0.98, 1.02, 100),
        'high': prices * np.random.uniform(1.00, 1.05, 100),
        'low': prices * np.random.uniform(0.95, 1.00, 100),
        'volume': np.random.uniform(1000000, 10000000, 100)
    }, index=dates)
    
    try:
        # Make predictions using the trained models
        predicted_price = predict_price(lstm_model, df)
        signal, confidence = predict_signal(xgb_model, df, symbol)
        
        prediction = PredictionResponse(
            symbol=symbol,
            predicted_price=float(predicted_price),
            signal=signal,
            confidence=float(confidence),
            timestamp=datetime.now(),
            model_version=settings.MODEL_VERSION + "-DEMO",
            cached=False
        )
        
        logger.info(
            f"Demo prediction successful for {symbol}",
            extra={
                "predicted_price": predicted_price,
                "signal": signal,
                "confidence": confidence
            }
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Demo prediction failed for {symbol}: {str(e)}")
        raise PredictionError(f"Failed to generate demo prediction: {str(e)}")