# Paul le Tuteur

> An AI-powered university tutoring assistant — chat with your course PDFs and study lecture by lecture, in French.

Paul le Tuteur lets you upload university lecture slides and PDFs and interact with them through a local AI tutor. Ask questions about your course material and get structured RAG-based explanations — all in French, all on your own machine.

---

## Features

- **Course & Lecture Management** — organize your material by course, add lectures by uploading PDFs
- **RAG-Powered Chat** — ask questions about a specific lecture or an entire course; answers are grounded in your actual slides via semantic retrieval
- **French-first** — queries are translated to English internally for better retrieval, but Paul always responds in French
- **Fully local** — your PDFs and conversations never leave your machine

---

## Architecture

```
┌─────────────────────────────────────────┐
│          Streamlit Frontend             │
│  login / home / course / chat / study   │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌──────────────────────┐
│  RAG API      │  │  Mistral Service     │
│  :8000        │  │  :8001               │
│               │  │                      │
│  ChromaDB     │  │  Ollama (local LLM)  │
│  PDF ingestion│  │  fine-tuned Mistral  │
│  retrieval    │  │  streaming responses │
└───────────────┘  └──────────────────────┘
```

The app is composed of three services that all run locally:

| Service | Port | Description |
|---|---|---|
| Streamlit App | 8501 | The UI — all pages and navigation |
| RAG API | 8000 | PDF ingestion, ChromaDB, semantic retrieval |
| Mistral Service | 8001 | Ollama wrapper — builds prompts, streams responses |

---

## The Model — A Fine-Tuning Journey

A core challenge was finding a capable model under 10B parameters that could respond naturally in French for a university tutoring context.

After evaluating several options, I settled on **Mistral 7B Instruct v0.3** as the base — strong instruction-following, good multilingual capability, and small enough to run locally on consumer hardware.

**Fine-tuning was done using QLoRA via [Unsloth](https://github.com/unslothai/unsloth)** on a French instruction dataset:

```python
MODEL_ID   = "mistralai/Mistral-7B-Instruct-v0.3"
DATASET_ID = "vonewman/french-instruction-dataset"  # 10,000 samples
```

**LoRA configuration:**
- Rank `r = 16`, Alpha `= 32`, Dropout `= 0.05`
- Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- Training: 1 epoch, batch size 2, gradient accumulation 4, lr `2e-4`

The fine-tuning notebook is included in this repo: [`Mistral 7b FineTuning`](https://github.com/MoBialyy/Mistral-7B-Finetuning)

**Published models on Hugging Face:**

| Model | Link | Description |
|---|---|---|
| Full merged model | [Bialy17/mistral-7b-french-tutor](https://huggingface.co/Bialy17/mistral-7b-french-tutor) | Merged 16-bit weights |
| LoRA adapters only | [Bialy17/mistral-7b-french-tutor-lora](https://huggingface.co/Bialy17/mistral-7b-french-tutor-lora) | Adapter configs + weights |
| GGUF (for Ollama) | [Bialy17/mistral-7b-french-tutor-gguf](https://huggingface.co/Bialy17/mistral-7b-french-tutor-gguf) | Quantized for local inference |

---

## Prerequisites

Before running this app, you need to set up **two separate components**:

### 1. Ollama + the fine-tuned model

Install [Ollama](https://ollama.com) and pull the GGUF model:

```bash
ollama pull hf.co/Bialy17/mistral-7b-french-tutor-gguf
```

Verify it's running:
```bash
ollama list
```
Also, I was using my GPU (RTX 3050) to run the ollama model, try to use it as it will be very much better.

### 2. RAG Pipeline

Clone and set up the RAG API from its own repository:

```
https://github.com/MoBialyy/cess-tutor-rag
```

Follow the setup instructions in that repo. Once installed, note the full path to the folder — you'll need it in the next step.

---

## Configuration

Open `run_all.py` and set the path to your local RAG pipeline folder:

```python
RAG_PROJECT_PATH = r"C:\path\to\your\cess-tutor-rag"
```

---

## Running the App

Once all prerequisites are set up, open a terminal in this project folder and run:

```bash
python .\run_all.py
```

This will open **three separate terminal windows**:

- `RAG API` on `http://localhost:8000`
- `Mistral Service` on `http://localhost:8001`
- `Streamlit App` on `http://localhost:8501`

Open your browser at **http://localhost:8501** to use the app.

---

## Project Structure

```
paul-le-tuteur/
├── app.py                  # Entry point — page config, CSS, router
├── run_all.py              # Launches all three services
├── config.py               # App-level configuration (URLs, thresholds)
├── utils.py                # Shared helpers (nav, init_state, to_collection_name)
│
├── pages/
│   ├── login.py
│   ├── home.py
│   ├── new_course.py
│   ├── course.py
│   ├── add_lecture.py
│   ├── chat.py
│   └── study.py
│
├── clients/
│   ├── rag_client.py       # HTTP client for the RAG API
│   └── mistral_client.py   # HTTP client for the Mistral service
│
├── mistral_service/
    ├── main.py             # FastAPI app — prompt builder, Ollama proxy
    ├── models.py           # Pydantic request/response models
    └── config.py           # System prompt, model name, Ollama URL
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Mistral 7B (fine-tuned), served via Ollama |
| Fine-tuning | Unsloth + QLoRA + TRL |
| RAG | ChromaDB, semantic search + reranking |
| Services | FastAPI |
| HTTP | httpx (async), requests (sync) |

---

## 📄 License

MIT
