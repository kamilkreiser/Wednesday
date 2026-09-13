#!/bin/bash
# launch_qa_secuura_ks1069_969.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #969 (KS-1069) @ fb23ca6aa: api-gateway `src/routes/verification.ts` — `persistedAnchored`
# validates the SHAPE of its three inputs (placeholder txHash refused; height must be a positive integer,
# strict — a numeric string is a shape defect, RULED; any truthy `simulated` is a declaration).
#
# #969 was cut on top of the branch head beneath it; the two PRs beneath it have since SQUASH-MERGED into
# develop as M1 163ca2c74 and M2 6696c6681, and #932 followed as M3 0f69129b3 (develop at 15:49 AEST 2026-09-13,
# having moved from M2 at 15:34:38 while this set was built — the pin below tripped on its own green run). So #969's parent commit is
# NOT an ancestor of develop, the GitHub compare merge-base is still 721b333a6 (where all three branches
# left develop — the compare API and `git merge-base` agree), and GitHub's file list for #969 is 5 files
# against that stale base while its TRUE delta is 3 files (`git diff <parent> fb23ca6aa`). The brief
# explains all three numbers; the launcher pins BOTH the merge-base (exit 10) AND develop (exit 18).
#
# The develop pin is DELIBERATELY strict: the brief's merged-tree ask (item 7) is written against M3. If
# develop moves (e.g. another seat's squash lands first), this launcher REFUSES with exit 18 — the installer
# then confirms the new develop delta is disjoint from the three files by name and re-pins DEVELOP_SHA in
# the launcher AND the brief's TARGET section; that is a different brief, so it must be a deliberate edit.
#
# Adapted from launch_qa_secuura_ks1071_1070_967_968.sh by gen_launcher_969.py (asserted substitutions,
# one asserted insertion, residual guard): same guards and exit codes, re-pointed at #969, plus exit 18.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1069_969.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA969_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-969-ks1069-tier2.md}"
PROMPT_FILE="${QA969_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-969-ks1069-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1069-gateway-verifys-persistedanchored-trusts-the-shape-of-its'
HEAD_SHA="${QA969_HEAD:-fb23ca6aa1661119beaeb5f45fb41dd006356f74}"
MERGE_BASE='721b333a6a58d7b45fd59946b8561432bf55d01a'
DEVELOP_SHA='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-969-ks1069-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

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

if ! git -C "$REPO" ls-remote origin refs/heads/develop | grep -q "^${DEVELOP_SHA}[[:space:]]"; then
  echo "REFUSING: origin develop is not at $DEVELOP_SHA (M3) — the brief's merged-tree ask is pinned to M3; re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
  git -C "$REPO" ls-remote origin refs/heads/develop >&2
  exit 18
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  origin develop still $DEVELOP_SHA (M3; git ls-remote)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA969_BRIEF:-}${QA969_PROMPT:-}${QA969_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
