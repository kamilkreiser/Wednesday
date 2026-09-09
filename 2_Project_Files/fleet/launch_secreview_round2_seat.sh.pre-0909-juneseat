#!/bin/bash
# launch_secreview_round2_seat.sh — launch ONE parallel Security Review round-2 seat.
#
# Kam, panel 2026-09-09, verbatim: "yes, run multiple agents on the security review."
#
# ONE SCRIPT, PARAMETERISED BY SEAT — not three near-copies. Three copies of a launcher
# drift, and the drift is invisible until a seat boots wrong; that is the reasoning in
# Launch_Tuesday.command's own header, applied here.
#
# SELF-LOCATING (portability rule 3, and the 2026-09-09 seat-resolver lesson).
#
# Usage: launch_secreview_round2_seat.sh <b|c|d> [--check]
# Exit: 0 launched (or guards pass under --check) · 2..12 a guard refused.
set -u

SEAT="${1:-}"
case "$SEAT" in
  b|c|d) ;;
  *) echo "usage: launch_secreview_round2_seat.sh <b|c|d> [--check]" >&2; exit 2 ;;
esac

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
METHOD="$STAGED/2026-09-09_secreview-round2-parallel-method.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-round2-seat-$SEAT.prompt.txt"
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"
R1="$SR_DIR/_Working/2026-09-09_VERIFY96_REPORT.md"
OUTDIR="$SR_DIR/_Working/verification-2026-09"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 3; }
[ -s "$METHOD" ]      || { echo "shared method brief missing or empty: $METHOD" >&2; exit 4; }
[ -s "$PROMPT_FILE" ] || { echo "seat prompt missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 6; }
[ -s "$R1" ]          || { echo "round-1 report missing — this round builds on it: $R1" >&2; exit 7; }
[ -d "$OUTDIR" ]      || { echo "verdict directory missing: $OUTDIR" >&2; exit 8; }

# ROUND 1 MUST HAVE LANDED, or this round builds on a state that never existed.
grep -q '^| \*\*ESTATE TOTAL\*\* | \*\*23\*\*' "$REG" || {
  echo "REFUSING: the register's ESTATE TOTAL does not read 23 Criticals — round 1's H-D1 ruling is not applied." >&2
  exit 9
}

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 10 ;;
esac
case "$PROMPT" in
  *2026-09-09_secreview-round2-parallel-method.md*) ;;
  *) echo "prompt does not name the shared method brief — refusing to launch a blind agent" >&2; exit 11 ;;
esac
# THE PARTITION-SAFETY CLAUSE IS STRUCTURALLY REQUIRED. Four seats share one register;
# a seat launched without this sentence is the one thing that can destroy the round's
# work, so it must be UNLAUNCHABLE rather than merely detectable afterwards.
case "$PROMPT" in
  *"DO NOT EDIT THE REGISTER"*) ;;
  *) echo "prompt does not carry the DO-NOT-EDIT-THE-REGISTER clause — refusing: four seats share that file" >&2; exit 12 ;;
esac

if [ "${2:-}" = "--check" ]; then
  echo "launch_secreview_round2_seat $SEAT: guards pass (project, method brief, seat prompt, register, round-1 report, verdict dir, estate=23, directive, method path, no-edit clause)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 13; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
