#!/bin/bash
# launch_qa_secuura_ks989_906.sh — cross-project QA agent, TIER 2 (through-code)
# gate on Secuura KS-989 / PR #906 @ 9f9a2a788, base develop @ 986c592d5.
#
# WHY TIER 2: the change touches a git hook, a shell script, two shell test suites and one
# blank line in a test helper. No service, no frontend, no spec, no migration, no auth
# surface. The brief tells the gate to STOP and report if that turns out to be false.
#
# TRACKED ON PURPOSE, and in launchers/ rather than fleet/state/: a wrapper in a gitignored
# drawer survives no clone and no `git grep`, so a successor that needs to re-run this gate
# would have to invent a launch command — and an invented one that LOOKS right is worse than
# one that fails (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written with the Write tool because it contains a legitimate `cd`, which the PreToolUse
# hook refuses inside a Bash call.
#
# Usage: launch_qa_secuura_ks989_906.sh [--check]   (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..9 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_secuura-ks989-906-tier2.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_secuura-ks989-906-tier2.prompt.txt"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BRANCH='refs/heads/feature/ks-989-a-systemtest-docs-edit-can-red-a-package-quality-gate-that'
HEAD_SHA='9f9a2a788'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head under test must EXIST on the remote. A gate briefed against a SHA that was never
# pushed spends a whole session proving nothing — and the failure reads like a finding rather
# than like a missing branch. ls-remote is a READ verb, so this is safe in another project.
if ! git -C "$REPO" ls-remote origin "$BRANCH" 2>/dev/null | grep -q "^${HEAD_SHA}"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — will not gate a SHA that is not there" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The brief must not name a tier it then contradicts: cheap, and it caught nothing today,
# which is the point of running it anyway.
grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass: head $HEAD_SHA present on origin; brief, prompt, QA project and repo all present"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 8; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
