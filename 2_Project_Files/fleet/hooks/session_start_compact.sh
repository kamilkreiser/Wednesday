#!/bin/bash
# session_start_compact.sh — SessionStart hook, matcher "compact" (built
# 2026-08-10, working-rhythm §4). If a session ever comes back from an
# emergency compaction despite the PreCompact block, its context is summaries
# of summaries — re-ground it immediately from disk. stdout from a
# SessionStart hook is injected into the session's context.
#
# Wired in .claude/settings.local.json (Wednesday project only). The matcher
# does the filtering; this script just emits the pointer.

#
# SEAT NOTES (2026-09-16): the pointer names the SEAT's own note directory (WEDNESDAY tree ->
# 0_Brain/daily/, TUESDAY tree -> 0_Brain/daily_tuesday/) via tools/seat_note.sh, resolved in a
# subshell. On a refusal (unrecognised tree, WED_AGENT disagreeing) this hook still exits 0 and
# puts the refusal INTO the injected text: a non-zero SessionStart hook's stdout is not injected,
# and a compacted session that is not told to re-ground is worse than one told the seat is unclear.

set -u
cat > /dev/null   # consume the hook payload
ROOT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RES="$( SN="$ROOT/2_Project_Files/tools/seat_note.sh"
  if [ -r "$SN" ] && . "$SN" && seat_note_dir "$ROOT" session_start_compact; then echo "OK|$SEAT_NOTE_REL"
  else echo "ERR|${SEAT_NOTE_ERR:-cannot load $SN}"; fi )"
case "$RES" in
  OK\|*) echo "Context was compacted. Re-ground: read CLAUDE.md boot ritual + today's ${RES#OK|}/ note before continuing." ;;
  *)     echo "Context was compacted. Re-ground: read CLAUDE.md boot ritual before continuing. WARNING — this seat's daily-note directory could NOT be resolved (${RES#ERR|}); settle the seat before writing any note." ;;
esac
exit 0
