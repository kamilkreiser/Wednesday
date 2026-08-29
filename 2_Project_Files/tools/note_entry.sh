#!/bin/bash
# note_entry.sh — append a bullet to TODAY's daily note with a GENERATED timestamp.
# WHY (consolidation 2026-08-30; ledger w=17/20/22/24/34/46 — six composed timestamps in
# ten days, the last one after a nine-hour gap, all self-consistent and wrong): a timestamp
# typed by hand is composed from narrative; the clock is read only if the WRITER reads it.
# This script reads it. Usage:
#   note_entry.sh "text"            → "- HH:MM — text" appended under the LAST heading of the note
#   note_entry.sh --h3 "title"      → "### HH:MM — title" appended (a new block)
# Refuses empty text. Never discards stderr. The note must already exist (created at boot).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
NOTE="${WED_NOTE_OVERRIDE:-$PROJECT_DIR/0_Brain/daily/$(date +%F).md}"
[ -f "$NOTE" ] || { echo "note_entry: no note at $NOTE — create it from _template.md first" >&2; exit 2; }
MODE=line; [ "${1:-}" = "--h3" ] && { MODE=h3; shift; }
TEXT="${1:-}"; [ -n "$TEXT" ] || { echo "note_entry: refusing empty text" >&2; exit 2; }
STAMP="$(date +%H:%M)"
case $MODE in
  line) printf -- '- %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
  h3)   printf -- '### %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
esac
echo "note_entry: $STAMP → $NOTE"
