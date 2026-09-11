#!/bin/bash
# launch_qa_hpsm_composer_afc10e9.sh — cross-project QA agent, TIER 1 gate, round 4 (Kam-authorised,
# beyond the two-NO-GO cap), on the Datasec/HPSM Policy Composer: local repo main @ afc10e9,
# 2 commits on 55160dd (3cd27d0 tests, afc10e9 migration 0006), NOT pushed. Built by HPSM session 38.
#
# PATTERN: launch_qa_hpsm_composer_55160dd.sh (the SOW and docker guards) merged with
# launch_qa_nexusai_rd372_abdb136.sh (range + ancestor guards, the project's OWN az/gh identity dirs
# so the tester never inherits Tuesday's, CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store).
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/HPSM-R4' "bash '<this file>'"), NEVER nohup:
# a headless gate exits at a turn that ends to wait (ledger 2026-09-12).
# The tester CLONES the repo into its own mktemp -d, so the builder's working tree is irrelevant
# (a builder seat is live there, holding for this verdict).
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_hpsm_composer_afc10e9.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..16 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_hpsm-composer-afc10e9-tier1r4.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_hpsm-composer-afc10e9-tier1r4.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer'
SOW='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials}"
BRANCH='refs/heads/main'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-afc10e98c51505be1f1943335370cf2de3b47d44}"
BASE_SHA='55160dd2cec6ae5eed5a040405e6abf2d2a375aa'
EXPECTED_COMMITS=2

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }

# The brief describes exactly this head. A builder commit after the brief was written means the
# brief describes a tree nobody is gating: refuse and re-brief rather than gate a guess.
GOT="$(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: $BRANCH is at '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }

[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW — CI's citation leg cannot run" >&2; exit 9; }

# The core measurements run containers. Without a daemon the agent would substitute a source read
# for them, which is the substitution this gate exists to stop.
docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — the stack and the database tests cannot run" >&2; exit 10; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: HPSM identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 14; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: brief or prompt does not name the head $HEAD_SHA" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to —" >&2
  echo "the agent has no inbox, and a Datasec verdict mailed to the Secuura seat is a cross-client leak" >&2
  exit 16; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $BRANCH == $HEAD_SHA (local); $BASE_SHA ancestor; range $EXPECTED_COMMITS commits"
  echo "  E8 SOW text present; docker responding"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
