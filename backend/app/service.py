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
            return _generate_with_granite(prompt), {"provider": provider, "used_fallback": used_fallback}
        except Exception:
            used_fallback = True

    # Fallback to Gemini if configured
    if GEMINI_API_KEY:
        provider = "gemini"
        try:
            return _generate_with_gemini(prompt), {"provider": provider, "used_fallback": used_fallback}
        except Exception:
            pass

    # Final fallback
    provider = "rule_based"
    return (
        "Here are some general personal finance tips: build an emergency fund, pay down high-interest debt, "
        "budget using the 50/30/20 rule, and invest regularly in low-cost diversified funds.",
        {"provider": provider, "used_fallback": True},
    )

