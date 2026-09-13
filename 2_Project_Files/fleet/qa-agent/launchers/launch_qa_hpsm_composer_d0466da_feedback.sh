#!/bin/bash
# launch_qa_hpsm_composer_d0466da_feedback.sh — cross-project QA agent, TIER 1, FEATURE-SCOPED gate, round 1:
#   the FEEDBACK feature (F-API + feedback root + edge row + G9 probes + F-WEB) of the Datasec/HPSM Policy Composer, LOCAL ONLY,
#   two verdicts (DELIVERABLES, SECURITY), on local main @ GATE_HEAD below, NOT pushed, NOT live.
# Tuesday s14, 2026-09-13 (briefs_staged/2026-09-13_hpsm-s45-answer-feedback-gate-before-live.md L1): a FEEDBACK-scoped tier-1 gate NOW,
#   local only, on d0466da, ports 21480-21599, first claim on the docker lock. The LIVE feedback upgrade waits for its verdict.
# Deliverables oracle, Kam, terminal 2026-09-13 16:53:31 AEST: "...add the feedback feature as deployed in Nexus AI to the HPSM project.
#   Naturally change all settings so that any feedback is registered against HPSM and works properly."
# PATTERN: launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh, line for line, with the ONE-head-pin pattern of
#   launch_qa_hpsm_composer_live_delta_after_gate_fix.sh. CHANGED: (1) GATE_HEAD is the ONE head pin, at the top; HEAD7 / REPORT_DIR /
#   SUBJECT derive from it; the prompt carries @GATE_HEAD@ / @GATE_HEAD7@ placeholders this launcher renders, and every prompt guard
#   reads the RENDERED text. The BRIEF stays pinned: it must name the head, the report path and the subject literally, so a re-point
#   without a re-brief REFUSES (exit 15/16/17) — a feature gate on another head is a new brief, not a new pin;
#   (2) Kam's live-demo ruling guard DROPPED: a LOCAL-ONLY gate touches no live site, so it needs no live ruling. Exit 10 is now
#   docker + the LOCAL-ONLY scope guard (both files say LOCAL ONLY; neither names the live host or a port of another seat's stack);
#   (3) feature-base guard: FEATURE_BASE (9b8ea76, where the upgrade path starts) is an ancestor, and 0016 is absent there and present
#   at the head (exit 9); (4) REFS re-pointed to what this brief cites; ARCH_FILES dropped (the S45 README and M16 report are REFS);
#   (5) the docker-lock path must be named in both; the named ports must lie inside 21480-21599;
#   (6) every QA_*_OVERRIDE refuses a real launch, not only the brief/prompt pair.
# INSTALL (Tuesday, after review): brief -> $BRIEF_FINAL, prompt -> $PROMPT_FINAL, this file -> fleet/qa-agent/launchers/.
# LAUNCH IN ITS OWN TMUX PANE (cockpit.sh add 'QA/HPSM-feedback' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd`.
# Usage: launch_qa_hpsm_composer_d0466da_feedback.sh [--check]
# Exit: 0 launched (or every guard passed under --check) · 2..22 a guard refused (10 = docker or the LOCAL-ONLY scope)
set -u

# ==== HEAD PIN ====================================================================================================================
GATE_HEAD='d0466daaa7f2ae30b2da8f8fd537e95250da0aa8'  # S45 READY FOR QA 2026-09-13T13:40:24Z (qa-s45/feedback-ready/README.md L4)
# git --no-optional-locks -C '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' rev-list --count afc10e98c51505be1f1943335370cf2de3b47d44..d0466da
EXPECTED_COMMITS=342           # measured by the drafter 2026-09-13T13:43Z
# git --no-optional-locks -C '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' rev-list --count 9b8ea76c073cefab0319d2bec7b5a82c54b4e9d1..d0466da
EXPECTED_FEATURE_COMMITS=22    # measured by the drafter 2026-09-13T13:43Z
# ==================================================================================================================================

MODE="${1:-}"
case "$MODE" in ''|--check) ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-d0466da-feedback-tier1.md"
PROMPT_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-d0466da-feedback-tier1.prompt.txt"
BRIEF="${QA_BRIEF_OVERRIDE:-$BRIEF_FINAL}"
PROMPT_FILE="${QA_PROMPT_OVERRIDE:-$PROMPT_FINAL}"
HPSM='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM'
REPO="$HPSM/6_Policy_Composer"
ARCH="$HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer"
SOW="$HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md"
NEXUS='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-$GATE_HEAD}"
HEAD7="${HEAD_SHA:0:7}"
REPORT_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-'"$HEAD7"'-feedback-tier1'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$HPSM/4_Credentials}"
BRANCH='refs/heads/main'
BASE_SHA='afc10e98c51505be1f1943335370cf2de3b47d44'
FEATURE_BASE='9b8ea76c073cefab0319d2bec7b5a82c54b4e9d1'
MIGRATION='packages/db/migrations/0016_feedback.sql'
DOCKER_LOCK='/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock'
PORTS='21480 21495 21580'
SUBJECT_STEM='[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer FEEDBACK feature @ '
SUBJECT="${SUBJECT_STEM}${HEAD7} (tier 1)"
# LOCAL ONLY: neither brief nor prompt may name the live demo's host, lane A's port or the S45 seat's ports.
FORBIDDEN_RE='hpsm-composer-demo|(^|[^0-9])(18580|20480|20580|20880)([^0-9]|$)'
# Every document the tester is told to read. Each must exist and be cited verbatim in the brief (validate what a brief points AT).
REFS=(
  "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
  "$ARCH/qa-s45/feedback-ready/README.md"
  "$ARCH/qa-s45/m16-0016-rollback/REPORT.md"
  "$HPSM/5_Project_History/HANDOVER-S43_seat-hpsm-28f5.md"
  "$HPSM/5_Project_History/HANDOVER-S44_seat-hpsm-375c.md"
  "$TUE/2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s43-successor-recover-remaining-feedback.md"
  "$TUE/2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s45-answer-feedback-gate-before-live.md"
  "$NEXUS/backend/routes/feedback.js"
  "$NEXUS/backend/feedbackAttachments.js"
  "$NEXUS/backend/feedbackTriage.js"
  "$NEXUS/static/js/feedback-widget.js"
  "$NEXUS/static/js/feedback-admin.js"
  "$SOW"
)
# Cited as BACKLOG.md L<n> — the file must exist (its lines move; the brief says cite by title if they do).
BACKLOG="$HPSM/BACKLOG.md"

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }
[[ "$HEAD_SHA" =~ ^[0-9a-f]{7,40}$ ]] || { echo "REFUSING: GATE_HEAD must be a 7-40 char hex commit SHA, got '$HEAD_SHA'" >&2; exit 6; }
HEAD_SHA="$(git --no-optional-locks -C "$REPO" rev-parse --verify "${HEAD_SHA}^{commit}" 2>/dev/null)" || {
  echo "REFUSING: $HEAD7 is not a commit in $REPO" >&2; exit 6; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$HEAD_SHA" "$BRANCH" 2>/dev/null || {
  echo "REFUSING: $HEAD_SHA is not reachable from $BRANCH — main was rewritten; re-brief" >&2; exit 18; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA" >&2; exit 7; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$FEATURE_BASE" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: the feature base $FEATURE_BASE is not an ancestor of $HEAD_SHA — the upgrade path has no start; re-brief" >&2; exit 7; }
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N' — re-count with GATE_HEAD" >&2; exit 8; }
NF="$(git --no-optional-locks -C "$REPO" rev-list --count "${FEATURE_BASE}..${HEAD_SHA}" 2>&1)"
[ "$NF" = "$EXPECTED_FEATURE_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_FEATURE_COMMITS feature commits, found '$NF'" >&2; exit 8; }
git --no-optional-locks -C "$REPO" cat-file -e "${FEATURE_BASE}:${MIGRATION}" 2>/dev/null && {
  echo "REFUSING: $MIGRATION already exists at the feature base — the 15 -> 16 upgrade path is not what the brief says" >&2; exit 9; }
git --no-optional-locks -C "$REPO" cat-file -e "${HEAD_SHA}:${MIGRATION}" 2>/dev/null || {
  echo "REFUSING: $MIGRATION is absent at $HEAD_SHA" >&2; exit 9; }
[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW (clean-clone CI needs PC_E8_SOW_TEXT)" >&2; exit 9; }
# Render the prompt: the ONE head pin fills its placeholders; every prompt guard below reads the text that is actually sent.
PROMPT_TEXT="$(sed -e "s/@GATE_HEAD@/$HEAD_SHA/g" -e "s/@GATE_HEAD7@/$HEAD7/g" "$PROMPT_FILE")"
perl -e 'alarm 30; exec @ARGV' docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding within 30 s" >&2; exit 10; }
grep -q 'LOCAL ONLY' <<<"$PROMPT_TEXT" && grep -q 'LOCAL ONLY' "$BRIEF" || {
  echo "REFUSING: brief and prompt must both say LOCAL ONLY" >&2; exit 10; }
grep -qE "$FORBIDDEN_RE" - "$BRIEF" <<<"$PROMPT_TEXT" && {
  echo "REFUSING: brief or prompt names the live host or another stack's port ($(grep -ohE "$FORBIDDEN_RE" - "$BRIEF" <<<"$PROMPT_TEXT" | sort -u | tr '\n' ' ')) — this gate is LOCAL ONLY" >&2; exit 10; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: HPSM identity dirs missing under $ID_ROOT — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' <<<"$PROMPT_TEXT" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 <<<"$PROMPT_TEXT" | grep -q '^ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF_FINAL" <<<"$PROMPT_TEXT" || { echo "REFUSING: prompt does not name the brief's final path" >&2; exit 14; }
grep -qF "$HEAD_SHA" <<<"$PROMPT_TEXT" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: brief or rendered prompt does not name the head $HEAD_SHA — a re-point needs a re-brief" >&2; exit 15; }
grep -qE '@[A-Z0-9_]+@' <<<"$PROMPT_TEXT" && { echo "REFUSING: rendered prompt still carries an unfilled @PLACEHOLDER@" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' <<<"$PROMPT_TEXT" && grep -q 'tuesday-agent@agentmail.to' <<<"$PROMPT_TEXT" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -qF "$SUBJECT" <<<"$PROMPT_TEXT" && grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief and prompt disagree on the verdict subject" >&2; exit 16; }
for v in 'DELIVERABLES' 'SECURITY'; do
  grep -q "$v" <<<"$PROMPT_TEXT" && grep -q "$v" "$BRIEF" || { echo "REFUSING: $v verdict not named in both brief and prompt" >&2; exit 20; }
done
for p in policy-composer-qa-fb-up policy-composer-qa-fb-fresh "$DOCKER_LOCK"; do
  grep -qF "$p" <<<"$PROMPT_TEXT" && grep -qF "$p" "$BRIEF" || { echo "REFUSING: '$p' not named in both brief and prompt" >&2; exit 20; }
done
for r in "${REFS[@]}"; do
  [ -e "$r" ] || { echo "REFUSING: reference document missing: $r" >&2; exit 21; }
  grep -qF "$r" "$BRIEF" || { echo "REFUSING: brief does not cite reference document verbatim: $r" >&2; exit 21; }
done
[ -s "$BACKLOG" ] && grep -qF 'BACKLOG.md L45' "$BRIEF" || { echo "REFUSING: BACKLOG.md missing, or the brief does not cite its declared items" >&2; exit 21; }
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
grep -qF "$REPORT_DIR/report.md" <<<"$PROMPT_TEXT" && grep -qF "$REPORT_DIR/report.md" "$BRIEF" || {
  echo "REFUSING: brief and prompt disagree on the report path ($REPORT_DIR/report.md)" >&2; exit 17; }
for p in $PORTS; do
  [ "$p" -ge 21480 ] && [ "$p" -le 21599 ] || { echo "REFUSING: port $p is outside the gate's range 21480-21599" >&2; exit 17; }
  lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1 && { echo "REFUSING: port $p already has a listener" >&2; exit 17; }
done
# (Kam's live-demo ruling guard dropped: LOCAL ONLY — no live site is in scope, so no live ruling is needed; exit 19 is @NOW@ only.)

if [ "$MODE" = "--check" ]; then
  echo "guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base + feature-base ancestors; range $EXPECTED_COMMITS / feature $EXPECTED_FEATURE_COMMITS; 0016 absent at base, present at head; SOW; docker; LOCAL-ONLY scope; identity dirs; tier/prompt/brief-path/head/mail/subject/two verdicts/project names/docker lock; ${#REFS[@]} reference docs + BACKLOG exist and are cited; no @NOW@; report dir absent; ports $PORTS in range and free"
  echo "pinned variables: HEAD_SHA=$HEAD_SHA · EXPECTED_COMMITS=$EXPECTED_COMMITS · REPORT_DIR=$REPORT_DIR · SUBJECT=$SUBJECT"
  exit 0
fi

[ -z "${QA_BRIEF_OVERRIDE:-}${QA_PROMPT_OVERRIDE:-}${QA_HEAD_SHA_OVERRIDE:-}${QA_IDENTITY_ROOT_OVERRIDE:-}" ] || {
  echo "REFUSING: QA_*_OVERRIDE variables are for --check on drafts only; install the files and unset them" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT_TEXT"
