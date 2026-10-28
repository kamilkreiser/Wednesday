#!/bin/bash
# keepdraining.sh - re-runs spark/queue.sh whenever queue.md has an entry, so a brief appended after the drainer had already
# exited (queue.sh exits when the queue is empty) is picked up within ~20 s. It never edits queue.md.
# Stop it: create spark/state/keepdraining.stop, or kill the PID in spark/state/keepdraining.pid.
# A stale stop file makes it exit at once: move the file to a _quarantine dir first. One drainer at a time is still
# enforced by queue.sh's own lock.
S="$(cd "$(dirname "$0")/.." && pwd)"
echo $$ > "$S/state/keepdraining.pid"
while [ ! -f "$S/state/keepdraining.stop" ]; do
  if grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$S/queue.md" | grep -q .; then
    bash "$S/queue.sh" >> "$S/state/queue.log" 2>&1
  fi
  sleep 20
done
