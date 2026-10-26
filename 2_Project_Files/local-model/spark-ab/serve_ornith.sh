#!/bin/bash
# spark-ab/serve_ornith.sh — runs ON the Spark (copied to /home/datasec-rd/ornith-1.5-122b-nvfp4/). 2026-10-26.
# Serves ornith-ai/Ornith-1.5-122B-NVFP4 (rev f049036f7946) with NVIDIA's vLLM 26.09 container (vLLM 0.29.0, arm64,
# sm_121) on 127.0.0.1:8888 — the port the laptop tunnel (spark/tunnel.sh, 47788) already reaches — while the DeepSeek
# container is STOPPED. One request at a time (max-num-seqs 1, as DeepSeek). No restart policy: a failed boot stays down.
# Usage: serve_ornith.sh start | stop | status. `stop` STOPS the container (never rm). No cd.
set -uo pipefail
D=/home/datasec-rd/ornith-1.5-122b-nvfp4
NAME=ornith-122b-nvfp4
IMG=nvcr.io/nvidia/vllm:26.09-py3
case "${1:-}" in
  start)
    if docker inspect "$NAME" >/dev/null 2>&1; then
      echo "container $NAME exists — starting it as it is"; docker start "$NAME"; exit $?
    fi
    docker run -d --name "$NAME" --gpus all --network host --ipc host --shm-size 16g \
      -v "$D/weights:/model:ro" "$IMG" \
      vllm serve /model --served-model-name Ornith-1.5-122B-NVFP4 --host 127.0.0.1 --port 8888 \
        --max-model-len 131072 --max-num-seqs 1 --gpu-memory-utilization 0.85 \
        --enable-prefix-caching --reasoning-parser qwen3 \
        --limit-mm-per-prompt '{"image":0,"video":0}'
    ;;
  stop)   docker stop -t 60 "$NAME" ;;
  status) docker ps -a --filter "name=$NAME" --format '{{.Names}} {{.Status}}'; curl -s -m 5 -o /dev/null -w 'health %{http_code}\n' http://127.0.0.1:8888/health ;;
  *) echo "usage: serve_ornith.sh start|stop|status" >&2; exit 64 ;;
esac
