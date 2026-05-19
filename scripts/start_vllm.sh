#!/usr/bin/env bash
set -e

cd ~/CAREER/local_rag_llm

source ~/miniconda3/etc/profile.d/conda.sh
conda activate rag_llm

export VLLM_USE_FLASHINFER_SAMPLER=0
export CUDA_VISIBLE_DEVICES=0

vllm serve Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key token \
  --dtype auto \
  --max-model-len 8192
