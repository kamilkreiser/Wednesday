#!/bin/bash
# launch_qa_secuura_ks754_914.sh — cross-project QA agent, TIER 1 gate on
# Secuura KS-1004 (a document carrying a txHash can now be marked anchor-failed)
# / PR #912 @ ae8751f38, base develop @ f9296f9e, merge-base e559f7bb.
#
# WHY TIER 1, stated here so this file and the brief cannot drift apart: the code
# commit drops a FOREIGN KEY from data_subject_requests.processed_by and converts a
# swallowed DB error into a THROWN one on a GDPR Article 17 erasure path whose caller
# previously ignored the return. Either half alone is tier 1 on Kam's tiering; the
# erasure half is the one to spend the pass on, because an erasure that used to
# complete may now abort AFTER the deletions have happened.
#
# This gate is on the critical path: every author in the repo, Peter and Stuart
# included, is push-blocked until #914 -> #915 -> develop lands. That is a reason to
# be thorough, not a reason to be quick.
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
# Usage: launch_qa_secuura_ks754_914.sh [--check]  (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..9 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks754-914-tier1.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-09_secuura-ks754-914-tier1.prompt.txt"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BRANCH='refs/heads/feature/ks-754-widen-processed-by-to-text'
HEAD_SHA='311dc1ae474f5a1d37f30147d810a2c7583efa6b'
MERGE_BASE='f9296f9eadb26c52d47116457de99fcfc44ce4dd'

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

# THIS GATE'S OWN GUARD, and it is not in the ks963 template: the brief tells the
# agent to diff against the MERGE-BASE, because this branch is behind develop and
# a diff against develop shows nine files instead of three. If the merge-base has
# moved, the brief's diffstat, its file list and its whole census are about a
# different change — so refuse rather than send an agent to verify stale numbers.
ACTUAL_MB="$(git -C "$REPO" merge-base f9296f9eadb26c52d47116457de99fcfc44ce4dd "$HEAD_SHA" 2>/dev/null)"
if [ "$ACTUAL_MB" != "$MERGE_BASE" ]; then
  echo "REFUSING: merge-base is now '$ACTUAL_MB', brief was written against '$MERGE_BASE'" >&2
  echo "the brief's diffstat and inFlight census describe a different change — rewrite it" >&2
  exit 10
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

# ADDED 2026-09-09 AFTER THIS GATE'S OWN FIRST RUN LOST ITS VERDICT TO A PANE.
# The QA agent is WRITE-ONLY in the comms fabric: it has no inbox, and its pane is an
# alternate screen holding ~19 lines with NO scrollback. This launcher's first run
# produced a 13 KB tier-1 verdict with a BLOCKER in it, and the prompt never told the
# agent where to SEND it — so the only copy was recoverable solely from the agent's
# session transcript. A gate that cannot report is a gate that did not run.
# (The working ks963_913 prompt carried this line and this one had simply omitted it.)
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not tell the agent to MAIL its verdict — its pane has no" >&2
  echo "scrollback and it has no inbox, so an unmailed verdict is lost at the pane close" >&2
  exit 12; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE — the brief's diffstat and census still describe this change"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1"
  echo "  prompt opens with the thinking directive and names the brief by path"
  echo "  prompt tells the agent to MAIL its verdict — it has no inbox and no scrollback"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 11; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
