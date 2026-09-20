#!/bin/bash
# launch_qa_nexusai_rd518_6ea15a0.sh — cross-project QA agent, TIER 1 gate, ROUND 1 of 2, on
# Datasec/NexusAI RD-518: branch rd-518-kv-identity-s72 @ 6ea15a0 (1 commit on main 34ad321, by S72).
#
# PATTERN: launch_qa_nexusai_rd464_r3_60c76d7.sh (tonight), with TWO deliberate differences:
#   - NO PINNED WORKTREE. Nothing holds 6ea15a0 on disk, and the r3 gate's own pattern was to make a
#     scratch worktree at the sha. So the worktree-HEAD guard (exit 6) is REPLACED by an object-store
#     guard: the sha must be a commit reachable in the repo, and must be at its branch on ORIGIN.
#     A guard that demands a worktree nobody created would refuse a legitimate launch.
#   - The repo's working checkout is at cd2b543, NOT origin/main. Nothing here reads HEAD.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD518' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# Usage: launch_qa_nexusai_rd518_6ea15a0.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_nexusai-rd518-6ea15a0-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_nexusai-rd518-6ea15a0-tier1.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-20-rd518-6ea15a0-tier1/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-6ea15a061992e49d9c6f3e07ddcbc8ecb538c092}"
BASE_SHA='34ad321ee18401c1f965244e5c4e06438aae01d0'
BRANCH='rd-518-kv-identity-s72'
EXPECTED_COMMITS=1
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-518 @ 6ea15a0 (tier 1)'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The sha must be a real commit in the object store — the gate builds its own worktree from it.
T="$(git --no-optional-locks -C "$REPO" cat-file -t "$HEAD_SHA" 2>&1)"
[ "$T" = "commit" ] || { echo "REFUSING: $HEAD_SHA is not a commit in $REPO (got '$T') — the gate could not check it out" >&2; exit 6; }

git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }

N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commit in range, found '$N'" >&2; exit 8; }

# The head must be AT ORIGIN on its branch — a verdict is only reachable later if the sha is remote.
LSR="$(git --no-optional-locks -C "$REPO" ls-remote origin "$BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: $HEAD_SHA is not at refs/heads/$BRANCH on origin — that head moved or was never pushed" >&2
  printf '%s\n' "$LSR" >&2; exit 18; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config)" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: prompt must name the brief path and the head, and the brief must name the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@; prompt and brief must carry the verdict subject" >&2; exit 15; }
# The two must-measures are the reason this gate exists: refuse if either is missing from the prompt.
grep -q 'M-A' "$PROMPT_FILE" && grep -q 'M-B' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must carry BOTH must-measures M-A and M-B by name" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $HEAD_SHA is a commit in the object store; $BASE_SHA ancestor; range $EXPECTED_COMMITS commit"
  echo "  head is at refs/heads/$BRANCH on origin"
  echo "  report path named in the brief; report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@, subject, M-A, M-B"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
