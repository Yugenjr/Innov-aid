import json
import os
import uuid
from datetime import datetime
from typing import List, Dict

SESSIONS_PATH = os.getenv("SESSIONS_PATH", os.path.join(os.path.dirname(__file__), "sessions.json"))

def _load() -> Dict:
    if not os.path.exists(SESSIONS_PATH):
        return {"sessions": []}
    try:
        with open(SESSIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"sessions": []}

def _save(data: Dict):
    os.makedirs(os.path.dirname(SESSIONS_PATH), exist_ok=True)
    with open(SESSIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def create_session(title: str | None = None) -> Dict:
    data = _load()
    sid = str(uuid.uuid4())[:8]
    session = {
        "id": sid,
        "title": title or f"Session {len(data['sessions'])+1}",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "messages": [],
    }
    data["sessions"].append(session)
    _save(data)
    return session

def list_sessions() -> List[Dict]:
    return _load().get("sessions", [])

def get_session(sid: str) -> Dict | None:
    for s in _load().get("sessions", []):
        if s.get("id") == sid:
            return s
    return None

def update_session_messages(sid: str, messages: List[Dict]) -> Dict | None:
    data = _load()
    for s in data.get("sessions", []):
        if s.get("id") == sid:
            s["messages"] = messages
            _save(data)
            return s
    return None

