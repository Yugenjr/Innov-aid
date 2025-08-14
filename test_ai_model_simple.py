#!/usr/bin/env python3
"""
Simple test script to load and test the Granite AI model
"""

import os
import sys
import time
from datetime import datetime

def test_ai_model():
    """Test the AI model loading and generation"""
    print("🤖 Granite AI Model Test")
    print("=" * 50)
    print(f"📅 Started: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        # Test dependencies
        print("🔍 Checking AI dependencies...")
        import torch
        import transformers
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ Transformers: {transformers.__version__}")
        print(f"✅ CUDA Available: {torch.cuda.is_available()}")
        print()
        
        # Model configuration
        MODEL_ID = "ibm-granite/granite-3.1-1b-a400m-instruct"
        print(f"🎯 Target Model: {MODEL_ID}")
        print()
        
        # Load tokenizer
        print("📝 Loading tokenizer...")
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True, use_fast=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer_time = time.time() - start_time
        print(f"✅ Tokenizer loaded in {tokenizer_time:.2f}s")
        print()
        
        # Load model
        print("🧠 Loading AI model...")
        print("   This may take 5-10 minutes on first download...")
        start_time = time.time()
        
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            trust_remote_code=True,
            torch_dtype=dtype,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True,
        )
        
        model_time = time.time() - start_time
        print(f"✅ Model loaded in {model_time:.2f}s")
        print(f"📊 Model size: ~{sum(p.numel() for p in model.parameters()) / 1e6:.1f}M parameters")
        print()
        
        # Test generation function
        def generate_response(prompt, max_length=200):
            """Generate response using the loaded model"""
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_new_tokens=max_length,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )
            
            text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return text.split("Response:")[-1].strip() if "Response:" in text else text
        
        # Test prompts
        test_prompts = [
            {
                "name": "Student Budgeting",
                "prompt": """You are a helpful financial advisor. Provide practical, actionable advice.

User Question: How should I budget as a college student?
Response Format: Provide a structured response with numbered steps and practical tips.
Response:"""
            },
            {
                "name": "Investment Advice", 
                "prompt": """You are a helpful financial advisor. Provide practical, actionable advice.

User Question: What's the best way to start investing with $500?
Response Format: Provide a structured response with numbered steps and practical tips.
Response:"""
            },
            {
                "name": "Emergency Fund",
                "prompt": """You are a helpful financial advisor. Provide practical, actionable advice.

User Question: How do I build an emergency fund?
Response Format: Provide a structured response with numbered steps and practical tips.
Response:"""
            }
        ]
        
        print("🧪 Testing AI responses...")
        print("=" * 50)
        
        for i, test in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}: {test['name']}")
            print("-" * 30)
            
            start_time = time.time()
            response = generate_response(test['prompt'])
            response_time = time.time() - start_time
            
            print(f"⏱️  Generation time: {response_time:.2f}s")
            print(f"🤖 AI Response:")
            print(response)
            print()
        
        print("=" * 50)
        print("✅ AI model test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"📅 Finished: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    test_ai_model()
