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

# ── RECOVERY: the only conflicts this sync can legitimately settle are DERIVED ──
# _boot_digest*.md is generated from the lesson files; 0_Brain/dashboard/data/*.json
# is this machine's collector output and the rendered chat log. Both are rebuilt
# from source below, so WHICH side wins the merge does not decide the content —
# the regeneration does. Anything else conflicting is real work, and this script
# has no business guessing at it: abort, leave the tree clean, log loudly.
#
# Either way the tree ends CLEAN. That is the whole point: the next cycle must be
# able to run. safe_push.sh already carried these same rules for the interactive
# path (its `0_Brain/learnings/_boot_digest*.md)` case) — the defect was that the
# unattended path never learned them.
DERIVED_RE='^(0_Brain/learnings/_boot_digest(_by_tier)?\.md|0_Brain/dashboard/data/.*\.json)$'
# ── ADVANCE THE OTHER SEAT'S STREAM WITHOUT A REBASE ───────────────────────
# Each seat is the SOLE writer of its own chat stream, so origin is authoritative
# for the other one. Bringing it forward needs no rebase and touches nothing of
# mine — which is why it is safe to do while my tree is dirty.
#
# TWO REFUSALS, both deliberate:
#   * never touch MY OWN stream (that is the one file this seat writes)
#   * never move a stream BACKWARDS — take origin's copy only when it is strictly
#     ahead. A stream that shrank is a symptom, not something to propagate.
advance_other_streams(){
  local mine other f before after
  case "${WED_AGENT:-wednesday}" in
    tuesday) mine="chat_tuesday.json";   other="chat_wednesday.json" ;;
    *)       mine="chat_wednesday.json"; other="chat_tuesday.json" ;;
  esac
  git fetch -q --no-write-fetch-head origin 2>/dev/null || { say "  advance: fetch failed, nothing taken"; return 0; }
  f="0_Brain/dashboard/data/$other"
  before=$(python3 -c "
import json,sys
try:
    d=json.load(open('$ROOT/$f'))
    print(len(d if isinstance(d,list) else d.get('messages',[])))
except Exception: print(-1)
" 2>/dev/null)
  after=$(git show "origin/main:$f" 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    print(len(d if isinstance(d,list) else d.get('messages',[])))
except Exception: print(-1)
" 2>/dev/null)
  case "$before$after" in *-1*) say "  advance: could not read both copies of $other; nothing taken"; return 0 ;; esac
  if [ "$after" -le "$before" ]; then
    say "  advance: origin $other ($after) is not ahead of local ($before); nothing taken"
    return 0
  fi
  git checkout "origin/main" -- "$f" 2>/dev/null || { say "  advance: checkout of $other FAILED"; return 0; }
  if python3 "$ROOT/2_Project_Files/tools/chat_streams.py" >/dev/null 2>&1; then
    say "  advance: $other $before -> $after rows from origin, rendered log rebuilt (my own $mine untouched)"
  else
    say "  advance: $other taken ($before -> $after) but chat_streams.py FAILED — the rendered log may be stale"
  fi
}

resolve_derived_or_abort(){
  git rev-parse --verify -q HEAD >/dev/null 2>&1 || { say "RECOVER: no HEAD, refusing"; return 1; }
  if [ ! -d .git/rebase-merge ] && [ ! -d .git/rebase-apply ] && [ ! -f .git/MERGE_HEAD ]; then
    say "RECOVER: no rebase/merge in progress, tree already clean"; return 0
  fi
  # A pull brings MANY commits. `rebase --continue` past one conflict routinely
  # lands on the NEXT one — MEASURED 2026-09-10 in the red-proof harness, where a
  # derived-file conflict was followed by a real-work conflict two commits later.
  # So this is a bounded LOOP that re-classifies at every stop, not a single pass.
  local i conflicted foreign cont cont_rc
  for i in $(seq 1 30); do
    if [ ! -d .git/rebase-merge ] && [ ! -d .git/rebase-apply ] && [ ! -f .git/MERGE_HEAD ]; then
      say "RECOVER: rebase completed after $((i-1)) resolution(s); rebuilding derived files from source"
      python3 "$ROOT/2_Project_Files/tools/boot_digest.py" --by-tier >/dev/null 2>&1
      python3 "$ROOT/2_Project_Files/tools/boot_digest.py" >/dev/null 2>&1
      python3 "$ROOT/2_Project_Files/tools/chat_streams.py" >/dev/null 2>&1
      if [ -n "$(git status --porcelain -- 0_Brain/learnings 0_Brain/dashboard/data 2>/dev/null)" ]; then
        git add -A 0_Brain/learnings 0_Brain/dashboard/data >/dev/null 2>&1
        git commit -q -m "panel_sync: derived files rebuilt from source after a conflict" >/dev/null 2>&1
      fi
      say "RECOVER: tree clean, derived files rebuilt"
      return 0
    fi
    conflicted=$(git diff --name-only --diff-filter=U 2>/dev/null)
    if [ -n "$conflicted" ]; then
      foreign=$(printf '%s\n' "$conflicted" | grep -Ev "$DERIVED_RE" || true)
      if [ -n "$foreign" ]; then
        say "RECOVER: ABORTING — conflict outside the derived set, real work is not guessed at: $(printf '%s' "$foreign" | tr '\n' ' ' | cut -c1-200)"
        git rebase --abort >/dev/null 2>&1 || git merge --abort >/dev/null 2>&1
        return 1
      fi
      printf '%s\n' "$conflicted" | while IFS= read -r f; do
        [ -n "$f" ] || continue
        git checkout --ours -- "$f" >/dev/null 2>&1 || git checkout --theirs -- "$f" >/dev/null 2>&1
        git add -- "$f" >/dev/null 2>&1
      done
    fi
    # Resolving a derived file to upstream can leave the replayed commit EMPTY.
    # git then refuses --continue and names --skip; dropping our copy is correct
    # here precisely because the content is rebuilt from source at the end.
    #
    # ORDERING IS LOad-BEARING AND IT WAS A REAL BUG, caught by the red-proof
    # harness on 2026-09-10 before this shipped: git's CONFLICT hint text itself
    # contains the string "git rebase --skip". An earlier version grepped the
    # combined output for `--skip`, matched that HINT while REALWORK.md was still
    # conflicted, and called `git rebase --skip` — which would have silently
    # DROPPED A REAL-WORK COMMIT. So: --skip is considered ONLY when there is
    # nothing conflicted at all, and the pattern no longer mentions --skip.
    cont=$(GIT_EDITOR=true git rebase --continue 2>&1); cont_rc=$?
    if [ "$cont_rc" -ne 0 ]; then
      if git diff --name-only --diff-filter=U 2>/dev/null | grep -q .; then
        continue    # a NEW conflict — go round and re-classify it, never skip
      fi
      if printf '%s' "$cont" | grep -qiE 'no changes|nothing to commit|patch is empty'; then
        git rebase --skip >/dev/null 2>&1 || { say "RECOVER: --skip failed, aborting"; git rebase --abort >/dev/null 2>&1; return 1; }
      else
        say "RECOVER: rebase --continue failed with nothing conflicted, aborting: $(printf '%s' "$cont" | tr '\n' ' ' | cut -c1-160)"
        git rebase --abort >/dev/null 2>&1 || git merge --abort >/dev/null 2>&1
        return 1
      fi
    fi
  done
  say "RECOVER: ABORTING — still unresolved after 30 rounds, refusing to loop"
  git rebase --abort >/dev/null 2>&1 || git merge --abort >/dev/null 2>&1
  return 1
}

cycle(){
  cd "$ROOT" || { say "FATAL cannot cd $ROOT"; return 2; }
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ]; then
    say "SKIP rebase/merge in progress"; return 0
  fi
  # MEASURED 2026-09-10: a bare dirty-tree skip fired 782 times in 790 cycles and
  # the page went 13 hours stale. The dashboard collector rewrites
  # 0_Brain/dashboard/data/*.json continuously, so this tree is ALWAYS dirty and a
  # guard that always trips is a mechanism that never runs.
  # Generated dashboard data is this seat's own output and the repo is the only
  # transport for it, so COMMIT it rather than stashing or skipping. Anything dirty
  # OUTSIDE that directory is real work in progress: skip, never stash.
  OTHER=$(git status --porcelain 2>/dev/null | grep -v ' 0_Brain/dashboard/data/' | grep -v '^?? 0_Brain/dashboard/data/')
  if [ -n "$OTHER" ]; then
    # `wc -l` on a string with no trailing newline undercounts by one and printed
    # "(0 paths)" while a path was plainly blocking — a log line that contradicts
    # itself is worse than no log line.
    N_OTHER=$(printf '%s\n' "$OTHER" | grep -c .)
    say "SKIP rebase: dirty outside dashboard/data ($N_OTHER path(s)); no autostash by design"
    # MEASURED 2026-09-10 12:11, found by the Datasec coordinator pushing back after I
    # closed her question: ONE uncommitted file of mine — an audit document I had been
    # editing since ~11:30 — blocked this sync for 42 MINUTES, and TEN of her messages
    # never reached Kam's panel. The guard's intent is right (never pull into a
    # half-finished tree) and its consequence was never costed: an ACTIVELY WORKING
    # coordinator blocks the sync indefinitely, and actively working is the NORMAL state.
    # So Kam's reading surface stops waiting on either of us finishing a piece of work.
    advance_other_streams
    return 0
  fi
  if [ -n "$(git status --porcelain -- 0_Brain/dashboard/data 2>/dev/null)" ]; then
    git add -A 0_Brain/dashboard/data >/dev/null 2>&1
    git commit -q -m "dashboard: generated data (panel_sync)" >/dev/null 2>&1 \
      && say "committed generated dashboard data" || say "WARN commit of dashboard data failed"
  fi
  # 2026-09-19 FETCH_HEAD race (0_Brain/reference/2026-09-18_fetch-head-race): never `pull` here —
  # pull READS FETCH_HEAD, which every concurrent fetch/pull on this clone rewrites (85-149/150 fails).
  if ! out=$( { { git fetch -q --no-write-fetch-head origin main || { sleep 1; git fetch -q --no-write-fetch-head origin main; }; } && git rebase origin/main; } 2>&1); then
    say "PULL FAILED: $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-200)"
    # MEASURED 2026-09-10: the old code logged and RETURNED here, leaving the
    # rebase in progress — so the guard at the top of cycle() skipped every
    # subsequent minute, forever. One conflict became a permanent silent outage:
    # 13 hours of Kam's input never left one machine, and four of the other
    # seat's replies to him existed in exactly one tree. A loop that cannot
    # recover from the ONE failure it will actually hit is not a loop.
    resolve_derived_or_abort
    return 1
  fi
  if ! sout=$(python3 "$ROOT/2_Project_Files/tools/chat_streams.py" 2>&1); then
    say "REGEN FAILED: $(printf '%s' "$sout" | tr '\n' ' ' | cut -c1-200)"; return 1
  fi
  git push origin main >/dev/null 2>&1 || say "WARN push failed"
  say "ok $(printf '%s' "$sout" | tr '\n' ' ' | cut -c1-120)"
  return 0
}

case "${1:-loop}" in
  once) cycle; exit $? ;;
  loop) say "panel_sync loop started (60s)"; while true; do cycle; sleep 60; done ;;
  *) echo "usage: panel_sync.sh once|loop" >&2; exit 2 ;;
esac
