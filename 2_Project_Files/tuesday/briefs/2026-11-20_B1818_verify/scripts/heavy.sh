#!/bin/bash
# heavy.sh <command...> : the gate reviewer's copy of the project heavy-lock wrapper (shape of the builder's, read whole).
# Lock = mkdir (atomic) of the project lock. Waits on a held lock in 120 s reads up to 3600 s (exit 75).
# Load: needs load1 < LOAD_MAX (default 7: the commission's rule, three seats of another project build here) at two reads 4 s apart; 30 s steps, exit 76.
T='/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer/.tools'
LOCK="${HEAVY_LOCK:-$T/composer-heavy.lock}"; Q='/private/tmp/b1818-gate/quarantine'
WAIT_S="${WAIT_S:-120}"; LOCK_MAX_S="${LOCK_MAX_S:-3600}"; LOAD_MAX_S="${LOAD_MAX_S:-5400}"; LOAD_MAX="${LOAD_MAX:-7}"
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
lw=0; dw=0
while :; do
  if [ -e "$LOCK" ]; then
    echo "heavy: $(date +%T) lock HELD by: $(cat "$LOCK/holder" 2>/dev/null || echo '<no holder file>')"
    [ "$lw" -ge "$LOCK_MAX_S" ] && { echo "heavy: STOP lock held ${lw}s"; exit 75; }
    sleep "$WAIT_S"; lw=$((lw+WAIT_S)); continue
  fi
  a=$(load1); sleep 4; b=$(load1)
  if awk -v a="$a" -v b="$b" -v m="$LOAD_MAX" 'BEGIN{exit !(a<m && b<m)}'; then
    if mkdir "$LOCK" 2>/dev/null; then break; else continue; fi
  fi
  echo "heavy: $(date +%T) lock free, load1 $a / $b (>= $LOAD_MAX), waiting"
  [ "$dw" -ge "$LOAD_MAX_S" ] && { echo "heavy: STOP load stayed >= $LOAD_MAX for ${dw}s"; exit 76; }
  sleep 30; dw=$((dw+30))
done
echo "independent gate reviewer $(date '+%F %T %Z') pid $$ cmd: $*" > "$LOCK/holder"
echo "heavy: $(date +%T) TAKEN (load1 $a / $b; uptime: $(LC_ALL=C uptime))"
"$@"; rc=$?
mv "$LOCK" "$Q/$(basename "$LOCK").$(date +%Y%m%d-%H%M%S).$$" && echo "heavy: $(date +%T) RELEASED (moved to quarantine) rc=$rc"
exit $rc
