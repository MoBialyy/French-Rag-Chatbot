# run_all.py
"""
Starts all three services + Streamlit in separate terminal windows.

Run from the learnai/ folder:
    python run_all.py

Make sure to set RAG_PROJECT_PATH below to your cess-tutor-rag folder path.
"""

import subprocess
import sys
import os

# ── Config — set your RAG project path here ────────────────────────────────
# put the full path to your local cess-tutor-rag folder here, e.g.:
RAG_PROJECT_PATH = r"C:\Users\YourName\Documents\cess-tutor-rag"   
LEARNAI_PATH     = os.path.dirname(os.path.abspath(__file__))
# ───────────────────────────────────────────────────────────────────────────

def run_in_new_terminal(title: str, command: str, cwd: str):
    """Open a new cmd window with a title and run a command in it."""
    full_cmd = f'start "{title}" cmd /k "{command}"'
    subprocess.Popen(full_cmd, shell=True, cwd=cwd)


if __name__ == "__main__":
    print("Starting all services...\n")

    run_in_new_terminal(
        title   = "RAG API (port 8000)",
        command = "uvicorn service.main:app --host 0.0.0.0 --port 8000 --reload",
        cwd     = RAG_PROJECT_PATH,
    )

    run_in_new_terminal(
        title   = "Mistral Service (port 8001)",
        command = "uvicorn mistral_service.main:app --host 0.0.0.0 --port 8001 --reload",
        cwd     = LEARNAI_PATH,
    )

    run_in_new_terminal(
        title   = "Streamlit App",
        command = "streamlit run app.py",
        cwd     = LEARNAI_PATH,
    )

    print("All services launched in separate windows.")
    print("\nURLs:")
    print("  Streamlit  → http://localhost:8501")
    print("  RAG API    → http://localhost:8000/docs")
    print("  Mistral    → http://localhost:8001/docs")
    print("  Ollama     → http://localhost:11434")