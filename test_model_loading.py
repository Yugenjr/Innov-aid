#!/usr/bin/env python3
"""
Test script to load the Granite AI model and show complete output
"""

import sys
import os
import time
from datetime import datetime

# Add backend to path
sys.path.append('backend')

def test_model_loading():
    """Test loading and using the Granite AI model"""
    print("🤖 Granite AI Model Loading Test")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Import the service module
        print("📦 Importing backend service...")
        from app.service import _load_model, generate_chat_response
        from app.schemas import ChatRequest
        print("✅ Backend service imported successfully")
        print()
        
        # Test model loading
        print("🔄 Loading Granite AI model...")
        print("   Model: ibm-granite/granite-3.1-1b-a400m-instruct")
        print("   This may take 5-10 minutes on first run...")
        print()
        
        start_time = time.time()
        model_loaded = _load_model()
        load_time = time.time() - start_time
        
        if model_loaded:
            print(f"✅ Model loaded successfully in {load_time:.2f} seconds!")
            print()
            
            # Test different types of financial questions
            test_questions = [
                {
                    "question": "How should I budget as a college student?",
                    "mode": "student",
                    "context": ""
                },
                {
                    "question": "What's the best investment strategy for retirement?", 
                    "mode": "professional",
                    "context": ""
                },
                {
                    "question": "Build an emergency fund",
                    "mode": "student", 
                    "context": "Emergency Fund: Building emergency savings step by step"
                }
            ]
            
            print("🧪 Testing AI responses...")
            print("=" * 40)
            
            for i, test in enumerate(test_questions, 1):
                print(f"\n📝 Test {i}: {test['question']}")
                print(f"👤 Mode: {test['mode']}")
                if test['context']:
                    print(f"📋 Context: {test['context']}")
                print("-" * 40)
                
                try:
                    # Create request object
                    request = ChatRequest(
                        user_input=test['question'],
                        user_mode=test['mode'],
                        scenario_context=test['context']
                    )
                    
                    # Generate response
                    start_time = time.time()
                    response, metadata = generate_chat_response(request)
                    response_time = time.time() - start_time
                    
                    # Display results
                    print(f"🤖 Response ({response_time:.2f}s):")
                    print(f"   Provider: {metadata.get('provider', 'unknown')}")
                    print(f"   Fallback: {metadata.get('used_fallback', False)}")
                    print()
                    print("💬 AI Response:")
                    print(response)
                    print()
                    
                except Exception as e:
                    print(f"❌ Error generating response: {e}")
                    print()
            
        else:
            print("❌ Failed to load model")
            print("   Falling back to rule-based responses...")
            print()
            
            # Test fallback responses
            print("🧪 Testing fallback responses...")
            print("=" * 40)
            
            test_request = ChatRequest(
                user_input="How should I budget as a student?",
                user_mode="student",
                scenario_context=""
            )
            
            response, metadata = generate_chat_response(test_request)
            print(f"🤖 Fallback Response:")
            print(f"   Provider: {metadata.get('provider', 'unknown')}")
            print()
            print("💬 Response:")
            print(response)
            print()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory and dependencies are installed")
        print("   Run: pip install -r backend/requirements.txt")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Model loading test finished!")

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔍 Checking Dependencies...")
    print("-" * 30)
    
    dependencies = [
        ("torch", "PyTorch for model inference"),
        ("transformers", "Hugging Face Transformers"),
        ("accelerate", "Model acceleration"),
        ("sentencepiece", "Tokenization"),
    ]
    
    all_available = True
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}: Available ({desc})")
        except ImportError:
            print(f"❌ {dep}: Missing ({desc})")
            all_available = False
    
    print()
    if all_available:
        print("✅ All dependencies available!")
    else:
        print("❌ Some dependencies missing. Run:")
        print("   pip install torch transformers accelerate sentencepiece")
    
    return all_available

if __name__ == "__main__":
    print("🏦 Finance App - AI Model Test")
    print("=" * 60)
    
    # Check dependencies first
    if test_dependencies():
        print()
        test_model_loading()
    else:
        print("\n❌ Cannot proceed without required dependencies")
        print("Install missing packages and try again.")
