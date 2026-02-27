# Quick Start Guide 🚀

## Get Started in 3 Minutes!

### Step 1: Start the Server (30 seconds)

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Test the API (1 minute)

Open a new terminal and run:

```bash
python3 test_api.py
```

Or test manually:

```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl "http://localhost:8000/api/v1/predict?symbol=AAPL"

# View metrics
curl http://localhost:8000/metrics
```

### Step 3: Explore the Docs (1 minute)

Open your browser:

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## What You Get

### ✅ Production-Ready Features

1. **Error Handling** - Graceful error responses
2. **Caching** - 10-minute cache for faster responses
3. **Logging** - Structured JSON logs
4. **Validation** - Input validation for all requests
5. **Metrics** - Performance tracking
6. **Health Checks** - System status monitoring
7. **Batch API** - Process multiple stocks at once
8. **Documentation** - Interactive Swagger UI

### 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/predict` | GET | Single stock prediction |
| `/api/v1/predict/batch` | POST | Batch predictions (max 10) |
| `/health` | GET | Health check |
| `/metrics` | GET | Performance metrics |
| `/docs` | GET | Interactive API docs |

### 🎯 Example Requests

#### Single Prediction
```bash
curl "http://localhost:8000/api/v1/predict?symbol=AAPL"
```

Response:
```json
{
  "symbol": "AAPL",
  "predicted_price": 175.32,
  "signal": "BUY",
  "confidence": 0.87,
  "timestamp": "2026-02-27T10:30:00",
  "model_version": "v2.1",
  "cached": false
}
```

#### Batch Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "GOOGL", "MSFT"]}'
```

#### Health Check
```bash
curl "http://localhost:8000/health"
```

Response:
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "timestamp": "2026-02-27T10:30:00",
  "models_loaded": true,
  "cache_size": 5
}
```

## Configuration

Edit `.env` file to customize:

```env
# Cache settings
CACHE_ENABLED=True
CACHE_TTL=600

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Debug mode
DEBUG=False
```

## Troubleshooting

### Server won't start?
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn app.main:app --reload --port 8001
```

### Models not loading?
```bash
# Train models first
python3 train_models_mock.py
```

### API limit errors?
- The free Alpha Vantage API has 25 requests/day limit
- Caching helps reduce API calls
- Wait 24 hours for limit reset

## Next Steps

1. **Share with Frontend** - API is ready for integration
2. **Customize Settings** - Edit `.env` file
3. **Add More Features** - See `STRATEGIC_IMPLEMENTATION_PLAN.md`
4. **Deploy to Production** - See deployment guides

## Support

- **Documentation**: See `IMPLEMENTATION_COMPLETE.md`
- **API Docs**: http://localhost:8000/docs
- **Strategic Plan**: See `STRATEGIC_IMPLEMENTATION_PLAN.md`

---

**That's it! Your production-ready API is running!** 🎉
