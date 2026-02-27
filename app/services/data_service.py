# app/services/data_service.py

import requests
import pandas as pd
from datetime import datetime, timedelta

# Apify API for Yahoo Finance data
APIFY_API_KEY = "apify_api_B4aZPaqSenlq1Kso41U0aVyuONgkqT4jY6UI"

def get_stock_data(symbol: str):
    """
    Fetch LIVE stock data using Apify's Yahoo Finance scraper
    """
    try:
        # Apify Yahoo Finance Actor
        url = "https://api.apify.com/v2/acts/curious_coder~yahoo-finance-scraper/run-sync-get-dataset-items"
        
        payload = {
            "startUrls": [{"url": f"https://finance.yahoo.com/quote/{symbol}/history"}],
            "maxItems": 100
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "token": APIFY_API_KEY
        }
        
        print(f"Fetching LIVE data for {symbol}...")
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"API returned status {response.status_code}")
        
        data = response.json()
        
        if not data or len(data) == 0:
            raise Exception(f"No data returned for {symbol}")
        
        # Parse the data
        rows = []
        for item in data:
            if 'historicalData' in item:
                for row in item['historicalData']:
                    rows.append({
                        'open': float(row.get('open', 0)),
                        'high': float(row.get('high', 0)),
                        'low': float(row.get('low', 0)),
                        'close': float(row.get('close', 0)),
                        'volume': float(row.get('volume', 0))
                    })
        
        if not rows:
            raise Exception(f"No historical data found for {symbol}")
        
        df = pd.DataFrame(rows)
        df = df.tail(100)  # Last 100 days
        
        print(f"✓ SUCCESS! Got LIVE data for {symbol}: {len(df)} days, latest price: ${df['close'].iloc[-1]:.2f}")
        
        return df
        
    except Exception as e:
        print(f"Apify error: {e}")
        # Fallback to simple method
        return get_stock_data_simple(symbol)


def get_stock_data_simple(symbol: str):
    """
    Simple fallback using direct Yahoo Finance API
    """
    try:
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=150)).timestamp())
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval=1d"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        result = data['chart']['result'][0]
        quotes = result['indicators']['quote'][0]
        
        df = pd.DataFrame({
            'open': quotes['open'],
            'high': quotes['high'],
            'low': quotes['low'],
            'close': quotes['close'],
            'volume': quotes['volume']
        })
        
        # Remove NaN rows
        df = df.dropna()
        df = df.tail(100)
        
        print(f"✓ Got LIVE data for {symbol}: {len(df)} days, latest: ${df['close'].iloc[-1]:.2f}")
        
        return df
        
    except Exception as e:
        raise Exception(f"Failed to fetch live data for {symbol}: {str(e)}")

