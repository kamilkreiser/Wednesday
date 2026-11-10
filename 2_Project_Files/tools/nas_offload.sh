#!/bin/bash
# nas_offload.sh — copy (backup / offload) files or folders to the DEV-Working NAS in a dated, named folder,
# verify every file by sha256, and write a MANIFEST so the folder can be reviewed and cleaned up later.
#
# Usage: nas_offload.sh --client <secuura|general> <topic-in-kebab-case> <why, one sentence> <source path> [source path ...]
#   -> /Volumes/DEV-Working/Secuura/Wednesday/<YYYY-MM-DD>_<topic>/...  (--client secuura)
#   -> /Volumes/DEV-Working/General/Wednesday/<YYYY-MM-DD>_<topic>/...  (--client general: WED's own, non-client work)
# WEDNESDAY SEAT COPY (2026-11-11, Kam to Wednesday: "dont forget the NAS is connected so you can offlaod things there too"),
# from Tuesday's 2_Project_Files/tuesday/tools/nas_offload.sh; only the root and the --client switch differ.
#      + MANIFEST.txt (date, why, each source's absolute path, file count, bytes, sha256 per file,
#        REVIEW-AFTER date = today + 30 days)
#
# WHY (Kam, Tuesday terminal 2026-11-11 ~09:00, verbatim): "there is a new NAS on the network with a folder called
# DEV-Working. If you need to backup or offload anything there you can use that drive. Put it in a logical folder
# and with a date so we can periodically clean this up. please save this as an ongoing workflow"
# Lesson: 0_Brain/learnings/2026-11-11_nas-dev-working-dated-offload.md
#
# Rules built in:
#  - CLIENT ISOLATION: this seat writes ONLY under /Volumes/DEV-Working/Secuura/Wednesday/ or /General/Wednesday/.
#    It never reads, lists or writes Datasec/ (Tuesday's). One offload carries ONE client's material.
#  - COPY, NEVER MOVE: the source is never deleted or changed. Removing a source after an offload is a separate
#    decision, made only after this tool printed VERIFIED.
#  - NO SECRETS: refuses any source under 4_Credentials/ or 3_Access_Keys/, or any .env / *.pem / *.key / id_* file.
#  - Refuses if the NAS is not mounted (an unmounted path would write onto the local disk under /Volumes).
#  - A target folder that already exists is refused (no overwrite); pick a more specific topic.
# Exit: 0 VERIFIED; 2 usage/refusal; 3 copy failed; 4 verification mismatch.
set -u
NAS=/Volumes/DEV-Working
[ "${1:-}" = "--client" ] || { echo "usage: nas_offload.sh --client <secuura|general> <topic-kebab> \"<why>\" <source> [source ...]" >&2; exit 2; }
case "${2:-}" in secuura) ROOT="$NAS/Secuura/Wednesday" ;; general) ROOT="$NAS/General/Wednesday" ;; *) echo "nas_offload: REFUSED — --client must be secuura or general" >&2; exit 2 ;; esac
shift 2
case "$*" in *"/!CODING/Datasec"*|*"/TUESDAY/"*) echo "nas_offload: REFUSED — a Datasec source is Tuesday's, never offloaded by this seat" >&2; exit 2 ;; esac
TOPIC="${1:-}"; WHY="${2:-}"
[ $# -ge 3 ] || { echo "usage: nas_offload.sh <topic-kebab> \"<why>\" <source> [source ...]" >&2; exit 2; }
shift 2
case "$TOPIC" in *[!a-z0-9-]*|""|-*) echo "nas_offload: REFUSED — topic '$TOPIC' must be kebab-case [a-z0-9-]" >&2; exit 2 ;; esac
[ ${#WHY} -ge 10 ] || { echo "nas_offload: REFUSED — give a one-sentence reason (it goes in the MANIFEST)" >&2; exit 2; }
# The NAS must be a real network mount, not a stray local folder named like it.
mount | /usr/bin/grep -q " on $NAS (smbfs" || { echo "nas_offload: REFUSED — $NAS is not mounted as a network share (mount shows no smbfs entry); nothing written" >&2; exit 2; }
for s in "$@"; do
  [ -e "$s" ] || { echo "nas_offload: REFUSED — no such source: $s" >&2; exit 2; }
  case "$s" in /*) ;; *) echo "nas_offload: REFUSED — give absolute source paths: $s" >&2; exit 2 ;; esac
  case "$s" in */4_Credentials*|*/3_Access_Keys*) echo "nas_offload: REFUSED — $s is under a secrets folder" >&2; exit 2 ;; esac
  hit=$(find "$s" \( -name '.env' -o -name '*.env' -o -name '*.pem' -o -name '*.key' -o -name 'id_rsa*' -o -name 'id_ed25519*' -o -name '*.p12' -o -name '*.pfx' \) -print 2>&1 | head -3)
  [ -z "$hit" ] || { echo "nas_offload: REFUSED — secret-shaped file(s) inside $s:"; echo "$hit"; exit 2; } >&2
done
DAY=$(date +%Y-%m-%d); REVIEW=$(date -v+30d +%Y-%m-%d)
DEST="$ROOT/${DAY}_${TOPIC}"
[ -e "$DEST" ] && { echo "nas_offload: REFUSED — $DEST already exists (never overwritten); use a more specific topic" >&2; exit 2; }
mkdir -p "$DEST" || { echo "nas_offload: could not create $DEST" >&2; exit 3; }
MAN="$DEST/MANIFEST.txt"
{
  echo "NAS OFFLOAD (copy; sources untouched) — written by tools/nas_offload.sh (Wednesday seat)"
  echo "date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "seat: Wednesday (Secuura + general coordinator)   host: $(scutil --get ComputerName 2>&1)"
  echo "topic: $TOPIC"
  echo "why: $WHY"
  echo "REVIEW-AFTER: $REVIEW  (eligible for clean-up review on or after this date; delete only on a human's word)"
  echo
} > "$MAN"
TOTAL_F=0; TOTAL_B=0; BAD=0
for s in "$@"; do
  name=$(basename "$s")
  echo "## source: $s" >> "$MAN"
  # -a keeps times/modes where SMB allows; no --delete; errors go to the manifest and the console, never discarded.
  if ! rsync -a "$s" "$DEST/" 2> "$DEST/.rsync_err_$name.txt"; then
    echo "nas_offload: COPY FAILED for $s (rsync stderr follows)" >&2; cat "$DEST/.rsync_err_$name.txt" >&2
    echo "COPY FAILED: $(cat "$DEST/.rsync_err_$name.txt")" >> "$MAN"; exit 3
  fi
  [ -s "$DEST/.rsync_err_$name.txt" ] && { echo "rsync warnings:"; cat "$DEST/.rsync_err_$name.txt"; } >> "$MAN"
  rm -f "$DEST/.rsync_err_$name.txt"
  # Verify every regular file: sha256 at source == sha256 at destination.
  if [ -d "$s" ]; then base="$s"; dbase="$DEST/$name"; else base=$(dirname "$s"); dbase="$DEST"; fi
  while IFS= read -r -d '' f; do
    rel="${f#$base/}"; d="$dbase/$rel"; [ -f "$s" ] && d="$DEST/$name"
    a=$(shasum -a 256 "$f" | awk '{print $1}'); b=$(shasum -a 256 "$d" 2>&1 | awk '{print $1}')
    sz=$(stat -f %z "$f")
    if [ "$a" = "$b" ]; then echo "ok  $a  $sz  $rel" >> "$MAN"; else echo "MISMATCH  src=$a dst=$b  $rel" >> "$MAN"; BAD=$((BAD+1)); fi
    TOTAL_F=$((TOTAL_F+1)); TOTAL_B=$((TOTAL_B+sz))
  done < <(find "$s" -type f -print0)
  echo >> "$MAN"
done
echo "TOTAL: $TOTAL_F files, $TOTAL_B bytes, mismatches $BAD" >> "$MAN"
if [ "$BAD" -ne 0 ] || [ "$TOTAL_F" -eq 0 ]; then
  echo "nas_offload: NOT VERIFIED — $BAD mismatch(es), $TOTAL_F file(s); see $MAN" >&2; exit 4
fi
echo "VERIFIED: $TOTAL_F files, $TOTAL_B bytes -> $DEST (MANIFEST.txt; review after $REVIEW). Sources untouched."
