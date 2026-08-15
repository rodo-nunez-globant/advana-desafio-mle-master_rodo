#!/usr/bin/env python3
"""
Simple script to test the Flight Delay Prediction API locally.
Run this script while the API server is running on localhost:8000
"""

import requests
import json
import time

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint with sample flight data."""
    print("\n✈️  Testing prediction endpoint...")
    
    # Sample flight data (valid)
    flight_data = {
        "flights": [
            {
                "OPERA": "Aerolineas Argentinas",
                "TIPOVUELO": "N",
                "MES": 3
            },
            {
                "OPERA": "Grupo LATAM", 
                "TIPOVUELO": "I",
                "MES": 7
            }
        ]
    }
    
    try:
        print(f"Sending request with data: {json.dumps(flight_data, indent=2)}")
        
        response = requests.post(
            "http://localhost:8000/predict",
            json=flight_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            predictions = response.json().get("predict", [])
            print(f"\n📊 Predictions:")
            for i, (flight, pred) in enumerate(zip(flight_data["flights"], predictions)):
                status = "✅ Delay predicted" if pred == 1 else "✅ No delay predicted"
                print(f"  Flight {i+1}: {flight['OPERA']} - {status}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_invalid_data():
    """Test with invalid data to see error handling."""
    print("\n🚫 Testing with invalid data...")
    
    # Invalid flight data (invalid airline)
    invalid_data = {
        "flights": [
            {
                "OPERA": "Invalid Airline",
                "TIPOVUELO": "X",  # Invalid flight type
                "MES": 13  # Invalid month
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 400
        
    except Exception as e:
        print(f"❌ Error test failed: {e}")
        return False

def test_api_docs():
    """Test access to API documentation."""
    print("\n📚 Testing API documentation...")
    
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ API docs available at: http://localhost:8000/docs")
            print("✅ ReDoc available at: http://localhost:8000/redoc")
            return True
        else:
            print(f"❌ Docs not available: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not access docs: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Flight Delay Prediction API")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    tests = [
        ("Health Check", test_health_check),
        ("API Documentation", test_api_docs),
        ("Valid Prediction", test_prediction),
        ("Invalid Data", test_invalid_data),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()