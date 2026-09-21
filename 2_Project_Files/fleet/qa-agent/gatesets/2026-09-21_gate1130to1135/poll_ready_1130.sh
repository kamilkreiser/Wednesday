#!/bin/bash
# poll_ready_1130.sh — bounded poller: every 180 s run inbox_digest.sh --all (does NOT mark seen),
# log the whole listing, count "READY FOR QA (Seat B 14th): PR N" subjects. Stops at six distinct PR
# numbers or after 40 minutes. Writes only under the gateset dir. Never marks seen, never sends.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135
DIG=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh
LOG="$G/poll_ready_1130.log"
START=$(date +%s)
DEADLINE=$((START + 40*60))
i=0
while :; do
  i=$((i+1))
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  out="$G/inbox_all_poll${i}.out"
  bash "$DIG" --all > "$out" 2>&1
  prs=$(grep -o 'READY FOR QA (Seat B 14th): PR [0-9]' "$out" | grep -o 'PR [0-9]' | sort -u | tr '\n' ' ')
  n=$(grep -o 'READY FOR QA (Seat B 14th): PR [0-9]' "$out" | grep -o 'PR [0-9]' | sort -u | wc -l | tr -d ' ')
  echo "$now poll=$i distinct_seatB14_READY=$n [$prs] file=$(basename "$out")" | tee -a "$LOG"
  if [ "$n" -ge 6 ]; then echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ALL SIX captured in listing — stop" | tee -a "$LOG"; exit 0; fi
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) DEADLINE 40 min reached with $n — stop" | tee -a "$LOG"; exit 2; fi
  sleep 180
done
