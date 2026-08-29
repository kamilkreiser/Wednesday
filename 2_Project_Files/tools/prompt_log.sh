#!/bin/bash
# prompt_log.sh — append one of Kam's prompts VERBATIM to the Discovery prompt log with a
# GENERATED date+time header (consolidation 2026-08-30; ledger w=46: the 08-29 entry was
# hand-stamped "11:1x" for a 19:53 message). Usage:
#   prompt_log.sh "<channel, e.g. terminal | dashboard chat>" "<verbatim text>" ["<note line>"]
# Header: "## YYYY-MM-DD HH:MM — Kam (<channel>, verbatim)". The text is written as a
# blockquote line-by-line. Refuses empty text. Never discards stderr.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG="${WED_PROMPTLOG_OVERRIDE:-$PROJECT_DIR/1_Project_Definition/Discovery/00_prompt-log.md}"
CH="${1:-}"; TEXT="${2:-}"; NOTE="${3:-}"
[ -n "$CH" ] && [ -n "$TEXT" ] || { echo "usage: prompt_log.sh <channel> <verbatim text> [note]" >&2; exit 2; }
[ -f "$LOG" ] || { echo "prompt_log: no log at $LOG" >&2; exit 2; }
STAMP="$(date '+%Y-%m-%d %H:%M')"
{ printf '\n## %s — Kam (%s, verbatim)\n' "$STAMP" "$CH"
  printf '%s\n' "$TEXT" | sed 's/^/> /'
  [ -n "$NOTE" ] && printf '\n*Note:* %s\n' "$NOTE"; } >> "$LOG"
echo "prompt_log: $STAMP → $LOG"
