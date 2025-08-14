#!/usr/bin/env python3
"""
Test the fraud detection API endpoints
"""

import requests
import json
from datetime import datetime

def test_fraud_api():
    """Test the fraud detection API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔒 Testing FraudAwarenessGPT API")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Test health first
    try:
        print("1. 🔍 Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend is healthy")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return
    
    print()
    
    # Test cases for fraud detection
    test_cases = [
        {
            "name": "Obvious Scam",
            "content": "Congratulations! You've won $1,000,000! Click here to claim your prize now!",
            "type": "general"
        },
        {
            "name": "Investment Scam",
            "content": "Send me $500 and I'll double your money in 24 hours guaranteed!",
            "type": "financial"
        },
        {
            "name": "Legitimate Question",
            "content": "What's the best way to invest in index funds for retirement?",
            "type": "financial"
        },
        {
            "name": "Phishing Email",
            "content": "Your bank account has been compromised. Click this link immediately to secure your account: http://fake-bank.com/secure",
            "type": "general"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. 🧪 Testing: {test_case['name']}")
        print(f"   Content: {test_case['content'][:50]}...")
        print(f"   Type: {test_case['type']}")
        
        try:
            # Choose endpoint based on type
            if test_case['type'] == 'financial':
                endpoint = f"{base_url}/api/fraud/analyze-financial"
            else:
                endpoint = f"{base_url}/api/fraud/detect"
            
            payload = {
                "content": test_case['content'],
                "analysis_type": test_case['type']
            }
            
            response = requests.post(endpoint, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response received")
                print(f"   🔍 Detected: {data.get('detected_content', 'Unknown')}")
                print(f"   ⚠️  Warning: {data.get('awareness_message', 'No message')[:100]}...")
                print(f"   🤖 Provider: {data.get('provider', 'unknown')} ({data.get('model', 'unknown')})")
                print(f"   ✅ Success: {data.get('success', False)}")
            else:
                print(f"   ❌ API returned status {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 60)
    print(f"📅 Finished: {datetime.now().strftime('%H:%M:%S')}")
    print("🎉 Fraud detection API test completed!")

if __name__ == "__main__":
    test_fraud_api()
