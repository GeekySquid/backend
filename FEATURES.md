# Advanced Features Documentation

## Technical Indicators

### 1. RSI (Relative Strength Index)
- **Purpose**: Measures momentum and identifies overbought/oversold conditions
- **Range**: 0-100
- **Interpretation**:
  - RSI > 70: Overbought (potential sell signal)
  - RSI < 30: Oversold (potential buy signal)
  - RSI = 50: Neutral

### 2. MACD (Moving Average Convergence Divergence)
- **Components**:
  - MACD Line: 12-day EMA - 26-day EMA
  - Signal Line: 9-day EMA of MACD
  - Histogram: MACD - Signal Line
- **Interpretation**:
  - MACD crosses above signal: Bullish signal
  - MACD crosses below signal: Bearish signal
  - Histogram expanding: Trend strengthening

### 3. Bollinger Bands
- **Components**:
  - Middle Band: 20-day SMA
  - Upper Band: Middle + (2 × standard deviation)
  - Lower Band: Middle - (2 × standard deviation)
- **BB Position**: Shows where price is relative to bands (0-1)
  - Near 1: Price at upper band (overbought)
  - Near 0: Price at lower band (oversold)

## Lag Features

### Previous 5 Days Prices
- `close_lag_1` to `close_lag_5`: Closing prices from 1-5 days ago
- `returns_lag_1` to `returns_lag_5`: Returns from 1-5 days ago

**Purpose**: Captures recent price patterns and trends

## Momentum Indicators

### Price Momentum
- `momentum_5`: Price change over 5 days
- `momentum_10`: Price change over 10 days

**Purpose**: Measures the rate of price change

## Volume Analysis

### Volume Ratio
- `volume_ratio`: Current volume / 10-day average volume
- **Interpretation**:
  - > 1: Higher than average volume (strong interest)
  - < 1: Lower than average volume (weak interest)

## News Sentiment

### Sentiment Score
- **Range**: -1 (very negative) to +1 (very positive)
- **Source**: Aggregated from financial news APIs
- **Note**: Currently using placeholder. In production, integrate with:
  - Alpha Vantage News Sentiment API
  - NewsAPI
  - Twitter/Reddit sentiment analysis
  - Financial news aggregators

## Feature Importance

Based on training, the top 5 most important features are:
1. **MACD**: Primary trend indicator
2. **Volume Ratio**: Trading activity strength
3. **MACD Signal**: Trend confirmation
4. **Returns Lag 3**: 3-day historical return
5. **Close Lag 3**: 3-day historical price

## Model Architecture

### XGBoost Classifier
- **Total Features**: 23
  - 4 basic features (returns, MA, volatility)
  - 3 MACD components
  - 1 RSI
  - 10 lag features (5 price + 5 returns)
  - 2 momentum features
  - 2 volume features
  - 1 Bollinger Band position
  - 1 news sentiment

### LSTM Model
- **Input**: 30-day price sequences
- **Architecture**: 
  - LSTM layer (50 hidden units)
  - Fully connected output layer
- **Purpose**: Predicts next-day closing price

## Integration Example

```python
# The model automatically calculates all features
response = requests.get('http://localhost:8000/predict?symbol=AAPL')
data = response.json()

# Response includes predictions based on all 23 features
{
  "symbol": "AAPL",
  "predicted_price": 175.32,  # LSTM prediction
  "signal": "BUY",             # XGBoost classification
  "confidence": 0.87           # Model confidence
}
```

## Future Enhancements

### Planned Features
1. **Real-time News Sentiment**: Integration with news APIs
2. **Social Media Sentiment**: Twitter/Reddit analysis
3. **Earnings Data**: Quarterly earnings impact
4. **Sector Performance**: Industry-wide trends
5. **Market Indices**: S&P 500, NASDAQ correlation
6. **Options Data**: Put/call ratios
7. **Insider Trading**: Insider buy/sell activity

### API Integrations
- Alpha Vantage News Sentiment
- NewsAPI for financial news
- Twitter API for social sentiment
- Reddit API for retail investor sentiment
- Yahoo Finance for additional data

## Performance Metrics

### Current Model Performance
- **Training Accuracy**: 100% (may indicate overfitting)
- **Test Accuracy**: 45.71%
- **Confidence Range**: 85-95%

### Recommendations
- Retrain with more data for better generalization
- Use real market data instead of mock data
- Implement cross-validation
- Add regularization to prevent overfitting
