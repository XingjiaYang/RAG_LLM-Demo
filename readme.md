# Local RAG LLM

Local RAG MVP with Qdrant, SentenceTransformers, vLLM, and FastAPI.

## Components

- vLLM serves `Qwen/Qwen2.5-7B-Instruct`
- Qdrant stores document chunks
- Markdown documents live in `data/docs/*.md`
- FastAPI exposes `POST /rag`
- Docker Compose can start Qdrant, vLLM, document ingest, and FastAPI with one
  command

## Docker Deployment

This is the recommended path when you do not want to start Qdrant, vLLM,
ingest, and FastAPI manually.

Prerequisites:

- Docker with Compose v2
- NVIDIA Container Toolkit if you run the default GPU vLLM service

Create an optional local env file:

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker compose up --build
```

Open the frontend:

```text
http://localhost:8080
```

Use a different host port:

```bash
APP_PORT=9000 docker compose up --build
```

Then open:

```text
http://localhost:9000
```

Startup behavior:

- `qdrant` persists vectors in the named Docker volume `qdrant_storage`
- `vllm` serves the configured `LLM_MODEL`
- `api` waits for Qdrant, ingests `data/docs/*.md`, waits for vLLM, then starts
  FastAPI
- `RECREATE_COLLECTION=1` rebuilds the Qdrant collection on startup so the
  collection matches the current Markdown files
- `WAIT_FOR_LLM=0` starts the frontend before vLLM finishes loading

Common settings are in `.env.example`:

```bash
APP_PORT=8080
VLLM_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_API_KEY=token
QDRANT_COLLECTION=tech_docs
INGEST_ON_STARTUP=1
RECREATE_COLLECTION=1
WAIT_FOR_LLM=1
```

If the containers cannot reach Hugging Face, set a mirror or proxy in `.env`:

```bash
HF_ENDPOINT=https://hf-mirror.com
```

or:

```bash
DOCKER_HTTP_PROXY=http://host.docker.internal:7890
DOCKER_HTTPS_PROXY=http://host.docker.internal:7890
DOCKER_NO_PROXY=qdrant,vllm,api,localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

For fully offline deployment, copy local model directories under `models/` and
point the services at those paths:

```text
models/
  bge-small-en-v1.5/
  qwen2.5-7b-instruct/
```

Then set:

```bash
EMBEDDING_MODEL=/models/bge-small-en-v1.5
VLLM_MODEL=/models/qwen2.5-7b-instruct
LLM_MODEL=qwen2.5-7b-instruct
```

Stop the stack:

```bash
docker compose down
```

Remove persisted Qdrant/model cache volumes when you want a clean rebuild:

```bash
docker compose down -v
```

## Local Setup

Use the existing conda environment:

```bash
conda activate rag_llm
pip install -r requirements.txt
```

## Manual Local Services

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

Rebuild the collection before ingesting:

```bash
python scripts/ingest_docs.py --recreate
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
