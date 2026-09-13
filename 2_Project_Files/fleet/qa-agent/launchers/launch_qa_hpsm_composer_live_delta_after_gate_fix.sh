#!/bin/bash
# launch_qa_hpsm_composer_live_delta_after_gate_fix.sh — cross-project QA agent, TIER 1, class "acceptance vs original brief + security",
#   LIVE-ONLY DELTA, round 1: re-runs on the LIVE Azure demo the half the caf63fd gate's D-B1 blocked, and verifies the builder's
#   b-tight gate fix. Two verdicts, DELIVERABLES (LIVE) and SECURITY (LIVE), about the head the LIVE site runs (LIVE_HEAD below).
# Kam, 2026-09-13 (relayed by Tuesday): re-test the live half after the gate fix; "make sure that you include the credentials in the
#   testing document harness" — the brief names them by PATH only; this launcher never opens them.
# PATTERN: launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh, line for line. CHANGED: (1) LIVE_HEAD is the ONE head pin, at
#   the top; HEAD7 / REPORT_DIR / SUBJECT derive from it, and the prompt file carries @LIVE_HEAD@ / @LIVE_HEAD7@ placeholders this
#   launcher renders, so a re-point is one edit (+ EXPECTED_COMMITS); every prompt guard reads the RENDERED text that is actually sent;
#   (2) the brief stays pinned to its drafting head (BRIEF_DRAFT_HEAD) and must carry its own re-point clause;
#   (3) docker + local-port guards and the compose-project names dropped — LIVE ONLY (brief §1, §3 "Out of scope"); exit 10 is now
#   the LIVE-only scope guard; (4) the live-demo ruling must be APPROVED — a veto leaves a live-only gate nothing to run;
#   (5) REFS re-pointed to what this brief cites verbatim (+ the prior report); credential files checked by stat only, never opened.
# INSTALL (Tuesday, after Kam's review): brief -> $BRIEF_FINAL, prompt -> $PROMPT_FINAL, this file -> fleet/qa-agent/launchers/.
# LAUNCH IN ITS OWN TMUX PANE (cockpit.sh add 'QA/HPSM-live-delta' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd`.
# Usage: launch_qa_hpsm_composer_live_delta_after_gate_fix.sh [--check]
# Exit: 0 launched (or every guard passed under --check) · 2..22 a guard refused (19 = Kam's live-demo ruling not recorded as APPROVED)
set -u

# ==== HEAD PIN ====================================================================================================================
# RE-POINT to the upgraded head from the S44 upgrade REPORT before launch
LIVE_HEAD='87c0026d94e8e13c14329852239d35a463168503'  # re-pointed by Tuesday s14 from S44 upgrade REPORT 2026-09-13T11:25:29Z
# ...and re-count for that head: git -C "$REPO" rev-list --count afc10e98c51505be1f1943335370cf2de3b47d44..<LIVE_HEAD>  (267 at caf63fd)
EXPECTED_COMMITS=308  # rev-list --count afc10e98..87c0026, measured by Tuesday s14 21:2x
# ==================================================================================================================================

MODE="${1:-}"
case "$MODE" in ''|--check) ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-live-delta-after-gate-fix-tier1.md"
PROMPT_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-live-delta-after-gate-fix-tier1.prompt.txt"
BRIEF="${QA_BRIEF_OVERRIDE:-$BRIEF_FINAL}"
PROMPT_FILE="${QA_PROMPT_OVERRIDE:-$PROMPT_FINAL}"
HPSM='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM'
REPO="$HPSM/6_Policy_Composer"
SRC="$HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10"
ARCH="$HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer"
SOW="$SRC/_extracted/sow_e8.md"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-$LIVE_HEAD}"
HEAD7="${HEAD_SHA:0:7}"
REPORT_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-'"$HEAD7"'-live-delta-after-gate-fix-tier1'
PRIOR_REPORT='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$HPSM/4_Credentials}"
BRANCH='refs/heads/main'
BASE_SHA='afc10e98c51505be1f1943335370cf2de3b47d44'
# The head this brief was DRAFTED against. NOT re-pointed: the brief says Tuesday re-points the launcher, not the brief.
BRIEF_DRAFT_HEAD='caf63fd54c3ad95384bcb7bc32d4e7b9e4a6f5c4'
LIVE_URL='https://hpsm-composer-demo.australiaeast.cloudapp.azure.com'
SUBJECT_STEM='[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer LIVE delta after gate fix @ '
SUBJECT="${SUBJECT_STEM}${HEAD7} (tier 1)"
# Every document the tester is told to read. Each must exist and be cited verbatim in the brief (validate what a brief points AT).
REFS=(
  "$SRC/Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx"
  "$SRC/_extracted/spec.md"
  "$SRC/HPSM Policy Composer - Screens.pptx"
  "$SRC/Policy Preview.pdf"
  "$SOW"
  "$TUE/2_Project_Files/fleet/briefs_staged/2026-09-10_hpsm-phase1-architecture.md"
  "$ARCH/"
  "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
  "$PRIOR_REPORT"
)
# Cited by file name under $ARCH/ — must exist.
ARCH_FILES=( README.md 2026-09-10_policy-composer_ARCHITECTURE.md 2026-09-10_source-measurements.md 2026-09-10_screens-MEASURED.md
  2026-09-10_seed-data-CONTRACT.md 2026-09-13_output-export-request-S40.md qa-wp4/README.md )
# Named in brief and prompt by PATH only. Checked by stat ([ -s ]) — this launcher never opens, reads or prints them.
CREDS=(
  "$HPSM/4_Credentials/hpsm-demo-site.txt"
  "$HPSM/4_Credentials/gate-check-public.env"
)

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }
[[ "$HEAD_SHA" =~ ^[0-9a-f]{7,40}$ ]] || { echo "REFUSING: LIVE_HEAD must be a 7-40 char hex commit SHA, got '$HEAD_SHA'" >&2; exit 6; }
HEAD_SHA="$(git --no-optional-locks -C "$REPO" rev-parse --verify "${HEAD_SHA}^{commit}" 2>/dev/null)" || {
  echo "REFUSING: $HEAD7 is not a commit in $REPO" >&2; exit 6; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$HEAD_SHA" "$BRANCH" 2>/dev/null || {
  echo "REFUSING: $HEAD_SHA is not reachable from $BRANCH — main was rewritten; re-brief" >&2; exit 18; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA" >&2; exit 7; }
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BRIEF_DRAFT_HEAD" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $HEAD_SHA does not descend from the brief's drafting head $BRIEF_DRAFT_HEAD — this is a delta after it; re-brief" >&2; exit 7; }
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N' — re-count EXPECTED_COMMITS with LIVE_HEAD" >&2; exit 8; }
[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW" >&2; exit 9; }
# Render the prompt: the ONE head pin fills its placeholders; every prompt guard below reads the text that is actually sent.
PROMPT_TEXT="$(sed -e "s/@LIVE_HEAD@/$HEAD_SHA/g" -e "s/@LIVE_HEAD7@/$HEAD7/g" "$PROMPT_FILE")"
# (docker guard dropped: LIVE ONLY — brief §1 "no docker in scope".) Exit 10 is the LIVE-only scope guard.
grep -q 'LIVE ONLY' <<<"$PROMPT_TEXT" && grep -q 'LIVE ONLY' "$BRIEF" && grep -qF "$LIVE_URL" <<<"$PROMPT_TEXT" && grep -qF "$LIVE_URL" "$BRIEF" || {
  echo "REFUSING: brief and prompt must both say LIVE ONLY and name $LIVE_URL" >&2; exit 10; }
grep -qE 'policy-composer-qa-|127\.0\.0\.1' - "$BRIEF" <<<"$PROMPT_TEXT" && {
  echo "REFUSING: brief or prompt names a local compose project or port — this gate is LIVE ONLY" >&2; exit 10; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: HPSM identity dirs missing under $ID_ROOT — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' <<<"$PROMPT_TEXT" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 <<<"$PROMPT_TEXT" | grep -q '^ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF_FINAL" <<<"$PROMPT_TEXT" || { echo "REFUSING: prompt does not name the brief's final path" >&2; exit 14; }
grep -qF "$HEAD_SHA" <<<"$PROMPT_TEXT" && grep -qF "$BRIEF_DRAFT_HEAD" "$BRIEF" || { echo "REFUSING: prompt does not name the head, or brief does not name its drafting head" >&2; exit 15; }
grep -qF "Tuesday re-points the launcher's HEAD_SHA" "$BRIEF" || { echo "REFUSING: brief does not authorise re-pointing the head in the launcher" >&2; exit 15; }
grep -qE '@[A-Z0-9_]+@' <<<"$PROMPT_TEXT" && { echo "REFUSING: rendered prompt still carries an unfilled @PLACEHOLDER@" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' <<<"$PROMPT_TEXT" && grep -q 'tuesday-agent@agentmail.to' <<<"$PROMPT_TEXT" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -qF "$SUBJECT" <<<"$PROMPT_TEXT" && grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief and prompt disagree on the verdict subject" >&2; exit 16; }
for v in 'DELIVERABLES (LIVE)' 'SECURITY (LIVE)'; do
  grep -qF "$v" <<<"$PROMPT_TEXT" && grep -qF "$v" "$BRIEF" || { echo "REFUSING: $v verdict not named in both brief and prompt" >&2; exit 20; }
done
for p in 'QA Harness (synthetic)' "never Kam's tenant"; do
  grep -qF "$p" <<<"$PROMPT_TEXT" && grep -qF "$p" "$BRIEF" || { echo "REFUSING: tenant rule '$p' not named in both" >&2; exit 20; }
done
for r in "${REFS[@]}"; do
  [ -e "$r" ] || { echo "REFUSING: reference document missing: $r" >&2; exit 21; }
  grep -qF "$r" "$BRIEF" || { echo "REFUSING: brief does not cite reference document verbatim: $r" >&2; exit 21; }
done
for f in "${ARCH_FILES[@]}"; do
  [ -e "$ARCH/$f" ] || { echo "REFUSING: architecture file missing: $ARCH/$f" >&2; exit 21; }
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not cite $f" >&2; exit 21; }
done
for c in "${CREDS[@]}"; do
  [ -s "$c" ] || { echo "REFUSING: credential file missing or empty (stat only): $c" >&2; exit 21; }
  grep -qF "$c" "$BRIEF" && grep -qF "$c" <<<"$PROMPT_TEXT" || { echo "REFUSING: credential path not named in both brief and prompt: $c" >&2; exit 21; }
done
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
grep -qF "$REPORT_DIR/report.md" <<<"$PROMPT_TEXT" && grep -qF '2026-09-13-composer-<head7>-live-delta-after-gate-fix-tier1/report.md' "$BRIEF" || {
  echo "REFUSING: brief and prompt disagree on the report path" >&2; exit 17; }
# (local-port guard dropped: LIVE ONLY — no compose project and no local port are in scope.)

# Kam's live-demo ruling (approval-class: his Monday demo). The brief's §1 line must read
#   LIVE DEMO RULING: APPROVED by Kam <YYYY-MM-DD HH:MM AEST>
# A LIVE-ONLY gate has nothing to run under a veto, so VETOED (by Kam, or by default) refuses as well.
RULING='recorded'
if grep -qF '@KAM_LIVE_DEMO_RULING@' "$BRIEF"; then RULING='PENDING (placeholder @KAM_LIVE_DEMO_RULING@ still in the brief)'
elif grep -qF 'LIVE DEMO RULING: VETOED' "$BRIEF"; then RULING='VETOED (a LIVE-ONLY gate has nothing to run)'
elif ! grep -qE 'LIVE DEMO RULING: APPROVED by Kam [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}' "$BRIEF"; then
  RULING='MALFORMED (need "LIVE DEMO RULING: APPROVED by Kam YYYY-MM-DD HH:MM")'
fi

if [ "$MODE" = "--check" ]; then
  echo "guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base + drafting-head ancestors; range $EXPECTED_COMMITS; SOW; LIVE-only scope; identity dirs; tier/prompt/brief-path/head/mail/subject/two verdicts/tenant rules; ${#REFS[@]} reference docs + ${#ARCH_FILES[@]} architecture files + ${#CREDS[@]} credential paths exist and are cited; no @NOW@; report dir absent"
  echo "re-pointed variables: HEAD_SHA=$HEAD_SHA · EXPECTED_COMMITS=$EXPECTED_COMMITS · REPORT_DIR=$REPORT_DIR · SUBJECT=$SUBJECT"
  [ "$RULING" = 'recorded' ] || { echo "NOT READY TO LAUNCH: Kam's live-demo ruling $RULING" >&2; exit 19; }
  echo "Kam's live-demo ruling recorded: $(grep -oE 'LIVE DEMO RULING: APPROVED by Kam [0-9: -]+' "$BRIEF" | head -1)"
  exit 0
fi

[ -z "${QA_BRIEF_OVERRIDE:-}${QA_PROMPT_OVERRIDE:-}" ] || {
  echo "REFUSING: QA_BRIEF_OVERRIDE/QA_PROMPT_OVERRIDE are for --check on drafts only; install the files and unset them" >&2; exit 22; }
[ "$RULING" = 'recorded' ] || { echo "REFUSING: Kam's live-demo ruling $RULING" >&2; exit 19; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT_TEXT"
