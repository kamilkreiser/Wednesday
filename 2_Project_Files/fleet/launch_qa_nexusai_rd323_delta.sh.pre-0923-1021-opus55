#!/bin/bash
# launch_qa_nexusai_rd323_delta.sh — cross-project QA agent, TIER 2 gate on the
# Datasec/NexusAI RD-323 DELTA (rd-323-scheduler-failure-vocabulary-s45,
# 99fb518..1b6bedb).
#
# WHY: RD-323's GO-with-findings was taken on 99fb518. RD-323-F-1's fix landed
# WITH the change on Wednesday's instruction, so the head moved to 1b6bedb and
# no verdict describes what would ship. Round 1 of this class; cap not near.
#
# T9 PATHS. DevMASTER is not mounted, and launchers.conf points at DevMASTER, so
# cockpit.sh launch cannot start this one.
#
# TRACKED ON PURPOSE: every wrapper in fleet/state/ is gitignored and so
# survives no clone and no `git grep`
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written via the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_nexusai_rd323_delta.sh [--check]   (--check runs the guards, launches nothing)
# Exit: 0 launched / guards pass · 2..11 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_nexusai-rd323-delta-tier2.md'
PROMPT_FILE='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_nexusai-rd323-delta-tier2.prompt.txt'
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
HEAD_SHA='1b6bedb'
BASE_SHA='99fb518'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 8; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that
# was never pushed spends a session proving nothing — and the failure looks like a
# finding rather than like a missing branch.
if ! git -C "$REPO" ls-remote origin 'refs/heads/rd-323-scheduler-failure-vocabulary-s45' 2>/dev/null | grep -q "^${HEAD_SHA}"; then
  echo "head $HEAD_SHA is not at refs/heads/rd-323-scheduler-failure-vocabulary-s45 on origin — refusing to gate a SHA that is not there" >&2
  exit 9
fi

# The BASE must be an ancestor of the head, or "the delta" names a range that is
# not the one the previous gate's verdict sits under. This is the whole scoping
# claim of the brief, so it is a guard and not a sentence.
if ! git -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null; then
  echo "$BASE_SHA is not an ancestor of $HEAD_SHA — the delta range in the brief is wrong; refusing" >&2
  exit 10
fi

# The range must be exactly the one commit the brief describes. If the builder
# pushed again between the brief being written and this launch, the brief's
# "one commit, three files, 108 insertions" is stale and the gate would be
# scoped by a sentence rather than by the tree.
N=$(git -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>/dev/null || echo -1)
if [ "$N" != "1" ]; then
  echo "expected exactly 1 commit in ${BASE_SHA}..${HEAD_SHA}, found $N — the brief is stale; refusing" >&2
  exit 11
fi

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-08_nexusai-rd323-delta-tier2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_nexusai_rd323_delta: guards pass (QA dir, brief, prompt, repo, head $HEAD_SHA on origin, $BASE_SHA is an ancestor, range is exactly 1 commit, directive, brief path)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
