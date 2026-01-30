import os
import sys
import time
import subprocess
import requests
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# LangChain Imports
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434"

def is_ollama_running():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=1)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def start_ollama_server():
    print("⏳ Ollama server not running. Starting it in the background...")
    # This command works on Windows/Mac/Linux provided Ollama is installed
    try:
        # We use Popen to run it detached (in the background)
        if sys.platform == "win32":
            subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for it to actually wake up
        for _ in range(20): # Wait up to 20 seconds
            if is_ollama_running():
                print("✅ Ollama server started successfully!")
                return True
            time.sleep(1)
        print("❌ Failed to start Ollama automatically. Please run 'ollama serve' manually.")
        return False
    except FileNotFoundError:
        print("❌ Error: 'ollama' command not found. Please install Ollama from https://ollama.com")
        sys.exit(1)

def ensure_model_is_pulled():
    if not is_ollama_running():
        start_ollama_server()

    print(f"🔍 Checking if model '{OLLAMA_MODEL}' is available...")
    try:
        # Get list of installed models
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        installed_models = [m['name'] for m in response.json()['models']]
        
        # Check if our model (or a variant like llama3:latest) exists
        if any(OLLAMA_MODEL in m for m in installed_models):
            print(f"✅ Model '{OLLAMA_MODEL}' is ready.")
            return
        
        print(f"⚠️ Model '{OLLAMA_MODEL}' not found. Downloading now (this may take a while)...")
        # Run 'ollama pull' command
        subprocess.run(["ollama", "pull", OLLAMA_MODEL], check=True)
        print(f"✅ Model '{OLLAMA_MODEL}' downloaded successfully!")
        
    except Exception as e:
        print(f"❌ Error checking/pulling model: {e}")
