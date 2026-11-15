#!/usr/bin/env bash
LOG=~/spark-eval/ornith_chain.log
echo "=== waiting for pull $(date -Is) ===" >> "$LOG"
# wait until ollama reports the model present
until ~/.local/bin/ollama list 2>/dev/null | grep -q '^ornith:35b'; do sleep 30; done
echo "=== pull complete $(date -Is) ===" >> "$LOG"
~/.local/bin/ollama list >> "$LOG" 2>&1

echo "=== smoke test (loads model onto GPU) ===" >> "$LOG"
curl -s -m 900 http://127.0.0.1:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"ornith:35b","messages":[{"role":"user","content":"Reply with exactly: ORNITH_OK"}],"max_tokens":32,"temperature":0}' >> "$LOG" 2>&1
echo "" >> "$LOG"
free -g | awk 'NR==2{print "mem after load: "$3"G/"$2"G"}' >> "$LOG"
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader >> "$LOG" 2>&1

echo "=== running the 10-task suite $(date -Is) ===" >> "$LOG"
cd ~/spark-eval && PROVIDER=ollama OLLAMA_MODEL=ornith:35b python3 -u runner.py >> "$LOG" 2>&1
echo "=== done rc=$? $(date -Is) ===" >> "$LOG"
