#!/usr/bin/env bash
set -e

cd ~/CAREER/local_rag_llm

docker run --rm \
  --name local-rag-qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant