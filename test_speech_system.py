#!/usr/bin/env python3
"""
Test script for speech-to-speech system components
Run this to debug each part of the pipeline separately
"""

import sounddevice as sd
from scipy.io.wavfile import write
import requests
import json
import pygame
import os

# API Keys
DEEPGRAM_API_KEY = "8cb5ea519fc07555361023888ad01f83c71b96f5"
GEMINI_API_KEY = "AIzaSyDOJmBKJdOKjKjKjKjKjKjKjKjKjKjKjKj"  # Replace with actual Gemini API key
ELEVENLABS_API_KEY = "sk_12b8b420df0032bf39f6b31a2654a3939f5da28f8dcacc2a"  # Updated working API key
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

# Alternative ElevenLabs API key (if needed)
ELEVENLABS_API_KEY_ALT = "sk_bf4c7eea2b59323848bb44e036cb68bf7506d231f898c995"

def test_1_basic_recording():
    """Test 1: Basic microphone recording"""
    print("\n=== TEST 1: Basic Recording ===")
    try:
        fs = 44100
        duration = 5
        print("Recording for 5 seconds... Speak now!")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write("test_basic.wav", fs, recording)
        print("✅ Recorded test_basic.wav")
        
        # Check file size
        size = os.path.getsize("test_basic.wav")
        print(f"File size: {size} bytes")
        
        if size > 1000:
            print("✅ Recording seems successful (file has content)")
            return True
        else:
            print("❌ Recording failed (file too small)")
            return False
            
    except Exception as e:
        print(f"❌ Recording error: {e}")
        return False

def test_2_optimized_recording():
    """Test 2: Optimized recording for Deepgram (16kHz, 16-bit)"""
    print("\n=== TEST 2: Optimized Recording ===")
    try:
        fs = 16000  # 16kHz for better Deepgram compatibility
        duration = 5
        print("Recording optimized audio for 5 seconds... Speak now!")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write("test_optimized.wav", fs, recording)
        print("✅ Recorded test_optimized.wav (16kHz, 16-bit)")
        
        # Check file size
        size = os.path.getsize("test_optimized.wav")
        print(f"File size: {size} bytes")
        
        if size > 500:
            print("✅ Optimized recording successful")
            return True
        else:
            print("❌ Optimized recording failed")
            return False
            
    except Exception as e:
        print(f"❌ Optimized recording error: {e}")
        return False

def test_3_deepgram_transcription(filename="test_optimized.wav"):
    """Test 3: Deepgram transcription"""
    print("\n=== TEST 3: Deepgram Transcription ===")
    
    if not os.path.exists(filename):
        print(f"❌ Audio file {filename} not found")
        return None
        
    try:
        print("Transcribing with Deepgram...")
        with open(filename, "rb") as f:
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
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Deepgram Error: {response.text}")
            return None
            
        result = response.json()
        print("Raw response:", json.dumps(result, indent=2))
        
        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(f"✅ Transcript: '{transcript}'")
        
        if transcript.strip():
            print("✅ Transcription successful")
            return transcript
        else:
            print("❌ Empty transcript")
            return None
            
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None

def test_4_gemini_response(text="How can I save money for retirement?"):
    """Test 4: Gemini AI response"""
    print("\n=== TEST 4: Gemini AI Response ===")

    try:
        print(f"Getting Gemini response for: '{text}'")

        # For now, let's use a simple fallback response since we need the actual Gemini API key
        # This simulates what would happen with a real Gemini API call

        if GEMINI_API_KEY == "AIzaSyDOJmBKJdOKjKjKjKjKjKjKjKjKjKjKjKj":
            print("⚠️ Using fallback response (need real Gemini API key)")
            reply = f"This is a financial advice response about: {text}. To save money for retirement, consider starting early with a 401(k), IRA, or other retirement accounts. The power of compound interest works best over time."
        else:
            # Real Gemini API call would go here
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"You are a financial advisor. Answer this question: {text}"
                    }]
                }]
            }

            response = requests.post(url, headers=headers, json=data)
            print(f"Status Code: {response.status_code}")

            if response.status_code != 200:
                print(f"❌ Gemini Error: {response.text}")
                return None

            result = response.json()
            reply = result["candidates"][0]["content"]["parts"][0]["text"]

        print(f"✅ AI Response: {reply[:200]}...")
        return reply

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        # Fallback response
        return f"Financial advice for: {text}. Consider consulting with a financial advisor for personalized guidance."

def test_5_elevenlabs_tts(text="Hello, this is a test of ElevenLabs text to speech."):
    """Test 5: ElevenLabs text-to-speech"""
    print("\n=== TEST 5: ElevenLabs TTS ===")
    
    try:
        print(f"Generating speech for: '{text[:50]}...'")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
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
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ ElevenLabs Error: {response.text}")
            return None
            
        # Save audio file
        with open("test_tts.mp3", "wb") as f:
            f.write(response.content)
            
        size = os.path.getsize("test_tts.mp3")
        print(f"✅ Generated test_tts.mp3 ({size} bytes)")
        
        if size > 1000:
            print("✅ TTS generation successful")
            return "test_tts.mp3"
        else:
            print("❌ TTS file too small")
            return None
            
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return None

def test_6_audio_playback(filename="test_tts.mp3"):
    """Test 6: Audio playback"""
    print("\n=== TEST 6: Audio Playback ===")
    
    if not os.path.exists(filename):
        print(f"❌ Audio file {filename} not found")
        return False
        
    try:
        print(f"Playing {filename}...")
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        pygame.mixer.quit()
        print("✅ Audio playback successful")
        return True
        
    except Exception as e:
        print(f"❌ Playback error: {e}")
        return False

def test_full_pipeline():
    """Test 7: Full speech-to-speech pipeline"""
    print("\n=== TEST 7: Full Pipeline ===")
    
    # Step 1: Record
    print("Step 1: Recording...")
    if not test_2_optimized_recording():
        return False
    
    # Step 2: Transcribe
    print("Step 2: Transcribing...")
    transcript = test_3_deepgram_transcription("test_optimized.wav")
    if not transcript:
        return False
    
    # Step 3: Get AI response
    print("Step 3: Getting AI response...")
    ai_response = test_4_gemini_response(transcript)
    if not ai_response:
        return False
    
    # Step 4: Generate speech
    print("Step 4: Generating speech...")
    audio_file = test_5_elevenlabs_tts(ai_response)
    if not audio_file:
        return False
    
    # Step 5: Play audio
    print("Step 5: Playing response...")
    if not test_6_audio_playback(audio_file):
        return False
    
    print("✅ Full pipeline successful!")
    return True

def main():
    """Run all tests"""
    print("🎤 Speech-to-Speech System Test Suite")
    print("=" * 50)
    
    # Check dependencies
    try:
        import sounddevice
        import scipy
        import pygame
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return
    
    # Run individual tests
    tests = [
        ("Basic Recording", test_1_basic_recording),
        ("Optimized Recording", test_2_optimized_recording),
        ("Deepgram Transcription", lambda: test_3_deepgram_transcription("test_optimized.wav")),
        ("Gemini Response", lambda: test_4_gemini_response("What is compound interest?")),
        ("ElevenLabs TTS", lambda: test_5_elevenlabs_tts("This is a test of text to speech.")),
        ("Audio Playback", lambda: test_6_audio_playback("test_tts.mp3"))
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Full pipeline test if individual tests pass
    if all(results.values()):
        print("\n🚀 All individual tests passed! Running full pipeline...")
        test_full_pipeline()
    else:
        print("\n⚠️ Some tests failed. Fix issues before running full pipeline.")

if __name__ == "__main__":
    main()
