#!/bin/bash
# launch_qa_hpsm_composer_a06ada3.sh — cross-project QA agent, TIER 1 gate, round 2 of 2, on the
# Datasec/HPSM Policy Composer work packages WP0 + WP1 + WP2, local repo main @ a06ada3
# (pushed to the private datasecau/HPSM-light at the same SHA on 2026-09-11 08:25).
#
# WHY TIER 1: WP2 carries row-level security and tenant isolation, WP0 carries the secret-scan
# control and the no-cloud egress proof — security surfaces
# (learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap). Tuesday scores session 33 on this
# verdict, and WP3/WP4 are built on this head.
#
# PATTERN: launch_qa_nexusai_s51remed.sh. Differences, each deliberate:
#   - the tester CLONES the Composer's local repo into its own mktemp -d, so the builder's working
#     tree is irrelevant to the gate — no "dirty worktree" guard (a builder seat may be live there);
#   - the E8 SOW text lives OUTSIDE the repo (gitignored source); CI's citation leg cannot run
#     without it, so its absence is refused here rather than discovered as a NOT RUN;
#   - the shared Docker daemon may be in use by another Datasec seat; the brief gives the tester its
#     own compose project name and edge port.
#
# ABSOLUTE PATHS ON PURPOSE (the pickup's red-proof note): a scratch copy of this file keeps
# pointing at the real brief, so a red-proof reaches the guard it means to test.
# TRACKED in launchers/ (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
# Written with the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_hpsm_composer_a06ada3.sh [--check]   (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..14 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer'
SOW='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md'
BRANCH='refs/heads/main'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-0c3078e8398d016cbbf250712da56585938d734f}"
EXPECTED_COMMITS=6

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ]   || { echo "repository under test missing: $REPO" >&2; exit 5; }

# The brief describes exactly this head. A builder commit after the brief was written means
# the brief describes a tree nobody is gating — refuse and re-brief rather than gate a guess.
GOT="$(git --no-optional-locks -C "$REPO" rev-parse "$BRANCH" 2>&1)"
if [ "$GOT" != "$HEAD_SHA" ]; then
  echo "REFUSING: $BRANCH is at '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6
fi
N="$(git --no-optional-locks -C "$REPO" rev-list --count "$HEAD_SHA" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || {
  echo "REFUSING: expected $EXPECTED_COMMITS commits reachable from $HEAD_SHA, found '$N'" >&2; exit 7; }

[ -s "$SOW" ] || { echo "REFUSING: E8 SOW text missing at $SOW — CI's citation leg cannot run" >&2; exit 8; }

# The core measurements run containers. Without a daemon the agent would substitute a source
# read for them, which is the substitution this gate exists to stop.
docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — the stack and the database tests cannot run" >&2; exit 9; }

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 10; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 11; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 12; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: brief or prompt does not name the head $HEAD_SHA" >&2; exit 13; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to —" >&2
  echo "the agent has no inbox, and a Datasec verdict mailed to the Secuura seat is a cross-client leak" >&2
  exit 14; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $BRANCH == $HEAD_SHA (local); $EXPECTED_COMMITS commits reachable"
  echo "  E8 SOW text present; docker responding; brief and prompt agree on TIER 1"
  echo "  prompt: thinking directive, brief path, head SHA, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 15; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
