# clients/rag_client.py
"""
HTTP client for the RAG microservice (localhost:8000).

All RAG API calls go through here — pages never call requests directly.
"""

import requests
from typing import Optional

RAG_BASE_URL = "http://localhost:8000"


# ── Ingestion ──────────────────────────────────────────────────────────────

def ingest_lecture(
    file_path: str,
    collection: str,
    lecture_num: int,
    lecture_title: str,
    replace: bool = True,
) -> dict:
    """
    Queue a lecture PDF for ingestion into the RAG pipeline.
    Returns the job dict: { job_id, status, message }
    """
    payload = {
        "files":         [file_path],
        "collection":    collection,
        "lecture_num":   lecture_num,
        "lecture_title": lecture_title,
        "replace":       replace,
    }
    response = requests.post(f"{RAG_BASE_URL}/ingest", json=payload)
    response.raise_for_status()
    return response.json()


def get_job_status(job_id: str) -> dict:
    """
    Poll the status of an ingestion job.
    Returns: { job_id, status, message, summary }
    status is one of: queued, running, done, failed
    """
    response = requests.get(f"{RAG_BASE_URL}/ingest/{job_id}")
    response.raise_for_status()
    return response.json()


# ── Retrieval ──────────────────────────────────────────────────────────────

def retrieve(
    query: str,
    collection: str,
    top_k: int = 2,
    lecture_num: Optional[int] = None,
) -> list:
    """
    Semantic search over a collection.
    Pass lecture_num to restrict search to a specific lecture.
    Returns list of chunk dicts: { chunk_id, text, metadata, rerank_score, fused_score }
    """
    payload = {
        "query":      query,
        "collection": collection,
        "top_k":      top_k,
    }
    if lecture_num is not None:
        payload["lecture_num"] = lecture_num

    response = requests.post(f"{RAG_BASE_URL}/retrieve", json=payload)
    response.raise_for_status()
    results = response.json()["results"]
    
    # Sort by fused_score descending instead of rerank_score
    results.sort(key=lambda x: x.get("fused_score", 0), reverse=True)
    
    return results


# ── Sequential chunk reading ───────────────────────────────────────────────

def get_chunk(
    collection: str,
    lecture_num: int,
    chunk_index: int,
) -> dict:
    """
    Fetch a single chunk by index for the study mode (chunk-by-chunk reading).
    Returns: { collection, lecture_num, chunk_index, total_chunks,
               chunk_id, lecture_title, text, is_last }
    """
    payload = {
        "collection":  collection,
        "lecture_num": lecture_num,
        "chunk_index": chunk_index,
    }
    response = requests.post(f"{RAG_BASE_URL}/chunks", json=payload)
    response.raise_for_status()
    return response.json()
