#!/bin/bash
# seat_note.sh — THE seat -> daily-note-directory mapping (2026-09-16, Tuesday's census 20:23).
# SOURCED, never executed, by:
#   tools/note_entry.sh                  (the only writer of note lines)
#   scheduler/close_wednesday.sh         (the 23:00 bell: wrap check, tracked check, stamp)
#   voice/speak.sh                       (.spoken.log — in a SUBSHELL, it must never die here)
#   fleet/hooks/session_start_compact.sh (the re-ground pointer — in a SUBSHELL)
# WHY: both seats wrote ONE note, 0_Brain/daily/<date>.md, so it conflicted on every rebase and
# the Datasec seat's episodic notes landed in the Secuura seat's note. One mapping, one copy.
#
# Mapping (agreed Wednesday + Tuesday 2026-09-16; amendment 20:35):
#   tree folder WEDNESDAY -> seat wednesday -> 0_Brain/daily          (UNCHANGED)
#   tree folder TUESDAY   -> seat tuesday   -> 0_Brain/daily_tuesday
#   tree folder FRIDAY    -> seat friday    -> 0_Brain/daily_friday   (2026-09-23, Kam 10:49: the laptop
#     seat, both clients; Wednesday creates the folder + README — this mapping only names it)
#   ANY OTHER folder name -> REFUSE. seat_resolve.sh maps "anything else" to wednesday by design
#     (pane lookup); for a NOTE that default would silently write one client's episodic memory
#     into the other's (R0). Recognition is install_all_jobs.sh's rule (lower-cased folder
#     name in {tuesday, wednesday, friday}); WED_AGENT alone never rescues an unrecognised tree.
#   WED_AGENT set AND different from the tree's seat -> REFUSE (two independent sources disagree).
# _template.md stays shared at 0_Brain/daily/_template.md.
#
# Provides:
#   seat_note_dir <project_dir> [caller-name]
#     rc 0: sets SEAT_NOTE_SEAT, SEAT_NOTE_REL (relative to the repo root, no trailing slash) and
#           SEAT_NOTE_DIR (absolute). Creates nothing — callers mkdir -p when they write.
#     rc 2: ONE stderr line naming the fix; the same text is left in SEAT_NOTE_ERR so a caller
#           can also log it. Never `exit`s (it is sourced), and every expansion is set -u safe.
#
# macOS bash 3.2: no declare -A, no ${var,,}. No `cd` of the caller's shell.

seat_note_dir() { # <project_dir> [caller] -> rc 0 (SEAT_NOTE_*) | rc 2 (stderr + SEAT_NOTE_ERR)
  local dir="${1:-}" who="${2:-seat_note}" name lower resolver
  SEAT_NOTE_SEAT=""; SEAT_NOTE_REL=""; SEAT_NOTE_DIR=""; SEAT_NOTE_ERR=""
  if [ -z "$dir" ]; then
    SEAT_NOTE_ERR="$who: REFUSED — seat_note_dir called without a project dir"
    echo "$SEAT_NOTE_ERR" >&2; return 2
  fi
  resolver="$(dirname "${BASH_SOURCE[0]}")/../fleet/cockpit/seat_resolve.sh"
  # shellcheck disable=SC1090
  if [ ! -r "$resolver" ] || ! . "$resolver" || ! command -v seat_resolve >/dev/null 2>&1; then
    SEAT_NOTE_ERR="$who: REFUSED — cannot load the seat resolver at $resolver"
    echo "$SEAT_NOTE_ERR" >&2; return 2
  fi
  name="$(basename "$dir")"
  lower="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"
  seat_resolve "$dir"   # sets TREE_SEAT (folder name) and SEAT (WED_AGENT else TREE_SEAT)
  # TREE_SEAT counts only where it genuinely came from the folder name: the name must be one the
  # installer recognises AND seat_resolve must read it the same way (a "TuEsday" folder would be
  # tuesday to the installer and wednesday to seat_resolve — that disagreement refuses too).
  case "$lower" in
    tuesday|wednesday|friday) ;;
    *) lower="" ;;
  esac
  if [ -z "$lower" ] || [ "${TREE_SEAT:-}" != "$lower" ]; then
    SEAT_NOTE_ERR="$who: REFUSED — cannot tell which seat this tree is — run from a WEDNESDAY, TUESDAY or FRIDAY tree (tree: $dir)"
    echo "$SEAT_NOTE_ERR" >&2; return 2
  fi
  if [ -n "${WED_AGENT:-}" ] && [ "$WED_AGENT" != "$TREE_SEAT" ]; then
    SEAT_NOTE_ERR="$who: REFUSED — WED_AGENT='$WED_AGENT' but this tree ('$name') is seat '$TREE_SEAT' — unset WED_AGENT, or run from the matching tree"
    echo "$SEAT_NOTE_ERR" >&2; return 2
  fi
  SEAT_NOTE_SEAT="$TREE_SEAT"
  case "$TREE_SEAT" in
    wednesday) SEAT_NOTE_REL="0_Brain/daily" ;;
    tuesday)   SEAT_NOTE_REL="0_Brain/daily_tuesday" ;;
    friday)    SEAT_NOTE_REL="0_Brain/daily_friday" ;;
  esac
  SEAT_NOTE_DIR="$dir/$SEAT_NOTE_REL"
  return 0
}
