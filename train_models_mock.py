# train_models_mock.py - Training with mock data for testing
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import joblib
from app.services.lstm_service import LSTMModel
from app.config import SEQUENCE_LENGTH


def create_mock_stock_data(days=200):
    """Create realistic mock stock data"""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
    
    # Generate realistic price movement
    np.random.seed(42)
    base_price = 150
    returns = np.random.normal(0.001, 0.02, days)
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
        'high': prices * (1 + np.random.uniform(0, 0.02, days)),
        'low': prices * (1 + np.random.uniform(-0.02, 0, days)),
        'close': prices,
        'volume': np.random.randint(50000000, 150000000, days).astype(float)
    }, index=dates)
    
    return df


def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_histogram = macd - macd_signal
    return macd, macd_signal, macd_histogram


def create_features(df):
    """Create advanced features"""
    df = df.copy()
    
    # Basic features
    df["returns"] = df["close"].pct_change()
    df["ma_10"] = df["close"].rolling(10).mean()
    df["ma_30"] = df["close"].rolling(30).mean()
    df["volatility"] = df["returns"].rolling(10).std()
    
    # RSI
    df["rsi"] = calculate_rsi(df["close"], period=14)
    
    # MACD
    df["macd"], df["macd_signal"], df["macd_histogram"] = calculate_macd(df["close"])
    
    # Lag features (previous 5 days)
    for i in range(1, 6):
        df[f"close_lag_{i}"] = df["close"].shift(i)
        df[f"returns_lag_{i}"] = df["returns"].shift(i)
    
    # Momentum
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


def prepare_lstm_data(df, sequence_length=30):
    """Prepare data for LSTM training"""
    scaler = MinMaxScaler()
    close_prices = df["close"].values.reshape(-1, 1)
    scaled = scaler.fit_transform(close_prices)
    
    X, y = [], []
    for i in range(len(scaled) - sequence_length):
        X.append(scaled[i:i + sequence_length])
        y.append(scaled[i + sequence_length])
    
    return np.array(X), np.array(y), scaler


def train_lstm(df, epochs=50):
    """Train LSTM model for price prediction"""
    print("Training LSTM model...")
    
    X, y, scaler = prepare_lstm_data(df, SEQUENCE_LENGTH)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    X_train = torch.FloatTensor(X_train)
    y_train = torch.FloatTensor(y_train)
    X_test = torch.FloatTensor(X_test)
    y_test = torch.FloatTensor(y_test)
    
    model = LSTMModel()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
    
    # Test the model
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test)
        test_loss = criterion(test_outputs, y_test)
        print(f"Test Loss: {test_loss.item():.4f}")
    
    torch.save(model.state_dict(), "app/models/lstm_model.pth")
    print("✓ LSTM model saved to app/models/lstm_model.pth")


def train_xgboost(df, use_gridsearch=True):
    """Train XGBoost model with cross-validation and hyperparameter tuning"""
    print("\nTraining XGBoost model...")
    print("="*60)
    
    df = create_features(df)
    
    # Create labels: 1 if next day price goes up, 0 otherwise
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
    df = df.dropna()
    
    # Feature list with all advanced features including lag features
    features = [
        "returns", "ma_10", "ma_30", "volatility",
        "rsi", "macd", "macd_signal", "macd_histogram",
        "close_lag_1", "close_lag_2", "close_lag_3", "close_lag_4", "close_lag_5",
        "returns_lag_1", "returns_lag_2", "returns_lag_3", "returns_lag_4", "returns_lag_5",
        "momentum_5", "momentum_10",
        "volume_ratio", "bb_position"
    ]
    
    X = df[features]
    y = df["target"]
    
    # Add news sentiment as additional feature (mock)
    np.random.seed(42)
    news_sentiment = np.random.uniform(-0.5, 0.5, len(X))
    X["news_sentiment"] = news_sentiment
    
    print(f"Dataset: {len(X)} samples, {len(features)+1} features")
    print(f"Class distribution: {y.value_counts().to_dict()}")
    
    # Split data (time series - no shuffle)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    if use_gridsearch:
        print("\n🔍 Performing GridSearchCV for hyperparameter tuning...")
        
        # Define parameter grid (smaller for faster training with mock data)
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }
        
        # Use TimeSeriesSplit for cross-validation (respects temporal order)
        tscv = TimeSeriesSplit(n_splits=3)
        
        # Base model
        base_model = xgb.XGBClassifier(
            random_state=42,
            eval_metric='logloss'
        )
        
        # GridSearchCV
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=tscv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        print("Training with cross-validation...")
        grid_search.fit(X_train, y_train)
        
        print(f"\n✓ Best parameters found:")
        for param, value in grid_search.best_params_.items():
            print(f"  {param}: {value}")
        print(f"\n✓ Best cross-validation score: {grid_search.best_score_:.4f}")
        
        # Use best model
        model = grid_search.best_estimator_
    else:
        print("\n🚀 Training with default parameters...")
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        model.fit(X_train, y_train)
    
    # Evaluate on test set
    print("\n📊 Model Evaluation:")
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"Train Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Classification report
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['SELL', 'BUY']))
    
    # Confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  True Negatives (SELL): {cm[0][0]}")
    print(f"  False Positives (predicted BUY, actual SELL): {cm[0][1]}")
    print(f"  False Negatives (predicted SELL, actual BUY): {cm[1][0]}")
    print(f"  True Positives (BUY): {cm[1][1]}")
    
    # Feature importance
    feature_importance = sorted(
        zip(X.columns, model.feature_importances_), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    
    print("\n🎯 Top 10 Important Features:")
    for i, (feat, importance) in enumerate(feature_importance, 1):
        print(f"  {i}. {feat}: {importance:.4f}")
    
    # Save model
    joblib.dump(model, "app/models/xgb_model.pkl")
    print("\n✓ XGBoost model saved to app/models/xgb_model.pkl")
    print("="*60)


if __name__ == "__main__":
    print("=" * 60)
    print("TRAINING WITH MOCK DATA (for testing)")
    print("=" * 60)
    print("\nNote: Using mock data because Alpha Vantage API limit reached")
    print("Once API limit resets, run train_models.py for real data\n")
    
    # Create mock data
    print("Generating mock stock data...")
    df = create_mock_stock_data(days=200)
    print(f"✓ Generated {len(df)} days of mock data")
    print(f"  Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}\n")
    
    # Train both models
    train_lstm(df, epochs=50)
    train_xgboost(df)
    
    print("\n" + "=" * 60)
    print("✓ Training complete! Models saved in app/models/")
    print("=" * 60)
    print("\nYou can now run the API server:")
    print("  uvicorn app.main:app --reload")
