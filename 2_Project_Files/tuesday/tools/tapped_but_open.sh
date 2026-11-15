#!/bin/bash
# tapped_but_open.sh — list every card Kam has TAPPED today (a "Decision <id>: <key>" row on the
# live board) that is still OPEN in the decision store, so it still shows on his fleet activity board.
#
# WHY (ledger 2026-11-16, w=3 REGRESSION; lesson 2026-10-12_clear-fleet-activity-once-answered-as-a-rule):
# Kam's taps arrive as chat rows; they do NOT change the store. The seat must `decision_queue.sh rule
# <id> <key>` itself. First ruled 2026-09-08, repeated 2026-10-12, repeated again 2026-11-16 10:22:53
# ("please clear the fleet activity cards once they are decided. do this as a standing rule please"):
# that morning six tapped cards stayed open for up to 3 h 20 min and he re-tapped them at 10:01. The
# lesson existed; nothing checked it. This runs at the end of kam_rulings_today.sh, so every read of his
# rulings prints the tapped-but-open cards beside them.
#
# Read-only: it reads the rulings tool's output and `decision_queue.sh show`; it writes nothing.
# Usage: tapped_but_open.sh [--selftest]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
DQ="$ROOT/2_Project_Files/tools/decision_queue.sh"
KR="$ROOT/2_Project_Files/tools/kam_rulings_today.sh"

parse() {  # stdin: rulings lines -> "id key" per tapped card, the LAST tap of each id wins
  /usr/bin/python3 -I -c '
import re,sys
last={}
for line in sys.stdin:
    m=re.search(r"Decision ([a-z0-9][a-z0-9-]+): ([A-Za-z0-9]+) —", line)
    if m: last[m.group(1)]=m.group(2)
for k,v in last.items(): print(k, v)'
}

if [ "${1:-}" = "--selftest" ]; then
  out=$(printf '%s\n' "10:01 [live] | Decision demo-x-1116: a — Go" "10:02 [live] | Decision demo-x-1116: b — Hold" "10:03 [live] | Decision demo-y-1116 note: only a note" | parse)
  [ "$out" = "demo-x-1116 b" ] && echo "selftest PASS (last tap wins; a note-only row is not a tap)" || { echo "selftest FAIL: [$out]"; exit 1; }
  exit 0
fi

KAM_TBO_INNER=1 bash "$KR" 2>/dev/null | parse | while read -r id key; do
  st=$(bash "$DQ" show "$id" 2>/dev/null | /usr/bin/grep -i -E '^status' | awk '{print $2}')
  if [ "$st" = "open" ]; then
    echo "  ⚠ TAPPED BUT OPEN: $id (Kam tapped '$key'; store: open) -> bash $DQ rule $id $key"
  fi
done | { out=$(cat); if [ -n "$out" ]; then echo "# TAPPED-BUT-OPEN (rule these now; his board still shows them):"; printf '%s\n' "$out"; else echo "# TAPPED-BUT-OPEN: none (every card he tapped today is ruled in the store)"; fi; }
