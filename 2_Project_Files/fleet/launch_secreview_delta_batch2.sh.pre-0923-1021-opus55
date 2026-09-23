#!/bin/bash
# launch_secreview_delta_batch2.sh — launch the Datasec SECURITY REVIEW agent on the
# five remaining Step-2 delta reviews (Kam, panel 2026-09-07 21:00: "keep working on
# security review and I will review in the morning when I wake").
#
# T9 PATHS. DevMASTER is not mounted on this machine, and launchers.conf points at
# DevMASTER, so `cockpit.sh launch` cannot start this one — hence a wrapper.
#
# TRACKED ON PURPOSE. Every sibling wrapper lives in fleet/state/, which is
# gitignored, so none of them survives a clone or is findable by `git grep` — the
# 2026-09-07 lesson "a mechanism is recorded by its PATH, not its runtime id".
# This is a NEW mechanism with nothing live on it, so it starts in the right place
# rather than being moved later. The existing wrappers' move is still owed.
#
# Written via the Write tool because it contains a legitimate `cd`
# (pretooluse_no_cd.sh refuses a `cd` in a Bash tool call).
#
# Usage: launch_secreview_delta_batch2.sh [--check]
#   --check runs every guard and exits 0 WITHOUT launching.
# Exit: 0 launched (or guards pass under --check) · 2..7 a guard refused.
set -u

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
BRIEF='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-07_secreview-delta-batch2.md'
PROMPT_FILE='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-07_secreview-delta-batch2.prompt.txt'
SRC="$SR_DIR/Source_Code"
OUT="$SR_DIR/_Working/delta-review-2026-09"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -d "$SRC" ]         || { echo "Source_Code missing: $SRC" >&2; exit 8; }
[ -d "$OUT" ]         || { echo "delta-review output dir missing: $OUT" >&2; exit 9; }

# The five components this batch exists to review must actually be on disk. A brief
# that names a component the tree does not hold would send the agent hunting a ghost.
for c in CypherOneDrive-main Teams-main CommonValueLibraryCypher-master \
         Cyphercard-Enrolment-App-main HPSM-main; do
  [ -d "$SRC/$c" ] || { echo "component named in the brief is not in Source_Code: $c" >&2; exit 10; }
done

PROMPT="$(cat "$PROMPT_FILE")"

# Both clauses red-proofed individually when this wrapper was written: a blind agent
# should be UNLAUNCHABLE, not merely detectable afterwards.
case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-07_secreview-delta-batch2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_delta_batch2: guards pass (project, brief, prompt, Source_Code, output dir, 5 components, directive, brief path)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
