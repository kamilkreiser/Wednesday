#!/bin/bash
# poll_ready_gate15.sh — bounded poller: every 120 s run inbox_digest.sh --all (does NOT mark seen),
# log the whole listing, count "READY FOR QA (Seat B 15th): PR N" subjects (N may be 10). Stops at ten
# distinct PR numbers or after 60 minutes. Writes only under the gateset dir. Never marks seen, never sends.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments
DIG=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh
LOG="$G/poll_ready_gate15.log"
START=$(date +%s)
DEADLINE=$((START + 60*60))
i=0
while :; do
  i=$((i+1))
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  out="$G/inbox_all_poll${i}.out"
  bash "$DIG" --all > "$out" 2>&1
  prs=$(grep -oE 'READY FOR QA \(Seat B 15th\): PR [0-9]+' "$out" | grep -oE 'PR [0-9]+' | sort -u | tr '\n' ' ')
  n=$(grep -oE 'READY FOR QA \(Seat B 15th\): PR [0-9]+' "$out" | grep -oE 'PR [0-9]+' | sort -u | wc -l | tr -d ' ')
  echo "$now poll=$i distinct_seatB15_READY=$n [$prs] file=$(basename "$out")" | tee -a "$LOG"
  if [ "$n" -ge 10 ]; then echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ALL TEN in listing — stop" | tee -a "$LOG"; exit 0; fi
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) DEADLINE 60 min reached with $n — stop" | tee -a "$LOG"; exit 2; fi
  sleep 120
done
