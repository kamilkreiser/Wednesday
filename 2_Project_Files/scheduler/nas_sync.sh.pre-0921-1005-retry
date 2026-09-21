#!/bin/bash
# nas_sync.sh — the nightly NAS sync leg, with a DELETION ALARM.
#
# Kam, 2026-09-08 14:57: "create a schedule for both agents to sync to the NAS drive at
# night. Get Tuesday to sync at 11pm, and I think you should sync at 3 or 4am."
#
# WHY THIS WRAPPER EXISTS AND IS NOT JUST A CRON LINE ON devnas-sync.sh.
# `!SYNC FILES/devnas.prf` runs `batch = true` with `confirmbigdel = false`. Unattended,
# that propagates a mass deletion in either direction with nobody watching. On 2026-08-26
# exactly that happened and cost a day of recovery — and until tonight a human was always
# awake when a sync ran. A 23:00 and an 03:30 job on two machines ends that.
#
# WHAT THIS CAN AND CANNOT DO, stated honestly rather than implied:
#   PREVENT  — it CANNOT. Unison acts before anything can inspect it, `devnas-sync.sh`
#              passes no flags through (its EXTRA_ARGS takes ignores only), and the profile
#              is Kam's file at the workspace root, not Wednesday's to edit. Prevention is
#              ONE LINE in his profile — `confirmbigdel = true` — and it is asked, not taken.
#   DETECT   — it does. It counts unison's own `Deleting` lines in the run it just ran.
#   RECOVER  — the profile already keeps `backup = Name *`, `maxbackups = 5`,
#              `backuploc = central`, so deleted files sit in ~/.unison/backup ON THE MACHINE
#              THAT RAN THE LEG. That is the recovery path that worked on 2026-08-26.
#   REPORT   — every run leaves a one-line summary the morning seat reads, so a silent night
#              is a fact rather than an assumption.
#
# NEVER add `>/dev/null` here. A sync failure you cannot diagnose costs more than it saves,
# and a deletion you cannot see is a deletion you keep.
set -u

SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"; SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
HERE="$(cd -P "$(dirname "$SOURCE")" && pwd)"
PROJECT_DIR="$(cd -P "$HERE/../.." && pwd)"
WORKSPACE="$(cd -P "$PROJECT_DIR/.." && pwd)"
AGENT="${WED_AGENT:-wednesday}"

# >>> ruled-ignores — KAM'S RULINGS ON WHAT THIS LEG SYNCS
# 2026-09-10 20:27 `stop-partition-rerun` + 20:28 `nas-shared-folders-owner = wednesday`:
#   this leg does NOT walk Datasec or the TUESDAY tree — Tuesday's leg owns those.
# 2026-09-11 07:23 `narrow-hard`: "Cut node_modules, worktrees and regenerable bulk from
#   the synced set, then re-run".
# WHY IT LIVES HERE: until 2026-09-11 the partition existed ONLY in the environment of a
# hand-launched re-run. The 03:30 launchd job passes NO environment, so the nightly leg
# would have run WITHOUT the partition Kam ruled. A ruling that lives in one shell is not
# in force.
# SCOPED to agent=wednesday: another agent running this wrapper must never inherit a set
# that excludes its own tree. An explicitly exported DEVNAS_IGNORE_NAMES still wins.
# The engine takes BASENAMES only (`-ignore "Name X"`, any depth), so every name below is
# one that is regenerable wherever it appears. `.azure/telemetry` was on the card as
# "similar bulk" and is NOT here: as a basename, `Name telemetry` would match every folder
# of that name. `dist`/`build`/`coverage` are NOT here either: those names hold real
# source in some trees.
if [ "$AGENT" = "wednesday" ] && [ -z "${DEVNAS_IGNORE_NAMES:-}" ]; then
  DEVNAS_IGNORE_NAMES="Datasec TUESDAY node_modules worktrees .venv __pycache__ .next .turbo .pytest_cache"
fi
export DEVNAS_IGNORE_NAMES="${DEVNAS_IGNORE_NAMES:-}"
# <<< ruled-ignores

ENGINE="$WORKSPACE/!SYNC FILES/devnas-sync.sh"
LOGDIR="$PROJECT_DIR/2_Project_Files/scheduler/logs"
STATEDIR="$PROJECT_DIR/2_Project_Files/scheduler/state"
mkdir -p "$LOGDIR" "$STATEDIR"
# PID in the stamp: two runs inside the same SECOND otherwise share a log, and the
# deletion count then reads the SUM of both runs. Found by exercising this script,
# not by reading it — cases 2 and 3 of the fixture collided exactly that way.
STAMP="$(date '+%Y-%m-%d_%H%M%S')_$$"
LOG="$LOGDIR/nas_sync_${AGENT}_${STAMP}.log"
REPORT="$STATEDIR/nas_sync_last_${AGENT}.txt"
ALERT_AT="${NAS_SYNC_DELETE_ALERT:-50}"

say() { printf '%s %s\n' "$(date '+%H:%M:%S')" "$*" | tee -a "$LOG"; }

say "=== NAS sync leg — agent=$AGENT workspace=$WORKSPACE ==="

if [ ! -x "$ENGINE" ]; then
  say "REFUSING: engine not executable at $ENGINE"
  printf '%s | agent=%s | ENGINE MISSING | log=%s\n' "$STAMP" "$AGENT" "$LOG" > "$REPORT"
  exit 1
fi

# The engine handles NAS ping + mount + lock + first-sync guard itself. We do not
# re-implement any of that — re-implementing a tool's method in order to check it is
# how two implementations of one idea end up disagreeing.
say "running: $ENGINE"
"$ENGINE" 2>&1 | tee -a "$LOG"
RC=${PIPESTATUS[0]}
say "engine exit rc=$RC"

# ── THE DELETION ALARM ────────────────────────────────────────────────────────────────
# `Deleting` is unison's own token — the one the 2026-08-26 recovery was found by. We
# search for the MACHINE's word, not the human's ("deleted", "removed" appear in prose).
# NOT `grep -c ... || echo 0`: grep EXITS 1 on zero matches, so that form prints the
# count AND the fallback — "0\n0" — and every downstream field is then malformed.
# Exercising it is what showed this; reading it did not.
#
# ── 2026-09-11 (Wednesday): THE COUNT HERE WAS BLIND UNTIL TODAY, AND THIS IS WHY ─────────
# These lines read `grep -c '^Deleting ' "$LOG"` and `grep -c 'conflict' "$LOG"`. The 07:27
# narrow-hard run propagated 248 deletions and they printed 0 and 163.
#   1. This unison writes `[BGN] Deleting <path> from <root>` (plus `[END] Deleting <path>`),
#      not a bare `Deleting`.
#   2. Its log is CARRIAGE-RETURN separated (progress repaints), so a `^` anchor on the RAW
#      file matched nothing: raw 0 against 248 once `\r` becomes `\n`.
#   3. 158 of the 163 'conflict' lines were FILE NAMES containing `conflict_on`; unison's own
#      conflict marker `<-?->` appeared 0 times.
# None of the three earlier logs held a single deletion, so this alarm had never been measured
# against one. A failed normalisation reports UNKNOWN — never a zero it did not measure.
NORM="$(mktemp -t nas_sync_norm)" || NORM=""
if [ -n "$NORM" ] && tr '\r' '\n' < "$LOG" > "$NORM"; then
  DELETES=$(grep -cE '^(\[BGN\] )?Deleting ' "$NORM"); DELETES=${DELETES:-0}
  DEL_BY_ROOT=$(grep -E '^(\[BGN\] )?Deleting ' "$NORM" | sed -nE 's/^.* from (.+)$/\1/p' | sort | uniq -c | awk '{n=$1; $1=""; printf "%s%s from%s", s, n, $0; s="; "}')
  CONFLICTS=$(grep -cF -- '<-?->' "$NORM"); CONFLICTS=${CONFLICTS:-0}
else
  say "🔴 could not normalise $LOG — deletion and conflict counts are UNKNOWN, not zero"
  DELETES=UNKNOWN; DEL_BY_ROOT=""; CONFLICTS=UNKNOWN
fi
say "deletions propagated: $DELETES (alarm at $ALERT_AT)${DEL_BY_ROOT:+ — $DEL_BY_ROOT} | conflicts (<-?->): $CONFLICTS"

SUMMARY="$STAMP | agent=$AGENT | rc=$RC | deletions=$DELETES${DEL_BY_ROOT:+ ($DEL_BY_ROOT)} | conflicts=$CONFLICTS | log=$LOG"
printf '%s\n' "$SUMMARY" > "$REPORT"

if [ "$DELETES" -ge "$ALERT_AT" ] 2>/dev/null; then
  ALERT="$STATEDIR/nas_sync_ALERT_${AGENT}_${STAMP}.txt"
  {
    echo "NAS SYNC DELETION ALARM — $DELETES files were DELETED by the $AGENT leg at $STAMP."
    echo
    echo "This is not necessarily wrong: a deletion you made on purpose propagates too."
    echo "It is flagged because nobody was awake to see it, and because on 2026-08-26 this"
    echo "exact mechanism cost a day of recovery."
    echo
    echo "RECOVERY, if any of it was not intended: the deleted files are in ~/.unison/backup"
    echo "ON THIS MACHINE (backup = Name *, maxbackups = 5). They are NOT on the drives."
    echo
    echo "The deleted paths, from unison's own output:"
    grep -E '^(\[BGN\] )?Deleting ' "$NORM" | head -200
  } > "$ALERT"
  say "🔴 ALARM WRITTEN: $ALERT"
  if [ -x "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" ]; then
    "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" \
"The overnight sync to the NAS deleted $DELETES files and I want you to see that before you trust the drives.

That is above the threshold where I stop treating it as routine. It may be entirely correct — a deletion you made on purpose propagates like any other change — but nobody was awake to watch it, and this is the mechanism that cost us a day in August.

Every deleted file is recoverable. They are in the unison backup store on the machine that ran the leg, not on the drives themselves. The full list of paths is in $ALERT, and the run log is at $LOG." 2>&1 | tee -a "$LOG"
  fi
fi

say "=== done — $SUMMARY ==="
exit "$RC"
