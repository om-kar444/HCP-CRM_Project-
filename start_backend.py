#!/usr/bin/env python3
"""
Startup script for HCP CRM Backend
"""
import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing backend dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "hcp-crm-backend/requirements.txt"])

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting FastAPI backend server...")
    os.chdir("hcp-crm-backend")
    subprocess.run(["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    install_requirements()
    start_backend()