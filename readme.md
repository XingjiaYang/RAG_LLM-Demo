# Local RAG LLM

Local RAG MVP with Qdrant, SentenceTransformers, vLLM, and FastAPI.

## Components

- vLLM serves `Qwen/Qwen2.5-7B-Instruct` at `http://localhost:8000/v1`
- Qdrant stores document chunks at `http://localhost:6333`
- Markdown documents live in `data/docs/*.md`
- FastAPI exposes `POST /rag`

## Setup

Use the existing conda environment:

```bash
conda activate rag_llm
pip install -r requirements.txt
```

## Start Services

Start Qdrant:

```bash
bash scripts/start_qdrant.sh
```

Start vLLM in another terminal:

```bash
bash scripts/start_vllm.sh
```

The default API key is `token`. Override runtime settings with environment
variables such as `LLM_API_KEY`, `LLM_MODEL`, `QDRANT_URL`, and
`QDRANT_COLLECTION`.

## Ingest Documents

Put Markdown files in `data/docs/`, then run:

```bash
python scripts/ingest_docs.py
```

## Test Retrieval

```bash
python scripts/test_retrieve.py
```

## Start API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Test RAG:

```bash
curl http://localhost:8080/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is DuckDB good for?",
    "top_k": 3
  }'
```

Health check:

```bash
curl http://localhost:8080/health
```

## Git Hygiene

Do not commit runtime storage, model caches, API keys, or logs. The repository
ignores `qdrant_storage/`, cache folders, virtual environments, `.env`, and log
files.
