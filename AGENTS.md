# Repository Guidelines

## Project Structure & Module Organization

This repository is a local RAG MVP built with FastAPI, Qdrant, SentenceTransformers, and vLLM.

- `app/`: application code. `main.py` exposes the FastAPI app, `static/` contains the web UI, `rag.py` coordinates retrieval and generation, `vector_store.py` manages Qdrant, `llm_client.py` calls the OpenAI-compatible vLLM API, and `config.py` reads environment settings.
- `scripts/`: operational scripts for starting local services, ingesting Markdown, and testing retrieval.
- `data/docs/`: source Markdown documents used for ingestion.
- `docker/`, `Dockerfile`, `compose.yaml`: container entrypoint and Docker Compose deployment.
- `configs/`, `benchmark/`: supporting configuration and evaluation assets when present.
- Runtime state such as `qdrant_storage/`, `models/`, caches, logs, and `.env` must stay uncommitted.

## Build, Test, and Development Commands

- `cp .env.example .env`: create local deployment settings.
- `docker compose up --build`: build and start Qdrant, vLLM, document ingest, and FastAPI.
- `APP_PORT=9000 docker compose up --build`: run the frontend/API on a different host port.
- `docker compose down`: stop the stack.
- `conda activate rag_llm && pip install -r requirements.txt`: set up manual local development.
- `python scripts/ingest_docs.py --recreate`: rebuild the Qdrant collection from `data/docs/*.md`.
- `python scripts/test_retrieve.py`: smoke-test vector retrieval.
- `uvicorn app.main:app --host 0.0.0.0 --port 8080`: run the API manually.
- `python -m compileall app scripts`: quick syntax check before pushing.

## Coding Style & Naming Conventions

Use Python 3.12-compatible code, 4-space indentation, type hints for public helpers, and concise docstrings or comments only where behavior is not obvious. Keep module names lowercase with underscores. Prefer environment-driven configuration through `Settings` in `app/config.py` instead of hard-coded service URLs or model names.

## Testing Guidelines

There is no formal pytest suite yet. For now, validate changes with `python -m compileall app scripts`, `python scripts/test_retrieve.py`, `curl http://localhost:8080/health`, and a `POST /rag` request. Add future tests under `tests/` using `test_*.py` naming.

## Commit & Pull Request Guidelines

Git history currently uses short descriptive commits such as `Deploy Demo to Docker.` Keep commits focused and imperative, for example `Add Docker Compose deployment` or `Fix Qdrant ingest retry`.

PRs should include a short summary, commands run, configuration changes, and any deployment notes. Include screenshots only when the web UI changes.

## Security & Configuration Tips

Do not commit `.env`, API keys, Hugging Face tokens, model weights, Qdrant storage, or cache directories. For restricted networks, configure runtime proxy values in `.env`; Docker daemon proxy settings only affect image pulls, not running containers.
