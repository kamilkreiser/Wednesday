#!/bin/bash
# launch_qa_secuura_ks1052_972.sh — cross-project QA agent, TIER 1 (through code; no rendered surface, so
# the real-browser half of tier 1 does not apply) gate ROUND 1 on Secuura KS-1052 / PR #972 @ b3ce8c9e7,
# merge-base 0f69129b3 (= develop, the PR's own parent — #972 is a rebase of #930 onto develop).
#
# KS-1052: `updateUser` answers `User | null` and 21 of its 24 non-test callers discarded that answer;
# four of them then burned a single-use credential or told the user their password changed. #930
# (d491c72c1, round 1: NO GO — F-1 Blocker, the guard 503'd AFTER the write landed under fail-closed RLS;
# round 2 7e5ae31d8 scoped the read-back and was NEVER gated) went `dirty` against develop, so its two
# commits are cherry-picked here onto develop 0f69129b3 — d58c9d279 (= d491c72c1, patch-id identical),
# 8e454ecf4 (= 7e5ae31d8 with ONE conflict hunk in userRepo.ts resolved keep-both by hand), and the
# builder's own b3ce8c9e7 (the backup-code burn's cause-(a) cell). Three pre-auth credential flows change
# their failure-mode status and the burn site is a login door: tier 1 per the 2026-09-05 tiers.
# Adapted from launch_qa_secuura_ks1020_966.sh by gen_launcher_972.py (asserted substitutions + one
# asserted insertion + residual guard): same guards and exit codes, re-pointed at #972, plus exit 18.
#
# BOTH pins read 0f69129b3 on purpose and measure different things: MERGE_BASE is what the GitHub compare
# API answers for develop...head (it stays 0f69129b3 while develop moves, because the branch was cut
# there); DEVELOP_SHA is origin's develop by ls-remote and is DELIBERATELY strict — the brief's merged-tree
# and #970-overlap asks are written against develop 0f69129b3. If develop moves, this launcher REFUSES
# with exit 18; the installer confirms the new delta is disjoint by name from the nine files and re-pins
# DEVELOP_SHA here AND the brief's TARGET AND the prompt — a deliberate edit, never a silent one.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1052_972.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA972_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-972-ks1052-tier1.md}"
PROMPT_FILE="${QA972_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-972-ks1052-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1052-updateuser-credential-lifecycle-r2'
HEAD_SHA="${QA972_HEAD:-b3ce8c9e76e43644e4a6f325fbb281333a5bfd11}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-972-ks1052-tier1.md"

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
  echo "REFUSING: origin develop is not at $DEVELOP_SHA — the brief's merged-tree and #970-overlap asks are pinned to it; re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
  git -C "$REPO" ls-remote origin refs/heads/develop >&2
  exit 18
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
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
  echo "  origin develop still $DEVELOP_SHA (git ls-remote)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA972_BRIEF:-}${QA972_PROMPT:-}${QA972_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
