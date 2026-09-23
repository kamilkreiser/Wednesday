#!/bin/bash
# monitor.sh — cockpit watchdog (delegation v2, WED-50).
# Watches every pane of the "fleet" tmux session. Pure tmux CLI — portable,
# headless-capable (the 06:00 scheduler can run it). Alert classes:
#   DEATH  — a pane's process died (pane_dead / pane vanished)
#   STALL  — no output change for STALL_MIN minutes
#   INPUT  — pane appears to wait on human input (prompt patterns)
# Alerts append to state/alerts.log (one line each, deduped per condition
# episode) and red flags (DEATH) get a spoken tap via voice/speak.sh AND a
# WAKE line typed into the COORDINATOR's pane (2026-09-14 — the L3b gate died
# 50 s after launch, this monitor logged [DEATH] within the minute, speak.sh
# has been silent by Kam's 2026-09-08 rule, and nobody read the log for 45 min:
# a refusal nobody reads is indistinguishable from working. The pane tap is the
# same mechanism the wake runner uses, resolved through seat_resolve.sh, held
# (log-only) if text sits at the coordinator's prompt.)
# Red-proof arm: `monitor.sh --test-death <name>` fires ONE synthetic DEATH alert
# (log + tap) and exits — run it after any edit to prove the tap path works.
#
# Usage: monitor.sh [--interval SECS] [--stall-min MIN] [--once] [--test-death NAME]
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
INTERVAL=60; STALL_MIN=10; ONCE=0; TEST_DEATH=""

while [ $# -gt 0 ]; do case "$1" in
  --interval) INTERVAL="$2"; shift 2;;
  --stall-min) STALL_MIN="$2"; shift 2;;
  --once) ONCE=1; shift;;
  --test-death) TEST_DEATH="$2"; shift 2;;
  *) echo "unknown arg $1" >&2; exit 1;;
esac; done

alert() { # class, name, detail  — dedupe: one alert per (class,name) episode
  local class="$1" name="$2" detail="$3"
  local flagfile="$STATE_DIR/.flag_${class}_${name//[^a-zA-Z0-9]/_}"
  [ -f "$flagfile" ] && return 0
  touch "$flagfile"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [$class] $name — $detail" >> "$ALERTS"
  if [ "$class" = "DEATH" ]; then
    [ -x "$SPEAK" ] && { "$SPEAK" "Heads up — the $name session just died in the cockpit." || true; }
    wake_coordinator "$(date '+%H:%M') [fleet-monitor] WAKE: pane '$name' DEAD — $detail. A dead fleet pane is not the context banner: read it (tmux capture-pane), relaunch or close it, and record it."
  fi
}
# wake_coordinator <msg> — type one WAKE line into the coordinator's pane, the way the
# wake runner does (send-keys -l + Enter), unless text already sits at its prompt
# (then log-only; the runner's held-tap rule). Never taps a non-coordinator pane.
wake_coordinator() {
  local msg="$1" wpane
  if [ -r "$SCRIPT_DIR/seat_resolve.sh" ]; then
    # shellcheck disable=SC1090
    . "$SCRIPT_DIR/seat_resolve.sh" 2>/dev/null && seat_resolve "$PROJECT_DIR" 2>/dev/null || true
    wpane=$(coord_pane_id "$SESSION" 2>/dev/null || true)
  fi
  if [ -z "${wpane:-}" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') [monitor] no coordinator pane resolved — WAKE logged only: $msg" >> "$ALERTS"; return 0
  fi
  # Held while text sits at the coordinator's prompt (a running turn echoes its command
  # there): retry every 30 s for up to 10 minutes IN THE BACKGROUND so the monitor loop
  # keeps checking the other panes; after that, log-only — the wake runner's own rule.
  (
    tries=0
    while :; do
      ptxt=$("$TMUX_BIN" capture-pane -p -t "$wpane" 2>/dev/null | grep -E '^❯ ' | tail -1 | sed -E 's/^❯ *//')
      [ -z "$ptxt" ] && break
      tries=$((tries + 1))
      if [ "$tries" -ge 20 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [monitor] coordinator prompt occupied for 10 min — WAKE logged only: $msg" >> "$ALERTS"; exit 0
      fi
      sleep 30
    done
    if "$TMUX_BIN" send-keys -t "$wpane" -l "$msg" && "$TMUX_BIN" send-keys -t "$wpane" Enter; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') [monitor] tapped coordinator pane $wpane (after $tries held tries): $msg" >> "$ALERTS"
    else
      echo "$(date '+%Y-%m-%d %H:%M:%S') [monitor] FAILED to tap coordinator pane $wpane" >> "$ALERTS"
    fi
  ) &
}
clear_flag() { rm -f "$STATE_DIR/.flag_${1}_${2//[^a-zA-Z0-9]/_}" 2>/dev/null; }

check() {
  "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || { echo "no fleet session"; return 1; }
  local now; now=$(date +%s)
  "$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}|#{pane_dead}|#{pane_title}|#{host}' | \
  while IFS='|' read -r name id dead title host; do
    name="${name:-$id}"
    local content hash hashfile timefile prev prevtime
    content=$("$TMUX_BIN" capture-pane -p -t "$id" -S -40 2>/dev/null | tail -40)
    # DEATH: pane_dead (remain-on-exit) OR a Claude seat pane whose TITLE has reverted to
    # the bare hostname — Claude Code sets "✳ <title>" while it runs; when it exits, the
    # wrapper's bash takes over and the title falls back to #{host}. A fact about the pane's
    # STATE. Until 2026-09-14 this matched the wrapper's "[cockpit] … exited" TEXT and fired
    # on the coordinator's own pane the moment that string was typed there in a respawn
    # command (the detector-keyed-on-the-banner's-words lesson, same day). fleet-monitor is
    # not a Claude seat — its title IS the hostname while it lives — so pane_dead only.
    # 17:52 the same day, THREE false DEATHs: a pane launched seconds earlier carries the
    # hostname title until Claude sets its own (~10-30 s). A dead pane stays dead; a booting
    # one does not — so the title condition must hold on TWO consecutive cycles (60 s apart)
    # before it is a DEATH. pane_dead=1 stays immediate. The marker is a state file, cleared
    # (moved aside, never rm'd from a Bash tool call — the no-rm hook) when the title is live.
    local revfile="$STATE_DIR/.rev_${name//[^a-zA-Z0-9]/_}"
    if [ "$dead" = "1" ]; then
      alert DEATH "$name" "process exited (pane_dead=1)"; continue
    elif [ "$name" != "fleet-monitor" ] && [ -n "$host" ] && [ "$title" = "$host" ]; then
      if [ -f "$revfile" ]; then
        alert DEATH "$name" "process exited (title reverted to the hostname on two consecutive checks)"; continue
      fi
      touch "$revfile"; continue
    else
      [ -f "$revfile" ] && mv "$revfile" "$STATE_DIR/.rev_cleared" 2>&1
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
      # Infrastructure panes: idle-at-prompt IS wednesday's normal state
      # between turns, and fleet-monitor prints once then only writes the
      # log — INPUT/STALL are always false positives for both (fired
      # 2026-08-04 21:45 + 21:52). DEATH still applies to both.
      case "$name" in wednesday|fleet-monitor) continue;; esac
      # Claude Code panes idling at prompt while a BACKGROUND SHELL works
      # (status bar shows "N shell(s)") are healthy holding patterns, not
      # input-waits — e.g. a CI watcher (false-fired 2026-08-05 07:27).
      # STALL still applies: a dead bg shell eventually stops changing output.
      if printf '%s' "$content" | grep -qE '[0-9]+ shells? (still running)?|· [0-9]+ shell'; then
        clear_flag INPUT "$name"
      # INPUT: quiet AND showing an interactive prompt pattern
      elif printf '%s' "$content" | grep -qE 'esc to interrupt|Do you want|y/n\)|❯|permission|(A|a)llow.*\?' && [ "$quiet" -ge 2 ]; then
        alert INPUT "$name" "waiting on input ~${quiet}m"
      elif [ "$quiet" -ge "$STALL_MIN" ]; then
        alert STALL "$name" "no output change for ${quiet}m"
      fi
    fi
  done
  return 0
}

if [ -n "$TEST_DEATH" ]; then
  rm -f "$STATE_DIR/.flag_DEATH_${TEST_DEATH//[^a-zA-Z0-9]/_}"
  alert DEATH "$TEST_DEATH" "SYNTHETIC test-death (monitor.sh --test-death) — not a real pane"
  rm -f "$STATE_DIR/.flag_DEATH_${TEST_DEATH//[^a-zA-Z0-9]/_}"
  echo "test-death alert fired for '$TEST_DEATH'; see $ALERTS"; exit 0
fi
if [ "$ONCE" = "1" ]; then check; exit $?; fi
echo "monitor: watching '$SESSION' every ${INTERVAL}s (stall ${STALL_MIN}m). Alerts: $ALERTS"
while true; do check || true; sleep "$INTERVAL"; done
