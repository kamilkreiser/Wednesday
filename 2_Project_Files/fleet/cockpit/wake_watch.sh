#!/bin/bash
# wake_watch.sh — Wednesday's fleet wake-up tripwire (built 2026-08-05 after
# Kam caught an in-pane plan-confirmation sitting unseen ~10 min; rewritten
# same night for macOS bash 3.2 — no associative arrays).
#
# Runs as a BACKGROUND TASK from Wednesday's own session: polls every 60s and
# EXITS (task-notification wakes Wednesday) when either:
#   (a) MAIL: a new message lands in wednesday-agent@ (timestamp > baseline), or
#   (b) PANE: an agent pane (not wednesday/fleet-monitor) sits idle at a
#       prompt with unchanged content for STABLE_N consecutive samples.
# Pane state lives in files under a per-run temp dir (bash-3.2-safe).
# The background runner caps runs at 10 min, so this re-arms on that heartbeat.
#
# Usage: wake_watch.sh <baseline-iso-ts> [stable_n] [interval_s]
set -u
BASELINE="${1:?usage: wake_watch.sh <baseline-iso-ts> [stable_n] [interval_s]}"
STABLE_N="${2:-3}"
INTERVAL="${3:-60}"
ENVF="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/4_Credentials/.env"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
STATE_DIR="$(mktemp -d /tmp/wake_watch.XXXXXX)"
trap 'rm -rf "$STATE_DIR"' EXIT
end=$((SECONDS + 14400))
while [ $SECONDS -lt $end ]; do
  # (a) mail tripwire
  # Latest INBOUND message only — own outbound copies (from wednesday-agent@)
  # must never fire the tripwire (false wake 2026-08-05 21:4x).
  ts=$(set -a; . "$ENVF" 2>/dev/null; set +a; curl -s -m 10 \
    "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=10" \
    -H "Authorization: Bearer ${AGENTMAIL_API_KEY:-}" \
    | python3 -c "
import json,sys
ms=[m for m in json.load(sys.stdin).get('messages',[]) if 'wednesday-agent@' not in str(m.get('from',''))]
print(ms[0].get('timestamp','')[:16] if ms else '')" 2>/dev/null)
  if [ -n "$ts" ] && [[ "$ts" > "$BASELINE" ]]; then
    echo "WAKE: new mail at $ts (baseline $BASELINE)"; exit 0
  fi
  # (b) pane idle-at-prompt tripwire
  "$TMUX_BIN" list-panes -t fleet:0 -F '#{pane_id}|#{@cockpit_name}' 2>/dev/null | \
  while IFS='|' read -r pid name; do
    case "$name" in wednesday|fleet-monitor|'') continue;; esac
    key=$(printf '%s' "$pid" | tr -c 'A-Za-z0-9' '_')
    tail=$("$TMUX_BIN" capture-pane -t "$pid" -p 2>/dev/null | grep -v '^$' | tail -20)
    h=$(printf '%s' "$tail" | shasum | cut -c1-12)
    hf="$STATE_DIR/h_$key"; cf="$STATE_DIR/c_$key"
    prev=$(cat "$hf" 2>/dev/null || echo none)
    cnt=$(cat "$cf" 2>/dev/null || echo 0)
    # A pane idle at its prompt but with a RUNNING background shell (Claude
    # status line shows "N shell(s)") is working (e.g. watching CI), not
    # waiting on Wednesday — its QUESTION mail / next turn is the real signal.
    # (Refined 2026-08-05 after two identical fires on a CI-watching agent.)
    if printf '%s' "$tail" | grep -qE 'shell still running|· [0-9]+ shell'; then
      cnt=0
    elif printf '%s' "$tail" | grep -qE '^❯[[:space:]]*$|Pick or adjust'; then
      if [ "$prev" = "$h" ]; then cnt=$((cnt + 1)); else cnt=1; fi
    else
      cnt=0
    fi
    printf '%s' "$h" > "$hf"; printf '%s' "$cnt" > "$cf"
    if [ "$cnt" -ge "$STABLE_N" ]; then
      echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday" > "$STATE_DIR/fired"
    fi
  done
  if [ -f "$STATE_DIR/fired" ]; then cat "$STATE_DIR/fired"; exit 0; fi
  sleep "$INTERVAL"
done
echo "WAKE: 4h max runtime reached with no tripwire — re-arm from the session"
exit 0
