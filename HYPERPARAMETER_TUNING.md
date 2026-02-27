# Hyperparameter Tuning & Cross-Validation

## Overview

The XGBoost model now uses **GridSearchCV** with **TimeSeriesSplit** cross-validation for optimal hyperparameter selection.

## Cross-Validation Strategy

### TimeSeriesSplit
- **Why**: Respects temporal order of stock data
- **Splits**: 3-5 folds depending on dataset size
- **Advantage**: Prevents data leakage from future to past

### Traditional K-Fold vs TimeSeriesSplit

```
K-Fold (❌ Wrong for time series):
[Train][Test][Train][Test][Train]  # Trains on future, tests on past

TimeSeriesSplit (✅ Correct):
[Train][Test]                      # Fold 1
[Train----][Test]                  # Fold 2
[Train---------][Test]             # Fold 3
```

## Hyperparameter Grid

### Parameters Tuned

1. **n_estimators**: [50, 100, 200]
   - Number of boosting rounds
   - More trees = better fit but slower training

2. **max_depth**: [3, 5, 7]
   - Maximum tree depth
   - Deeper trees = more complex patterns but risk overfitting

3. **learning_rate**: [0.01, 0.1, 0.3]
   - Step size shrinkage
   - Lower = more conservative, needs more trees

4. **subsample**: [0.8, 1.0]
   - Fraction of samples used per tree
   - < 1.0 helps prevent overfitting

5. **colsample_bytree**: [0.8, 1.0]
   - Fraction of features used per tree
   - < 1.0 adds randomness, reduces overfitting

6. **min_child_weight**: [1, 3, 5]
   - Minimum sum of instance weight in a child
   - Higher = more conservative

## Best Parameters Found

From the latest training run:

```python
{
    'colsample_bytree': 0.8,
    'learning_rate': 0.1,
    'max_depth': 3,
    'n_estimators': 100,
    'subsample': 1.0
}
```

### Interpretation
- **max_depth=3**: Shallow trees prevent overfitting
- **learning_rate=0.1**: Moderate learning rate
- **n_estimators=100**: 100 boosting rounds
- **colsample_bytree=0.8**: Uses 80% of features per tree
- **subsample=1.0**: Uses all samples

## Model Performance

### Cross-Validation Score
- **Best CV Score**: 0.5882 (58.82% accuracy)

### Test Set Performance
- **Train Accuracy**: 100% (overfitting indicator)
- **Test Accuracy**: 60%

### Classification Metrics

```
              precision    recall  f1-score   support
        SELL       0.59      0.59      0.59        17
         BUY       0.61      0.61      0.61        18
    accuracy                           0.60        35
```

### Confusion Matrix

```
                Predicted
              SELL    BUY
Actual SELL    10      7
       BUY      7     11
```

## Feature Importance (Top 10)

After hyperparameter tuning:

1. **returns_lag_3** (6.82%) - 3-day historical return
2. **volatility** (6.30%) - Price volatility
3. **volume_ratio** (5.67%) - Volume vs average
4. **returns_lag_4** (5.66%) - 4-day historical return
5. **macd_histogram** (5.45%) - MACD histogram
6. **macd_signal** (4.83%) - MACD signal line
7. **returns_lag_2** (4.78%) - 2-day historical return
8. **close_lag_4** (4.78%) - 4-day historical price
9. **macd** (4.75%) - MACD line
10. **returns_lag_5** (4.68%) - 5-day historical return

### Key Insights
- **Lag features dominate**: Historical returns are most predictive
- **MACD indicators**: Strong trend indicators
- **Volume ratio**: Trading activity matters
- **Volatility**: Market uncertainty is important

## Training Options

### With GridSearch (Recommended)
```bash
python3 train_models_mock.py
```

This will:
- Test 48 parameter combinations (mock data)
- Test 144 parameter combinations (real data)
- Use 3-5 fold cross-validation
- Select best parameters automatically
- Take 2-5 minutes

### Without GridSearch (Fast)
Edit the training script:
```python
train_xgboost(df, use_gridsearch=False)
```

This will:
- Use default parameters
- Train in < 1 minute
- Good for quick testing

## Preventing Overfitting

### Current Issues
- Train accuracy: 100%
- Test accuracy: 60%
- **Gap indicates overfitting**

### Solutions Implemented
1. ✅ Cross-validation with TimeSeriesSplit
2. ✅ Hyperparameter tuning
3. ✅ Feature subsampling (colsample_bytree)
4. ✅ Shallow trees (max_depth=3)

### Additional Recommendations
1. **More data**: Collect more historical data
2. **Feature selection**: Remove less important features
3. **Regularization**: Increase min_child_weight
4. **Early stopping**: Stop when validation score plateaus
5. **Ensemble methods**: Combine multiple models

## Customizing Hyperparameter Grid

Edit `train_models.py` or `train_models_mock.py`:

```python
param_grid = {
    'n_estimators': [100, 200, 300],      # Add more options
    'max_depth': [3, 5, 7, 9],            # Try deeper trees
    'learning_rate': [0.01, 0.05, 0.1],   # Finer granularity
    'subsample': [0.7, 0.8, 0.9, 1.0],    # More options
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
    'min_child_weight': [1, 3, 5, 7],
    'gamma': [0, 0.1, 0.2],               # Add new parameter
    'reg_alpha': [0, 0.1, 1],             # L1 regularization
    'reg_lambda': [1, 1.5, 2]             # L2 regularization
}
```

**Warning**: More parameters = longer training time
- 48 combinations → ~2 minutes
- 144 combinations → ~5 minutes
- 1000+ combinations → 30+ minutes

## Monitoring Training

The training script outputs:
1. Dataset size and class distribution
2. GridSearch progress
3. Best parameters found
4. Cross-validation score
5. Train/test accuracy
6. Classification report
7. Confusion matrix
8. Feature importance

## Next Steps

### For Better Performance
1. **Collect more data**: 1+ years of historical data
2. **Feature engineering**: Add more technical indicators
3. **Ensemble models**: Combine XGBoost with Random Forest
4. **Deep learning**: Try LSTM for classification too
5. **Real-time tuning**: Retrain periodically with new data

### For Production
1. **Save CV results**: Log all parameter combinations
2. **A/B testing**: Compare old vs new model
3. **Monitoring**: Track prediction accuracy over time
4. **Auto-retraining**: Retrain weekly/monthly
5. **Backtesting**: Test on historical data

## References

- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Scikit-learn GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
- [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
