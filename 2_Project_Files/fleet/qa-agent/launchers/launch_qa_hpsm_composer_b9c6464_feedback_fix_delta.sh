#!/bin/bash
# launch_qa_hpsm_composer_b9c6464_feedback_fix_delta.sh — cross-project QA agent, TIER 1, FEATURE-SCOPED DELTA gate, round 1:
#   the FEEDBACK credential-scan fix (S45 G45) of the Datasec/HPSM Policy Composer, DELTA_BASE..GATE_HEAD, LOCAL ONLY,
#   two verdicts (DELIVERABLES, SECURITY), on local main @ GATE_HEAD below, NOT pushed, NOT live.
# Tuesday s15, 2026-09-14 (briefs_staged/2026-09-14_hpsm-s45-answer-b9c6464-received-delta-gate.md L1-6, L15): the delta tier-1 gate
#   on d0466da..b9c6464, ports 21610-21729. TIER 1 because it is a security surface (credential storage) headed for a live deploy:
#   b9c6464 is the accepted live target, and the live GO needs this verdict with no Blocker or Major.
# Oracle, Tuesday 14:34:04Z ruling (a) (briefs_staged/2026-09-14_hpsm-s45-answer-g45-defect-retarget.md L14-16): credential-shaped
#   free text fails closed with 422; whether the decoding catches every encoded form on every feedback field and path is this gate's.
# DRAFTED by a subagent for Tuesday s15 and NOT launched by the drafter. Another gate runs concurrently on other ports and projects;
#   this one is independent of it and shares only the docker lock.
# PATTERN: launch_qa_hpsm_composer_d0466da_feedback.sh, line for line. CHANGED: (1) GATE_HEAD b9c6464; the report dir, subject, ports
#   (21610-21729) and compose projects (policy-composer-qa-fbfix-*) follow; (2) the feature-base guard becomes a DELTA guard: DELTA_BASE
#   is an ancestor AND the head's first parent, the delta is EXPECTED_DELTA_COMMITS commits, it touches EXACTLY DELTA_FILES and no
#   migration, and 0016 is present at both ends (exit 7/8/9); the brief and the rendered prompt must name DELTA_BASE in full (exit 15);
#   (3) FORBIDDEN_RE also refuses the concurrent gate's ports, compose projects and report dir, and the S45 live-run tunnel port, so
#   neither file can point the tester at a stack it does not own; (4) REFS re-pointed to what this brief cites (the delta README, the
#   two Tuesday answers, HANDOVER-S45, the architecture's secrets section); the NexusAI parity refs, the S43/S44 handovers and the M16
#   report are dropped (parity and the 15 -> 16 upgrade are not in a fix delta); the BACKLOG citation is the G45 entry, L52.
# INSTALL: already in place (brief -> $BRIEF_FINAL, prompt -> $PROMPT_FINAL, this file -> fleet/qa-agent/launchers/). Tuesday reviews first.
# LAUNCH IN ITS OWN TMUX PANE (cockpit.sh add 'QA/HPSM-fbfix' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd`.
# Usage: launch_qa_hpsm_composer_b9c6464_feedback_fix_delta.sh [--check]
# Exit: 0 launched (or every guard passed under --check) · 2..22 a guard refused (10 = docker or the LOCAL-ONLY scope)
set -u

# ==== HEAD PIN ====================================================================================================================
GATE_HEAD='b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a'  # S45 READY FOR QA delta 14:51:46Z (qa-s45/feedback-fix-delta/README.md L4)
# git --no-optional-locks -C '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' rev-list --count afc10e98c51505be1f1943335370cf2de3b47d44..b9c6464
EXPECTED_COMMITS=348           # measured by the drafter 2026-09-13T14:54Z
# git --no-optional-locks -C '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' rev-list --count d0466daaa7f2ae30b2da8f8fd537e95250da0aa8..b9c6464
EXPECTED_DELTA_COMMITS=6       # measured by the drafter 2026-09-13T14:54Z
# ==================================================================================================================================

MODE="${1:-}"
case "$MODE" in ''|--check) ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_hpsm-composer-b9c6464-feedback-fix-delta-tier1.md"
PROMPT_FINAL="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_hpsm-composer-b9c6464-feedback-fix-delta-tier1.prompt.txt"
BRIEF="${QA_BRIEF_OVERRIDE:-$BRIEF_FINAL}"
PROMPT_FILE="${QA_PROMPT_OVERRIDE:-$PROMPT_FINAL}"
HPSM='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM'
REPO="$HPSM/6_Policy_Composer"
ARCH="$HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer"
SOW="$HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-$GATE_HEAD}"
HEAD7="${HEAD_SHA:0:7}"
REPORT_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-14-composer-'"$HEAD7"'-feedback-fix-delta-tier1'
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$HPSM/4_Credentials}"
BRANCH='refs/heads/main'
BASE_SHA='afc10e98c51505be1f1943335370cf2de3b47d44'
DELTA_BASE='d0466daaa7f2ae30b2da8f8fd537e95250da0aa8'
# The builder's claim, read by the drafter with `git diff --name-only d0466da b9c6464` (git's own path order). Exactly these, nothing else.
DELTA_FILES='apps/api/src/feedback.ts
apps/api/src/routes/feedback.ts
apps/api/test/api-credential-shapes.db.test.ts'
MIGRATION='packages/db/migrations/0016_feedback.sql'
DOCKER_LOCK='/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock'
PORTS='21610 21625 21710'
SUBJECT_STEM='[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer FEEDBACK fix delta @ '
SUBJECT="${SUBJECT_STEM}${HEAD7} (tier 1)"
# LOCAL ONLY: neither brief nor prompt may name the live demo's host, lane A's port, the S45 seat's ports or live-run tunnel port,
# or the concurrently running feedback gate's ports, compose projects or report directory.
FORBIDDEN_RE='hpsm-composer-demo|policy-composer-qa-fb-(up|fresh)|2026-09-13-composer-d0466da-feedback-tier1|(^|[^0-9])(18580|20480|20580|20880|21480|21495|21580|23990)([^0-9]|$)'
# Every document the tester is told to read. Each must exist and be cited verbatim in the brief (validate what a brief points AT).
REFS=(
  "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
  "$ARCH/qa-s45/feedback-fix-delta/README.md"
  "$ARCH/qa-s45/feedback-ready/README.md"
  "$ARCH/2026-09-10_policy-composer_ARCHITECTURE.md"
  "$HPSM/5_Project_History/HANDOVER-S45_seat-hpsm-3562.md"
  "$TUE/2_Project_Files/fleet/briefs_staged/2026-09-14_hpsm-s45-answer-g45-defect-retarget.md"
  "$TUE/2_Project_Files/fleet/briefs_staged/2026-09-14_hpsm-s45-answer-b9c6464-received-delta-gate.md"
  "$SOW"
)
# Cited as BACKLOG.md L<n> — the file must exist (its lines move; the brief cites by title where they already have).
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
git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$DELTA_BASE" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: the delta base $DELTA_BASE is not an ancestor of $HEAD_SHA — the delta has no start; re-brief" >&2; exit 7; }
P1="$(git --no-optional-locks -C "$REPO" rev-parse --verify "${HEAD_SHA}^1" 2>/dev/null)"
[ "$P1" = "$DELTA_BASE" ] || { echo "REFUSING: the head's first parent is '$P1', not the delta base $DELTA_BASE — re-brief" >&2; exit 7; }
N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N' — re-count with GATE_HEAD" >&2; exit 8; }
ND="$(git --no-optional-locks -C "$REPO" rev-list --count "${DELTA_BASE}..${HEAD_SHA}" 2>&1)"
[ "$ND" = "$EXPECTED_DELTA_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_DELTA_COMMITS delta commits, found '$ND'" >&2; exit 8; }
FILES_NOW="$(git --no-optional-locks -C "$REPO" diff --name-only "$DELTA_BASE" "$HEAD_SHA" 2>&1)"
[ "$FILES_NOW" = "$DELTA_FILES" ] || {
  echo "REFUSING: the delta touches [$(tr '\n' ' ' <<<"$FILES_NOW")], not exactly the brief's three files — re-brief" >&2; exit 9; }
git --no-optional-locks -C "$REPO" diff --quiet "$DELTA_BASE" "$HEAD_SHA" -- packages/db/migrations packages/db/src/migrate.ts 2>/dev/null || {
  echo "REFUSING: the delta changes a migration or the migrator — the brief says it carries none" >&2; exit 9; }
for c in "$DELTA_BASE" "$HEAD_SHA"; do
  git --no-optional-locks -C "$REPO" cat-file -e "${c}:${MIGRATION}" 2>/dev/null || {
    echo "REFUSING: $MIGRATION is absent at $c — the brief's 16-migration stacks are not what it says" >&2; exit 9; }
done
[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW (clean-clone CI needs PC_E8_SOW_TEXT)" >&2; exit 9; }
# Render the prompt: the ONE head pin fills its placeholders; every prompt guard below reads the text that is actually sent.
PROMPT_TEXT="$(sed -e "s/@GATE_HEAD@/$HEAD_SHA/g" -e "s/@GATE_HEAD7@/$HEAD7/g" "$PROMPT_FILE")"
perl -e 'alarm 30; exec @ARGV' docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding within 30 s" >&2; exit 10; }
grep -q 'LOCAL ONLY' <<<"$PROMPT_TEXT" && grep -q 'LOCAL ONLY' "$BRIEF" || {
  echo "REFUSING: brief and prompt must both say LOCAL ONLY" >&2; exit 10; }
grep -qE "$FORBIDDEN_RE" - "$BRIEF" <<<"$PROMPT_TEXT" && {
  echo "REFUSING: brief or prompt names the live host or another stack's port, project or report ($(grep -ohE "$FORBIDDEN_RE" - "$BRIEF" <<<"$PROMPT_TEXT" | sort -u | tr '\n' ' ')) — this gate is LOCAL ONLY" >&2; exit 10; }
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
grep -qF "$DELTA_BASE" <<<"$PROMPT_TEXT" && grep -qF "$DELTA_BASE" "$BRIEF" || {
  echo "REFUSING: brief or rendered prompt does not name the delta base $DELTA_BASE — a re-base needs a re-brief" >&2; exit 15; }
grep -qE '@[A-Z0-9_]+@' <<<"$PROMPT_TEXT" && { echo "REFUSING: rendered prompt still carries an unfilled @PLACEHOLDER@" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' <<<"$PROMPT_TEXT" && grep -q 'tuesday-agent@agentmail.to' <<<"$PROMPT_TEXT" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }
grep -qF "$SUBJECT" <<<"$PROMPT_TEXT" && grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief and prompt disagree on the verdict subject" >&2; exit 16; }
for v in 'DELIVERABLES' 'SECURITY'; do
  grep -q "$v" <<<"$PROMPT_TEXT" && grep -q "$v" "$BRIEF" || { echo "REFUSING: $v verdict not named in both brief and prompt" >&2; exit 20; }
done
for p in policy-composer-qa-fbfix-up policy-composer-qa-fbfix-fresh "$DOCKER_LOCK"; do
  grep -qF "$p" <<<"$PROMPT_TEXT" && grep -qF "$p" "$BRIEF" || { echo "REFUSING: '$p' not named in both brief and prompt" >&2; exit 20; }
done
for r in "${REFS[@]}"; do
  [ -e "$r" ] || { echo "REFUSING: reference document missing: $r" >&2; exit 21; }
  grep -qF "$r" "$BRIEF" || { echo "REFUSING: brief does not cite reference document verbatim: $r" >&2; exit 21; }
done
[ -s "$BACKLOG" ] && grep -qF 'BACKLOG.md L52' "$BRIEF" || { echo "REFUSING: BACKLOG.md missing, or the brief does not cite its G45 entry" >&2; exit 21; }
grep -q '@NOW@' "$BRIEF" && { echo "REFUSING: brief still carries an unfilled @NOW@ placeholder" >&2; exit 19; }
[ -e "$REPORT_DIR" ] && { echo "REFUSING: report dir already exists: $REPORT_DIR — re-run under a NEW path" >&2; exit 17; }
grep -qF "$REPORT_DIR/report.md" <<<"$PROMPT_TEXT" && grep -qF "$REPORT_DIR/report.md" "$BRIEF" || {
  echo "REFUSING: brief and prompt disagree on the report path ($REPORT_DIR/report.md)" >&2; exit 17; }
for p in $PORTS; do
  [ "$p" -ge 21610 ] && [ "$p" -le 21729 ] || { echo "REFUSING: port $p is outside the gate's range 21610-21729" >&2; exit 17; }
  lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1 && { echo "REFUSING: port $p already has a listener" >&2; exit 17; }
done
# (No live-demo ruling guard: LOCAL ONLY — no live site is in scope, so no live ruling is needed; exit 19 is @NOW@ only.)

if [ "$MODE" = "--check" ]; then
  echo "guards pass: $HEAD_SHA reachable from $BRANCH (now $(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)); base + delta-base ancestors; first parent = delta base; range $EXPECTED_COMMITS / delta $EXPECTED_DELTA_COMMITS; delta touches exactly [$(tr '\n' ' ' <<<"$FILES_NOW")] and no migration; 0016 present at both ends; SOW; docker; LOCAL-ONLY scope; identity dirs; tier/prompt/brief-path/head/delta-base/mail/subject/two verdicts/project names/docker lock; ${#REFS[@]} reference docs + BACKLOG exist and are cited; no @NOW@; report dir absent; ports $PORTS in range and free"
  echo "pinned variables: HEAD_SHA=$HEAD_SHA · DELTA_BASE=$DELTA_BASE · EXPECTED_COMMITS=$EXPECTED_COMMITS · REPORT_DIR=$REPORT_DIR · SUBJECT=$SUBJECT"
  exit 0
fi

[ -z "${QA_BRIEF_OVERRIDE:-}${QA_PROMPT_OVERRIDE:-}${QA_HEAD_SHA_OVERRIDE:-}${QA_IDENTITY_ROOT_OVERRIDE:-}" ] || {
  echo "REFUSING: QA_*_OVERRIDE variables are for --check on drafts only; install the files and unset them" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT_TEXT"
