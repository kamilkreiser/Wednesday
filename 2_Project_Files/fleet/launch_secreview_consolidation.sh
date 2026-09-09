#!/bin/bash
# launch_secreview_consolidation.sh — the CLOSING action of round 2: apply five seats'
# verdicts to the register in one atomic, checkable edit.
#
# 🔴 THE POINT OF THIS SCRIPT IS ITS FIRST GUARD, AND IT IS NOT PARANOIA.
# On 2026-09-09 a rung-6 ghost appeared at seat A's prompt reading "go ahead and
# consolidate", three minutes after that seat published "I hold the pen and will not start
# the consolidation until you say so". It was inert — the detector classified it and it was
# never acted on — but the round's worst outcome is a consolidation run with verdicts
# missing, and until now the only thing preventing it was discipline.
# THIS GUARD MAKES THAT SENTENCE UNEXECUTABLE: no five verdict files, no launch, rc 9.
# A discipline that has been tested once is a rule; a refusal in the path is a mechanism.
#
# SELF-LOCATING (portability rule 3, and the 2026-09-09 seat-resolver lesson).
#
# Usage: launch_secreview_consolidation.sh [--check]
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
BRIEF="$STAGED/2026-09-09_secreview-consolidation.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-consolidation.prompt.txt"
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"
JUNE="$SR_DIR/Deliverables/03_Findings_Register.md"
V="$SR_DIR/_Working/verification-2026-09"
BUILD="$SR_DIR/_Working/build-doc13.sh"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 5; }
[ -s "$JUNE" ]        || { echo "June register missing: $JUNE" >&2; exit 6; }
[ -s "$BUILD" ]       || { echo "docx build script missing — the .docx is what ships: $BUILD" >&2; exit 7; }

# ── GUARD 1: ALL FIVE VERDICTS, OR NOTHING. ───────────────────────────────────────────
MISSING=""
for f in round2-a.md round2-b.md round2-c.md round2-d.md round2-june.md; do
  [ -s "$V/$f" ] || MISSING="$MISSING $f"
done
if [ -n "$MISSING" ]; then
  echo "REFUSING: the consolidation needs all FIVE verdict files and these are missing or empty:" >&2
  for f in $MISSING; do echo "    $f" >&2; done
  echo "  A consolidation run with verdicts missing is this round's worst outcome — it writes a" >&2
  echo "  headline number that no later pass can tell was partial. Wait for the seats." >&2
  exit 9
fi

# ── GUARD 2: the register must still be UNCONSOLIDATED. Refuse to run twice. ──────────
grep -q '^| \*\*ESTATE TOTAL\*\* | \*\*23\*\*' "$REG" || {
  echo "REFUSING: the register's ESTATE TOTAL no longer reads 23 Criticals." >&2
  echo "  Either a consolidation has already run, or the file moved under us. Read it before re-running." >&2
  exit 10
}

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 11 ;;
esac
case "$PROMPT" in
  *2026-09-09_secreview-consolidation.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 12 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_consolidation: guards pass (project, brief, prompt, both registers, build script, ALL FIVE verdicts present, register still unconsolidated, directive, brief path)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 8; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
