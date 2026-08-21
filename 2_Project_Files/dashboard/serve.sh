#!/bin/bash
# serve.sh — Wednesday dashboard: collect + generate every 5 min,
# serve site/ on 127.0.0.1:$PORT (LAN-only NEVER exposed; remote = Phase 4/Tailscale).
#
# PORT POLICY (Kam, 2026-08-05): never common dev/Docker ports (Secuura and
# Datasec stacks use those by default). Wednesday's block is 47780-47789 —
# registry in ../PORTS.md. Dashboard default = 47787.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${WEDNESDAY_DASHBOARD_PORT:-47787}"
export WEDNESDAY_DASHBOARD_PORT="$PORT"
cd "$DIR"

# Double-start guard: if OUR dashboard already answers, nothing to do.
if curl -s -m 2 "http://127.0.0.1:$PORT/api/health" 2>/dev/null | grep -q wednesday-dashboard; then
  echo "dashboard already running: http://127.0.0.1:$PORT"
  exit 0
fi
# Foreign-process guard: never bind-fight, never kill (PORTS.md rule 4).
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERROR: 127.0.0.1:$PORT is held by a FOREIGN process — not starting." >&2
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >&2
  exit 2
fi

( while true; do
    python3 collect.py >/dev/null 2>&1
    python3 generate.py >/dev/null 2>&1
    sleep 300
  done ) &
LOOP_PID=$!
echo "dashboard: http://127.0.0.1:$PORT (refresh loop pid $LOOP_PID)"
# Supervisor pattern (WED-113 round 2 hygiene): the old `exec python3` replaced
# this shell and DESTROYED the trap, so killing the server orphaned the
# collect/generate loop. Now the shell stays as supervisor: however this ends
# (server killed directly, or this script signalled), BOTH sides die together.
python3 "$DIR/server.py" &
SRV_PID=$!
trap 'kill $LOOP_PID $SRV_PID 2>/dev/null' EXIT INT TERM
wait $SRV_PID
