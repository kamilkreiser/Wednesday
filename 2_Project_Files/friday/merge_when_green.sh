#!/bin/bash
# merge_when_green.sh <owner/repo> <pr-number> <head-sha> [max-minutes]
# Friday's ONE way to merge a Datasec PR (ledger w=2, 2026-10-01: two hand-rolled loops misread GitHub state in one
# morning — one printed "merged" after a refused merge, one merged while a CodeQL leg was still in progress because an
# EMPTY conclusion was not recognised as pending).
# Rules it enforces:
#   1. the PR head must equal <head-sha> (the tested head), else STOP (rc 3);
#   2. EVERY check-run on that head must have status == completed (never inferred from a conclusion string);
#   3. every completed conclusion must be success / neutral / skipped, else STOP (rc 4);
#   4. merge with --squash --match-head-commit; then read `state` back: MERGED or it failed (rc 5).
#   5. (2026-10-04, PR HPSM-POC #94) a CodeQL run (named CodeQL or Analyze (…)) must be PRESENT on the head: the Datasec
#      org ruleset requires it, and a PR whose CodeQL never started showed 5/5 green and was refused by the branch policy.
#      Absent at the timeout = rc 7. Repos without CodeQL: MWG_REQUIRE_CODEQL=0.
#   6. only the LATEST check-run per name counts (a re-run's success supersedes its cancelled predecessor).
# Prints the new base-branch sha on success. Never uses --admin or --auto.
set -u
REPO="${1:?owner/repo}"; PR="${2:?pr number}"; HEAD="${3:?head sha}"; MAX="${4:-40}"
FA="$(cd "$(dirname "$0")" && pwd)/friday_as.sh"
gh_() { bash "$FA" datasec gh "$@"; }
for ((i=0; i<MAX*2; i++)); do
  cur=$(gh_ pr view "$PR" -R "$REPO" --json headRefOid --jq .headRefOid 2>&1) || { echo "merge_when_green: cannot read PR: $cur" >&2; exit 2; }
  [ "$cur" = "$HEAD" ] || { echo "merge_when_green: STOP — PR #$PR head is $cur, not the tested $HEAD" >&2; exit 3; }
  runs=$(gh_ api "repos/$REPO/commits/$HEAD/check-runs?per_page=100" --jq '[.check_runs[] | {n:.name, s:.status, c:(.conclusion // ""), id:.id}]' 2>&1) || { echo "merge_when_green: cannot read checks: $runs" >&2; exit 2; }
  # Rule 6 (2026-10-04, HPSM-POC #95): a re-run leaves the OLD check-run on the same head; GitHub's required checks read the
  # LATEST run per name, so this does too (highest id per name). Without it a cancelled-then-passed check stops the merge forever.
  runs=$(echo "$runs" | python3 -c 'import sys,json;r=json.load(sys.stdin);b={};[b.__setitem__(x["n"],x) for x in sorted(r,key=lambda x:x["id"])];print(json.dumps(list(b.values())))')
  total=$(echo "$runs" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)))')
  pending=$(echo "$runs" | python3 -c 'import sys,json;print(sum(1 for r in json.load(sys.stdin) if r["s"]!="completed"))')
  codeql=$(echo "$runs" | python3 -c 'import sys,json;print(sum(1 for r in json.load(sys.stdin) if r["n"]=="CodeQL" or r["n"].startswith("Analyze")))')
  bad=$(echo "$runs" | python3 -c 'import sys,json;print(",".join(r["n"]+"="+r["c"] for r in json.load(sys.stdin) if r["s"]=="completed" and r["c"] not in ("success","neutral","skipped")))')
  if [ -n "$bad" ]; then echo "merge_when_green: STOP — failing checks on $HEAD: $bad" >&2; exit 4; fi
  if [ "$total" -gt 0 ] && [ "$pending" -eq 0 ] && { [ "${MWG_REQUIRE_CODEQL:-1}" = 0 ] || [ "$codeql" -gt 0 ]; }; then
    out=$(gh_ pr merge "$PR" -R "$REPO" --squash --match-head-commit "$HEAD" 2>&1); rc=$?
    st=$(gh_ pr view "$PR" -R "$REPO" --json state,mergeCommit --jq '.state+" "+(.mergeCommit.oid // "")' 2>&1)
    case "$st" in MERGED*) echo "merged PR #$PR ($REPO) head $HEAD → ${st#MERGED }; checks: $total completed"; exit 0;;
      *) echo "merge_when_green: merge did NOT happen (rc=$rc, state=$st): $out" >&2; exit 5;; esac
  fi
  sleep 30
done
if [ "${MWG_REQUIRE_CODEQL:-1}" != 0 ] && [ "${codeql:-0}" -eq 0 ] && [ "${pending:-1}" -eq 0 ]; then
  echo "merge_when_green: STOP — no CodeQL/Analyze run ever appeared on $HEAD after $MAX min ($total other checks green); push a fresh commit or re-run code scanning" >&2; exit 7; fi
echo "merge_when_green: timeout after $MAX min — total=$total pending=$pending codeql=${codeql:-0}" >&2; exit 6
