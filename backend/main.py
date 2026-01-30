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
from utils import ensure_model_is_pulled

from models import UserInput


OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434"


ensure_model_is_pulled()

# ==========================================
# 2. FASTAPI APP
# ==========================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Chat Model
llm = ChatOllama(
    model=OLLAMA_MODEL, 
    temperature=0.7,
    base_url=OLLAMA_URL
)


async def generate_response(message: str):
    messages = [
        SystemMessage(content="You are a helpful, intelligent AI agent. Answer clearly using Markdown formatting."),
        HumanMessage(content=message),
    ]

    async for chunk in llm.astream(messages):
        if chunk.content:
            yield chunk.content

@app.post("/chat")
async def chat_endpoint(user_input: UserInput):
    return StreamingResponse(
        generate_response(user_input.message), 
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
