#!/bin/bash
# launch_qa_nexusai_rd342_rd382_tier2.sh — cross-project QA agent, TWO TIER 2 gates (round 1 each) in ONE session, on Datasec/NexusAI
# RD-342: rd-342-s57 @ c43214e (1 commit on main 34e7fc4, built by S57).
# RD-382: rd-382-jira-site-scheme-s55 @ d4d3bfb (1 commit on ae2588b, built by S55).
# Batched for capacity (7-day allowance 88% at 11:56 AEST); precedent 2026-09-06: one tester session, two verdicts.
#
# PATTERN: launch_qa_nexusai_rd372_a3d15b8.sh, with two worktrees / heads / bases, TIER 2, and guards that
# the brief names BOTH report paths, that neither report exists yet, and that the prompt names BOTH heads
# and BOTH verdict subjects.
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD342-382' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd342_rd382_tier2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..17 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd342-c43214e-rd382-d4d3bfb-tier2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd342-c43214e-rd382-d4d3bfb-tier2.prompt.txt"
REPORTS="$QA_DIR/projects/nexusai/reports"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

H342="${QA_HEAD342_OVERRIDE:-c43214ed0b72e447688578e42bb4a39bb557bce6}"
B342='34e7fc4eacb3a80425a2f3cdd993addf28050dad'
H382="${QA_HEAD382_OVERRIDE:-d4d3bfbf46211d93159a13d5b2e8510f11e6c425}"
B382='ae2588bfd60a1f9f22130aa794378382e3aab629'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }

# check_wt <name> <worktree> <head> <base> <expected commits>
check_wt() {
  local name="$1" wt="$2" head="$3" base="$4" n_exp="$5" got n
  [ -d "$wt" ] || { echo "REFUSING $name: worktree under test missing: $wt" >&2; return 5; }
  got="$(git --no-optional-locks -C "$wt" rev-parse HEAD 2>&1)"
  [ "$got" = "$head" ] || { echo "REFUSING $name: worktree HEAD is '$got', not $head — the brief is stale" >&2; return 6; }
  git --no-optional-locks -C "$wt" merge-base --is-ancestor "$base" "$head" || {
    echo "REFUSING $name: $base is not an ancestor of $head — the base in the brief is wrong" >&2; return 7; }
  n="$(git --no-optional-locks -C "$wt" rev-list --count "${base}..${head}" 2>&1)"
  [ "$n" = "$n_exp" ] || { echo "REFUSING $name: expected $n_exp commits in range, found '$n'" >&2; return 8; }
  grep -qF "$head" "$BRIEF" && grep -qF "$head" "$PROMPT_FILE" || {
    echo "REFUSING $name: brief and prompt must both name head $head" >&2; return 9; }
  return 0
}
check_wt RD-342 "$NX/worktrees/rd-342-s57" "$H342" "$B342" 1 || exit $?
check_wt RD-382 "$NX/worktrees/rd-382-s55" "$H382" "$B382" 1 || exit $?

for R in "2026-09-12-rd342-c43214e-tier2" "2026-09-12-rd382-d4d3bfb-tier2"; do
  grep -qF "$REPORTS/$R/report.md" "$BRIEF" || { echo "REFUSING: brief does not name report path $REPORTS/$R/report.md" >&2; exit 10; }
  [ ! -e "$REPORTS/$R/report.md" ] || { echo "REFUSING: $REPORTS/$R/report.md already exists — a stale report would read as this gate's" >&2; exit 17; }
done

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 14; }
S342='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-342 @ c43214e (tier 2)'
S382='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-382 @ d4d3bfb (tier 2)'
grep -q 'MAIL EACH VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$S342" "$PROMPT_FILE" && grep -qF "$S382" "$PROMPT_FILE" \
  && grep -qF "$S342" "$BRIEF" && grep -qF "$S382" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL EACH VERDICT, name tuesday-agent@agentmail.to, and both prompt and brief must carry both verdict subjects" >&2; exit 15; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  RD-342: worktree HEAD == $H342; $B342 ancestor; range 1 commit"
  echo "  RD-382: worktree HEAD == $H382; $B382 ancestor; range 1 commit"
  echo "  both report paths named in the brief; neither report exists yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, both heads, MAIL EACH VERDICT, tuesday-agent@, both subjects"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
