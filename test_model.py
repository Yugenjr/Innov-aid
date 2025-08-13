#!/usr/bin/env python3
"""
Simple test script to verify IBM Granite model loading
"""

def test_model_loading():
    print("🔍 Testing IBM Granite Model Loading...")
    
    try:
        print("📦 Importing required libraries...")
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print("✅ Libraries imported successfully!")
        
        print(f"🖥️  PyTorch version: {torch.__version__}")
        print(f"🔧 CUDA available: {torch.cuda.is_available()}")
        
        print("\n📥 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "ibm-granite/granite-3.1-1b-a400m-instruct",
            trust_remote_code=True
        )
        print("✅ Tokenizer loaded successfully!")
        
        print("\n🧠 Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            "ibm-granite/granite-3.1-1b-a400m-instruct",
            trust_remote_code=True,
            torch_dtype=torch.float32,
            device_map="auto" if torch.cuda.is_available() else "cpu"
        )
        print("✅ Model loaded successfully!")
        
        print(f"📊 Model device: {model.device}")
        print(f"💾 Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        print("\n🧪 Testing text generation...")
        test_prompt = "What is a good way to save money?"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=50,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        print(f"🤖 Generated response: {response}")
        
        print("\n🎉 All tests passed! Model is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install missing dependencies: pip install torch transformers accelerate")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This might be due to insufficient memory or network issues.")
        return False

if __name__ == "__main__":
    success = test_model_loading()
    if success:
        print("\n✅ Your system is ready to run the IBM Granite model!")
    else:
        print("\n⚠️  Model loading failed, but the app will use fallback responses.")
