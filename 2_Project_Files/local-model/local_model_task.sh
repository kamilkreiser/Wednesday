#!/bin/bash
# local_model_task.sh — bounded single-shot task runner for the local-model
# harness (Kam, panel 2026-09-14 11:26: "download and implement Qwen 3 30b
# and use it within the workflow ... assign simple and manageable tasks to
# it"). This is the ONLY thing that talks to ollama for pilot tasks: it
# never calls Linear/GitHub, and the model holds no board identity — inputs
# are files a seat dumped, outputs are files a seat reads back.
#
# Usage: local_model_task.sh <task.md> <input.json> <out.md>
#
# Env:
#   LM_MODEL     ollama model tag (default qwen3:30b-a3b)
#   LM_NUM_CTX   context window to request (default 16384 — see README for
#                the measured model default of 262144)
#   LM_MAX_LOAD  refuse above this 1-min load (default 16, per the headroom
#                doc's "no local generation while a tier-1 gate runs suites
#                at load > ~16" rule)
#   LM_FORCE     1 = run anyway when the load rule would refuse
#   LM_THINK     1 (default) sends think:true — the clean content/thinking
#                split (README finding); 0 sends think:false and strips any
#                <think>…</think> from the answer — the Ornith runtime-cut
#                workaround (2026-09-14 head-to-head; night runner default)
#   OLLAMA_URL   default http://127.0.0.1:11434
#
# Exit codes: 0 ok, 2 usage/missing-input/ollama-unreachable, 3 load rule
# refused, 4 HTTP/JSON failure from the model call.
#
# bash 3.2 compatible (macOS ships 3.2: no `declare -A`, no `timeout` —
# the HTTP call's timeout is handled inside lib/lm_call.py). stderr is
# NEVER sent to /dev/null (ledger rule, this project).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LM_MODEL="${LM_MODEL:-qwen3:30b-a3b}"
LM_NUM_CTX="${LM_NUM_CTX:-16384}"
LM_MAX_LOAD="${LM_MAX_LOAD:-16}"
LM_FORCE="${LM_FORCE:-0}"
LM_THINK="${LM_THINK:-1}"
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"

TASK_FILE="${1:-}"
INPUT_FILE="${2:-}"
OUT_FILE="${3:-}"

if [ -z "$TASK_FILE" ] || [ -z "$INPUT_FILE" ] || [ -z "$OUT_FILE" ]; then
  echo "usage: local_model_task.sh <task.md> <input.json> <out.md>" >&2
  exit 2
fi
if [ ! -f "$TASK_FILE" ]; then
  echo "local_model_task: task file missing: $TASK_FILE" >&2
  exit 2
fi
if [ ! -f "$INPUT_FILE" ]; then
  echo "local_model_task: input file missing: $INPUT_FILE" >&2
  exit 2
fi

# --- ollama reachability ---
TAGS_OUT="$(curl -sS -m 10 "$OLLAMA_URL/api/tags" 2>&1)"
TAGS_RC=$?
if [ "$TAGS_RC" -ne 0 ]; then
  echo "local_model_task: ollama not answering $OLLAMA_URL/api/tags (rc=$TAGS_RC): $TAGS_OUT" >&2
  exit 2
fi

# --- load rule: the model counts as a seat ---
LOAD1="$(sysctl -n vm.loadavg | awk '{gsub(/[{}]/,""); print $1}')"
LOAD_UNDER_LIMIT=1
python3 -c "import sys; sys.exit(0 if float('$LOAD1') <= float('$LM_MAX_LOAD') else 1)" > /dev/null 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then
  LOAD_UNDER_LIMIT=0
fi
if [ "$LOAD_UNDER_LIMIT" -eq 0 ] && [ "$LM_FORCE" != "1" ]; then
  echo "local_model_task: REFUSING — 1-min load $LOAD1 > LM_MAX_LOAD $LM_MAX_LOAD (set LM_FORCE=1 to override; this is the load rule from 1_Project_Definition/Architecture/2026-09-14_local-model-headroom.md)" >&2
  exit 3
fi
if [ "$LOAD_UNDER_LIMIT" -eq 0 ] && [ "$LM_FORCE" = "1" ]; then
  echo "local_model_task: load $LOAD1 > $LM_MAX_LOAD but LM_FORCE=1 — proceeding anyway" >&2
fi

META_FILE="${OUT_FILE}.meta.json"
mkdir -p "$SCRIPT_DIR/logs"
RUN_LOG="$SCRIPT_DIR/logs/runs.log"
START_TS="$(date '+%Y-%m-%d %H:%M:%S')"

OUT_TMP=$(python3 "$SCRIPT_DIR/lib/lm_call.py" "$TASK_FILE" "$INPUT_FILE" "$OUT_FILE" "$META_FILE" "$LM_MODEL" "$LM_NUM_CTX" "$OLLAMA_URL" "$LM_THINK" 2>&1 > /dev/null)
CALL_RC=$?
# lib/lm_call.py writes its one-line status to stderr; capture it for the log
# without ever discarding stderr (we re-ran nothing — this captures the same
# stream the caller would see, then also prints it).
if [ "$CALL_RC" -ne 0 ]; then
  echo "local_model_task: model call failed (rc=$CALL_RC): $OUT_TMP" >&2
  echo "$START_TS | task=$(basename "$(dirname "$TASK_FILE")") model=$LM_MODEL rc=$CALL_RC load=$LOAD1 err=$OUT_TMP" >> "$RUN_LOG"
  exit 4
fi

echo "$OUT_TMP" >&2
echo "$START_TS | task=$(basename "$(dirname "$TASK_FILE")") model=$LM_MODEL think=$LM_THINK rc=0 load=$LOAD1 out=$OUT_FILE $OUT_TMP" >> "$RUN_LOG"
exit 0
