#!/bin/bash
# nas_backup.sh — Friday's backup of trees to the DEV-Working NAS, in a dated, named folder, every copied file
# verified by sha256, with a MANIFEST so the folder can be reviewed and cleaned up later.
# Derived from tuesday/tools/nas_offload.sh (same rules), adding: an AREA per client, excludes for secrets and
# regenerable build output (so a whole seat or project tree can be backed up), a file-count match between what
# rsync selects and what landed, and a secret-name scan of the destination with a positive control.
#
# Usage: nas_backup.sh <area: friday|datasec|general> <topic-kebab> "<why, one sentence>" <abs source> [source ...]
#   friday  -> /Volumes/DEV-Working/Friday/<YYYY-MM-DD>_<topic>/          (sources under /Volumes/Laptop-DEV/FRIDAY only)
#   datasec -> /Volumes/DEV-Working/Datasec/Friday/<YYYY-MM-DD>_<topic>/  (each source path must name Datasec)
#   general -> /Volumes/DEV-Working/General/Friday/<YYYY-MM-DD>_<topic>/  (each source path must name General or Claude to Claude)
#
# WHY (Kam, Friday terminal 2026-11-19, verbatim): "please backup all the work we did and yourself to the NAS
# /DEV-Working.  create a folder for yourself and for datasec and the projects you have worked on."
# Workflow lesson (Tuesday's, same NAS): 0_Brain/learnings/2026-11-11_nas-dev-working-dated-offload.md
#
# Rules built in:
#  - CLIENT ISOLATION: one area per run; the area's source check refuses a path naming another client. Never writes
#    under Secuura/ (no area maps there). A Secuura backup is the Wednesday seat's.
#  - COPY, NEVER MOVE: sources never changed. No --delete. An existing destination is refused (never overwritten).
#  - NO SECRETS: rsync excludes 4_Credentials/, 3_Access_Keys/, .env, *.env, *.pem, *.key, id_rsa*, id_ed25519*,
#    *.p12, *.pfx; afterwards the destination is scanned for those names (must be 0) and the scanner is proved on a
#    planted control file in a temp dir first. RESIDUAL (not covered): a secret written INSIDE an ordinary file
#    (a config, a note) is copied as it is in the source.
#  - REGENERABLE OUTPUT excluded: tools/target/ (Rust build output), node_modules/. Said in the MANIFEST.
#  - Refuses if the NAS is not an smbfs mount (an unmounted path would write onto the local disk).
# Exit: 0 VERIFIED; 2 usage/refusal; 3 copy failed; 4 verification failed (mismatch, count, or secret found).
set -u
NAS=/Volumes/DEV-Working
AREA="${1:-}"; TOPIC="${2:-}"; WHY="${3:-}"
[ $# -ge 4 ] || { echo "usage: nas_backup.sh <friday|datasec|general> <topic-kebab> \"<why>\" <source> [source ...]" >&2; exit 2; }
shift 3
case "$AREA" in
  friday)  ROOT="$NAS/Friday" ;;
  datasec) ROOT="$NAS/Datasec/Friday" ;;
  general) ROOT="$NAS/General/Friday" ;;
  *) echo "nas_backup: REFUSED — area must be friday, datasec or general (got '$AREA')" >&2; exit 2 ;;
esac
case "$TOPIC" in *[!a-z0-9-]*|""|-*) echo "nas_backup: REFUSED — topic '$TOPIC' must be kebab-case [a-z0-9-]" >&2; exit 2 ;; esac
[ ${#WHY} -ge 10 ] || { echo "nas_backup: REFUSED — give a one-sentence reason (it goes in the MANIFEST)" >&2; exit 2; }
mount | /usr/bin/grep -q " on $NAS (smbfs" || { echo "nas_backup: REFUSED — $NAS is not mounted as a network share (no smbfs entry); nothing written" >&2; exit 2; }
for s in "$@"; do
  [ -e "$s" ] || { echo "nas_backup: REFUSED — no such source: $s" >&2; exit 2; }
  case "$s" in /*) ;; *) echo "nas_backup: REFUSED — give absolute source paths: $s" >&2; exit 2 ;; esac
  case "$s" in */4_Credentials*|*/3_Access_Keys*) echo "nas_backup: REFUSED — $s is a secrets folder" >&2; exit 2 ;; esac
  lc=$(printf '%s' "$s" | tr 'A-Z' 'a-z')
  case "$AREA" in
    friday)  case "$s" in /Volumes/Laptop-DEV/FRIDAY|/Volumes/Laptop-DEV/FRIDAY/*) ;; *) echo "nas_backup: REFUSED — area friday takes only the FRIDAY tree: $s" >&2; exit 2 ;; esac ;;
    datasec) case "$lc" in *datasec*) ;; *) echo "nas_backup: REFUSED — area datasec: source path does not name Datasec: $s" >&2; exit 2 ;; esac
             case "$lc" in *secuura*) echo "nas_backup: REFUSED — area datasec: source names another client: $s" >&2; exit 2 ;; esac ;;
    general) case "$lc" in *general*|*"claude to claude"*|*claude-to-claude*) ;; *) echo "nas_backup: REFUSED — area general: source path does not name General or Claude to Claude: $s" >&2; exit 2 ;; esac
             case "$lc" in *secuura*|*datasec*) echo "nas_backup: REFUSED — area general: source names another client: $s" >&2; exit 2 ;; esac ;;
  esac
done
EXCL=( --exclude='4_Credentials/' --exclude='3_Access_Keys/' --exclude='.env' --exclude='*.env' --exclude='*.pem'
       --exclude='*.key' --exclude='id_rsa*' --exclude='id_ed25519*' --exclude='*.p12' --exclude='*.pfx'
       --exclude='tools/target/' --exclude='node_modules/' )
secret_scan() {  # prints secret-shaped file names under $1
  find "$1" \( -name '.env' -o -name '*.env' -o -name '*.pem' -o -name '*.key' -o -name 'id_rsa*' -o -name 'id_ed25519*' -o -name '*.p12' -o -name '*.pfx' \) -print 2>&1
}
# Positive control: the scanner must find a planted file before its zero on the NAS means anything.
CTL=$(mktemp -d); : > "$CTL/control.pem"
[ -n "$(secret_scan "$CTL")" ] || { echo "nas_backup: REFUSED — the secret scanner failed its positive control" >&2; exit 2; }
mv "$CTL/control.pem" "$CTL/control.pem.done"
DAY=$(date +%Y-%m-%d); REVIEW=$(date -v+30d +%Y-%m-%d)
DEST="$ROOT/${DAY}_${TOPIC}"
[ -e "$DEST" ] && { echo "nas_backup: REFUSED — $DEST already exists (never overwritten); use a more specific topic" >&2; exit 2; }
mkdir -p "$DEST" || { echo "nas_backup: could not create $DEST" >&2; exit 3; }
MAN="$DEST/MANIFEST.txt"
{
  echo "NAS BACKUP (copy; sources untouched) — written by FRIDAY 2_Project_Files/friday/nas_backup.sh"
  echo "date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "seat: Friday (laptop coordinator)   area: $AREA   host: $(scutil --get ComputerName 2>&1)"
  echo "topic: $TOPIC"
  echo "why: $WHY"
  echo "excluded: secrets (4_Credentials/, 3_Access_Keys/, .env, *.env, *.pem, *.key, id_rsa*, id_ed25519*, *.p12, *.pfx) and regenerable build output (tools/target/, node_modules/)"
  echo "REVIEW-AFTER: $REVIEW  (eligible for clean-up review on or after this date; delete only on a human's word)"
  echo
} > "$MAN"
TOTAL_F=0; TOTAL_B=0; BAD=0
for s in "$@"; do
  name=$(basename "$s")
  echo "## source: $s" >> "$MAN"
  # What rsync SELECTS (regular files after excludes), counted before the copy, compared after it.
  want=$(rsync -a -n "${EXCL[@]}" --out-format='%i %n' "$s" "$CTL/dry/" 2>&1 | /usr/bin/grep -c '^>f')
  if ! rsync -rlt "${EXCL[@]}" "$s" "$DEST/" 2> "$DEST/.rsync_err_$name.txt"; then
    echo "nas_backup: COPY FAILED for $s (rsync stderr follows)" >&2; cat "$DEST/.rsync_err_$name.txt" >&2
    echo "COPY FAILED: $(cat "$DEST/.rsync_err_$name.txt")" >> "$MAN"; exit 3
  fi
  [ -s "$DEST/.rsync_err_$name.txt" ] && { echo "rsync warnings:"; cat "$DEST/.rsync_err_$name.txt"; } >> "$MAN"
  rm -f "$DEST/.rsync_err_$name.txt"
  if [ -d "$s" ]; then base="$s"; dbase="$DEST/$name"; else base=$(dirname "$s"); dbase="$DEST"; fi
  got=0
  # Verify every file that LANDED against its source (the copied set is the excluded-filtered set).
  while IFS= read -r -d '' d; do
    if [ -d "$s" ]; then rel="${d#$dbase/}"; f="$base/$rel"; else rel="$name"; f="$s"; fi
    a=$(shasum -a 256 "$f" 2>&1 | awk '{print $1}'); b=$(shasum -a 256 "$d" 2>&1 | awk '{print $1}')
    sz=$(stat -f %z "$d" 2>&1)
    if [ "$a" = "$b" ]; then echo "ok  $a  $sz  $rel" >> "$MAN"; else echo "MISMATCH  src=$a dst=$b  $rel" >> "$MAN"; BAD=$((BAD+1)); fi
    got=$((got+1)); TOTAL_F=$((TOTAL_F+1)); TOTAL_B=$((TOTAL_B+sz))
  done < <(if [ -d "$s" ]; then find "$dbase" -type f -print0; else printf '%s\0' "$DEST/$name"; fi)
  echo "count: rsync selected $want regular files, $got landed and were hashed" >> "$MAN"
  [ "$want" -eq "$got" ] || { echo "COUNT MISMATCH for $s: selected $want, landed $got" >> "$MAN"; BAD=$((BAD+1)); }
  echo >> "$MAN"
done
SEC=$(secret_scan "$DEST" | /usr/bin/grep -v '/MANIFEST.txt$')
if [ -n "$SEC" ]; then echo "SECRET-SHAPED FILES ON THE NAS (must be none):"; echo "$SEC"; BAD=$((BAD+1)); fi >> "$MAN"
echo "secret scan of destination: $( [ -z "$SEC" ] && echo '0 names (scanner proved on a planted control first)' || echo 'FOUND, see above')" >> "$MAN"
echo "TOTAL: $TOTAL_F files, $TOTAL_B bytes, problems $BAD" >> "$MAN"
if [ "$BAD" -ne 0 ] || [ "$TOTAL_F" -eq 0 ]; then
  echo "nas_backup: NOT VERIFIED — $BAD problem(s), $TOTAL_F file(s); see $MAN" >&2; exit 4
fi
echo "VERIFIED: $TOTAL_F files, $TOTAL_B bytes -> $DEST (MANIFEST.txt; review after $REVIEW). Sources untouched."
