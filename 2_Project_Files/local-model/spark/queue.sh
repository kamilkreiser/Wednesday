#!/bin/bash
# queue.sh [--max N] — drain local-model/spark/queue.md through round.sh, ONE round at a time (2026-10-05).
#
# queue.md: one brief per non-comment line —  <brief_dir> [pin=value ...]   (`#` lines and blank lines ignored;
# a relative brief_dir resolves against local-model/night/briefs/). The FIRST line is taken each time; when its round
# ends the line is REMOVED from queue.md and a row is APPENDED to done.md:
#   | <when> | <tag> | <verdict> | <round s> | <model s> | <prompt+completion tok> | golden | <run dir> | <queue line> |
#
# Stops (line LEFT in the queue) and prints a loud `SPARK QUEUE STOPPED` line when:
#   - round.sh says ENDPOINT DOWN (rc 4) — the tunnel or the box; this never restarts either;
#   - free space on the runs volume < SPARK_MIN_FREE_GB (default 20) — per-round clones are ~335 MB each and are
#     removed by prune_work.py once their done.md row is written (and at start, any > 24 h with a row).
# A BUSY round (rc 3: a hand-run round holds spark/state/round.lock) is waited for, not dropped. REFUSED / FAIL /
# HARNESS rounds are recorded and the loop moves on. Exits 0 when the queue is empty.
#
# One drainer at a time: spark/state/queue.lock (pid; a dead pid's lock is moved aside, never deleted).
# Background:  nohup bash local-model/spark/queue.sh >> local-model/spark/state/queue.log 2>&1 &
# Env: SPARK_QUEUE / SPARK_DONE (file overrides, for tests), SPARK_WAIT_S (busy poll, default 30), plus everything
# round.sh reads (SPARK_URL, ...). bash 3.2; stderr never discarded; no cd. It never raises PRs, pushes or merges.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(dirname "$HERE")"
QUEUE="${SPARK_QUEUE:-$HERE/queue.md}"
DONE="${SPARK_DONE:-$HERE/done.md}"
STATE="${SPARK_STATE:-$HERE/state}"
RUNS="${SPARK_RUNS:-$LM/runs}"
WAIT_S="${SPARK_WAIT_S:-30}"
MIN_FREE_GB="${SPARK_MIN_FREE_GB:-20}"
MAX=0
while [ $# -gt 0 ]; do
  case "$1" in
    --max) MAX="${2:-0}"; shift 2 ;;
    -h|--help) sed -n 2,22p "$0"; exit 0 ;;
    *) echo "usage: queue.sh [--max N]" >&2; exit 64 ;;
  esac
done
ts() { date '+%F %T'; }
mkdir -p "$STATE"
[ -f "$QUEUE" ] || { echo "queue: no queue file at $QUEUE" >&2; exit 64; }

QLOCK="$STATE/queue.lock"
if ! mkdir "$QLOCK" 2>/dev/null; then
  OLD="$(cat "$QLOCK/pid" 2>/dev/null)"
  if [ -n "$OLD" ] && kill -0 "$OLD" 2>/dev/null; then echo "queue: another drainer is running (pid $OLD) — exiting"; exit 3; fi
  ST="$STATE/stale_locks/$(date +%Y%m%d-%H%M%S)"; mkdir -p "$ST"; mv "$QLOCK" "$ST/queue.lock"
  echo "queue: moved a stale queue lock (pid ${OLD:-none}) -> $ST"
  mkdir "$QLOCK" 2>/dev/null || { echo "queue: could not take $QLOCK" >&2; exit 3; }
fi
echo $$ > "$QLOCK/pid"
trap 'rm -f "$QLOCK/pid"; rmdir "$QLOCK" 2>/dev/null' EXIT

if [ ! -f "$DONE" ]; then
  printf '# spark/done.md — one row per Spark round drained from spark/queue.md by queue.sh (newest at the bottom)\n| when | tag | verdict | round s | model s | tokens (prompt+completion) | golden | run dir | queue line |\n|---|---|---|---|---|---|---|---|---|\n' > "$DONE"
fi

first_line() { python3 - "$QUEUE" <<'PY'
import sys
for l in open(sys.argv[1], encoding="utf-8"):
    s = l.strip()
    if s and not s.startswith("#"):
        print(s); break
PY
}
drop_line() { # remove the FIRST line equal (stripped) to $1, atomically (tmp + mv)
  python3 - "$QUEUE" "$1" <<'PY'
import os, sys
p, want = sys.argv[1], sys.argv[2]
lines = open(p, encoding="utf-8").read().split("\n")
for i, l in enumerate(lines):
    if l.strip() == want:
        del lines[i]; break
else:
    print(f"queue: WARNING the line was no longer in {p} (edited meanwhile?) — nothing removed"); sys.exit(0)
t = p + ".tmp"
open(t, "w", encoding="utf-8").write("\n".join(lines)); os.replace(t, p)
PY
}

N=0
echo "queue: started $(ts) pid $$ — $QUEUE"
# catch-up (crashes): the runner's own work clones older than 24 h whose round has a verdict row (prune_work.py guards)
SPARK_DONE="$DONE" SPARK_STATE="$STATE" python3 "$HERE/prune_work.py" --older-than-hours "${SPARK_PRUNE_CATCHUP_H:-24}"
while :; do
  LINE="$(first_line)"
  if [ -z "$LINE" ]; then echo "queue: empty at $(ts) after $N round(s) — exiting"; exit 0; fi
  if [ "$MAX" -gt 0 ] && [ "$N" -ge "$MAX" ]; then echo "queue: --max $MAX reached at $(ts) — exiting, $(grep -cv '^\s*\(#\|$\)' "$QUEUE") line(s) left"; exit 0; fi
  FREE_GB="$(df -g "$RUNS" 2>/dev/null | awk 'NR==2{print $4}')"
  if [ -n "$FREE_GB" ] && [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
    echo "!!!!! SPARK QUEUE STOPPED $(ts): ${FREE_GB} GB free on the runs volume < SPARK_MIN_FREE_GB=$MIN_FREE_GB — quarantine old spark/cache/work clones first. Line left in the queue: $LINE"
    exit 6
  fi
  # shellcheck disable=SC2086
  set -- $LINE
  BD="$1"; shift
  case "$BD" in /*) ;; *) BD="$LM/night/briefs/$BD" ;; esac
  SUM="$STATE/last_round.json"; rm -f "$SUM"
  echo "queue: ---- $(ts) round $((N+1)): $LINE"
  SPARK_ROUND_SUMMARY="$SUM" bash "$HERE/round.sh" "$BD" "$@"; RC=$?
  if [ "$RC" -eq 3 ]; then
    echo "queue: round lock held by a hand-run round — waiting ${WAIT_S}s, line kept"; sleep "$WAIT_S"; continue
  fi
  if [ "$RC" -eq 4 ]; then
    echo "!!!!! SPARK QUEUE STOPPED $(ts): the Spark endpoint is DOWN (round.sh rc 4). Line left in the queue: $LINE"
    echo "!!!!! check the tunnel (pgrep -fl 'L 47788:127.0.0.1:8888') and the box; then re-run queue.sh"
    exit 4
  fi
  N=$((N+1))
  python3 - "$SUM" "$DONE" "$LINE" "$RC" "$(ts)" "$(basename "$BD")" <<'PY'
import json, os, sys
sp, done, line, rc, when, tag = sys.argv[1:7]
d = json.load(open(sp)) if os.path.isfile(sp) else {}
verdict = d.get("verdict") or {"0": "PASS", "1": "FAIL", "2": "REFUSED", "5": "HARNESS"}.get(rc, f"rc{rc}")
if d.get("checker_result") and verdict in ("PASS", "FAIL"):
    verdict = f"{verdict} ({d['checker_result']})"
elif verdict not in ("PASS", "FAIL") and d.get("line"):
    verdict = d["line"][:200]
tok = (f"{d.get('prompt_tokens')}+{d.get('completion_tokens')}" if d.get("prompt_tokens") is not None else "-")
row = [when, tag, verdict, str(d.get("round_wall_s", "-")), str(d.get("model_wall_s") or "-"), tok,
       d.get("golden") or "-", d.get("run_dir") or "-", line.replace("|", "\\|")]
open(done, "a", encoding="utf-8").write("| " + " | ".join(row) + " |\n")
PY
  drop_line "$LINE"
  # the verdict row is written: remove THIS round's work clone (regenerable; the run dir is the record)
  WD="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("work_dir") or "")' "$SUM" 2>&1)"
  if [ -n "$WD" ] && [ -d "$WD" ]; then SPARK_DONE="$DONE" SPARK_STATE="$STATE" python3 "$HERE/prune_work.py" "$WD"; fi
done
