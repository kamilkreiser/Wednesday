#!/bin/bash
# seat_rung5.sh — did a launched seat RECEIVE its commission? (rung 5 of the launch-evidence ladder,
# lesson 2026-08-06_artifact-presence-is-not-execution). Reads the seat's own Claude transcripts.
#
# WHY (ledger 2026-10-09, Friday, self-found twice in one session): hand-rolled checks said "NOT SEEN"
# for real launches — once because they read only the 3 newest transcripts while other seats were
# writing (a frame too narrow), once because they grepped the brief's filename stem, which the seat
# never printed (it named its STATUS path instead). Both were false absences with no control.
#
# Usage: seat_rung5.sh <project-folder> <brief-id e.g. B111> [control-id e.g. B110] [n-transcripts, default 40]
#   rc 0  SEEN       — a transcript among the N newest names the brief id (prints the file + first line no.)
#   rc 1  NOT SEEN   — the control id WAS found (the instrument works), the brief id was not: read the pane next
#   rc 3  NO CONTROL — the control id was not found either, or none given: the absence means nothing
#   rc 2  usage / no transcript directory
# A NOT SEEN is never a sentence on its own: read the seat's pane before saying anything.
P="${1:?project folder}"; ID="${2:?brief id}"; CTL="${3:-}"; N="${4:-40}"
case "$P" in /*) ;; *) echo "seat_rung5: project folder must be absolute" >&2; exit 2;; esac
ROOT="${CLAUDE_TRANSCRIPTS_ROOT:-$HOME/.claude/projects}"
D="$ROOT/$(printf '%s' "$P" | sed 's#[^A-Za-z0-9]#-#g')"
[ -d "$D" ] || { echo "seat_rung5: no transcript dir $D" >&2; exit 2; }
FILES=$(ls -t "$D"/*.jsonl 2>/dev/null | head -n "$N")
[ -n "$FILES" ] || { echo "seat_rung5: no transcripts in $D" >&2; exit 2; }
hit(){ printf '%s\n' "$FILES" | while IFS= read -r f; do l=$(/usr/bin/grep -n -F -m1 "$1" "$f" | cut -d: -f1); [ -n "$l" ] && { echo "$f:$l"; break; }; done; }
h=$(hit "$ID")
if [ -n "$h" ]; then echo "SEEN $ID in $h (frame: $N newest of $D)"; exit 0; fi
if [ -n "$CTL" ] && [ -n "$(hit "$CTL")" ]; then echo "NOT SEEN $ID in the $N newest transcripts; control $CTL found, so the instrument reads — read the pane next"; exit 1; fi
echo "NO CONTROL: $ID not found and control '${CTL:-none}' not found either — this absence means nothing"; exit 3
