#!/bin/bash
# launch_qa_nexusai_s51remed.sh — cross-project QA agent, TIER 1 gate on the
# Datasec/NexusAI marketplace remediation branch s51-marketplace-remediation @ ed8b208,
# based on cd2b543 (origin main). Kam builds the Azure Marketplace containers from this
# head on 2026-09-11, so this verdict is what that build rests on.
#
# WHY TIER 1: .dockerignore is the control that decides whether key and env files enter
# the customer image; the masking change sits on the first-run page that handles Entra
# identifiers; the screenshots are public listing assets that carried real surnames.
# Security surface plus a human handover (learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap).
#
# THE HEAD IS LOCAL-ONLY, AND THAT CHANGES ONE GUARD FROM THE rd369r3 PATTERN.
# That launcher refused unless the SHA was on origin. This branch is NOT pushed, and
# Tuesday must not push it: a push is a write verb into another project's repo
# (learnings/2026-09-06_other-projects-repos-are-read-only-git-verbs-that-write).
# So the guard pins the exact 40-char SHA at the LOCAL branch ref instead, with
# read-only git (--no-optional-locks, so not even the index stat cache is written).
#
# TRACKED ON PURPOSE in launchers/ (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
# Written with the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_nexusai_s51remed.sh [--check]   (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..14 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-10_nexusai-s51remed-ed8b208-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-10_nexusai-s51remed-ed8b208-tier1.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed'
BRANCH='refs/heads/s51-marketplace-remediation'
HEAD_SHA='ed8b208dccccb74d449227e3b968eab1b30bd0f5'
BASE_SHA='cd2b54397b0e'
EXPECTED_COMMITS=6

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$WT" ]          || { echo "worktree under test missing: $WT" >&2; exit 5; }

# The exact head must be what the local branch points at — a builder commit after this
# brief was written would make the brief describe a tree nobody is gating.
GOT="$(git --no-optional-locks -C "$WT" rev-parse "$BRANCH" 2>&1)"
if [ "$GOT" != "$HEAD_SHA" ]; then
  echo "REFUSING: $BRANCH is at '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6
fi

# The range the brief describes must be the range in the tree.
git --no-optional-locks -C "$WT" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }
N="$(git --no-optional-locks -C "$WT" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || {
  echo "REFUSING: expected $EXPECTED_COMMITS commits in ${BASE_SHA}..${HEAD_SHA}, found '$N'" >&2; exit 8; }

# Uncommitted work in the worktree would mean the head is not the whole story.
DIRTY="$(git --no-optional-locks -C "$WT" status --porcelain 2>&1)"
[ -z "$DIRTY" ] || { echo "REFUSING: the worktree has uncommitted changes:" >&2; echo "$DIRTY" >&2; exit 9; }

# The core measurement is building and enumerating the image. Without a daemon the agent
# would substitute a source read for it, which is the substitution this gate exists to stop.
docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — the image cannot be built and enumerated" >&2; exit 10; }

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 11; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 12; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 13; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to —" >&2
  echo "the agent has no inbox, and a Datasec verdict mailed to the Secuura seat is a cross-client leak" >&2
  exit 14; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $BRANCH == $HEAD_SHA (local; not pushed, deliberately not pushed by Tuesday)"
  echo "  $BASE_SHA is an ancestor; range is exactly $EXPECTED_COMMITS commits; worktree clean"
  echo "  docker responding; brief and prompt agree on TIER 1"
  echo "  prompt: thinking directive, brief path, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 15; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
