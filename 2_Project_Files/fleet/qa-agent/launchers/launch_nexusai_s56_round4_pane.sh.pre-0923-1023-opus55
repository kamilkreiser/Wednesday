#!/bin/bash
# launch_nexusai_s56_round4_pane.sh — the Datasec/NexusAI Marketplace round-4 BUILD seat (S56), in a tmux pane.
# Lives beside the QA launchers because that is where Tuesday's tracked, guarded launchers are.
#
# LAUNCH: cockpit.sh add 'Datasec/NexusAI-B' "bash '<this file>'"   — a PANE, never nohup (ledger 2026-09-12).
# TRAP 8a FIXED: exports NexusAI's own AZURE_CONFIG_DIR / GH_CONFIG_DIR (the S54 headless launcher inherited
# Tuesday's). CLAUDE_CONFIG_DIR is NexusAI's own project-local store if it exists, else Tuesday's (stated in --check).
# The seat works in the existing worktree wt-s51-mktremed (branch s51-marketplace-remediation @ b8c4646).
# Usage: launch_nexusai_s56_round4_pane.sh [--check]
set -u
N='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
WT="$N/wt-s51-mktremed"
BRIEF="$TUE/2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s56-mktpkg-round4.md"
ID_ROOT="${S56_IDENTITY_ROOT_OVERRIDE:-$N/4_Credentials}"
HEAD_SHA="${S56_HEAD_SHA_OVERRIDE:-b8c4646ab7d271567364876757403bfb8d23cf08}"

[ -s "$BRIEF" ] || { echo "brief missing: $BRIEF" >&2; exit 2; }
[ -d "$WT" ] || { echo "worktree missing: $WT" >&2; exit 3; }
GOT="$(git --no-optional-locks -C "$WT" rev-parse HEAD 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: worktree HEAD '$GOT' is not $HEAD_SHA" >&2; exit 4; }
BR="$(git --no-optional-locks -C "$WT" rev-parse --abbrev-ref HEAD 2>&1)"
[ "$BR" = "s51-marketplace-remediation" ] || { echo "REFUSING: worktree is on '$BR', not s51-marketplace-remediation" >&2; exit 5; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT" >&2; exit 6; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
if [ -d "$ID_ROOT/.claude" ]; then export CLAUDE_CONFIG_DIR="$ID_ROOT/.claude"; else export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"; fi
grep -q 'YOU ARE S56' "$BRIEF" && grep -q 'NEVER PUSH TO MAIN' "$BRIEF" || { echo "REFUSING: brief lacks the S56 shared-inbox section or the main hold" >&2; exit 7; }

PROMPT="ultrathink

You are the Datasec/NexusAI seat S56. Kam ruled ROUND 4 on the Azure Marketplace package at 08:50: make the deployed product GPT-only (wizard sets GPT, setup save works, Phi-3/Ollama removed) and mask the tenant IDs, then re-check.

READ YOUR BRIEF FIRST, IN FULL, BEFORE ANYTHING ELSE:
$BRIEF
It is also in the datasec-nexusai@ inbox from tuesday-agent@agentmail.to. That inbox is SHARED with seat S55; mail about S55's RD tickets is not yours.

Work only in the worktree wt-s51-mktremed, branch s51-marketplace-remediation, head b8c4646. Send your PLAN CONFIRMATION to tuesday-agent@agentmail.to before building.

HOLDS, verbatim and absolute:
NEVER PUSH TO MAIN. SUBMISSION IS KAM'S. B2 (registry) IS KAM'S — no registry login or push. No az, no gh. Never rm — quarantine. Merge nothing.
Run long commands in the FOREGROUND.

Send plan confirmation, questions, READY FOR QA and wrap to tuesday-agent@agentmail.to — not wednesday-agent@."

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  worktree $WT on s51-marketplace-remediation @ $HEAD_SHA"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  brief has the S56 shared-inbox section and the main hold"
  exit 0
fi
cd "$WT" || exit 8
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
