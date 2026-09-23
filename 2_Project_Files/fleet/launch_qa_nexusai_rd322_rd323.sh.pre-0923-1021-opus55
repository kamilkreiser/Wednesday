#!/bin/bash
# launch_qa_nexusai_rd322_rd323.sh — cross-project QA agent, TIER 1 gate on
# Datasec/NexusAI RD-322 + RD-323 (TIER 2, two subjects) (rd-361-round4-s45 @ 400718f).
#
# Round 4 of a class Kam capped at two, bent for round 3, and then authorised
# explicitly. A NO GO here goes to Kam, not to a round 5.
#
# T9 PATHS. DevMASTER is not mounted, and launchers.conf points at DevMASTER, so
# cockpit.sh launch cannot start this one.
#
# TRACKED ON PURPOSE, like its security-review sibling: every wrapper in
# fleet/state/ is gitignored and so survives no clone and no `git grep`
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
# New mechanisms start in the right place; the existing wrappers' move is owed.
#
# Written via the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_nexusai_rd322_rd323.sh [--check]   (--check runs the guards, launches nothing)
# Exit: 0 launched / guards pass · 2..9 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_nexusai-rd322-rd323-tier2.md'
PROMPT_FILE='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_nexusai-rd322-rd323-tier2.prompt.txt'
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
HEAD_SHA='432617a'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 8; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that
# was never pushed spends a session proving nothing — and the failure looks like a
# finding rather than like a missing branch.
if ! git -C "$REPO" ls-remote origin 'refs/heads/rd-322-root-guard-vacuity-s45' 2>/dev/null | grep -q "^${HEAD_SHA}"; then
  echo "head $HEAD_SHA is not at refs/heads/rd-322-root-guard-vacuity-s45 on origin — refusing to gate a SHA that is not there" >&2
  exit 9
fi

# SECOND SUBJECT. This gate has TWO heads and the first draft of this wrapper
# verified only one — a guard that covers half its subject. Both are checked.
HEAD_SHA_2='99fb518'
if ! git -C "$REPO" ls-remote origin 'refs/heads/rd-323-scheduler-failure-vocabulary-s45' 2>/dev/null | grep -q "^${HEAD_SHA_2}"; then
  echo "head $HEAD_SHA_2 is not at refs/heads/rd-323-scheduler-failure-vocabulary-s45 on origin — refusing to gate a SHA that is not there" >&2
  exit 11
fi

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-07_nexusai-rd322-rd323-tier2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_nexusai_rd322_rd323: guards pass (QA dir, brief, prompt, repo, BOTH heads on origin, directive, brief path)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
