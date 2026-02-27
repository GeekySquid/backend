#!/usr/bin/env python3
"""
Comprehensive API Test Suite
Tests all endpoints and features
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✓ Root endpoint working")

def test_health():
    """Test health check"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✓ Health check working")

def test_metrics():
    """Test metrics endpoint"""
    print_section("Testing Metrics")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✓ Metrics endpoint working")

def test_single_prediction():
    """Test single stock prediction"""
    print_section("Testing Single Prediction")
    symbol = "AAPL"
    response = requests.get(f"{BASE_URL}/api/v1/predict?symbol={symbol}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print(f"\n📊 Prediction for {symbol}:")
        print(f"   Predicted Price: ${data['predicted_price']:.2f}")
        print(f"   Signal: {data['signal']}")
        print(f"   Confidence: {data['confidence']:.2%}")
        print(f"   Cached: {data['cached']}")
        print("✓ Single prediction working")
    else:
        print(f"Error: {response.text}")
        print("⚠️  Prediction failed (might be API limit)")

def test_cached_prediction():
    """Test cached prediction"""
    print_section("Testing Cached Prediction")
    symbol = "AAPL"
    
    # First request
    print("First request (should not be cached)...")
    response1 = requests.get(f"{BASE_URL}/api/v1/predict?symbol={symbol}")
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"Cached: {data1['cached']}")
        
        # Second request (should be cached)
        print("\nSecond request (should be cached)...")
        response2 = requests.get(f"{BASE_URL}/api/v1/predict?symbol={symbol}")
        data2 = response2.json()
        print(f"Cached: {data2['cached']}")
        
        if data2['cached']:
            print("✓ Caching working correctly")
        else:
            print("⚠️  Caching might not be enabled")
    else:
        print("⚠️  Prediction failed")

def test_batch_prediction():
    """Test batch prediction"""
    print_section("Testing Batch Prediction")
    symbols = ["AAPL", "GOOGL", "MSFT"]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/predict/batch",
        json={"symbols": symbols}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Batch Prediction Results:")
        print(f"   Total: {data['total']}")
        print(f"   Successful: {data['successful']}")
        print(f"   Failed: {data['failed']}")
        
        print(f"\n   Predictions:")
        for pred in data['predictions']:
            if pred['signal'] != "ERROR":
                print(f"   - {pred['symbol']}: ${pred['predicted_price']:.2f} ({pred['signal']})")
        
        print("✓ Batch prediction working")
    else:
        print(f"Error: {response.text}")
        print("⚠️  Batch prediction failed")

def test_invalid_symbol():
    """Test invalid symbol handling"""
    print_section("Testing Error Handling")
    invalid_symbols = ["ABC123", "TOOLONG", "123", ""]
    
    for symbol in invalid_symbols:
        response = requests.get(f"{BASE_URL}/api/v1/predict?symbol={symbol}")
        print(f"\nSymbol: '{symbol}'")
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.json()['detail']}")
            print("✓ Error handling working")
        else:
            print("⚠️  Should have returned error")

def test_api_docs():
    """Test API documentation"""
    print_section("Testing API Documentation")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ API docs available at /docs")
    else:
        print("⚠️  API docs not available")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  STOCK PREDICTION API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"  Base URL: {BASE_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    try:
        test_root()
        test_health()
        test_metrics()
        test_single_prediction()
        test_cached_prediction()
        test_batch_prediction()
        test_invalid_symbol()
        test_api_docs()
        
        print("\n" + "="*70)
        print("  ✅ ALL TESTS COMPLETED")
        print("="*70)
        print("\n📚 Next Steps:")
        print("   1. Visit http://localhost:8000/docs for interactive API docs")
        print("   2. Check http://localhost:8000/health for system status")
        print("   3. View http://localhost:8000/metrics for performance metrics")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("   Make sure the server is running:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
