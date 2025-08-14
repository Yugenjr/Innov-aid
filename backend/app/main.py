from fastapi import FastAPI, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse, SessionCreate, Session, SessionList, Message
from .service import generate_chat_response
from .finance import BudgetInput, BudgetAnalysis, analyze_budget, SavingsInput, SavingsProjection, project_savings, InvestInput, InvestOutput, invest_calculate
from .speech import call_deepgram, call_elevenlabs
from .storage import create_session, list_sessions, get_session, update_session_messages
import base64
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
def chat(req: ChatRequest):
    text, meta = generate_chat_response(req)
    return ChatResponse(response=text, provider=meta.get("provider", "unknown"), used_fallback=meta.get("used_fallback", False))

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

# Speech endpoints
@app.post("/api/speech/transcribe")
async def transcribe(file: UploadFile = File(...), content_type: str | None = Header(default=None)):
    audio_bytes = await file.read()
    text = call_deepgram(audio_bytes, content_type)
    return {"text": text}

@app.post("/api/speech/tts")
async def tts(body: dict):
    txt = body.get("text", "")
    audio = call_elevenlabs(txt)
    return {"audio_base64": base64.b64encode(audio).decode("utf-8")}

