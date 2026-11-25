#!/bin/bash
# wait_any.sh — Friday's OWN wake path for CoAgent seats and merge checks (ledger 2026-11-25:
# the fleet watcher's silence reads the same as a quiet floor; this is the first path, it the second).
#
# READ-ONLY. It writes only its own baseline file. It exits (which wakes the session that started it
# in the background) when ONE of these happens:
#   - a watched merge-check output file gains a MERGE_CHECK_EXIT line it did not have at the start
#   - the LAST LINE of a watched STATUS file changes AND the new line is a stop shape
#     (READY, MERGED, BLOCKED, BLOCKER, STOP, VERDICT, or holds a question mark)
#   - a watched file disappears
#   - the maximum runtime passes (exit 4: a timeout is a wake too, never a silent end)
#
# usage: wait_any.sh <baseline-file> <max-seconds> <file> [<file> ...]
#   a file whose name ends in .out is a merge-check output; any other file is a STATUS file.
#   --once as the FIRST argument: take the baseline, run ONE comparison pass, print QUIET or the
#   event, and exit (0 quiet, 10 fired). Used to prove both paths before arming.
#
# exit codes: 10 fired · 4 timeout · 2 usage · 3 a watched file was missing at the start
#
# The baseline and the comparison use the SAME per-file loop (2026-11-25: one grep over several
# files returned its lines in another order and fired at once).

set -u
ONCE=0
if [ "${1:-}" = "--once" ]; then ONCE=1; shift; fi
if [ $# -lt 3 ]; then
  echo "usage: wait_any.sh [--once] <baseline-file> <max-seconds> <file> [<file> ...]" >&2
  exit 2
fi
BASE="$1"; MAX="$2"; shift 2
case "$MAX" in ''|*[!0-9]*) echo "max-seconds must be a whole number, got '$MAX'" >&2; exit 2;; esac

STOP_RE='(READY|MERGED|BLOCKED|BLOCKER|STOP|VERDICT|\?)'

sig_of() {  # prints one line: the state of one watched file
  local f="$1"
  if [ ! -e "$f" ]; then echo "MISSING"; return 0; fi
  case "$f" in
    *.out) /usr/bin/grep -c 'MERGE_CHECK_EXIT' "$f" ;;
    *)     tail -n 1 "$f" ;;
  esac
}

: > "$BASE" || { echo "cannot write baseline $BASE" >&2; exit 2; }
for f in "$@"; do
  s="$(sig_of "$f")"
  if [ "$s" = "MISSING" ]; then echo "watched file missing at the start: $f" >&2; exit 3; fi
  printf '%s\t%s\n' "$f" "$s" >> "$BASE"
done
echo "armed $(date '+%H:%M:%S'): $# file(s), max ${MAX}s, baseline $BASE"

check_pass() {  # prints the event and returns 10 when something fired
  local f old new
  for f in "$@"; do
    old="$(awk -F'\t' -v k="$f" '$1==k{sub(/^[^\t]*\t/,""); print; exit}' "$BASE")"
    new="$(sig_of "$f")"
    [ "$new" = "$old" ] && continue
    if [ "$new" = "MISSING" ]; then echo "FIRED $(date '+%H:%M:%S') GONE: $f"; return 10; fi
    case "$f" in
      *.out) echo "FIRED $(date '+%H:%M:%S') MERGE-CHECK-EXIT: $f :: $(/usr/bin/grep 'MERGE_CHECK_EXIT' "$f" | tail -n 1)"; return 10 ;;
      *) if printf '%s' "$new" | /usr/bin/grep -E -q "$STOP_RE"; then
           echo "FIRED $(date '+%H:%M:%S') STATUS: $f :: $new"; return 10
         fi ;;
    esac
  done
  return 0
}

if [ "$ONCE" = 1 ]; then
  check_pass "$@"; rc=$?
  [ "$rc" = 0 ] && echo "QUIET"
  exit "$rc"
fi

START=$(date +%s)
while :; do
  check_pass "$@"; rc=$?
  [ "$rc" != 0 ] && exit "$rc"
  NOW=$(date +%s)
  if [ $((NOW - START)) -ge "$MAX" ]; then
    echo "TIMEOUT $(date '+%H:%M:%S') after ${MAX}s with no event: re-arm and read a figure that moves"
    exit 4
  fi
  sleep "${WAIT_ANY_SLEEP:-30}"
done
