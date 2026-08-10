#!/bin/bash
# ingest.sh — pull NEW items into Wednesday's unified attention queue.
# Kam's ruling 2026-08-10: ONE local queue mixing all clients (local
# structures are exempt from client walls). Wednesday's and Kam's ONLY —
# no project agent ever reads it.
#
# Sources: AgentMail (wednesday-agent@ + coagent@, inbound only),
#          dashboard chat (role=kam), Linear WED issues.
# Queue:   0_Brain/attention/queue.json (summary + pointer, never bodies)
# State:   state/ (gitignored — cursors only)
#
# bash 3.2-safe. Keys sourced from 4_Credentials/.env, never echoed.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

ENV_FILE="$PROJECT_DIR/4_Credentials/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: $ENV_FILE not found — cannot ingest mail/linear" >&2
  exit 1
fi
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

exec python3 "$SCRIPT_DIR/ingest.py"
