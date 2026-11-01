#!/bin/bash
# arm_wake_watch.sh — the ARMING half of wake_watch (built 2026-08-10).
#
# Why this exists (ledger w=5, learnings/2026-08-10_a-ritual-nothing-triggers-
# is-not-a-ritual + 2026-08-09_an-enforcement-you-must-arm-is-not-one):
# wake_watch.sh was hand-armed three times and dead within a day each time.
# A safeguard that runs beside the work needs something that arms it (this
# script, called by Launch_Wednesday.command on every boot) and something
# that checks it is armed (doctor.sh's existing hard-fail). Hand-arming is
# now only for recovery, never the plan.
#
# What it does:
#   - Idempotent: if a runner is already alive, exits 0 saying so. Safe to
#     call on every launch.
#   - Starts a detached runner loop that re-arms wake_watch.sh forever:
#       baseline = now (UTC, minute precision — matches wake_watch's compare)
#       stable_n = 3 when agent panes are live, 9999 (mail-only) when not —
#                  recomputed at every re-arm, so a wrapped-idle pane never
#                  false-fires all morning (2026-08-09 false positive).
#   - On a WAKE (mail or pane): delivers it through the PROVEN mechanism —
#     tmux send-keys into the wednesday pane, exactly like shift_change.sh.
#     No wednesday pane (launcher-only session, cockpit down): the WAKE line
#     is in the log and the runner re-arms; doctor/next boot reads the log.
#   - On the 4h no-fire timeout: re-arms silently with a fresh baseline.
#
# Usage: arm_wake_watch.sh            (arm if not armed)
#        arm_wake_watch.sh status     (report, exit 0 armed / 1 not)
#        arm_wake_watch.sh cycle      (re-arm NOW: kill the CHILD only, never the runner)
#        arm_wake_watch.sh disarm     (stop runner + watcher)
#        arm_wake_watch.sh taptest <pane-id> <msg>
#                                     (TEST ONLY, 2026-10-06: run the runner's own
#                                     deliver_wake ONCE against <pane-id>. Requires
#                                     WAKE_WATCH_STATE_DIR so a test can never write
#                                     the live state dir; point PATH at a tmux wrapper
#                                     with its own -L socket so it can never reach the
#                                     live server. Never touches PIDFILE or the runner.)
#
# Env knobs read by the RUNNING runner (defaults = the live behaviour):
#   WAKE_HOLD_TRIES (20)  WAKE_HOLD_SLEEP (30s)  WAKE_SUBMIT_SETTLE (3s)
#   WAKE_ESCALATE_AFTER (2 held cycles)  WAKE_ESCALATE_EVERY (1800s per pane)
#   WAKE_ESCALATE_CMD (2_Project_Files/tools/chat_reply.sh — tests stub it)

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$HERE/../../.." && pwd)"
[ -f "$HERE/seat_resolve.sh" ] || { echo "arm_wake_watch: $HERE/seat_resolve.sh missing — the runner cannot resolve the coordinator seat/pane" >&2; exit 2; }
STATE_DIR="$HERE/state"
if [ "${1:-}" = "taptest" ]; then
  STATE_DIR="${WAKE_WATCH_STATE_DIR:-}"
  [ -n "$STATE_DIR" ] || { echo "taptest REFUSED: set WAKE_WATCH_STATE_DIR to a scratch dir (never the live state dir)" >&2; exit 2; }
  [ "$STATE_DIR" != "$HERE/state" ] || { echo "taptest REFUSED: WAKE_WATCH_STATE_DIR is the live state dir" >&2; exit 2; }
fi
LOG_DIR="$HERE/logs"
PIDFILE="$STATE_DIR/wake_watch_runner.pid"
LOG="$LOG_DIR/wake_watch_runner.log"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
mkdir -p "$STATE_DIR" "$LOG_DIR"

# ── deliver_wake: the tap, its guards and its off-pane escalation (2026-10-06) ──
# Lifted out of RUNNER into its own string so the runner and the taptest
# subcommand execute the SAME bytes. Same rule as RUNNER: single-quoted, so no
# apostrophes anywhere inside it, comments included.
TAPFN='
  wake_log() { echo "$(date "+%Y-%m-%d %H:%M:%S") $*"; }
  # Prompt line of <pane>: SGR-2 ghost spans + colour codes + NBSP stripped,
  # whitespace removed. Ghost text never survives this read, so nothing below
  # can ever mistake a dim suggestion for text to submit.
  wake_read_prompt() {
    '"$TMUX_BIN"' capture-pane -t "$1" -p -e 2>/dev/null | grep -a "$(printf "\342\235\257")" | tail -1 | \
      LC_ALL=C perl -pe "s/\x1b\[2m.*?(?=\x1b|\$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//" 2>/dev/null | tr -d "[:space:]"
  }
  # OWN-TAP TEST (2026-10-06, ledger: Wednesday deaf ~8 h). The 09-15 test was
  # ONLY "substring of the last tap": at 00:57 the read-back found text that
  # failed it, logged STUCK - the next cycle submits it, and the next cycle then
  # failed the same test and held every wake for 8 h (own-stuck-tap submits in
  # the whole log: zero). Every tap this runner sends begins with the literal
  # [wake_watch] prefix, so that prefix IS the discriminator; the substring test
  # stays as a second arm. Text that passes neither (Kam typing) is never submitted.
  wake_is_own_tap() { # <stripped prompt text> <stripped tap text>
    case "$1" in "[wake_watch]"*) return 0 ;; esac
    if [ -n "$2" ] && [ "${#1}" -ge 12 ]; then case "$2" in *"$1"*) return 0 ;; esac; fi
    return 1
  }
  wake_hold_file() { echo "'"$STATE_DIR"'/wake_hold_${SEAT}_${1#%}.txt"; }
  wake_hold_note() { # <pane>: count ONE more held wake on this pane
    local f s n; f=$(wake_hold_file "$1"); s=""; n=""
    [ -s "$f" ] && read -r s n < "$f"
    case "$s" in ""|*[!0-9]*) s=$(date +%s); n=0 ;; esac
    case "$n" in ""|*[!0-9]*) n=0 ;; esac
    echo "$s $((n + 1))" > "$f"
  }
  wake_hold_clear() { # <pane>: prompt is clear again - close the hold record
    local f s n; f=$(wake_hold_file "$1"); s=""; n=""
    [ -s "$f" ] || return 0
    read -r s n < "$f"; : > "$f"
    wake_log "hold on $SEAT pane $1 CLEARED (${n:-?} wake(s) had been held since $(date -r "${s:-0}" "+%H:%M" 2>/dev/null))"
  }
  # ESCALATE OFF-PANE (2026-10-06): the alarm channel used to be the blocked
  # pane itself plus a log nobody reads. Post ONE line to Kam panel through
  # chat_reply.sh, at most once per WAKE_ESCALATE_EVERY per blocked pane.
  # Panel only - no speech here, so there is no quiet-hours question.
  wake_escalate() { # <pane> <reason>
    local pane="$1" why="$2" ts now last s n txt out rc cmd
    ts="'"$STATE_DIR"'/wake_escalated_${SEAT}_${pane#%}.ts"; now=$(date +%s); last=0
    [ -s "$ts" ] && last=$(cat "$ts" 2>/dev/null)
    case "$last" in ""|*[!0-9]*) last=0 ;; esac
    if [ $((now - last)) -lt "${WAKE_ESCALATE_EVERY:-1800}" ]; then
      wake_log "ESCALATION SUPPRESSED ($SEAT pane $pane, $why): last panel post $(( (now - last) / 60 )) min ago, limit $(( ${WAKE_ESCALATE_EVERY:-1800} / 60 )) min"
      return 0
    fi
    s=""; n=""; [ -s "$(wake_hold_file "$pane")" ] && read -r s n < "$(wake_hold_file "$pane")"
    case "$s" in ""|*[!0-9]*) s=$now ;; esac
    txt="Seat $SEAT: the coordinator prompt (pane $pane) is blocked by text the wake watcher will not overwrite; ${n:-1} wake(s) held since $(date -r "$s" "+%H:%M"). Check the $SEAT pane. (Repeats at most every $(( ${WAKE_ESCALATE_EVERY:-1800} / 60 )) min while blocked.)"
    cmd="${WAKE_ESCALATE_CMD:-'"$PROJECT_DIR"'/2_Project_Files/tools/chat_reply.sh}"
    out=$(WED_AGENT="$SEAT" CHAT_ALLOW_REPEAT=1 "$cmd" --project WED "$txt" 2>&1); rc=$?
    if [ "$rc" -eq 0 ]; then
      echo "$now" > "$ts"
      wake_log "ESCALATED off-pane to Kam panel ($SEAT pane $pane, $why): $txt"
    else
      # retry in 5 min, not every 30 s: a failing poster must not flood the log
      echo "$((now - ${WAKE_ESCALATE_EVERY:-1800} + 300))" > "$ts"
      wake_log "ESCALATION FAILED rc=$rc ($SEAT pane $pane, $why) via $cmd - retry in 5 min: $(printf "%s" "$out" | tail -2 | tr "\n" " ")"
    fi
  }
  deliver_wake() { # <pane> <msg>
    WPANE="$1"; MSG="$2"
    # KAM-TYPING GUARD (2026-08-12): the tap presses Enter in the
    # wednesday pane — if Kam is mid-typing there, it SUBMITS his
    # half-written message (happened twice today, both truncated at the
    # wake text). Before tapping: read the prompt line, strip SGR-2
    # ghost spans + colour codes + NBSP; if any real text sits after
    # the prompt char, wait 30s and re-check, up to 20 tries (10 min).
    # Still occupied -> log-only wake; losing immediacy beats
    # destroying his input. (Ghost text does NOT block the tap - it is
    # not his.)
    # OWN-STUCK-TAP DISCRIMINATOR (2026-09-15, ledger w=2 - the night Ornith lost):
    # the 22:14 band tap went into a BUSY pane and its Enter never submitted;
    # the guard below then read the runner OWN unsent tap as Kam typing and
    # held every wake for seven hours (LOG-ONLY x17). Text at the prompt that
    # is OUR OWN TAP (wake_is_own_tap: [wake_watch] prefix, or a substring of
    # the last tap) is not Kam typing: submit it with Enter (a late wake beats a
    # lost one) and READ BACK. At most 3 Enters per wake - if a line that looks
    # like ours will not clear, it is not the input box and it is held (and
    # escalated) like anything else. And every tap is READ BACK: prompt clear =
    # delivered; text still there = Enter again, up to 3 times, then logged
    # STUCK so the next cycle can see and submit it.
    # ESCALATION (2026-10-06): after WAKE_ESCALATE_AFTER consecutive held
    # cycles, or at LOG-ONLY, whichever is first, raise it off-pane.
    LASTTAP=""; [ -f "'"$STATE_DIR"'/last_tap_$SEAT.txt" ] && LASTTAP=$(tr -d "[:space:]" < "'"$STATE_DIR"'/last_tap_$SEAT.txt")
    TRIES=0; SUBMITS=0; HELD=0; ESCALATED=0
    while [ "$TRIES" -lt "${WAKE_HOLD_TRIES:-20}" ]; do
      PTXT=$(wake_read_prompt "$WPANE")
      [ -z "$PTXT" ] && break
      if [ "$SUBMITS" -lt 3 ] && wake_is_own_tap "$PTXT" "$LASTTAP"; then
        SUBMITS=$((SUBMITS + 1))
        '"$TMUX_BIN"' send-keys -t "$WPANE" Enter
        wake_log "SUBMIT own stuck tap at $SEAT prompt ($WPANE, ${#PTXT} chars, begins $(printf "%s" "$PTXT" | cut -c1-24)) - Enter sent ($SUBMITS/3)"
        sleep "${WAKE_SUBMIT_SETTLE:-3}"
        PTXT=$(wake_read_prompt "$WPANE")
        if [ -z "$PTXT" ]; then
          wake_log "SUBMIT read-back: $SEAT prompt clear - own stuck tap delivered"
          break
        fi
        wake_log "SUBMIT read-back: text still at $SEAT prompt after Enter ($SUBMITS/3)"
        TRIES=$((TRIES + 1)); continue
      fi
      TRIES=$((TRIES + 1)); HELD=$((HELD + 1))
      [ "$HELD" -eq 1 ] && wake_hold_note "$WPANE"
      echo "$(date "+%Y-%m-%d %H:%M:%S") tap held - text at $SEAT prompt (try $TRIES/${WAKE_HOLD_TRIES:-20})"
      if [ "$ESCALATED" -eq 0 ] && [ "$HELD" -ge "${WAKE_ESCALATE_AFTER:-2}" ]; then
        ESCALATED=1; wake_escalate "$WPANE" "held $HELD consecutive cycles"
      fi
      sleep "${WAKE_HOLD_SLEEP:-30}"
    done
    if [ -n "$PTXT" ]; then
      echo "$(date "+%Y-%m-%d %H:%M:%S") WAKE LOG-ONLY (prompt still occupied after $TRIES tries): $MSG"
      if [ "$ESCALATED" -eq 0 ]; then
        [ "$HELD" -eq 0 ] && wake_hold_note "$WPANE"
        ESCALATED=1; wake_escalate "$WPANE" "LOG-ONLY"
      fi
    else
      wake_hold_clear "$WPANE"
      printf "%s" "$MSG" > "'"$STATE_DIR"'/last_tap_$SEAT.txt"
      if '"$TMUX_BIN"' send-keys -t "$WPANE" -l "$MSG" && '"$TMUX_BIN"' send-keys -t "$WPANE" Enter; then
        MSGN=$(printf "%s" "$MSG" | tr -d "[:space:]"); RB=0
        while [ "$RB" -lt 3 ]; do
          sleep 2
          PTXT=$(wake_read_prompt "$WPANE")
          [ -z "$PTXT" ] && break
          if wake_is_own_tap "$PTXT" "$MSGN"; then
            RB=$((RB + 1)); '"$TMUX_BIN"' send-keys -t "$WPANE" Enter
            echo "$(date "+%Y-%m-%d %H:%M:%S") tap text still at $SEAT prompt - Enter re-sent ($RB/3)"
          else
            break
          fi
        done
        if [ -z "$PTXT" ]; then
          echo "$(date "+%Y-%m-%d %H:%M:%S") tapped $SEAT pane $WPANE (read back: prompt clear)"
        else
          echo "$(date "+%Y-%m-%d %H:%M:%S") tapped $SEAT pane $WPANE but text remains at the prompt after read-back - STUCK; the next cycle submits it if it begins [wake_watch], else holds and escalates"
        fi
      else
        echo "$(date "+%Y-%m-%d %H:%M:%S") FAILED to tap $SEAT pane $WPANE"
      fi
    fi
  }
'

# The runner body. Assigned here, ABOVE the subcommand case (2026-10-06), so that
# check/taptest can syntax-check it without ever reaching the arm path pkill.
RUNNER='
  # Baseline discipline (fixed 2026-08-10 after a QUESTION mail fell into the
  # fire->re-arm gap, ledger w=2 on the 08-04 blanket-markseen root cause):
  # the baseline NEVER advances to "now" — it advances ONLY to the timestamp
  # of a mail/chat event that actually fired a wake (so I was provably tapped
  # about everything up to it). A refire on an already-read mail costs one
  # tap; a swallowed mail costs a 15-minute fallback. Always err toward refire.
  BASELINE=$(date -u +%Y-%m-%dT%H:%M)   # first arm only: session boot has read everything
  # SEAT + coordinator pane (2026-09-13, Tuesday 19:1x finding): this runner used
  # to HARDCODE the literal wednesday for the DEAD case and the tap target and
  # handed --dead no WED_AGENT, so a dead Tuesday seat could never be respawned.
  # The ONE resolver (seat_resolve.sh) now decides: WED_AGENT, else the tree name;
  # coord_pane_id accepts the seat name OR the legacy wednesday pane on this seat
  # own tree. On the Studio SEAT resolves to wednesday - byte-identical in effect.
  . "'"$HERE"'"/seat_resolve.sh || { echo "$(date "+%Y-%m-%d %H:%M:%S") FATAL: seat_resolve.sh missing - runner exiting"; exit 2; }
  seat_resolve "'"$PROJECT_DIR"'"
  echo "$(date "+%Y-%m-%d %H:%M:%S") runner seat=$SEAT (tree seat $TREE_SEAT)"
  while true; do
    # agent panes = everything except the coordinator (by seat name AND the legacy name) and the monitor
    AGENTS=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}" 2>/dev/null | grep -vE "^($SEAT|wednesday|fleet-monitor)$" | grep -c . || true)
    if [ "${AGENTS:-0}" -gt 0 ] 2>/dev/null; then N=3; else N=9999; fi
    echo "$(date "+%Y-%m-%d %H:%M:%S") armed: baseline=$BASELINE stable_n=$N agents=$AGENTS"
    OUT=$("'"$HERE"'"/wake_watch.sh "$BASELINE" "$N" 60 2>&1)   # quoted 2026-09-23: the laptop tree lives under a path with spaces
    echo "$(date "+%Y-%m-%d %H:%M:%S") $OUT"
    NEWTS=$(printf "%s" "$OUT" | sed -nE "s/.*(new mail at|message from Kam at) ([0-9T:-]+).*/\2/p" | tail -1)
    [ -n "$NEWTS" ] && BASELINE="$NEWTS"
    # ctx wakes (working-rhythm §2, 2026-08-10) pass through EXACTLY like pane
    # fires: tap, no baseline movement (the sed above only matches mail/chat).
    case "$OUT" in
      # message-from-Kam added 2026-08-17: the chat leg wake wording never
      # matched this case, so chat wakes advanced the baseline and SILENTLY
      # skipped the tap (the 12:08 chat message sat unseen ~10 min). Family:
      # enforcement-scoped-narrower, ledger 2026-08-12 w=3 -> now w=4. NOTE:
      # this whole runner body is a single-quoted string - no apostrophes in
      # comments here, ever; one broke the arm path on the first fix attempt.
      # subagent-wait bound added 2026-09-16 (wake_watch.sh leg b). Placed ABOVE the idle
      # line, which its wording also matches so that runners started before today still tap it.
      *"subagents with no change"*) MSG="[wake_watch] $OUT — read the pane and its subagent transcripts: which one is still running, is it progressing or queued on a lock. Ack it with wake_ack.sh if it is fine." ;;
      *"new mail"*|*"idle at prompt"*|*"message from Kam"*) MSG="[wake_watch] $OUT — check the fleet inbox / pane now." ;;
      *"ctx at"*) MSG="[wake_watch] $OUT — apply rhythm §2 now; rotate at the task boundary via cockpit.sh rotate <Client/Project> (wednesday pane: own checkpoint ritual)." ;;
      # content-FROZEN added 2026-09-01 (WED-136, ledger w=5 enforcement-scoped-narrower):
      # the FROZEN-BUSY leg (wake_watch.sh, 2026-08-23) fired 14 times on an idle
      # Secuura pane with a permanent sentinel shell and every fire fell through
      # this case un-tapped. Same defect as the 08-17 chat-leg row: leg widened,
      # consumer not. Any new wake shape gets a line HERE the day it is added.
      *"content FROZEN"*) MSG="[wake_watch] $OUT — turn likely ended with work or mail pending: check the inbox FIRST, then the transcript mtime, then the detector at the pane; tap or score as the state requires." ;;
      # DEAD coordinator (2026-09-02): do NOT tap a pane that cannot read a tap.
      # Respawn it through wednesday_rotate.sh --dead (which re-checks the
      # literal before killing anything) and give the boot ten minutes.
      # 2026-09-13: matched on the wake shape, not the literal wednesday (the
      # message names $SEAT), and WED_AGENT=$SEAT is passed EXPLICITLY so the
      # rotate script respawns THIS seat with THIS seat launcher.
      *"DEAD"*"respawn required"*)
        echo "$(date "+%Y-%m-%d %H:%M:%S") DEAD coordinator ($SEAT) detected — respawning via WED_AGENT=$SEAT wednesday_rotate.sh --dead"
        if WED_AGENT="$SEAT" "'"$HERE"'"/wednesday_rotate.sh --dead >> "'"$LOG"'" 2>&1; then
          echo "$(date "+%Y-%m-%d %H:%M:%S") respawn issued; waiting 600s for the boot before re-arming"; sleep 600
        else
          echo "$(date "+%Y-%m-%d %H:%M:%S") respawn REFUSED or FAILED (rc=$?) — see rotate_wednesday.log; will re-check next cycle"; sleep 120
        fi
        MSG="" ;;
      *) echo "$(date "+%Y-%m-%d %H:%M:%S") WAKE UNMATCHED by tap case (add a pattern): $OUT"; MSG="" ;;
    esac
    if [ -n "$MSG" ]; then
        # Tap target = the resolved coordinator pane id (seat name, else the guarded legacy name) - 2026-09-13
        WPANE=$(coord_pane_id fleet:0 2>/dev/null || true)
        if [ -n "$WPANE" ]; then
          # Guard, own-stuck-tap submit, tap, read-back and off-pane escalation:
          # deliver_wake in TAPFN above (2026-10-06; same bytes the taptest runs).
          deliver_wake "$WPANE" "$MSG"
        else
          echo "$(date "+%Y-%m-%d %H:%M:%S") no $SEAT coordinator pane (nor an adoptable legacy wednesday pane) — WAKE logged only"
        fi
        sleep 120   # give the session time to read before re-arming
    fi
  done
'

runner_alive() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
}

case "${1:-arm}" in
  status)
    if runner_alive; then echo "armed (runner pid $(cat "$PIDFILE"))"; exit 0
    else echo "NOT armed"; exit 1; fi
    ;;
  disarm)
    if runner_alive; then kill "$(cat "$PIDFILE")" 2>/dev/null; fi
    pkill -f 'wake_watch\.sh' 2>/dev/null
    rm -f "$PIDFILE"
    echo "disarmed"
    exit 0
    ;;
  cycle)
    # Force the runner to re-arm NOW, so stable_n/agents are recomputed after a
    # pane is added or closed — WITHOUT touching the runner itself.
    #
    # Why this is a subcommand and not a command I type (ledger w=3, 2026-08-13):
    # three times in one day I cycled by hand with a grep on 'wake_watch.sh' and
    # a positional head -1, and the RUNNER matched too — its bash -c body quotes
    # the child's path. Twice that killed the watcher I was trying to refresh.
    # The discriminator is not greppable by eye but it is exact: the runner's pid
    # is in PIDFILE; every other match is a child. Encoding it is the fix,
    # because the selector lesson had already been written and still did not
    # prevent the third occurrence.
    runner_alive || { echo "NOT armed — nothing to cycle (run 'arm' first)" >&2; exit 1; }
    RPID="$(cat "$PIDFILE")"
    [ -x "$HERE/wake_watch.sh" ] || { echo "cycle ABORTED — $HERE/wake_watch.sh not found or not executable" >&2; exit 2; }
    KILLED=0
    while IFS= read -r line; do
      cpid="${line%% *}"
      [ "$cpid" = "$RPID" ] && continue          # never the runner
      kill "$cpid" 2>/dev/null && KILLED=$((KILLED + 1))
    done <<EOF
$(ps -eo pid=,command= | awk -v s="$HERE/wake_watch.sh" '$2 == s || $3 == s {print $1" "$0}')
EOF
    if [ "$KILLED" -eq 0 ]; then
      echo "runner $RPID alive; no child to cycle (it will re-arm on its own timer)"
    else
      echo "cycled: killed $KILLED child process(es); runner $RPID untouched, re-arms within ~60s"
    fi
    exit 0
    ;;
  check)
    # Parse the exact body the runner would run, and nothing else.
    if bash -n -c "$TAPFN$RUNNER"; then echo "runner body OK (bash -n)"; exit 0; else echo "runner body FAILS bash -n"; exit 1; fi
    ;;
  taptest)
    # TEST ONLY - see the header. Same TAPFN bytes as the runner, one delivery.
    [ $# -eq 3 ] || { echo "usage: WAKE_WATCH_STATE_DIR=<scratch> arm_wake_watch.sh taptest <pane-id> <msg>" >&2; exit 2; }
    bash -n -c "$TAPFN$RUNNER" || { echo "taptest: runner body fails bash -n" >&2; exit 1; }
    SEAT="${WED_AGENT:-wednesday}" bash -c "$TAPFN"'
      deliver_wake "$1" "$2"' taptest "$2" "$3"
    exit $?
    ;;
  arm) ;;
  *) echo "usage: arm_wake_watch.sh [arm|status|cycle|disarm|check|taptest]"; exit 2 ;;
esac

if runner_alive; then
  echo "already armed (runner pid $(cat "$PIDFILE"))"
  exit 0
fi
# A stray watcher without a runner (old hand-armed instance) would double-fire
# once a runner starts — fold it in rather than run two.
pkill -f 'wake_watch\.sh' 2>/dev/null && sleep 1

# Syntax gate (2026-10-06): an apostrophe in a comment once broke the arm path;
# refuse to launch a body bash cannot parse instead of launching a dead runner.
bash -n -c "$TAPFN$RUNNER" 2>>"$LOG" || { echo "ARM REFUSED - runner body fails bash -n (see $LOG)"; exit 2; }
nohup bash -c "$TAPFN$RUNNER" >> "$LOG" 2>&1 &
echo "$!" > "$PIDFILE"
sleep 1
if runner_alive; then
  echo "armed (runner pid $(cat "$PIDFILE"), log $LOG)"
  exit 0
else
  echo "ARM FAILED — see $LOG"
  tail -5 "$LOG" 2>/dev/null
  exit 1
fi
