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
#   --self   the seat rotates ITSELF inside the 80-90% band (Kam 2026-09-07 10:49;
#            supersedes 80-85 of 09-05 and 70-80 of 09-02). 70% is a CHECKPOINT
#            ONLY - refresh the handover, start nothing heavy, do NOT rotate. Refuse
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
# ── SEAT RESOLUTION (2026-09-13, Tuesday's ask; learnings/2026-09-09_the-seat-
# resolver-is-the-layer-above-every-agent-aware-fix.md): WED_AGENT if set, else the
# TREE'S OWN NAME — the same resolver wake_watch.sh uses. Wednesday's tree resolves
# to "wednesday", so the pane lookup and launcher below are byte-identical to before;
# Tuesday's seat (same script, her own `fleet`) gets her pane name and her launcher.
# No fallback to the other seat's launcher: a missing one REFUSES (a guess here
# boots the wrong identity — the 2026-09-09 case).
_tree_seat=wednesday
case "$(basename "$PROJECT_DIR")" in TUESDAY|Tuesday|tuesday) _tree_seat=tuesday ;; esac
SEAT="${WED_AGENT:-$_tree_seat}"
case "$SEAT" in
  tuesday)   SEAT_LAUNCHER="$PROJECT_DIR/Launch_Tuesday.command" ;;
  wednesday) SEAT_LAUNCHER="$PROJECT_DIR/Launch_Wednesday.command" ;;
  *) log "REFUSED: WED_AGENT='$SEAT' is not a seat this script knows (wednesday|tuesday)"; exit 2 ;;
esac
export WED_AGENT="$SEAT"   # the detached checker resolves the seat from this
if [ -z "${ROTATE_LAUNCH_CMD:-}" ] && [ ! -f "$SEAT_LAUNCHER" ]; then
  log "REFUSED: seat '$SEAT' but its launcher is missing: $SEAT_LAUNCHER"; exit 2
fi
LAUNCH_CMD="${ROTATE_LAUNCH_CMD:-bash \"$SEAT_LAUNCHER\"}"

"$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null || { log "REFUSED: no tmux session '$FLEET'"; exit 2; }
WROW=$("$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{@cockpit_name}|#{pane_id}' 2>/dev/null | awk -F'|' -v s="$SEAT" '$1==s' | head -1)
[ -n "$WROW" ] || { log "REFUSED: no '$SEAT' pane in '$FLEET'"; exit 2; }
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
  REASON="planned rotation inside Kam's 80-90% context band"
fi

STAMP=$(date '+%H:%M')

# ── POST-RESPAWN LIVENESS CHECK (2026-09-13; the 16:04:29 loss — see
# reference/2026-09-13_fleet-loss-1604/rotation_1604_diagnosis.md and the header of
# rotate_liveness.sh). At 16:04:29 on 09-12 the `respawn-pane -k` below was followed
# 36 ms later by the death of the WHOLE fleet session (3 agents + QA gate + monitor);
# this script said "respawned OK" and told Kam "agents are untouched" without looking.
# Now: (1) the pane inventory is recorded BEFORE the respawn, to the log and to a
# state file; (2) a checker is spawned DETACHED WITH NO TTY before the respawn (it
# must not share this pane's tty — learnings/2026-09-03_a-pane-close-is-a-session-
# kill.md) and, ~25 s later, verifies the session, every agent pane and the new
# coordinator process, alarming + relaunching the coordinator on loss. The
# `ps -o pid,ppid,sess,tty` of the checker goes in the log: tty must read `??`.
# (Measured 2026-09-13: macOS `ps -o sess` prints 0 for EVERY process, pane shells
# included — the tty column is the reading that decides; `os.getsid()` is the
# instrument if the session id itself is ever needed.)
# macOS has no setsid(1); python's os.setsid + execvp is the portable shape (the same
# one the 08:45 panel_sync restart used). The state dir is gitignored by design
# (.gitignore:44); the SCRIPTS are tracked.
STATE_DIR="$HERE/state"; mkdir -p "$STATE_DIR"
BEFORE_TS="$(date '+%Y%m%d_%H%M%S')"
BEFORE_FILE="$STATE_DIR/rotate_before_${BEFORE_TS}.txt"
"$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{pane_id} [#{@cockpit_name}] #{pane_title} #{pane_pid}' > "$BEFORE_FILE" 2>>"$LOG"
log "pane inventory BEFORE respawn ($(grep -c . "$BEFORE_FILE") panes) -> $BEFORE_FILE"
while IFS= read -r _row; do log "  before: $_row"; done < "$BEFORE_FILE"
LIVENESS="$HERE/rotate_liveness.sh"
if [ -x "$LIVENESS" ]; then
  LIVENESS_TEST=0; LIVENESS_STUB_DIR=""
  if [ -n "${ROTATE_TMUX_SESSION:-}" ]; then LIVENESS_TEST=1; LIVENESS_STUB_DIR="${ROTATE_LIVENESS_STUB_DIR:-}"; fi
  LIVENESS_LAUNCH_CMD="$LAUNCH_CMD" LIVENESS_TEST="$LIVENESS_TEST" LIVENESS_STUB_DIR="$LIVENESS_STUB_DIR" \
    python3 -c 'import os,sys; os.setsid(); os.execvp(sys.argv[1], sys.argv[1:])' \
      nohup bash "$LIVENESS" "$FLEET" "$BEFORE_FILE" "$PANE_ID" </dev/null >>"$LOG" 2>&1 &
  LIVE_PID=$!
  sleep 1
  LIVE_PS="$(ps -o pid=,ppid=,sess=,tty= -p "$LIVE_PID" 2>/dev/null | tr -s ' ')"
  LIVE_TTY="$(printf '%s' "$LIVE_PS" | awk '{print $4}')"
  if [ -z "$LIVE_PS" ]; then
    log "WARNING: liveness checker pid $LIVE_PID is NOT running one second after spawn — respawning UNGUARDED (see log above)"
  elif [ "$LIVE_TTY" != "??" ]; then
    log "WARNING: liveness checker pid $LIVE_PID has a tty ($LIVE_PS) — it may die with this pane; respawning anyway"
  else
    log "liveness checker spawned detached: pid/ppid/sess/tty =$LIVE_PS (fires in ~25 s)"
  fi
else
  log "WARNING: $LIVENESS missing or not executable — respawning UNGUARDED (doctor.sh should have failed on this)"
fi

log "respawning $SEAT pane $PANE_ID in '$FLEET' ($MODE): $REASON"
if "$TMUX_BIN" respawn-pane -k -t "$PANE_ID" "$LAUNCH_CMD; echo; echo '[cockpit] $SEAT exited — pane stays for inspection'; exec bash"; then
  "$TMUX_BIN" set-option -p -t "$PANE_ID" @cockpit_name "$SEAT" 2>>"$LOG" || true
  log "respawned OK ($MODE) — liveness verdict follows in ~25 s"
  if [ -z "${ROTATE_TMUX_SESSION:-}" ]; then
    # "agents are untouched" is no longer asserted here (the 16:04 loss): the liveness
    # checker reports the agents' state; this line only says what was checked.
    bash "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" "Coordinator seat rotated automatically at $STAMP — $REASON. A fresh seat is booting now (about ten minutes); agents' mail waits for it. A liveness check runs 25 s after the respawn and will alarm here if the fleet session or any agent pane was lost." >>"$LOG" 2>&1 || log "chat mirror failed (see log)"
    H=$((10#$(date +%H)))
    if [ "$H" -ge 6 ] && [ "$H" -lt 23 ]; then
      bash "$PROJECT_DIR/2_Project_Files/voice/speak.sh" "Kam, my seat rotated itself. A fresh one is booting now." >>"$LOG" 2>&1 || true
    fi
  fi
  exit 0
else
  log "ERROR: respawn-pane failed for $PANE_ID"; exit 1
fi
