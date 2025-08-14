#!/usr/bin/env python3
"""
Comprehensive startup script for the Finance App
Starts both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import threading
import signal
import requests

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✓ Python version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ Python check failed: {e}")
        return False

def check_node():
    """Check if Node.js is available"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✓ Node.js version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ Node.js not found: {e}")
        print("  Please install Node.js from https://nodejs.org/")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True)
        print("✓ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install backend dependencies: {e}")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd="frontend", check=True)
        print("✓ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install frontend dependencies: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    try:
        os.chdir("backend")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        os.chdir("..")
        return process
    except Exception as e:
        print(f"✗ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("\n🚀 Starting frontend server...")
    try:
        process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend")
        return process
    except Exception as e:
        print(f"✗ Failed to start frontend: {e}")
        return None

def wait_for_backend():
    """Wait for backend to be ready"""
    print("\n⏳ Waiting for backend to be ready...")
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://127.0.0.1:8000/api/health", timeout=2)
            if response.status_code == 200:
                print("✓ Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"  Waiting... ({i+1}/30)")
    
    print("✗ Backend failed to start within 30 seconds")
    return False

def main():
    print("🏦 Finance App Startup Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python():
        return
    
    if not check_node():
        return
    
    # Install dependencies
    if not install_backend_deps():
        return
    
    if not install_frontend_deps():
        return
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Wait for backend to be ready
    if not wait_for_backend():
        backend_process.terminate()
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n🎉 Both servers are running!")
    print("📱 Frontend: http://localhost:5173")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers")
    
    # Handle shutdown
    def signal_handler(sig, frame):
        print("\n\n🛑 Shutting down servers...")
        frontend_process.terminate()
        backend_process.terminate()
        print("✓ Servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Wait for processes
        while True:
            if backend_process.poll() is not None:
                print("✗ Backend process died")
                break
            if frontend_process.poll() is not None:
                print("✗ Frontend process died")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        frontend_process.terminate()
        backend_process.terminate()

if __name__ == "__main__":
    main()
