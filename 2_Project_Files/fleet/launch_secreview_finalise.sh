#!/bin/bash
# launch_secreview_finalise.sh — the finishing action on Kam's word:
#   "Complete the document and finish the analysis."
# Applies Tuesday's six rulings, settles the UI call worth two Criticals, closes the
# analysis in three buckets. NOT a new verification round.
#
# SELF-LOCATING (portability rule 3, and the 2026-09-09 seat-resolver lesson).
#
# Usage: launch_secreview_finalise.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..12 a guard refused.
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
BRIEF="$STAGED/2026-09-09_secreview-finalise.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-finalise.prompt.txt"
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"
JUNE="$SR_DIR/Deliverables/03_Findings_Register.md"
CONSOL="$SR_DIR/_Working/2026-09-09_CONSOLIDATION_REPORT.md"
BUILD="$SR_DIR/_Working/build-doc13.sh"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 5; }
[ -s "$JUNE" ]        || { echo "June register missing: $JUNE" >&2; exit 6; }
[ -s "$BUILD" ]       || { echo "docx build script missing — the .docx is what ships: $BUILD" >&2; exit 7; }

# GUARD 1 — THE CONSOLIDATION MUST HAVE RUN. This seat applies what that pass HELD;
# without its report there are no six changes to apply and the brief points at nothing.
[ -s "$CONSOL" ] || {
  echo "REFUSING: the consolidation report is missing — this seat applies what IT held." >&2
  echo "  $CONSOL" >&2
  exit 9
}

# GUARD 2 — THE REGISTER MUST BE AT THE CONSOLIDATED STATE. If it does not read 27
# Criticals, either the consolidation never landed or something has moved since, and
# applying six deltas to an unknown base is how a total silently stops reconciling.
grep -q '^| \*\*ESTATE TOTAL\*\* | \*\*27\*\*' "$REG" || {
  echo "REFUSING: the register's ESTATE TOTAL does not read 27 Criticals." >&2
  echo "  This seat applies six deltas ON TOP of the consolidated state. Re-read before running." >&2
  exit 10
}

# GUARD 3 — the held changes must still be OPEN. If the withdrawal marker is gone, a
# finalise pass has already run and this one would double-apply.
grep -q 'WITHDRAWAL HELD' "$REG" || {
  echo "REFUSING: no 'WITHDRAWAL HELD' marker in the register — the six may already be applied." >&2
  echo "  Double-applying a withdrawal removes a row twice from the tallies. Read it first." >&2
  exit 11
}

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 8 ;;
esac
case "$PROMPT" in
  *2026-09-09_secreview-finalise.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 12 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_finalise: guards pass (project, brief, prompt, both registers, build script, consolidation report present, register at 27 Criticals, withdrawals still held, directive, brief path)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 13; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
