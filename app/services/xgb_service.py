# app/services/xgb_service.py

import joblib
import pandas as pd
import numpy as np

def load_xgb_model():
    return joblib.load("app/models/xgb_model.pkl")


def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_histogram = macd - macd_signal
    return macd, macd_signal, macd_histogram


def get_news_sentiment(symbol):
    """
    Get news sentiment for a stock symbol
    Returns a sentiment score between -1 (negative) and 1 (positive)
    
    Note: This is a placeholder. In production, integrate with:
    - Alpha Vantage News Sentiment API
    - NewsAPI
    - Twitter/Reddit sentiment analysis
    - Financial news APIs
    """
    # Placeholder: Random sentiment for now
    # In production, replace with actual API call
    import random
    random.seed(hash(symbol) % 100)
    sentiment = random.uniform(-0.5, 0.5)
    return sentiment


def create_features(df):
    """Create advanced features including technical indicators and lag features"""
    df = df.copy()
    
    # Basic features
    df["returns"] = df["close"].pct_change()
    df["ma_10"] = df["close"].rolling(10).mean()
    df["ma_30"] = df["close"].rolling(30).mean()
    df["volatility"] = df["returns"].rolling(10).std()
    
    # RSI (Relative Strength Index)
    df["rsi"] = calculate_rsi(df["close"], period=14)
    
    # MACD indicators
    df["macd"], df["macd_signal"], df["macd_histogram"] = calculate_macd(df["close"])
    
    # Lag features (previous 5 days prices)
    for i in range(1, 6):
        df[f"close_lag_{i}"] = df["close"].shift(i)
        df[f"returns_lag_{i}"] = df["returns"].shift(i)
    
    # Price momentum
    df["momentum_5"] = df["close"] - df["close"].shift(5)
    df["momentum_10"] = df["close"] - df["close"].shift(10)
    
    # Volume features
    df["volume_ma_10"] = df["volume"].rolling(10).mean()
    df["volume_ratio"] = df["volume"] / df["volume_ma_10"]
    
    # Bollinger Bands
    df["bb_middle"] = df["close"].rolling(20).mean()
    bb_std = df["close"].rolling(20).std()
    df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
    df["bb_lower"] = df["bb_middle"] - (bb_std * 2)
    df["bb_position"] = (df["close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])
    
    df = df.dropna()
    return df


def predict_signal(model, df, symbol="UNKNOWN"):
    """Predict trading signal with advanced features"""
    df = create_features(df)
    
    # Get news sentiment
    news_sentiment = get_news_sentiment(symbol)
    
    latest = df.iloc[-1]
    
    # Feature list matching training
    feature_columns = [
        "returns", "ma_10", "ma_30", "volatility",
        "rsi", "macd", "macd_signal", "macd_histogram",
        "close_lag_1", "close_lag_2", "close_lag_3", "close_lag_4", "close_lag_5",
        "returns_lag_1", "returns_lag_2", "returns_lag_3", "returns_lag_4", "returns_lag_5",
        "momentum_5", "momentum_10",
        "volume_ratio", "bb_position"
    ]
    
    features = latest[feature_columns].values.reshape(1, -1)
    
    # Add news sentiment as additional feature
    features = np.append(features, [[news_sentiment]], axis=1)
    
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].max()
    
    signal = "BUY" if prediction == 1 else "SELL"
    
    return signal, float(probability)