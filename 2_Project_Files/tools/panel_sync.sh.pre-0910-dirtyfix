#!/bin/bash
# panel_sync.sh — keep this seat's half of Kam's ONE chat page current, automatically.
#
# Kam, 2026-09-09: both pages synced "without agent intervention or both synced by
# either agent". He reads the Studio page; this seat's replies reach it only through
# the repo. Symmetric script runs on both machines; agreed with the Studio seat.
#
# DESIGN NOTES, each earned today:
#  - NO --autostash. A dirty tree SKIPS the cycle and retries in a minute. An
#    automatic autostash corrupted decisions.json and chat_log.json today, twice,
#    from exactly this shape of routine pull. Fail closed; latency cost is one cycle.
#  - stderr goes to a LOG, never /dev/null: a sync failing silently every minute is
#    worse than no sync at all.
#  - SKIP if a rebase or merge is already in progress rather than pulling into a
#    half-finished state.
#  - No server poke. MEASURED 2026-09-09: this seat's server re-reads chat_log.json
#    per request (append -> served count 2037 -> 2038 with no restart). The stale
#    page earlier today was NOT a cache — the server was running from the abandoned
#    WEDNESDAY tree and reading that tree's file correctly.
#
# Usage: panel_sync.sh once   (a single cycle, for testing)
#        panel_sync.sh loop   (forever, 60s)
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG="$ROOT/2_Project_Files/tools/logs/panel_sync.log"
mkdir -p "$(dirname "$LOG")"
say(){ printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" >> "$LOG"; }

cycle(){
  cd "$ROOT" || { say "FATAL cannot cd $ROOT"; return 2; }
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ]; then
    say "SKIP rebase/merge in progress"; return 0
  fi
  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    say "SKIP dirty tree (no autostash by design; retrying next cycle)"; return 0
  fi
  if ! out=$(git pull --rebase 2>&1); then
    say "PULL FAILED: $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-200)"; return 1
  fi
  if ! sout=$(python3 "$ROOT/2_Project_Files/tools/chat_streams.py" 2>&1); then
    say "REGEN FAILED: $(printf '%s' "$sout" | tr '\n' ' ' | cut -c1-200)"; return 1
  fi
  say "ok $(printf '%s' "$sout" | tr '\n' ' ' | cut -c1-120)"
  return 0
}

case "${1:-loop}" in
  once) cycle; exit $? ;;
  loop) say "panel_sync loop started (60s)"; while true; do cycle; sleep 60; done ;;
  *) echo "usage: panel_sync.sh once|loop" >&2; exit 2 ;;
esac
