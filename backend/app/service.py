import os
from typing import Tuple, Dict

# Lazy imports for heavy deps
_tokenizer = None
_model = None
_TRANSFORMERS_AVAILABLE = False
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    _TRANSFORMERS_AVAILABLE = True
except Exception:
    pass

MODEL_ID = os.getenv("GRANITE_MODEL_ID", "ibm-granite/granite-3.1-1b-a400m-instruct")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def _load_model():
    global _tokenizer, _model
    if not _TRANSFORMERS_AVAILABLE or _model is not None:
        return _TRANSFORMERS_AVAILABLE and _model is not None
    try:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True, use_fast=True)
        if _tokenizer.pad_token is None:
            _tokenizer.pad_token = _tokenizer.eos_token
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            trust_remote_code=True,
            torch_dtype=dtype,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True,
        )
        if not torch.cuda.is_available():
            _model = _model.to("cpu")
        _model.eval()
        return True
    except Exception:
        _model = None
        return False


def _build_prompt(user_input: str, user_mode: str, scenario_context: str) -> str:
    if user_mode == "student":
        base_prompt = (
            "You are a financial advisor specializing in student financial wellness. "
            "Your advice is practical, budget-conscious, and focused on building strong financial foundations.\n\n"
        )
        response_format = (
            "Provide practical, budget-friendly advice with:\n"
            "1. One key financial principle for students\n"
            "2. 2-3 actionable steps within a student budget\n"
            "3. One money-saving tip or resource for students\n"
        )
    else:
        base_prompt = (
            "You are a senior financial advisor for working professionals. "
            "Your advice is sophisticated, comprehensive, and focused on wealth optimization.\n\n"
        )
        response_format = (
            "Provide comprehensive professional advice with:\n"
            "1. One strategic financial insight\n"
            "2. 2-3 specific action steps with numbers/percentages\n"
            "3. One advanced tip or optimization strategy\n"
        )

    if scenario_context:
        base_prompt += scenario_context + "\n\n"

    return f"{base_prompt}User Question: {user_input}\n{response_format}\nResponse:"


def _generate_with_granite(prompt: str) -> str:
    import torch  # local import for type
    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=450,
        padding=True,
        return_attention_mask=True,
    )
    device = next(_model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = _model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=120,
            temperature=0.5,
            do_sample=True,
            top_p=0.9,
            pad_token_id=_tokenizer.pad_token_id,
            eos_token_id=_tokenizer.eos_token_id,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
            use_cache=True,
            early_stopping=True,
        )
    text = _tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text.split("Response:")[-1].strip() if "Response:" in text else text


def _generate_with_gemini(prompt: str) -> str:
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=data, timeout=30)
    r.raise_for_status()
    j = r.json()
    # Minimal extraction
    try:
        return j["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return "I'm sorry, I couldn't generate a response right now."


def generate_chat_response(req) -> Tuple[str, Dict]:
    prompt = _build_prompt(req.user_input, req.user_mode or "professional", req.scenario_context or "")

    used_fallback = False
    provider = ""

    # Try Granite if available and loads
    if _load_model():
        try:
            provider = "granite"
            response = _generate_with_granite(prompt)
            if response and len(response.strip()) > 10:
                return response, {"provider": provider, "used_fallback": used_fallback}
        except Exception as e:
            print(f"Granite model error: {e}")
            used_fallback = True

    # Fallback to Gemini if configured
    if GEMINI_API_KEY:
        provider = "gemini"
        try:
            response = _generate_with_gemini(prompt)
            if response and len(response.strip()) > 10:
                return response, {"provider": provider, "used_fallback": used_fallback}
        except Exception as e:
            print(f"Gemini API error: {e}")

    # Enhanced rule-based fallback
    provider = "rule_based"
    return _generate_rule_based_response(req.user_input, req.user_mode or "professional"), {"provider": provider, "used_fallback": True}


def _generate_rule_based_response(user_input: str, user_mode: str) -> str:
    """Generate rule-based responses for common financial questions"""
    user_input_lower = user_input.lower()

    # Budget-related responses
    if any(word in user_input_lower for word in ["budget", "budgeting", "spending", "expenses"]):
        if user_mode == "student":
            return """🎓 **Student Budgeting Guide**

1. **Track Your Income & Expenses**: Use apps like Mint or YNAB to monitor where your money goes
2. **Follow the 50/30/20 Rule**: 50% needs, 30% wants, 20% savings
3. **Student-Specific Tips**:
   • Cook meals instead of eating out
   • Buy used textbooks or rent them
   • Take advantage of student discounts

💡 **Pro Tip**: Start with a simple spreadsheet to track expenses for one month."""
        else:
            return """💼 **Professional Budgeting Strategy**

1. **Zero-Based Budgeting**: Assign every dollar a purpose before the month begins
2. **Automate Your Finances**: Set up automatic transfers to savings and investments
3. **Advanced Strategies**:
   • Use multiple savings accounts for different goals
   • Review and adjust quarterly
   • Consider tax-advantaged accounts

📊 **Recommendation**: Aim to save 20-25% of gross income for optimal financial health."""

    # Investment-related responses
    elif any(word in user_input_lower for word in ["invest", "investment", "stocks", "portfolio"]):
        if user_mode == "student":
            return """🎓 **Student Investment Basics**

1. **Start Small**: Begin with $25-50/month in a low-cost index fund
2. **Use Student-Friendly Platforms**: Consider Acorns, Stash, or Robinhood
3. **Focus on Learning**:
   • Read "The Bogleheads' Guide to Investing"
   • Understand compound interest
   • Learn about diversification

⚠️ **Important**: Only invest money you won't need for 5+ years."""
        else:
            return """💼 **Professional Investment Strategy**

1. **Asset Allocation**: Diversify across stocks, bonds, and real estate
2. **Tax-Advantaged Accounts**: Max out 401(k) match, then Roth IRA
3. **Advanced Strategies**:
   • Dollar-cost averaging into index funds
   • Consider target-date funds for simplicity
   • Rebalance annually

📈 **Target**: Aim for 10-15% total savings rate including employer match."""

    # Emergency fund responses
    elif any(word in user_input_lower for word in ["emergency", "fund", "savings"]):
        return """🚨 **Emergency Fund Essentials**

1. **Target Amount**: 3-6 months of essential expenses
2. **Where to Keep It**: High-yield savings account (2-5% APY)
3. **Building Strategy**:
   • Start with $500-1000 mini emergency fund
   • Save $25-100 per week consistently
   • Use windfalls (tax refunds, bonuses)

💰 **Quick Start**: Set up automatic transfer of $50/week to savings."""

    # Debt-related responses
    elif any(word in user_input_lower for word in ["debt", "credit card", "loan", "pay off"]):
        return """💳 **Debt Elimination Strategy**

1. **List All Debts**: Amount, minimum payment, interest rate
2. **Choose Your Method**:
   • **Debt Avalanche**: Pay minimums, extra to highest interest rate
   • **Debt Snowball**: Pay minimums, extra to smallest balance
3. **Accelerate Payoff**:
   • Use windfalls for extra payments
   • Consider balance transfers for high-interest debt
   • Avoid taking on new debt

🎯 **Priority**: Pay off credit cards first (typically 18-25% interest)."""

    # Default response
    else:
        return """💰 **Personal Finance Fundamentals**

1. **Emergency Fund**: Save 3-6 months of expenses
2. **Debt Management**: Pay off high-interest debt first
3. **Budgeting**: Track income and expenses monthly
4. **Investing**: Start with low-cost index funds
5. **Insurance**: Protect against major financial risks

📚 **Recommended Reading**: "The Total Money Makeover" by Dave Ramsey

💡 **Next Step**: Choose one area to focus on this month and take action!"""

