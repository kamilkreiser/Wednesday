#!/bin/bash
# archive_gate_clones_20261103.sh — move the repo/ clone (and ONLY repo/) of the 13 gates whose PRs
# have closed, from 0_Brain/reference/ to G-DRIVE. Kam's ruling: card wed-gate-clones-hook-blocks-removal-1103
# = a ("Plug in the G-DRIVE and I move them there", 2026-11-03 18:49). A MOVE, never a delete
# (learnings/2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month.md;
#  2026-10-15_a-sync-is-not-done-until-every-folder-is-counted-on-both-sides.md).
# Closed state measured 2026-11-03 19:5x: `git ls-remote origin refs/pull/N/merge` returns nothing for all 12 PRs,
# positive control: open PRs 1968/1987/1988 return a merge ref.
# Per folder: count files at source, copy (rsync -a, no --delete), count at destination; ONLY if the counts
# are equal does a second pass (rsync --remove-source-files) complete the move. A mismatch leaves the source
# untouched. Usage: archive_gate_clones_20261103.sh --dry | --run
set -u
MODE="${1:-}"; [ "$MODE" = "--dry" ] || [ "$MODE" = "--run" ] || { echo "usage: $0 --dry|--run" >&2; exit 2; }
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference
DST=/Volumes/G-DRIVE/Secuura/Blockchain/archive/2026-11-03_gate-clones
[ -d /Volumes/G-DRIVE/Secuura/Blockchain/archive ] || { echo "ABORT: G-DRIVE archive dir absent" >&2; exit 3; }
G="2026-11-03_gate148-ks1868-pr1970 2026-11-03_gate156-ks1868-pr1973 2026-11-03_gate157-ks1868-pr1974 2026-11-03_gate159-ks1868-pr1976 2026-11-03_gate160-ks1868-pr1977 2026-11-03_gate161-ks1868-pr1978 2026-11-03_gate162-ks1956-pr1979 2026-11-03_gate163-ks1957-pr1980 2026-11-03_gate164-ks1868-pr1981 2026-11-03_gate167-ks1572-pr1984 2026-11-03_gate168-ks1961-pr1985 2026-11-03_gate169-ks1962-pr1986 2026-11-03_gate170-ks1961-pr1985"
echo "df before:"; df -h /Volumes/DevMASTER | tail -1
mkdir -p "$DST"
MAN="$DST/manifest.txt"
[ "$MODE" = "--run" ] && echo "# manifest $(date '+%Y-%m-%d %H:%M:%S %Z') — name | source | files at source | files at destination | result" >> "$MAN"
FAILS=0
for g in $G; do
  SRC="$R/$g/repo"
  [ -d "$SRC" ] || { echo "$g: no repo/ (skip)"; continue; }
  NS=$(find "$SRC" -type f 2>&1 | wc -l | tr -d ' ')
  if [ "$MODE" = "--dry" ]; then echo "$g: would move repo/ ($NS files) -> $DST/$g/repo"; continue; fi
  mkdir -p "$DST/$g"
  rsync -a "$SRC/" "$DST/$g/repo/" ; RC=$?
  ND=$(find "$DST/$g/repo" -type f 2>&1 | wc -l | tr -d ' ')
  if [ $RC -eq 0 ] && [ "$NS" = "$ND" ]; then
    # Complete the MOVE Kam ruled: a second rsync pass removes ONLY source files it has confirmed present
    # and identical at the destination; the empty directory skeleton stays (a record of where it was).
    rsync -a --remove-source-files "$SRC/" "$DST/$g/repo/"; RC2=$?
    NL=$(find "$SRC" -type f 2>&1 | wc -l | tr -d ' ')
    echo "$g | $SRC | $NS | $ND | MOVED (remove pass rc=$RC2, files left at source $NL)" | tee -a "$MAN"
    [ "$RC2" -eq 0 ] && [ "$NL" = "0" ] || FAILS=$((FAILS+1))
  else
    FAILS=$((FAILS+1)); echo "$g | $SRC | $NS | $ND | MISMATCH rsync rc=$RC — source LEFT IN PLACE" | tee -a "$MAN"
  fi
done
echo "df after:"; df -h /Volumes/DevMASTER | tail -1
echo "FAILS=$FAILS"; [ $FAILS -eq 0 ]
