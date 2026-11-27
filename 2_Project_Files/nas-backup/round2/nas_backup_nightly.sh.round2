#!/bin/bash
# nas_backup_nightly.sh — what the scheduler calls (launchd; see jobs/nasbackup.plist.template).
#
# It RUNS a backup when there is no good backup since this seat's last scheduled window opened, so:
#   - a missed night is caught up the next time the window opens (Kam: "If it does not happen one night, it
#     should happen the next");
#   - the job fires several times inside the window (hourly), so a Mac that woke late or a NAS that came back
#     late still gets its run that night;
#   - a fire while a run is in progress is skipped, with the reason logged.
# It NEVER runs outside its window on its own (seats/<seat>.conf: late_fire=refuse). A fire outside the window
# is logged and skipped; an out-of-sequence backup is Kam's decision (the three-day card).
# Every decision is appended to logs/<seat>/nightly.log and recorded as last_fire in state/<seat>.json, so a
# night of skips is a fact someone can read, not an absence. After deciding, it calls the three-day check
# (which ALSO runs from the launcher and doctor: a job that never fires cannot report itself).
#
#   nas_backup_nightly.sh                  decide and act
#   nas_backup_nightly.sh --decide-only    print the decision, change nothing
# Exit: 0 skipped or good; otherwise nas_backup.sh's exit code. NEVER add >/dev/null here.
set -u
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nb_common.sh"
nb_resolve_seat || exit $?
nb_find_python || exit $?
EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --decide-only) EXTRA+=( "$1" ); shift ;;
    --now) [ $# -ge 2 ] || { echo "nas_backup_nightly: --now needs a value" >&2; exit 2; }; EXTRA+=( "$1" "$2" ); shift 2 ;;
    *) echo "nas_backup_nightly: REFUSED — unknown argument '$1'; nothing run" >&2; exit 2 ;;
  esac
done
exec "$NB_PY" "$NB_HERE/nb_core.py" nightly --seat "$NB_SEAT" --tree "$NB_TREE" ${EXTRA[@]+"${EXTRA[@]}"}
