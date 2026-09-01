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
# --stdin (added 2026-09-01, ledger w=4 in the unquoted-heredoc/backtick family): text passed as an
# ARGUMENT goes through the calling shell first — a backtick or $(…) inside a double-quoted
# argument is EXECUTED before this script runs (tonight: `git ls-remote --heads` ran and a
# handover line landed with a hole). With --stdin the caller writes  note_entry.sh --stdin <<'EOF'
# and nothing in the body can expand. This is the path Wednesday uses for ANY text containing
# a backtick, a dollar sign or a command; the argument form stays for one-line plain prose.
MODE=line; [ "${1:-}" = "--h3" ] && { MODE=h3; shift; }
if [ "${1:-}" = "--stdin" ]; then
  TEXT="$(cat)"; TEXT="${TEXT%$'\n'}"
else
  TEXT="${1:-}"
  case "$TEXT" in *'`'*|*'$('*) echo "note_entry: text contains a backtick or \$( — the shell may already have expanded it; use --stdin with a quoted heredoc" >&2 ;; esac
fi
[ -n "$TEXT" ] || { echo "note_entry: refusing empty text" >&2; exit 2; }
STAMP="$(date +%H:%M)"
case $MODE in
  line) printf -- '- %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
  h3)   printf -- '### %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
esac
echo "note_entry: $STAMP → $NOTE"
