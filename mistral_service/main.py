# mistral_service/main.py
"""
Mistral microservice — FastAPI wrapper around the local Ollama instance.

Responsibilities:
  - Build the system prompt (with or without RAG context chunks)
  - Forward the conversation to Ollama
  - Stream the response back to the caller

Run:
  uvicorn mistral_service.main:app --host 0.0.0.0 --port 8001 --reload

Docs:
  http://localhost:8001/docs
"""

import json
import httpx

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from .models import ChatRequest
from .config import (
    OLLAMA_BASE_URL,
    MODEL_NAME,
    SYSTEM_PROMPT,
    CONTEXT_PROMPT_TEMPLATE,
)


app = FastAPI(
    title="Mistral Service",
    description="Local Ollama wrapper — builds prompts, injects RAG context, streams responses.",
    version="0.1.0",
)


# ── Helpers ────────────────────────────────────────────────────────────────

def _build_system_prompt(context_chunks: list) -> str:
    """Return base system prompt, or augmented one if chunks are provided."""
    if not context_chunks:
        return SYSTEM_PROMPT

    chunks_text = "\n---\n".join(chunk.text for chunk in context_chunks)
    return CONTEXT_PROMPT_TEMPLATE.format(
        base=SYSTEM_PROMPT,
        chunks=chunks_text,
    )


def _build_messages(request: ChatRequest) -> list:
    """Prepend system prompt + a priming exchange, then the real conversation."""
    system_prompt = _build_system_prompt(request.context_chunks)
    
    priming = [
        {"role": "user",      "content": "salut"},
        {"role": "assistant", "content": "Salut ! Comment je peux t'aider ?"},
        {"role": "user",      "content": "bonjour"},
        {"role": "assistant", "content": "Bonjour ! Tu as des questions sur ton cours ?"},
    ]
    
    real_messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    return [
        {"role": "system", "content": system_prompt},
        *priming,
        *real_messages,
    ]


# ── Health ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


# ── Chat (streaming) ───────────────────────────────────────────────────────

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Stream a response from the local Ollama model.

    The caller receives server-sent text chunks as they are generated.
    Each chunk is a plain string token — no JSON wrapping — for easy
    consumption by the Streamlit frontend.
    """
    messages = _build_messages(request)

    ollama_payload = {
        "model":    MODEL_NAME,
        "messages": messages,
        "stream":   True,
        "options": {
            "temperature": 0.85,
            "num_predict": 1024,
        },
    }

    async def token_stream():
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json=ollama_payload,
                ) as response:
                    if response.status_code != 200:
                        error_body = await response.aread()
                        raise HTTPException(
                            status_code=502,
                            detail=f"Ollama returned {response.status_code}: {error_body.decode()}"
                        )
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            token = data.get("message", {}).get("content", "")
                            if token:
                                yield token
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
        except httpx.ConnectError:
            yield "\n[ERROR] Cannot connect to Ollama. Is it running on localhost:11434?]"
        except Exception as e:
            yield f"\n[ERROR] {str(e)}"

    return StreamingResponse(token_stream(), media_type="text/plain")


@app.post("/translate")
async def translate(request: dict):
    """Translate any text to English for RAG retrieval."""
    text = request.get("text", "")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a translator. Return only the English translation, nothing else."
            },
            {
                "role": "user",
                "content": f"Translate to English: {text}"
            }
        ],
        "stream": True,
        "options": {"temperature": 0.1, "num_predict": 200},
    }

    full_response = ""
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream(
            "POST",
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        ) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        full_response += token
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue

    return {"translation": full_response.strip()}