from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    user_input: str
    scenario_context: Optional[str] = ""
    user_mode: Optional[str] = "professional"  # 'student' or 'professional'

class ChatResponse(BaseModel):
    response: str
    provider: str
    used_fallback: bool = False

class Message(BaseModel):
    role: str
    content: str

class SessionCreate(BaseModel):
    title: Optional[str] = None

class Session(BaseModel):
    id: str
    title: str
    created_at: str
    messages: List[Message] = []

class SessionList(BaseModel):
    sessions: List[Session]
