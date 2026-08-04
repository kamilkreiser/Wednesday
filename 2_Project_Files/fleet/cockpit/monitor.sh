#!/bin/bash
# monitor.sh — cockpit watchdog (delegation v2, WED-50).
# Watches every pane of the "fleet" tmux session. Pure tmux CLI — portable,
# headless-capable (the 06:00 scheduler can run it). Alert classes:
#   DEATH  — a pane's process died (pane_dead / pane vanished)
#   STALL  — no output change for STALL_MIN minutes
#   INPUT  — pane appears to wait on human input (prompt patterns)
# Alerts append to state/alerts.log (one line each, deduped per condition
# episode) and red flags (DEATH) get a spoken tap via voice/speak.sh.
#
# Usage: monitor.sh [--interval SECS] [--stall-min MIN] [--once]
# Reads panes' @cockpit_name; content hashing via capture-pane (tail 40 lines).
# R0 note: captured content is used ONLY for change-hashing + pattern checks,
# never stored beyond the hash, never quoted into another client's context.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
STATE_DIR="$SCRIPT_DIR/state"; mkdir -p "$STATE_DIR"
ALERTS="$STATE_DIR/alerts.log"
SPEAK="$PROJECT_DIR/2_Project_Files/voice/speak.sh"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
SESSION="fleet"
INTERVAL=60; STALL_MIN=10; ONCE=0

while [ $# -gt 0 ]; do case "$1" in
  --interval) INTERVAL="$2"; shift 2;;
  --stall-min) STALL_MIN="$2"; shift 2;;
  --once) ONCE=1; shift;;
  *) echo "unknown arg $1" >&2; exit 1;;
esac; done

alert() { # class, name, detail  — dedupe: one alert per (class,name) episode
  local class="$1" name="$2" detail="$3"
  local flagfile="$STATE_DIR/.flag_${class}_${name//[^a-zA-Z0-9]/_}"
  [ -f "$flagfile" ] && return 0
  touch "$flagfile"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [$class] $name — $detail" >> "$ALERTS"
  if [ "$class" = "DEATH" ] && [ -x "$SPEAK" ]; then
    "$SPEAK" "Heads up — the $name session just died in the cockpit." || true
  fi
}
clear_flag() { rm -f "$STATE_DIR/.flag_${1}_${2//[^a-zA-Z0-9]/_}" 2>/dev/null; }

check() {
  "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || { echo "no fleet session"; return 1; }
  local now; now=$(date +%s)
  "$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}|#{pane_dead}' | \
  while IFS='|' read -r name id dead; do
    name="${name:-$id}"
    local content hash hashfile timefile prev prevtime
    content=$("$TMUX_BIN" capture-pane -p -t "$id" -S -40 2>/dev/null | tail -40)
    # DEATH: pane_dead (remain-on-exit) OR the cockpit exit marker (panes wrap
    # their command with an exit note + shell so they stay inspectable)
    if [ "$dead" = "1" ] || printf '%s' "$content" | grep -q '\[cockpit\] .* exited'; then
      alert DEATH "$name" "process exited"; continue
    fi
    clear_flag DEATH "$name"
    hash=$(printf '%s' "$content" | md5 -q)
    hashfile="$STATE_DIR/.hash_${name//[^a-zA-Z0-9]/_}"
    timefile="$STATE_DIR/.time_${name//[^a-zA-Z0-9]/_}"
    prev=$(cat "$hashfile" 2>/dev/null || echo "")
    if [ "$hash" != "$prev" ]; then
      echo "$hash" > "$hashfile"; echo "$now" > "$timefile"
      clear_flag STALL "$name"; clear_flag INPUT "$name"
    else
      prevtime=$(cat "$timefile" 2>/dev/null || echo "$now")
      local quiet=$(( (now - prevtime) / 60 ))
      # Wednesday's own pane: idle-at-prompt IS her normal state between
      # turns — INPUT/STALL are always false positives there (first fired
      # 2026-08-04 21:45, 2 min after she ended a turn). DEATH still applies.
      [ "$name" = "wednesday" ] && continue
      # INPUT: quiet AND showing an interactive prompt pattern
      if printf '%s' "$content" | grep -qE 'esc to interrupt|Do you want|y/n\)|❯|permission|(A|a)llow.*\?' && [ "$quiet" -ge 2 ]; then
        alert INPUT "$name" "waiting on input ~${quiet}m"
      elif [ "$quiet" -ge "$STALL_MIN" ]; then
        alert STALL "$name" "no output change for ${quiet}m"
      fi
    fi
  done
  return 0
}

if [ "$ONCE" = "1" ]; then check; exit $?; fi
echo "monitor: watching '$SESSION' every ${INTERVAL}s (stall ${STALL_MIN}m). Alerts: $ALERTS"
while true; do check || true; sleep "$INTERVAL"; done
