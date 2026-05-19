#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

source ~/miniconda3/etc/profile.d/conda.sh
conda activate rag_llm

export VLLM_USE_FLASHINFER_SAMPLER=0
export CUDA_VISIBLE_DEVICES=0

MODEL_NAME="${LLM_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
API_KEY="${LLM_API_KEY:-token}"

vllm serve "${MODEL_NAME}" \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key "${API_KEY}" \
  --dtype auto \
  --max-model-len 8192
