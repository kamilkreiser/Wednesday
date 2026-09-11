#!/bin/bash
# launch_qa_secuura_ks1086_953_round2.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 2
# on Secuura KS-1086 / PR #953 @ 8987b8a0e (parent de1ab62c0), merge-base develop 2d864ae92.
#
# Round 1 (launch_qa_secuura_ks1086_953.sh) returned GO WITH FINDINGS on de1ab62c0 — the fix
# ESTABLISHED. Round 2 gates the builder's delta closing QA-1 (cells) and QA-2 (refusal on zero
# parsed names / no GIT_DIR), with a mandatory NO-FALSE-REFUSAL leg and a bash 3.2 check.
#
# Guards = round 1's, plus the round-N template rule: the prompt must name round 1's report path
# (the QA agent has no inbox, so a carry-forward with no pointer is unanswerable), and that report
# must still be on disk.
#
# Written with the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1086_953_round2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..17 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-953-ks1086-tier2-round2.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-953-ks1086-tier2-round2.prompt.txt"
ROUND1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-de1ab62c0-tier1/report.md'
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1086-preflight-leg-14-runs-the-shell-suites-under-the-hooks-git'
HEAD_SHA='8987b8a0ecfae29aed2b934188d947a1a6a581df'
MERGE_BASE='2d864ae9220c57ddcd8dc77af1b80fbd8001d530'

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$ROUND1_REPORT" ]  || { echo "round-1 report missing: $ROUND1_REPORT" >&2; exit 14; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$ROUND1_REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name round 1's report path — the agent has no inbox to ask" >&2; exit 17; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  brief, prompt, round-1 report, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 2"
  echo "  prompt opens with the thinking directive, names the brief AND round 1's report"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
