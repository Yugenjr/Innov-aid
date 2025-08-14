#!/usr/bin/env python3
"""
Test chat API with extended timeout for AI model loading
"""

import requests
import time
from datetime import datetime

def test_chat_with_extended_timeout():
    """Test the chat API with extended timeout"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Chat API with Extended Timeout")
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
        print("   Make sure the backend is running on port 8000")
        return
    
    print()
    print("2. 🤖 Testing AI chat with extended timeout...")
    print("   ⚠️  First request may take 5-10 minutes while AI model loads")
    print("   ⏳ Please be patient...")
    print()
    
    test_request = {
        "user_input": "How should I budget as a college student?",
        "user_mode": "student",
        "scenario_context": ""
    }
    
    try:
        start_time = time.time()
        print(f"   📤 Sending request at {datetime.now().strftime('%H:%M:%S')}")
        print(f"   💬 Question: {test_request['user_input']}")
        print(f"   👤 Mode: {test_request['user_mode']}")
        print()
        
        # Extended timeout for AI model loading
        response = requests.post(
            f"{base_url}/api/chat", 
            json=test_request, 
            timeout=600  # 10 minutes
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Response received in {elapsed_time:.2f} seconds")
            print(f"   🤖 Provider: {data.get('provider', 'unknown')}")
            print(f"   🔄 Used Fallback: {data.get('used_fallback', False)}")
            print()
            print("   💬 AI Response:")
            print("   " + "─" * 50)
            
            # Format the response nicely
            response_text = data.get('response', 'No response')
            lines = response_text.split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            
            print("   " + "─" * 50)
            print()
            print("   🎉 Chat API test successful!")
            
        else:
            print(f"   ❌ API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ Request timed out after 10 minutes")
        print("   This might indicate the AI model is still loading")
        print("   Try again in a few minutes")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 60)
    print(f"📅 Finished: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    test_chat_with_extended_timeout()
