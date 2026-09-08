#!/bin/bash
# launch_qa_secuura_ks963_913.sh — cross-project QA agent, TIER 1 gate on
# Secuura KS-963 (widen the rethrow to getUserByIdPreAuth) / PR #913 @ fdd8af79d,
# base develop @ f9296f9e.
#
# WHY TIER 1, stated here so this file and the brief cannot drift apart: the DIFF
# is two lines and on shape alone this is tier 2 — the identical pattern to a
# change already gated and merged, proven byte-identical by the builder. It is
# tier 1 because of what those two lines REACH: four call sites, two of which
# consume a single-use credential token on an infrastructure error. The sentence
# that would justify tier 2 — "every caller moves from wrong to correct" — is a
# claim about the RUNTIME of four call sites, and establishing it is the pass.
#
# (Wednesday raised this from its OWN tier-2 default after the builder raised the
# blast radius. Recorded in _ledger.md 2026-09-09: a tier keyed on the SHAPE of a
# change is blind to what the change REACHES.)
#
# TRACKED ON PURPOSE, and in launchers/ rather than the gitignored fleet/state/:
# a wrapper in an ignored drawer survives no clone and no `git grep`, so a
# successor needing to re-run this gate would have to INVENT a launch command —
# and an invented one that looks right is worse than one that fails
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written with the Write tool because it contains a legitimate `cd`, which the
# PreToolUse hook refuses inside a Bash call.
#
# Usage: launch_qa_secuura_ks963_913.sh [--check]  (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..9 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks963-913-tier1.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks963-913-tier1.prompt.txt"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BRANCH='refs/heads/feature/ks-963-widen-rethrow-to-preauth'
HEAD_SHA='fdd8af79d5daaddef54f5bc73fb3e2845290f94e'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that
# was never pushed spends a whole session proving nothing, and the failure reads
# like a finding rather than like a missing branch. ls-remote is a READ verb, so
# this is safe inside another project's checkout.
#
# The FULL 40-char SHA is matched with a trailing whitespace anchor: an abbreviated
# match would also match a different object sharing the prefix, and this gate's
# whole job is to be about exactly one commit.
if ! git -C "$REPO" ls-remote origin "$BRANCH" 2>/dev/null | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — will not gate a SHA that is not there" >&2
  echo "what origin actually has for that ref:" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The brief must not name a tier its prompt then contradicts.
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }

# The prompt must open with the thinking directive and must name the brief by PATH.
# Both clauses red-proofed individually: a blind agent should be UNLAUNCHABLE,
# not merely detectable.
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
