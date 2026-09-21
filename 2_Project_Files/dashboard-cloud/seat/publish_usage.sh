#!/bin/bash
# publish_usage.sh — the loop that keeps THIS SEAT's weekly usage gauge on the live board current (2026-09-22).
#
# Kam, live board 08:57:36: "with the local version, I was able to see the weekly usage count on both Wednesday and
# Tuesday. Is this possible for the live version?" — yes: the seat's statusline already writes usage_<seat>.json on its
# own machine; this loop hands that reading to seat/post_usage.py every INTERVAL seconds, which POSTs it to the live
# board as the seat (certificate token; the server attributes the row by the token, never the body).
#
# THE SEAT IS RESOLVED, NEVER GUESSED: fleet/cockpit/seat_resolve.sh (the ONE resolver — $WED_AGENT, else the tree's
# folder name: TUESDAY -> tuesday, else wednesday). --seat overrides for arms. A seat name outside {wednesday,tuesday}
# refuses (rc 2). Same shape as fleet/cockpit/live_chat_poll.sh: a detached loop from THIS script file, a log, a health
# file doctor.sh reads (OK / FAILING after 3 consecutive failed publishes), --once / --dry-run seams for arms.
#
# A stale or missing reading publishes NOTHING (post_usage.py rc 3) and the tick is logged as such — that is the seat
# being idle, not a failure; the live row keeps its last reading and the page shows "no reading" past 30 min.
#
# Usage: publish_usage.sh [--seat wednesday] [--interval 120] [--once] [--dry-run] [--arm] [--status]
#   --arm     spawn the loop detached (idempotent: refuses if one is already running for this seat), print its pid
#   --status  print whether a loop runs for this seat + the health line; rc 0 running / 1 not
#   USAGE_PUB_HEALTH / USAGE_PUB_LOG override the health + log files (arms use scratch files).
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$HERE/../../.." && pwd)"
RESOLVER="$ROOT/2_Project_Files/fleet/cockpit/seat_resolve.sh"
if [ -f "$RESOLVER" ]; then . "$RESOLVER"; seat_resolve "$ROOT"; else SEAT="${WED_AGENT:-}"; fi
INTERVAL=120; ONCE=0; DRY=0; ARM=0; STATUS=0
while [ $# -gt 0 ]; do case "$1" in
  --seat) SEAT="${2:-}"; shift ;; --interval) INTERVAL="${2:-120}"; shift ;; --once) ONCE=1 ;; --dry-run) DRY=1 ;; --arm) ARM=1 ;; --status) STATUS=1 ;;
  *) echo "publish_usage: unknown arg $1" >&2; exit 2 ;; esac; shift; done
case "${SEAT:-}" in wednesday|tuesday) ;; *) echo "publish_usage: seat '${SEAT:-unset}' is neither wednesday nor tuesday — REFUSING (a guessed seat would publish under the wrong name; export WED_AGENT or pass --seat)" >&2; exit 2 ;; esac
PY="$ROOT/2_Project_Files/dashboard-cloud/.venv/bin/python"; POST="$HERE/post_usage.py"
CERT_DIR="$ROOT/4_Credentials/dashboard-cloud"
STATE_DIR="$ROOT/2_Project_Files/fleet/cockpit/state"; LOG_DIR="$ROOT/2_Project_Files/fleet/cockpit/logs"
HEALTH="${USAGE_PUB_HEALTH:-$STATE_DIR/usage_publish.health}"; LOG="${USAGE_PUB_LOG:-$LOG_DIR/usage_publish.log}"
mkdir -p "$(dirname "$HEALTH")" "$(dirname "$LOG")"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; [ "$DRY" = 1 ] && echo "$*"; }
PATTERN="seat/publish_usage.sh"
running_pids() { pgrep -f "$PATTERN" 2>/dev/null | while read -r p; do [ "$p" = "$$" ] && continue; ps -o command= -p "$p" 2>/dev/null | /usr/bin/grep -q -- "--seat $SEAT" && echo "$p"; done; }

if [ "$STATUS" = 1 ]; then
  pids="$(running_pids | tr '\n' ' ')"
  if [ -n "$pids" ]; then echo "publish_usage: RUNNING seat=$SEAT pid(s) $pids"; echo "health: $(cat "$HEALTH" 2>/dev/null || echo '<none>')"; exit 0
  else echo "publish_usage: NOT RUNNING seat=$SEAT"; echo "health: $(cat "$HEALTH" 2>/dev/null || echo '<none>')"; exit 1; fi
fi
[ -x "$PY" ] || { echo "publish_usage: no venv python at $PY (PORTABILITY.md)" >&2; exit 2; }
[ -f "$CERT_DIR/$SEAT-seat.pem" ] || { echo "publish_usage: no certificate for seat $SEAT at $CERT_DIR (PORTABILITY.md)" >&2; exit 2; }

if [ "$ARM" = 1 ]; then
  pids="$(running_pids | tr '\n' ' ')"
  if [ -n "$pids" ]; then echo "publish_usage: already armed for seat=$SEAT (pid(s) $pids) — nothing spawned"; exit 0; fi
  nohup bash "$HERE/publish_usage.sh" --seat "$SEAT" --interval "$INTERVAL" >> "$LOG" 2>&1 &
  pid=$!; sleep 1
  if kill -0 "$pid" 2>/dev/null; then echo "publish_usage: armed seat=$SEAT pid $pid interval ${INTERVAL}s log $LOG"; exit 0
  else echo "publish_usage: ARM FAILED — see $LOG" >&2; tail -3 "$LOG" >&2; exit 1; fi
fi

FAILS="$(cat "$HEALTH.count" 2>/dev/null || echo 0)"; case "$FAILS" in ''|*[!0-9]*) FAILS=0;; esac
tick() {
  local out rc last
  if [ "$DRY" = 1 ]; then out="$("$PY" "$POST" --seat "$SEAT" --cert-dir "$CERT_DIR" --dry-run 2>&1)"; rc=$?
  else out="$("$PY" "$POST" --seat "$SEAT" --cert-dir "$CERT_DIR" 2>&1)"; rc=$?; fi
  last="$(printf '%s\n' "$out" | /usr/bin/grep -v '^rc=' | tail -1 | cut -c1-200)"
  case "$rc" in
    0) if [ "$DRY" = 1 ]; then log "dry-run: $last"; return 0; fi     # a dry run never touches the health file
       if [ "$FAILS" -gt 0 ]; then log "publish recovered after $FAILS failure(s)"; fi
       FAILS=0; printf '0\n' > "$HEALTH.count"; printf 'OK %s seat=%s %s\n' "$(date '+%F %T')" "$SEAT" "$last" > "$HEALTH"; log "ok: $last" ;;
    3) log "idle: $last" ;;   # nothing to publish (stale/missing reading) — not a failure; the health line is left as it was
    *) FAILS=$((FAILS+1)); printf '%s\n' "$FAILS" > "$HEALTH.count"; log "FAILED rc=$rc (consecutive $FAILS): $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-240)"
       [ "$FAILS" -ge 3 ] && printf 'FAILING %s seat=%s consecutive_failures=%s rc=%s\n' "$(date '+%F %T')" "$SEAT" "$FAILS" "$rc" > "$HEALTH" ;;
  esac
  return $rc
}
if [ "$ONCE" = 1 ]; then tick; exit $?; fi
log "publisher started seat=$SEAT interval=${INTERVAL}s health=$HEALTH"
while :; do tick; sleep "$INTERVAL"; done
