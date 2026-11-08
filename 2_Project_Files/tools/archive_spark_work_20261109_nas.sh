#!/bin/bash
# archive_spark_work_20261109_nas.sh — copy Wednesday's regenerable Spark per-round work clones
# (spark/cache/work/spark_*) to the NAS (DEV-Working), and remove a SOURCE folder ONLY after the NAS copy's
# file count matches the source's. Kam 2026-11-09: card wed-disk-16gib-prune-freed-nothing-1109 = a, and
# "use the nas" on wed-disk-clone-delete-blocked-by-hook-1108. Pattern copied from archive_gate_clones_20261108_nas.sh.
# Excludes: non-spark_ names, and anything with a file or dir modified in the last 2 hours (live round).
# The ONLY removal is of a source folder whose destination count matched.
# Usage: archive_spark_work_20261109_nas.sh --dry | --run   (env SRCDIR / DSTDIR / MOUNT / COPY_HOOK override, red-proof only)
set -u
MODE="${1:-}"; [ "$MODE" = "--dry" ] || [ "$MODE" = "--run" ] || { echo "usage: $0 --dry|--run" >&2; exit 2; }
W="${SRCDIR:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work}"
DST="${DSTDIR:-/Volumes/DEV-Working/Secuura/Blockchain/WIP/2026-11-09_spark-work-clones}"
MOUNT="${MOUNT:-/Volumes/DEV-Working}"
COPY_HOOK="${COPY_HOOK:-}"   # red-proof only: a command run after the copy, given the dest dir
[ -d "$MOUNT" ] || { echo "ABORT: $MOUNT not mounted" >&2; exit 3; }
echo "df before:"; df -h /Volumes/DevMASTER | tail -1
[ "$MODE" = "--run" ] && mkdir -p "$DST"
MAN="$DST/manifest.txt"
[ "$MODE" = "--run" ] && echo "# manifest $(date '+%Y-%m-%d %H:%M:%S %Z') — name | files at source | files at destination | result" >> "$MAN"
FAILS=0; N=0; EXC=0
for p in "$W"/*/; do
  g=$(basename "$p"); SRC="$W/$g"
  case "$g" in spark_*) ;; *) echo "EXCLUDED $g | not a spark_ work clone"; EXC=$((EXC+1)); continue;; esac
  [ -L "$SRC" ] && { echo "EXCLUDED $g | symlink"; EXC=$((EXC+1)); continue; }
  if [ -n "$(find "$SRC" -mmin -120 -print -quit 2>/dev/null)" ]; then echo "EXCLUDED $g | modified within 2h (may be live)"; EXC=$((EXC+1)); continue; fi
  NS=$(find "$SRC" -type f 2>&1 | wc -l | tr -d ' ')
  if [ "$MODE" = "--dry" ]; then echo "$g: would copy $NS files -> $DST/$g, then remove source if counts match"; N=$((N+1)); continue; fi
  rsync -a "$SRC/" "$DST/$g/" ; RC=$?
  [ -n "$COPY_HOOK" ] && $COPY_HOOK "$DST/$g"
  ND=$(find "$DST/$g" -type f 2>&1 | wc -l | tr -d ' ')
  if [ $RC -eq 0 ] && [ "$NS" = "$ND" ]; then
    rm -rf "$SRC"; RM=$?
    echo "$g | $NS | $ND | MOVED (source removed rc=$RM)" | tee -a "$MAN"
    [ $RM -eq 0 ] || FAILS=$((FAILS+1))
  else
    FAILS=$((FAILS+1)); echo "$g | $NS | $ND | MISMATCH rsync rc=$RC — source LEFT IN PLACE" | tee -a "$MAN"
  fi
  N=$((N+1))
done
echo "processed=$N excluded=$EXC"
echo "df after:"; df -h /Volumes/DevMASTER | tail -1
echo "FAILS=$FAILS"; [ $FAILS -eq 0 ]
