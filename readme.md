# Local RAG LLM

A self-hosted Retrieval-Augmented Generation application for querying a local
Markdown knowledge base. The project runs Qdrant for vector search, vLLM for an
OpenAI-compatible local LLM endpoint, SentenceTransformers for embeddings, and
FastAPI for both the API and the browser UI.

The current dataset focuses on database systems, including embedded databases,
OLTP engines, OLAP engines, distributed SQL systems, time-series databases,
search engines, graph databases, and vector databases.

## Highlights

- Docker Compose deployment for Qdrant, vLLM, document ingestion, and FastAPI.
- Chat-style web UI at `/` with adjustable `top_k` retrieval.
- Intent routing avoids vector search for off-topic or direct-chat questions.
- Source references are shown when retrieval is used.
- Conversation history is sent to the backend and older turns are compacted into
  a reusable summary.
- Runtime configuration is environment-driven through `.env`.
- Supports Hugging Face cache volumes, local model directories, mirrors, and
  host-side HTTP proxy settings for restricted networks.

## Architecture

```text
Browser UI
   |
FastAPI /rag
   |
IntentRouter
   |-- keyword rules
   |-- embedding similarity
   |-- vLLM zero-shot fallback for ambiguous cases
   |
RAGPipeline or Direct Chat
   |-- optional SentenceTransformers -> Qdrant vector search
   |-- vLLM OpenAI-compatible /v1/chat/completions
   |
Answer + retrieved references + compacted conversation memory
```

Main modules:

- `app/main.py`: FastAPI routes, health check, and static UI serving.
- `app/static/index.html`: browser chat interface.
- `app/intent_router.py`: keyword, embedding, and LLM fallback routing.
- `app/rag.py`: retrieval, prompt construction, and history compaction.
- `app/vector_store.py`: Markdown chunking, embeddings, Qdrant collection
  management, and search.
- `app/llm_client.py`: local OpenAI-compatible LLM client.
- `scripts/`: manual service, ingest, and retrieval smoke-test commands.
- `data/docs/`: Markdown documents ingested into Qdrant.

## Repository Contents

This repository is intended to be pushed without local runtime state. The
committed project should include:

- Source code under `app/`, `scripts/`, and `docker/`.
- Deployment files: `Dockerfile`, `compose.yaml`, `.env.example`, and
  dependency files.
- Markdown corpus files under `data/docs/`.
- Contributor/project docs such as `readme.md` and `AGENTS.md`.

The repository should not include `.env`, model weights, Hugging Face caches,
Qdrant storage, logs, virtual environments, or local editor files. These are
covered by `.gitignore`.

## Quick Start With Docker Compose

Prerequisites:

- Docker with Compose v2.
- NVIDIA Container Toolkit for the default GPU-backed vLLM service.
- Enough GPU memory for the selected local model.

Create local settings:

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker compose up --build
```

Open the app:

```text
http://localhost:8080
```

Use a different host port:

```bash
APP_PORT=9000 docker compose up --build
```

Then open `http://localhost:9000`.

Stop services:

```bash
docker compose down
```

Reset persisted Qdrant data and Hugging Face cache volumes:

```bash
docker compose down -v
```

## Startup Behavior

`compose.yaml` starts three services:

- `qdrant`: stores vectors in the `qdrant_storage` Docker volume.
- `vllm`: serves `VLLM_MODEL` on `http://vllm:8000/v1`.
- `api`: waits for Qdrant, optionally ingests `data/docs/*.md`, optionally waits
  for vLLM readiness, then starts FastAPI on container port `8080`.

Important startup flags:

```bash
INGEST_ON_STARTUP=1      # ingest docs before API starts
RECREATE_COLLECTION=1    # rebuild the collection during startup
WAIT_FOR_LLM=1           # wait for vLLM before serving API traffic
APP_PORT=8080            # host port mapped to FastAPI/UI
```

For fast restarts after the image has already been built:

```bash
docker compose up -d
```

## Configuration

Common settings from `.env.example`:

```bash
VLLM_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_API_KEY=token
VLLM_MAX_MODEL_LEN=32768
VLLM_GPU_MEMORY_UTILIZATION=0.92
LLM_TEMPERATURE=0.2
LLM_TOP_P=0.9
LLM_MAX_TOKENS=2048

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
QDRANT_COLLECTION=tech_docs
RETRIEVE_TOP_K=4
CHUNK_SIZE=800
CHUNK_OVERLAP=120

HISTORY_RECENT_TURNS=6
HISTORY_MAX_MESSAGES=80
MESSAGE_MAX_CHARS=4000
CONVERSATION_SUMMARY_MAX_CHARS=2200
SUMMARY_HISTORY_MAX_CHARS=9000
SUMMARY_MAX_TOKENS=700
SEARCH_QUERY_MAX_CHARS=1800

INTENT_ROUTER_ENABLED=1
INTENT_LLM_FALLBACK=1
INTENT_LLM_HISTORY_MAX_CHARS=1800
INTENT_LLM_SUMMARY_MAX_CHARS=1200
INTENT_LLM_MAX_TOKENS=80
INTENT_EMBEDDING_HISTORY_MAX_CHARS=2600
INTENT_EMBEDDING_SUMMARY_MAX_CHARS=1000
INTENT_EMBEDDING_TEXT_MAX_CHARS=3600
INTENT_EMBEDDING_DB_THRESHOLD=0.38
INTENT_EMBEDDING_DIRECT_THRESHOLD=0.40
INTENT_EMBEDDING_MARGIN=0.06
```

The default vLLM settings are tuned for a local 7B model on a high-memory GPU.
If vLLM reports out-of-memory errors, reduce `VLLM_MAX_MODEL_LEN`,
`VLLM_GPU_MEMORY_UTILIZATION`, or `LLM_MAX_TOKENS`.

## Restricted Network Setup

Docker daemon proxy settings only help image pulls. Runtime containers need
their own proxy or mirror settings in `.env`.

For a Hugging Face mirror:

```bash
HF_ENDPOINT=https://hf-mirror.com
```

For host-side Mihomo, enable Allow LAN / bind to `0.0.0.0`, then set:

```bash
DOCKER_HTTP_PROXY=http://host.docker.internal:7890
DOCKER_HTTPS_PROXY=http://host.docker.internal:7890
DOCKER_NO_PROXY=qdrant,vllm,api,localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

Do not use `127.0.0.1` for the proxy host inside containers; it points to the
container itself.

## Offline Models

You can mount local model directories through `./models:/models:ro`:

```text
models/
  bge-small-en-v1.5/
  qwen2.5-7b-instruct/
```

Then configure:

```bash
EMBEDDING_MODEL=/models/bge-small-en-v1.5
VLLM_MODEL=/models/qwen2.5-7b-instruct
LLM_MODEL=qwen2.5-7b-instruct
```

## API Usage

Health check:

```bash
curl http://localhost:8080/health
```

RAG request:

```bash
curl http://localhost:8080/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When should I choose DuckDB over ClickHouse?",
    "top_k": 4,
    "history": [
      {"role": "user", "content": "Compare embedded OLAP options."},
      {"role": "assistant", "content": "DuckDB is embedded; ClickHouse is server-oriented."}
    ],
    "conversation_summary": ""
  }'
```

Response fields:

- `answer`: generated response.
- `contexts`: retrieved chunks with `source`, `chunk_id`, `score`,
  `content_type`, `headings`, line bounds, and `h1`/`h2`/`h3` metadata.
- `conversation_summary`: compact memory for future turns.
- `compacted_history_messages`: number of old messages merged into memory.
- `used_rag`: whether Qdrant retrieval was used for this answer.
- `route` and `route_reason`: intent-router decision metadata.

## Manual Development

Set up Python dependencies:

```bash
conda activate rag_llm
pip install -r requirements.txt
```

For API-only development with Docker-managed vLLM/Qdrant, the smaller runtime
dependency set is:

```bash
pip install -r requirements.api.txt
```

Start local services manually:

```bash
bash scripts/start_qdrant.sh
bash scripts/start_vllm.sh
```

Ingest Markdown:

```bash
python scripts/ingest_docs.py --recreate
```

Smoke-test retrieval:

```bash
python scripts/test_retrieve.py
```

Smoke-test Markdown chunking:

```bash
python scripts/test_chunking.py
```

Smoke-test intent routing:

```bash
python scripts/test_intent_router.py
```

Smoke-test prompt budgeting and history trimming:

```bash
python scripts/test_prompt_budget.py
```

Run FastAPI:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Run a quick syntax check before pushing:

```bash
python -m compileall app scripts
```

## Document Corpus

Markdown files in `data/docs/` are the RAG source of truth. Current files cover
PostgreSQL, MySQL/InnoDB, SQLite, DuckDB, RocksDB, LMDB, ClickHouse, Druid,
Pinot, Snowflake, BigQuery, MongoDB, Cassandra, ScyllaDB, Redis, Elasticsearch,
Neo4j, TimescaleDB, InfluxDB, Qdrant, Milvus, Weaviate, pgvector, Chroma, FAISS,
CockroachDB, YugabyteDB, TiDB, and a database selection guide.

Chunking is Markdown-aware and metadata-driven: Markdown blocks are parsed,
headings are stored as `h1`/`h2`/`h3` payload metadata, and text, code, and
tables are chunked separately. Heading context is included in embedding input
but kept separate from stored chunk text to avoid duplicating titles in every
chunk. Oversized text chunks use an effective chunk budget that leaves room for
overlap, while fenced code chunks preserve complete fences.

After adding or editing documents, or after changing chunking logic, rebuild the
collection:

```bash
python scripts/ingest_docs.py --recreate
```

or restart Compose with `RECREATE_COLLECTION=1`.

## Before Pushing to GitHub

Run these checks from the repository root:

```bash
git status --short --ignored
python -m compileall app scripts
python scripts/test_chunking.py
python scripts/test_intent_router.py
python scripts/test_prompt_budget.py
docker compose config
```

Expected ignored local paths may include `.env`, `.vscode/`, `qdrant_storage/`,
`models/`, and `__pycache__/`. Do not add those files. New source files such as
`app/intent_router.py`, `app/static/index.html`, data docs, and scripts should
be tracked.

## Git Hygiene

Do not commit `.env`, API keys, Hugging Face tokens, model weights, Qdrant
storage, cache directories, virtual environments, or logs. Runtime state such as
`qdrant_storage/`, `models/`, `.cache/`, local database files, and `.env` is
intentionally ignored.
