#!/bin/bash
# drain.sh - drain the Spark filler queue: run run_filler.py once per iteration while `queued` rows exist.
# usage: bash drain.sh [extra run_filler.py args, e.g. --stub-reply FILE]
# Stops: queue empty -> rc 0 | gated by run_filler (rc 3) -> rc 3 | run_filler usage error (rc 2) -> rc 2 |
#        any other runner rc -> that rc | queued count did not fall after a run -> rc 4 (no spin) | lock held/stale -> rc 5 |
#        iteration cap DRAIN_MAX (default 200) -> rc 6.
# Never two at once: lock DIR $DRAIN_STATE/drain.lock holding a `pid` file. A live holder -> refuse. A dead holder (stale) -> ALSO refuse,
# loudly, and leave the lock for a human; this script never removes a lock it does not own.
# One log line per iteration (plus start/stop lines) in $DRAIN_STATE/drain.log (tab-separated: utc, event, iter, row, rc, detail).
# Env seams: FILLER_QUEUE, FILLER_RUNS, FILLER_LOG (read by run_filler.py too), DRAIN_STATE, DRAIN_RUNNER, DRAIN_MAX. bash 3.2 safe.
# Does not install anything (no launchd); the schedule is the coordinator's call. Never touches boards, mail, git.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUEUE="${FILLER_QUEUE:-$HERE/queue.tsv}"
STATE="${DRAIN_STATE:-$HERE/state}"
RUNNER="${DRAIN_RUNNER:-python3 $HERE/run_filler.py}"
MAX="${DRAIN_MAX:-200}"
LOCK="$STATE/drain.lock"
LOG="$STATE/drain.log"
mkdir -p "$STATE" || { echo "drain: cannot create $STATE" >&2; exit 2; }

log() { # event iter row rc detail
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "$2" "$3" "$4" "$5" >> "$LOG"
  echo "drain: $1 iter=$2 row=$3 rc=$4 $5" >&2
}
queued_ids() { awk -F'\t' '/^#/ || /^id\t/ || NF==0 {next} $4=="queued" {print $1}' "$QUEUE" 2>/dev/null; }
status_of() { awk -F'\t' -v id="$1" '$1==id {print $4}' "$QUEUE" 2>/dev/null; }

# ---- lock (mkdir is atomic) ----
if ! mkdir "$LOCK" 2>/dev/null; then
  holder="$(cat "$LOCK/pid" 2>/dev/null)"
  if [ -n "$holder" ] && kill -0 "$holder" 2>/dev/null; then
    log refused 0 - 5 "lock held by live pid $holder ($LOCK)"
  else
    log refused 0 - 5 "STALE lock (pid '${holder:-none}' not running) at $LOCK - NOT removed; a human must check and rmdir it"
  fi
  exit 5
fi
echo $$ > "$LOCK/pid"
cleanup() { [ "$(cat "$LOCK/pid" 2>/dev/null)" = "$$" ] && { rm -f "$LOCK/pid"; rmdir "$LOCK" 2>/dev/null; }; }
trap cleanup EXIT
trap 'log interrupted "$i" "$id" 130 "signal"; exit 130' INT TERM

i=0; id=-
log start 0 - 0 "queue=$QUEUE"
while :; do
  ids="$(queued_ids)"
  if [ -z "$ids" ]; then log empty "$i" - 0 "no queued rows; drained $i"; exit 0; fi
  if [ "$i" -ge "$MAX" ]; then log cap "$i" - 6 "DRAIN_MAX=$MAX reached"; exit 6; fi
  id="$(printf '%s\n' "$ids" | head -n 1)"
  before="$(printf '%s\n' "$ids" | wc -l | tr -d ' ')"
  i=$((i + 1))
  $RUNNER "$@"
  rc=$?
  after="$(queued_ids | wc -l | tr -d ' ')"
  st="$(status_of "$id")"
  case "$rc" in
    0) : ;;
    3) log gated "$i" "$id" 3 "runner gated; row left queued"; exit 3 ;;
    2) log usage "$i" "$id" 2 "runner usage error"; exit 2 ;;
    *) log failed "$i" "$id" "$rc" "runner rc $rc; status=$st"; exit "$rc" ;;
  esac
  log ran "$i" "$id" 0 "status=$st queued $before->$after"
  if [ "$after" -ge "$before" ]; then log stuck "$i" "$id" 4 "queued count did not fall ($before->$after); stopping to avoid a spin"; exit 4; fi
done
