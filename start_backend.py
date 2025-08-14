#!/usr/bin/env python3
"""
Simple script to start the backend server
"""

import subprocess
import sys
import os
import time

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"Python version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"Python check failed: {e}")
        return False

def install_requirements():
    """Install backend requirements"""
    print("Installing backend requirements...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True)
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("Starting FastAPI server...")
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"✗ Failed to start server: {e}")

def main():
    print("Backend Server Startup Script")
    print("=" * 40)
    
    # Check Python
    if not check_python():
        print("Please ensure Python is properly installed")
        return
    
    # Install requirements
    if not install_requirements():
        print("Please fix the requirements installation issue")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
