#!/bin/bash
# status_watch.sh <STATUS file> [interval-seconds]
#
# Waits until the LAST line of a brief_seat STATUS file is a final marker, then
# prints it and exits 0. Run it as a tracked background task (run_in_background),
# never disowned: its exit is what wakes the coordinator.
#
# WHY IT IS TRACKED (2026-10-20, s122): until today this lived as status_watch2.sh
# in each seat's session scratchpad and died at every rotation, so each successor
# rebuilt it from a pickup line (learnings/2026-09-20_prepared-in-a-scratchpad-is-lost).
#
# RECORDS CHECK (ledger _ledger_laptop_datasec.md 2026-10-20, w=2): twice a seat's
# final line named a records branch that held no commit (B287 records/b287, B296
# records/b296 = main), and both times Tuesday took the seat's word. So for every
# records/bNNN named in the final line this prints, from the repo that holds the
# STATUS file: the branch sha, main's sha, and how many commits the branch has
# that main does not. "EQUALS MAIN" or "NOT FOUND" means the claim has nothing
# behind it: read the seat's worktree before accepting or closing anything.
# Read verbs only (rev-parse, rev-list): this may run against another project's repo.
# MARKERS + --changed (2026-10-22, s138; s141 added READY FOR REVIEW: (B449 missed 10 min) and ROLLED BACK: (deploy seats needed hand waiters)): three seats in one night (B425 LANDED:, B427 READY:, B428 FOLDED:) and the
# gate kits (LANDING CHECKLIST:, PARKED:) needed hand-built waiters because this list lacked their final lines. And a
# watcher re-armed on a RESUMED seat fired at once on the STOPPED line still in place: with --changed as the 3rd
# argument it remembers the last line at start and fires only on a DIFFERENT final line.
F="$1"; I="${2:-30}"; CHANGED=0; [ "${3:-}" = "--changed" ] && CHANGED=1
[ -n "$F" ] || { echo "usage: status_watch.sh <STATUS file> [interval] [--changed]" >&2; exit 2; }
START=""; [ "$CHANGED" = 1 ] && [ -f "$F" ] && START=$(tail -n 1 "$F")

records_check() {
  local line="$1" dir top ref sha main ahead
  # No records ref named: nothing to check (2026-10-20 09:30 false "no git repo" line on B302's STOP).
  printf '%s\n' "$line" | grep -qE 'records/b[0-9]+' || return 0
  dir=$(dirname "$F")
  top=$(git -C "$dir" rev-parse --show-toplevel 2>&1) || { echo "RECORDS CHECK: no git repo holds $F ($top)"; return; }
  for ref in $(printf '%s\n' "$line" | grep -oE 'records/b[0-9]+[A-Za-z0-9_-]*' | sort -u); do
    sha=$(git -C "$top" rev-parse --verify -q "$ref^{commit}" 2>/dev/null \
       || git -C "$top" rev-parse --verify -q "refs/remotes/origin/$ref^{commit}" 2>/dev/null)
    # 2026-10-23 s149: compare to origin/main when the clone has it; the LOCAL main of a project clone is often stale
    # (B508: local main 76bb8ba printed "156 commits ahead" for a branch 1 commit on origin/main eaa09fc3).
    main=$(git -C "$top" rev-parse --verify -q "refs/remotes/origin/main^{commit}" 2>/dev/null || git -C "$top" rev-parse --verify -q "main^{commit}" 2>/dev/null)
    if [ -z "$sha" ]; then
      echo "RECORDS CHECK: $ref NOT FOUND in $top"
    elif [ "$sha" = "$main" ]; then
      echo "RECORDS CHECK: $ref EQUALS MAIN ($sha) in $top: no commit behind the claim"
    else
      ahead=$(git -C "$top" rev-list --count "$main..$sha" 2>&1)
      echo "RECORDS CHECK: $ref = $sha, main = $main, $ahead commit(s) on the branch not on main ($top)"
    fi
  done
}

while :; do
  if [ -f "$F" ]; then
    L=$(tail -n 1 "$F")
    case "$L" in
      VERDICT:*|STOPPED:*|"READY FOR QA:"*|READY:*|BLOCKED:*|"RECORDS DONE:"*|"RECORDS COMMITTED:"*|DONE:*|LANDED:*|FOLDED:*|"LANDING CHECKLIST:"*|PARKED:*|DEPLOYED:*|"READY FOR REVIEW:"*|"ROLLED BACK:"*)
        [ "$CHANGED" = 1 ] && [ "$L" = "$START" ] && { sleep "$I"; continue; }
        echo "FINAL $(date '+%H:%M:%S') :: $F :: $L"
        records_check "$L"
        exit 0;;
    esac
  fi
  sleep "$I"
done
