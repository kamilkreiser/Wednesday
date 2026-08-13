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
#        arm_wake_watch.sh cycle      (re-arm NOW: kill the CHILD only, never the runner)
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
  cycle)
    # Force the runner to re-arm NOW, so stable_n/agents are recomputed after a
    # pane is added or closed — WITHOUT touching the runner itself.
    #
    # Why this is a subcommand and not a command I type (ledger w=3, 2026-08-13):
    # three times in one day I cycled by hand with a grep on 'wake_watch.sh' and
    # a positional head -1, and the RUNNER matched too — its bash -c body quotes
    # the child's path. Twice that killed the watcher I was trying to refresh.
    # The discriminator is not greppable by eye but it is exact: the runner's pid
    # is in PIDFILE; every other match is a child. Encoding it is the fix,
    # because the selector lesson had already been written and still did not
    # prevent the third occurrence.
    runner_alive || { echo "NOT armed — nothing to cycle (run 'arm' first)" >&2; exit 1; }
    RPID="$(cat "$PIDFILE")"
    [ -x "$HERE/wake_watch.sh" ] || { echo "cycle ABORTED — $HERE/wake_watch.sh not found or not executable" >&2; exit 2; }
    KILLED=0
    while IFS= read -r line; do
      cpid="${line%% *}"
      [ "$cpid" = "$RPID" ] && continue          # never the runner
      kill "$cpid" 2>/dev/null && KILLED=$((KILLED + 1))
    done <<EOF
$(ps -eo pid=,command= | awk -v s="$HERE/wake_watch.sh" '$2 == s || $3 == s {print $1" "$0}')
EOF
    if [ "$KILLED" -eq 0 ]; then
      echo "runner $RPID alive; no child to cycle (it will re-arm on its own timer)"
    else
      echo "cycled: killed $KILLED child process(es); runner $RPID untouched, re-arms within ~60s"
    fi
    exit 0
    ;;
  arm) ;;
  *) echo "usage: arm_wake_watch.sh [arm|status|cycle|disarm]"; exit 2 ;;
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
    # ctx wakes (working-rhythm §2, 2026-08-10) pass through EXACTLY like pane
    # fires: tap, no baseline movement (the sed above only matches mail/chat).
    case "$OUT" in
      *"new mail"*|*"idle at prompt"*) MSG="[wake_watch] $OUT — check the fleet inbox / pane now." ;;
      *"ctx at"*) MSG="[wake_watch] $OUT — apply rhythm §2 now; rotate at the task boundary via cockpit.sh rotate <Client/Project> (wednesday pane: own checkpoint ritual)." ;;
      *) MSG="" ;;
    esac
    if [ -n "$MSG" ]; then
        if '"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep -q "^wednesday|"; then
          WPANE=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep "^wednesday|" | head -1 | cut -d"|" -f2)
          # KAM-TYPING GUARD (2026-08-12): the tap presses Enter in the
          # wednesday pane — if Kam is mid-typing there, it SUBMITS his
          # half-written message (happened twice today, both truncated at the
          # wake text). Before tapping: read the prompt line, strip SGR-2
          # ghost spans + colour codes + NBSP; if any real text sits after
          # the prompt char, wait 30s and re-check, up to 20 tries (10 min).
          # Still occupied -> log-only wake; losing immediacy beats
          # destroying his input. (Ghost text does NOT block the tap - it is
          # not his.)
          TRIES=0
          while [ "$TRIES" -lt 20 ]; do
            PTXT=$('"$TMUX_BIN"' capture-pane -t "$WPANE" -p -e 2>/dev/null | grep -a "$(printf "\342\235\257")" | tail -1 | \
              LC_ALL=C perl -pe "s/\x1b\[2m.*?(?=\x1b|\$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//" 2>/dev/null | tr -d "[:space:]")
            [ -z "$PTXT" ] && break
            TRIES=$((TRIES + 1))
            echo "$(date "+%Y-%m-%d %H:%M:%S") tap held - text at wednesday prompt (try $TRIES/20)"
            sleep 30
          done
          if [ -n "$PTXT" ]; then
            echo "$(date "+%Y-%m-%d %H:%M:%S") WAKE LOG-ONLY (prompt still occupied after 10 min): $MSG"
          else
            '"$TMUX_BIN"' send-keys -t "$WPANE" -l "$MSG" && '"$TMUX_BIN"' send-keys -t "$WPANE" Enter \
              && echo "$(date "+%Y-%m-%d %H:%M:%S") tapped wednesday pane $WPANE" \
              || echo "$(date "+%Y-%m-%d %H:%M:%S") FAILED to tap wednesday pane"
          fi
        else
          echo "$(date "+%Y-%m-%d %H:%M:%S") no wednesday pane — WAKE logged only"
        fi
        sleep 120   # give the session time to read before re-arming
    fi
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
