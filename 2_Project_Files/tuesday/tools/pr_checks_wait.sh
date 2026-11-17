#!/bin/bash
# pr_checks_wait.sh <owner/repo> <pr number> <head sha> [interval-seconds] [max-minutes]
#                   [--min-checks N] [--accept-superseded]
#
# Waits until every check-run on <head sha> has completed, then prints the table and exits 0 (all success, neutral or
# skipped) or 1 (any other conclusion). Run it as a tracked background task (run_in_background): its exit is the wake.
# Uses the caller's GH_CONFIG_DIR (export the project's own before running it).
#
# WHY (ledger _ledger_laptop_datasec.md 2026-10-17: a hand-written waiter grouped `.conclusion // .state` and counted
# in-progress checks as finished): the PENDING set is counted explicitly (status not "completed"), and a read that
# returns no check-runs at all is "not started", never "done". Also refuses if the PR head moved off <head sha>.
#
# --min-checks N (2026-11-18, ledger row s287): "all completed" is only "done" once at least N distinct check names
# exist. On NexusAI #220 this tool printed ALL GREEN one second after the PR opened, on a set of 1 of 7. Below N it
# keeps waiting (pending = expected but not yet created). Known repos have a default (EXPECTED below, each measured
# from a merged PR's check table); any other repo REFUSES to start without --min-checks (rc 2): an expected set
# nobody wrote down is the bug this flag exists for.
#
# MIXED (2026-11-18, same row): if a name's NEWEST run is green but an OLDER completed run of the same name on this
# head is not, the verdict is "NOT GREEN (MIXED)" rc 5 — two runs of one name can come from two events (push and
# pull_request), and newest-per-name alone would read the success. --accept-superseded downgrades that to a printed
# warning, for a deliberate re-trigger (pr_retrigger.sh) whose older failure is the run you replaced; say so wherever
# you act on it.
POS=(); MIN=""; ACCEPT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --min-checks) MIN="$2"; shift 2 ;;
    --accept-superseded) ACCEPT=1; shift ;;
    *) POS+=("$1"); shift ;;
  esac
done
R="${POS[0]}"; N="${POS[1]}"; SHA="${POS[2]}"; I="${POS[3]:-60}"; MAX="${POS[4]:-40}"
[ -n "$R" ] && [ -n "$N" ] && [ -n "$SHA" ] || { echo "usage: pr_checks_wait.sh <owner/repo> <pr> <head sha> [interval] [max-min] [--min-checks N] [--accept-superseded]" >&2; exit 2; }
# Expected distinct check names per repo, read from a merged PR's table (source in the comment).
EXPECTED_datasecau_Reporting_Dashboard_Au=7   # NexusAI #216/#218 tables 2026-11-18: CodeQL, Analyze x3, audit-production-deps, build, scan
if [ -z "$MIN" ]; then
  V="EXPECTED_$(printf '%s' "$R" | tr '/-' '__')"
  MIN="${!V}"
  [ -n "$MIN" ] || { echo "REFUSED: no expected check count for $R; pass --min-checks N (count the names on the last merged PR's table)" >&2; exit 2; }
fi
case "$MIN" in ''|*[!0-9]*|0) echo "REFUSED: --min-checks must be a positive integer, got '$MIN'" >&2; exit 2 ;; esac
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START=$(date +%s)
while :; do
  HEAD=$(gh api "repos/$R/pulls/$N" --jq .head.sha 2>&1)
  [ "$HEAD" = "$SHA" ] || { echo "REFUSED: #$N head is $HEAD, not $SHA"; exit 3; }
  T=$(gh api "repos/$R/commits/$SHA/check-runs?per_page=100" 2>&1) || { echo "$(date +%H:%M:%S) read failed (UNKNOWN), retrying"; sleep "$I"; continue; }
  # newest instance of each check-run name only (a re-trigger leaves older completed runs beside the new ones)
  ROWS=$(printf '%s' "$T" | python3 -I "$HERE/pr_checks_newest.py")
  TOTAL=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -i -E '.')
  PEND=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -v -i -E '^completed')
  echo "$(date +%H:%M:%S) #$N checks $TOTAL of at least $MIN expected, pending $PEND"
  if [ "$TOTAL" -ge "$MIN" ] && [ "$PEND" -eq 0 ]; then
    printf '%s\n' "$ROWS"
    BAD=$(printf '%s\n' "$ROWS" | /usr/bin/grep -c -v -i -E '^completed	(success|neutral|skipped)	')
    [ "$BAD" -eq 0 ] || { echo "NOT GREEN: #$N $BAD check(s)"; exit 1; }
    MIXED=$(printf '%s' "$T" | python3 -I "$HERE/pr_checks_newest.py" --mixed)
    if [ -n "$MIXED" ]; then
      printf '%s\n' "$MIXED"
      [ "$ACCEPT" -eq 1 ] || { echo "NOT GREEN (MIXED): #$N an older run of a green check failed on this head; read both runs (or --accept-superseded for a deliberate re-trigger)"; exit 5; }
      echo "WARNING: superseded older failures accepted by --accept-superseded"
    fi
    echo "ALL GREEN: #$N $SHA ($TOTAL checks, at least $MIN expected)"; exit 0
  fi
  [ $(( $(date +%s) - START )) -ge $((MAX*60)) ] && { echo "GAVE UP after ${MAX} min ($TOTAL of at least $MIN checks); pending set:"; printf '%s\n' "$ROWS" | /usr/bin/grep -v -i -E '^completed'; exit 4; }
  sleep "$I"
done
