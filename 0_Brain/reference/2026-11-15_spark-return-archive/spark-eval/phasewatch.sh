#!/usr/bin/env bash
SNAP=~/DeepSeek-v4-Flash-One-DGX-Spark/hf-hub/hub/models--0xSero--deepseek-v4-flash-0731-spark/snapshots/22f28d32b9b29b4352eaa380ff8c2c170b2847ab
LOG=~/spark-eval/phase.log
DL_DONE=0
for i in $(seq 1 240); do   # up to 2h at 30s
  N=$(find "$SNAP" -type f -not -path '*/.cache/*' 2>/dev/null | wc -l)
  M=$(free -g | awk 'NR==2{print $3}')
  D=$(du -sm ~/DeepSeek-v4-Flash-One-DGX-Spark/data 2>/dev/null | cut -f1)
  H=$(curl -sf -m 3 http://127.0.0.1:8888/health >/dev/null 2>&1 && echo UP || echo -)
  echo "$(date -Is) files=$N/190 mem=${M}G data=${D}MB health=$H" >> "$LOG"
  if [ "$N" -ge 190 ] && [ "$DL_DONE" -eq 0 ]; then
    DL_DONE=1; echo "=== DOWNLOAD COMPLETE $(date -Is) -> load phase should begin ===" >> "$LOG"
  fi
  [ "$H" = "UP" ] && { echo "=== HEALTH UP $(date -Is) ===" >> "$LOG"; break; }
  sleep 30
done
