#!/bin/bash
# nightly.sh - the launchd entry point of the NIGHTLY STALE-TICKET SCREEN (Kam 2026-11-12 11:36, routine (b)).
# Fires once at 01:15 (com.wednesday.stalescreen); window 01:00-05:00; bounded N tickets per night (STALE_N, default 60);
# PROPOSALS ONLY: screen.py writes nothing to Linear or any checkout. A Claude board seat confirms before any board change.
#
# Refuses CLEANLY (exit 0, one line in the log saying why) when: outside the 01:00-05:00 window; another copy is running;
# the Spark tunnel is down; a Spark round / queue drainer holds the box; vLLM is already serving a request.
# The refusal logic lives in screen.py (box_state), so the job and the tests share one gate. --wait 0: a nightly never queues
# behind a gate or the digest harness; it skips the night and says so (the next night picks the same tickets up first).
# Wednesday seat only (Secuura content on Wednesday's Spark). Logs: ~/Library/Logs/<seat>_stalescreen.{out,err}.
# Env seams: STALE_N, STALE_FORCE=1 (ignore the window: for a hand run), STALE_OUT (output dir), STALE_HOUR / STALE_STATE (tests).
set -u
PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
SELF="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
N="${STALE_N:-60}"
H="${STALE_HOUR:-$(date +%H)}"; H=$((10#$H))
echo "stalescreen: fired $(date '+%F %T') (limit $N)"
if [ "${STALE_FORCE:-0}" != "1" ] && { [ "$H" -lt 1 ] || [ "$H" -ge 5 ]; }; then
  echo "stalescreen: REFUSED - outside the 01:00-05:00 window (hour $H); nothing run, exit 0"; exit 0
fi
STATE="${STALE_STATE:-$SELF/state}"
LOCKD="$STATE/nightly.lock"; mkdir -p "$STATE"
if ! mkdir "$LOCKD" 2>/dev/null; then
  op="$(cat "$LOCKD/pid" 2>/dev/null)"
  if [ -n "$op" ] && kill -0 "$op" 2>/dev/null; then echo "stalescreen: REFUSED - another stalescreen run is live (pid $op); exit 0"; exit 0; fi
  echo "stalescreen: stale nightly.lock (holder ${op:-none} not alive) - moved aside"; mv "$LOCKD" "$STATE/nightly.lock.stale.$(date +%s)" && mkdir "$LOCKD" || { echo "stalescreen: REFUSED - could not take nightly.lock"; exit 0; }
fi
echo $$ > "$LOCKD/pid"
trap 'rm -f "$LOCKD/pid"; rmdir "$LOCKD" 2>/dev/null' EXIT
OUT="${STALE_OUT:-$SELF/runs/$(date +%Y-%m-%d)}"
[ -e "$OUT" ] && OUT="${OUT}_$(date +%H%M)"
PYBIN="$(command -v python3)" || { echo "stalescreen: HARNESS - no python3 on PATH; exit 0"; exit 0; }
"$PYBIN" -I "$SELF/screen.py" --limit "$N" --out "$OUT" --update-state --state-file "$STATE/screened.tsv" --deadline 05:00
rc=$?
echo "stalescreen: finished $(date '+%F %T') rc=$rc out=$OUT"
[ -f "$OUT/report.md" ] && sed -n 3p "$OUT/report.md" | cut -c1-400
date '+%F %T' > "$STATE/last_run_at"; echo "rc=$rc" > "$STATE/last_run_rc"
exit 0
