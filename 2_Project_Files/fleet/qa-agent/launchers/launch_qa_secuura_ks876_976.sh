#!/bin/bash
# launch_qa_secuura_ks876_976.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #976 (KS-876 / KS-891 / KS-894 / KS-895) @ 0d5f5e6ab: packages/shared
# `ks860-test-listeners-bind-loopback.test.ts` — the test-listener guard (a CHECKER: source walk + comment-mask
# lexer + listen(0) site counter + desync announcement) now walks packages/ too with its own file excluded BY
# NAME (KS-876, the ruled shape), announces a re-synchronising mask desync via a recorded suspect line (KS-891),
# counts sites not rows through sitesOnly() (KS-894), and names the real desync cause (KS-895). ONE file,
# +269 -30, test-only; 14 -> 23 cells; the lexer's transitions and startsRegex are byte-identical to base.
#
# #976's parent IS develop 0f69129b3 (16:34:51 AEST 2026-09-13), so the GitHub compare merge-base and the
# develop pin are the SAME sha and the PR is fast-forward-shaped. This launcher pins both anyway (exit 10 for
# the merge-base via the compare API, exit 18 for origin develop via ls-remote): if develop moves, exit 18
# fires first and the installer confirms the new develop delta is disjoint BY NAME from this one file (the
# likely mover is #975's ks781-p3-3-body-parser-order.test.ts — disjoint; it flips the full-package ratio the
# brief quotes from 794/796 to 796/796) before re-pinning DEVELOP_SHA here AND in the brief's TARGET section
# and the prompt; that is a different brief, so it must be a deliberate edit.
#
# Adapted from launch_qa_secuura_ks1069_969.sh by gen_launcher_976.py (asserted substitutions, residual
# guard): same guards and exit codes, re-pointed at #976.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks876_976.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA976_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-976-ks876-891-894-895-tier2.md}"
PROMPT_FILE="${QA976_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-976-ks876-891-894-895-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-876-ks-891-ks-894-ks-895-listener-guard-walk-and-mask'
HEAD_SHA="${QA976_HEAD:-0d5f5e6ab7a9162b84dba7d375260af35ebdde81}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-976-ks876-891-894-895-tier2.md"

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
  echo "REFUSING: origin develop is not at $DEVELOP_SHA (the PR's parent) — the brief's fast-forward ask and its 794/796 ratio are pinned to it; confirm the new develop delta is disjoint by name from packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
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
  echo "  origin develop still $DEVELOP_SHA (= the PR's parent and merge-base; git ls-remote)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA976_BRIEF:-}${QA976_PROMPT:-}${QA976_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
