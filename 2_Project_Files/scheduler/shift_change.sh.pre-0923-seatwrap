#!/bin/bash
# WED-16 — 05:30 morning shift change. Fired by launchd (com.wednesday.shiftchange).
# Kam's directive 2026-08-06: before his ~06:00 start, every live agent session
# wraps up and finishes, so he launches FRESH sessions with Wednesday — the
# night crew hands over before the day crew clocks in.
#
# Deterministic (no LLM): taps each live cockpit pane's prompt with a wrap-up
# instruction (tmux send-keys — same mechanism as cockpit.sh say) and drops one
# for-the-record mail on the bus. Claude Code queues typed input while a tool
# is running, so tapping a busy pane is safe — the instruction lands when the
# current step finishes. The 06:00 wake session then VERIFIES wraps arrived.
#
# Guards: once per day · only fires in the 05:00–05:59 window (launchd
# coalesces missed jobs to next Mac wake — a coalesced fire after 06:00 could
# wrap sessions Kam is actively using; skip instead, the wake session reports
# any still-open panes).

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG_DIR="$SELF_DIR/logs"
STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/shift_change_$(date +%F).log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

TODAY="$(date +%F)"
HOUR="$((10#$(date +%H)))"
if [ -n "${WEDNESDAY_TEST_HOUR:-}" ]; then
  HOUR="$WEDNESDAY_TEST_HOUR"
  log "TEST: hour overridden to $HOUR (WEDNESDAY_TEST_HOUR)"
fi

if [ -f "$STATE_DIR/last_shift_change" ] && [ "$(cat "$STATE_DIR/last_shift_change")" = "$TODAY" ]; then
  log "skip: already ran today"
  exit 0
fi
if [ "$HOUR" -ne 5 ]; then
  log "skip: outside 05:00-05:59 window (coalesced fire — wake session will report open panes instead)"
  exit 0
fi

DRYRUN="${WEDNESDAY_DRYRUN:-0}"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
SESSION="fleet"

WRAP_AGENT="[Wednesday, scheduled 05:30 shift change — CHECKPOINT, per the 2026-08-28 overnight-is-working-time grant] If your queue is LIVE: CONTINUE working — checkpoint at your own rhythm boundary; do NOT wrap on this tap. If your queue is DRY: run your end-of-session ritual now (commit+push, history entry, wrap email to wednesday-agent@agentmail.to). Signature classes still pause for Kam. The 06:00 wake verifies state either way."
WRAP_WED="[Scheduled 05:30 shift change] Wrap the overnight session now: retro, handover email [Wednesday-overnight -> Wednesday-morning], commit+push. Do not start new work — the 06:00 wake begins fresh."

TAPPED=0
if [ -x "$TMUX_BIN" ] && "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null; then
  while IFS='|' read -r name id dead; do
    [ -z "${name:-}" ] && continue
    [ "$dead" = "1" ] && { log "pane $name: dead, skipped"; continue; }
    case "$name" in
      fleet-monitor) continue ;;
      wednesday) MSG="$WRAP_WED" ;;
      *) MSG="$WRAP_AGENT" ;;
    esac
    if [ "$DRYRUN" = "1" ]; then
      log "DRYRUN: would tap pane $name ($id)"
    else
      "$TMUX_BIN" send-keys -t "$id" -l "$MSG" && "$TMUX_BIN" send-keys -t "$id" Enter \
        && { log "tapped pane $name ($id)"; TAPPED=$((TAPPED+1)); } \
        || log "FAILED to tap pane $name ($id)"
    fi
  done < <("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}|#{pane_dead}' 2>/dev/null)
else
  log "fleet session down — no panes to wrap"
fi

# ── For-the-record bus mail (best-effort; never blocks) ──
ENV_FILE="$PROJECT_DIR/4_Credentials/.env"
if [ "$DRYRUN" != "1" ] && [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE" 2>/dev/null || true
  if [ -n "${AGENTMAIL_API_KEY:-}" ]; then
    HTTP_CODE="$(curl -s -o /dev/null -w '%{http_code}' -m 15 \
      -X POST "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages/send" \
      -H "Authorization: Bearer $AGENTMAIL_API_KEY" -H "Content-Type: application/json" \
      -d "{\"to\":[\"coagent@agentmail.to\"],\"subject\":\"[Wednesday -> all agents] Morning shift change $TODAY — checkpoint (continue if your queue is live)\",\"text\":\"Scheduled 05:30 shift change (WED-16), per the 2026-08-28 overnight-is-working-time grant: a session with a LIVE queue CONTINUES (checkpoint at its own boundary); only a session with a DRY queue wraps now (end-of-session ritual, wrap email to wednesday-agent@). Panes tapped directly: $TAPPED. This mail is the record; the tap on your prompt is the trigger.\"}" 2>/dev/null)"
    log "bus mail HTTP $HTTP_CODE"
  else
    log "bus mail skipped: AGENTMAIL_API_KEY unset"
  fi
fi

[ "$DRYRUN" = "1" ] || echo "$TODAY" > "$STATE_DIR/last_shift_change"
log "shift change complete: $TAPPED pane(s) tapped"
