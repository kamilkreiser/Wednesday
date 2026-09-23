#!/bin/bash
# launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh — cross-project QA agent, TIER 1, NEW gate class, round 1:
#   platform ACCEPTANCE against the ORIGINAL Composer brief (spec v1.1) + SECURITY, two verdicts (DELIVERABLES, SECURITY),
#   on the Datasec/HPSM Policy Composer local main @ caf63fd (re-pointed from 09c1591 by Tuesday s12, 2026-09-13), NOT pushed.
# Kam, 2026-09-13 17:00 AEST: "...write a testing harness prompt to test the platform from a security perspective as well as
#   from a deliverables perspective against the original brief."
# PATTERN: launch_qa_hpsm_composer_09c1591_combined.sh (reachable-from-main head guard, report-dir, port, identity guards),
#   without a gate letter. ADDED: (1) a reference-document guard: every source the brief cites exists AND is named in the brief;
#   (2) Kam's live-demo ruling guard: the launch refuses while the brief's LIVE DEMO RULING line is unresolved;
#   (3) docker info bounded to 30 s (the shared daemon was measured hanging on 2026-09-13 with three gates on it);
#   (4) QA_BRIEF_OVERRIDE / QA_PROMPT_OVERRIDE so --check can validate a draft BEFORE it is installed; a real launch refuses them.
# INSTALL (Tuesday, after Kam's review): brief -> $BRIEF_FINAL, prompt -> $PROMPT_FINAL, this file -> fleet/qa-agent/launchers/.
# LAUNCH IN ITS OWN TMUX PANE (cockpit.sh add 'QA/HPSM-BAS' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd`.
# Usage: launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh [--check]
# Exit: 0 launched (or every guard passed under --check) · 2..22 a guard refused (19 = Kam's live-demo ruling not recorded)
set -u

MODE="${1:-}"
case "$MODE" in ''|--check) ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md"
PROMPT_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.prompt.txt"
BRIEF="${QA_BRIEF_OVERRIDE:-$BRIEF_FINAL}"
PROMPT_FILE="${QA_PROMPT_OVERRIDE:-$PROMPT_FINAL}"
HPSM='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM'
REPO="$HPSM/6_Policy_Composer"
SRC="$HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10"
ARCH="$HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer"
SOW="$SRC/_extracted/sow_e8.md"
REPORT_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$HPSM/4_Credentials}"
BRANCH='refs/heads/main'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-caf63fd54c3ad95384bcb7bc32d4e7b9e4a6f5c4}"
BASE_SHA='afc10e98c51505be1f1943335370cf2de3b47d44'
EXPECTED_COMMITS=267
PORTS='21480 21495 21580'
SUBJECT='[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer acceptance vs original brief + security @ caf63fd (tier 1)'
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
  "$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1.md"
  "$HPSM/5_Project_History/BACKLOG-candidates_s42_seat-hpsm-3e04.md"
  "$HPSM/BACKLOG.md"
)
# Cited by file name under $ARCH/ — must exist.
ARCH_FILES=( README.md 2026-09-10_policy-composer_ARCHITECTURE.md 2026-09-10_source-measurements.md 2026-09-10_screens-MEASURED.md
  2026-09-10_seed-data-CONTRACT.md 2026-09-13_output-export-request-S40.md qa-wp4/README.md )

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
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }
[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW" >&2; exit 9; }
perl -e 'alarm 30; exec @ARGV' docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding within 30 s" >&2; exit 10; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: HPSM identity dirs missing under $ID_ROOT — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q '^ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF_FINAL" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief's final path" >&2; exit 14; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || { echo "REFUSING: brief or prompt does not name the head" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief and prompt disagree on the verdict subject" >&2; exit 16; }
for v in 'DELIVERABLES' 'SECURITY'; do
  grep -q "$v" "$PROMPT_FILE" && grep -q "$v" "$BRIEF" || { echo "REFUSING: $v verdict not named in both brief and prompt" >&2; exit 20; }
done
for p in policy-composer-qa-bas-on policy-composer-qa-bas-off; do
  grep -qF "$p" "$PROMPT_FILE" && grep -qF "$p" "$BRIEF" || { echo "REFUSING: compose project $p not named in both" >&2; exit 20; }
done
for r in "${REFS[@]}"; do
  [ -e "$r" ] || { echo "REFUSING: reference document missing: $r" >&2; exit 21; }
  grep -qF "$r" "$BRIEF" || { echo "REFUSING: brief does not cite reference document verbatim: $r" >&2; exit 21; }
done
for f in "${ARCH_FILES[@]}"; do
  [ -e "$ARCH/$f" ] || { echo "REFUSING: architecture file missing: $ARCH/$f" >&2; exit 21; }
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not cite $f" >&2; exit 21; }
done
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
for p in $PORTS; do
  lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1 && { echo "REFUSING: port $p already has a listener" >&2; exit 17; }
done

# Kam's live-demo ruling (approval-class: his Monday demo). The brief's §1 line must read
#   LIVE DEMO RULING: APPROVED by Kam <YYYY-MM-DD HH:MM AEST>   or   LIVE DEMO RULING: VETOED by Kam <YYYY-MM-DD HH:MM AEST>
RULING='recorded'
if grep -qF '@KAM_LIVE_DEMO_RULING@' "$BRIEF"; then RULING='PENDING (placeholder @KAM_LIVE_DEMO_RULING@ still in the brief)'
elif ! grep -qE 'LIVE DEMO RULING: ((APPROVED|VETOED) by Kam|VETOED by default - Tuesday, Kam has not ruled) [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}' "$BRIEF"; then
  RULING='MALFORMED (need "LIVE DEMO RULING: APPROVED|VETOED by Kam YYYY-MM-DD HH:MM")'
fi

if [ "$MODE" = "--check" ]; then
  echo "guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base ancestor; range $EXPECTED_COMMITS; SOW; docker; identity dirs; tier/prompt/brief-path/head/mail/subject/two verdicts/project names; ${#REFS[@]} reference docs + ${#ARCH_FILES[@]} architecture files exist and are cited; no @NOW@; report dir absent; ports $PORTS free"
  [ "$RULING" = 'recorded' ] || { echo "NOT READY TO LAUNCH: Kam's live-demo ruling $RULING" >&2; exit 19; }
  echo "Kam's live-demo ruling recorded: $(grep -oE 'LIVE DEMO RULING: ((APPROVED|VETOED) by Kam|VETOED by default - Tuesday, Kam has not ruled) [0-9: -]+' "$BRIEF" | head -1)"
  exit 0
fi

[ -z "${QA_BRIEF_OVERRIDE:-}${QA_PROMPT_OVERRIDE:-}" ] || {
  echo "REFUSING: QA_BRIEF_OVERRIDE/QA_PROMPT_OVERRIDE are for --check on drafts only; install the files and unset them" >&2; exit 22; }
[ "$RULING" = 'recorded' ] || { echo "REFUSING: Kam's live-demo ruling $RULING" >&2; exit 19; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
