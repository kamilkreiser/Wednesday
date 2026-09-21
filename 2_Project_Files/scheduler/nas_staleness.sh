#!/bin/bash
# nas_staleness.sh — did the files that matter actually LAND on the NAS? (Kam 2026-09-21)
#
# A sync leg's rc certifies that its two roots agree about what it managed to copy; it says
# nothing about the file you care about (2026-08-05_verify-the-chain-not-the-legs). Six nights
# of rc=2 hid that history.md on the NAS was six days old while a finished daily note was
# byte-identical. This prints, for a fixed list of the busiest files, the mtime on each side
# and one word per file, decided by sha256 — never by mtime alone, because unison preserves
# mtimes (`times = true`) and an equal mtime with different bytes is exactly the case a
# "modified during synchronization" abort leaves behind.
#
#   SAME               sha256 equal on both sides
#   STALE <h>h         differs, source newer by <h> hours   (the retry pass should have carried it)
#   DIFF-NAS-NEWER <h>h differs, NAS newer — someone wrote there directly, or another leg did
#   MISSING            present at the source, absent on the NAS
#   NO-SRC             absent at the source — not a staleness (nothing to land)
#   SKIP               the NAS is not mounted / a root is absent — stated, not silently green
#
# READ-ONLY: stat + shasum on both trees, nothing else. Report, not enforcement: exit 0 always,
# EXCEPT with --warn-hours N (doctor.sh's mode), where exit 1 means at least one key file is
# MISSING or STALE by more than N hours. Agent-neutral: the seat directory is this script's own
# project folder, so on Tuesday's tree it reads TUESDAY/… .
#
# Usage:
#   nas_staleness.sh                         key files, source = this drive, NAS = /Volumes/Development
#   nas_staleness.sh --warn-hours 36         same, exit 1 on MISSING or STALE > 36 h
#   nas_staleness.sh --src DIR --dst DIR --file rel1 --file rel2 …   (the arms use this on temp trees;
#                                            --files takes a NEWLINE-separated list — paths may hold spaces)
set -u
SELF="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF/../.." && pwd)"
WORKSPACE="$(cd -P "$PROJECT_DIR/.." && pwd)"
SEAT_DIR="$(basename "$PROJECT_DIR")"

SRC="$WORKSPACE"
DST="${DEVNAS_TARGET_ROOT:-/Volumes/Development}"
WARN_HOURS=""
FILES=""
while [ $# -gt 0 ]; do
  case "$1" in
    --src) SRC="$2"; shift 2 ;;
    --dst) DST="$2"; shift 2 ;;
    --files) FILES="$2"; shift 2 ;;                       # NEWLINE-separated (paths may contain spaces)
    --file)  FILES="${FILES:+$FILES
}$2"; shift 2 ;;                                          # repeatable, one path each
    --warn-hours) WARN_HOURS="$2"; shift 2 ;;
    *) echo "nas_staleness: unknown argument $1" >&2; exit 2 ;;
  esac
done
if [ -z "$FILES" ]; then
  TODAY="$(date +%F)"; YESTERDAY="$(date -v-1d +%F)"
  FILES="$SEAT_DIR/5_Project_History/history.md
$SEAT_DIR/0_Brain/learnings/_ledger.md
$SEAT_DIR/0_Brain/daily/$TODAY.md
$SEAT_DIR/0_Brain/daily/$YESTERDAY.md
$SEAT_DIR/0_Brain/tasks/NEXT-PICKUP.md
$SEAT_DIR/2_Project_Files/local-model/night/done.md"
fi

echo "=== NAS staleness — $(date '+%Y-%m-%d %H:%M:%S') — src=$SRC nas=$DST (sha256 decides; hours from stat -f %m) ==="
if [ "$DST" = "/Volumes/Development" ] && ! mount | /usr/bin/grep -q " on $DST "; then
  echo "SKIP: $DST is not mounted — nothing measured (a stat on an unmounted path would report every file MISSING, which is not a measurement)"
  exit 0
fi
if [ ! -d "$SRC" ] || [ ! -d "$DST" ]; then
  echo "SKIP: a root is absent (src present=$([ -d "$SRC" ] && echo yes || echo no), nas present=$([ -d "$DST" ] && echo yes || echo no))"
  exit 0
fi

fmt_mtime() { date -r "$1" '+%m-%d %H:%M'; }   # $1 is always a stat -f %m integer here
n_same=0; n_stale=0; n_missing=0; n_nosrc=0; n_nasnewer=0; n_over=0
printf '%-22s %-12s %-12s %s\n' "STATUS" "SRC-MTIME" "NAS-MTIME" "FILE"
while IFS= read -r rel; do
  [ -n "$rel" ] || continue
  s="$SRC/$rel"; d="$DST/$rel"
  if [ ! -f "$s" ]; then
    printf '%-22s %-12s %-12s %s\n' "NO-SRC" "-" "$([ -f "$d" ] && fmt_mtime "$(stat -f %m "$d")" || echo -)" "$rel"
    n_nosrc=$((n_nosrc+1)); continue
  fi
  sm="$(stat -f %m "$s")"
  if [ ! -f "$d" ]; then
    printf '%-22s %-12s %-12s %s\n' "MISSING" "$(fmt_mtime "$sm")" "-" "$rel"
    n_missing=$((n_missing+1)); continue
  fi
  dm="$(stat -f %m "$d")"
  sh_s="$(shasum -a 256 "$s" | awk '{print $1}')"
  sh_d="$(shasum -a 256 "$d" | awk '{print $1}')"
  if [ "$sh_s" = "$sh_d" ]; then
    printf '%-22s %-12s %-12s %s\n' "SAME" "$(fmt_mtime "$sm")" "$(fmt_mtime "$dm")" "$rel"
    n_same=$((n_same+1))
  elif [ "$sm" -ge "$dm" ]; then
    h="$(awk -v a="$sm" -v b="$dm" 'BEGIN{printf "%.1f", (a-b)/3600}')"
    printf '%-22s %-12s %-12s %s\n' "STALE ${h}h" "$(fmt_mtime "$sm")" "$(fmt_mtime "$dm")" "$rel"
    n_stale=$((n_stale+1))
    if [ -n "$WARN_HOURS" ] && awk -v h="$h" -v w="$WARN_HOURS" 'BEGIN{exit !(h>w)}'; then n_over=$((n_over+1)); fi
  else
    h="$(awk -v a="$dm" -v b="$sm" 'BEGIN{printf "%.1f", (a-b)/3600}')"
    printf '%-22s %-12s %-12s %s\n' "DIFF-NAS-NEWER ${h}h" "$(fmt_mtime "$sm")" "$(fmt_mtime "$dm")" "$rel"
    n_nasnewer=$((n_nasnewer+1))
  fi
done <<< "$FILES"
echo "staleness: same=$n_same stale=$n_stale${WARN_HOURS:+ (over ${WARN_HOURS}h: $n_over)} nas-newer=$n_nasnewer missing=$n_missing no-src=$n_nosrc"
if [ -n "$WARN_HOURS" ]; then
  [ "$n_missing" -eq 0 ] && [ "$n_over" -eq 0 ] && exit 0
  exit 1
fi
exit 0
