#!/bin/bash
# launch_qa_hpsm_composer_1a6b68d_wp3r2.sh — cross-project QA agent, TIER 1 gate, ROUND 2 of 2 under the cap,
# on the Datasec/HPSM Policy Composer WP3 rules engine: local main @ 1a6b68d (range 0523193..1a6b68d), NOT pushed.
# PATTERN: launch_qa_hpsm_composer_0523193_wp3.sh (reachable-from-main head guard, report-dir and port guards).
# LAUNCH IN A TMUX PANE (cockpit.sh add 'QA/HPSM-WP3R2' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_hpsm_composer_1a6b68d_wp3r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-1a6b68d-wp3-tier1r2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-1a6b68d-wp3-tier1r2.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer'
SOW='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md'
REPORT_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-1a6b68d-wp3-tier1r2'
PRIOR_REPORT='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials}"
BRANCH='refs/heads/main'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-1a6b68d793b60dbbfa227f35464725790714f42b}"
BASE_SHA='052319342974fc05aabdf056da73558182b871f0'
EXPECTED_COMMITS=61
PORT=18980

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }
[ -s "$PRIOR_REPORT" ] || { echo "REFUSING: prior-round report missing: $PRIOR_REPORT" >&2; exit 5; }
git --no-optional-locks -C "$REPO" rev-parse --verify "${HEAD_SHA}^{commit}" >/dev/null 2>&1 || {
  echo "REFUSING: $HEAD_SHA is not a commit in $REPO" >&2; exit 6; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$HEAD_SHA" "$BRANCH" 2>/dev/null || {
  echo "REFUSING: $HEAD_SHA is not reachable from $BRANCH — main was rewritten; re-brief" >&2; exit 18; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA" >&2; exit 7; }
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }
[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW" >&2; exit 9; }
docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding" >&2; exit 10; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: HPSM identity dirs missing under $ID_ROOT — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 14; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || { echo "REFUSING: brief or prompt does not name the head" >&2; exit 15; }
grep -qF "$PRIOR_REPORT" "$BRIEF" || { echo "REFUSING: brief does not point at the prior-round report" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1 && { echo "REFUSING: port $PORT already has a listener" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base 0523193 ancestor; range $EXPECTED_COMMITS; prior report present; SOW; docker; report dir absent; port $PORT free; identity dirs; tier/prompt/head/mail; no placeholder"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
