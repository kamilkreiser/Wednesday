#!/bin/bash
# chat_sync.sh — keep Kam's ONE page current on BOTH machines, without either agent
# remembering to do it.
#
# WHY (Kam, 2026-09-09 17:53 and 17:54, panel, verbatim):
#   "Please coordinate with Tuesday to make it work so that I can review and work off a
#    single page for both agents."
#   "it would be good if both pages were automatically synced without agent intervention
#    or both synced by either agent."
# Before this, Tuesday's replies reached his page only when a Wednesday seat happened to
# pull — a person standing in for a mechanism, which is the exact class this fleet keeps
# filing. Measured that day: his 17:48 test sat invisible to him until a manual pull.
#
# WHY IT IS SAFE TO AUTOMATE (Tuesday's argument, verified here before arming):
#   every chat file is SINGLE-WRITER by design — Wednesday writes only chat_wednesday.json,
#   Tuesday only chat_tuesday.json, the panel only chat_kam.json — and chat_log.json is
#   GITIGNORED and REBUILT from the three. So an automatic pull has nothing to conflict on.
#
# NO --autostash, DELIBERATELY. On 2026-09-09 a routine `pull --rebase --autostash` on a
# dirty tree left conflict markers in BOTH decisions.json (Kam's rulings) and chat_log.json,
# twice in one day. A background job that reaches into a live working tree to force a sync
# through is not worth 60s of latency. FAIL CLOSED AND RETRY: if the tree is busy this
# cycle skips and the next one picks it up.
#
# stderr is NEVER discarded (2026-08-06): a sync that fails silently every minute is worse
# than no sync at all.
#
# ── 2026-09-11 (Wednesday, claimed with Tuesday 05:09Z and in the WED claim ledger) ──
# MEASURED: at 14:40:48 this script's `pull --rebase` hit a conflict on panel_sync's own
# derived-data commit, printed "SKIP: pull rc=1 … Rebasing (1/3)…(3/3)", and EXITED WITH
# THE REBASE STILL STOPPED. Every later cycle — here AND in panel_sync.sh — then read
# "rebase/merge in progress" and skipped: Kam's panel sync sat dead for 23 minutes
# (14:40:48 → 15:03:54) until a seat repaired it by hand. The comment above was true of the
# CHAT files and silent about everything else a pull brings: panel_sync commits generated
# dashboard data in this same tree every 60 s, and that data does conflict.
# The root cause is TWO PULLERS IN ONE TREE. Two changes, both in the path:
#   (A) STAND DOWN while THIS tree's `panel_sync.sh loop` is live. That loop already pulls,
#       resolves derived conflicts, rebuilds chat_log.json and pushes every 60 s, and it
#       carries the recovery this script never had — so a second puller adds nothing but
#       the race. Matched on this ROOT's own path, so each seat stands down only for its
#       own loop. The pattern reaches awk through the ENVIRONMENT, never argv: a pattern in
#       awk's argv is in `ps` output and matches itself (the 2026-09-10 22:28 self-matching
#       grep, which read 6 where the answer was 2).
#   (B) ABORT a rebase THIS pull stopped in, so a failed pull can never leave the tree in a
#       state that blocks every other sync. "This pull's" = the rebase's orig-head equals
#       the HEAD read immediately before the pull. A rebase that was already running is
#       still refused at step (1) and never touched.
# RESIDUAL, stated rather than carried quietly: a rebase started by ANOTHER process, from the
# same HEAD, in the sub-second between step (1) and the pull, is indistinguishable by
# orig-head and would be aborted. On this seat the only such process is panel_sync, whose
# loop (A) stands down for; an abort costs that process one cycle and no commits.
set -u
SELF="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$SELF/../.." && pwd)"          # self-locating: works from WEDNESDAY or TUESDAY
LOG="$ROOT/2_Project_Files/fleet/state/chat_sync.log"
mkdir -p "$(dirname "$LOG")"
say(){ printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S')" "$*" >> "$LOG"; }

# (1) Never pull into a half-finished rebase/merge.
if [ -d "$ROOT/.git/rebase-merge" ] || [ -d "$ROOT/.git/rebase-apply" ] || [ -f "$ROOT/.git/MERGE_HEAD" ]; then
  say "SKIP: rebase/merge in progress"; exit 0
fi

# (1b) Stand down while this tree's panel_sync loop owns the pulls — change (A) above.
# The env assignment prefixes AWK, not ps: `VAR=x ps | awk` gives VAR to ps only, awk then
# reads an EMPTY pattern, and BSD awk's index($0, "") is non-zero on every line — the first
# red-proof of this change stood down for "pid 1" (launchd) on all six arms. An empty
# pattern is therefore refused explicitly: a matcher that matches everything cannot fail.
LOOP_PID="$(ps -axo pid=,command= | \
  LOOP_PAT="$ROOT/2_Project_Files/tools/panel_sync.sh loop" \
  awk 'BEGIN { p = ENVIRON["LOOP_PAT"] } p != "" && index($0, p) { print $1; exit }')"
if [ -n "$LOOP_PID" ]; then
  say "SKIP: panel_sync loop live (pid $LOOP_PID) owns pulls in this tree"; exit 0
fi

# (2) Pull WITHOUT autostash. A dirty tree makes this fail, and that is the intended
#     behaviour — we skip rather than touching the working tree.
PRE_HEAD="$(git -C "$ROOT" rev-parse HEAD 2>&1)"
OUT="$(git -C "$ROOT" pull --rebase 2>&1)"; rc=$?
if [ $rc -ne 0 ]; then
  RDIR=""
  [ -d "$ROOT/.git/rebase-merge" ] && RDIR="$ROOT/.git/rebase-merge"
  [ -z "$RDIR" ] && [ -d "$ROOT/.git/rebase-apply" ] && RDIR="$ROOT/.git/rebase-apply"
  if [ -n "$RDIR" ]; then
    ORIG=""
    [ -f "$RDIR/orig-head" ] && ORIG="$(cat "$RDIR/orig-head")"
    if [ -n "$ORIG" ] && [ "$ORIG" = "$PRE_HEAD" ]; then
      # (B) this pull stopped in its own rebase: abort it and PROVE the tree is out of it.
      AOUT="$(git -C "$ROOT" rebase --abort 2>&1)"; arc=$?
      NOW_HEAD="$(git -C "$ROOT" rev-parse HEAD 2>&1)"
      if [ $arc -eq 0 ] && [ ! -d "$ROOT/.git/rebase-merge" ] && [ ! -d "$ROOT/.git/rebase-apply" ] && [ "$NOW_HEAD" = "$PRE_HEAD" ]; then
        say "ABORTED the rebase this pull stopped in (pull rc=$rc; HEAD back at ${PRE_HEAD:0:9}) — $(printf '%s' "$OUT" | tr '\n' ' ' | cut -c1-160)"
      else
        say "ABORT FAILED rc=$arc HEAD=${NOW_HEAD:0:9} want ${PRE_HEAD:0:9} — REBASE DIR MAY BE LEFT; panel_sync will SKIP until repaired — $(printf '%s' "$AOUT" | tr '\n' ' ' | cut -c1-160)"
      fi
      exit 0
    fi
    say "SKIP: pull rc=$rc and a rebase this pull did NOT start is in progress (orig-head ${ORIG:0:9} != HEAD ${PRE_HEAD:0:9}) — not touched"
    exit 0
  fi
  say "SKIP: pull rc=$rc — $(printf '%s' "$OUT" | tr '\n' ' ' | cut -c1-160)"
  exit 0
fi

# (3) Rebuild the merged log the panel serves. Its own orphan guard refuses (rc 4) if the
#     derived file holds an entry no stream has — that guard is left to fail loudly.
GOUT="$(python3 "$SELF/chat_streams.py" 2>&1)"; grc=$?
if [ $grc -ne 0 ]; then
  say "REGEN FAILED rc=$grc — $(printf '%s' "$GOUT" | tr '\n' ' ' | cut -c1-200)"
  exit 0
fi
# Log HONESTLY: git's rebase path says "up to date" in more than one wording, and a log
# that prints PULLED every minute makes a real pull invisible (a detector that cries wolf).
case "$OUT" in
  *"Already up to date"*|*"is up to date"*|*"up to date with"*)
      say "ok: nothing upstream; $(printf '%s' "$GOUT" | tail -1)" ;;
  *)  say "PULLED; $(printf '%s' "$GOUT" | tail -1)" ;;
esac
exit 0
