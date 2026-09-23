#!/bin/bash
# launch_nexusai_marketplace_package.sh — Kam's 2026-09-11 08:06 ask: "is the Nexus AI zip file for
# Azure Marketplace submission ready?" + "Don't forget all the screenshots and everything else."
# One NexusAI seat: push the remediation branch, fix two findings, re-shoot the listing screenshots
# Kam ruled, and assemble a DRAFT submission zip for his review. Submission stays Kam's.
#
# WHY THE GUARDS:
#   - a push to `main` deploys the demo VM (.github/workflows/deploy-demo.yml, read at ed8b208),
#     so a prompt that lost "NEVER PUSH TO MAIN" is refused;
#   - Kam ruled KEEP on docs/Authorized_Users.md at 19:43 — a prompt that lost it could remove it;
#   - submission to Partner Center is Kam's signature class — a prompt that lost that line is refused;
#   - the worktree must still be the gated head, clean, or the brief describes a tree nobody measured;
#   - docker must be up, or the screenshots and the zip cannot be produced from a real run.
#
# Headless on purpose: the seat's rulings and holds are all in the brief; S51/S52 ran this way.
# No az and no gh are used by this round (the brief says stop and ask if either is needed).
# T9 PATHS; SELF-LOCATING. Written with the Write tool because it contains a legitimate `cd`.
# Usage: launch_nexusai_marketplace_package.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..14 a guard refused
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

NX_DIR="${NEXUSAI_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI}"
WT="$NX_DIR/wt-s51-mktremed"
BRIEF="$STAGED/2026-09-11_nexusai-mktpkg-round3.md"
PROMPT_FILE="$STAGED/2026-09-11_nexusai-mktpkg-round3.prompt.txt"
HEAD_SHA="${PKG_HEAD_SHA_OVERRIDE:-20a723b1fbdc5afeb2a1a3bd316d30689f75146b}"

[ -d "$NX_DIR" ]      || { echo "NexusAI project missing: $NX_DIR" >&2; exit 2; }
[ -d "$WT" ]          || { echo "worktree missing: $WT" >&2; exit 3; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 4; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 5; }

GOT="$(git --no-optional-locks -C "$WT" rev-parse HEAD 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: worktree HEAD is '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }
DIRTY="$(git --no-optional-locks -C "$WT" status --porcelain 2>&1)"
[ -z "$DIRTY" ] || { echo "REFUSING: worktree has uncommitted changes:" >&2; echo "$DIRTY" >&2; exit 7; }

docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — no real run, no screenshots, no zip" >&2; exit 8; }

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "REFUSING: prompt lacks the thinking directive" >&2; exit 9 ;; esac
case "$PROMPT" in *2026-09-11_nexusai-mktpkg-round3.md*) ;; *) echo "REFUSING: prompt does not name the brief" >&2; exit 10 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "REFUSING: prompt does not route mail to tuesday-agent@" >&2; exit 11 ;; esac
case "$PROMPT" in *"NEVER PUSH TO MAIN"*) ;; *) echo "REFUSING: prompt lost NEVER PUSH TO MAIN — a main push deploys the demo VM" >&2; exit 12 ;; esac
case "$PROMPT" in *"KEEP docs/Authorized_Users.md"*) ;; *) echo "REFUSING: prompt lost Kam's 19:43 KEEP ruling on docs/Authorized_Users.md" >&2; exit 13 ;; esac
case "$PROMPT" in *"SUBMISSION IS KAM'S"*) ;; *) echo "REFUSING: prompt lost SUBMISSION IS KAM'S — Partner Center is his signature class" >&2; exit 14 ;; esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_nexusai_marketplace_package: all guards pass"
  echo "  worktree at $HEAD_SHA, clean; docker responding"
  echo "  prompt: directive, brief path, tuesday-agent@, NEVER PUSH TO MAIN, KEEP Authorized_Users, SUBMISSION IS KAM'S"
  exit 0
fi

cd "$NX_DIR" || { echo "cannot enter $NX_DIR" >&2; exit 15; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
