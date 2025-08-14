from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse, SessionCreate, Session, SessionList, Message, FraudDetectionRequest, FraudDetectionResponse
from .service import generate_chat_response
from .finance import BudgetInput, BudgetAnalysis, analyze_budget, SavingsInput, SavingsProjection, project_savings, InvestInput, InvestOutput, invest_calculate
from .fraud_detection import detect_fraud, analyze_financial_content
from .storage import create_session, list_sessions, get_session, update_session_messages
import os

app = FastAPI(title="Finance Chatbot API", version="0.1.0")

# CORS
allowed_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Chat endpoint with extended timeout for AI model processing
    First request may take 5-10 minutes due to model loading
    """
    import asyncio

    # Run the chat generation in a thread to avoid blocking
    def generate_response():
        return generate_chat_response(req)

    # Extended timeout for AI model processing
    try:
        text, meta = await asyncio.get_event_loop().run_in_executor(None, generate_response)
        return ChatResponse(response=text, provider=meta.get("provider", "unknown"), used_fallback=meta.get("used_fallback", False))
    except Exception as e:
        # Fallback response if model fails
        fallback_text = "I'm currently loading the AI model. This may take a few minutes on the first request. Please try again shortly, or I can provide some general financial advice in the meantime."
        return ChatResponse(response=fallback_text, provider="fallback", used_fallback=True)

# Sessions endpoints (JSON storage)
@app.post("/api/sessions", response_model=Session)
def create_session_ep(payload: SessionCreate):
    s = create_session(payload.title)
    return Session(**s)

@app.get("/api/sessions", response_model=SessionList)
def list_sessions_ep():
    sessions = [Session(**s) for s in list_sessions()]
    return {"sessions": sessions}

@app.get("/api/sessions/{sid}", response_model=Session)
def get_session_ep(sid: str):
    s = get_session(sid)
    if not s:
        return {"id": sid, "title": "Not found", "created_at": "", "messages": []}
    return Session(**s)

@app.put("/api/sessions/{sid}", response_model=Session)
def update_session_ep(sid: str, messages: list[Message]):
    s = update_session_messages(sid, [m.model_dump() for m in messages])
    return Session(**s) if s else Session(id=sid, title="Not found", created_at="", messages=[])

# Finance endpoints
@app.post("/api/budget/analyze", response_model=BudgetAnalysis)
def budget_analyze(payload: BudgetInput):
    return analyze_budget(payload)

@app.post("/api/savings/project", response_model=SavingsProjection)
def savings_project(payload: SavingsInput):
    return project_savings(payload)

@app.post("/api/invest/calc", response_model=InvestOutput)
def invest_calc(payload: InvestInput):
    return invest_calculate(payload)

# Fraud Detection endpoints
@app.post("/api/fraud/detect", response_model=FraudDetectionResponse)
def detect_fraud_content(request: FraudDetectionRequest):
    """
    Detect fraud/scam content in text using FraudAwarenessGPT
    """
    if request.analysis_type == "financial":
        result = analyze_financial_content(request.content)
    else:
        result = detect_fraud(request.content)

    return FraudDetectionResponse(**result)

@app.post("/api/fraud/analyze-financial", response_model=FraudDetectionResponse)
def analyze_financial_fraud(request: FraudDetectionRequest):
    """
    Specialized financial fraud detection for investment scams, phishing, etc.
    """
    result = analyze_financial_content(request.content)
    return FraudDetectionResponse(**result)

