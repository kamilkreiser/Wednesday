#!/usr/bin/env bash
# Wait for /health, then immediately run the probe suite and log it.
LOG=~/spark-eval/autorun.log
echo "=== watcher started $(date -Is) ===" >> "$LOG"
until curl -sf -m 5 http://127.0.0.1:8888/health >/dev/null 2>&1; do sleep 30; done
echo "=== /health UP at $(date -Is) ===" >> "$LOG"
sleep 20
python3 ~/spark-eval/probe.py >> "$LOG" 2>&1
echo "=== probe finished rc=$? at $(date -Is) ===" >> "$LOG"
