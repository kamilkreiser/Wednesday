#!/bin/bash
# launch_secreview_verify_the_96.sh — launch the Datasec SECURITY REVIEW agent on Kam's
# 2026-09-09 commission: independently verify the 96 rows filed into §2.3.3/§2.3.4 of the
# consolidated findings register on 2026-09-08.
#
# Kam, panel, verbatim: "Let's start working on the security review."
# He asked what remained; this is the item the register itself names as the highest-value
# next action, and the only one on that list needing neither his ruling nor a live system.
#
# SELF-LOCATING (2026-07-31 portability rule 3, and the 2026-09-09 seat-resolver lesson).
# The sibling script launch_secreview_fix_verify_continue.sh hardcodes
# /Volumes/KK_T9_External_HDD/WEDNESDAY for its brief paths; this tree is TUESDAY, and a
# stored absolute path is exactly what wakes up wrong on a renamed volume
# ([[2026-08-25_travel-drive-stale-pointers]]). Derive from BASH_SOURCE instead.
#
# TRACKED ON PURPOSE (2026-09-07: a mechanism is recorded by its PATH, not its runtime id).
#
# Written via the Write tool because it contains a legitimate `cd`
# (pretooluse_no_cd.sh refuses a `cd` inside a Bash tool call).
#
# Usage: launch_secreview_verify_the_96.sh [--check]
#   --check runs every guard and exits 0 WITHOUT launching.
# Exit: 0 launched (or guards pass under --check) · 2..9 a guard refused.
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"          # .../TUESDAY/2_Project_Files/fleet
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
BRIEF="$STAGED/2026-09-09_secreview-verify-the-96.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-verify-the-96.prompt.txt"
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 8; }

# THE SUBJECT MUST STILL BE PRESENT. If another session has already verified these rows,
# this launch would commission a ghost — refuse and say so. The subject is §7 item 5's
# claim that the rows are unverified; its absence means the work is done or the file moved.
grep -q 'have NOT been' "$REG" || {
  echo "REFUSING: §7 item 5's unverified-rows claim is no longer in the register." >&2
  echo "The 96 may already be verified, or the file changed. Re-read it and re-brief." >&2
  exit 7
}

PROMPT="$(cat "$PROMPT_FILE")"

# Both clauses red-proofed individually: a blind agent should be UNLAUNCHABLE, not merely
# detectable afterwards (2026-08-06 artifact-presence-is-not-execution, rung 5/6).
case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-09_secreview-verify-the-96.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 9 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_verify_the_96: guards pass (project, brief, prompt, register, unverified-rows subject present, thinking directive, brief path named)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
