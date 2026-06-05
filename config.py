# config.py
"""
App-level configuration.
All tunable values live here — nothing is hardcoded in pages or clients.
"""

import os

# ── API endpoints ──────────────────────────────────────────────────────────
RAG_API_URL     = "http://localhost:8000"
MISTRAL_API_URL = "http://localhost:8001"

# ── File uploads ───────────────────────────────────────────────────────────
# Uploaded PDFs are saved here before being passed to the RAG API.
# The RAG service reads from this path, so it must be on the same machine.
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# ── RAG settings ───────────────────────────────────────────────────────────
RETRIEVAL_TOP_K      = 2
RELEVANCE_THRESHOLD  = 0.3   # chunks below this score are not injected into prompt
