#!/bin/bash
# launch_secreview_appendix_tables.sh — Kam's 2026-09-10 11:25 round on the two consolidated
# registers: sub-item spacing, table widths, and the EVIDENCE APPENDIX (project/file/line per
# finding).
#
# WHY THE GUARDS ARE WHAT THEY ARE. Every failure mode in this round is silent:
#   - the appendix is only as good as the seed evidence, so a missing seed directory produces
#     a plausible appendix built from prose, with invented line numbers nobody will question
#     until they open the file;
#   - a missing build script produces a .md that cannot ship, and the .docx is what Kam reads;
#   - the register's totals moving is how a presentation round quietly becomes a re-analysis;
#   - and a verdict mailed to the wrong coordinator is a Datasec document in the Secuura seat's
#     inbox, which is Kam's very-important-number-one.
#
# T9 PATHS. DevMASTER is not mounted on this machine; every path below was verified present
# before this file was written. SELF-LOCATING per portability rule 3.
#
# Usage: launch_secreview_appendix_tables.sh [--check]   (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..14 a guard refused
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR="${SECREVIEW_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review}"
BRIEF="$STAGED/2026-09-10_secreview-appendix-and-tables.md"
PROMPT_FILE="$STAGED/2026-09-10_secreview-appendix-and-tables.prompt.txt"
REGA="$SR_DIR/Deliverables/13A_HPAM_Consolidated_Findings_Register_2026-09.md"
REGB="$SR_DIR/Deliverables/13B_Datasec_Products_Consolidated_Findings_Register_2026-09.md"
BUILDA="$SR_DIR/_Working/build-doc13A.sh"
BUILDB="$SR_DIR/_Working/build-doc13B.sh"
SEED="$SR_DIR/_Working/findings-seed-2026-09"
RULES="$SEED/_AGENT_RULES.md"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -s "$REGA" ]        || { echo "13A register missing: $REGA" >&2; exit 5; }
[ -s "$REGB" ]        || { echo "13B register missing: $REGB" >&2; exit 6; }
[ -s "$BUILDA" ]      || { echo "build-doc13A.sh missing — the rendered .docx is what ships: $BUILDA" >&2; exit 7; }
[ -s "$BUILDB" ]      || { echo "build-doc13B.sh missing — the rendered .docx is what ships: $BUILDB" >&2; exit 8; }

# GUARD: the appendix is built FROM the seed evidence. No seed directory, no round.
[ -d "$SEED" ] || {
  echo "REFUSING: findings-seed directory missing: $SEED" >&2
  echo "  The appendix must be built from recorded file:line evidence. Without it an agent" >&2
  echo "  would reconstruct locations from the register's prose and invent line numbers." >&2
  exit 9; }
[ -s "$RULES" ] || { echo "REFUSING: $RULES missing — rule 6 (never reproduce a secret) is the authority for the appendix's redaction." >&2; exit 10; }

# GUARD: the seed evidence must actually carry file:line citations, not just exist.
CITES=$(grep -rhoE '[A-Za-z0-9_./-]+\.[a-zA-Z]{1,5}:[0-9]+' "$SEED" 2>/dev/null | wc -l | tr -d ' ')
[ "${CITES:-0}" -ge 200 ] || {
  echo "REFUSING: only ${CITES:-0} file:line citations found under $SEED (expected many hundreds)." >&2
  echo "  Either the seed set is not what this brief assumes, or the search is broken." >&2
  echo "  Read it before re-running — a thin evidence base produces a confident, wrong appendix." >&2
  exit 11; }

# GUARD: both registers must still be the current output — an ESTATE TOTAL row in each.
A=$(grep -c 'ESTATE TOTAL' "$REGA"); B=$(grep -c 'ESTATE TOTAL' "$REGB")
[ "$A" -ge 1 ] && [ "$B" -ge 1 ] || {
  echo "REFUSING: one of the two registers no longer carries an ESTATE TOTAL row." >&2
  echo "  This round edits the CURRENT registers. Read both before re-running." >&2
  exit 12; }

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 13 ;; esac
case "$PROMPT" in *2026-09-10_secreview-appendix-and-tables.md*) ;; *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 14 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "prompt does not route the wrap to tuesday-agent@ — a Datasec wrap must not land in the Secuura seat's inbox" >&2; exit 15 ;; esac
case "$PROMPT" in *wednesday-agent@*) echo "prompt routes to wednesday-agent@ — refusing: cross-client" >&2; exit 16 ;; *) ;; esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_appendix_tables: all guards pass"
  echo "  project, brief, prompt present (T9 paths; DevMASTER not mounted)"
  echo "  both registers present and each carries an ESTATE TOTAL row"
  echo "  both docx build scripts present"
  echo "  seed evidence present with $CITES file:line citations, and _AGENT_RULES.md (secret rule) present"
  echo "  prompt opens with the thinking directive and names the brief by path"
  echo "  prompt routes the wrap to tuesday-agent@ and mentions no Secuura inbox"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
