import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import logging

app = FastAPI()

# Default Ollama base URL
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama.ai-platform.svc.cluster.local:11434")

# Model routing rules
MODEL_ROUTING = {
    "coding": "qwen2.5-coder:7b",
    "general": "qwen2.5:3b",
    "summarization": "qwen2.5:3b"
}

# Default task classification rules
DEFAULT_TASK_CLASSIFICATION = {
    "code": "coding",
    "programming": "coding",
    "script": "coding",
    "general": "general",
    "summary": "summarization"
}

# Request timeout
REQUEST_TIMEOUT = 10.0  # seconds

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: list
    task: Optional[str] = None

@app.get("/healthz")
async def healthz():
    return {"status": "healthy"}

@app.get("/readyz")
async def readyz():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/healthz", timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        return {"status": "ready"}
    except httpx.RequestError:
        return {"status": "not ready"}, status.HTTP_503_SERVICE_UNAVAILABLE

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        data = await request.json()
        chat_request = ChatCompletionRequest(**data)

        # Determine task if not provided
        if not chat_request.task:
            task = DEFAULT_TASK_CLASSIFICATION.get(chat_request.messages[-1]["content"].lower(), "general")
        else:
            task = chat_request.task.lower()

        # Route model based on task
        model = MODEL_ROUTING.get(task, "qwen2.5:3b")

        # Prepare request to Ollama
        ollama_request = {
            "model": model,
            "messages": chat_request.messages,
            "stream": False
        }

        # Log the selected model and downstream URL
        logger.info(f"Selected model: {model}")
        logger.info(f"Downstream URL: {OLLAMA_BASE_URL}/api/chat")

        # Call Ollama
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=ollama_request, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

        # Add X-Selected-Model header
        response.headers["X-Selected-Model"] = model

        # Return OpenAI-compatible response
        return response.json()
    except (httpx.RequestError, ValueError, KeyError) as e:
        # Include the downstream Ollama response body in errors
        if response:
            error_message = f"Error: {e}, Ollama Response: {response.text}"
        else:
            error_message = f"Error: {e}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
