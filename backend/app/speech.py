import os
from pydantic import BaseModel
import requests

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")

tt_headers = {"xi-api-key": ELEVENLABS_API_KEY, "accept": "audio/mpeg", "Content-Type": "application/json"}

audio_auth_header = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}

class TranscribeResponse(BaseModel):
    text: str

class TTSRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    audio_base64: str  # mp3 base64


def call_deepgram(audio_bytes: bytes, content_type: str | None) -> str:
    if not DEEPGRAM_API_KEY:
        return ""
    url = "https://api.deepgram.com/v1/listen?punctuate=true"
    headers = dict(audio_auth_header)
    if content_type:
        headers["Content-Type"] = content_type
    r = requests.post(url, headers=headers, data=audio_bytes, timeout=60)
    r.raise_for_status()
    j = r.json()
    try:
        return j["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception:
        return ""


def call_elevenlabs(text: str) -> bytes:
    if not ELEVENLABS_API_KEY:
        return b""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    payload = {"text": text, "model_id": "eleven_multilingual_v2"}
    r = requests.post(url, headers=tt_headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.content

