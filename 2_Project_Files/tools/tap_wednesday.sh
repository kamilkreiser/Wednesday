#!/bin/bash
# tap_wednesday.sh — THE shared tap-with-guard helper (Kam, 2026-08-17).
#
# Delivers a one-line message into the fleet session's wednesday pane via
# tmux send-keys, honouring the Kam-typing guard. This starts the WED-112
# consolidation of the four hand-rolled guard copies (wake_wednesday.sh,
# arm_wake_watch.sh runner, shift_change.sh, watcher) — new callers use THIS;
# existing copies migrate ticket-by-ticket, not in this change.
#
# Proven patterns copied, not reinvented:
#   - pane lookup: exact-match session target (=fleet) + list-panes -s +
#     @cockpit_name (wake_wednesday.sh findings 9+10)
#   - guard: capture prompt line, strip SGR-2 ghost spans + colour + NBSP;
#     real text after ❯ = Kam typing → do NOT tap (arm_wake_watch.sh,
#     ledger w=3 2026-08-12: a blind tap SUBMITS his half-typed text)
#   - no prompt line visible at all → do NOT type blind (wake_wednesday.sh
#     finding 5: modal dialog / scrolled prompt = keystrokes land unknowably)
#
# Policy for THIS helper: occupied → retry once after 20s → LOG-ONLY.
# Never blind-fire, never destroy input. Callers that need the watcher's
# 10-minute patience keep their own loop until WED-112 parameterises it.
#
# Usage: tap_wednesday.sh "message text"
# Exit:  0 tapped · 3 log-only (guard held / no prompt) · 1 error
# Log:   2_Project_Files/fleet/cockpit/logs/tap_wednesday.log
#
# Test hook (offline guard test, no tmux, no tap):
#   TAP_GUARD_TEST=1 tap_wednesday.sh < capture-fixture
#   prints occupied|empty|noprompt for the pane capture on stdin — this runs
#   the EXACT classify function the live path uses.

set -u

# ── guard classification (single source of truth for this helper) ──
# stdin: a raw `tmux capture-pane -p -e` dump. stdout: occupied|empty|noprompt.
classify_capture() {
  local line
  line=$(grep -a "$(printf '\342\235\257')" | tail -1)
  if [ -z "$line" ]; then printf 'noprompt'; return; fi
  local txt
  txt=$(printf '%s\n' "$line" | \
    LC_ALL=C perl -pe 's/\x1b\[2m.*?(?=\x1b|$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//' 2>/dev/null | \
    tr -d '[:space:]')
  if [ -n "$txt" ]; then printf 'occupied'; else printf 'empty'; fi
}

if [ "${TAP_GUARD_TEST:-0}" = "1" ]; then
  classify_capture
  echo
  exit 0
fi

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_DIR/2_Project_Files/fleet/cockpit/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/tap_wednesday.log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "usage: tap_wednesday.sh \"message text\"" >&2
  exit 1
fi

# Spawners (dashboard server, launchd) may hand us a stripped PATH.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
FLEET="fleet"

if ! "$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null; then
  log "ERROR: no '$FLEET' tmux session — tap undeliverable: $MSG"
  echo "tap_wednesday: no '$FLEET' session" >&2
  exit 1
fi

WROW=$("$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{@cockpit_name}|#{pane_id}' 2>/dev/null | \
  awk -F'|' '$1=="wednesday"' | head -1)
if [ -z "$WROW" ]; then
  log "ERROR: no wednesday pane in '$FLEET' — tap undeliverable: $MSG"
  echo "tap_wednesday: no wednesday pane in '$FLEET'" >&2
  exit 1
fi
PANE_ID="${WROW#*|}"

pane_state() { "$TMUX_BIN" capture-pane -t "$PANE_ID" -p -e 2>/dev/null | classify_capture; }

STATE=$(pane_state)
if [ "$STATE" = "occupied" ]; then
  log "guard held: text at wednesday prompt in $PANE_ID (try 1/2) — retrying in 20s"
  sleep 20
  STATE=$(pane_state)
fi
case "$STATE" in
  noprompt)
    log "LOG-ONLY: no prompt line visible in $PANE_ID — not typing blind: $MSG"
    exit 3 ;;
  occupied)
    log "LOG-ONLY (Kam-typing guard, prompt still occupied after retry): $MSG"
    exit 3 ;;
esac

if "$TMUX_BIN" send-keys -t "$PANE_ID" -l "$MSG" && "$TMUX_BIN" send-keys -t "$PANE_ID" Enter; then
  log "tapped $PANE_ID: $MSG"
  exit 0
else
  log "ERROR: send-keys failed for $PANE_ID: $MSG"
  echo "tap_wednesday: send-keys failed for $PANE_ID" >&2
  exit 1
fi
