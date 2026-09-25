#!/bin/bash
# One-way, ADDITIVE pull NAS -> DevMASTER of Tuesday's recent work (Kam, live board 2026-09-25 15:37:
# "sync with the NAS and once done, sync again with the Laptop drive"). Wednesday's recommendation sent
# 17:4x with an 18:00 default: only files dated since 2026-09-17, never overwrite a newer DevMASTER file
# (--update), never delete, skip the stale in-repo Datasec leftovers (code comes via git). File lists were
# built from the 15:39 dry run (nasdry itemized output) with the NAS leg's exclude set applied per path part.
# Usage: run_nas_pull.sh [--dry-run]   (writes a log beside this script; never discards stderr)
set -u
H="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY=(); [ "${1:-}" = "--dry-run" ] && DRY=(--dry-run)
RS=/opt/homebrew/bin/rsync
LOG="$H/run_$(date +%Y%m%d_%H%M%S)${DRY:+_dry}.log"
rc_all=0
for pair in "!CODING/Datasec|CODING_Datasec.files" "TUESDAY|TUESDAY.files" "Notes (MASTER)/Datasec|Notes_MASTER_Datasec.files"; do
  root="${pair%%|*}"; list="$H/${pair##*|}"
  [ -s "$list" ] || { echo "skip $root: empty list" | tee -a "$LOG"; continue; }
  echo "=== $root ($(wc -l < "$list") files) $(date '+%F %T')" | tee -a "$LOG"
  "$RS" -a --update --itemize-changes ${DRY[@]+"${DRY[@]}"} --files-from="$list" "/Volumes/Development/$root/" "/Volumes/DevMASTER/$root/" >> "$LOG" 2>&1
  rc=$?; echo "rc=$rc $root" | tee -a "$LOG"; [ $rc -ne 0 ] && rc_all=$rc
done
echo "=== done rc_all=$rc_all $(date '+%F %T')" | tee -a "$LOG"; exit $rc_all
