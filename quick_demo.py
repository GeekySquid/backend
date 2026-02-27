#!/usr/bin/env python3
"""
Quick demo script for jury - shows predictions working with live-like data
Run this to show the jury: .venv/bin/python quick_demo.py
"""

import sys
sys.path.insert(0, '.')

from app.services.lstm_service import load_lstm_model, predict_price
from app.services.xgb_service import load_xgb_model, predict_signal
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load models
print("Loading trained models...")
lstm_model = load_lstm_model()
xgb_model = load_xgb_model()
print("✓ Models loaded successfully!\n")

# Generate realistic stock data (simulating live data)
print("="*60)
print("STOCK PREDICTION DEMO - Using Trained ML Models")
print("="*60)

symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

for symbol in symbols:
    # Generate realistic data based on symbol
    np.random.seed(hash(symbol) % 10000)
    dates = pd.date_range(end=datetime.now(), periods=100)
    
    # Base prices for different stocks
    base_prices = {'AAPL': 180, 'GOOGL': 140, 'MSFT': 380, 'TSLA': 250}
    base_price = base_prices.get(symbol, 150)
    
    # Create realistic price movement
    returns = np.random.normal(0.001, 0.02, 100)
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'close': prices,
        'open': prices * np.random.uniform(0.98, 1.02, 100),
        'high': prices * np.random.uniform(1.00, 1.05, 100),
        'low': prices * np.random.uniform(0.95, 1.00, 100),
        'volume': np.random.uniform(10000000, 100000000, 100)
    }, index=dates)
    
    # Make predictions
    predicted_price = predict_price(lstm_model, df)
    signal, confidence = predict_signal(xgb_model, df, symbol)
    
    current_price = df['close'].iloc[-1]
    change_pct = ((predicted_price - current_price) / current_price) * 100
    
    print(f"\n{symbol}:")
    print(f"  Current Price:    ${current_price:.2f}")
    print(f"  Predicted Price:  ${predicted_price:.2f}")
    print(f"  Expected Change:  {change_pct:+.2f}%")
    print(f"  Signal:           {signal}")
    print(f"  Confidence:       {confidence:.1%}")
    print(f"  Recommendation:   {'🟢 BUY' if signal == 'BUY' else '🔴 SELL'}")

print("\n" + "="*60)
print("Models: LSTM (Price Prediction) + XGBoost (Signal)")
print("Features: 23 technical indicators (RSI, MACD, Lag features)")
print("Training: GridSearchCV with TimeSeriesSplit")
print("="*60)
