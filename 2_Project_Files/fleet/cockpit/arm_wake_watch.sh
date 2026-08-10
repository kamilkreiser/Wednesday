#!/bin/bash
# arm_wake_watch.sh — the ARMING half of wake_watch (built 2026-08-10).
#
# Why this exists (ledger w=5, learnings/2026-08-10_a-ritual-nothing-triggers-
# is-not-a-ritual + 2026-08-09_an-enforcement-you-must-arm-is-not-one):
# wake_watch.sh was hand-armed three times and dead within a day each time.
# A safeguard that runs beside the work needs something that arms it (this
# script, called by Launch_Wednesday.command on every boot) and something
# that checks it is armed (doctor.sh's existing hard-fail). Hand-arming is
# now only for recovery, never the plan.
#
# What it does:
#   - Idempotent: if a runner is already alive, exits 0 saying so. Safe to
#     call on every launch.
#   - Starts a detached runner loop that re-arms wake_watch.sh forever:
#       baseline = now (UTC, minute precision — matches wake_watch's compare)
#       stable_n = 3 when agent panes are live, 9999 (mail-only) when not —
#                  recomputed at every re-arm, so a wrapped-idle pane never
#                  false-fires all morning (2026-08-09 false positive).
#   - On a WAKE (mail or pane): delivers it through the PROVEN mechanism —
#     tmux send-keys into the wednesday pane, exactly like shift_change.sh.
#     No wednesday pane (launcher-only session, cockpit down): the WAKE line
#     is in the log and the runner re-arms; doctor/next boot reads the log.
#   - On the 4h no-fire timeout: re-arms silently with a fresh baseline.
#
# Usage: arm_wake_watch.sh            (arm if not armed)
#        arm_wake_watch.sh status     (report, exit 0 armed / 1 not)
#        arm_wake_watch.sh disarm     (stop runner + watcher)

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$HERE/state"
LOG_DIR="$HERE/logs"
PIDFILE="$STATE_DIR/wake_watch_runner.pid"
LOG="$LOG_DIR/wake_watch_runner.log"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
mkdir -p "$STATE_DIR" "$LOG_DIR"

runner_alive() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
}

case "${1:-arm}" in
  status)
    if runner_alive; then echo "armed (runner pid $(cat "$PIDFILE"))"; exit 0
    else echo "NOT armed"; exit 1; fi
    ;;
  disarm)
    if runner_alive; then kill "$(cat "$PIDFILE")" 2>/dev/null; fi
    pkill -f 'wake_watch\.sh' 2>/dev/null
    rm -f "$PIDFILE"
    echo "disarmed"
    exit 0
    ;;
  arm) ;;
  *) echo "usage: arm_wake_watch.sh [status|disarm]"; exit 2 ;;
esac

if runner_alive; then
  echo "already armed (runner pid $(cat "$PIDFILE"))"
  exit 0
fi
# A stray watcher without a runner (old hand-armed instance) would double-fire
# once a runner starts — fold it in rather than run two.
pkill -f 'wake_watch\.sh' 2>/dev/null && sleep 1

RUNNER='
  # Baseline discipline (fixed 2026-08-10 after a QUESTION mail fell into the
  # fire->re-arm gap, ledger w=2 on the 08-04 blanket-markseen root cause):
  # the baseline NEVER advances to "now" — it advances ONLY to the timestamp
  # of a mail/chat event that actually fired a wake (so I was provably tapped
  # about everything up to it). A refire on an already-read mail costs one
  # tap; a swallowed mail costs a 15-minute fallback. Always err toward refire.
  BASELINE=$(date -u +%Y-%m-%dT%H:%M)   # first arm only: session boot has read everything
  while true; do
    AGENTS=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}" 2>/dev/null | grep -vE "^(wednesday|fleet-monitor)$" | grep -c . || true)
    if [ "${AGENTS:-0}" -gt 0 ] 2>/dev/null; then N=3; else N=9999; fi
    echo "$(date "+%Y-%m-%d %H:%M:%S") armed: baseline=$BASELINE stable_n=$N agents=$AGENTS"
    OUT=$('"$HERE"'/wake_watch.sh "$BASELINE" "$N" 60 2>&1)
    echo "$(date "+%Y-%m-%d %H:%M:%S") $OUT"
    NEWTS=$(printf "%s" "$OUT" | sed -nE "s/.*(new mail at|message from Kam at) ([0-9T:-]+).*/\2/p" | tail -1)
    [ -n "$NEWTS" ] && BASELINE="$NEWTS"
    case "$OUT" in
      *"new mail"*|*"idle at prompt"*)
        MSG="[wake_watch] $OUT — check the fleet inbox / pane now."
        if '"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep -q "^wednesday|"; then
          WPANE=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep "^wednesday|" | head -1 | cut -d"|" -f2)
          '"$TMUX_BIN"' send-keys -t "$WPANE" -l "$MSG" && '"$TMUX_BIN"' send-keys -t "$WPANE" Enter \
            && echo "$(date "+%Y-%m-%d %H:%M:%S") tapped wednesday pane $WPANE" \
            || echo "$(date "+%Y-%m-%d %H:%M:%S") FAILED to tap wednesday pane"
        else
          echo "$(date "+%Y-%m-%d %H:%M:%S") no wednesday pane — WAKE logged only"
        fi
        sleep 120   # give the session time to read before re-arming
        ;;
    esac
  done
'
nohup bash -c "$RUNNER" >> "$LOG" 2>&1 &
echo "$!" > "$PIDFILE"
sleep 1
if runner_alive; then
  echo "armed (runner pid $(cat "$PIDFILE"), log $LOG)"
  exit 0
else
  echo "ARM FAILED — see $LOG"
  tail -5 "$LOG" 2>/dev/null
  exit 1
fi
