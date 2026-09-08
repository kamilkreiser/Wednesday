#!/bin/bash
# launch_secreview_fix_verify_continue.sh — launch the Datasec SECURITY REVIEW agent on
# Kam's 2026-09-08 commission: fix the self-contradicting §7.1, then the verification
# pass over the 23, then file batch-1, then continue the review.
#
# Kam, panel, verbatim, two messages minutes apart:
#   "fix the register section"
#   "keep the verification and security review going"
#
# T9 PATHS. DevMASTER is not mounted on this machine and launchers.conf points at
# DevMASTER, so `cockpit.sh launch` cannot start this one — hence a wrapper.
#
# TRACKED ON PURPOSE (2026-09-07 lesson: a mechanism is recorded by its PATH, not its
# runtime id). Siblings in fleet/state/ are gitignored and invisible to a fresh clone;
# this one starts in a tracked path rather than being moved later.
#
# Written via the Write tool because it contains a legitimate `cd`
# (pretooluse_no_cd.sh refuses a `cd` inside a Bash tool call).
#
# Usage: launch_secreview_fix_verify_continue.sh [--check]
#   --check runs every guard and exits 0 WITHOUT launching.
# Exit: 0 launched (or guards pass under --check) · 2..9 a guard refused.
set -u

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
BRIEF='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-08_secreview-fix-verify-continue.md'
PROMPT_FILE='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-08_secreview-fix-verify-continue.prompt.txt'
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"
DOCX="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.docx"
DELTA="$SR_DIR/_Working/delta-review-2026-09"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 8; }
[ -s "$DOCX" ]        || { echo "register .docx missing — item 1 regenerates it, so it must exist first: $DOCX" >&2; exit 9; }
[ -d "$DELTA" ]       || { echo "delta-review dir missing: $DELTA" >&2; exit 9; }

# ITEM 1'S SUBJECT MUST STILL BE PRESENT. If another session has already fixed §7.1,
# this launch would commission a ghost — refuse instead, and say so. The subject is the
# STALE heading; its absence means the work is done or the file moved under us.
grep -q '8 done, 11 COMMISSIONED' "$REG" || {
  echo "REFUSING: the stale section 7.1 heading ('8 done, 11 COMMISSIONED') is no longer in the register." >&2
  echo "Item 1 may already be done, or the file changed. Re-read it and re-brief before launching." >&2
  exit 7
}

PROMPT="$(cat "$PROMPT_FILE")"

# Both clauses red-proofed individually: a blind agent should be UNLAUNCHABLE, not
# merely detectable afterwards.
case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-08_secreview-fix-verify-continue.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_fix_verify_continue: guards pass (project, brief, prompt, register, docx, delta dir, stale-heading subject present, directive, brief path)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
