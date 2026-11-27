#!/bin/bash
# nas_backup_watch.sh — the THREE-DAY check (Kam 2026-11-27: "Flag it with me if backup not done for 3 days so I
# can approve an out of sequence backup"). ROUND 2.
#
# WHY IT IS ITS OWN SCRIPT (2026-09-20_a-guard-inside-the-thing-it-guards): a backup job that never fires cannot
# report that it never fired. This reads only state/<seat>.json on the drive and the clock; it needs neither the
# NAS nor the backup job, and no other script has to set a mark for its clock to run.
#
#   nas_backup_watch.sh            --check: one status line. READ-ONLY (apart from starting the clock once when
#                                  nothing at all is on record). The nightly job calls this mode: its output goes
#                                  to a launchd log no seat reads, so it must never be where the card is issued.
#   nas_backup_watch.sh --card     when OVERDUE and the card is not recorded as raised: prints the exact
#                                  decision_queue.sh command for ONE card (a = approve an out-of-sequence backup
#                                  now, b = wait for tonight's window; default b). Printing CONSUMES NOTHING: it
#                                  prints again at every call until --mark-raised. The card id is fixed per gap
#                                  and decision_queue.sh refuses a duplicate id, so the card exists once per gap.
#                                  THIS TOOL PRINTS THE COMMAND AND NEVER RUNS IT.
#   nas_backup_watch.sh --mark-raised <card id>   record that the card is on Kam's board (the seat that added it)
#   nas_backup_watch.sh --mark-armed              optional: start the clock explicitly
# THE CHANNEL TO A SEAT: doctor.sh (proposed/doctor_nasbackup_block.sh) prints a hard-failure line naming
# `nas_backup_watch.sh --card` while a card is due and not raised; the launcher carries doctor's hard-failure
# lines into the boot prompt.
# Exit: 0 ok, held, or nothing on record · 3 OVERDUE and no card recorded as raised, or the state file was found
#       damaged (it is moved aside, never deleted) · 4 overdue, card recorded as raised · 2 refused.
# NEVER add >/dev/null here.
set -u
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nb_common.sh"
nb_resolve_seat || exit $?
nb_find_python || exit $?
EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --check|--card|--mark-armed) EXTRA+=( "$1" ); shift ;;
    --mark-raised|--now) [ $# -ge 2 ] || { echo "nas_backup_watch: $1 needs a value" >&2; exit 2; }; EXTRA+=( "$1" "$2" ); shift 2 ;;
    *) echo "nas_backup_watch: REFUSED — unknown argument '$1'; nothing done" >&2; exit 2 ;;
  esac
done
exec "$NB_PY" "$NB_HERE/nb_core.py" watch --seat "$NB_SEAT" --tree "$NB_TREE" ${EXTRA[@]+"${EXTRA[@]}"}
