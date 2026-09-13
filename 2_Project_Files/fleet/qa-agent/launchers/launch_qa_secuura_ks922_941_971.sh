#!/bin/bash
# launch_qa_secuura_ks922_941_971.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #971 (KS-922 + KS-941) @ c229aa256: TWO CI-harness files, no product code.
#   KS-922  `Blockchain/Testing/ci/orchestrate.sh` — the Stage-1 JOIN's `"${stage1_pids[@]:-}"` expanded an
#           EMPTY array to one empty word on bash 3.2, so `wait ""` failed and the run logged "a Stage-1 job
#           exited non-zero" about a job that never existed; now the `+alternate` expansion (:119).
#   KS-941  `Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh` — a `[ -r ]` subject guard beside the
#           `[ -f ]` one (:54); a `skip()` helper + third counter; CELL 12/16/17 skip branches; the totals line
#           "N passed, M failed, K skipped" (:538); and, RULED Q1 (b) 2026-09-13 (STANDING_LINES rule 2), K > 0
#           exits 1 (:540). CELLS 14-17 new (13 -> 17 cells). This PR changes a CHECKER, so the brief carries a
#           LEGITIMATE-SHAPES table (BRIEF_TEMPLATE section 2a) and the gate drives it cell by cell.
#
# #971 was cut from develop M2 6696c6681 (its ONE parent); develop has since moved to M3 0f69129b3 (#932's
# squash, ONE file `startup-migrations.ts`, disjoint by name from #971's two files). So the compare merge-base is
# 6696c6681 (M2 IS an ancestor of M3 — no squash gap this time) and stays so while develop descends from M2;
# the launcher pins BOTH the merge-base (exit 10) AND develop (exit 18).
#
# The develop pin is DELIBERATELY strict: the brief's merged-tree ask is written against M3. If develop moves,
# this launcher REFUSES with exit 18 — the installer confirms the new develop delta is disjoint from the two
# files by name (`git diff --name-only 0f69129b3 <new> -- Blockchain/Testing Blockchain/Dev/scripts`) and
# re-pins DEVELOP_SHA in the launcher AND the brief's TARGET section AND the prompt; a deliberate edit.
#
# Adapted from launch_qa_secuura_ks1069_969.sh by gen_launcher_971.py (asserted substitutions, one asserted
# insertion, residual guard): same guards and exit codes, re-pointed at #971, plus exit 19 (the brief and the
# prompt must both name the head SHA — a prompt about another SHA is another gate).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks922_941_971.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA971_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-971-ks922-ks941-tier2.md}"
PROMPT_FILE="${QA971_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-971-ks922-ks941-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-922-ks-941-orchestrator-join-and-harness-guards'
HEAD_SHA="${QA971_HEAD:-c229aa25622a4a5e4ab19c6e586a04d2a8fdac28}"
MERGE_BASE='6696c6681196bb2bfcde09cb8916849f68dae219'
DEVELOP_SHA='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-971-ks922-ks941-tier2.md"

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
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 19; }
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
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA971_BRIEF:-}${QA971_PROMPT:-}${QA971_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
