#!/bin/bash
# launch_nexusai_marketplace_remediation.sh — Kam's 2026-09-10 review of NexusAI ahead of
# preparing the containers for Azure Marketplace submission tomorrow.
#
# WHY THE GUARDS. A marketplace publish is effectively irreversible, so the expensive
# failure here is a review that reports GO on an image nobody enumerated. The guards
# therefore refuse anything that would produce a confident, hollow verdict:
#   - no Dockerfile or submission package = there is nothing to review against;
#   - no docker daemon = the agent cannot export an image and will "review" the source
#     instead, which is exactly the substitution this whole round exists to prevent;
#   - a prompt that does not name the brief, or routes its wrap to the Secuura seat.
#
# T9 PATHS. DevMASTER is not mounted here. SELF-LOCATING per portability rule 3.
# Usage: launch_nexusai_marketplace_remediation.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..15 a guard refused
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

NX_DIR="${NEXUSAI_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI}"
WT="$NX_DIR/wt-s49"
BRIEF="$STAGED/2026-09-10_nexusai-marketplace-remediation.md"
PROMPT_FILE="$STAGED/2026-09-10_nexusai-remed-successor.prompt.txt"

[ -d "$NX_DIR" ]      || { echo "NexusAI project missing: $NX_DIR" >&2; exit 2; }
[ -d "$WT" ]          || { echo "wt-s49 worktree missing (the newest committed state): $WT" >&2; exit 3; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 4; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -s "$WT/Dockerfile" ] || { echo "REFUSING: no Dockerfile at $WT — there is no container to review." >&2; exit 6; }
[ -s "$WT/AZURE_MARKETPLACE_SUBMISSION_PACKAGE.md" ] || {
  echo "REFUSING: submission package missing — the review has nothing to check the offer against." >&2; exit 7; }

# GUARD: docker must actually be up. Without it the agent cannot export an image and will
# silently substitute a source read for the one measurement this round is FOR.
docker info >/dev/null 2>&1 || {
  echo "REFUSING: docker is not responding." >&2
  echo "  This review's core instruction is to enumerate the built image by export, not to read" >&2
  echo "  the Dockerfile. Without a daemon the agent would produce a confident source-only" >&2
  echo "  verdict on an image nobody opened. Start Docker Desktop and re-run." >&2
  exit 8; }

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "prompt does not begin with the thinking directive — refusing" >&2; exit 9 ;; esac
case "$PROMPT" in *2026-09-10_nexusai-marketplace-remediation.md*) ;; *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 10 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "prompt does not route the wrap to tuesday-agent@ — refusing" >&2; exit 11 ;; esac
case "$PROMPT" in *wednesday-agent@*) echo "prompt routes to wednesday-agent@ — refusing: cross-client" >&2; exit 12 ;; *) ;; esac
# GUARD: Kam's standing ruling on the stale main tree must be carried, or a review that
# notices the discrepancy will helpfully "fix" the thing he ruled must not be touched.
case "$PROMPT" in *keep-as-is*) ;; *) echo "prompt does not carry Kam's main-tree ruling — refusing" >&2; exit 13 ;; esac
# GUARD: item 1 is a CHECK before a DELETE. A prompt that lost that clause would delete on a recollection.
case "$PROMPT" in *"CHECK, NOT AN ACTION"*) ;; *) echo "REFUSING: prompt does not carry Kam's check-before-delete instruction for item 1." >&2; exit 18 ;; esac
# GUARD: item 3 was RULED ACCEPTED. Without it the agent re-fixes what he accepted.
case "$PROMPT" in *ACCEPTED*) ;; *) echo "REFUSING: prompt does not carry Kam's item-3 acceptance." >&2; exit 19 ;; esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_nexusai_marketplace_remediation: all guards pass"
  echo "  project + wt-s49 present (T9 paths; DevMASTER not mounted)"
  echo "  Dockerfile and AZURE_MARKETPLACE_SUBMISSION_PACKAGE.md present"
  echo "  docker daemon responding — the image can actually be exported"
  echo "  prompt: thinking directive, brief path, tuesday-agent@ routing, no Secuura inbox"
  echo "  prompt carries Kam's 'keep the stale main tree as-is' ruling"
  exit 0
fi

cd "$NX_DIR" || { echo "cannot enter $NX_DIR" >&2; exit 14; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
