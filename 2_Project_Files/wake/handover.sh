#!/bin/bash
# handover.sh — the ONE-BLOCK handover for a coordinator seat (WED-170 step 1, 2026-11-27).
# WHY: the pickup file's rule was "replace wholesale; never stack" and 106 blocks were stacked on it
# in 14 days. A rule nothing enforces. Here the state file holds ONE block; writing a new one moves
# the previous one to the top of the archive in the same action, so a stack cannot be made.
#
# Usage:
#   handover.sh write --stdin <<'EOF'     replace the block (previous block -> top of the archive)
#   handover.sh write --stdin --dry <<'EOF'   print what would happen; writes nothing
#   handover.sh show                      print the current block
#   handover.sh check                     rc 0 when the state file is one clean tool-written block (or absent)
#   handover.sh --where                   print seat, paths and cap; writes nothing
#   handover.sh seed --from-legacy        CUT-OVER HELPER, DRY BY DEFAULT: print the FIRST block, built from the
#                                         legacy pickup's newest block mapped into the five parts; writes nothing
#   handover.sh seed --from-legacy --run  write that first block. REFUSES when a state file already exists.
#
# The block has five headed parts, each once, each with text under it (write 'none' if none):
#   ## FLOOR            who is running
#   ## FIRST WORK       the first work of the next session
#   ## OWED             what is owed, to whom
#   ## OPEN CARDS       cards waiting on Kam
#   ## GRANTS IN PLAY   grants this state relies on
# REFUSED (rc 3, nothing written): an empty block; a block over HANDOVER_CAP_BYTES (default 10000);
# a clock with an x digit (11:4x); a missing, repeated or empty part; any other '## ' heading.
# QUOTING text that already carries an x-digit clock (a grant's name, an older block): the owned override,
# in note_entry.sh's shape:  HANDOVER_ALLOW_XCLOCK='<why, 15 characters or more>' handover.sh write --stdin
# The reason is recorded in the block's header and, when the block is archived, in its archive heading.
# rc 2: seat or usage. rc 4: conservation or I/O fault. rc 5: the write lock is held, stale, or was
# taken away before a rename. rc 6: the files were replaced but the lock was not this process's at
# release, so the write is NOT acknowledged (look with `show`, write again if it is not your block).
# ONE WRITER AT A TIME: the whole write runs under a lock directory (0_Brain/tasks/STATE-<seat>.lock.d).
# A second writer waits HANDOVER_LOCK_WAIT seconds (default 20), then refuses.
#   LOCK BUSY  = a write is running: run the command again.
#   STALE LOCK = a write died and left its lock (reported only after a second look): run the `mv -n`
#                recovery line the message prints (a seat may run it itself), then the write again.
# The tool never removes a lock it did not take. Its temp files live inside the lock directory, so a
# writer whose lock was moved away cannot rename anything into place.
# Inside a block the ONLY heading lines are the five parts, written exactly; any other heading, of any
# level or indented, is refused (write it as a bold line or a bullet).
#
# Files (seat from the tree, never typed): 0_Brain/tasks/STATE-<seat>.md and STATE-<seat>-archive.md.
# It never WRITES NEXT-PICKUP*.md, and reads it only for `seed --from-legacy`.
# Seat: tools/seat_note.sh (the guard over fleet/cockpit/seat_resolve.sh): an unrecognised tree, or a
# WED_AGENT that disagrees with the tree, REFUSES rather than defaulting to wednesday.
# Seams (tests only): HANDOVER_TREE=<tree root> (its folder name decides the seat),
# HANDOVER_TEST_STAMP, HANDOVER_TEST_BREAK. They are INERT IN PRODUCTION: honoured only when the target
# tree is under a system temp or scratch directory (/tmp, /private/tmp, /var/folders); set for any other
# tree they are REFUSED (rc 2), with a line saying so. The clock is read here with `date`, never typed.
# macOS bash 3.2. Never discards stderr.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TREE="${HANDOVER_TREE:-$PROJECT_DIR}"

# ── test seams are inert outside temp / scratch trees (round 3, m4) ──
tree_is_temp() { # <dir> -> rc 0 when its real path is under a system temp or scratch root
  local real root
  real="$(cd -P "$1" 2>/dev/null && pwd -P)" || return 1
  for root in /tmp /private/tmp /var/folders /private/var/folders; do
    root="$(cd -P "$root" 2>/dev/null && pwd -P)" || continue
    case "$real/" in "$root"/*) return 0 ;; esac
  done
  return 1
}
if [ -n "${HANDOVER_TREE:-}${HANDOVER_TEST_STAMP:-}${HANDOVER_TEST_BREAK:-}" ] && ! tree_is_temp "$TREE"; then
  echo "handover: REFUSED — HANDOVER_TREE, HANDOVER_TEST_STAMP and HANDOVER_TEST_BREAK are test seams, honoured only for a tree under a system temp or scratch directory (/tmp, /private/tmp, /var/folders). The target here is '$TREE'. Unset them." >&2
  exit 2
fi
CORE="$SCRIPT_DIR/handover_core.py"
SEAT_LIB="$SCRIPT_DIR/../tools/seat_note.sh"

usage() {
  echo "usage: handover.sh write --stdin [--dry] | show | check | --where | seed --from-legacy [--run]" >&2
}

CMD=""; STDIN=0; DRY=0; FROM_LEGACY=0; RUN=0
[ $# -gt 0 ] || { usage; exit 2; }
while [ $# -gt 0 ]; do
  case "$1" in
    write|show|check|seed) [ -z "$CMD" ] || { echo "handover: REFUSED — two commands given ('$CMD' and '$1')" >&2; exit 2; }; CMD="$1" ;;
    --where|where)    [ -z "$CMD" ] || { echo "handover: REFUSED — two commands given ('$CMD' and '$1')" >&2; exit 2; }; CMD="where" ;;
    --stdin)          STDIN=1 ;;
    --dry|--dry-run)  DRY=1 ;;
    --from-legacy)    FROM_LEGACY=1 ;;
    --run)            RUN=1 ;;
    -h|--help)        usage; exit 0 ;;
    *) echo "handover: REFUSED — unknown argument '$1'. The block is never passed as an argument (a shell expands it first): use  handover.sh write --stdin <<'EOF'" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$CMD" ] || { usage; exit 2; }
if [ "$CMD" = "write" ] && [ "$STDIN" != 1 ]; then
  echo "handover: REFUSED — write takes the block on stdin only: handover.sh write --stdin <<'EOF'" >&2; exit 2
fi
if [ "$CMD" != "write" ] && { [ "$STDIN" = 1 ] || [ "$DRY" = 1 ]; }; then
  echo "handover: REFUSED — --stdin and --dry belong to write, not to '$CMD' (seed is dry unless --run is given)" >&2; exit 2
fi
if [ "$CMD" = "seed" ] && [ "$FROM_LEGACY" != 1 ]; then
  echo "handover: REFUSED — seed needs its source named: handover.sh seed --from-legacy [--run]" >&2; exit 2
fi
if [ "$CMD" != "seed" ] && { [ "$FROM_LEGACY" = 1 ] || [ "$RUN" = 1 ]; }; then
  echo "handover: REFUSED — --from-legacy and --run belong to seed, not to '$CMD'" >&2; exit 2
fi

# shellcheck disable=SC1090
. "$SEAT_LIB" || { echo "handover: REFUSED — cannot load the seat guard at $SEAT_LIB" >&2; exit 2; }
seat_note_dir "$TREE" handover || exit 2
SEAT="$SEAT_NOTE_SEAT"
[ -n "$SEAT" ] || { echo "handover: REFUSED — the seat guard returned no seat" >&2; exit 2; }
[ -f "$CORE" ] || { echo "handover: REFUSED — engine missing at $CORE" >&2; exit 2; }

CAP="${HANDOVER_CAP_BYTES:-10000}"
case "$CAP" in
  ''|*[!0-9]*) echo "handover: REFUSED — HANDOVER_CAP_BYTES must be a whole number, got '$CAP'" >&2; exit 2 ;;
esac

ARGS=(--seat "$SEAT" --tasks-dir "$TREE/0_Brain/tasks" --cap "$CAP" --tool "2_Project_Files/wake/handover.sh")
if [ "$CMD" = "write" ]; then
  STAMP="${HANDOVER_TEST_STAMP:-$(date '+%Y-%m-%d %H:%M:%S %Z')}"
  ARGS+=(--stamp "$STAMP")
  [ "$DRY" = 1 ] && ARGS+=(--dry)
fi
if [ "$CMD" = "seed" ] && [ "$RUN" = 1 ]; then
  STAMP="${HANDOVER_TEST_STAMP:-$(date '+%Y-%m-%d %H:%M:%S %Z')}"
  ARGS+=(--stamp "$STAMP" --run)
fi
exec python3 "$CORE" "$CMD" "${ARGS[@]}"
