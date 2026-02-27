# Changelog

## Version 2.1 - Hyperparameter Tuning & Cross-Validation (Current)

### Added
- ✅ **GridSearchCV** - Automated hyperparameter tuning
- ✅ **TimeSeriesSplit** - Cross-validation respecting temporal order
- ✅ **Classification Report** - Precision, recall, F1-score metrics
- ✅ **Confusion Matrix** - Detailed prediction analysis
- ✅ **Extended Feature Importance** - Top 10 features displayed

### Improved
- XGBoost model now auto-tunes 6 hyperparameters
- Cross-validation with 3-5 folds prevents overfitting
- Better model evaluation with comprehensive metrics
- Lag features confirmed as most important predictors

### Model Performance
- Cross-validation score: 58.82%
- Test accuracy: 60%
- Top features: returns_lag_3, volatility, volume_ratio

### Training Time
- With GridSearch: 2-5 minutes (48-144 combinations)
- Without GridSearch: < 1 minute

## Version 2.0 - Enhanced Features

### Added
- ✅ **RSI (Relative Strength Index)** - 14-period momentum indicator
- ✅ **MACD Indicators** - MACD line, signal line, and histogram
- ✅ **Lag Features** - Previous 5 days closing prices and returns
- ✅ **Momentum Indicators** - 5-day and 10-day price momentum
- ✅ **Volume Analysis** - Volume ratio compared to 10-day average
- ✅ **Bollinger Bands** - Upper, middle, lower bands and position indicator
- ✅ **News Sentiment** - Placeholder for sentiment analysis (ready for API integration)

### Improved
- XGBoost model now uses 23 features (up from 4)
- Better prediction accuracy with advanced technical indicators
- Feature importance analysis shows MACD and volume as top indicators

### Model Performance
- Top 5 Important Features:
  1. MACD (7.70%)
  2. Volume Ratio (7.54%)
  3. MACD Signal (6.64%)
  4. Returns Lag 3 (5.95%)
  5. Close Lag 3 (5.36%)

## Version 1.0 - Initial Release

### Features
- LSTM model for price prediction
- XGBoost model for buy/sell signals
- Basic technical indicators (MA, volatility, returns)
- Alpha Vantage API integration
- FastAPI REST endpoint
- CORS support for frontend integration

### Models
- LSTM: 30-day sequence, 50 hidden units
- XGBoost: 4 basic features

## Roadmap

### Version 2.2 (Planned)
- [ ] Early stopping for XGBoost
- [ ] Bayesian optimization for hyperparameters
- [ ] Model performance monitoring dashboard
- [ ] Automated retraining pipeline

### Version 3.0 (Future)
- [ ] Real-time news sentiment API integration
- [ ] Social media sentiment analysis
- [ ] Multiple timeframe analysis
- [ ] Portfolio optimization
- [ ] Risk management features
- [ ] Real-time WebSocket updates
- [ ] Advanced ML models (Transformer, Attention mechanisms)
