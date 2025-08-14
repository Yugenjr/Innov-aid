#!/usr/bin/env python3
"""
Test script to verify the backend API is working properly
"""

import requests
import json
import time

def test_backend_api():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Backend API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        print("  Make sure the backend server is running on port 8000")
        return False
    
    # Test 2: Chat endpoint
    print("\n2. Testing chat endpoint...")
    chat_requests = [
        {
            "user_input": "What's a good budgeting tip for students?",
            "user_mode": "student",
            "scenario_context": ""
        },
        {
            "user_input": "How should I invest my money?",
            "user_mode": "professional", 
            "scenario_context": ""
        }
    ]
    
    for i, test_req in enumerate(chat_requests, 1):
        print(f"\n  Test 2.{i}: {test_req['user_input']}")
        print(f"  Mode: {test_req['user_mode']}")
        
        try:
            response = requests.post(f"{base_url}/api/chat", json=test_req, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"  ✓ Status: {response.status_code}")
            print(f"  ✓ Provider: {data.get('provider', 'unknown')}")
            print(f"  ✓ Used Fallback: {data.get('used_fallback', False)}")
            print(f"  ✓ Response: {data.get('response', 'No response')[:100]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False
    
    # Test 3: Budget analysis endpoint
    print("\n3. Testing budget analysis endpoint...")
    budget_data = {
        "monthly_income": 3000,
        "rent": 1000,
        "utilities": 150,
        "insurance": 200,
        "food": 400,
        "transportation": 300,
        "entertainment": 200,
        "other": 150
    }
    
    try:
        response = requests.post(f"{base_url}/api/budget/analyze", json=budget_data, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("  ✓ Budget analysis successful")
        print(f"  ✓ Total expenses: ${data.get('total_expenses', 0)}")
        print(f"  ✓ Remaining: ${data.get('remaining', 0)}")
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Budget analysis error: {e}")
    
    # Test 4: Investment calculation endpoint
    print("\n4. Testing investment calculation endpoint...")
    invest_data = {
        "initial_investment": 1000,
        "monthly_investment": 300,
        "annual_return_pct": 7,
        "years": 20
    }
    
    try:
        response = requests.post(f"{base_url}/api/invest/calc", json=invest_data, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("  ✓ Investment calculation successful")
        print(f"  ✓ Future value: ${data.get('total_future_value', 0):,.2f}")
        print(f"  ✓ Total gains: ${data.get('total_gains', 0):,.2f}")
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Investment calculation error: {e}")
    
    print("\n" + "=" * 50)
    print("Backend API test completed!")
    return True

if __name__ == "__main__":
    test_backend_api()
