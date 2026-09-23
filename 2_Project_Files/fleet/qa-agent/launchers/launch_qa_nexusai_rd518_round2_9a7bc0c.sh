#!/bin/bash
# launch_qa_nexusai_rd518_round2_9a7bc0c.sh — cross-project QA agent, THROUGH-CODE gate, ROUND 2 of 2,
# on Datasec/NexusAI RD-518 Key Vault identity + loud fallback: branch rd-518-kv-identity-r2-s75c
# @ 9a7bc0c, built by S75C.
#
# WHY ROUND 2 IS THROUGH-CODE AND NOT TIER 1 AGAIN: round 1 ran at 6ea15a0 and returned NO GO with
# five findings (F-01 BLOCKER, F-02 + F-03 MAJOR, F-04 + F-05 MINOR). The tier-1 weight was spent
# establishing the subject; this round carries the five findings and the merge's disturbance through
# the code. The stakes are unchanged — whether customer secrets are protected by a Key-Vault-managed
# key or a machine-derived one, and whether a broken deployment says so out loud.
#
# PATTERN: launch_qa_nexusai_rd518_6ea15a0.sh — the ROUND 1 launcher, not the RD-516 round-2 one.
# Round 1 is the right base because NO WORKTREE IS PINNED for this gate either: the agent builds its
# own from the object store, so the object-store guard (exit 6) is the right shape and the
# worktree-HEAD guard would have nothing to check. FOUR DELIBERATE CHANGES from round 1:
#   - the tier constant moves from 'TIER 1' to 'THROUGH-CODE' (exit 12), matching the brief's own title.
#   - the must-measure guard (exit 19) now asserts the two DECLARED LIMITS L-1 and L-2 by name
#     instead of round 1's M-A/M-B. Those limits are this gate's reason to exist: the builder declared
#     them itself, and a declared limit is where the evidence stops, not a place it is cleared.
#   - exit 21 is NEW: the COMPANION runbook branch must be at origin. F-05's fix lives on
#     rd-518-r2-runbook-fix-s75c @ c54d44c and is deliberately NOT in the head under test, but the
#     gate cannot drive a local run without it. A gate briefed to follow a runbook that is not
#     fetchable spends its session on the obstacle again — which is exactly what F-05 was.
#   - BASE is the MERGE commit 1c4fcb0, so the one-commit range guard (exit 8) still asks a
#     meaningful question: it scopes the delta to the fix commit alone, not to the merge.
#
# Shape verified at commission, from the object store and not from the builder's mail:
#   9a7bc0c parents [1c4fcb0]          — the fix commit
#   1c4fcb0 parents [6ea15a0 60c76d7]  — round 1's head merged forward with main (C-68, never rebased)
#   6ea15a0                            — the sha round 1 gated and FAILED
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD518r2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd518_round2_9a7bc0c.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd518-round2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd518-round2.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd518-9a7bc0c-round2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-9a7bc0c36d59c264040c9c6dce982c7576591ec1}"
BASE_SHA='1c4fcb0'
BRANCH='rd-518-kv-identity-r2-s75c'
EXPECTED_COMMITS=1

# F-05's fix — needed to DRIVE the gate, judged separately, deliberately not in the head.
RUNBOOK_BRANCH='rd-518-r2-runbook-fix-s75c'
RUNBOOK_SHA='c54d44cea9f2aea6090015118606cdc48ec6a71b'

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-518 round 2 @ 9a7bc0c (through-code)'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The sha must be a real commit in the object store — the gate builds its own worktree from it.
T="$(git --no-optional-locks -C "$REPO" cat-file -t "$HEAD_SHA" 2>&1)"
[ "$T" = "commit" ] || { echo "REFUSING: $HEAD_SHA is not a commit in $REPO (got '$T') — the gate could not check it out" >&2; exit 6; }

git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }

N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commit in ${BASE_SHA}..${HEAD_SHA}, found '$N' — the builder pushed again and the brief is stale" >&2; exit 8; }

# The head must be AT ORIGIN on its branch — a verdict is only reachable later if the sha is remote.
LSR="$(git --no-optional-locks -C "$REPO" ls-remote origin "$BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: $HEAD_SHA is not at refs/heads/$BRANCH on origin — that head moved or was never pushed" >&2
  printf '%s\n' "$LSR" >&2; exit 18; }

# 21 — the COMPANION runbook branch. The gate drives a local run by this runbook; without it the
# session is spent on the obstacle rather than on the findings. That is F-05 repeating itself.
LSR2="$(git --no-optional-locks -C "$REPO" ls-remote origin "$RUNBOOK_BRANCH" 2>&1)"
printf '%s\n' "$LSR2" | grep -q "^${RUNBOOK_SHA}[[:space:]]refs/heads/${RUNBOOK_BRANCH}\$" || {
  echo "REFUSING: $RUNBOOK_SHA is not at refs/heads/$RUNBOOK_BRANCH on origin — the runbook fix the gate needs to RUN is not fetchable" >&2
  printf '%s\n' "$LSR2" >&2; exit 21; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

TIER='THROUGH-CODE'
grep -qi "$TIER" "$BRIEF" && grep -qi "$TIER" "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare tier '$TIER'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: prompt must name the brief path and the head, and the brief must name the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }

grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path (DELTA 40)" >&2; exit 20; }

# 19 — THE TWO DECLARED LIMITS. This gate exists to decide whether the verdict can stand on evidence
# that stops where the builder said it stops. A prompt that drops them commissions a victory lap.
grep -q 'L-1' "$PROMPT_FILE" && grep -q 'L-2' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must carry BOTH declared limits L-1 and L-2 by name" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $HEAD_SHA is a commit in the object store"
  echo "  base $BASE_SHA is an ancestor; range is exactly $EXPECTED_COMMITS commit (the fix, not the merge)"
  echo "  head is at refs/heads/$BRANCH on origin"
  echo "  companion runbook $RUNBOOK_SHA is at refs/heads/$RUNBOOK_BRANCH on origin (21)"
  echo "  report path named in the brief; report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier '$TIER' agrees; AgentMail key absolute (20); limits L-1 and L-2 present (19)"
  echo "  prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@, subject"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
