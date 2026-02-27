# train_models.py
# Script to train LSTM and XGBoost models

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import joblib
from app.services.data_service import get_stock_data
from app.services.lstm_service import LSTMModel
from app.services.xgb_service import create_features
from app.config import SEQUENCE_LENGTH


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


def train_lstm(symbol="AAPL", epochs=50):
    """Train LSTM model for price prediction"""
    print(f"Training LSTM model on {symbol}...")
    
    df = get_stock_data(symbol)
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
    
    torch.save(model.state_dict(), "app/models/lstm_model.pth")
    print("LSTM model saved to app/models/lstm_model.pth")


def train_xgboost(symbol="AAPL", use_gridsearch=True):
    """Train XGBoost model with cross-validation and hyperparameter tuning"""
    print(f"\nTraining XGBoost model on {symbol}...")
    print("="*60)
    
    df = get_stock_data(symbol)
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
    
    # Add news sentiment as additional feature (mock for training)
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
        
        # Define parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
            'min_child_weight': [1, 3, 5]
        }
        
        # Use TimeSeriesSplit for cross-validation (respects temporal order)
        tscv = TimeSeriesSplit(n_splits=5)
        
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
        
        print("Training with cross-validation (this may take a few minutes)...")
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
    print("Starting model training...")
    print("Note: This requires historical data from Alpha Vantage API")
    
    # Train both models
    train_lstm(symbol="AAPL", epochs=50)
    train_xgboost(symbol="AAPL")
    
    print("\nTraining complete! Models saved in app/models/")
