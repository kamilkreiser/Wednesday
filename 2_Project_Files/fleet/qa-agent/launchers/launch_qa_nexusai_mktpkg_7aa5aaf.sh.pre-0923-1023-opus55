#!/bin/bash
# launch_qa_nexusai_mktpkg_7aa5aaf.sh — cross-project QA agent, TIER 1 gate, ROUND 4 (Kam-authorised,
# beyond the cap), on the Datasec/NexusAI Marketplace package: branch s51-marketplace-remediation @ 7aa5aaf
# (range b8c4646..7aa5aaf, 10 commits, on origin) AND the DRAFT submission zips S56 built from it.
# Kam uploads the package himself; this verdict decides whether it reaches him as ready.
#
# PATTERN: launch_qa_nexusai_mktpkg_b8c4646.sh (round 3). Differences, each deliberate:
#   - new head/base/count and the S56 package folder;
#   - the brief must name ROUND 3's report path (a round-N brief names N-1's);
#   - exports NexusAI's OWN az/gh dirs and pins CLAUDE_CONFIG_DIR, as launch_qa_nexusai_rd372_abdb136.sh does,
#     so the tester never inherits Tuesday's identity state.
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-MKT-R4' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_mktpkg_7aa5aaf.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-mktpkg-7aa5aaf-tier1r4.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-mktpkg-7aa5aaf-tier1r4.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed'
PKG='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s56-marketplace-package/DRAFT-submission-package-7aa5aaf'
R3='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-b8c4646-tier1r3'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
BRANCH='refs/heads/s51-marketplace-remediation'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-7aa5aaf646b9c89cffde6180f3adc7cfd1a2a203}"
BASE_SHA='b8c4646ab7d271567364876757403bfb8d23cf08'
EXPECTED_COMMITS=10

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$WT" ]          || { echo "worktree under test missing: $WT" >&2; exit 5; }

GOT="$(git --no-optional-locks -C "$WT" rev-parse "$BRANCH" 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: $BRANCH is at '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }
git --no-optional-locks -C "$WT" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }
N="$(git --no-optional-locks -C "$WT" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }

for f in "DRAFT-pending-regate_plan-managed-ai_7aa5aaf.zip" "DRAFT-pending-regate_listing-assets_7aa5aaf.zip" "MANIFEST.txt"; do
  [ -s "$PKG/$f" ] || { echo "REFUSING: DRAFT package file missing or empty: $PKG/$f" >&2; exit 9; }
done
[ -s "$R3/report.md" ] || { echo "REFUSING: round-3 report missing at $R3/report.md" >&2; exit 10; }
grep -qF "$R3" "$BRIEF" || { echo "REFUSING: brief does not name round 3's report path" >&2; exit 11; }

docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — the container checks cannot run" >&2; exit 12; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 13; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 14; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 15; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 16; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: brief or prompt does not name the head $HEAD_SHA" >&2; exit 17; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 18; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $BRANCH == $HEAD_SHA; $BASE_SHA ancestor; range $EXPECTED_COMMITS commits"
  echo "  DRAFT package: both zips + MANIFEST present; round-3 report present and named in the brief"
  echo "  docker responding"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 19; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
