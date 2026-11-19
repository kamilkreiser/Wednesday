#!/bin/bash
# nas_verify.sh — verify a NAS backup folder against its source, read-only on both sides.
# WHY (2026-11-19): nas_backup.sh's per-file check compared two FAILED hash commands as equal ("ok  shasum:")
# and then died on a size lookup with exit 0, so a run reported success with three quarters of the files unchecked.
# This tool hashes each side in one batch (shasum over xargs), compares the two lists BY PATH, retries only the
# entries that differ, and treats ANY read error as a failure. It never prints VERIFIED unless every selected source
# file is on the NAS with the same sha256 and nothing errored.
#
# Usage: nas_verify.sh <source dir> <dest dir: the copy of that source on the NAS> <report file>
# Selection mirrors nas_backup.sh's excludes: 4_Credentials/, 3_Access_Keys/, .env, *.env, *.pem, *.key,
#   id_rsa*, id_ed25519*, *.p12, *.pfx, tools/target/, node_modules/; regular files only; MANIFEST.txt at the
#   destination top is ignored.
# Exit: 0 VERIFIED · 2 usage · 4 NOT VERIFIED (missing, extra, mismatch or read error; see the report).
set -u
SRC="${1:-}"; DST="${2:-}"; REP="${3:-}"
[ -d "$SRC" ] && [ -d "$DST" ] && [ -n "$REP" ] || { echo "usage: nas_verify.sh <source dir> <dest dir> <report file>" >&2; exit 2; }
W=$(mktemp -d)
sel() {  # $1 = root; prints sha256 lines "hash  ./rel" for the selected regular files; errors to $2
  ( cd "$1" && find . \( -type d \( -name 4_Credentials -o -name 3_Access_Keys -o -name node_modules -o -path '*/tools/target' \) -prune \) -o \
      \( -type f ! -name '.env' ! -name '*.env' ! -name '*.pem' ! -name '*.key' ! -name 'id_rsa*' ! -name 'id_ed25519*' \
         ! -name '*.p12' ! -name '*.pfx' ! -path './MANIFEST.txt' -print0 \) | xargs -0 shasum -a 256 ) 2> "$2"
}
sel "$SRC" "$W/src.err" | LC_ALL=C sort -k2 > "$W/src.sha"
sel "$DST" "$W/dst.err" | LC_ALL=C sort -k2 > "$W/dst.sha"
# Every line must be a 64-hex hash, two spaces, a path. Anything else is a read problem.
badfmt() { LC_ALL=C /usr/bin/grep -c -v -E '^[0-9a-f]{64}  \./' "$1"; }
NS=$(wc -l < "$W/src.sha" | tr -d ' '); ND=$(wc -l < "$W/dst.sha" | tr -d ' ')
cut -c67- "$W/src.sha" > "$W/src.paths"; cut -c67- "$W/dst.sha" > "$W/dst.paths"
LC_ALL=C comm -23 "$W/src.paths" "$W/dst.paths" > "$W/missing"
LC_ALL=C comm -13 "$W/src.paths" "$W/dst.paths" > "$W/extra"
LC_ALL=C join -t "$(printf '\t')" -j 1 \
  <(awk '{print substr($0,67) "\t" substr($0,1,64)}' "$W/src.sha" | LC_ALL=C sort) \
  <(awk '{print substr($0,67) "\t" substr($0,1,64)}' "$W/dst.sha" | LC_ALL=C sort) \
  | awk -F'\t' '$2 != $3 {print $1}' > "$W/differ"
# Retry each missing or differing entry once, after a pause (a file can be briefly unreadable).
: > "$W/still"; RETRIED=0
if [ -s "$W/missing" ] || [ -s "$W/differ" ]; then
  sleep 5
  cat "$W/missing" "$W/differ" | while IFS= read -r p; do
    a=$(shasum -a 256 "$SRC/${p#./}" 2>&1 | awk '{print $1}'); b=$(shasum -a 256 "$DST/${p#./}" 2>&1 | awk '{print $1}')
    case "$a" in *[!0-9a-f]*|"") echo "SRC-READ-ERROR  $p" >> "$W/still"; continue ;; esac
    [ ${#a} -eq 64 ] || { echo "SRC-READ-ERROR  $p" >> "$W/still"; continue; }
    [ "$a" = "$b" ] || echo "DIFFERS-OR-MISSING  src=$a dst=$b  $p" >> "$W/still"
  done
  RETRIED=$(cat "$W/missing" "$W/differ" | wc -l | tr -d ' ')
fi
BF_S=$(badfmt "$W/src.sha"); BF_D=$(badfmt "$W/dst.sha")
PROB=0
[ -s "$W/still" ] && PROB=$((PROB + $(wc -l < "$W/still")))
[ -s "$W/extra" ] && PROB=$((PROB + $(wc -l < "$W/extra")))
[ "$BF_S" -eq 0 ] || PROB=$((PROB+BF_S)); [ "$BF_D" -eq 0 ] || PROB=$((PROB+BF_D))
[ -s "$W/src.err" ] && PROB=$((PROB+1)); [ -s "$W/dst.err" ] && PROB=$((PROB+1))
[ "$NS" -gt 0 ] || PROB=$((PROB+1))
{
  echo "NAS VERIFY — written by FRIDAY 2_Project_Files/friday/nas_verify.sh at $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "source: $SRC"; echo "dest:   $DST"
  echo "selected source files: $NS · files at dest: $ND · first-pass missing: $(wc -l < "$W/missing" | tr -d ' ') · differing: $(wc -l < "$W/differ" | tr -d ' ') · retried: $RETRIED"
  echo "badly formed hash lines: src $BF_S, dest $BF_D"
  [ -s "$W/src.err" ] && { echo "SOURCE READ ERRORS:"; cat "$W/src.err"; }
  [ -s "$W/dst.err" ] && { echo "DEST READ ERRORS:"; cat "$W/dst.err"; }
  [ -s "$W/extra" ] && { echo "EXTRA AT DEST (not in the source selection):"; cat "$W/extra"; }
  [ -s "$W/still" ] && { echo "STILL WRONG AFTER RETRY:"; cat "$W/still"; }
  echo "problems: $PROB"
  echo "## per-file sha256 (source side)"; cat "$W/src.sha"
} > "$REP"
mv "$W" "$W.done"
if [ "$PROB" -eq 0 ]; then echo "VERIFIED: $NS files, every one on the NAS with the same sha256 (report $REP)"; exit 0; fi
echo "NOT VERIFIED: $PROB problem(s) over $NS selected files; see $REP" >&2; exit 4
