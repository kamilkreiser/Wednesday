#!/bin/bash
# wed_build_seat.sh — run a BUILD seat for WEDNESDAY-project work (WED tickets) in a cockpit pane.
# Written 2026-11-27 for WED-170 (Kam: "put this into action"; build seats run in visible cockpit panes,
# learnings/2026-09-23_build-seats-run-in-cockpit-panes.md). Modelled on friday/brief_seat.sh.
#
# It runs INSIDE a cockpit pane, started by the coordinator:
#   cockpit.sh add "WED/<lane>" "bash '<this file>' '<lane dir, absolute>' '<brief path, absolute>' <model id>"
# The prompt names the brief path, so the launch is verifiable at the pane (the pane shows the brief being read).
# The seat works ONLY inside its lane directory; it never commits, pushes, mails or posts (its brief says so).
# The model id is passed by the coordinator from 0_Brain/dashboard/data/models_latest.json; never typed from memory.
set -u
LANE="${1:?lane directory (absolute)}"; BRIEF="${2:?brief path (absolute)}"; MODEL="${3:?model id}"
SELF_DIR="$(cd -P "$(dirname "$0")" && pwd)"
ROOT="$(cd -P "$SELF_DIR/../.." && pwd)"
case "$LANE" in "$ROOT"/2_Project_Files/*) : ;; *) echo "wed_build_seat: REFUSED: lane '$LANE' is not under $ROOT/2_Project_Files/" >&2; exit 2 ;; esac
[ -d "$LANE" ] || { echo "wed_build_seat: REFUSED: no such lane directory: $LANE" >&2; exit 2; }
[ -f "$BRIEF" ] || { echo "wed_build_seat: REFUSED: no such brief: $BRIEF" >&2; exit 2; }
case "$MODEL" in claude-*) : ;; *) echo "wed_build_seat: REFUSED: '$MODEL' does not look like a model id" >&2; exit 2 ;; esac
cd "$ROOT" || exit 2
PROMPT="ultrathink

You are a BUILD SEAT for the WEDNESDAY project, launched by Wednesday (the coordinator) into a cockpit pane. You are NOT the coordinator and you are NOT Wednesday: do NOT run the session-start ritual in CLAUDE.md, do NOT read the brain at boot, do NOT greet, speak, post to any board, send mail, or write a daily note. Your whole job is the brief at ${BRIEF}. Read it WHOLE first, with the Read tool, then do exactly what it says. Your lane directory is ${LANE}; you write nowhere else unless the brief names the path. When you stop for any reason, your last act is to update the STATUS.md file the brief names: the coordinator is woken by your pane going idle and reads that file."
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
