#!/bin/bash
# launch_qa_nexusai_rd372_a3d15b8.sh — cross-project QA agent, TIER 1 gate, ROUND 2 of 2, on Datasec/NexusAI
# RD-372: branch rd-372-r2-s57 @ a3d15b8 (2 commits on main ae2588b: abdb136 cherry-picked, then the round-2 fix),
# built by S57 2026-09-12.
#
# PATTERN: launch_qa_nexusai_rd372_abdb136.sh (round 1), with the head, base, count, worktree and brief changed,
# plus a guard that the brief names round 1's report (a round-N brief names N-1's).
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD372-R2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd372_a3d15b8.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..15 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd372-a3d15b8-tier1r2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd372-a3d15b8-tier1r2.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-372-r2-s57'
R1='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd372-abdb136-tier1'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-a3d15b88f08fde634ccac132677152c8521ecf97}"
BASE_SHA='ae2588bfd60a1f9f22130aa794378382e3aab629'
EXPECTED_COMMITS=2

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

[ -s "$R1/report.md" ] || { echo "REFUSING: round-1 report missing at $R1/report.md" >&2; exit 9; }
grep -qF "$R1" "$BRIEF" || { echo "REFUSING: brief does not name round 1's report path" >&2; exit 10; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path and the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 15; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  worktree HEAD == $HEAD_SHA; $BASE_SHA ancestor; range $EXPECTED_COMMITS commits"
  echo "  round-1 report present and named in the brief"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
