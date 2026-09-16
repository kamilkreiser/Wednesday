#!/bin/bash
# Move Kam's PERSONAL ollama store (~/.ollama, 141 GB, 55 files) onto DevMASTER.
#
# Kam, 2026-09-16 13:40 + 13:46: the internal disk is 95% full; ollama, external models and anything
# large should run off DevMASTER, under a new system folder at the drive root. "yes, create a folder
# and move ollama. change all the reference pointers".
#
# ADDITIVE ONLY — rsync without --delete, and the SOURCE IS NOT REMOVED by this script. Kam's rule is
# never delete (2026-08-26); reclaiming the 141 GB is a separate, explicit step he authorises once the
# destination is verified. Verification is by FILE COUNT plus a HASH SAMPLE at the DESTINATION, never
# by `du` and never by rsync's exit code alone (2026-08-05_verify-the-chain-not-the-legs).
#
# Note this writes outside /Volumes/DevMASTER/WEDNESDAY, which hard rule 1 normally forbids. It is on
# Kam's explicit instruction, it is workspace-general rather than any client's, and it is recorded here.
#
# Usage:
#   bash move_ollama_store.sh            # copy + verify
#   bash move_ollama_store.sh --verify   # verify only (re-runnable)
set -u
SRC="$HOME/.ollama"
DST="/Volumes/DevMASTER/SYSTEM/ollama"
LOG="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/logs/move_ollama_$(date +%Y%m%d_%H%M).log"
mkdir -p "$(dirname "$LOG")" "$DST"

verify() {
  local sc dc bad=0
  sc="$(find "$SRC" -type f 2>/dev/null | wc -l | tr -d ' ')"
  dc="$(find "$DST" -type f 2>/dev/null | wc -l | tr -d ' ')"
  echo "file count: source $sc -> destination $dc"
  [ "$sc" = "$dc" ] || { echo "MISMATCH: counts differ"; bad=1; }
  # Hash sample: the three LARGEST blobs, compared at both ends. A size match is not a content match.
  local rel
  find "$SRC" -type f -size +1G 2>/dev/null | head -3 | while read -r f; do
    rel="${f#$SRC/}"
    if [ ! -f "$DST/$rel" ]; then echo "MISSING at destination: $rel"; continue; fi
    local a b
    a="$(shasum -a 256 "$f" | awk '{print $1}')"
    b="$(shasum -a 256 "$DST/$rel" | awk '{print $1}')"
    if [ "$a" = "$b" ]; then echo "  hash OK  ${rel:0:70}"; else echo "  HASH MISMATCH  $rel"; fi
  done
  return $bad
}

if [ "${1:-}" = "--verify" ]; then verify; exit $?; fi

echo "$(date '+%F %T') copying $SRC -> $DST (additive, no --delete)" | tee -a "$LOG"
rsync -a --info=progress2 "$SRC/" "$DST/" >> "$LOG" 2>&1
rc=$?
echo "$(date '+%F %T') rsync rc=$rc" | tee -a "$LOG"
[ "$rc" -eq 0 ] || { echo "rsync FAILED rc=$rc — see $LOG (source untouched)"; exit "$rc"; }
verify | tee -a "$LOG"
echo
echo "SOURCE NOT REMOVED. $SRC still holds its 141 GB — that is deliberate."
echo "Reclaim it only on Kam's word, and by moving it aside rather than deleting:"
echo "  mv \"$SRC\" \"$HOME/.ollama_superseded_$(date +%F)\""
