#!/bin/bash
# brief_seat.sh — run a Claude build seat in a project folder whose own launcher cannot run on this laptop
# (HPSM's requires the DevMASTER !CODING layout). It runs INSIDE a cockpit pane:
#   cockpit.sh add <Client/Name> "bash '<this file>' <client> '<project dir>' '<brief path relative to it>'"
# The client's identity comes only through friday_as.sh (one client, nothing else). The prompt names the brief
# path, so a launch is verifiable at rung 5 (the pane shows the brief) — see learnings/2026-08-06_artifact-presence-is-not-execution.
# First used 2026-09-25 for HPSM B02 (the 13:40 HPSM push seat was the same shape, typed by hand).
set -u
CLIENT="${1:?client (datasec|secuura)}"; DIR="${2:?project dir}"; BRIEF="${3:?brief path relative to the project dir}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
[ -d "$DIR" ] || { echo "brief_seat: no such project dir: $DIR" >&2; exit 2; }
[ -f "$DIR/$BRIEF" ] || { echo "brief_seat: no such brief: $DIR/$BRIEF" >&2; exit 2; }
cd "$DIR" || exit 2
PROMPT="ultrathink

You are a build seat launched by Friday (Kam's laptop coordinator) in the project folder $(basename "$DIR"). Read ./CLAUDE.md and 1_Project_Definition/CLARIFICATIONS.md first, then execute the brief ${BRIEF} exactly. Your wrap is the STATUS file the brief names; replies go to Friday. Never delete (quarantine). Secrets stay in 4_Credentials/ and 3_Access_Keys/."
exec bash "$SELF_DIR/friday_as.sh" "$CLIENT" claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
