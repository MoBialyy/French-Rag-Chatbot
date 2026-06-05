# clients/mistral_client.py
"""
HTTP client for the Mistral microservice (localhost:8001).

Handles streaming responses — yields tokens one by one so Streamlit
can update the UI in real time as the model generates.
"""

import requests
from typing import Generator
from config import RELEVANCE_THRESHOLD
MISTRAL_BASE_URL = "http://localhost:8001"




# ── Chat ───────────────────────────────────────────────────────────────────

def chat_stream(
    messages: list,
    context_chunks: list = [],
) -> Generator[str, None, None]:
    """
    Stream a response from the Mistral service.

    messages: list of { role, content } dicts (full conversation history)
    context_chunks: list of chunk dicts from rag_client.retrieve()
                    — filtered by RELEVANCE_THRESHOLD before injection

    Yields string tokens as they arrive. Use in Streamlit like:
        for token in chat_stream(messages, chunks):
            accumulated += token
            placeholder.markdown(accumulated)
    """
    # Filter chunks by relevance score before injecting
    filtered_chunks = [
        {"chunk_id": c["chunk_id"], "text": c["text"]}
        for c in context_chunks
        if (c.get("rerank_score") or c.get("fused_score") or 0) >= RELEVANCE_THRESHOLD
    ]

    payload = {
        "messages":       messages,
        "context_chunks": filtered_chunks,
    }

    with requests.post(
        f"{MISTRAL_BASE_URL}/chat",
        json=payload,
        stream=True,
        timeout=120,
    ) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


def translate_to_english(text: str) -> str:
    """Translate text to English before RAG retrieval."""
    try:
        response = requests.post(
            f"{MISTRAL_BASE_URL}/translate",
            json={"text": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("translation", text)
    except Exception:
        return text  # fallback to original if translation fails
