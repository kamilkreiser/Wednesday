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
# 2026-09-13 (Tuesday's 19:1x finding): the seat AND the pane lookup now come from
# the ONE shared resolver, seat_resolve.sh — the same rule as before (WED_AGENT,
# else the tree's own name), so Wednesday's tree still resolves to "wednesday".
. "$HERE/seat_resolve.sh" || { log "REFUSED: $HERE/seat_resolve.sh missing — cannot resolve the seat"; exit 2; }
seat_resolve "$PROJECT_DIR"
case "$SEAT" in
  tuesday)   SEAT_LAUNCHER="$PROJECT_DIR/Launch_Tuesday.command" ;;
  wednesday) SEAT_LAUNCHER="$PROJECT_DIR/Launch_Wednesday.command" ;;
  friday)    SEAT_LAUNCHER="$PROJECT_DIR/Launch_Friday.command" ;;   # 2026-09-23: the laptop seat (FRIDAY tree)
  *) log "REFUSED: WED_AGENT='$SEAT' is not a seat this script knows (wednesday|tuesday|friday)"; exit 2 ;;
esac
export WED_AGENT="$SEAT"   # the detached checker resolves the seat from this
if [ -z "${ROTATE_LAUNCH_CMD:-}" ] && [ ! -f "$SEAT_LAUNCHER" ]; then
  log "REFUSED: seat '$SEAT' but its launcher is missing: $SEAT_LAUNCHER"; exit 2
fi
LAUNCH_CMD="${ROTATE_LAUNCH_CMD:-bash \"$SEAT_LAUNCHER\"}"

"$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null || { log "REFUSED: no tmux session '$FLEET'"; exit 2; }
# The pane: @cockpit_name == $SEAT, else the legacy "wednesday" pane IF this tree's
# own seat is $SEAT (cockpit.conf still names pane 0 "wednesday" on the mini —
# the case that refused --self and --dead for Tuesday on 2026-09-13). The guard
# and the refusal wording live in seat_resolve.sh; the respawn below renames the
# pane to $SEAT, so after one rotation the legacy branch is no longer taken.
PANE_ID=$(coord_pane_id "=$FLEET" 2>"$LOG_DIR/.rotate_resolve_err.$$") || {
  log "REFUSED: $(cat "$LOG_DIR/.rotate_resolve_err.$$" 2>/dev/null) [session '$FLEET']"; rm -f "$LOG_DIR/.rotate_resolve_err.$$"; exit 2; }
rm -f "$LOG_DIR/.rotate_resolve_err.$$"

if [ "$MODE" = "--dead" ]; then
  # 2026-09-14: same predicate as the watcher's DEAD leg (dead_banner_check.sh) — a bare
  # literal grep re-confirmed two false kills; the re-check must discriminate, not repeat.
  # 2026-09-17: an EXITED session (shell in the pane, the cockpit's exit marker, no claude process —
  # exited_seat_check.sh) is dead too; before this the watcher could see it and this re-check refused it.
  if TMUX_BIN="$TMUX_BIN" bash "$HERE/dead_banner_check.sh" "$PANE_ID"; then
    REASON="the previous seat hit its hard context limit and could not act"
  elif TMUX_BIN="$TMUX_BIN" bash "$HERE/exited_seat_check.sh" "$PANE_ID"; then
    REASON="the previous seat's Claude session exited and left a shell in its pane"
  else
    log "REFUSED (--dead): pane $PANE_ID shows neither 'Context limit reached' nor an exited session — not killing a seat that may be alive"; exit 3
  fi
else
  # --self: everything durable must be on origin before the seat is replaced.
  #
  # 2026-09-16 (ledger w=2 — the 01:11 refusal): a --self REFUSE went to this log and
  # NOTHING ELSE. The seat had launched the script detached, written "rotating" into
  # its note and ended its turn; no watcher leg fires on a refused respawn, so the
  # pane sat 4 h 19 min with the model idle on a never-idle day — found only when the
  # 05:30 shift-change tap landed on it. Two mechanisms, both in the path:
  #   (1) every --self refusal is TAPPED at the seat's own pane through cockpit.sh say
  #       (a bare pointer at this log; read back by `say`) — a refusal that no one
  #       reads is indistinguishable from working (learnings/2026-09-10_a-refusal-
  #       nobody-reads-is-indistinguishable-from-working.md);
  #   (2) "HEAD not contained in origin" is met with ONE push of the seat's OWN repo
  #       before it is a refusal — the 01:11 case was a panel_sync commit that landed
  #       between the seat's push and this check, on Wednesday's own tree; a push that
  #       fails (a genuine divergence) is the refusal.
  # ROTATE_GIT_DIR (test hook, honoured ONLY with ROTATE_TMUX_SESSION set) points the git
  # check at a scratch repo so both branches are exercised without touching this tree.
  refuse_self() {  # $1 = the reason. Logs it, taps the seat's pane with a pointer, exits 4.
    log "REFUSED (--self): $1"
    local _ptr="ROTATION REFUSED rc 4 — this seat is STILL HERE. Read the tail of fleet/cockpit/logs/rotate_wednesday.log, fix what it names, re-run --self and read its last line."
    local _rc=0
    if [ -n "${ROTATE_TMUX_SESSION:-}" ]; then
      COCKPIT_SESSION="$ROTATE_TMUX_SESSION" bash "$HERE/cockpit.sh" say "$SEAT" "$_ptr" >>"$LOG" 2>&1 || _rc=$?
    else
      bash "$HERE/cockpit.sh" say "$SEAT" "$_ptr" >>"$LOG" 2>&1 || _rc=$?
    fi
    if [ "$_rc" -eq 0 ]; then log "refusal TAPPED at pane $PANE_ID (cockpit.sh say read it back)"
    else log "WARNING: the refusal tap FAILED (cockpit.sh say rc $_rc) — this refusal is in the log ONLY; the seat may not know"; fi
    exit 4
  }
  GIT_CHECK_DIR="$PROJECT_DIR"
  if [ -n "${ROTATE_TMUX_SESSION:-}" ] && [ -n "${ROTATE_GIT_DIR:-}" ]; then GIT_CHECK_DIR="$ROTATE_GIT_DIR"; fi
  if [ -z "${ROTATE_TMUX_SESSION:-}" ] || [ "${ROTATE_SELF_GIT_CHECK:-1}" = "1" ]; then
    git -C "$GIT_CHECK_DIR" fetch -q origin main 2>>"$LOG" || refuse_self "git fetch failed (see log)"
    LOCAL=$(git -C "$GIT_CHECK_DIR" rev-parse HEAD 2>>"$LOG"); REMOTE=$(git -C "$GIT_CHECK_DIR" rev-parse origin/main 2>>"$LOG")
    # 2026-09-13 15:5x: EQUALITY was the gate until today, and it became structurally
    # unpassable — two seats and two panel_sync loops push every minute, so origin moves
    # in the seconds between the fetch and the compare (three refusals in one rotation;
    # the guard's condition had become NORMAL, not exceptional — learnings/2026-09-10_
    # a-refusal-nobody-reads-is-indistinguishable-from-working). The property the gate
    # exists to prove is "nothing local is unpushed" = HEAD is an ANCESTOR of origin/main.
    # A remote that is AHEAD is fine (the successor pulls at boot); a HEAD with commits
    # origin lacks is the only refusal.
    if [ -z "$LOCAL" ] || ! git -C "$GIT_CHECK_DIR" merge-base --is-ancestor "$LOCAL" "$REMOTE" 2>>"$LOG"; then
      log "HEAD $LOCAL is NOT contained in origin/main $REMOTE — pushing the seat's OWN repo ONCE before refusing (2026-09-16)"
      if git -C "$GIT_CHECK_DIR" push origin main >>"$LOG" 2>&1; then
        git -C "$GIT_CHECK_DIR" fetch -q origin main 2>>"$LOG" || refuse_self "git fetch after the push failed (see log)"
        LOCAL=$(git -C "$GIT_CHECK_DIR" rev-parse HEAD 2>>"$LOG"); REMOTE=$(git -C "$GIT_CHECK_DIR" rev-parse origin/main 2>>"$LOG")
        log "push OK — re-checking containment: HEAD $LOCAL vs origin/main $REMOTE"
      else
        log "push FAILED (see log) — a genuine divergence, not a race"
      fi
      if [ -z "$LOCAL" ] || ! git -C "$GIT_CHECK_DIR" merge-base --is-ancestor "$LOCAL" "$REMOTE" 2>>"$LOG"; then
        refuse_self "HEAD $LOCAL is NOT contained in origin/main $REMOTE after one push attempt — resolve the divergence, push the handover, re-run (rhythm §3 item 3)"
      fi
    fi
    [ "$LOCAL" = "$REMOTE" ] || log "note: origin/main $REMOTE is ahead of HEAD $LOCAL (contained) — the successor pulls at boot"
    DIRTY=$(git -C "$GIT_CHECK_DIR" status --porcelain 2>>"$LOG" | grep -v '0_Brain/dashboard/data/' | grep -v '^?? .*conflict_on_' || true)
    if [ -n "$DIRTY" ]; then
      printf '%s\n' "$DIRTY" | head -10 >> "$LOG"
      refuse_self "working tree has uncommitted changes outside the dashboard data churn (listed above) — commit + push the handover first"
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
# -- D1, 2026-09-20: the checker armed 40 times against the real `fleet` and logged a
# verdict 15 times; since 2026-09-15 it was 1 in 25, and since 09-18 00:54:09 zero --
# nine armings, nine "respawned OK" lines proving the log was still being written,
# and not one verdict. Nothing anywhere said so for two days.
#
# What the measurement showed (command + output in the session report; arms below):
#   - the checker ALWAYS logs its own "armed for ..." line, so it starts every time;
#   - there is no traceback and no bash error anywhere in the log, so it is signalled,
#     not failing;
#   - a setsid+nohup child of a PLAIN pane shell survives `respawn-pane -k` of that
#     pane and reaches its verdict -- measured directly in a scratch session, so the
#     old "it dies with the pane's tty" theory is RULED OUT;
#   - under the test hooks (scratch session, trivial respawn command) the verdict rate
#     is 20/20; against the real fleet it is 15/40;
#   - and in 21 of the 25 real failures the ROTATE SCRIPT ITSELF also stopped: its own
#     post-respawn chat_reply/speak output is absent from the log too. So whatever
#     happens at `respawn-pane -k` reaches the seat's whole descendant TREE, not the
#     checker specifically -- and setsid alone does not escape it, because setsid
#     changes the session, not the parentage.
# The exact killer was NOT established. The fix therefore attacks the property that
# was measured -- descendancy -- rather than a mechanism that was guessed:
#
#   DOUBLE FORK. After os.setsid() the process forks again and the intermediate
#   parent exits, so the checker reparents to launchd (ppid 1) BEFORE the respawn
#   happens. It is then not a descendant of this script, of the seat's Claude
#   process, or of the pane -- so a tree walk cannot enumerate it, and a process-group
#   or session kill cannot reach it. `ppid == 1` is what the arm asserts.
#   (Consequence: $! is the FIRST fork, which exits immediately, so "is it alive one
#   second later" can no longer use $!. The daemon publishes its own pid to a file
#   and that is what is checked -- a pidfile that never appears is itself a warning.)
#
#   PENDING MARKER. A process-survival fix cannot be *proved* in production, so the
#   absence of a verdict is made loud instead of silent: a marker is written here,
#   before the respawn, and rotate_liveness.sh is the only thing that clears it --
#   on every path that logs a verdict. A marker left behind therefore means exactly
#   "a checker armed and never reported". doctor.sh warns on a stale one, so the
#   successor lands on it at its next boot. Two days of silence become one boot.
if [ -x "$LIVENESS" ]; then
  LIVENESS_TEST=0; LIVENESS_STUB_DIR=""
  if [ -n "${ROTATE_TMUX_SESSION:-}" ]; then LIVENESS_TEST=1; LIVENESS_STUB_DIR="${ROTATE_LIVENESS_STUB_DIR:-}"; fi
  # Both names carry BEFORE_TS, so they are unique per rotation and never need
  # clearing out of the way (2026-08-26 never-delete: nothing here removes a file).
  LIVE_PIDFILE="$STATE_DIR/rotate_liveness_${BEFORE_TS}.pid"
  PENDING_FILE="$STATE_DIR/rotate_pending_${BEFORE_TS}.txt"
  # First line shape matches ROTATE_LOSS_*.txt so doctor.sh can tell a real-fleet
  # marker from a scratch-session one with the same `session '<name>'` read.
  {
    echo "ROTATE_PENDING - $(date '+%F %T') - seat $SEAT - session '$FLEET' - coordinator $PANE_ID"
    echo "A liveness checker was armed for this rotation and has NOT logged a verdict."
    echo "before-file: $BEFORE_FILE"
    echo "checker pidfile: $LIVE_PIDFILE"
    echo "If this file is more than a few minutes old the checker died before reporting:"
    echo "the rotation went UNVERIFIED - check the fleet session and its agent panes BY HAND,"
    echo "then quarantine this file (move, never rm)."
  } > "$PENDING_FILE" 2>>"$LOG"
  LIVENESS_LAUNCH_CMD="$LAUNCH_CMD" LIVENESS_TEST="$LIVENESS_TEST" LIVENESS_STUB_DIR="$LIVENESS_STUB_DIR" \
  LIVENESS_PENDING_FILE="$PENDING_FILE" \
    python3 -c 'import os,sys
pidfile = sys.argv[1]; cmd = sys.argv[2:]
os.setsid()                       # new session, no controlling tty
if os.fork() > 0: os._exit(0)     # double fork: the child reparents to launchd (ppid 1)
open(pidfile, "w").write(str(os.getpid()))
os.execvp(cmd[0], cmd)' \
      "$LIVE_PIDFILE" nohup bash "$LIVENESS" "$FLEET" "$BEFORE_FILE" "$PANE_ID" </dev/null >>"$LOG" 2>&1 &
  wait $! 2>/dev/null || true     # reap the first fork; the daemon is not our child
  sleep 1
  LIVE_PID=""
  [ -s "$LIVE_PIDFILE" ] && LIVE_PID="$(tr -dc '0-9' < "$LIVE_PIDFILE")"
  if [ -z "$LIVE_PID" ]; then
    log "WARNING: the liveness checker wrote no pidfile ($LIVE_PIDFILE) one second after spawn - respawning UNGUARDED (see log above); the pending marker $(basename "$PENDING_FILE") makes this visible at the next boot"
  else
    LIVE_PS="$(ps -o pid=,ppid=,sess=,tty= -p "$LIVE_PID" 2>/dev/null | tr -s ' ')"
    LIVE_PPID="$(printf '%s' "$LIVE_PS" | awk '{print $2}')"
    LIVE_TTY="$(printf '%s' "$LIVE_PS" | awk '{print $4}')"
    if [ -z "$LIVE_PS" ]; then
      log "WARNING: liveness checker pid $LIVE_PID is NOT running one second after spawn - respawning UNGUARDED (see log above)"
    elif [ "$LIVE_TTY" != "??" ]; then
      log "WARNING: liveness checker pid $LIVE_PID has a tty ($LIVE_PS) - it may die with this pane; respawning anyway"
    elif [ "$LIVE_PPID" != "1" ]; then
      # The whole point of the double fork. ppid != 1 means it is still a descendant
      # of this seat and is exposed to whatever killed 25 of the last 40 checkers.
      log "WARNING: liveness checker pid $LIVE_PID did NOT reparent (ppid $LIVE_PPID, expected 1) - it is still in this seat's process tree and may die at the respawn; respawning anyway ($LIVE_PS)"
    else
      log "liveness checker spawned detached + reparented: pid/ppid/sess/tty =$LIVE_PS (fires in ~25 s; pending marker $(basename "$PENDING_FILE"))"
    fi
  fi
else
  log "WARNING: $LIVENESS missing or not executable - respawning UNGUARDED (doctor.sh should have failed on this)"
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
