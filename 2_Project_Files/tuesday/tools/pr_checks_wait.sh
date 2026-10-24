#!/bin/bash
# pr_checks_wait.sh <owner/repo> <pr number> <head sha> [interval-seconds] [max-minutes]
#
# Waits until every check-run on <head sha> has completed, then prints the table and exits 0 (all success, neutral or
# skipped) or 1 (any other conclusion). Run it as a tracked background task (run_in_background): its exit is the wake.
# Uses the caller's GH_CONFIG_DIR (export the project's own before running it).
#
# WHY (ledger _ledger_laptop_datasec.md 2026-10-17: a hand-written waiter grouped `.conclusion // .state` and counted
# in-progress checks as finished): the PENDING set is counted explicitly (status not "completed"), and a read that
# returns no check-runs at all is "not started", never "done". Also refuses if the PR head moved off <head sha>.
# Only check-runs created after the newest pull_request run started are counted, so a reopen's fresh run is what is read.
R="$1"; N="$2"; SHA="$3"; I="${4:-60}"; MAX="${5:-40}"
[ -n "$R" ] && [ -n "$N" ] && [ -n "$SHA" ] || { echo "usage: pr_checks_wait.sh <owner/repo> <pr> <head sha> [interval] [max-min]" >&2; exit 2; }
START=$(date +%s)
while :; do
  HEAD=$(gh api "repos/$R/pulls/$N" --jq .head.sha 2>&1)
  [ "$HEAD" = "$SHA" ] || { echo "REFUSED: #$N head is $HEAD, not $SHA"; exit 3; }
  T=$(gh api "repos/$R/commits/$SHA/check-runs?per_page=100" 2>&1) || { echo "$(date +%H:%M:%S) read failed (UNKNOWN), retrying"; sleep "$I"; continue; }
  # newest instance of each check-run name only (a re-trigger leaves older completed runs beside the new ones)
  ROWS=$(printf '%s' "$T" | python3 -I "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pr_checks_newest.py")
  TOTAL=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -i -E '.')
  PEND=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -v -i -E '^completed')
  echo "$(date +%H:%M:%S) #$N checks $TOTAL, pending $PEND"
  if [ "$TOTAL" -gt 0 ] && [ "$PEND" -eq 0 ]; then
    printf '%s\n' "$ROWS"
    BAD=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -v -i -E '^completed	(success|neutral|skipped)	')
    [ "$BAD" -eq 0 ] && { echo "ALL GREEN: #$N $SHA"; exit 0; } || { echo "NOT GREEN: #$N $BAD check(s)"; exit 1; }
  fi
  [ $(( $(date +%s) - START )) -ge $((MAX*60)) ] && { echo "GAVE UP after ${MAX} min; pending set:"; printf '%s\n' "$ROWS" | /usr/bin/grep -v -i -E '^completed'; exit 4; }
  sleep "$I"
done
