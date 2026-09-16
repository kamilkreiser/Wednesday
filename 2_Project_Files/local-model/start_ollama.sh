#!/bin/bash
# Start the DRIVE-LOCAL ollama server for the night runner.
#
# Why this file exists (2026-09-16 13:3x): the server died some time before
# 12:24 and night_run's G5 gate refused SIX consecutive cycles (12:24 -> 13:24)
# into a log nobody reads — Ornith sat idle 09:58 -> 13:3x on a day Kam had
# twice said never to idle. A refusal nobody reads is indistinguishable from
# working (learnings/2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working.md),
# and the recovery had lived only as prose in README.md line 153.
#
# The two things a hand-start gets wrong, both proven wrong once:
#   1. the Homebrew binary (/opt/homebrew/bin/ollama) is too old for ornith:35b;
#      the drive-local v0.34 build at tools/ollama/ollama is the one.
#   2. without OLLAMA_MODELS the server reads ~/.ollama and ornith:35b is ABSENT
#      — /api/tags answers 200 and G5 still refuses.
#
# Usage: bash 2_Project_Files/local-model/start_ollama.sh [--check]
#   --check  report only (rc 0 serving ornith:35b, rc 1 not)

set -u
LM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$LM_DIR/../tools/ollama/ollama"
# 2026-09-16 14:1x — ONE store, at the drive root (Kam 13:40: "Create a new folder at root for system
# files and put things there"; 14:11: "As ollama is running programmatically, can you deal with this?
# Quit it and restart it."). A server serves exactly ONE models dir, and after his 141 GB moved to
# DevMASTER there were two on the drive: his and the fleet's. Serving either one alone leaves the
# other's models invisible, so the fleet's ornith + gpt-oss were copied INTO the system store
# (additive; the fleet copy is still on disk and is the fallback below).
# The cost, recorded rather than discovered: the fleet's weights now live OUTSIDE the WEDNESDAY
# folder, so that folder is no longer self-contained on another machine — PORTABILITY item.
OLLAMA_STORE_DEFAULT="/Volumes/DevMASTER/SYSTEM/ollama/models"
[ -d "$OLLAMA_STORE_DEFAULT/manifests" ] || OLLAMA_STORE_DEFAULT="$LM_DIR/models"   # fallback: the in-tree copy
export OLLAMA_MODELS="${OLLAMA_STORE_OVERRIDE:-$OLLAMA_STORE_DEFAULT}"
URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
LOG="$LM_DIR/logs/ollama_serve.log"
WANT="${NIGHT_MODEL:-ornith:35b}"

serving() { curl -sS -m 10 "$URL/api/tags" 2>/dev/null | /usr/bin/grep -q "\"$WANT\""; }

if serving; then
  echo "OK — $URL already serves $WANT"
  exit 0
fi
if [ "${1:-}" = "--check" ]; then
  echo "NOT SERVING — $URL does not list $WANT (models dir: $OLLAMA_MODELS)"
  exit 1
fi

[ -x "$BIN" ] || { echo "REFUSED — drive-local ollama binary not executable at $BIN" >&2; exit 2; }
[ -d "$OLLAMA_MODELS/manifests" ] || { echo "REFUSED — no manifests under $OLLAMA_MODELS" >&2; exit 2; }

# A server may be up on the WRONG models dir (the 13:29 mistake): if /api/tags
# answers but does not list the model, that process owns the port and must go.
if curl -sS -m 5 "$URL/api/tags" >/dev/null 2>&1; then
  echo "A server answers $URL but does not list $WANT — it is on the wrong models dir." >&2
  echo "Stop it by PORT (never by a parent walk), then re-run:" >&2
  echo "  lsof -nP -iTCP:11434 -sTCP:LISTEN -t" >&2
  exit 3
fi

mkdir -p "$LM_DIR/logs"
nohup "$BIN" serve >> "$LOG" 2>&1 &
sleep 5
for _ in 1 2 3 4 5 6; do
  if serving; then echo "STARTED — $URL now serves $WANT (log: $LOG)"; exit 0; fi
  sleep 3
done
echo "FAILED — server did not come up serving $WANT within ~23s; tail of $LOG:" >&2
tail -20 "$LOG" >&2
exit 4
