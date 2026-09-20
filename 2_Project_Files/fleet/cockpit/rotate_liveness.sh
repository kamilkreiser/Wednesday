#!/bin/bash
# rotate_liveness.sh — the post-respawn LIVENESS CHECK for wednesday_rotate.sh.
#
# WHY (2026-09-13, reference/2026-09-13_fleet-loss-1604/rotation_1604_diagnosis.md):
# at 16:04:29 on 2026-09-12 `respawn-pane -k` ran on the coordinator's pane %0 and
# 36 ms later the ENTIRE `fleet` tmux session died as one unit — three agents, the
# QA gate, the monitor, and the launcher that had just started. The trigger was
# never established (1 loss in 63 rotations). The rotate script logged "respawned
# OK" and told Kam "agents are untouched" WITHOUT CHECKING, and nothing recovered
# a missing fleet session for 16 hours. Kam's 14:2x grant (learnings/2026-09-13_
# rotation-never-blocks-the-work-delegate-then-rotate.md) answers the loss with a
# MECHANISM, not a hold: this script.
#
# Usage: rotate_liveness.sh <session> <before-file> <coordinator-pane-id>
#   <session>      the tmux session the rotation respawned inside (fleet, or a
#                  scratch wedtest_* session under the rotate test hooks)
#   <before-file>  the pane inventory wednesday_rotate.sh wrote BEFORE the respawn
#                  (state/rotate_before_<ts>.txt; one pane per line, pane_id first,
#                  pane_pid last, [@cockpit_name] second, pane_title in between)
#   <coordinator-pane-id>  the pane that was respawned (%N); it is EXPECTED to
#                  change process — it is checked for presence + a live process,
#                  not for identity with the before-file.
#
# It MUST be spawned DETACHED with NO tty (learnings/2026-09-03_a-pane-close-is-a-
# session-kill.md): a process sharing the respawned pane's tty dies with the pane
# whatever its ppid says. wednesday_rotate.sh does this via python os.setsid (macOS
# ships no setsid binary) + nohup, stdin from /dev/null, and logs `ps -o
# pid,ppid,sess,tty` of the spawned checker so the tty reading is in the record.
#
# Waits LIVENESS_DELAY (25 s) then checks:
#   (a) `tmux has-session -t <session>`
#   (b) every pane id in the before-file except the coordinator's still exists
#   (c) every one of those panes still has a LIVE AGENT in it — pane_agent_live.sh
#       (2026-09-20; see below). PRESENCE IS NOT ALIVENESS.
#   (d) the coordinator pane exists, is not pane_dead, and its process is alive
# QUIET path: logs `LIVENESS OK: session alive, N/N agent panes present, M agent-live,
#   coordinator pid P`. Nothing else.
#
# (c) — ADDED 2026-09-20, the second defect of the day. Until today this script
# compared the before-file's pane ids against the ids present after and called that
# aliveness. It is not. At 16:03:26 the before-file recorded
#     %124 [Secuura/Blockchain-BOARD] Kamils-Mac-Studio.local 49466
# — a pane whose agent had exited ~15 minutes earlier, leaving a bare shell — and the
# rotation logged OK and moved on. Every pane in the before-file that is neither the
# coordinator nor a DECLARED SHELL ROLE must now prove a live agent, via the
# two-source predicate in pane_agent_live.sh (no claude process under the pane's pid
# AND no `✳` activity marker in its title ⇒ NOT LIVE). A pane that fails that is a
# FIRE, on the same alarm + speak + panel path as a missing pane.
#   LIVENESS_SHELL_ROLES — space-separated @cockpit_name values that are ALLOWED to
#   be bare shells; default `fleet-monitor`, which is legitimately a shell (measured
#   2026-09-20: %1 fleet-monitor title `Kamils-Mac-Studio.local`, no claude process)
#   and must never alarm. The COORDINATOR is exempt implicitly — it was just
#   respawned and is still booting, so it has no claude process yet; it keeps its own
#   check (d), which asks only that its pane and process exist.
# FIRE path (session gone, or any agent pane missing or fallen to a shell, or
# coordinator dead):
#   - logs `LIVENESS FAIL …` naming what is missing
#   - writes state/ROTATE_LOSS_<ts>.txt (before-list + after-list); doctor.sh
#     WARNS on that file until the seat quarantines it — never deleted here
#   - speaks (speak.sh, WEDNESDAY_SPEAK_URGENT=1 + WEDNESDAY_SPEAK_LOCAL=1: the
#     browser-only rule of 2026-09-08 names "a genuine emergency" as the case for
#     LOCAL; a dead fleet is one)
#   - mirrors ONE line to Kam's panel (chat_reply.sh --project WED)
#   - if the WHOLE SESSION is gone: relaunches the COORDINATOR ONLY, by running
#     $LIVENESS_LAUNCH_CMD (the launcher command the rotate script already knows)
#     inside a fresh tmux session of the same name, the same shape cockpit.sh `up`
#     uses for its first pane. Agents cannot be resurrected mid-turn; the successor
#     relaunches them from the pickup file. Session survived but a pane missing:
#     alarm only, no relaunch.
#
# SEAT-AGNOSTIC (Tuesday's ask, 2026-09-13; learnings/2026-09-09_the-seat-resolver-
# is-the-layer-above-every-agent-aware-fix.md): nothing seat-specific is hardcoded.
# The seat is resolved ONCE: WED_AGENT if set → else the coordinator pane's
# [@cockpit_name] as recorded in the before-file → else the tree's own name
# (TUESDAY → tuesday, otherwise wednesday). The log/mirror line names that seat.
#
# Environment (set by wednesday_rotate.sh):
#   LIVENESS_LAUNCH_CMD  launcher command for the coordinator relaunch (required)
#   LIVENESS_DELAY       seconds before the check (default 25)
#   LIVENESS_TEST=1      TEST MODE: the rotate test hooks are in force. The real
#                        speak.sh / chat_reply.sh are NEVER called; the alarm
#                        actions go to $LIVENESS_STUB_DIR/speak.sh and
#                        $LIVENESS_STUB_DIR/chat_reply.sh, and if a stub is missing
#                        the action is SKIPPED and logged (08-17 rule: a test hook
#                        never defaults to the production action).
#   LIVENESS_STUB_DIR    directory of the two stubs (test mode only)
#   LIVENESS_PENDING_FILE  the marker wednesday_rotate.sh wrote BEFORE the respawn.
#                        THIS SCRIPT IS THE ONLY THING THAT CLEARS IT — on every
#                        exit path that logs a verdict. A marker still on disk
#                        therefore means "a rotation armed a checker and no verdict
#                        was ever logged", which is exactly the 2026-09-20 D1 defect
#                        (25 real armings, 0 verdicts, and nothing anywhere said so).
#                        doctor.sh warns on a stale one, so the SUCCESSOR lands on it
#                        at its next boot instead of the silence lasting two days.
#                        Cleared by RENAME (…/consumed_<name>), never rm — 2026-08-26
#                        never-delete; cleanup means quarantine.
#   LIVENESS_SHELL_ROLES  @cockpit_name values allowed to be bare shells
#                        (default: fleet-monitor)
# macOS bash 3.2 — no declare -A, no timeout. Never discards stderr.
# Logs to cockpit/logs/rotate_wednesday.log (the rotate script's log), tagged
# [liveness]. rc 0 = OK, 1 = usage, 10 = LIVENESS FAIL (after the alarm actions).
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$HERE/../../.." && pwd)"
LOG_DIR="$HERE/logs"; mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/rotate_wednesday.log"
STATE_DIR="$HERE/state"; mkdir -p "$STATE_DIR"
log() { echo "$(date '+%F %T') [liveness] $*" >> "$LOG"; }
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

SESSION="${1:-}"; BEFORE="${2:-}"; COORD="${3:-}"
if [ -z "$SESSION" ] || [ -z "$BEFORE" ] || [ -z "$COORD" ]; then
  echo "usage: rotate_liveness.sh <session> <before-file> <coordinator-pane-id>" >&2; exit 1
fi
[ -r "$BEFORE" ] || { log "USAGE ERROR: before-file '$BEFORE' unreadable — check NOT run"; exit 1; }
LAUNCH_CMD="${LIVENESS_LAUNCH_CMD:-}"
DELAY="${LIVENESS_DELAY:-25}"
TEST_MODE="${LIVENESS_TEST:-0}"
STUB_DIR="${LIVENESS_STUB_DIR:-}"
PENDING="${LIVENESS_PENDING_FILE:-}"
SHELL_ROLES="${LIVENESS_SHELL_ROLES:-fleet-monitor}"
AGENTLIVE="$HERE/pane_agent_live.sh"

# Clear the "a checker armed and never reported" marker. Called on EVERY path that
# logs a verdict, and on no other path.
clear_pending() {
  [ -n "$PENDING" ] || return 0
  [ -e "$PENDING" ] || return 0
  if mv "$PENDING" "$(dirname "$PENDING")/consumed_$(basename "$PENDING")" 2>>"$LOG"; then
    log "pending marker cleared (verdict logged): $(basename "$PENDING")"
  else
    log "WARNING: could not clear the pending marker $PENDING — doctor.sh will warn on it although a verdict WAS logged"
  fi
}
is_shell_role() {  # $1 = @cockpit_name
  for _r in $SHELL_ROLES; do [ "$1" = "$_r" ] && return 0; done
  return 1
}

# ── seat resolution (once) ─────────────────────────────────────────────────
_tree_seat=wednesday
case "$(basename "$PROJECT_DIR")" in TUESDAY|Tuesday|tuesday) _tree_seat=tuesday ;; esac
_pane_seat="$(awk -v c="$COORD" '$1==c{gsub(/[\[\]]/,"",$2); print $2; exit}' "$BEFORE" 2>/dev/null)"
case "${WED_AGENT:-}" in
  tuesday|wednesday) SEAT="$WED_AGENT" ;;
  *) case "$_pane_seat" in tuesday|wednesday) SEAT="$_pane_seat" ;; *) SEAT="$_tree_seat" ;; esac ;;
esac
case "$SEAT" in tuesday) SEAT_NAME="Tuesday" ;; *) SEAT_NAME="Wednesday" ;; esac

TS="$(date '+%Y%m%d_%H%M%S')"
log "armed for '$SESSION' (seat $SEAT, coordinator $COORD, before-file $(basename "$BEFORE"), delay ${DELAY}s, test=$TEST_MODE)"
sleep "$DELAY"

# ── measure ────────────────────────────────────────────────────────────────
SESSION_ALIVE=0
"$TMUX_BIN" has-session -t "=$SESSION" 2>/dev/null && SESSION_ALIVE=1
AFTER=""
if [ "$SESSION_ALIVE" = 1 ]; then
  AFTER="$("$TMUX_BIN" list-panes -s -t "=$SESSION" -F '#{pane_id} [#{@cockpit_name}] #{pane_title} #{pane_pid} dead=#{pane_dead}' 2>>"$LOG")"
fi
EXPECTED=0; PRESENT=0; MISSING=""; DEADAGENTS=""; AGENTLIVE_OK=0
if [ ! -x "$AGENTLIVE" ]; then
  # A check that silently does not run is the defect this whole file exists to stop.
  log "WARNING: $AGENTLIVE missing or not executable — the agent-LIVENESS half of the check is NOT running; presence only (doctor.sh should have failed on this)"
fi
while read -r pid_ name_ rest_; do
  [ -n "$pid_" ] || continue
  [ "$pid_" = "$COORD" ] && continue
  # Never hand anything but a real pane id to tmux: an empty or malformed -t target
  # is NOT a no-op, it applies to the caller's own pane (2026-09-17, the arm that
  # renamed the live coordinator pane and blinded the watcher for ten minutes).
  case "$pid_" in %[0-9]*) : ;; *) log "  skipping malformed before-file row (pane id '$pid_')"; continue ;; esac
  EXPECTED=$((EXPECTED+1))
  if printf '%s\n' "$AFTER" | awk -v p="$pid_" '$1==p{f=1} END{exit !f}'; then
    PRESENT=$((PRESENT+1))
    _nm="$(printf '%s' "${name_:-}" | tr -d '[]')"
    if is_shell_role "${_nm:-?}"; then
      :   # a declared shell role (fleet-monitor): present is all that is asked of it
    elif [ -x "$AGENTLIVE" ]; then
      # </dev/null so the helper can never swallow this loop's stdin (the before-file).
      if TMUX_BIN="$TMUX_BIN" bash "$AGENTLIVE" "${pid_:?}" </dev/null 2>>"$LOG"; then
        AGENTLIVE_OK=$((AGENTLIVE_OK+1))
      else
        DEADAGENTS="$DEADAGENTS ${pid_}[${_nm:-?}]"
      fi
    fi
  else
    MISSING="$MISSING $pid_"
  fi
done < "$BEFORE"
COORD_PID=""; COORD_STATE="missing"
if [ "$SESSION_ALIVE" = 1 ]; then
  _crow="$(printf '%s\n' "$AFTER" | awk -v c="$COORD" '$1==c{print; exit}')"
  if [ -n "$_crow" ]; then
    COORD_PID="$(printf '%s\n' "$_crow" | awk '{print $(NF-1)}')"
    case "$_crow" in *"dead=1"*) COORD_STATE="pane_dead" ;; *)
      if [ -n "$COORD_PID" ] && kill -0 "$COORD_PID" 2>/dev/null; then COORD_STATE="live"; else COORD_STATE="no live process (pid ${COORD_PID:-?})"; fi ;;
    esac
  fi
fi

# ── quiet path ─────────────────────────────────────────────────────────────
if [ "$SESSION_ALIVE" = 1 ] && [ -z "$MISSING" ] && [ -z "$DEADAGENTS" ] && [ "$COORD_STATE" = "live" ]; then
  log "LIVENESS OK: session alive, $PRESENT/$EXPECTED agent panes present, $AGENTLIVE_OK agent-live, coordinator pid $COORD_PID"
  clear_pending
  exit 0
fi

# ── fire path ──────────────────────────────────────────────────────────────
if [ "$SESSION_ALIVE" = 0 ]; then
  WHAT="tmux session '$SESSION' is GONE (all $EXPECTED agent pane(s) + coordinator lost)"
elif [ -n "$MISSING" ] || [ -n "$DEADAGENTS" ]; then
  WHAT="session alive"
  [ -n "$MISSING" ]    && WHAT="$WHAT but agent pane(s) MISSING:${MISSING}"
  [ -n "$DEADAGENTS" ] && WHAT="$WHAT; agent pane(s) PRESENT BUT DEAD (fallen to a shell):${DEADAGENTS}"
  WHAT="$WHAT ($PRESENT/$EXPECTED present, $AGENTLIVE_OK agent-live); coordinator $COORD $COORD_STATE"
else
  WHAT="session alive, $PRESENT/$EXPECTED agent panes present, but coordinator $COORD is $COORD_STATE"
fi
log "LIVENESS FAIL: $WHAT"
clear_pending
ALARM="$STATE_DIR/ROTATE_LOSS_${TS}.txt"
{
  echo "ROTATE_LOSS — $(date '+%F %T') — seat $SEAT — session '$SESSION' — coordinator $COORD"
  echo "WHAT: $WHAT"
  echo; echo "BEFORE ($(basename "$BEFORE")):"; cat "$BEFORE"
  echo; echo "AFTER:"; if [ -n "$AFTER" ]; then printf '%s\n' "$AFTER"; else echo "(no session)"; fi
  echo; echo "Quarantine this file after reading (move, never rm); doctor.sh WARNS while it is here."
} > "$ALARM" 2>>"$LOG"
log "alarm file written: $ALARM"

if [ "$SESSION_ALIVE" = 0 ]; then
  SPOKEN="Kam — the fleet session died during my rotation. Relaunch needed: I am bringing the coordinator back; the agents must be relaunched from the pickup file."
  PANEL="${SEAT_NAME}: the fleet tmux session DIED during my rotation ($(date '+%H:%M')) — every agent pane was lost. Coordinator relaunch attempted automatically; agents need relaunching from the pickup file. Alarm: $(basename "$ALARM")."
elif [ -n "$DEADAGENTS" ] && [ -z "$MISSING" ]; then
  # The 2026-09-20 failure mode: nothing vanished, but an agent pane is a bare shell.
  # It gets the SAME alarm file + speak + panel path as a lost pane — a new failure
  # mode that only reaches the log is the defect being fixed, not a fix.
  SPOKEN="Kam — an agent pane is alive but empty: its agent has exited and left a shell. The fleet session is fine; that project is doing nothing."
  PANEL="${SEAT_NAME}: agent pane(s) PRESENT BUT DEAD at my rotation ($(date '+%H:%M')) —${DEADAGENTS} had exited, leaving a bare shell. Nothing was lost by the rotation; that work is simply stopped. Relaunch from the pickup file. Alarm: $(basename "$ALARM")."
else
  SPOKEN="Kam — a pane was lost during my rotation. The fleet session is alive; check the alarm file."
  PANEL="${SEAT_NAME}: pane loss during my rotation ($(date '+%H:%M')) — $WHAT. No relaunch (session alive). Alarm: $(basename "$ALARM")."
fi

# speak + mirror. TEST MODE never reaches the real scripts.
if [ "$TEST_MODE" = 1 ]; then
  if [ -n "$STUB_DIR" ] && [ -x "$STUB_DIR/speak.sh" ]; then
    WEDNESDAY_SPEAK_URGENT=1 WEDNESDAY_SPEAK_LOCAL=1 bash "$STUB_DIR/speak.sh" "$SPOKEN" >>"$LOG" 2>&1 || log "speak STUB failed rc=$?"
  else log "test mode: speak.sh stub missing in '${STUB_DIR:-unset}' — speak SKIPPED (never the production action from a test)"; fi
  if [ -n "$STUB_DIR" ] && [ -x "$STUB_DIR/chat_reply.sh" ]; then
    bash "$STUB_DIR/chat_reply.sh" --project WED "$PANEL" >>"$LOG" 2>&1 || log "chat_reply STUB failed rc=$?"
  else log "test mode: chat_reply.sh stub missing in '${STUB_DIR:-unset}' — panel mirror SKIPPED (never the production action from a test)"; fi
else
  WEDNESDAY_SPEAK_URGENT=1 WEDNESDAY_SPEAK_LOCAL=1 bash "$PROJECT_DIR/2_Project_Files/voice/speak.sh" "$SPOKEN" >>"$LOG" 2>&1 || log "speak failed rc=$? (see log)"
  bash "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" --project WED "$PANEL" >>"$LOG" 2>&1 || log "panel mirror failed rc=$? (see log)"
fi

# relaunch the COORDINATOR only, and only when the whole session is gone
if [ "$SESSION_ALIVE" = 0 ]; then
  if [ -z "$LAUNCH_CMD" ]; then
    log "RELAUNCH SKIPPED: LIVENESS_LAUNCH_CMD is empty — relaunch the coordinator by hand"
  elif "$TMUX_BIN" has-session -t "=$SESSION" 2>/dev/null; then
    log "RELAUNCH SKIPPED: session '$SESSION' reappeared before the relaunch — not creating a second one"
  else
    log "RELAUNCH: creating tmux session '$SESSION' with the coordinator only: $LAUNCH_CMD"
    if "$TMUX_BIN" new-session -d -s "$SESSION" -n main "$LAUNCH_CMD; echo; echo '[cockpit] $SEAT exited — pane stays for inspection'; exec bash" 2>>"$LOG"; then
      NEWPANE="$("$TMUX_BIN" list-panes -t "=$SESSION:0" -F '#{pane_id}' 2>>"$LOG" | head -1)"
      "$TMUX_BIN" set-option -p -t "$NEWPANE" @cockpit_name "$SEAT" 2>>"$LOG" || true
      log "RELAUNCH OK: coordinator '$SEAT' running in $NEWPANE of new session '$SESSION' (agents NOT restored — successor relaunches them from the pickup file)"
    else
      log "RELAUNCH FAILED: tmux new-session rc=$? — relaunch the coordinator by hand"
    fi
  fi
fi
exit 10
