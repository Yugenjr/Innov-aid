#!/usr/bin/env python3
"""
Test script to download and verify the IBM Granite 3.1-1b-a400m-instruct model
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "ibm-granite/granite-3.1-1b-a400m-instruct"

def test_model_download():
    print(f"Testing download and loading of {MODEL_ID}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    try:
        print("\n1. Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, 
            trust_remote_code=True, 
            use_fast=True
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        print("✓ Tokenizer loaded successfully")
        
        print("\n2. Downloading model...")
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            trust_remote_code=True,
            torch_dtype=dtype,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True,
        )
        
        if not torch.cuda.is_available():
            model = model.to("cpu")
            
        model.eval()
        print("✓ Model loaded successfully")
        
        print("\n3. Testing model inference...")
        test_prompt = "What is a good financial tip for students?"
        inputs = tokenizer(
            test_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=450,
            padding=True,
            return_attention_mask=True,
        )
        
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=50,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Model inference successful!")
        print(f"Test response: {response}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_model_download()
    if success:
        print("\n🎉 Granite model is ready to use!")
    else:
        print("\n❌ Model setup failed. Check the error above.")
