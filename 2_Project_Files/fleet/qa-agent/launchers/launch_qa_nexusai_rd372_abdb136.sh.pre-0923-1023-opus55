#!/bin/bash
# launch_qa_nexusai_rd372_abdb136.sh — cross-project QA agent, TIER 1 gate, round 1, on Datasec/NexusAI
# RD-372: branch rd-372-provisioning-load-silent-s55 @ abdb136 (1 commit on main cd2b543), built by S55 2026-09-12.
#
# PATTERN: launch_qa_nexusai_rd293_599058b.sh, with the tier, head, worktree and brief changed.
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD372' "bash '<this file>'"), NEVER nohup:
# the RD-293 gate's headless run exited at a turn that ended to wait (ledger 2026-09-12).
# Identity: exports NexusAI's OWN az/gh dirs (trap 8a); CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd372_abdb136.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..14 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd372-abdb136-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd372-abdb136-tier1.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-372-s55'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-abdb136f860048911fa79c54a7fbb78332b5ca0e}"
BASE_SHA='cd2b54397b0e83ccbd51e5b030c2ad614eb0e811'
EXPECTED_COMMITS=1

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$WT" ]          || { echo "worktree under test missing: $WT" >&2; exit 5; }

GOT="$(git --no-optional-locks -C "$WT" rev-parse HEAD 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: worktree HEAD is '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }
git --no-optional-locks -C "$WT" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }
N="$(git --no-optional-locks -C "$WT" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 9; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 10; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 11; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path and the head" >&2; exit 12; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 13; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  worktree HEAD == $HEAD_SHA; $BASE_SHA ancestor; range $EXPECTED_COMMITS commit"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 14; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
