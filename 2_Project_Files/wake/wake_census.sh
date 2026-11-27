#!/bin/bash
# wake_census.sh — BEFORE and AFTER of a seat's boot, in bytes and estimated tokens (WED-170 step 1).
# BEFORE = the whole-file reads the CURRENT boot prompt mandates (census 2026-11-27, tables A3/A4:
#   steps 1 to 5; partial reads, live sources and on-demand files are not counted), re-measured
#   from the files now.
# AFTER  = the wake pack, and the pack plus the whole reads the proposed prompt still mandates
#   (both rules files, the week instruction, yesterday's and today's notes: Kam's 2026-08-06 rule
#   on the two daily notes is kept).
# Tokens are bytes/4 rounded up: an estimate, not a tokenizer reading.
#
# Usage: wake_census.sh [--seat <wednesday|tuesday|friday>] [--pack <path>] [--root <tree>] [--today YYYY-MM-DD]
#   --seat   default: the tree's seat (fleet/cockpit/seat_resolve.sh)
#   --pack   default: <root>/0_Brain/wake/WAKE-<seat>.md
# Reads sizes only (wc -c); opens no file for content except the pack's own manifest table.
# Writes nothing. macOS bash 3.2 (uses BSD `date -j -v`). Never discards stderr.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SEAT=""; PACK=""; TODAY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --seat)  SEAT="${2:-}"; shift 2 ;;
    --pack)  PACK="${2:-}"; shift 2 ;;
    --root)  ROOT="${2:-}"; shift 2 ;;
    --today) TODAY="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,15p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "wake_census: unknown argument '$1'" >&2; exit 2 ;;
  esac
done
[ -d "$ROOT/0_Brain" ] || { echo "wake_census: no 0_Brain under root '$ROOT'" >&2; exit 2; }
if [ -z "$SEAT" ]; then
  RES="$SCRIPT_DIR/../fleet/cockpit/seat_resolve.sh"
  # shellcheck disable=SC1090
  . "$RES" || { echo "wake_census: cannot load $RES; pass --seat" >&2; exit 2; }
  seat_resolve "$ROOT"
fi
case "$SEAT" in
  wednesday) LEDGER="_ledger.md";                PICKUP="NEXT-PICKUP.md";         WEEK="WEEK-INSTRUCTION.md";         DAILY="daily" ;;
  tuesday)   LEDGER="_ledger_laptop_datasec.md"; PICKUP="NEXT-PICKUP-TUESDAY.md"; WEEK="WEEK-INSTRUCTION-TUESDAY.md"; DAILY="daily_tuesday" ;;
  friday)    LEDGER="_ledger_friday.md";         PICKUP="NEXT-PICKUP-FRIDAY.md";  WEEK="WEEK-INSTRUCTION-FRIDAY.md";  DAILY="daily_friday" ;;
  *) echo "wake_census: unknown seat '$SEAT' (wednesday, tuesday or friday)" >&2; exit 2 ;;
esac
[ -n "$TODAY" ] || TODAY="$(date +%F)"
YDAY="$(date -j -v-1d -f %Y-%m-%d "$TODAY" +%F)" || { echo "wake_census: cannot derive yesterday from '$TODAY'" >&2; exit 2; }
[ -n "$PACK" ] || PACK="$ROOT/0_Brain/wake/WAKE-$SEAT.md"

B="$ROOT/0_Brain"
TOTAL=0; NOIDX=0; KEPT=0; NOTES=0
tok() { echo $(( ($1 + 3) / 4 )); }
bytes() { if [ -f "$1" ]; then wc -c < "$1" | tr -d ' '; else echo ""; fi; }
row() { # <step> <label> <abs path> <flags: i = index/entries, k = still read whole after the change>
  local n; n="$(bytes "$3")"
  if [ -z "$n" ]; then
    printf '  %-5s %-58s %10s %9s\n' "$1" "$2" "absent" "-"
    return 0
  fi
  printf '  %-5s %-58s %10d %9d\n' "$1" "$2" "$n" "$(tok "$n")"
  TOTAL=$((TOTAL + n))
  case "${4:-}" in *i*) ;; *) NOIDX=$((NOIDX + n)) ;; esac
  case "${4:-}" in *k*) KEPT=$((KEPT + n)) ;; esac
  case "${4:-}" in *d*) NOTES=$((NOTES + n)) ;; esac
  return 0
}

echo "wake census: seat $SEAT, tree $ROOT, measured $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo
echo "BEFORE: whole reads the current boot prompt mandates (steps 1 to 5)"
printf '  %-5s %-58s %10s %9s\n' "step" "file" "bytes" "~tokens"
row 1 "CLAUDE.md" "$ROOT/CLAUDE.md" k
row 1 "0_Brain/CLAUDE.md" "$B/CLAUDE.md" k
row 2 "0_Brain/identity/persona.md" "$B/identity/persona.md"
row 2 "0_Brain/identity/voice-protocol.md" "$B/identity/voice-protocol.md"
row 2 "0_Brain/people/kam.md" "$B/people/kam.md"
if [ -f "$B/learnings/_rules_card_$SEAT.md" ]; then
  row 3 "0_Brain/learnings/_rules_card_$SEAT.md" "$B/learnings/_rules_card_$SEAT.md"
else
  row 3 "0_Brain/learnings/_boot_digest_by_tier.md (no card)" "$B/learnings/_boot_digest_by_tier.md"
fi
row 3 "0_Brain/learnings/$LEDGER" "$B/learnings/$LEDGER"
row 4 "0_Brain/tasks/$PICKUP" "$B/tasks/$PICKUP"
row 4 "0_Brain/tasks/EXPIRING-GRANTS.md" "$B/tasks/EXPIRING-GRANTS.md"
row 4 "0_Brain/tasks/TASKS.md" "$B/tasks/TASKS.md"
row 4 "0_Brain/projects_index/INDEX.md" "$B/projects_index/INDEX.md" i
ENT_N=0; ENT_B=0; ENT_C=0; ENT_CB=0
if [ -d "$B/projects_index/entries" ]; then
  for f in "$B/projects_index/entries"/*; do
    [ -f "$f" ] || continue
    n="$(bytes "$f")"; ENT_N=$((ENT_N + 1)); ENT_B=$((ENT_B + n))
    case "$(basename "$f")" in *"(conflict_on_"*|*.pre-*) ENT_C=$((ENT_C + 1)); ENT_CB=$((ENT_CB + n)) ;; esac
  done
fi
printf '  %-5s %-58s %10d %9d\n' 4 "0_Brain/projects_index/entries/* ($ENT_N files, $ENT_C conflict/backup)" "$ENT_B" "$(tok "$ENT_B")"
TOTAL=$((TOTAL + ENT_B))
row 4 "0_Brain/tasks/$WEEK" "$B/tasks/$WEEK" k
row 5 "0_Brain/$DAILY/$YDAY.md (yesterday)" "$B/$DAILY/$YDAY.md" kd
row 5 "0_Brain/$DAILY/$TODAY.md (today)" "$B/$DAILY/$TODAY.md" kd
printf '  %-5s %-58s %10d %9d\n' "" "TOTAL, with INDEX.md and entries whole" "$TOTAL" "$(tok "$TOTAL")"
CLEAN=$((TOTAL - ENT_CB))
printf '  %-5s %-58s %10d %9d\n' "" "TOTAL, without the $ENT_C sync-conflict / backup copies" "$CLEAN" "$(tok "$CLEAN")"
printf '  %-5s %-58s %10d %9d\n' "" "TOTAL, without INDEX.md and entries" "$NOIDX" "$(tok "$NOIDX")"
echo "  (The prompt says 'every file in entries/', so a seat obeying it reads the conflict copies too: the first total."
echo "   A seat that skips them reads the second. The honest headline is the reduction against the SECOND, the lower one.)"
echo
echo "AFTER: the wake pack"
if [ -f "$PACK" ]; then
  PB="$(bytes "$PACK")"
  printf '  %-5s %-58s %10d %9d\n' "" "pack: $PACK" "$PB" "$(tok "$PB")"
  AFTER=$((PB + KEPT))
  printf '  %-5s %-58s %10d %9d\n' "" "pack + rules files + week instruction + two daily notes" "$AFTER" "$(tok "$AFTER")"
  ALT=$((PB + KEPT - NOTES))
  printf '  %-5s %-58s %10d %9d\n' "" "the same with earlier notes on demand (Kam's to rule)" "$ALT" "$(tok "$ALT")"
  echo
  echo "  pack, per part (its own manifest):"
  awk '/^## Manifest/{f=1; next} f && /^## /{exit} f && /^\|/{print "  " $0}' "$PACK"
  echo
  if [ "$TOTAL" -gt 0 ]; then
    pct() { # <before> <after> -> the reduction in percent, one decimal, truncated; negative when after is larger
      local pm=$(( ($1 - $2) * 1000 / $1 )) sign=""
      [ "$pm" -lt 0 ] && { sign="-"; pm=$(( -pm )); }
      echo "${sign}$(( pm / 10 )).$(( pm % 10 ))"
    }
    echo "REDUCTION (headline, the lower figure): $CLEAN -> $AFTER bytes, $(pct "$CLEAN" "$AFTER")% less, against BEFORE without sync-conflict copies; ~$(tok "$CLEAN") -> ~$(tok "$AFTER") tokens."
    echo "           against BEFORE with the conflict copies counted ($TOTAL bytes): $(pct "$TOTAL" "$AFTER")% less."
    echo "           against BEFORE without INDEX.md and entries ($NOIDX bytes): $(pct "$NOIDX" "$AFTER")% less."
  fi
else
  echo "  pack: MISSING at $PACK (build it: python3 2_Project_Files/wake/wake_pack.py --seat $SEAT)"
fi
echo
echo "Not counted on either side: partial reads (scoreboard head, other ledgers' headlines), live sources (Linear, mail, boards), on-demand files and the prompt itself."
