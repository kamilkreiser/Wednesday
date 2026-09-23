#!/bin/bash
# launch_qa_nexusai_rd574_6ec3606.sh — cross-project QA agent, TIER 1 gate, ROUND 1, on
# Datasec/NexusAI RD-574 seam-dependent cells: branch rd-574-seam-cells-s74 @ 6ec3606, built by S74.
#
# WHY TIER 1 FOR A TEST-ONLY BRANCH: the change touches no product code (verified below, exit 22),
# which lowers blast radius but does not lower the tier. The whole PRODUCT of this branch is test
# confidence, so a cell that is green for a weaker reason than it claims is a defect in the very
# thing being delivered. RD-590 — declared by the builder — says four existing cells will do exactly
# that, and that inertness structurally cannot see it.
#
# WHO IS DOWNSTREAM: RD-516's round-2 gate returned GO but explicitly did NOT clear its merge,
# because RD-516 section 5 needs these cells ON MAIN. This gate's verdict therefore unblocks (or
# mis-unblocks) another ticket, which is why the brief and prompt both require the verdict to state
# what it means for that dependency.
#
# PATTERN: launch_qa_nexusai_rd518_6ec3606-shaped round-1 launcher (object-store guard, no pinned
# worktree). FOUR DELIBERATE CHANGES:
#   - EXPECTED_COMMITS is 6, not 1 — this is a chain, and the guard still scopes the delta exactly.
#   - exit 19 asserts the three DECLARED SELF-CRITICISMS W-1, W-2, W-3 by name. Same principle as the
#     RD-518 round-2 launcher's L-1/L-2 guard: a prompt that drops them commissions a victory lap over
#     the exact places the builder said its own evidence stops.
#   - exit 22 is NEW and is a PRODUCT-CODE GUARD: the diff must touch ZERO backend/ files. The branch's
#     hard stop 1 is "no backend/ file", and a launcher that takes that on trust would let a gate be
#     briefed as test-only against a tree that is not. Measured here, not read from the mail.
#   - exit 23 is NEW: the RD-516 round-2 report must EXIST on disk. The brief tells the gate its
#     verdict feeds RD-516's blocked merge; if that report is absent the gate cannot check the claim
#     it is asked to speak to, and would take the dependency from this launcher's prose instead.
#
# Shape verified at commission from the object store, not from the builder's mail:
#   6ec3606 <- e421392 <- acbe9f9 <- 7200079 <- 8f7264d <- 5f3341e, base 60c76d7 (main), 6 commits.
#   6 files changed, ALL under __tests__/, ZERO backend/.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD574' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd574_6ec3606.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd574-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd574-tier1.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd574-6ec3606-tier1/report.md"
RD516_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-6ec36065eeadb9d445d9c32c3d13826748bab651}"
BASE_SHA='60c76d7'
BRANCH='rd-574-seam-cells-s74'
EXPECTED_COMMITS=6

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-574 @ 6ec3606 (tier 1)'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The sha must be a real commit in the object store — the gate builds its own worktree from it.
T="$(git --no-optional-locks -C "$REPO" cat-file -t "$HEAD_SHA" 2>&1)"
[ "$T" = "commit" ] || { echo "REFUSING: $HEAD_SHA is not a commit in $REPO (got '$T')" >&2; exit 6; }

git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }

N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in ${BASE_SHA}..${HEAD_SHA}, found '$N' — the builder pushed again and the brief is stale" >&2; exit 8; }

# The head must be AT ORIGIN on its branch — a verdict is only reachable later if the sha is remote.
LSR="$(git --no-optional-locks -C "$REPO" ls-remote origin "$BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: $HEAD_SHA is not at refs/heads/$BRANCH on origin — that head moved or was never pushed" >&2
  printf '%s\n' "$LSR" >&2; exit 18; }

# 22 — PRODUCT-CODE GUARD. Hard stop 1 of this branch is "no backend/ file". Measured, never trusted:
# a gate briefed as test-only against a tree that touches product code is briefed wrong.
NB="$(git --no-optional-locks -C "$REPO" diff --name-only "$BASE_SHA" "$HEAD_SHA" 2>/dev/null | grep -c '^backend/')"
[ "$NB" = "0" ] || {
  echo "REFUSING: $NB backend/ file(s) in ${BASE_SHA}..${HEAD_SHA} — this branch claims to be test-only; it is not" >&2
  git --no-optional-locks -C "$REPO" diff --name-only "$BASE_SHA" "$HEAD_SHA" | grep '^backend/' >&2; exit 22; }

# 23 — the DOWNSTREAM report. The gate is told its verdict feeds RD-516's blocked merge; without that
# report on disk it cannot check the dependency and would take it from this launcher's prose.
[ -s "$RD516_REPORT" ] || { echo "REFUSING: RD-516 round-2 report absent: $RD516_REPORT — the gate cannot verify the dependency it is asked to speak to" >&2; exit 23; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

TIER='TIER 1'
grep -q "$TIER" "$BRIEF" && grep -q "$TIER" "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare '$TIER'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: prompt must name the brief path and the head, and the brief must name the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }

grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path (DELTA 40)" >&2; exit 20; }

# 19 — THE THREE DECLARED SELF-CRITICISMS. W-2 in particular says four existing cells will pass for a
# weaker reason while staying green, and that the branch's own headline property cannot see it. A
# prompt without these commissions a victory lap over the places the evidence stops.
grep -q 'W-1' "$PROMPT_FILE" && grep -q 'W-2' "$PROMPT_FILE" && grep -q 'W-3' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must carry ALL THREE declared self-criticisms W-1, W-2 and W-3 by name" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $HEAD_SHA is a commit in the object store"
  echo "  base $BASE_SHA is an ancestor; range is exactly $EXPECTED_COMMITS commits"
  echo "  head is at refs/heads/$BRANCH on origin"
  echo "  ZERO backend/ files in the delta — the test-only claim holds (22)"
  echo "  RD-516 round-2 report present for the downstream dependency (23)"
  echo "  report path named in the brief; report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier '$TIER' agrees; AgentMail key absolute (20); W-1/W-2/W-3 present (19)"
  echo "  prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@, subject"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
