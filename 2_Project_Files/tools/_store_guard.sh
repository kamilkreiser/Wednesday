#!/bin/bash
# _store_guard.sh — sourced by every tool that WRITES Kam's decision store.
#
# WHY (2026-09-08): `decisions.json` was committed to main with git conflict
# markers in it and was unparseable by every tool for ~20 minutes. It entered via
# an autostash conflict on one seat and was pushed. The OTHER seat then held a
# broken copy and, because neither `decision_queue.sh` nor `sync_kam_rulings.sh`
# pulls or checks anything before writing, a single card add from that seat would
# have silently reverted the repair and taken Kam's rulings back out.
#
# TWO REFUSALS, and both are REFUSALS rather than fixes ON PURPOSE:
#   1. origin holds a newer commit touching the store  -> "pull first", rc 7
#   2. the store on disk carries conflict markers      -> "resolve by hand", rc 8
#
# It does NOT auto-pull. An automatic `pull --rebase --autostash` is EXACTLY what
# produced the markers, and wiring that into two more tools would spread the
# defect rather than contain it. A human or a seat resolves this file BY HAND,
# because it is one of the two irreplaceable files in dashboard/data
# (the other is chat_log.json, which has the same standing rule from 2026-09-07).
#
# Usage:  store_guard "<path to the store>"   — call before any write path only.
#         Read commands (list/show/--dry-run) must NOT call it: a stale store is
#         still readable, and a guard that blocks reading gets routed around.
# Set STORE_GUARD_SKIP=1 to bypass (stated in the caller's output when used).

store_guard() {
  local f="${1:?store_guard: needs the store path}"
  [ "${STORE_GUARD_SKIP:-0}" = "1" ] && { echo "store_guard: SKIPPED by STORE_GUARD_SKIP=1" >&2; return 0; }
  [ -f "$f" ] || return 0                      # nothing to protect yet

  # (2) markers first — cheapest, and the failure we actually had
  if grep -qE '^(<<<<<<< |=======$|>>>>>>> )' "$f" 2>/dev/null; then
    echo "store_guard: REFUSED — $f contains GIT CONFLICT MARKERS." >&2
    grep -nE '^(<<<<<<< |=======$|>>>>>>> )' "$f" 2>/dev/null | head -6 >&2
    echo "  This file is IRREPLACEABLE (it holds Kam's rulings). Resolve it BY HAND," >&2
    echo "  card by card, keeping the RULED version of any card present on both sides." >&2
    echo "  Do not resolve it with a checkout/autostash — that is what put them here." >&2
    return 8
  fi

  # (1) staleness — measured against origin, without pulling
  local root; root="$(cd -P "$(dirname "$f")" && git rev-parse --show-toplevel 2>/dev/null)" || return 0
  git -C "$root" fetch -q origin 2>/dev/null || { echo "store_guard: could not reach origin; proceeding (offline)" >&2; return 0; }
  local rel; rel="$(git -C "$root" ls-files --full-name -- "$f" 2>/dev/null | head -1)"
  [ -n "$rel" ] || return 0                    # untracked: nothing to be stale against
  local behind; behind="$(git -C "$root" rev-list --count HEAD..origin/main -- "$rel" 2>/dev/null || echo 0)"
  if [ "${behind:-0}" -gt 0 ]; then
    echo "store_guard: REFUSED — origin/main has $behind newer commit(s) touching $rel." >&2
    git -C "$root" log --oneline -3 HEAD..origin/main -- "$rel" >&2
    echo "  PULL FIRST. Writing now would revert whatever those commits changed," >&2
    echo "  and on this file that means losing Kam's rulings." >&2
    return 7
  fi
  return 0
}
