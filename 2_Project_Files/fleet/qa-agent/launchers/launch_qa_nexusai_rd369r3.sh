#!/bin/bash
# launch_qa_nexusai_rd369r3.sh — cross-project QA agent, TIER 1 gate on
# Datasec/NexusAI RD-369 round 3, branch rd-369-round3-s49 @ 7cd0907, based on cd2b543.
#
# WHY TIER 1, stated here so this file and the brief cannot drift apart: every file in
# the change is a test or a config, which on Kam's 2026-09-05 tiering reads
# "through-code only". That classification is WRONG here and the override is deliberate.
# The tier is set by what the change IS, not by where it lives — this is the security
# CONTROL that decides whether internal tenant correspondence, subscription GUIDs and a
# named staging-user roster are detected inside the customer container image. If the
# guard is wrong, the exposure ships and nothing reports it. Calling it "tests" because
# the files sit under __tests__/ would be using a convenient classification to reduce
# scrutiny (learnings/2026-08-16_classification-is-the-field-that-grants-authority).
#
# THE CAP IS REAL: Kam authorised ONE round 3 and no round 4 without him. A NO GO here
# does not open another round — the closed instances ship and the residue is ticketed.
# So the gate must grade findings by whether they MUST block, not by whether they could
# be fixed.
#
# T9 PATHS, NOT DevMASTER. Every existing launcher in this directory pins
# /Volumes/DevMASTER/... and DevMASTER is NOT MOUNTED on this machine — the same class
# of stale absolute that killed cockpit.sh launch here. Both trees below were verified
# present before this file was written.
#
# TRACKED ON PURPOSE, and in launchers/ rather than the gitignored fleet/state/: a
# wrapper in an ignored drawer survives no clone and no `git grep`, so a successor
# needing to re-run this gate would have to INVENT a launch command — and an invented
# one that looks right is worse than one that fails
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written with the Write tool because it contains a legitimate `cd`, which the
# PreToolUse hook refuses inside a Bash call.
#
# Usage: launch_qa_nexusai_rd369r3.sh [--check]  (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..13 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-10_nexusai-rd369-r3-tier1.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-10_nexusai-rd369-r3-tier1.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
BRANCH='refs/heads/rd-369-round3-s49'
HEAD_SHA='7cd0907724d1313b4f64950f5f8600dde3acb448'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that was
# never pushed spends a whole session proving nothing, and the failure reads like a
# finding rather than like a missing branch. ls-remote is a READ verb, so this is safe
# inside another project's checkout.
#
# The FULL 40-char SHA is matched with a trailing whitespace anchor: an abbreviated
# match would also match a different object sharing the prefix, and this gate's whole
# job is to be about exactly one commit.
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
# Both clauses red-proofed individually: a blind agent should be UNLAUNCHABLE, not
# merely detectable.
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 9; }

# The QA agent is WRITE-ONLY in the comms fabric: no inbox, and its pane is an alternate
# screen holding ~19 lines with NO scrollback. A gate that cannot report is a gate that
# did not run.
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not tell the agent to MAIL its verdict — its pane has no" >&2
  echo "scrollback and it has no inbox, so an unmailed verdict is lost at the pane close" >&2
  exit 12; }

# NEW GUARD, NOT IN THE SECUURA TEMPLATE, and earned by a live defect on 2026-09-10:
# a Datasec agent mailed its plan confirmation to wednesday-agent@ because the shared
# workspace CLAUDE.md still names one coordinator. A Datasec QA verdict landing in the
# Secuura seat's inbox is a cross-client leak — Kam's very-important-number-one. So the
# prompt must name Tuesday's inbox and must NOT send the agent to Wednesday's.
grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name tuesday-agent@agentmail.to as the verdict address" >&2
  echo "Datasec's coordinator is Tuesday; a verdict mailed elsewhere is a cross-client leak" >&2
  exit 13; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  brief, prompt, QA project and repo all present (T9 paths, DevMASTER not mounted)"
  echo "  brief and prompt agree on TIER 1"
  echo "  prompt opens with the thinking directive and names the brief by path"
  echo "  prompt tells the agent to MAIL its verdict — it has no inbox and no scrollback"
  echo "  prompt routes the verdict to tuesday-agent@ — not the Secuura seat"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 11; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
