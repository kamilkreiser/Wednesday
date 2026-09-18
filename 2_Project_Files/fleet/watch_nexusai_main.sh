#!/bin/bash
# watch_nexusai_main.sh — exit when Datasec/NexusAI's origin/main MOVES.
#
# WHY THIS EXISTS (Kam, 2026-09-18: "let me know when the push is unblocked").
# His release-image push is gated on the checklist merging to main. The agents mail
# MERGED on each merge and that mail wakes this seat — but that wake depends on the
# REPORTER being alive. A seat that dies quietly produces no merge and no mail, and
# silence from an agent is a question, never an answer
# (learnings/2026-08-09_an-enforcement-you-must-arm-is-not-one.md rule 3).
# This watcher observes the WORLD instead: it reads origin directly, so it is
# independent of every seat's liveness — a control that can fail independently of the
# failure it is testing for (2026-09-08_a-false-absence..., rule 11).
#
# It EXITS on the event. The harness re-invokes the seat when a background job exits,
# so the exit IS the wake — not a poll the seat has to remember
# (2026-09-07_an-instruction-to-wait-must-name-what-wakes.md).
#
# Usage: watch_nexusai_main.sh [baseline-sha] [poll-seconds] [max-minutes]
#   rc 0 = main moved (prints old and new)   rc 3 = timed out, main unchanged
#   rc 4 = could not read origin N times running (reported, never silently retried forever)
set -u
REPO="/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files"
POLL="${2:-60}"; MAXMIN="${3:-180}"
LOG="/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/logs/watch_nexusai_main.log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || LOG=/dev/stderr

read_main() { git -C "$REPO" ls-remote origin main 2>>"$LOG" | awk '{print $1}' | head -1; }

BASE="${1:-}"
if [ -z "$BASE" ]; then
  BASE="$(read_main)"
  [ -n "$BASE" ] || { echo "watch: cannot read origin/main at start" | tee -a "$LOG" >&2; exit 4; }
fi
echo "$(date -u +%FT%TZ) watch armed: baseline $BASE poll ${POLL}s max ${MAXMIN}m" >>"$LOG"

DEADLINE=$(( $(date +%s) + MAXMIN*60 ))
FAILS=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  sleep "$POLL"
  CUR="$(read_main)"
  if [ -z "$CUR" ]; then
    FAILS=$((FAILS+1))
    echo "$(date -u +%FT%TZ) read failed ($FAILS/5)" >>"$LOG"
    [ "$FAILS" -ge 5 ] && { echo "watch: origin unreadable 5 times running — reporting rather than looping" | tee -a "$LOG" >&2; exit 4; }
    continue
  fi
  FAILS=0
  if [ "$CUR" != "$BASE" ]; then
    echo "$(date -u +%FT%TZ) MAIN MOVED $BASE -> $CUR" >>"$LOG"
    echo "NEXUSAI MAIN MOVED: $BASE -> $CUR"
    exit 0
  fi
done
echo "$(date -u +%FT%TZ) timed out, main still $BASE" >>"$LOG"
echo "NEXUSAI MAIN UNCHANGED after ${MAXMIN}m: $BASE"
exit 3
