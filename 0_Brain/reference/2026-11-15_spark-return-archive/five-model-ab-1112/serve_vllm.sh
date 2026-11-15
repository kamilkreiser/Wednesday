#!/bin/bash
# serve_vllm.sh <container-name> <weights dir> <served-name> [extra vllm args...] — 2026-11-12 five-model A/B (replacement operator).
# One model at a time, 127.0.0.1:8888 (the port the Mac tunnel reaches), weights mounted read-only, MAX_NUM_SEQS 1.
# Never removes anything; containers are stopped (not rm) after use.
set -uo pipefail
NAME=$1; DIR=$2; SERVED=$3; shift 3
IMG=${VLLM_IMAGE:-vllm/vllm-openai:v0.33.0}
date -u +"%FT%TZ run $NAME image=$IMG dir=$DIR served=$SERVED args=$*" >> /home/datasec-rd/five-model-ab-1112/swap_times.txt
docker run -d --name "$NAME" --gpus all --network host --ipc host --entrypoint vllm \
  -v "$DIR":/models:ro "$IMG" \
  serve /models --served-model-name "$SERVED" --host 127.0.0.1 --port 8888 \
  --max-num-seqs 1 --max-model-len 131072 "$@"
