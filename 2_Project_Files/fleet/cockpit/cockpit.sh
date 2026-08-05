#!/bin/bash
# cockpit.sh — the fleet cockpit (delegation v2, WED-50).
# Creates (or attaches to) the tmux session "fleet": one window, one pane per
# active project session + Wednesday's own pane. Each pane runs that project's
# OWN launcher — per-client env isolation (R0) is untouched; tmux only hosts.
#
# View natively in iTerm2:  tmux -CC attach -t fleet   (panes render as
# native iTerm2 split panes — persistence underneath, macOS glass on top).
# Plain view anywhere:      tmux attach -t fleet
#
# Usage:
#   cockpit.sh up                 create session from cockpit.conf (idempotent)
#   cockpit.sh launch <Client/Project>   start a REGISTERED launcher pane by
#                                 name (launchers.conf) — the standard way to
#                                 start an agent; keeps monitor coverage full
#   cockpit.sh resolve <Client/Project>  print what launch would run (dry-run)
#   cockpit.sh add <name> <cmd>   add a pane running <cmd> (unregistered/raw)
#   cockpit.sh status             list panes: name, alive, last activity
#   cockpit.sh say <name> <text>  type a line into a pane's prompt (the live
#                                 "tap on the shoulder" — substantive
#                                 instructions still go by mail for the record)
#   cockpit.sh down               kill the whole fleet session (asks first via -f)
#
# cockpit.conf format (same dir):  <pane-name>|<command to run>
# Lines starting with # ignored. Wednesday's pane is defined there too.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# WEDNESDAY root — conf commands reference it as the literal token
# ${PROJECT_DIR} so the cockpit is volume-portable (PORTABILITY 3: the drive
# may mount under any name; hardcoded /Volumes/... paths broke on KK_DEV_Local
# 2026-08-05).
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CONF="$SCRIPT_DIR/cockpit.conf"
SESSION="fleet"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

die() { echo "cockpit: $*" >&2; exit 1; }
[ -x "$TMUX_BIN" ] || die "tmux not found (PORTABILITY: brew install tmux)"

pane_exists() { # by @cockpit_name
  "$TMUX_BIN" list-panes -t "$SESSION" -F '#{@cockpit_name}' 2>/dev/null | grep -qx "$1"
}

apply_layout() {
  # THE default view (Kam, 2026-08-05): Wednesday = left column (main pane,
  # 45%), every agent + the monitor = stacked rows on the right. Enforced,
  # not assumed: main-vertical makes pane index 0 the left main pane, so if
  # the wednesday pane isn't index 0 (pane churn), swap it there first.
  local wed_id first_id
  wed_id=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_id}|#{@cockpit_name}' | awk -F'|' '$2=="wednesday"{print $1}' | head -1)
  first_id=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_index}|#{pane_id}' | awk -F'|' '$1==0{print $2}')
  if [ -n "$wed_id" ] && [ -n "$first_id" ] && [ "$wed_id" != "$first_id" ]; then
    "$TMUX_BIN" swap-pane -d -s "$wed_id" -t "$first_id"
  fi
  "$TMUX_BIN" set-option -t "$SESSION:0" main-pane-width "45%" 2>/dev/null
  "$TMUX_BIN" select-layout -t "$SESSION:0" main-vertical >/dev/null
  # Liveness borders (Kam, 2026-08-05: silence must not look like death) —
  # each pane border carries its name + a clock that ticks every 5s, so a
  # frozen VIEW is instantly distinguishable from a quiet AGENT.
  "$TMUX_BIN" set-option -t "$SESSION:0" pane-border-status top 2>/dev/null
  "$TMUX_BIN" set-option -t "$SESSION:0" pane-border-format ' #{?#{@cockpit_name},#{@cockpit_name},-} · #{?#{pane_dead},DEAD,live} #(date +%H:%M:%S) ' 2>/dev/null
  "$TMUX_BIN" set-option -t "$SESSION" status-interval 5 2>/dev/null
}

add_pane() { # name, cmd
  local name="$1" cmd="$2"
  if pane_exists "$name"; then echo "pane '$name' already present — skip"; return 0; fi
  local pane_id
  pane_id=$("$TMUX_BIN" split-window -t "$SESSION:0" -P -F '#{pane_id}' -d "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash")
  "$TMUX_BIN" set-option -p -t "$pane_id" @cockpit_name "$name"
  apply_layout
  echo "pane '$name' added ($pane_id)"
}

case "${1:-}" in
  up)
    if "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null; then
      echo "fleet session already running"
    else
      [ -f "$CONF" ] || die "no cockpit.conf at $CONF"
      # First entry becomes pane 0
      first=1
      while IFS='|' read -r name cmd; do
        case "$name" in ''|\#*) continue;; esac
        cmd="${cmd//'${PROJECT_DIR}'/$PROJECT_DIR}"
        if [ $first -eq 1 ]; then
          "$TMUX_BIN" new-session -d -s "$SESSION" -n main "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash"
          pid=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_id}' | head -1)
          "$TMUX_BIN" set-option -p -t "$pid" @cockpit_name "$name"
          first=0
        else
          add_pane "$name" "$cmd"
        fi
      done < "$CONF"
      apply_layout
      echo "fleet session created. Attach: tmux -CC attach -t fleet (iTerm2) or tmux attach -t fleet"
    fi
    ;;
  add)
    [ $# -eq 3 ] || die "usage: cockpit.sh add <name> <command>"
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session — run 'cockpit.sh up' first"
    add_pane "$2" "$3"
    ;;
  launch|resolve)
    # launch <Client/Project>: start a registered project's launcher in a new
    # pane, by name. resolve <Client/Project>: print what launch WOULD run.
    [ $# -eq 2 ] || die "usage: cockpit.sh $1 <Client/Project>  (see launchers.conf)"
    REG="$SCRIPT_DIR/launchers.conf"
    [ -f "$REG" ] || die "no launchers.conf at $REG"
    LPATH=$(awk -F'|' -v n="$2" '$1==n{print $2}' "$REG" | head -1)
    [ -n "$LPATH" ] || die "'$2' not in launchers.conf — register it (validated path) or use 'add'"
    [ -f "$LPATH" ] || die "registered launcher missing on disk: $LPATH (registry stale — fix launchers.conf)"
    if [ "$1" = resolve ]; then echo "would launch pane '$2': bash \"$LPATH\""; exit 0; fi
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session — run 'cockpit.sh up' first"
    add_pane "$2" "bash \"$LPATH\""
    ;;
  layout)
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session"
    apply_layout
    echo "layout applied: wednesday left column (45%), agents+monitor rows right"
    ;;
  status)
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || { echo "fleet session: DOWN"; exit 0; }
    echo "fleet session: UP"
    "$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}|#{pane_dead}|#{t:pane_activity}' | \
    while IFS='|' read -r name id dead act; do
      printf "  %-28s %-6s %s  last-activity: %s\n" "${name:-unnamed}" "$id" "$([ "$dead" = 1 ] && echo DEAD || echo alive)" "$act"
    done
    ;;
  say)
    [ $# -eq 3 ] || die "usage: cockpit.sh say <pane-name> <text>"
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session"
    PANE=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}' | awk -F'|' -v n="$2" '$1==n{print $2}')
    [ -n "$PANE" ] || die "no pane named '$2'"
    "$TMUX_BIN" send-keys -t "$PANE" -l "$3"
    "$TMUX_BIN" send-keys -t "$PANE" Enter
    echo "sent to '$2'"
    ;;
  down)
    "$TMUX_BIN" kill-session -t "$SESSION" 2>/dev/null && echo "fleet session killed" || echo "no fleet session"
    ;;
  *)
    die "usage: cockpit.sh up|launch|resolve|add|layout|status|say|down"
    ;;
esac
