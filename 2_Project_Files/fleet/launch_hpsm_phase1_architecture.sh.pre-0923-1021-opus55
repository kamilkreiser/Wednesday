#!/bin/bash
# launch_hpsm_phase1_architecture.sh — Kam's 2026-09-10 HPSM Phase 1 architecture round.
# Guards: the excluded mis-attached document must stay excluded; the local-first constraint and
# the architecture-only constraint must both survive into the prompt, because either one lost
# turns a design round into an unauthorised build or a cloud spend Kam has not approved.
set -u
SELF="${BASH_SOURCE[0]}"; while [ -L "$SELF" ]; do D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"; [[ $SELF != /* ]] && SELF="$D/$SELF"; done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"; STAGED="$FLEET_DIR/briefs_staged"
HP_DIR="${HPSM_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM}"
SRC="/Users/kamil/Downloads/Archive"
BRIEF="$STAGED/2026-09-10_hpsm-phase1-architecture.md"
PROMPT_FILE="$STAGED/2026-09-10_hpsm-phase1-architecture.prompt.txt"
[ -d "$HP_DIR" ]      || { echo "HPSM project missing: $HP_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing: $PROMPT_FILE" >&2; exit 4; }
[ -s "$SRC/Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx" ] || { echo "REFUSING: the design spec — the primary input — is not at $SRC" >&2; exit 5; }
[ -s "$SRC/Policy Preview.pdf" ] || { echo "REFUSING: the target output sample is missing" >&2; exit 6; }
PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "prompt lacks the thinking directive" >&2; exit 7 ;; esac
case "$PROMPT" in *2026-09-10_hpsm-phase1-architecture.md*) ;; *) echo "prompt does not name the brief" >&2; exit 8 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "prompt does not route the wrap to tuesday-agent@" >&2; exit 9 ;; esac
case "$PROMPT" in *EXCLUDED*) ;; *) echo "REFUSING: prompt lost the exclusion of the mis-attached discovery document — it would be designed in." >&2; exit 10 ;; esac
case "$PROMPT" in *"LOCAL FIRST"*) ;; *) echo "REFUSING: prompt lost Kam's local-first constraint — an agent could spin up billable cloud resources he has not approved." >&2; exit 11 ;; esac
case "$PROMPT" in *"Architecture only"*) ;; *) echo "REFUSING: prompt lost the architecture-only constraint — this round would become an unauthorised build." >&2; exit 12 ;; esac
if [ "${1:-}" = "--check" ]; then
  echo "launch_hpsm_phase1_architecture: all guards pass"
  echo "  HPSM project, brief, prompt present; design spec and Policy Preview present at source"
  echo "  prompt carries: thinking directive, brief path, tuesday-agent@ routing"
  echo "  prompt carries: the EXCLUSION, LOCAL FIRST, and architecture-only"
  exit 0
fi
cd "$HP_DIR" || { echo "cannot enter $HP_DIR" >&2; exit 13; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
