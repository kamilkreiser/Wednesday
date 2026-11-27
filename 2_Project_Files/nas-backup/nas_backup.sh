#!/bin/bash
# nas_backup.sh — COPY-ONLY backup of this seat's folder and its working projects to the DEV-Working NAS.
# WED-170, Kam 2026-11-27 12:03. Engine and every guarantee: nb_core.py (read its header).
#
#   nas_backup.sh                 DRY RUN (the default): reads both sides, prints what a run WOULD copy. Writes
#                                 nothing to the NAS, the state file or the index.
#   nas_backup.sh --dry [--no-hash]   the same, said out loud. --no-hash skips the sha256 comparison of files
#                                 that are already on the NAS with the same size but are not yet indexed.
#   nas_backup.sh --run           a REAL run. Refused outside this seat's nightly window, while HOLD_<seat>
#                                 exists, while the NAS is not mounted, etc. (each refusal says why).
#   nas_backup.sh --run --out-of-sequence <card id>
#                                 a real run OUTSIDE the window: only after Kam approved it on the card named.
#   nas_backup.sh --clear-stale-lock   move a lock whose process is dead into state/_quarantine_<date>/.
#   nas_backup.sh --scan [--measure-excluded]   census numbers for the configured sets (reads the drive only).
#
# Where it writes: <NAS>/<own client>/<Seat>/nightly-backup/ (allow-list in nb_core.py SEATS) and, on the drive,
# this lane's state/, logs/ and manifests/. Sources and schedule: seats/<seat>.conf.
# Exit: 0 good (or dry run done) · 2 refused · 3 held · 4 run-time cap · 5 engine error · 6 locked · 7 stalled
#       · 8 not counted equal · 9 the engine's log held a deleting line.
# NEVER add >/dev/null here (2026-08-06_never-discard-stderr).
set -u
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/nb_common.sh"
nb_resolve_seat || exit $?
nb_find_python || exit $?

MODE="--dry"; EXTRA=(); CMD="backup"
while [ $# -gt 0 ]; do
  case "$1" in
    --run) MODE="--run"; shift ;;
    --dry|--dry-run) MODE="--dry"; shift ;;
    --no-hash|--scheduled|--measure-excluded) EXTRA+=( "$1" ); shift ;;
    --out-of-sequence|--max-seconds|--now)
      [ $# -ge 2 ] || { echo "nas_backup: $1 needs a value" >&2; exit 2; }
      EXTRA+=( "$1" "$2" ); shift 2 ;;
    --clear-stale-lock) CMD="clear-stale-lock"; shift ;;
    --scan) CMD="scan"; shift ;;
    -h|--help) sed -n '2,22p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "nas_backup: REFUSED — unknown argument '$1' (see --help); nothing run" >&2; exit 2 ;;
  esac
done
if [ "$CMD" = "backup" ]; then
  exec "$NB_PY" "$NB_HERE/nb_core.py" backup --seat "$NB_SEAT" --tree "$NB_TREE" "$MODE" ${EXTRA[@]+"${EXTRA[@]}"}
fi
exec "$NB_PY" "$NB_HERE/nb_core.py" "$CMD" --seat "$NB_SEAT" --tree "$NB_TREE" ${EXTRA[@]+"${EXTRA[@]}"}
