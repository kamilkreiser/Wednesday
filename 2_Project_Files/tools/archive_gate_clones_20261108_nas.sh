#!/bin/bash
# archive_gate_clones_20261108_nas.sh — move the clone/ folder (and ONLY clone/) of the 9 gates whose PRs
# MERGED (B's MERGED mails, read from the inbox API 2026-11-08), from 0_Brain/reference/ to the NAS share
# DEV-Working. Kam: card wed-disk-25gib-delete-merged-gate-clones-1106 = a, then his note on
# wed-disk-clone-delete-blocked-by-hook-1108 (2026-11-08 21:05:07): "create the right Secuura WIP folder and
# place things in sub folders there". Copied from archive_gate_clones_20261103.sh; destination, list and subdir changed. A MOVE, never a delete
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
DST=/Volumes/DEV-Working/Secuura/Blockchain/WIP/2026-11-08_merged-gate-clones
[ -d /Volumes/DEV-Working ] || { echo "ABORT: DEV-Working share not mounted" >&2; exit 3; }
G="2026-11-06_gate217-tier1-pr2032-2036 2026-11-06_gate218-tier2-pr2037-2038 2026-11-06_gate219-ks1951-pr2039 2026-11-06_gate220-ks1613-pr2040 2026-11-06_gate221-ks1136-pr2041 2026-11-06_gate229-tier1-pr2048-ks2038 2026-11-06_gate231-tier2-pr2050-ks1707 2026-11-06_gate232-tier1-pr2051-ks2058 2026-11-06_gate234-tier1-pr2053-ks957"
echo "df before:"; df -h /Volumes/DevMASTER | tail -1
mkdir -p "$DST"
MAN="$DST/manifest.txt"
[ "$MODE" = "--run" ] && echo "# manifest $(date '+%Y-%m-%d %H:%M:%S %Z') — name | source | files at source | files at destination | result" >> "$MAN"
FAILS=0
for g in $G; do
  SRC="$R/$g/clone"
  [ -d "$SRC" ] || { echo "$g: no clone/ (skip)"; continue; }
  NS=$(find "$SRC" -type f 2>&1 | wc -l | tr -d ' ')
  if [ "$MODE" = "--dry" ]; then echo "$g: would move clone/ ($NS files) -> $DST/$g/clone"; continue; fi
  mkdir -p "$DST/$g"
  rsync -a "$SRC/" "$DST/$g/clone/" ; RC=$?
  ND=$(find "$DST/$g/clone" -type f 2>&1 | wc -l | tr -d ' ')
  if [ $RC -eq 0 ] && [ "$NS" = "$ND" ]; then
    # Complete the MOVE Kam ruled: a second rsync pass removes ONLY source files it has confirmed present
    # and identical at the destination; the empty directory skeleton stays (a record of where it was).
    rsync -a --remove-source-files "$SRC/" "$DST/$g/clone/"; RC2=$?
    NL=$(find "$SRC" -type f 2>&1 | wc -l | tr -d ' ')
    echo "$g | $SRC | $NS | $ND | MOVED (remove pass rc=$RC2, files left at source $NL)" | tee -a "$MAN"
    [ "$RC2" -eq 0 ] && [ "$NL" = "0" ] || FAILS=$((FAILS+1))
  else
    FAILS=$((FAILS+1)); echo "$g | $SRC | $NS | $ND | MISMATCH rsync rc=$RC — source LEFT IN PLACE" | tee -a "$MAN"
  fi
done
echo "df after:"; df -h /Volumes/DevMASTER | tail -1
echo "FAILS=$FAILS"; [ $FAILS -eq 0 ]
