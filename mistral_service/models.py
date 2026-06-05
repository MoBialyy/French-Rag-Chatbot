# mistral_service/models.py

from typing import List, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(..., description="One of: user, assistant, system")
    content: str


class ContextChunk(BaseModel):
    chunk_id: str
    text: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(
        ...,
        description="Full conversation history. Do NOT include the system message — "
                    "the service builds it automatically."
    )
    context_chunks: List[ContextChunk] = Field(
        default=[],
        description="RAG chunks to inject into the system prompt. "
                    "Pass empty list when no relevant context was found."
    )


class ChatResponse(BaseModel):
    """Used only when streaming is disabled. We use streaming by default."""
    response: str
