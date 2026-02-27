# Frontend Integration Guide

Quick guide for integrating the Stock AI Backend with your frontend.

## API Endpoint

**Base URL:** `http://localhost:8000`

**Endpoint:** `GET /predict?symbol={SYMBOL}`

## Example Integrations

### React/Next.js

```javascript
import { useState } from 'react';

function StockPredictor() {
  const [symbol, setSymbol] = useState('AAPL');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPrediction = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/predict?symbol=${symbol}`
      );
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <input 
        value={symbol} 
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        placeholder="Enter stock symbol"
      />
      <button onClick={fetchPrediction} disabled={loading}>
        {loading ? 'Loading...' : 'Get Prediction'}
      </button>
      
      {prediction && (
        <div>
          <h3>{prediction.symbol}</h3>
          <p>Predicted Price: ${prediction.predicted_price.toFixed(2)}</p>
          <p>Signal: {prediction.signal}</p>
          <p>Confidence: {(prediction.confidence * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
}
```

### Vanilla JavaScript

```javascript
async function getPrediction(symbol) {
  const response = await fetch(
    `http://localhost:8000/predict?symbol=${symbol}`
  );
  const data = await response.json();
  return data;
}

// Usage
getPrediction('AAPL').then(data => {
  console.log('Predicted Price:', data.predicted_price);
  console.log('Signal:', data.signal);
  console.log('Confidence:', data.confidence);
});
```

### Axios (React/Vue)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const getStockPrediction = async (symbol) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/predict`, {
      params: { symbol }
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Usage
getStockPrediction('AAPL')
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## Response Format

```typescript
interface PredictionResponse {
  symbol: string;           // Stock ticker (e.g., "AAPL")
  predicted_price: number;  // Predicted next-day price
  signal: "BUY" | "SELL";  // Trading signal
  confidence: number;       // Confidence score (0-1)
}
```

## Error Handling

```javascript
async function fetchWithErrorHandling(symbol) {
  try {
    const response = await fetch(
      `http://localhost:8000/predict?symbol=${symbol}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    if (error.message.includes('API limit')) {
      alert('API rate limit reached. Please try again later.');
    } else {
      alert('Error fetching prediction. Please try again.');
    }
    console.error('Error:', error);
  }
}
```

## CORS Configuration

The backend is configured to accept requests from any origin (`*`). 

For production, update `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Change this
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the API

### Using Browser
Open: `http://localhost:8000/docs`

### Using cURL
```bash
curl "http://localhost:8000/predict?symbol=AAPL"
```

### Using Postman
- Method: GET
- URL: `http://localhost:8000/predict`
- Params: `symbol=AAPL`

## Common Stock Symbols

- AAPL - Apple
- GOOGL - Google
- MSFT - Microsoft
- TSLA - Tesla
- AMZN - Amazon
- META - Meta (Facebook)
- NVDA - NVIDIA

## Notes

- Backend must be running on port 8000
- API responses are in JSON format
- All prices are in USD
- Confidence is a decimal between 0 and 1 (multiply by 100 for percentage)
