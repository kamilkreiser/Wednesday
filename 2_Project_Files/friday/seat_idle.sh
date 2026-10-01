#!/bin/bash
# seat_idle.sh — has a seat's TURN finished? Answer from the pane, before telling the seat
# that something it reported is missing.
#
# WHY (Friday ledger, the absence-stale rows, w=3 on 2026-10-01): three times Friday told a seat
# "your records are not on origin / step 5 is missing" while the seat was still mid-turn finishing
# exactly that, because Friday read idleness from the visible `❯` prompt box — which Claude Code
# draws even during a turn. The rule since 09-27: a seat is idle only when a turn-ENDED line
# ("✻ Worked for 3m 12s · done 8:17 pm") is the newest turn-status line and nothing in-flight
# (spinner, token counter, "esc to interrupt", "Waiting for N agents") sits after it.
#
# It does NOT keep its own patterns: it reads WAIT_RE / ENDED_RE / SPIN_RE / STRONG_RE out of
# fleet/cockpit/wake_watch.sh at run time (the watcher's turn-status discriminators, arms in
# fleet/tests/wake_watch_falsewake_arms.sh), so the two can never disagree. If any of the four
# cannot be read it REFUSES (rc 5) rather than guessing.
#
# Usage:  seat_idle.sh <pane-id|cockpit-name>      e.g. seat_idle.sh %8   or   seat_idle.sh Datasec/MPSCalc-A
#         seat_idle.sh --file <capture.ansi|.txt>  (tests: a saved pane capture)
# Prints ONE line: IDLE / IDLE-HOLDING (turn ended, background shell/monitor alive) / BUSY / WAITING /
#         UNKNOWN (no turn-status line at all: not a Claude seat, or no turn yet — never read as idle).
# Exit:   0 IDLE or IDLE-HOLDING · 1 BUSY · 3 UNKNOWN · 4 WAITING on subagents · 2 usage/capture failed ·
#         5 the watcher's patterns could not be read.
# Override for tests only: SEAT_IDLE_WAKE_WATCH=<path to a wake_watch.sh>.

set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WW="${SEAT_IDLE_WAKE_WATCH:-$SELF_DIR/../fleet/cockpit/wake_watch.sh}"
TMUX_BIN="${TMUX_BIN:-tmux}"

pat() { # the single-quoted value of NAME='…' in wake_watch.sh
  grep -m1 -E "^[[:space:]]*$1='" "$WW" 2>/dev/null | sed -E "s/^[[:space:]]*$1='(.*)'[[:space:]]*$/\1/"
}
[ -r "$WW" ] || { echo "seat_idle: REFUSED (rc 5) — cannot read $WW" >&2; exit 5; }
WAIT_RE=$(pat WAIT_RE); ENDED_RE=$(pat ENDED_RE); SPIN_RE=$(pat SPIN_RE); STRONG_RE=$(pat STRONG_RE)
for v in WAIT_RE ENDED_RE SPIN_RE STRONG_RE; do
  [ -n "${!v}" ] || { echo "seat_idle: REFUSED (rc 5) — $v not found in $WW; refusing rather than guessing" >&2; exit 5; }
done

if [ "${1:-}" = "--file" ]; then
  [ $# -eq 2 ] && [ -r "$2" ] || { echo "usage: seat_idle.sh --file <capture>" >&2; exit 2; }
  RAW=$(cat "$2")
else
  [ $# -eq 1 ] || { echo "usage: seat_idle.sh <pane-id|cockpit-name> | --file <capture>" >&2; exit 2; }
  T="$1"
  case "$T" in
    %*) : ;;
    *) T=$("$TMUX_BIN" list-panes -a -F '#{pane_id}|#{@cockpit_name}' 2>&1 | awk -F'|' -v n="$1" '$2==n{print $1; exit}')
       [ -n "$T" ] || { echo "seat_idle: no pane named '$1' (tmux list-panes -a)" >&2; exit 2; } ;;
  esac
  RAW=$("$TMUX_BIN" capture-pane -t "$T" -p 2>&1) || { echo "seat_idle: capture-pane failed for $T: $RAW" >&2; exit 2; }
fi

# Same tail the watcher hashes: no blank lines, no statusline, no idle-hint line, last 20.
TAIL=$(printf '%s\n' "$RAW" | LC_ALL=C perl -pe 's/\x1b\[[0-9;]*m//g' | grep -v '^$' \
  | grep -v 'ctx:[0-9-]*%' | grep -v 'new task? /clear to save' | tail -20)
[ -n "$TAIL" ] || { echo "seat_idle: empty capture — cannot judge" >&2; exit 2; }

last() { printf '%s\n' "$TAIL" | LC_ALL=C grep -n $1 "$2" | tail -1 | cut -d: -f1; }
wl=$(last -aiE "$WAIT_RE"); dl=$(last -aE "$ENDED_RE"); sl=$(last -aE "$SPIN_RE")
wl=${wl:-0}; dl=${dl:-0}; sl=${sl:-0}
# Live in-flight markers BELOW the newest ended line mean a new turn is running.
strong_after=0
if [ "$dl" -gt 0 ]; then
  printf '%s\n' "$TAIL" | sed -n "$((dl+1)),\$p" | LC_ALL=C grep -qE "$STRONG_RE" && strong_after=1
else
  printf '%s\n' "$TAIL" | LC_ALL=C grep -qE "$STRONG_RE" && strong_after=1
fi

if [ "$wl" -gt "$dl" ] && [ "$wl" -gt "$sl" ]; then
  echo "WAITING — the seat's turn is parked on subagents (line: $(printf '%s\n' "$TAIL" | sed -n "${wl}p" | sed 's/^[[:space:]]*//'))"; exit 4
fi
if [ "$dl" -gt 0 ] && [ "$dl" -gt "$sl" ] && [ "$strong_after" = 0 ]; then
  endl=$(printf '%s\n' "$TAIL" | sed -n "${dl}p" | sed 's/^[[:space:]]*//')
  if printf '%s' "$TAIL" | grep -qE 'shell still running|monitor still running'; then
    echo "IDLE-HOLDING — turn ended, background work alive ($endl)"; exit 0
  fi
  echo "IDLE — turn ended ($endl)"; exit 0
fi
if [ "$dl" = 0 ] && [ "$sl" = 0 ] && [ "$wl" = 0 ] && [ "$strong_after" = 0 ]; then
  echo "UNKNOWN — no turn-status line in the last 20 lines (not a Claude seat, or no turn has run yet)"; exit 3
fi
echo "BUSY — a turn is in flight (no ended line after the last spinner/marker)"; exit 1
