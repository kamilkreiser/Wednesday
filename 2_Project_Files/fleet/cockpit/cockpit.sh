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
CONF="$SCRIPT_DIR/cockpit.conf"
SESSION="fleet"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

die() { echo "cockpit: $*" >&2; exit 1; }
[ -x "$TMUX_BIN" ] || die "tmux not found (PORTABILITY: brew install tmux)"

pane_exists() { # by @cockpit_name
  "$TMUX_BIN" list-panes -t "$SESSION" -F '#{@cockpit_name}' 2>/dev/null | grep -qx "$1"
}

add_pane() { # name, cmd
  local name="$1" cmd="$2"
  if pane_exists "$name"; then echo "pane '$name' already present — skip"; return 0; fi
  local pane_id
  pane_id=$("$TMUX_BIN" split-window -t "$SESSION:0" -P -F '#{pane_id}' -d "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash")
  "$TMUX_BIN" set-option -p -t "$pane_id" @cockpit_name "$name"
  "$TMUX_BIN" set-option -t "$SESSION:0" main-pane-width "45%" 2>/dev/null; "$TMUX_BIN" select-layout -t "$SESSION:0" main-vertical >/dev/null
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
        if [ $first -eq 1 ]; then
          "$TMUX_BIN" new-session -d -s "$SESSION" -n main "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash"
          pid=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_id}' | head -1)
          "$TMUX_BIN" set-option -p -t "$pid" @cockpit_name "$name"
          first=0
        else
          add_pane "$name" "$cmd"
        fi
      done < "$CONF"
      "$TMUX_BIN" set-option -t "$SESSION:0" main-pane-width "45%" 2>/dev/null; "$TMUX_BIN" select-layout -t "$SESSION:0" main-vertical >/dev/null
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
    die "usage: cockpit.sh up|launch|resolve|add|status|say|down"
    ;;
esac
