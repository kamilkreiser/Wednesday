#!/bin/bash
# wednesday_rotate.sh — respawn the coordinator's OWN pane with the launcher.
#
# WHY THIS EXISTS (enforcement, not advice — 2026-09-02): the 06:39 seat was
# woken at ctx 50% (06:46) and 65% (07:45) by the watcher, dismissed both as a
# "statusline misparse" on the strength of the harness token-budget counter,
# and hit the hard context limit at 09:49:58 AEST ("Prompt is too long"). From
# then until Kam killed the fleet at 16:06 — six hours — the watcher tapped the
# dead pane 94 times ("Context limit reached · /compact or /clear to continue")
# and nothing could act: `cockpit.sh rotate wednesday` is refused by design and
# no script existed to respawn the coordinator. Both agents sat idle on
# unanswered mail the whole time. A coordinator that cannot rotate itself, and
# nothing that rotates it from outside, is a single point of failure with a
# six-hour blast radius.
#
# Modes (exactly one):
#   --dead   the seat is DEAD: refuse unless the wednesday pane's capture shows
#            the literal "Context limit reached" (never kill a live seat on a
#            guess). Called by the wake runner's DEAD case. rc 3 = refused.
#   --self   the seat rotates ITSELF at 70% (Kam's 2026-08-21 rule): refuse
#            unless the WEDNESDAY repo HEAD equals origin/main (everything
#            durable is pushed — rhythm §3 item 3). rc 4 = refused. Run it
#            DETACHED from the seat (nohup … &): the respawn kills the caller.
# Test hooks — BOTH or NONE (08-17 rule: a test hook may never default to the
# production action): ROTATE_TMUX_SESSION + ROTATE_LAUNCH_CMD.
# Never discards stderr. Logs to cockpit/logs/rotate_wednesday.log.
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$HERE/../../.." && pwd)"
LOG_DIR="$HERE/logs"; mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/rotate_wednesday.log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; echo "$*"; }
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

MODE="${1:-}"
case "$MODE" in --dead|--self) ;; *) echo "usage: wednesday_rotate.sh --dead | --self" >&2; exit 2 ;; esac

if [ -n "${ROTATE_TMUX_SESSION:-}" ] && [ -z "${ROTATE_LAUNCH_CMD:-}" ] || [ -z "${ROTATE_TMUX_SESSION:-}" ] && [ -n "${ROTATE_LAUNCH_CMD:-}" ]; then
  log "REFUSED: test hooks must be set both or none (ROTATE_TMUX_SESSION + ROTATE_LAUNCH_CMD)"; exit 2
fi
FLEET="${ROTATE_TMUX_SESSION:-fleet}"
LAUNCH_CMD="${ROTATE_LAUNCH_CMD:-bash \"$PROJECT_DIR/Launch_Wednesday.command\"}"

"$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null || { log "REFUSED: no tmux session '$FLEET'"; exit 2; }
WROW=$("$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{@cockpit_name}|#{pane_id}' 2>/dev/null | awk -F'|' '$1=="wednesday"' | head -1)
[ -n "$WROW" ] || { log "REFUSED: no wednesday pane in '$FLEET'"; exit 2; }
PANE_ID="${WROW#*|}"

if [ "$MODE" = "--dead" ]; then
  CAP=$("$TMUX_BIN" capture-pane -t "$PANE_ID" -p -S -60 2>/dev/null)
  if ! printf '%s\n' "$CAP" | grep -q 'Context limit reached'; then
    log "REFUSED (--dead): pane $PANE_ID does not show 'Context limit reached' — not killing a seat that may be alive"; exit 3
  fi
  REASON="the previous seat hit its hard context limit and could not act"
else
  # --self: everything durable must be on origin before the seat is replaced.
  if [ -z "${ROTATE_TMUX_SESSION:-}" ] || [ "${ROTATE_SELF_GIT_CHECK:-1}" = "1" ]; then
    git -C "$PROJECT_DIR" fetch -q origin main 2>>"$LOG" || { log "REFUSED (--self): git fetch failed (see log)"; exit 4; }
    LOCAL=$(git -C "$PROJECT_DIR" rev-parse HEAD 2>>"$LOG"); REMOTE=$(git -C "$PROJECT_DIR" rev-parse origin/main 2>>"$LOG")
    if [ -z "$LOCAL" ] || [ "$LOCAL" != "$REMOTE" ]; then
      log "REFUSED (--self): HEAD $LOCAL != origin/main $REMOTE — push the handover first (rhythm §3 item 3)"; exit 4
    fi
    DIRTY=$(git -C "$PROJECT_DIR" status --porcelain 2>>"$LOG" | grep -v '0_Brain/dashboard/data/' | grep -v '^?? .*conflict_on_' || true)
    if [ -n "$DIRTY" ]; then
      log "REFUSED (--self): working tree has uncommitted changes outside the dashboard data churn — commit + push the handover first:"; printf '%s\n' "$DIRTY" | head -10 >> "$LOG"; exit 4
    fi
  fi
  REASON="planned rotation at the 70% context tripwire"
fi

STAMP=$(date '+%H:%M')
log "respawning wednesday pane $PANE_ID in '$FLEET' ($MODE): $REASON"
if "$TMUX_BIN" respawn-pane -k -t "$PANE_ID" "$LAUNCH_CMD; echo; echo '[cockpit] wednesday exited — pane stays for inspection'; exec bash"; then
  "$TMUX_BIN" set-option -p -t "$PANE_ID" @cockpit_name wednesday 2>>"$LOG" || true
  log "respawned OK ($MODE)"
  if [ -z "${ROTATE_TMUX_SESSION:-}" ]; then
    bash "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" "Coordinator seat rotated automatically at $STAMP — $REASON. A fresh seat is booting now (about ten minutes); agents are untouched and their mail waits for it." >>"$LOG" 2>&1 || log "chat mirror failed (see log)"
    H=$((10#$(date +%H)))
    if [ "$H" -ge 6 ] && [ "$H" -lt 23 ]; then
      bash "$PROJECT_DIR/2_Project_Files/voice/speak.sh" "Kam, my seat rotated itself. A fresh one is booting now." >>"$LOG" 2>&1 || true
    fi
  fi
  exit 0
else
  log "ERROR: respawn-pane failed for $PANE_ID"; exit 1
fi
