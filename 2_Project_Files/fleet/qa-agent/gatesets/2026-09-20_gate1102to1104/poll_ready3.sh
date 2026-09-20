#!/bin/bash
# poll_ready3.sh — poll wednesday-agent@ every 60 s for up to 20 min for "READY FOR QA (Seat B 10th): PR 3"; on arrival re-run the capture. Read-only on the inbox.
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1102to1104
for i in $(seq 1 20); do
  ( set -a; . /Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env; set +a; python3 "$G/list_ready_mail.py" ) > "$G/poll_ready3.last" 2>&1
  if /usr/bin/grep -q 'READY FOR QA (Seat B 10th): PR 3' "$G/poll_ready3.last"; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ARRIVED on poll $i"; /usr/bin/grep 'PR 3' "$G/poll_ready3.last"
    python3 "$G/capture_ready_mail.py" >> "$G/capture_ready_mail.out" 2>&1; echo "capture rc=$?"
    exit 0
  fi
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) poll $i: not yet"
  sleep 60
done
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) TIMEOUT after 20 polls"; exit 3
