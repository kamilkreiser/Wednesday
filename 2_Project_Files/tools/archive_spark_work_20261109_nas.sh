#!/bin/bash
# archive_spark_work_20261109_nas.sh — MOVE Wednesday's regenerable Spark per-round work clones from
# spark/cache/work/ to the NAS share DEV-Working. Kam 2026-11-09: card wed-disk-16gib-prune-freed-nothing-1109 = a
# ("Remove the regenerable clones my own agents made") + note "use the nas" on wed-disk-clone-delete-blocked-by-hook-1108.
# Copied from archive_gate_clones_20261108_nas.sh; source, list, destination changed. Only spark_* folders are
# candidates; a folder modified in the last 120 minutes is skipped (a live round may use it).
# Per folder: count non-directory entries at source; rsync -a (no --delete); count at destination; ONLY if equal,
# a second pass (--remove-source-files) completes the move. The empty directory skeleton stays at the source
# (the same as the gate-clone move; the no-delete hook forbids removing it). A mismatch leaves the source untouched.
# Usage: archive_spark_work_20261109_nas.sh --dry | --run [LISTFILE]
# Test overrides (red-proof): SRC_ROOT, DST, MANDIR env vars; SABOTAGE=1 renames one file in the destination copy
# before it is counted (honoured only when DST is under /private/tmp).
set -u
MODE="${1:-}"; [ "$MODE" = "--dry" ] || [ "$MODE" = "--run" ] || { echo "usage: $0 --dry|--run [LISTFILE]" >&2; exit 2; }
LIST="${2:-}"
SRC_ROOT="${SRC_ROOT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work}"
DST="${DST:-/Volumes/DEV-Working/Secuura/Blockchain/WIP/2026-11-09_spark-work-clones}"
MANDIR="${MANDIR:-/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-clones-to-nas}"
case "$DST" in /private/tmp/*) ;; *) [ -d /Volumes/DEV-Working ] || { echo "ABORT: DEV-Working share not mounted" >&2; exit 3; };; esac
[ -d "$SRC_ROOT" ] || { echo "ABORT: no source root" >&2; exit 3; }
if [ -n "$LIST" ]; then NAMES=$(cat "$LIST"); else NAMES=$(ls "$SRC_ROOT" | grep '^spark_'); fi
echo "df before:"; df -h /Volumes/DevMASTER | tail -1
mkdir -p "$DST" "$MANDIR"
MAN="$DST/manifest.txt"
[ "$MODE" = "--run" ] && echo "# manifest $(date '+%Y-%m-%d %H:%M:%S %Z') — name | files at source | files at destination | result" >> "$MAN"
FAILS=0; N=0
for g in $NAMES; do
  case "$g" in spark_*) ;; *) echo "$g: not a spark_ clone (skip)"; continue;; esac
  SRC="$SRC_ROOT/$g"
  [ -d "$SRC" ] || { echo "$g: missing (skip)"; continue; }
  if [ -n "$(find "$SRC" -maxdepth 0 -mmin -120)" ]; then echo "$g: modified <2h ago (skip)"; continue; fi
  NS=$(find "$SRC" -not -type d 2>&1 | wc -l | tr -d ' ')
  if [ "$MODE" = "--dry" ]; then echo "$g: would move ($NS files) -> $DST/$g"; N=$((N+1)); continue; fi
  mkdir -p "$DST/$g"
  rsync -a "$SRC/" "$DST/$g/"; RC=$?
  if [ "${SABOTAGE:-}" = "1" ]; then case "$DST" in /private/tmp/*) f=$(find "$DST/$g" -type f | head -1); [ -n "$f" ] && mv "$f" "$f.sabotaged";; esac; fi
  ND=$(find "$DST/$g" -not -type d 2>&1 | wc -l | tr -d ' ')
  if [ $RC -eq 0 ] && [ "$NS" = "$ND" ]; then
    rsync -a --remove-source-files "$SRC/" "$DST/$g/"; RC2=$?
    NL=$(find "$SRC" -not -type d 2>&1 | wc -l | tr -d ' ')
    echo "$g | $NS | $ND | MOVED (remove pass rc=$RC2, files left at source $NL)" | tee -a "$MAN"
    [ "$RC2" -eq 0 ] && [ "$NL" = "0" ] || FAILS=$((FAILS+1))
  else
    FAILS=$((FAILS+1)); echo "$g | $NS | $ND | MISMATCH rsync rc=$RC — source LEFT IN PLACE" | tee -a "$MAN"
  fi
  N=$((N+1))
done
[ "$MODE" = "--run" ] && cp "$MAN" "$MANDIR/manifest.txt"
echo "df after:"; df -h /Volumes/DevMASTER | tail -1
echo "processed=$N FAILS=$FAILS"; [ $FAILS -eq 0 ]
