#!/bin/bash
# launch_secreview_round2.sh — ROUND 2 of 2: re-derive each finding's CVSS vector at source,
# then score. Commissioned on the agent's own round-1 recommendation.
#
# SELF-LOCATING (portability rule 3, and the 2026-09-09 seat-resolver lesson).
# Usage: launch_secreview_round2.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..9 a guard refused.
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review'
BRIEF="$STAGED/2026-09-09_secreview-round2-vectors-at-source.md"
PROMPT_FILE="$STAGED/2026-09-09_secreview-round2-vectors-at-source.prompt.txt"
REG="$SR_DIR/Deliverables/13_Consolidated_Findings_Register_2026-09.md"
R1="$SR_DIR/_Working/2026-09-09_VERIFY96_REPORT.md"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -s "$REG" ]         || { echo "register missing: $REG" >&2; exit 8; }
[ -s "$R1" ]          || { echo "round-1 report missing — this round builds on it: $R1" >&2; exit 4; }

# GUARD A — ROUND 1 MUST HAVE LANDED. If the estate row does not read 23 Criticals, the H-D1
# ruling is not in the register and round 2 would build on a state that never existed.
grep -q '^| \*\*ESTATE TOTAL\*\* | \*\*23\*\*' "$REG" || {
  echo "REFUSING: the register's ESTATE TOTAL does not read 23 Criticals." >&2
  echo "Round 1's H-D1 ruling is not applied, or the file changed. Re-read before launching round 2." >&2
  exit 7
}

# GUARD B — WORK MUST REMAIN. If nothing is pending, this round would commission a ghost.
grep -qi 'pending' "$REG" || {
  echo "REFUSING: no 'pending' rows remain in the register — round 2 has no subject." >&2
  exit 6
}

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 9 ;;
esac
case "$PROMPT" in
  *2026-09-09_secreview-round2-vectors-at-source.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 10 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_round2: guards pass (project, brief, prompt, register, round-1 report, estate=23 so round 1 landed, work still pending, directive, brief path)"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 11; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
