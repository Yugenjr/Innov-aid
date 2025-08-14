#!/usr/bin/env python3
"""
Test script to verify the chat API is working with the Granite model
"""

import requests
import json

def test_chat_api():
    url = "http://127.0.0.1:8000/api/chat"
    
    # Test data
    test_requests = [
        {
            "user_input": "What's a good budgeting tip for students?",
            "user_mode": "student",
            "scenario_context": ""
        },
        {
            "user_input": "How should I invest my money?",
            "user_mode": "professional", 
            "scenario_context": ""
        },
        {
            "user_input": "Help me create an emergency fund",
            "user_mode": "student",
            "scenario_context": "Emergency Fund: Building emergency savings step by step"
        }
    ]
    
    print("Testing Chat API with Granite Model")
    print("=" * 50)
    
    for i, test_req in enumerate(test_requests, 1):
        print(f"\nTest {i}: {test_req['user_input']}")
        print(f"Mode: {test_req['user_mode']}")
        
        try:
            response = requests.post(url, json=test_req, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Provider: {data.get('provider', 'unknown')}")
            print(f"✓ Used Fallback: {data.get('used_fallback', False)}")
            print(f"✓ Response: {data.get('response', 'No response')[:200]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_chat_api()
