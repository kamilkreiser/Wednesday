#!/bin/bash
# serve_nemotron.sh — 2026-11-12 nemotron-local-ab operator. NVIDIA card "1x DGX Spark" vLLM Quick Start recipe, with the
# native MTP head (5 draft tokens, the card table row for 1x DGX Spark vLLM) in place of the LiLiCorr drafter, which is
# NOT downloaded. Port 8888 on 127.0.0.1 (the Mac tunnel), weights read-only, max-num-seqs 1. Never removes anything.
# Extra args after the first are appended (e.g. --max-model-len N).
set -uo pipefail
NAME=${1:-ab1112-nemotron}; shift || true
IMG=${VLLM_IMAGE:-vllm/vllm-openai:v0.33.0}
DIR=/home/datasec-rd/five-model-ab-1112/nemotron35-super-vl-nvfp4
date -u +"%FT%TZ run $NAME image=$IMG dir=$DIR served=nemotron-3.5-super-vl extra=$*" >> /home/datasec-rd/five-model-ab-1112/swap_times.txt
docker run -d --name "$NAME" --gpus all --network host --ipc host --entrypoint vllm \
  -v "$DIR":/models:ro "$IMG" \
  serve /models --served-model-name nemotron-3.5-super-vl --host 127.0.0.1 --port 8888 \
  --max-num-seqs 1 --trust-remote-code --gpu-memory-utilization 0.75 --max-num-batched-tokens 8192 \
  --speculative_config.method mtp --speculative_config.num_speculative_tokens 5 \
  --mamba-backend flashinfer --mamba-ssm-cache-dtype float16 --enable-mamba-cache-stochastic-rounding \
  --mamba-cache-philox-rounds 5 --enable-mamba-shared-prefix-checkpoint \
  --block-size 64 --prefix-match-unit 64 \
  --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser nemotron_v3 "$@"
