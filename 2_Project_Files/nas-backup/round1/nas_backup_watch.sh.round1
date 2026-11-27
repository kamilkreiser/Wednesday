#!/bin/bash
# nas_backup_watch.sh — the THREE-DAY check (Kam 2026-11-27: "Flag it with me if backup not done for 3 days so I
# can approve an out of sequence backup").
#
# WHY IT IS ITS OWN SCRIPT (2026-09-20_a-guard-inside-the-thing-it-guards): a backup job that never fires cannot
# report that it never fired. This reads only state/<seat>.json on the drive and the clock; it needs neither the
# NAS nor the backup job. It is meant to be called from THREE places that run on their own clocks: the seat's
# launcher at boot, doctor.sh, and the nightly job (proposed lines: proposed/).
#
#   nas_backup_watch.sh               --check: one status line; exit 3 when no good backup for 72 hours
#   nas_backup_watch.sh --flag        the same, and when OVERDUE it prints the exact decision_queue.sh command
#                                     for ONE card (a = approve an out-of-sequence backup now, b = wait for
#                                     tonight's window; default b) ONCE per gap: it records that in the state
#                                     file, and later calls print one reminder line, not the command.
#                                     THIS TOOL PRINTS THE COMMAND AND NEVER RUNS IT.
#   nas_backup_watch.sh --reprint     print the card command again (changes nothing)
#   nas_backup_watch.sh --mark-raised <card id>   record that the card is on Kam's board
#   nas_backup_watch.sh --mark-armed  start the three-day clock (the arming step runs this once)
# The clock starts at the last good backup; before the first good backup, at --mark-armed (or the first attempt).
# Exit: 0 ok or not armed · 3 overdue · 2 refused. NEVER add >/dev/null here.
set -u
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nb_common.sh"
nb_resolve_seat || exit $?
nb_find_python || exit $?
EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --check|--flag|--reprint|--mark-armed) EXTRA+=( "$1" ); shift ;;
    --mark-raised|--now) [ $# -ge 2 ] || { echo "nas_backup_watch: $1 needs a value" >&2; exit 2; }; EXTRA+=( "$1" "$2" ); shift 2 ;;
    *) echo "nas_backup_watch: REFUSED — unknown argument '$1'; nothing done" >&2; exit 2 ;;
  esac
done
exec "$NB_PY" "$NB_HERE/nb_core.py" watch --seat "$NB_SEAT" --tree "$NB_TREE" ${EXTRA[@]+"${EXTRA[@]}"}
