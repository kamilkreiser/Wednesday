#!/bin/bash
# launch_qa_hpsm_composer_09c1591_combined.sh — cross-project QA agent, TIER 1, COMBINED gate round 1, split into
# THREE parallel gates on disjoint verdict areas (Kam's standing agents rule, 2026-09-13 09:17:37):
#   A engine+content · B api+db · C web+renderers — on the Datasec/HPSM Policy Composer local main @ 09c1591, NOT pushed.
# PATTERN: launch_qa_hpsm_composer_1a6b68d_wp4_wp5.sh (reachable-from-main head guard, report-dir and port guards),
# parameterised by gate letter so the three sessions cannot share a stack, port or report.
# LAUNCH EACH IN ITS OWN TMUX PANE (cockpit.sh add 'QA/HPSM-C-A' "bash '<this file>' A"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_hpsm_composer_09c1591_combined.sh <A|B|C> [--check]
# Exit: 0 launched (or guards passed under --check) · 2..20 a guard refused
set -u

GATE="${1:-}"
case "$GATE" in
  A) SLUG='a-engine-content'; PORT=21080; CI_PORT=21095 ;;
  B) SLUG='b-api-db';         PORT=21180; CI_PORT=21195 ;;
  C) SLUG='c-web-renderers';  PORT=21280; CI_PORT=21295 ;;
  *) echo "usage: $0 <A|B|C> [--check]" >&2; exit 2 ;;
esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1-$GATE.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer'
SOW='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md'
REPORT_DIR="/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-09c1591-combined-$SLUG-tier1"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials}"
BRANCH='refs/heads/main'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-09c15918fadfee8a9bd590a1282113637f44515d}"
BASE_SHA='afc10e98c51505be1f1943335370cf2de3b47d44'
FOCUS_SHA='1a6b68d793b60dbbfa227f35464725790714f42b'
EXPECTED_COMMITS=249

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }
git --no-optional-locks -C "$REPO" rev-parse --verify "${HEAD_SHA}^{commit}" >/dev/null 2>&1 || {
  echo "REFUSING: $HEAD_SHA is not a commit in $REPO" >&2; exit 6; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$HEAD_SHA" "$BRANCH" 2>/dev/null || {
  echo "REFUSING: $HEAD_SHA is not reachable from $BRANCH — main was rewritten; re-brief" >&2; exit 18; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA" >&2; exit 7; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$FOCUS_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: focus base $FOCUS_SHA is not an ancestor of $HEAD_SHA" >&2; exit 7; }
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
grep -qF "You are GATE $GATE" "$PROMPT_FILE" || { echo "REFUSING: prompt is not the GATE $GATE prompt" >&2; exit 20; }
grep -qF "GATE $GATE:" "$BRIEF" || { echo "REFUSING: brief has no GATE $GATE section" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
for p in "$PORT" "$CI_PORT"; do
  lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1 && { echo "REFUSING: port $p already has a listener" >&2; exit 17; }
done

if [ "${2:-}" = "--check" ]; then
  echo "GATE $GATE all guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base + focus ancestors; range $EXPECTED_COMMITS; SOW; docker; report dir absent; ports $PORT/$CI_PORT free; identity dirs; tier/prompt/head/gate/mail; no placeholder"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
