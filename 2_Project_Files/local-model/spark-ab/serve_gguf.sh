#!/bin/bash
# spark-ab/serve_gguf.sh — runs ON the Spark (copied to /home/datasec-rd/deepseek-v4-flash-gguf/). 2026-10-26, BRIEF_QUANT.md.
# Serves an unsloth/DeepSeek-V4-Flash-0731-GGUF quant (rev fbbb5b93) with the OFFICIAL llama.cpp server image
# ghcr.io/ggml-org/llama.cpp:server-cuda13 (arm64, CUDA 13, built 2026-10-25, digest pinned below; arch deepseek4,
# sm_121a cubins) on 127.0.0.1:8888 — the port the laptop tunnel (spark/tunnel.sh, 47788) reaches — while the DeepSeek
# container is STOPPED. One slot (-np 1, as DeepSeek's MAX_NUM_SEQS=1). No restart policy: a failed boot stays down.
# Usage: serve_gguf.sh start UD-IQ2_XXS|UD-IQ1_M | stop UD-IQ2_XXS|UD-IQ1_M | status. `stop` STOPS (never rm). No cd.
set -uo pipefail
B=/home/datasec-rd/deepseek-v4-flash-gguf
IMG=ghcr.io/ggml-org/llama.cpp@sha256:2ac42bff86574137dd69b1c8ad85330729d8292e1b4fac0639b67a722c4e9558
Q="${2:-}"
NAME="dsv4-gguf-$(echo "$Q" | tr 'A-Z_' 'a-z-')"
case "${1:-}" in
  start)
    [ -n "$Q" ] && [ -d "$B/$Q" ] || { echo "no quant dir $B/$Q" >&2; exit 64; }
    if docker inspect "$NAME" >/dev/null 2>&1; then
      echo "container $NAME exists — starting it as it is"; docker start "$NAME"; exit $?
    fi
    docker run -d --name "$NAME" --gpus all --network host --ipc host \
      -v "$B/$Q:/model:ro" "$IMG" \
      -m "/model/DeepSeek-V4-Flash-0731-$Q-00001-of-00003.gguf" --alias "DeepSeek-V4-Flash-0731-$Q" \
      --host 127.0.0.1 --port 8888 -c 131072 -np 1 -ngl 999 --jinja -lm none --no-warmup -t 20
    ;;
  stop)   docker stop -t 60 "$NAME" ;;
  status) docker ps -a --filter "name=dsv4-gguf" --format '{{.Names}} {{.Status}}'; curl -s -m 5 -o /dev/null -w 'health %{http_code}\n' http://127.0.0.1:8888/health ;;
  *) echo "usage: serve_gguf.sh start|stop <quant> | status" >&2; exit 64 ;;
esac
