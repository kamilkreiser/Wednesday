#!/bin/bash
# Friday's STATUS watcher (moved from a session scratchpad 2026-09-24: it had to be re-created at every rotation).
# Usage: watch_status.sh <seen-file> <glob> [<glob>…]     e.g.
#   watch_status.sh ~/.friday_seen "/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC/1_Project_Definition/Briefs/2026-09-24_B0*STATUS*.md"
# Run it in the background: it EXITS (waking the seat) when a STATUS gains a NEW "READY FOR REVIEW" line or states BLOCKED/STOP,
# or after ~55 min ("re-arm"). Keyed on the COUNT of READY lines, not the mtime: seats re-save a reviewed STATUS many times,
# and an mtime key false-fired on every save (2026-09-24). A seat that writes READY before its push/CI lines (B04 did) is caught
# by reading the file on the wake — the watcher is the wake, not the review.
#
# 2026-10-03 (ledger row of that date: THREE seats sat waiting on Friday unnoticed — a "READY FOR GATE", a
# "STOPPED: NEEDS FRIDAY" and a READY whose count had already been taken by an earlier "not ready for review"):
#   * READY FOR GATE counts as a READY; a line saying STOPPED / NEEDS FRIDAY / BLOCKED fires on its own count.
#   * WATCH_PANES="%6 %7 …" (optional): the watcher also EXITS when one of those panes goes from BUSY to any
#     not-busy state (seat_idle.sh's verdict), because a seat that ends its turn is the event, whatever it wrote.
#   * --seed as the first argument records the CURRENT keys in the seen file and exits 0 (the successor's first step;
#     an unseeded file fires on old READY lines).
# 2026-10-07 (ledger w=3 of the watcher-miss family: seats REPLACED their single READY line, the count stayed 1,
#   the key READY#1 was already seen, so four READYs sat ~8 h): the READY key now carries the LINE NUMBER of the last
#   READY line (READY#<count>@L<line>). A replaced READY lands on a new line and fires; text appended BELOW a READY
#   does not move it and stays quiet. Same day: a -LINE/-ROW/-FILE skeleton token needs TWO segments before it
#   (CI-RUN2-LINE), so prose like PRE-LINE no longer holds a real READY (arm A11 had hidden this: its cut -c1-5 matched
#   the expiry line's own "WAKE:"). Old-format seen files do not match: --seed once at boot after this change.
SEED=0; [ "${1:-}" = "--seed" ] && { SEED=1; shift; }
shopt -s nullglob
SEEN="${1:?seen-file}"; shift; [ $# -gt 0 ] || { echo "usage: $0 [--seed] <seen-file> <glob>…" >&2; exit 2; }
touch "$SEEN"
IDLE_TOOL="$(cd "$(dirname "$0")" && pwd)/seat_idle.sh"
pane_state() { bash "$IDLE_TOOL" "$1" 2>/dev/null | awk '{print $1}'; }
PANE_PREV=""
for p in ${WATCH_PANES:-}; do PANE_PREV="$PANE_PREV $p=$(pane_state "$p")"; done
for i in $(seq 1 "${WATCH_LOOPS:-110}"); do
  if [ -n "${WATCH_PANES:-}" ] && [ "$SEED" = 0 ]; then
    for p in $WATCH_PANES; do
      prev=$(printf '%s\n' $PANE_PREV | awk -F= -v k="$p" '$1==k{print $2}'); now=$(pane_state "$p")
      if [ "$prev" = "BUSY" ] && [ -n "$now" ] && [ "$now" != "BUSY" ]; then echo "WAKE: pane $p went $now (was BUSY)"; exit 0; fi
      PANE_PREV=$(printf '%s\n' $PANE_PREV | awk -F= -v k="$p" -v v="$now" '$1==k{$0=k"="v}1' | tr '\n' ' ')
    done
  fi
  for g in "$@"; do
    # IFS= : glob-expand WITHOUT word-splitting — every path here contains spaces ("1FILES TO SYNC"); an unset IFS
    # split them and the watcher grepped the pieces and never fired (Friday 2026-09-25).
    IFS= ; for f in $g; do unset IFS
      [ -f "$f" ] || continue   # 2026-10-05: an unmatched glob or a not-yet-written STATUS is skipped, not grep'd (it errored 100+ lines per loop)
      # A seat's DRAFT carries a placeholder line ("READY FOR REVIEW `<when-filled>`", B05 2026-09-25): lines holding a
      # `<…>` placeholder are not a READY, or the watcher fires early and then misses the real one (same count).
      rl=$(/usr/bin/grep -n -i -E 'READY FOR (REVIEW|RE-GATE|GATE)' "$f" | /usr/bin/grep -v -i -E '\bnot ready for' | /usr/bin/grep -v -E '<[a-z_-]+>|\b[A-Z]{3,}_[A-Z_]{3,}\b' | /usr/bin/grep -v -i -E '(\bat|until|end at|ends at|to|before)[ *`]+READY FOR (REVIEW|RE-GATE|GATE)')
      n=$(printf '%s' "$rl" | /usr/bin/grep -c .); ln=$(printf '%s\n' "$rl" | tail -1 | cut -d: -f1)   # a line that PROMISES a future READY ("full table at READY FOR REVIEW", Composer B09 2026-09-25) is not one   # also READY_TIME-style tokens (Composer B06, 2026-09-25)   # "NOT READY FOR REVIEW" is not one (2026-10-03)
      # A SKELETON STATUS (READY line written first, body still template tokens: @@BODY@@, __VERDICT__,
      # CI_RESULT_PLACEHOLDER, CI-RUN2-LINE) is not a READY yet: count none until every token is gone, so the
      # filled file is the one that fires (seen 4x on 2026-10-04: B57, B59, B61, B62). STOP lines still fire.
      # NOT bare PLACEHOLDER: finished Composer STATUS files say it in prose (the question texts ARE placeholders, E-01),
      # and KNOWN_PLACEHOLDER_ENTRIES is a real identifier (HPSM-POC B111): only *_PLACEHOLDER as a whole token holds.
      s=$(/usr/bin/grep -c -E '@@[A-Za-z0-9_]+@@|__[A-Z][A-Z0-9_]*__|(^|[^A-Za-z0-9_])[A-Z0-9]+(_[A-Z0-9]+)*_PLACEHOLDER([^A-Za-z0-9_]|$)|(^|[^A-Za-z0-9-])[A-Z0-9]+(-[A-Z0-9]+)+-(LINE|ROW|FILE)([^A-Za-z0-9-]|$)' "$f")
      [ "$s" -gt 0 ] && n=0
      m=$(/usr/bin/grep -c -E '^(\*\*State:\*\* *)?(BLOCKED|STOP)|STOPPED|NEEDS FRIDAY' "$f")
      if [ "$n" -gt 0 ] || [ "$m" -gt 0 ]; then
        for key in "$f READY#$n@L${ln:-0}" "$f STOP#$m"; do
          case "$key" in *"#0"|*"#0@L"*) continue;; esac
          if ! /usr/bin/grep -qxF "$key" "$SEEN"; then echo "$key" >> "$SEEN"; [ "$SEED" = 1 ] && continue; echo "WAKE: $f ($key)"; exit 0; fi
        done
      fi
    done
  done
  [ "$SEED" = 1 ] && { echo "seeded: $(wc -l < "$SEEN" | tr -d ' ') key(s) in $SEEN"; exit 0; }
  [ "$i" -lt "${WATCH_LOOPS:-110}" ] && sleep "${WATCH_SLEEP:-30}"
done
echo "WAKE: watcher leg expired (55 min), no new READY — re-arm"
