#!/bin/bash

echo "================================"
echo "Stock AI Backend - Quick Start"
echo "================================"
echo ""

# Check if models exist
if [ ! -f "app/models/lstm_model.pth" ] || [ ! -f "app/models/xgb_model.pkl" ]; then
    echo "⚠️  Models not found. Training with mock data..."
    python3 train_models_mock.py
    echo ""
fi

echo "🚀 Starting server..."
echo "📍 Server will run at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
