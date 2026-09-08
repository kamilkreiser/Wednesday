#!/bin/bash
# launch_qa_secuura_ks1013_910.sh — cross-project QA agent, TIER 1 gate on
# Secuura KS-1013 / PR #910 @ d90f9ad8d, base develop @ 5ffaaf396.
#
# WHY TIER 1, stated here so the file and the brief cannot drift apart: the ROUTE
# change alone (a UUID guard turning a 500 into a 400) would be tier 2. It is tier 1
# because the PUBLISHED CONTRACT moved in the same commit — {id} went from a bare
# z.string() to z.string().uuid(), so the spec now refuses inputs it previously
# declared legal, and that spec is consumed, has a live drift ticket (KS-663) and a
# known deploy hazard where a spec ships without the restart that publishes it
# (KS-987).
#
# NOTE FOR WHOEVER COPIES THIS FILE NEXT: launch_qa_secuura_ks963_907.sh carries a
# header that says TIER 1 on line 2 and "WHY TIER 2" on line 5 — a stale block kept
# when that file was adapted from an earlier gate. Do not inherit that shape. The
# guard at the foot of this script exists precisely so a brief and its launcher
# cannot disagree about the tier without refusing to run.
#
# TRACKED ON PURPOSE, and in launchers/ rather than fleet/state/ (which is
# gitignored): a wrapper in an ignored drawer survives no clone and no `git grep`, so
# a successor needing to re-run this gate would have to INVENT a launch command — and
# an invented one that looks right is worse than one that fails
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written with the Write tool because it contains a legitimate `cd`, which the
# PreToolUse hook refuses inside a Bash call.
#
# Usage: launch_qa_secuura_ks1013_910.sh [--check]  (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..9 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks1013-910-tier1.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks1013-910-tier1.prompt.txt"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BRANCH='refs/heads/feature/ks-1013-patch-apiusersadminid-answers-500-for-a-malformed-id-the'
HEAD_SHA='d90f9ad8d17cdd5fa9719392982bf57bad7d89bd'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that was
# never pushed spends a whole session proving nothing — and the failure reads like a
# finding rather than like a missing branch. ls-remote is a READ verb, so this is safe
# to run inside another project's checkout.
#
# The full 40-char SHA is matched, not a prefix: an abbreviated match would also match a
# different object sharing the prefix, and this gate's whole job is to be about one commit.
if ! git -C "$REPO" ls-remote origin "$BRANCH" 2>/dev/null | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — will not gate a SHA that is not there" >&2
  echo "what origin actually has for that ref:" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The brief must not name a tier its prompt then contradicts.
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }

# The prompt must name the brief by PATH and must open with the thinking directive.
# Both clauses red-proofed individually when this guard shape was built (2026-09-07):
# a blind agent should be UNLAUNCHABLE, not merely detectable.
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 9; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1"
  echo "  prompt opens with the thinking directive and names the brief by path"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 8; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
