import streamlit as st
from datetime import datetime
import time
import math
import re
import requests
import base64
import io
import tempfile
import os
import json

# Try to import optional dependencies
try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available. Charts will be simplified.")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Removed voice functionality imports

# Speech-to-Speech Configuration - WORKING SETUP
DEEPGRAM_API_KEY = "8cb5ea519fc07555361023888ad01f83c71b96f5"
GEMINI_API_KEY = "AIzaSyDj76Ad7Yyb9J8Sn48i45E5tehmpySDmTk"  # Updated Gemini API key
ELEVENLABS_API_KEY = "sk_12b8b420df0032bf39f6b31a2654a3939f5da28f8dcacc2a"  # Updated ElevenLabs API key
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default voice

# Audio file settings
AUDIO_FILENAME = "user_input.wav"
BOT_AUDIO_FILENAME = "bot_response.mp3"

# Page configuration
st.set_page_config(
    page_title="Personal Finance Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with enhanced typography and UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

    /* Global Styles */
    .main {
        font-family: 'Source Sans Pro', sans-serif;
        min-height: 100vh;
    }

    /* Student Mode Styling */
    .student-mode .main {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    .student-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .student-card {
        background: rgba(79, 172, 254, 0.1);
        border: 1px solid rgba(79, 172, 254, 0.2);
        backdrop-filter: blur(10px);
    }

    .student-button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        box-shadow: 0 4px 16px rgba(33, 150, 243, 0.3);
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .student-button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4);
        transform: translateY(-2px);
    }

    /* Student Mode Specific Button Styling */
    .student-mode .stButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3) !important;
    }

    .student-mode .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4) !important;
    }

    .student-message {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        border-left: 4px solid #0d47a1;
        color: white !important;
        border-bottom-right-radius: 4px;
        margin-left: 2rem;
        margin-right: 0.5rem;
    }

    .student-message strong {
        color: white !important;
        font-weight: 700 !important;
    }

    .student-bot-message {
        background: #f8f9fa;
        border: 1px solid #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #263238 !important;
        border-bottom-left-radius: 4px;
        margin-right: 2rem;
        margin-left: 0.5rem;
    }

    .student-bot-message h1, .student-bot-message h2, .student-bot-message h3, .student-bot-message h4 {
        color: #1565c0 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        margin: 0.5rem 0 !important;
    }

    .student-bot-message strong {
        color: #0d47a1 !important;
        font-weight: 700 !important;
    }

    .student-bot-message p, .student-bot-message li, .student-bot-message span {
        color: #263238 !important;
        line-height: 1.6 !important;
        margin: 0.5rem 0 !important;
    }

    .student-bot-message ul, .student-bot-message ol {
        color: #263238 !important;
        margin: 0.5rem 0 !important;
        padding-left: 1.2rem !important;
    }

    .student-bot-message li {
        margin: 0.3rem 0 !important;
    }

    /* Professional Mode Styling */
    .professional-mode .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .professional-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .professional-card {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
    }

    .professional-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }

    .professional-button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .professional-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        margin-left: 2rem;
        margin-right: 0.5rem;
        border-bottom-right-radius: 4px;
    }

    .professional-message strong {
        color: white !important;
        font-weight: 700 !important;
    }

    .professional-bot-message {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-left: 4px solid #667eea;
        color: #2c3e50 !important;
        margin-right: 2rem;
        margin-left: 0.5rem;
        border-bottom-left-radius: 4px;
    }

    .professional-bot-message h1, .professional-bot-message h2, .professional-bot-message h3, .professional-bot-message h4 {
        color: #4527a0 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        margin: 0.5rem 0 !important;
    }

    .professional-bot-message strong {
        color: #311b92 !important;
        font-weight: 700 !important;
    }

    .professional-bot-message p, .professional-bot-message li {
        color: #2c3e50 !important;
        margin: 0.5rem 0 !important;
        line-height: 1.6 !important;
    }

    .professional-bot-message ul, .professional-bot-message ol {
        margin: 0.5rem 0 !important;
        padding-left: 1.2rem !important;
    }

    .professional-bot-message li {
        margin: 0.3rem 0 !important;
    }

    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -1px;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }

    /* Professional Chat Container */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        scrollbar-width: thin;
        scrollbar-color: #667eea #f1f1f1;
    }

    .chat-container::-webkit-scrollbar {
        width: 8px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: #f5f5f5;
        border-radius: 10px;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    .chat-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }

    /* Professional Chat Messages */
    .chat-message {
        font-family: 'Source Sans Pro', sans-serif;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        animation: slideIn 0.3s ease-out;
        line-height: 1.6;
        font-size: 0.95rem;
        border: 1px solid rgba(0,0,0,0.05);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        margin-left: 2rem;
        margin-right: 0.5rem;
        font-weight: 500;
        border-bottom-right-radius: 4px;
    }

    .user-message strong {
        font-weight: 700 !important;
        color: white !important;
    }

    .bot-message {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-left: 4px solid #667eea;
        margin-right: 2rem;
        margin-left: 0.5rem;
        color: #2c3e50 !important;
        border-bottom-left-radius: 4px;
        font-weight: 400;
    }

    .bot-message p {
        margin: 0.5rem 0 !important;
        color: #2c3e50 !important;
    }

    .bot-message ul, .bot-message ol {
        margin: 0.5rem 0 !important;
        padding-left: 1.2rem !important;
    }

    .bot-message li {
        margin: 0.3rem 0 !important;
        color: #2c3e50 !important;
    }

    /* Professional Typography for Bot Messages */
    .bot-message h1, .bot-message h2, .bot-message h3, .bot-message h4 {
        font-family: 'Poppins', sans-serif;
        color: #2c3e50;
        margin: 0.8rem 0 0.5rem 0;
        font-weight: 600;
    }

    .bot-message strong {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #1a202c;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .bot-message ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }

    .bot-message li {
        margin: 0.6rem 0;
        color: #4a5568;
        font-weight: 400;
        line-height: 1.6;
    }

    .bot-message ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }

    .bot-message ol li {
        margin: 0.8rem 0;
        color: #4a5568;
        font-weight: 500;
        line-height: 1.6;
    }

    /* Professional Scenario Buttons */
    .scenario-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 1.8rem;
        border-radius: 15px;
        margin: 0.4rem;
        cursor: pointer;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .scenario-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }

    /* Professional Input Styling */
    .stTextInput > div > div > input {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        padding: 1rem 1.2rem;
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        background: rgba(255, 255, 255, 0.95);
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        background: white;
    }

    .stTextInput > div > div > input::placeholder {
        color: #a0aec0;
        font-style: italic;
    }

    /* Professional Status Cards */
    .model-status {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(56, 178, 172, 0.1) 100%);
        border: 1px solid rgba(72, 187, 120, 0.2);
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #2d3748;
        backdrop-filter: blur(10px);
    }

    /* Professional Buttons */
    .stButton > button {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: white !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }

    /* Text Input Styling */
    .stTextInput > div > div > input {
        color: #2c3e50 !important;
        background: white !important;
    }

    /* General Text Colors */
    .main .element-container {
        color: #2c3e50 !important;
    }

    /* Markdown Text */
    .main .markdown-text-container {
        color: #2c3e50 !important;
    }

    /* Ensure all text is visible */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: #2c3e50 !important;
    }

    /* Welcome Message Styling */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #4a5568;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.1rem;
        font-style: italic;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 1rem 0;
    }

    /* Hide Streamlit Elements */
    .stSpinner {
        display: none !important;
    }

    .stAlert {
        display: none !important;
    }

    .stSuccess {
        display: none !important;
    }

    .stInfo {
        display: none !important;
    }

    .stWarning {
        display: none !important;
    }

    .stError {
        display: none !important;
    }

    /* Professional Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    .css-1d391kg .css-1v0mbdj {
        color: white;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'financial_context' not in st.session_state:
    st.session_state.financial_context = {}
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'user_mode' not in st.session_state:
    st.session_state.user_mode = 'professional'  # Default mode
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = {}
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'voice_input' not in st.session_state:
    st.session_state.voice_input = ""
if 'auto_submit_voice' not in st.session_state:
    st.session_state.auto_submit_voice = False
# Removed voice-related session state

def load_model_silently():
    """Load the IBM Granite model silently in background"""
    if not TRANSFORMERS_AVAILABLE or st.session_state.model_loaded:
        return st.session_state.model_loaded

    try:
        # Load tokenizer with optimizations
        st.session_state.tokenizer = AutoTokenizer.from_pretrained(
            "ibm-granite/granite-3.1-1b-a400m-instruct",
            trust_remote_code=True,
            use_fast=True
        )

        # Set pad token if not available
        if st.session_state.tokenizer.pad_token is None:
            st.session_state.tokenizer.pad_token = st.session_state.tokenizer.eos_token

        # Load model with optimizations for faster inference
        st.session_state.model = AutoModelForCausalLM.from_pretrained(
            "ibm-granite/granite-3.1-1b-a400m-instruct",
            trust_remote_code=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True
        )

        # Move to CPU if no CUDA and set to eval mode for faster inference
        if not torch.cuda.is_available():
            st.session_state.model = st.session_state.model.to('cpu')

        st.session_state.model.eval()  # Set to evaluation mode for faster inference
        st.session_state.model_loaded = True
        return True

    except Exception as e:
        st.session_state.model_loaded = False
        return False

def load_model():
    """Load the IBM Granite model completely silently"""
    if not TRANSFORMERS_AVAILABLE:
        return False

    if not st.session_state.model_loaded:
        try:
            success = load_model_silently()
            return success
        except Exception as e:
            st.session_state.model_loaded = False
            return False
    return True

def create_new_session():
    """Create a new chat session"""
    import uuid
    from datetime import datetime

    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    session_data = {
        'id': session_id,
        'timestamp': timestamp,
        'mode': st.session_state.user_mode,
        'chat_history': [],
        'title': f"{st.session_state.user_mode.title()} Session - {timestamp}"
    }

    st.session_state.chat_sessions[session_id] = session_data
    st.session_state.current_session_id = session_id
    st.session_state.chat_history = []

    return session_id

def save_current_session():
    """Save current chat to session history"""
    if st.session_state.current_session_id and st.session_state.chat_history:
        session_id = st.session_state.current_session_id
        if session_id in st.session_state.chat_sessions:
            st.session_state.chat_sessions[session_id]['chat_history'] = st.session_state.chat_history.copy()

            # Update title based on first user message
            if st.session_state.chat_history and st.session_state.chat_history[0]['role'] == 'user':
                first_message = st.session_state.chat_history[0]['content']
                title = first_message[:50] + "..." if len(first_message) > 50 else first_message
                st.session_state.chat_sessions[session_id]['title'] = title

def load_session(session_id):
    """Load a previous chat session"""
    if session_id in st.session_state.chat_sessions:
        session_data = st.session_state.chat_sessions[session_id]
        st.session_state.current_session_id = session_id
        st.session_state.chat_history = session_data['chat_history'].copy()
        st.session_state.user_mode = session_data['mode']
        return True
    return False

def delete_session(session_id):
    """Delete a chat session"""
    if session_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[session_id]
        if st.session_state.current_session_id == session_id:
            st.session_state.current_session_id = None
            st.session_state.chat_history = []

# Voice functionality
# Working Speech-to-Speech Functions
import sounddevice as sd
from scipy.io.wavfile import write
import pygame
import tempfile
import os

def record_audio(filename=None, duration=5, fs=44100):
    """Record audio from microphone"""
    if filename is None:
        filename = AUDIO_FILENAME

    try:
        st.info("🎤 Recording... Speak now!")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filename, fs, audio)
        st.success("✅ Audio recorded successfully!")
        return filename
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def transcribe_deepgram(audio_path):
    """Transcribe audio using Deepgram"""
    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }
        params = {
            "punctuate": "true",  # Fixed: should be string "true" not boolean True
            "language": "en-US"
        }
        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers=headers,
            params=params,
            data=audio_data
        )
        response.raise_for_status()
        result = response.json()
        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
        return transcript
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def get_gemini_reply(prompt):
    """Get response from Gemini AI or fallback to local model"""
    try:
        # Use fallback for now (can be updated with real Gemini API key later)
        if GEMINI_API_KEY == "AIzaSyDOJmBKJdOKjKjKjKjKjKjKjKjKjKjKjKj":
            # Fallback to local model
            return generate_response(prompt)
        else:
            # Real Gemini API call
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"You are a financial advisor. Answer this question: {prompt}"
                    }]
                }]
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            return reply
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        # Fallback to local model
        return generate_response(prompt)

def text_to_speech_elevenlabs(text, voice_id=ELEVENLABS_VOICE_ID, output_path=None):
    """Generate speech using ElevenLabs"""
    if output_path is None:
        output_path = BOT_AUDIO_FILENAME

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def play_audio_pygame(file_path):
    """Play audio using pygame"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.quit()
        return True
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")
        return False

def process_speech_to_speech_complete(user_message):
    """Complete speech-to-speech processing"""
    try:
        # Get AI response using Gemini
        ai_response = get_gemini_reply(user_message)

        # Generate voice response
        audio_file = text_to_speech_elevenlabs(ai_response)

        if audio_file:
            with open(audio_file, "rb") as f:
                audio_data = f.read()
            return {
                "success": True,
                "response": ai_response,
                "audio_data": audio_data,
                "audio_file": audio_file
            }
        else:
            return {
                "success": True,
                "response": ai_response,
                "audio_data": None,
                "audio_file": None
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_working_speech_interface():
    """Create working speech-to-speech interface"""
    speech_html = """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem; border-radius: 20px; border: 2px solid #667eea;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center; font-family: 'Inter', sans-serif;">

        <h3 style="color: white; margin-bottom: 1.5rem; font-weight: 700;">
            🎤 Working Speech-to-Speech System
        </h3>

        <div id="status" style="margin-bottom: 1rem; padding: 1rem; border-radius: 10px;
                               background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
            <div id="statusText" style="font-weight: 600; color: white;">
                🎤 Ready for speech-to-speech conversation
            </div>
            <div id="statusSubtext" style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
                Powered by Deepgram + Gemini + ElevenLabs
            </div>
        </div>

        <!-- Speech-to-Speech Button -->
        <div style="margin-bottom: 1.5rem;">
            <button id="speechBtn" onclick="startSpeechToSpeech()"
                    style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
                           color: white; border: none; padding: 1.5rem 3rem;
                           border-radius: 50px; font-size: 1.2rem; cursor: pointer;
                           box-shadow: 0 6px 20px rgba(0,0,0,0.3); transition: all 0.3s ease;
                           font-weight: 600;">
                <span id="speechBtnText">🎤 Start Speaking</span>
            </button>
        </div>

        <!-- Conversation Display -->
        <div id="transcript" style="background: rgba(255,255,255,0.9); padding: 1.2rem; border-radius: 12px;
                                   border: 1px solid rgba(255,255,255,0.3); min-height: 80px;
                                   font-size: 0.95rem; color: #333; line-height: 1.5;
                                   box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            Your speech-to-speech conversation will appear here...
        </div>

        <!-- Audio Player -->
        <div id="audioContainer" style="margin-top: 1rem; display: none;">
            <audio id="responseAudio" controls style="width: 100%; border-radius: 8px;">
                Your browser does not support the audio element.
            </audio>
        </div>
    </div>

    <script>
        let recognition;
        let isRecording = false;

        // Initialize speech recognition
        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                recognition.maxAlternatives = 1;
                return true;
            }
            return false;
        }

        function startSpeechToSpeech() {
            if (!recognition && !initSpeechRecognition()) {
                alert('Speech recognition not supported in this browser');
                return;
            }

            if (!isRecording) {
                startRecording();
            } else {
                stopRecording();
            }
        }

        function startRecording() {
            isRecording = true;
            document.getElementById('statusText').innerHTML = '🎤 Listening... Speak your financial question';
            document.getElementById('statusSubtext').innerHTML = 'AI will respond with ElevenLabs voice when you finish speaking';
            document.getElementById('speechBtnText').innerHTML = '⏹️ Stop Recording';
            document.getElementById('speechBtn').style.background = 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
            document.getElementById('transcript').innerHTML = '<em style="color: #666;">Listening...</em>';

            recognition.onstart = function() {
                document.getElementById('statusText').innerHTML = '🎤 Recording... Speak clearly';
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('transcript').innerHTML = 'You: ' + transcript;
                processWorkingSpeech(transcript);
            };

            recognition.onerror = function(event) {
                document.getElementById('statusText').innerHTML = '❌ Recording error: ' + event.error;
                resetButton();
            };

            recognition.onend = function() {
                resetButton();
            };

            try {
                recognition.start();
            } catch (error) {
                alert('Could not start recording: ' + error);
                resetButton();
            }
        }

        function stopRecording() {
            if (recognition && isRecording) {
                recognition.stop();
            }
        }

        function resetButton() {
            isRecording = false;
            document.getElementById('speechBtnText').innerHTML = '🎤 Start Speaking';
            document.getElementById('speechBtn').style.background = 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)';
        }

        function processWorkingSpeech(userMessage) {
            document.getElementById('statusText').innerHTML = '🤖 AI is processing your question...';
            document.getElementById('statusSubtext').innerHTML = 'Generating response with Gemini + ElevenLabs voice...';

            // Trigger Streamlit processing with voice input
            const url = new URL(window.location);
            url.searchParams.set('working_voice_input', userMessage);
            url.searchParams.set('working_mode', 'speech_to_speech');
            window.location.href = url.toString();
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            initSpeechRecognition();
        });
    </script>
    """
    return speech_html

def create_elevenlabs_style_voice_interface(mode="student"):
    """Create ElevenLabs-style voice interface with reliable recording"""
    mode_colors = {
        "student": {
            "primary": "#2196f3",
            "secondary": "#1976d2",
            "accent": "#e3f2fd",
            "text": "#1565c0"
        },
        "professional": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#f8f9ff",
            "text": "#4527a0"
        }
    }

    colors = mode_colors[mode]
    mode_emoji = "🎓" if mode == "student" else "💼"
    mode_title = "Student Voice Assistant" if mode == "student" else "Executive Voice Assistant"

    speech_html = f"""
    <div style="background: linear-gradient(135deg, {colors['accent']} 0%, white 100%);
                padding: 2rem; border-radius: 20px; border: 2px solid {colors['primary']};
                box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center; font-family: 'Inter', sans-serif;">

        <h3 style="color: {colors['text']}; margin-bottom: 1.5rem; font-weight: 700;">
            {mode_emoji} {mode_title}
        </h3>

        <!-- ElevenLabs-style Voice Button -->
        <div style="margin-bottom: 1.5rem;">
            <button id="recordBtn" onclick="toggleRecording()"
                    style="background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
                           color: white; border: none; padding: 1.2rem 2.5rem;
                           border-radius: 50px; font-size: 1.1rem; cursor: pointer;
                           box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.2s ease;
                           font-weight: 600; position: relative; min-width: 200px;">
                <span id="btnText">🎤 Click to Record</span>
            </button>
        </div>

        <!-- Recording Status -->
        <div id="status" style="font-size: 1rem; font-weight: 500; color: {colors['text']};
                               margin-bottom: 1rem; min-height: 25px;">
            Click the button and speak your financial question
        </div>

        <!-- Transcription Display -->
        <div id="transcript" style="background: white; padding: 1.2rem; border-radius: 12px;
                                   border: 1px solid #e0e0e0; min-height: 60px;
                                   font-size: 0.95rem; color: #333; line-height: 1.5;
                                   box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
            Your speech will appear here...
        </div>

        <!-- Audio Player (hidden initially) -->
        <div id="audioContainer" style="margin-top: 1rem; display: none;">
            <audio id="responseAudio" controls style="width: 100%; border-radius: 8px;">
                Your browser does not support the audio element.
            </audio>
        </div>
    </div>

    <script>
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;
        let recognition;
        let finalTranscript = '';

        // Initialize speech recognition
        function initSpeechRecognition() {{
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                recognition.maxAlternatives = 1;

                recognition.onstart = function() {{
                    isRecording = true;
                    document.getElementById('status').innerHTML = '🎤 Listening... Speak clearly';
                    document.getElementById('btnText').innerHTML = '⏹️ Stop Recording';
                    document.getElementById('recordBtn').style.background = 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
                    document.getElementById('transcript').innerHTML = '<em style="color: #666;">Listening...</em>';
                }};

                recognition.onresult = function(event) {{
                    let interimTranscript = '';
                    finalTranscript = '';

                    for (let i = event.resultIndex; i < event.results.length; i++) {{
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {{
                            finalTranscript += transcript;
                        }} else {{
                            interimTranscript += transcript;
                        }}
                    }}

                    const displayText = finalTranscript + '<span style="color: #999; font-style: italic;">' + interimTranscript + '</span>';
                    document.getElementById('transcript').innerHTML = displayText || '<em style="color: #666;">Listening...</em>';
                }};

                recognition.onerror = function(event) {{
                    console.error('Speech recognition error:', event.error);
                    document.getElementById('status').innerHTML = '❌ Error: ' + event.error + '. Please try again.';
                    resetRecording();
                }};

                recognition.onend = function() {{
                    if (finalTranscript.trim()) {{
                        document.getElementById('transcript').innerHTML = finalTranscript;
                        document.getElementById('status').innerHTML = '🤖 Processing and generating voice response...';

                        // Automatically process the transcript
                        processVoiceInput(finalTranscript.trim());
                    }} else {{
                        document.getElementById('status').innerHTML = '🔄 No speech detected. Please try again.';
                        document.getElementById('transcript').innerHTML = 'Your speech will appear here...';
                    }}
                    resetRecording();
                }};

                return true;
            }} else {{
                document.getElementById('status').innerHTML = '❌ Speech recognition not supported in this browser';
                return false;
            }}
        }}

        function toggleRecording() {{
            if (!isRecording) {{
                startRecording();
            }} else {{
                stopRecording();
            }}
        }}

        function startRecording() {{
            if (!recognition && !initSpeechRecognition()) {{
                return;
            }}

            if (recognition && !isRecording) {{
                finalTranscript = '';
                audioChunks = [];

                try {{
                    recognition.start();
                }} catch (error) {{
                    console.error('Error starting recognition:', error);
                    document.getElementById('status').innerHTML = '❌ Could not start recording. Please try again.';
                }}
            }}
        }}

        function stopRecording() {{
            if (recognition && isRecording) {{
                recognition.stop();
            }}
        }}

        function resetRecording() {{
            isRecording = false;
            document.getElementById('btnText').innerHTML = '🎤 Click to Record';
            document.getElementById('recordBtn').style.background = 'linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%)';
        }}

        async function processVoiceInput(text) {{
            try {{
                // Send to Streamlit backend for processing
                const response = await fetch(window.location.origin + '/voice_process', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        text: text,
                        mode: '{mode}'
                    }})
                }});

                if (response.ok) {{
                    const data = await response.json();
                    if (data.audio_url) {{
                        // Play the generated audio
                        const audioContainer = document.getElementById('audioContainer');
                        const audio = document.getElementById('responseAudio');
                        audio.src = data.audio_url;
                        audioContainer.style.display = 'block';

                        document.getElementById('status').innerHTML = '🔊 Voice response ready! Playing...';
                        audio.play();

                        audio.onended = function() {{
                            document.getElementById('status').innerHTML = '✅ Complete! Ready for next question.';
                            setTimeout(() => {{
                                document.getElementById('status').innerHTML = 'Click the button and speak your financial question';
                                document.getElementById('transcript').innerHTML = 'Your speech will appear here...';
                                audioContainer.style.display = 'none';
                            }}, 3000);
                        }};
                    }} else {{
                        throw new Error('No audio response received');
                    }}
                }} else {{
                    throw new Error('Server error');
                }}
            }} catch (error) {{
                console.error('Error processing voice input:', error);

                // Fallback: Use Streamlit's session state
                const event = new CustomEvent('voiceInputReceived', {{
                    detail: {{ text: text, mode: '{mode}' }}
                }});
                window.dispatchEvent(event);

                // Update UI for fallback processing
                document.getElementById('status').innerHTML = '🤖 Processing with fallback method...';

                // Trigger page refresh with voice input
                setTimeout(() => {{
                    const url = new URL(window.location);
                    url.searchParams.set('voice_input', text);
                    url.searchParams.set('voice_mode', '{mode}');
                    window.location.href = url.toString();
                }}, 1000);
            }}
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            initSpeechRecognition();
        }});
    </script>
    """
    return speech_html

def extract_financial_context(user_input):
    """Extract financial context from user input for better responses"""
    context = {}

    # Extract amounts
    amounts = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', user_input.lower())
    if amounts:
        context['amounts'] = [float(amt.replace(',', '')) for amt in amounts]

    # Extract time periods
    time_patterns = {
        'months': r'(\d+)\s*months?',
        'years': r'(\d+)\s*years?',
        'weeks': r'(\d+)\s*weeks?'
    }
    for period, pattern in time_patterns.items():
        matches = re.findall(pattern, user_input.lower())
        if matches:
            context[period] = [int(m) for m in matches]

    # Extract financial keywords
    financial_keywords = {
        'debt_types': ['student loan', 'credit card', 'mortgage', 'car loan', 'personal loan'],
        'investment_types': ['stocks', 'bonds', '401k', 'ira', 'roth', 'mutual fund', 'etf'],
        'account_types': ['checking', 'savings', 'high-yield', 'money market'],
        'goals': ['retirement', 'house', 'car', 'vacation', 'wedding', 'education'],
        'life_stage': ['student', 'graduate', 'married', 'single', 'parent', 'retired']
    }

    for category, keywords in financial_keywords.items():
        found = [kw for kw in keywords if kw in user_input.lower()]
        if found:
            context[category] = found

    return context

def get_mode_specific_context(mode):
    """Get context specific to user mode"""
    if mode == 'student':
        return {
            'income_level': 'limited or part-time income',
            'debt_focus': 'student loans and credit building',
            'investment_horizon': 'long-term with small amounts',
            'priorities': 'education funding, building credit, emergency fund',
            'constraints': 'tight budget, irregular income, high debt-to-income ratio',
            'opportunities': 'time advantage, potential for growth, learning phase'
        }
    else:  # professional
        return {
            'income_level': 'steady professional income',
            'debt_focus': 'mortgage, investment optimization, tax planning',
            'investment_horizon': 'medium to long-term with substantial amounts',
            'priorities': 'wealth building, retirement planning, tax optimization',
            'constraints': 'time limitations, complex financial situations',
            'opportunities': 'higher income, employer benefits, investment capacity'
        }

def build_financial_prompt(user_input, scenario_context="", financial_context=None):
    """Build optimized financial prompt with mode-specific context"""
    if financial_context is None:
        financial_context = extract_financial_context(user_input)

    # Get mode-specific context
    mode_context = get_mode_specific_context(st.session_state.user_mode)

    # Mode-specific base prompts
    if st.session_state.user_mode == 'student':
        base_prompt = """You are a financial advisor specializing in student financial wellness. You understand:
- Limited budgets and irregular income patterns
- Student loan management and federal aid programs
- Building credit history from scratch
- Balancing education costs with living expenses
- Entry-level career financial planning
- Maximizing student discounts and resources

Your advice is practical, budget-conscious, and focused on building strong financial foundations.

"""
    else:  # professional mode
        base_prompt = """You are a senior financial advisor for working professionals. You specialize in:
- Advanced investment strategies and portfolio optimization
- Tax-efficient wealth building and retirement planning
- Complex financial planning including real estate and insurance
- Executive compensation and equity planning
- Business financial strategies and entrepreneurship
- Estate planning and wealth preservation

Your advice is sophisticated, comprehensive, and focused on wealth optimization.

"""

    # Add mode-specific context
    base_prompt += f"""
Client Profile: {mode_context['income_level']} with focus on {mode_context['debt_focus']}.
Investment Horizon: {mode_context['investment_horizon']}.
Key Priorities: {mode_context['priorities']}.
Main Constraints: {mode_context['constraints']}.
Opportunities: {mode_context['opportunities']}.

"""

    # Add specific context based on extracted information
    if financial_context.get('amounts'):
        amounts = financial_context['amounts']
        base_prompt += f"Amounts mentioned: ${', $'.join(map(str, amounts))}. "

    if financial_context.get('debt_types'):
        debt_types = ', '.join(financial_context['debt_types'])
        base_prompt += f"Focus on {debt_types} management. "

    if financial_context.get('investment_types'):
        inv_types = ', '.join(financial_context['investment_types'])
        base_prompt += f"Provide {st.session_state.user_mode}-appropriate guidance on {inv_types}. "

    # Add scenario context
    if scenario_context:
        base_prompt += f"{scenario_context} "

    # Mode-specific response format
    if st.session_state.user_mode == 'student':
        response_format = """
Provide practical, budget-friendly advice with:
1. One key financial principle for students
2. 2-3 actionable steps within a student budget
3. One money-saving tip or resource for students
"""
    else:
        response_format = """
Provide comprehensive professional advice with:
1. One strategic financial insight
2. 2-3 specific action steps with numbers/percentages
3. One advanced tip or optimization strategy
"""

    # Build final prompt
    prompt = f"""{base_prompt}

User Question: {user_input}
{response_format}
Response:"""

    return prompt

def generate_response(user_input, scenario_context=""):
    """Generate optimized financial response using IBM Granite model"""
    if not st.session_state.model_loaded or not TRANSFORMERS_AVAILABLE:
        return generate_fallback_response(user_input, scenario_context)

    # Extract financial context for better responses
    financial_context = extract_financial_context(user_input)
    st.session_state.financial_context = financial_context

    try:
        # Build optimized financial prompt with context
        financial_prompt = build_financial_prompt(user_input, scenario_context, financial_context)

        # Optimized tokenization for financial content
        inputs = st.session_state.tokenizer(
            financial_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=450,  # Slightly increased for financial context
            padding=True,
            return_attention_mask=True
        )

        # Move inputs to same device as model
        device = next(st.session_state.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Optimized generation parameters for financial advice
        with torch.no_grad():
            outputs = st.session_state.model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_new_tokens=120,  # Increased for detailed financial advice
                temperature=0.5,     # Lower for more consistent financial advice
                do_sample=True,
                top_p=0.9,          # Nucleus sampling for better quality
                pad_token_id=st.session_state.tokenizer.pad_token_id,
                eos_token_id=st.session_state.tokenizer.eos_token_id,
                repetition_penalty=1.15,  # Higher to avoid repetition
                no_repeat_ngram_size=3,
                use_cache=True,
                early_stopping=True  # Stop when complete thought is generated
            )

        # Decode only the new tokens
        response = st.session_state.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[-1]:],
            skip_special_tokens=True
        )

        # Clean and format the response
        response = response.strip()
        if not response or len(response) < 15:
            return generate_fallback_response(user_input, scenario_context)

        # Format the response with financial context
        formatted_response = format_financial_response(response, financial_context)
        return formatted_response

    except Exception as e:
        # Fall back to enhanced manual responses
        return generate_fallback_response(user_input, scenario_context)

def format_financial_response(response, financial_context):
    """Format AI response with enhanced financial structure"""
    # Clean up the response
    response = response.strip()

    # Split into logical sections
    sections = []
    current_section = ""

    for line in response.split('\n'):
        line = line.strip()
        if line:
            if line.startswith(('1.', '2.', '3.', '•', '-')):
                if current_section:
                    sections.append(current_section)
                current_section = line
            else:
                if current_section:
                    current_section += f" {line}"
                else:
                    current_section = line

    if current_section:
        sections.append(current_section)

    # Build formatted response
    formatted = "🤖 **AI Financial Advisor**\n\n"

    # Add financial context if available
    if financial_context.get('amounts'):
        amounts = financial_context['amounts']
        if len(amounts) == 1:
            formatted += f"💰 **Amount in Focus:** ${amounts[0]:,.2f}\n\n"
        elif len(amounts) > 1:
            formatted += f"💰 **Amounts Discussed:** ${', $'.join(f'{amt:,.2f}' for amt in amounts)}\n\n"

    # Format main content
    if len(sections) == 1:
        formatted += f"**Financial Guidance:** {sections[0]}\n\n"
    else:
        # First section as key insight
        if sections:
            formatted += f"**Key Insight:** {sections[0]}\n\n"

        # Remaining sections as action steps
        if len(sections) > 1:
            formatted += "**Action Steps:**\n"
            for i, section in enumerate(sections[1:], 1):
                # Clean up numbering
                clean_section = section
                for prefix in ['1.', '2.', '3.', '•', '-']:
                    if clean_section.startswith(prefix):
                        clean_section = clean_section[len(prefix):].strip()
                        break
                formatted += f"{i}. {clean_section}\n"

    # Add relevant financial tips based on context
    tips = get_contextual_tips(financial_context)
    if tips:
        formatted += f"\n💡 **Pro Tip:** {tips}\n"

    return formatted

def calculate_financial_insights(financial_context):
    """Calculate useful financial insights based on context"""
    insights = {}

    if financial_context.get('amounts'):
        amounts = financial_context['amounts']

        # Emergency fund calculations
        if len(amounts) >= 2:
            monthly_expenses = min(amounts)  # Assume smaller amount is monthly
            emergency_target = monthly_expenses * 6
            insights['emergency_fund'] = {
                'monthly_expenses': monthly_expenses,
                'target': emergency_target,
                'current': max(amounts) if max(amounts) < emergency_target else 0
            }

        # Debt payoff calculations (assuming 18% credit card rate)
        for amount in amounts:
            if amount >= 1000:  # Likely debt amount
                min_payment = amount * 0.02  # 2% minimum
                payoff_time_min = -math.log(1 - (amount * 0.18) / (min_payment * 12)) / math.log(1 + 0.18/12)
                insights['debt_payoff'] = {
                    'amount': amount,
                    'min_payment': min_payment,
                    'payoff_years_minimum': payoff_time_min / 12
                }

    return insights

def get_contextual_tips(financial_context):
    """Get enhanced contextual financial tips with calculations"""
    tips = []
    insights = calculate_financial_insights(financial_context)

    # Debt-specific tips with calculations
    if financial_context.get('debt_types'):
        if 'credit card' in financial_context['debt_types']:
            if insights.get('debt_payoff'):
                debt_info = insights['debt_payoff']
                tips.append(f"Paying just minimums on ${debt_info['amount']:,.0f} takes {debt_info['payoff_years_minimum']:.1f} years - double payments cut this in half!")
            else:
                tips.append("Pay more than minimum on credit cards - even $50 extra saves thousands in interest")

        if 'student loan' in financial_context['debt_types']:
            tips.append("Federal student loans offer income-driven plans with payments as low as $0/month")

    # Investment tips with specific numbers
    if financial_context.get('investment_types'):
        if '401k' in financial_context['investment_types']:
            tips.append("Employer 401(k) match is 100% return - contribute enough to get full match first")
        if any(inv in financial_context['investment_types'] for inv in ['stocks', 'etf', 'mutual fund']):
            tips.append("Low-cost index funds (under 0.1% fees) outperform 90% of actively managed funds")

    # Amount-based tips with calculations
    if financial_context.get('amounts'):
        amounts = financial_context['amounts']
        if any(amt >= 50000 for amt in amounts):
            tips.append("For amounts over $50K, consider fee-only financial advisors (1% annual fee typical)")
        elif any(1000 <= amt <= 10000 for amt in amounts):
            tips.append(f"${max(amounts):,.0f} invested in S&P 500 historically grows to ${max(amounts) * 2:.0f} in ~10 years")
        elif any(amt < 1000 for amt in amounts):
            tips.append("Start with any amount - $25/month invested becomes $10,000+ over 20 years with compound growth")

    # Emergency fund specific tips
    if insights.get('emergency_fund'):
        ef = insights['emergency_fund']
        tips.append(f"Target emergency fund: ${ef['target']:,.0f} (6 months of ${ef['monthly_expenses']:,.0f} expenses)")

    # Life stage tips
    if financial_context.get('life_stage'):
        if 'student' in financial_context['life_stage']:
            tips.append("Build credit with student credit card - keep utilization under 30% and pay in full monthly")
        elif 'retired' in financial_context['life_stage']:
            tips.append("Follow 4% withdrawal rule - need 25x annual expenses saved for retirement")

    return tips[0] if tips else None

def format_ai_response(response):
    """Legacy format function - redirects to enhanced version"""
    return format_financial_response(response, {})

def generate_fallback_response(user_input, scenario_context=""):
    """Generate enhanced fallback responses with mode-specific financial intelligence"""
    # Extract context for smarter responses
    financial_context = extract_financial_context(user_input)

    # Mode-specific financial responses
    if st.session_state.user_mode == 'student':
        fallback_responses = get_student_responses()
    else:
        fallback_responses = get_professional_responses()

def get_student_responses():
    """Student-specific financial responses"""
    return {
        "student loan": {
            "title": "Student Loan Survival Guide",
            "advice": "Smart loan management while in school and after graduation can save you thousands.",
            "points": [
                "Apply for income-driven repayment (IDR) plans - payments can be $0 if income is low",
                "Make interest-only payments while in school to prevent capitalization",
                "Use any extra money (tax refunds, gifts) for high-interest loan principal",
                "Research loan forgiveness programs for your career field (teaching, public service, healthcare)",
                "Avoid private loan refinancing until you have stable income and good credit",
                "Set up autopay for 0.25% interest rate reduction on federal loans"
            ]
        },
        "emergency fund": {
            "title": "Student Emergency Fund Starter",
            "advice": "Even $500 can prevent you from going into debt during emergencies.",
            "points": [
                "Start with $500 goal - achievable with part-time work or side gigs",
                "Save loose change and small bills in a jar - can add up to $200+ yearly",
                "Use student bank accounts with no fees and mobile deposit features",
                "Automate $10-25 weekly transfers from checking to savings",
                "Keep emergency fund separate from spending money to avoid temptation",
                "True emergencies: car repairs, medical bills, unexpected school costs"
            ]
        },
        "budget": {
            "title": "Student Budget Mastery",
            "advice": "Track every dollar to maximize your limited income and avoid debt.",
            "points": [
                "Use free apps like Mint, YNAB (free for students), or simple spreadsheets",
                "Follow 50/30/20 rule: 50% needs, 30% wants, 20% savings/debt payments",
                "Track textbook costs and look for rentals, used books, or digital versions",
                "Budget for irregular expenses: spring break, summer without income",
                "Take advantage of student discounts (Amazon Prime, Spotify, software)",
                "Review weekly - student budgets change with semesters and jobs"
            ]
        },
        "spending": {
            "title": "Expense Optimization Framework",
            "advice": "Strategic spending cuts can free up 15-30% of your income for savings.",
            "points": [
                "Audit all subscriptions and cancel unused services (average household has $273/month)",
                "Implement the 24-48 hour rule for purchases over $100 to reduce impulse buying",
                "Use the envelope method or spending apps to track discretionary categories",
                "Negotiate bills (insurance, phone, internet) annually - can save $500-1000/year",
                "Cook at home more often - meal planning can save $200-400/month per person",
                "Consider generic brands and bulk buying for 20-40% savings on groceries"
            ]
        },
        "save": {
            "title": "Compound Savings Acceleration",
            "advice": "Consistent saving with compound growth creates exponential wealth building.",
            "points": [
                "Automate savings immediately after payday using the 'pay yourself first' principle",
                "Start with 1% of income, increase by 1% every 6 months until reaching 20%",
                "Use high-yield savings (4-5% APY) for short-term goals, investments for long-term",
                "Save windfalls (tax refunds, bonuses) - can accelerate goals by years",
                "Set specific SMART goals: $10,000 emergency fund by December 2025",
                "Track net worth monthly to visualize progress and stay motivated"
            ]
        },
        "stress": {
            "title": "Financial Wellness Recovery Plan",
            "advice": "Financial stress affects 72% of Americans - you're not alone and it's manageable.",
            "points": [
                "Start with a simple budget to regain control - even basic tracking reduces stress",
                "Focus on one financial goal at a time to avoid overwhelm",
                "Build a $500 starter emergency fund first for immediate peace of mind",
                "Consider free financial counseling through NFCC (National Foundation for Credit Counseling)",
                "Practice financial self-care: celebrate small wins and progress milestones",
                "Remember: financial setbacks are temporary, but good habits create lasting change"
            ]
        },
        "investment": {
            "title": "Investment Fundamentals for Beginners",
            "advice": "Time in market beats timing the market - start investing early and consistently.",
            "points": [
                "Begin with employer 401(k) match (100% return) before other investments",
                "Use low-cost index funds (expense ratios under 0.1%) for broad market exposure",
                "Follow age-based allocation: (100 - your age)% in stocks, rest in bonds",
                "Invest consistently regardless of market conditions (dollar-cost averaging)",
                "Prioritize tax-advantaged accounts: 401(k), IRA, HSA before taxable accounts",
                "Rebalance annually to maintain target allocation and capture gains"
            ]
        },
        "retirement": {
            "title": "Retirement Planning Roadmap",
            "advice": "Starting early gives you the power of compound interest over decades.",
            "points": [
                "Aim to save 10-15% of income for retirement starting in your 20s",
                "Use the 4% rule: need 25x annual expenses saved for retirement",
                "Maximize employer match first, then IRA, then additional 401(k) contributions",
                "Consider Roth vs Traditional based on current vs expected future tax rates",
                "Increase contributions by 1% annually or with each raise",
                "Review and adjust strategy every 5 years or with major life changes"
            ]
        }
    }

def get_professional_responses():
    """Professional-specific financial responses"""
    return {
        "student loan": {
            "title": "Professional Loan Optimization Strategy",
            "advice": "Strategic loan management and tax optimization can save significant money.",
            "points": [
                "Evaluate refinancing options with rates as low as 3-4% for excellent credit",
                "Consider tax deductibility of student loan interest (up to $2,500 annually)",
                "Implement avalanche method: pay minimums on all, extra on highest rate",
                "Explore employer student loan repayment benefits (up to $5,250 tax-free)",
                "Balance loan payoff vs investment returns - invest if market returns > loan rate",
                "Consider PSLF only if committed to 10+ years of qualifying employment"
            ]
        },
        "emergency fund": {
            "title": "Professional Emergency Fund Strategy",
            "advice": "Optimize emergency fund placement for maximum returns while maintaining liquidity.",
            "points": [
                "Target 6 months of expenses for professionals (higher than 3-month minimum)",
                "Use high-yield savings accounts earning 4-5% APY for immediate access",
                "Consider laddered CDs for portion of emergency fund to maximize returns",
                "Automate transfers of 10-15% of gross income until fully funded",
                "Keep emergency fund separate from investment accounts to avoid market risk",
                "Review annually and adjust for lifestyle inflation and income changes"
            ]
        },
        "budget": {
            "title": "Professional Wealth Building Budget",
            "advice": "Optimize cash flow for maximum wealth accumulation and tax efficiency.",
            "points": [
                "Implement zero-based budgeting with focus on wealth building categories",
                "Maximize tax-advantaged accounts: 401(k), IRA, HSA before taxable investing",
                "Track net worth monthly, not just cash flow - focus on asset accumulation",
                "Automate investments and bill payments to reduce decision fatigue",
                "Budget for professional development, networking, and career advancement",
                "Review quarterly with focus on optimizing tax efficiency and investment allocation"
            ]
        },
        "investment": {
            "title": "Professional Investment Portfolio Strategy",
            "advice": "Build diversified, tax-efficient portfolio aligned with professional income growth.",
            "points": [
                "Maximize employer 401(k) match first - guaranteed 100% return on investment",
                "Use low-cost index funds with expense ratios under 0.1% for core holdings",
                "Implement tax-loss harvesting in taxable accounts to minimize tax burden",
                "Consider backdoor Roth IRA if income exceeds direct contribution limits",
                "Rebalance annually or when allocations drift 5% from target",
                "Evaluate need for financial advisor when portfolio exceeds $500K-1M"
            ]
        },
        "retirement": {
            "title": "Executive Retirement Planning",
            "advice": "Maximize retirement savings with sophisticated strategies and tax optimization.",
            "points": [
                "Contribute maximum to 401(k): $23,000 + $7,500 catch-up if 50+ (2024 limits)",
                "Utilize mega backdoor Roth if plan allows after-tax contributions",
                "Consider defined benefit plans or cash balance plans for high earners",
                "Implement tax diversification: traditional, Roth, and taxable accounts",
                "Plan for healthcare costs in retirement - consider HSA as retirement account",
                "Review estate planning and beneficiary designations annually"
            ]
        }
    }

    # Enhanced keyword matching with financial intelligence
    user_lower = user_input.lower()

    # Create keyword mapping for better matching
    keyword_mapping = {
        "student loan": ["student", "loan", "college", "university", "education debt", "federal loan", "private loan"],
        "emergency fund": ["emergency", "fund", "rainy day", "unexpected", "crisis", "job loss"],
        "budget": ["budget", "budgeting", "spending plan", "money management", "track expenses"],
        "spending": ["spending", "expenses", "cut costs", "reduce", "save money", "frugal"],
        "save": ["saving", "savings", "save money", "build wealth", "accumulate"],
        "stress": ["stress", "anxiety", "worried", "overwhelmed", "financial pressure"],
        "investment": ["invest", "investing", "stocks", "bonds", "401k", "ira", "portfolio", "market"],
        "retirement": ["retirement", "retire", "pension", "401k", "roth", "social security"]
    }

    # Score each category based on keyword matches
    scores = {}
    for category, keywords in keyword_mapping.items():
        score = sum(1 for keyword in keywords if keyword in user_lower)
        if score > 0:
            scores[category] = score

    # Find best match
    if scores:
        best_match = max(scores.keys(), key=lambda k: scores[k])
        if best_match in fallback_responses:
            response_data = fallback_responses[best_match]

            # Enhanced formatting with financial context
            mode_emoji = "🎓" if st.session_state.user_mode == 'student' else "💼"
            formatted_response = f"{mode_emoji} **{response_data['title']}**\n\n"

            # Add amount context if available
            if financial_context.get('amounts'):
                amounts = financial_context['amounts']
                if len(amounts) == 1:
                    formatted_response += f"💰 **Amount Focus:** ${amounts[0]:,.2f}\n\n"

            formatted_response += f"**Key Insight:** {response_data['advice']}\n\n"
            formatted_response += "**Actionable Steps:**\n"
            for i, point in enumerate(response_data['points'], 1):
                formatted_response += f"{i}. {point}\n"

            # Add contextual tip
            tip = get_contextual_tips(financial_context)
            if tip:
                formatted_response += f"\n💡 **Pro Tip:** {tip}\n"

            return formatted_response

    # Enhanced default response with mode-specific guidance
    mode_emoji = "🎓" if st.session_state.user_mode == 'student' else "💼"
    mode_title = "Student Financial Guidance" if st.session_state.user_mode == 'student' else "Professional Financial Strategy"

    if st.session_state.user_mode == 'student':
        specialties = [
            "💳 **Student Loan Management** - Federal aid, repayment plans, forgiveness programs",
            "💰 **Budget-Friendly Saving** - Emergency funds, part-time income optimization",
            "📊 **College Budgeting** - Textbooks, living expenses, entertainment on a budget",
            "🏦 **Credit Building** - Safe strategies to build credit history from scratch",
            "🎯 **Post-Grad Planning** - Career transition, salary negotiation, first job finances",
            "💡 **Student Resources** - Discounts, free tools, money-saving tips"
        ]
    else:
        specialties = [
            "💳 **Advanced Debt Strategy** - Mortgage optimization, tax-efficient payoff plans",
            "💰 **Wealth Building** - Investment portfolios, retirement acceleration",
            "📊 **Tax Optimization** - 401(k) maximization, tax-loss harvesting, estate planning",
            "📈 **Investment Strategy** - Asset allocation, rebalancing, alternative investments",
            "🏠 **Major Financial Goals** - Real estate, business investment, wealth preservation",
            "💡 **Executive Planning** - Stock options, compensation optimization, advanced strategies"
        ]

    specialty_text = "\n".join([f"• {specialty}" for specialty in specialties])

    return f"""{mode_emoji} **{mode_title}**

**I'm your specialized AI financial advisor!** I focus on:

{specialty_text}

{f"**I noticed you mentioned:** ${', $'.join(f'{amt:,.2f}' for amt in financial_context['amounts'])}" if financial_context.get('amounts') else ""}

**Ask me anything specific about your {st.session_state.user_mode} financial situation!**"""

def main():
    # Sidebar navigation
    st.sidebar.title("🏦 Personal Finance App")
    
    pages = {
        "🏠 Home": "home",
        "💬 Finance Chatbot": "chatbot",
        "🎤 Speech-to-Speech": "speech",
        "📊 Budget Tracker": "budget",
        "💰 Savings Goals": "savings",
        "📈 Investment Guide": "investment"
    }
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key

    # Show session history for chatbot page
    if st.session_state.current_page == "chatbot":
        show_session_history()

    # Main content based on current page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "chatbot":
        show_chatbot_page()
    elif st.session_state.current_page == "speech":
        show_speech_to_speech_page()
    elif st.session_state.current_page == "budget":
        show_budget_page()
    elif st.session_state.current_page == "savings":
        show_savings_page()
    elif st.session_state.current_page == "investment":
        show_investment_page()

def show_session_history():
    """Show session history in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Chat History")

    # New session button
    if st.sidebar.button("🆕 New Chat Session", help="Start a fresh conversation"):
        save_current_session()  # Save current session first
        create_new_session()
        st.rerun()

    # Show existing sessions
    if st.session_state.chat_sessions:
        st.sidebar.markdown("**Previous Sessions:**")

        # Sort sessions by timestamp (newest first)
        sorted_sessions = sorted(
            st.session_state.chat_sessions.items(),
            key=lambda x: x[1]['timestamp'],
            reverse=True
        )

        for session_id, session_data in sorted_sessions:
            col1, col2 = st.sidebar.columns([3, 1])

            with col1:
                # Session button with title and mode
                mode_emoji = "🎓" if session_data['mode'] == 'student' else "💼"
                button_label = f"{mode_emoji} {session_data['title'][:25]}..."

                if st.button(button_label, key=f"load_{session_id}",
                           help=f"Load {session_data['mode']} session from {session_data['timestamp']}"):
                    save_current_session()  # Save current before loading
                    load_session(session_id)
                    st.rerun()

            with col2:
                # Delete button
                if st.button("🗑️", key=f"del_{session_id}", help="Delete this session"):
                    delete_session(session_id)
                    st.rerun()

        # Clear all sessions button
        if len(st.session_state.chat_sessions) > 1:
            if st.sidebar.button("🗑️ Clear All History", help="Delete all chat sessions"):
                st.session_state.chat_sessions = {}
                st.session_state.current_session_id = None
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.sidebar.info("No previous sessions yet. Start chatting to create history!")

def show_home_page():
    st.markdown('<h1 class="main-header">Personal Finance Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Intelligent Guidance for Savings, Taxes, and Investments</h3>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Financial Advisor</h3>
            <p>Get personalized financial advice powered by IBM's Granite AI model. Our chatbot understands your unique situation and provides tailored recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Smart Budget Analysis</h3>
            <p>Track your expenses, analyze spending patterns, and get actionable insights to optimize your budget and increase your savings.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Goal-Based Planning</h3>
            <p>Set and track financial goals whether it's building an emergency fund, saving for a house, or planning for retirement.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Personalized Recommendations</h3>
            <p>Receive customized advice based on your demographics, financial situation, and goals. Different guidance for students vs. professionals.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Get Started")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Start Chatting", type="primary"):
            st.session_state.current_page = "chatbot"
            st.rerun()
    
    with col2:
        if st.button("📊 Track Budget"):
            st.session_state.current_page = "budget"
            st.rerun()
    
    with col3:
        if st.button("💰 Set Goals"):
            st.session_state.current_page = "savings"
            st.rerun()

def show_speech_to_speech_page():
    """Speech-to-Speech page using working implementation"""
    st.title("🎤 Speech-to-Speech Financial Advisor")
    st.markdown("### Powered by Deepgram + DeepSeek + ElevenLabs")

    # Handle working voice input processing
    try:
        working_voice_input = st.query_params.get('working_voice_input', '')
        working_mode = st.query_params.get('working_mode', '')

        if working_voice_input and working_mode == 'speech_to_speech':
            # Process voice input automatically
            st.session_state.chat_history.append({"role": "user", "content": working_voice_input})

            # Generate response using working system
            with st.spinner("🤖 Processing with DeepSeek AI..."):
                result = process_speech_to_speech_complete(working_voice_input)

            if result["success"]:
                st.session_state.chat_history.append({"role": "assistant", "content": result["response"]})

                st.success("🔊 ElevenLabs voice response ready!")

                # Show conversation
                st.markdown("### 💬 Speech-to-Speech Conversation")
                st.write(f"**You said:** {working_voice_input}")
                st.write(f"**AI responded:** {result['response']}")

                # Play audio if available
                if result["audio_data"]:
                    st.audio(result["audio_data"], format='audio/mp3', autoplay=True)
                else:
                    st.warning("Voice generation failed, but text response available")
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")

            # Save session
            save_current_session()

            # Clear the query parameters
            st.query_params.clear()
            st.rerun()

    except Exception as e:
        pass  # Fallback for older Streamlit versions

    # Main Speech-to-Speech Interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 🎤 Voice Interface")
        # Working speech-to-speech interface
        st.components.v1.html(create_working_speech_interface(), height=400)

    with col2:
        st.markdown("#### 🧪 Test Working System")

        # Demo text input for testing
        demo_text = st.text_input("Test with text:", value="How can I improve my credit score?")

        # Voice selection (ElevenLabs voices)
        voice_options = {
            "Default Voice": ELEVENLABS_VOICE_ID,
            "Alternative Voice 1": "21m00Tcm4TlvDq8ikWAM",
            "Alternative Voice 2": "AZnzlk1XvdvUeBnXmlld"
        }

        selected_voice_name = st.selectbox("Choose ElevenLabs Voice:", list(voice_options.keys()))
        selected_voice_id = voice_options.get(selected_voice_name, ELEVENLABS_VOICE_ID)

        if st.button("🔊 Generate Working Voice Response") and demo_text:
            with st.spinner("🤖 Processing with working system..."):
                result = process_speech_to_speech_complete(demo_text)

                if result["success"]:
                    st.success("✅ Working speech-to-speech successful!")
                    st.write(f"**Question:** {demo_text}")
                    st.write(f"**AI Response:** {result['response']}")

                    if result["audio_data"]:
                        st.audio(result["audio_data"], format='audio/mp3')
                    else:
                        st.warning("Voice generation failed, but text response available")
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")

        # System information
        st.markdown("#### ℹ️ System Info")
        st.info("🎯 **Working System:**\n- Deepgram: Speech-to-text\n- Gemini: AI responses\n- ElevenLabs: Text-to-speech\n- Proven & reliable")

        # API status
        st.markdown("#### 🔧 API Status")
        if DEEPGRAM_API_KEY:
            st.success("✅ Deepgram API configured")
        else:
            st.error("❌ Deepgram API missing")

        if GEMINI_API_KEY:
            st.success("✅ Gemini API configured")
        else:
            st.error("❌ Gemini API missing")

        if ELEVENLABS_API_KEY:
            st.success("✅ ElevenLabs API configured")
        else:
            st.error("❌ ElevenLabs API missing")

    # Show chat history if available
    if st.session_state.chat_history:
        st.markdown("### 💬 Recent Conversations")
        for i, message in enumerate(st.session_state.chat_history[-4:]):  # Show last 4 messages
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")
            st.markdown("---")

def show_chatbot_page():
    # Initialize session if needed
    if not st.session_state.current_session_id:
        create_new_session()

    # Add JavaScript to handle voice input messages
    st.markdown("""
    <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'voice_submit') {
                // Set voice input in Streamlit session state
                window.parent.postMessage({
                    type: 'streamlit_voice_input',
                    text: event.data.text,
                    autoSubmit: event.data.autoSubmit
                }, '*');
            }
        });
    </script>
    """, unsafe_allow_html=True)

    # Removed speech-to-speech handling

    # Show the appropriate interface based on mode
    if st.session_state.user_mode == 'student':
        show_student_interface()
    else:
        show_professional_interface()

def show_student_interface():
    # Student-specific header and styling
    st.markdown("""
    <div class="student-mode">
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 3rem; font-weight: 800;
                   color: #1565c0; text-align: center; margin: 2rem 0; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            🎓 Student Financial Advisor
        </h1>
        <div style="background: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
                    border: 2px solid #2196f3; box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);">
            <p style="font-family: 'Source Sans Pro', sans-serif; font-size: 1.2rem; color: #263238; margin: 0; font-weight: 500;">
                💡 Smart financial guidance for students and recent graduates
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mode switch button
    if st.button("🔄 Switch to Professional Mode", key="switch_to_pro_top", help="Switch to professional financial advisor"):
        st.session_state.user_mode = 'professional'
        st.session_state.chat_history = []
        st.rerun()

    # Student-specific scenarios
    st.markdown("### 🎯 Student Financial Scenarios")

    student_scenarios = {
        "💳 Student Loan Help": "I have student loans and need help understanding my repayment options and strategies to minimize interest while managing other expenses on a tight budget.",
        "💰 College Budgeting": "Help me create a realistic budget for college life including tuition, textbooks, living expenses, and some entertainment money while working part-time.",
        "🏦 Building Credit": "I'm new to credit and want to build a good credit score safely as a student. What's the best way to start building credit without getting into debt?",
        "📚 Textbook & Expenses": "How can I save money on textbooks, school supplies, and other college expenses while still getting quality education materials?",
        "🎓 Post-Grad Planning": "I'm graduating soon and need help planning my finances for the transition from student life to professional career. What should I prepare for?",
        "😰 Money Stress": "I'm stressed about money as a student with limited income. Can you help me manage my finances better and reduce financial anxiety?"
    }

    # Student scenario buttons with custom styling
    cols = st.columns(2)
    for i, (scenario, prompt) in enumerate(student_scenarios.items()):
        with cols[i % 2]:
            if st.button(scenario, key=f"student_scenario_{i}",
                        help=f"Get student-focused advice about {scenario.lower()}"):
                # Auto-load model silently if not loaded and available
                if not st.session_state.model_loaded and TRANSFORMERS_AVAILABLE:
                    load_model_silently()

                # Add the full question as if user typed it
                st.session_state.chat_history.append({"role": "user", "content": prompt})

                # Generate response using the same logic as manual input
                response = generate_response(prompt)

                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Removed voice response generation

                # Save session automatically
                save_current_session()
                st.rerun()

    # Student chat interface
    st.markdown("### 💬 Chat with Your Student Financial Advisor")

    # Student-specific chat display
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message student-message">
                    <strong>🎓 You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Render student bot messages
                st.markdown('<div class="chat-message student-bot-message">', unsafe_allow_html=True)
                st.markdown(message["content"])
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem; background: white;
                    border-radius: 15px; margin: 1rem 0; border: 2px solid #2196f3;
                    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);">
            <h3 style="color: #1565c0; font-family: 'Poppins', sans-serif; font-weight: 700; margin-bottom: 1rem;">👋 Welcome, Student!</h3>
            <p style="color: #263238; font-family: 'Source Sans Pro', sans-serif; font-size: 1.1rem; font-weight: 500; line-height: 1.6;">
                I'm here to help you navigate your financial journey as a student.<br>
                Ask me about budgeting, student loans, building credit, or any money questions!
            </p>
            <p style="color: #546e7a; font-style: italic; margin-top: 1rem;">Try the scenario buttons above for quick help!</p>
        </div>
        """, unsafe_allow_html=True)

    # Removed speech-to-speech interface

    # Student input interface
    user_input = st.text_input(
        "Ask your student financial question:",
        placeholder="e.g., How can I save money on textbooks and still build an emergency fund?",
        key="student_chat_input",
        value=st.session_state.voice_input if st.session_state.voice_input else ""
    )

    # Process student input (both typed and voice)
    if (user_input and user_input.strip()) or st.session_state.auto_submit_voice:
        # Use voice input if available, otherwise use typed input
        input_text = st.session_state.voice_input if st.session_state.voice_input else user_input

        if input_text and input_text.strip():
            # Auto-load model silently
            if not st.session_state.model_loaded and TRANSFORMERS_AVAILABLE:
                load_model_silently()

            st.session_state.chat_history.append({"role": "user", "content": input_text})

            # Show processing message for voice input
            if st.session_state.voice_input:
                with st.spinner("🤖 AI is thinking about your question..."):
                    response = generate_response(input_text)
            else:
                response = generate_response(input_text)

            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Removed voice response generation

            # Reset voice input state
            st.session_state.voice_input = ""
            st.session_state.auto_submit_voice = False

            # Save session automatically
            save_current_session()
            st.rerun()

    # Student action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Chat", key="student_clear", help="Start fresh conversation"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("💡 Study Tips", key="student_tips", help="Get money-saving tips for students"):
            st.session_state.chat_history.append({"role": "user", "content": "Student Money-Saving Tips"})
            response = generate_response("Give me the top 10 money-saving tips every college student should know, including ways to save on textbooks, food, and entertainment.")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    with col3:
        if st.button("🔄 Switch to Professional", key="switch_to_pro", help="Switch to professional mode"):
            st.session_state.user_mode = 'professional'
            st.session_state.chat_history = []  # Clear chat when switching modes
            st.rerun()



def show_professional_interface():
    # Professional-specific header and styling
    st.markdown("""
    <div class="professional-mode">
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 3rem; font-weight: 800;
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   text-align: center; margin: 2rem 0;">
            💼 Professional Financial Strategist
        </h1>
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    padding: 1rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
                    border: 1px solid rgba(102, 126, 234, 0.2);">
            <p style="font-family: 'Source Sans Pro', sans-serif; font-size: 1.1rem; color: #2c3e50; margin: 0;">
                🚀 Advanced wealth building and optimization strategies
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mode switch button
    if st.button("🔄 Switch to Student Mode", key="switch_to_student_top", help="Switch to student financial advisor"):
        st.session_state.user_mode = 'student'
        st.session_state.chat_history = []
        st.rerun()

    # Professional-specific scenarios
    st.markdown("### 🎯 Professional Financial Strategies")

    professional_scenarios = {
        "📈 Portfolio Optimization": "I'm a working professional looking to optimize my investment portfolio for maximum returns with appropriate risk management. Help me create a strategy for long-term wealth building.",
        "💰 Tax Strategy": "I need advanced tax optimization strategies for my high income and investment portfolio. What are the best ways to minimize taxes while building wealth?",
        "🏠 Real Estate Investment": "I'm considering real estate investment as part of my portfolio diversification strategy. What should I know about property investment and how to get started?",
        "🎯 Retirement Acceleration": "I want to retire early or maximize my retirement savings with advanced strategies. What are the best approaches for aggressive retirement planning?",
        "💼 Executive Compensation": "Help me optimize my executive compensation package including stock options, 401k matching, and other benefits. How can I maximize my total compensation?",
        "🏛️ Wealth Preservation": "I've built substantial wealth and want to focus on preservation, estate planning, and tax-efficient growth strategies for long-term wealth management."
    }

    # Professional scenario buttons with custom styling
    cols = st.columns(2)
    for i, (scenario, prompt) in enumerate(professional_scenarios.items()):
        with cols[i % 2]:
            if st.button(scenario, key=f"professional_scenario_{i}",
                        help=f"Get advanced professional advice about {scenario.lower()}"):
                # Auto-load model silently if not loaded and available
                if not st.session_state.model_loaded and TRANSFORMERS_AVAILABLE:
                    load_model_silently()

                # Add the full question as if user typed it
                st.session_state.chat_history.append({"role": "user", "content": prompt})

                # Generate response using the same logic as manual input
                response = generate_response(prompt)

                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Removed voice response generation

                # Save session automatically
                save_current_session()
                st.rerun()

    # Professional chat interface
    show_professional_chat()

def show_professional_chat():
    st.markdown("### 💬 Executive Financial Consultation")

    # Professional-specific chat display
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message professional-message">
                    <strong>💼 You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Render professional bot messages
                st.markdown('<div class="chat-message professional-bot-message">', unsafe_allow_html=True)
                st.markdown(message["content"])
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(102, 126, 234, 0.2);">
            <h3 style="color: #667eea; font-family: 'Poppins', sans-serif;">👋 Welcome, Professional!</h3>
            <p style="color: #2c3e50; font-family: 'Source Sans Pro', sans-serif; font-size: 1.1rem;">
                I'm your advanced financial strategist, ready to help optimize your wealth.<br>
                Ask me about investments, tax strategies, real estate, or complex financial planning!
            </p>
            <p style="color: #666; font-style: italic;">Try the strategy buttons above for expert guidance!</p>
        </div>
        """, unsafe_allow_html=True)

    # Removed executive speech-to-speech interface

    # Professional input interface
    user_input = st.text_input(
        "Ask your strategic financial question:",
        placeholder="e.g., How should I allocate $500K across different asset classes for optimal returns?",
        key="professional_chat_input",
        value=st.session_state.voice_input if st.session_state.voice_input else ""
    )

    # Process professional input (both typed and voice)
    if (user_input and user_input.strip()) or st.session_state.auto_submit_voice:
        # Use voice input if available, otherwise use typed input
        input_text = st.session_state.voice_input if st.session_state.voice_input else user_input

        if input_text and input_text.strip():
            # Auto-load model silently
            if not st.session_state.model_loaded and TRANSFORMERS_AVAILABLE:
                load_model_silently()

            st.session_state.chat_history.append({"role": "user", "content": input_text})

            # Show processing message for voice input
            if st.session_state.voice_input:
                with st.spinner("🤖 AI is analyzing your strategic question..."):
                    response = generate_response(input_text)
            else:
                response = generate_response(input_text)

            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Removed voice response generation

            # Reset voice input state
            st.session_state.voice_input = ""
            st.session_state.auto_submit_voice = False

            # Save session automatically
            save_current_session()
            st.rerun()

    # Professional action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Strategy Session", key="professional_clear", help="Start fresh consultation"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("📊 Portfolio Analysis", key="professional_analysis", help="Get comprehensive portfolio review"):
            st.session_state.chat_history.append({"role": "user", "content": "Portfolio Analysis Request"})
            response = generate_response("Provide a comprehensive portfolio analysis framework including asset allocation, risk assessment, tax efficiency, and rebalancing strategies for a high-net-worth professional.")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    with col3:
        if st.button("🔄 Switch to Student", key="switch_to_student", help="Switch to student mode"):
            st.session_state.user_mode = 'student'
            st.session_state.chat_history = []  # Clear chat when switching modes
            st.rerun()

def show_budget_page():
    st.markdown('<h1 class="main-header">📊 Budget Tracker</h1>', unsafe_allow_html=True)

    st.markdown("### 💰 Monthly Budget Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Income")
        monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=3000.0, step=100.0)

        st.subheader("Fixed Expenses")
        rent = st.number_input("Rent/Mortgage ($)", min_value=0.0, value=1000.0, step=50.0)
        utilities = st.number_input("Utilities ($)", min_value=0.0, value=150.0, step=25.0)
        insurance = st.number_input("Insurance ($)", min_value=0.0, value=200.0, step=25.0)

        st.subheader("Variable Expenses")
        food = st.number_input("Food & Groceries ($)", min_value=0.0, value=400.0, step=25.0)
        transportation = st.number_input("Transportation ($)", min_value=0.0, value=300.0, step=25.0)
        entertainment = st.number_input("Entertainment ($)", min_value=0.0, value=200.0, step=25.0)
        other = st.number_input("Other Expenses ($)", min_value=0.0, value=150.0, step=25.0)

    with col2:
        # Calculate totals
        total_expenses = rent + utilities + insurance + food + transportation + entertainment + other
        remaining = monthly_income - total_expenses

        # Create expense breakdown
        if PLOTLY_AVAILABLE:
            expenses_data = {
                'Category': ['Rent/Mortgage', 'Utilities', 'Insurance', 'Food', 'Transportation', 'Entertainment', 'Other'],
                'Amount': [rent, utilities, insurance, food, transportation, entertainment, other]
            }

            fig = px.pie(expenses_data, values='Amount', names='Category', title='Expense Breakdown')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("### 📊 Expense Breakdown")
            expenses = [
                ("Rent/Mortgage", rent),
                ("Utilities", utilities),
                ("Insurance", insurance),
                ("Food", food),
                ("Transportation", transportation),
                ("Entertainment", entertainment),
                ("Other", other)
            ]
            for category, amount in expenses:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                st.write(f"**{category}**: ${amount:,.2f} ({percentage:.1f}%)")
                st.progress(percentage / 100)

        # Budget summary
        st.markdown("### 📈 Budget Summary")
        st.metric("Monthly Income", f"${monthly_income:,.2f}")
        st.metric("Total Expenses", f"${total_expenses:,.2f}")

        if remaining >= 0:
            st.metric("Remaining/Savings", f"${remaining:,.2f}", delta=f"{(remaining/monthly_income)*100:.1f}%")
            st.success(f"Great! You have ${remaining:,.2f} left for savings and investments.")
        else:
            st.metric("Over Budget", f"${abs(remaining):,.2f}", delta=f"{(remaining/monthly_income)*100:.1f}%")
            st.error(f"You're over budget by ${abs(remaining):,.2f}. Consider reducing expenses.")

        # 50/30/20 rule comparison
        st.markdown("### 🎯 50/30/20 Rule Comparison")
        needs_target = monthly_income * 0.5
        wants_target = monthly_income * 0.3
        savings_target = monthly_income * 0.2

        needs_actual = rent + utilities + insurance + food
        wants_actual = transportation + entertainment + other
        savings_actual = remaining if remaining > 0 else 0

        if PLOTLY_AVAILABLE:
            comparison_data = pd.DataFrame({
                'Category': ['Needs (50%)', 'Wants (30%)', 'Savings (20%)'],
                'Target': [needs_target, wants_target, savings_target],
                'Actual': [needs_actual, wants_actual, savings_actual]
            })

            fig2 = px.bar(comparison_data, x='Category', y=['Target', 'Actual'],
                         title='Budget vs 50/30/20 Rule', barmode='group')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.markdown("### 🎯 50/30/20 Rule Comparison")
            categories = [
                ("Needs (50%)", needs_target, needs_actual),
                ("Wants (30%)", wants_target, wants_actual),
                ("Savings (20%)", savings_target, savings_actual)
            ]
            for category, target, actual in categories:
                st.write(f"**{category}**")
                st.write(f"Target: ${target:,.2f} | Actual: ${actual:,.2f}")
                if target > 0:
                    percentage = min(actual / target * 100, 100)
                    st.progress(percentage / 100)
                st.write("---")

def show_savings_page():
    st.markdown('<h1 class="main-header">💰 Savings Goals</h1>', unsafe_allow_html=True)

    st.markdown("### 🎯 Set Your Financial Goals")

    col1, col2 = st.columns(2)

    with col1:
        goal_name = st.text_input("Goal Name", value="Emergency Fund")
        target_amount = st.number_input("Target Amount ($)", min_value=0.0, value=5000.0, step=100.0)
        current_amount = st.number_input("Current Amount ($)", min_value=0.0, value=500.0, step=50.0)
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=200.0, step=25.0)

        # Calculate progress
        progress = (current_amount / target_amount) * 100 if target_amount > 0 else 0
        remaining = target_amount - current_amount
        months_to_goal = remaining / monthly_contribution if monthly_contribution > 0 else float('inf')

        st.markdown("### 📊 Goal Progress")
        st.progress(progress / 100)
        st.write(f"Progress: {progress:.1f}% ({current_amount:,.0f} / {target_amount:,.0f})")

        if months_to_goal != float('inf'):
            st.write(f"Time to goal: {months_to_goal:.1f} months")
            target_date = datetime.now().month + months_to_goal
            st.write(f"Estimated completion: {int(target_date)} months from now")

        st.metric("Remaining Amount", f"${remaining:,.2f}")

    with col2:
        # Savings projection
        if PLOTLY_AVAILABLE:
            months = list(range(0, int(months_to_goal) + 2 if months_to_goal != float('inf') else 25))
            projected_savings = [current_amount + (month * monthly_contribution) for month in months]
            projected_savings = [min(amount, target_amount) for amount in projected_savings]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=projected_savings, mode='lines+markers', name='Projected Savings'))
            fig.add_hline(y=target_amount, line_dash="dash", line_color="red", annotation_text="Target")
            fig.update_layout(title='Savings Projection', xaxis_title='Months', yaxis_title='Amount ($)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("### 📈 Savings Projection")
            st.write(f"**Current Amount**: ${current_amount:,.2f}")
            st.write(f"**Target Amount**: ${target_amount:,.2f}")
            st.write(f"**Monthly Contribution**: ${monthly_contribution:,.2f}")
            if months_to_goal != float('inf'):
                for i in range(0, min(int(months_to_goal) + 1, 12), 3):
                    projected = min(current_amount + (i * monthly_contribution), target_amount)
                    st.write(f"Month {i}: ${projected:,.2f}")
            else:
                st.write("Add monthly contributions to see projection")

        # Savings tips
        st.markdown("### 💡 Savings Tips")
        tips = [
            "Automate your savings to make it effortless",
            "Start small and gradually increase your contributions",
            "Use the 24-hour rule for non-essential purchases",
            "Track your progress weekly to stay motivated",
            "Consider high-yield savings accounts for better returns"
        ]

        for tip in tips:
            st.write(f"• {tip}")

def show_investment_page():
    st.markdown('<h1 class="main-header">📈 Investment Guide</h1>', unsafe_allow_html=True)

    st.markdown("### 🎓 Investment Basics")

    tab1, tab2, tab3 = st.tabs(["Getting Started", "Risk Assessment", "Portfolio Suggestions"])

    with tab1:
        st.markdown("""
        #### 🌟 Investment Fundamentals

        **1. Emergency Fund First**
        - Build 3-6 months of expenses before investing
        - Keep emergency funds in high-yield savings accounts

        **2. Understand Your Timeline**
        - Short-term goals (< 5 years): Conservative investments
        - Long-term goals (> 10 years): Growth-oriented investments

        **3. Diversification is Key**
        - Don't put all eggs in one basket
        - Mix stocks, bonds, and other asset classes

        **4. Start Early**
        - Time in market beats timing the market
        - Compound interest is your best friend
        """)

        # Investment calculator
        st.markdown("### 🧮 Investment Calculator")
        col1, col2 = st.columns(2)

        with col1:
            initial_investment = st.number_input("Initial Investment ($)", min_value=0.0, value=1000.0, step=100.0)
            monthly_investment = st.number_input("Monthly Investment ($)", min_value=0.0, value=300.0, step=50.0)
            annual_return = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)
            years = st.slider("Investment Period (years)", min_value=1, max_value=40, value=20)

        with col2:
            # Calculate compound growth
            monthly_rate = annual_return / 100 / 12
            months = years * 12

            # Future value calculation
            fv_initial = initial_investment * (1 + annual_return/100) ** years
            fv_monthly = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            total_future_value = fv_initial + fv_monthly
            total_invested = initial_investment + (monthly_investment * months)
            total_gains = total_future_value - total_invested

            st.metric("Total Future Value", f"${total_future_value:,.2f}")
            st.metric("Total Invested", f"${total_invested:,.2f}")
            st.metric("Total Gains", f"${total_gains:,.2f}", delta=f"{(total_gains/total_invested)*100:.1f}%")

    with tab2:
        st.markdown("### 🎯 Risk Assessment")

        age = st.slider("Your Age", min_value=18, max_value=80, value=30)
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
            value="Moderate"
        )
        investment_timeline = st.selectbox(
            "Investment Timeline",
            ["Less than 5 years", "5-10 years", "10-20 years", "More than 20 years"]
        )

        # Risk-based recommendations
        if risk_tolerance in ["Very Conservative", "Conservative"]:
            st.info("**Recommended Allocation:** 70% Bonds, 30% Stocks")
        elif risk_tolerance == "Moderate":
            st.info("**Recommended Allocation:** 60% Stocks, 40% Bonds")
        else:
            st.info("**Recommended Allocation:** 80% Stocks, 20% Bonds")

    with tab3:
        st.markdown("### 📊 Sample Portfolios")

        portfolio_type = st.selectbox(
            "Choose Portfolio Type",
            ["Conservative", "Balanced", "Growth", "Aggressive Growth"]
        )

        portfolios = {
            "Conservative": {"Bonds": 60, "Large Cap Stocks": 25, "International": 10, "Cash": 5},
            "Balanced": {"Large Cap Stocks": 40, "Bonds": 30, "International": 20, "Small Cap": 10},
            "Growth": {"Large Cap Stocks": 50, "International": 25, "Small Cap": 15, "Bonds": 10},
            "Aggressive Growth": {"Large Cap Stocks": 45, "Small Cap": 25, "International": 20, "Emerging Markets": 10}
        }

        selected_portfolio = portfolios[portfolio_type]

        # Portfolio allocation display
        if PLOTLY_AVAILABLE:
            fig = px.pie(
                values=list(selected_portfolio.values()),
                names=list(selected_portfolio.keys()),
                title=f"{portfolio_type} Portfolio Allocation"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(f"### 📊 {portfolio_type} Portfolio Allocation")
            for asset, percentage in selected_portfolio.items():
                st.write(f"**{asset}**: {percentage}%")
                st.progress(percentage / 100)

        st.markdown("### ⚠️ Important Disclaimers")
        st.warning("""
        - This is educational content only, not financial advice
        - Past performance doesn't guarantee future results
        - Consider consulting with a financial advisor
        - Invest only what you can afford to lose
        - Do your own research before investing
        """)

if __name__ == "__main__":
    main()
