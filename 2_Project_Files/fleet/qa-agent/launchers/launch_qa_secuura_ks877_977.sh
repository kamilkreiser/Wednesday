#!/bin/bash
# launch_qa_secuura_ks877_977.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #977 (KS-877 + KS-922's two comment items) @ a70585823: ONE build script + ONE NEW shell suite,
# no product code.
#   KS-877  `Blockchain/Dev/scripts/docker-build.sh` — with an EMPTY SERVICES_TABLE the `[ -n ]` guard left
#           BUILD_LIST genuinely empty and the banner's `${BUILD_LIST[*]}` (:162 at base) died with
#           `BUILD_LIST[*]: unbound variable` under bash 3.2 + `set -u`. The ticket's FIRST option
#           (`${BUILD_LIST[*]:-}`) was tried and only moves the death 55 lines down to the parallel loop's
#           `"${BUILD_LIST[@]}"` (:217 at base); the SECOND option shipped: a guard on `${#BUILD_LIST[@]}`
#           right after the target list is resolved (:159-162 at head), printing `ERROR: no services matched
#           — SERVICES_TABLE is empty or unparseable (0 rows); nothing to build` to stderr, exit 1.
#   KS-922  its two COMMENT items on this file's re-index note (:238-239 at base, :252-261 at head): the
#           sentence calling the `:-` idiom "correct for a `for` loop" (it is not) and the stale
#           `orchestrate.sh:47` pointer (a blank line) — now cites the symbols stage1_pids / stage2_pids and
#           names the form that is right in both places. KS-922's OWN fix (the Stage-1 JOIN) is a sibling PR,
#           gated separately; KS-922 carries both PRs on purpose.
#   NEW     `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (3 cells; docker a recording
#           stub on a private PATH; the emptied fixture copy's row count asserted 29 -> 0 before scoring).
# This PR changes a JOB SCRIPT that refuses inputs, so the brief carries a LEGITIMATE-SHAPES table
# (BRIEF_TEMPLATE section 2a) and the gate drives it cell by cell; the gate re-derives BOTH the dead option and
# the shipped guard under bash 3.2 with cells-run quoted.
#
# #977 was cut from develop M3 0f69129b3 (its ONE parent) and develop is STILL M3, so the compare merge-base
# IS develop (ahead 1 / behind 0) and a merge today is a fast-forward. The launcher pins BOTH the merge-base
# (exit 10) AND develop (exit 18). If the merge seat squashes another PR onto develop first (service files,
# disjoint from scripts/), the merge-base stays M3 (M3 is then an ancestor) and ONLY the develop guard fires.
#
# The develop pin is DELIBERATELY strict: the brief's merged-tree ask is written against M3. If develop moves,
# this launcher REFUSES with exit 18 — the installer confirms the new develop delta is disjoint from the two
# files by name (`git diff --name-only 0f69129b3 <new> -- Blockchain/Dev/scripts`) and re-pins DEVELOP_SHA in
# the launcher AND the brief's TARGET section AND the prompt; a deliberate edit.
#
# Adapted from launch_qa_secuura_ks922_941_971.sh by gen_launcher_977.py (asserted substitutions, residual
# guard): same guards and exit codes (2..19, incl. exit 19: the brief and the prompt must both name the head
# SHA — a prompt about another SHA is another gate), re-pointed at #977.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks877_977.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA977_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2.md}"
PROMPT_FILE="${QA977_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-877-docker-build-empty-table-guard'
HEAD_SHA="${QA977_HEAD:-a70585823221d30b0b86684dbc0fb78b0efee784}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='506cd3a3349ddad0c614e052de63d3fa63e523e7'  # re-pinned 2026-09-13 16:59 AEST by Wednesday: develop moved to M7 (#969's squash, 3 api-gateway files, disjoint from scripts/ — git diff --name-only measured); the merge-base stays M3
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2.md"

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

[ -z "${QA977_BRIEF:-}${QA977_PROMPT:-}${QA977_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
