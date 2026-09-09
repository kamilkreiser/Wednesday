#!/bin/bash
# launch_secreview_round2_structure.sh — Kam's 2026-09-09 proofread-and-reformat round.
#
# Guards exist because this round's failure modes are all SILENT: a missing model
# document produces a plausible reformat matched to nothing; a missing build script
# produces a .md nobody can ship; and the register's totals moving is how a
# presentation pass quietly becomes a re-analysis.
#
# SELF-LOCATING (portability rule 3; the 2026-09-09 seat-resolver lesson).
# Usage: launch_secreview_round2_structure.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..12 a guard refused.
set -u
SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR="${SECREVIEW_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review}"
BRIEF="$STAGED/2026-09-09_secreview-round2-structure.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-round2-structure.prompt.txt"
REG="$SR_DIR/Deliverables/13A_HPAM_Consolidated_Findings_Register_2026-09.md"
REGB="$SR_DIR/Deliverables/13B_Datasec_Products_Consolidated_Findings_Register_2026-09.md"
MODEL="$SR_DIR/Test Related Documents/Datasec - Penetration Test Report - 1.0.pdf"
JUNE="$SR_DIR/Deliverables/03_Findings_Register.md"
BUILD="$SR_DIR/_Working/build-doc13.sh"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 5; }
[ -s "$MODEL" ]       || { echo "MyEmpire model report missing — a reformat with no model matches nothing: $MODEL" >&2; exit 6; }
[ -s "$JUNE" ]        || { echo "June register missing (the in-house section order): $JUNE" >&2; exit 7; }
[ -s "$BUILD" ]       || { echo "docx build script missing — the rendered file is what ships: $BUILD" >&2; exit 8; }

[ -s "$REGB" ] || { echo "13B register missing: $REGB" >&2; exit 14; }
# GUARD: both registers must still be the round-1 output (342 across the pair).
A=$(grep -c 'ESTATE TOTAL' "$REG"); B=$(grep -c 'ESTATE TOTAL' "$REGB")
[ "$A" -ge 1 ] && [ "$B" -ge 1 ] || {
  echo "REFUSING: one of the two registers no longer carries an ESTATE TOTAL row." >&2
  echo "  Round 1 output is what this round edits. Read both before re-running." >&2
  exit 9; }

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 11 ;; esac
case "$PROMPT" in *2026-09-09_secreview-round2-structure.md*) ;; *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 12 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "prompt does not say where to send the verdict — a round that cannot report is a round that did not run" >&2; exit 13 ;; esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_round2_structure: guards pass (project, brief, prompt, BOTH round-1 registers present with ESTATE TOTAL rows, MyEmpire model, build script, directive, brief path, mail destination)"
  exit 0
fi
cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 10; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
