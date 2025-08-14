"""
FraudAwarenessGPT - AI-powered fraud detection service using Groq API
"""

import os
import json
from typing import Dict, Any
from groq import Groq

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY environment variable not set. Fraud detection will use fallback responses.")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are FraudAwarenessGPT, an AI expert in detecting financial scams and suspicious content.
Your task:
1. Identify any scam, spam, phishing, or fraud-related content in the given text.
2. Summarize the scam method in simple words.
3. Generate a short awareness warning for the public.

Format your response as:
{
  "detected_content": "...",
  "awareness_message": "..."
}

If no suspicious content is found, reply with:
{"detected_content": "None", "awareness_message": "No scam detected."}
"""

def detect_fraud(text: str) -> Dict[str, Any]:
    """
    Detect fraud/scam content in the given text using Groq API

    Args:
        text: The text content to analyze for fraud/scam indicators

    Returns:
        Dictionary containing detected_content and awareness_message
    """
    if not client:
        return {
            "detected_content": "Service unavailable",
            "awareness_message": "Fraud detection service requires GROQ_API_KEY environment variable. Please set it to enable AI-powered fraud detection.",
            "provider": "fallback",
            "model": "none",
            "success": False
        }

    try:
        # Create the chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user", 
                    "content": f"Analyze this text for fraud/scam content: {text}"
                }
            ],
            model="llama3-8b-8192",  # Using Llama 3 8B model
            temperature=0.1,  # Low temperature for consistent detection
            max_tokens=500,
            top_p=1,
            stream=False
        )
        
        # Extract the response
        response_content = chat_completion.choices[0].message.content
        
        # Try to parse as JSON
        try:
            result = json.loads(response_content)
            return {
                "detected_content": result.get("detected_content", "Unknown"),
                "awareness_message": result.get("awareness_message", "Analysis completed"),
                "provider": "groq",
                "model": "llama3-8b-8192",
                "success": True
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response
            return {
                "detected_content": "Analysis completed",
                "awareness_message": response_content,
                "provider": "groq",
                "model": "llama3-8b-8192", 
                "success": True
            }
            
    except Exception as e:
        # Fallback response if Groq API fails
        return {
            "detected_content": "Error",
            "awareness_message": f"Fraud detection service temporarily unavailable: {str(e)}",
            "provider": "fallback",
            "model": "none",
            "success": False
        }

def analyze_financial_content(content: str) -> Dict[str, Any]:
    """
    Analyze financial content for potential scams with enhanced context

    Args:
        content: Financial content to analyze

    Returns:
        Enhanced fraud detection results
    """
    if not client:
        return {
            "detected_content": "Service unavailable",
            "awareness_message": "Financial fraud detection requires GROQ_API_KEY environment variable. Please set it to enable AI-powered analysis.",
            "provider": "fallback",
            "model": "none",
            "success": False,
            "analysis_type": "financial"
        }

    # Enhanced prompt for financial context
    financial_prompt = f"""
You are FraudAwarenessGPT, specialized in detecting financial scams and fraudulent schemes.

Analyze this financial content for:
- Investment scams (Ponzi schemes, fake investments)
- Phishing attempts (fake bank emails, credential theft)
- Romance scams involving money
- Cryptocurrency scams
- Fake loan offers
- Identity theft attempts
- Advance fee frauds
- Fake financial advisors

Text to analyze: "{content}"

Respond in JSON format:
{{
  "detected_content": "Description of any scam/fraud detected or 'None'",
  "awareness_message": "Public warning message or 'No scam detected.'"
}}
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert fraud detection AI specializing in financial scams."
                },
                {
                    "role": "user",
                    "content": financial_prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.1,
            max_tokens=600,
            top_p=1,
            stream=False
        )
        
        response_content = chat_completion.choices[0].message.content
        
        try:
            result = json.loads(response_content)
            return {
                "detected_content": result.get("detected_content", "Unknown"),
                "awareness_message": result.get("awareness_message", "Analysis completed"),
                "provider": "groq",
                "model": "llama3-8b-8192",
                "success": True,
                "analysis_type": "financial"
            }
        except json.JSONDecodeError:
            return {
                "detected_content": "Analysis completed",
                "awareness_message": response_content,
                "provider": "groq", 
                "model": "llama3-8b-8192",
                "success": True,
                "analysis_type": "financial"
            }
            
    except Exception as e:
        return {
            "detected_content": "Error",
            "awareness_message": f"Financial fraud detection temporarily unavailable: {str(e)}",
            "provider": "fallback",
            "model": "none", 
            "success": False,
            "analysis_type": "financial"
        }

# Test function
def test_fraud_detection():
    """Test the fraud detection functionality"""
    test_cases = [
        "Congratulations! You've won $1,000,000! Click here to claim your prize now!",
        "I need help with my budget for college expenses",
        "Send me $500 and I'll double your money in 24 hours guaranteed!",
        "What's the best way to invest in index funds?"
    ]
    
    print("🔒 Testing FraudAwarenessGPT")
    print("=" * 50)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_text}")
        result = detect_fraud(test_text)
        print(f"Detected: {result['detected_content']}")
        print(f"Warning: {result['awareness_message']}")
        print(f"Provider: {result['provider']}")

if __name__ == "__main__":
    test_fraud_detection()
