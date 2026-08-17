#!/bin/bash
# WED-16 — 06:00 scheduled wake. Fired by launchd (com.wednesday.wake).
# Opens a full interactive Wednesday session via the normal launcher; the boot
# ritual does the rest (greeting, briefing, day plan). A marker file tells the
# launcher this is the SCHEDULED morning wake so the session knows to lead
# with the morning briefing + contemplation/consolidation slot.
#
# Guards: once per day · never before 06:00 · not after noon (launchd coalesces
# missed jobs to next Mac wake — a "morning" briefing at 22:00 would be silly).
# Portability: everything here is on-drive; only the plist is machine-local
# (PORTABILITY.md item 12, installed by install_scheduler.command).

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG_DIR="$SELF_DIR/logs"
STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/wake_$(date +%F).log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

TODAY="$(date +%F)"
HOUR="$((10#$(date +%H)))"

if [ -f "$STATE_DIR/last_wake" ] && [ "$(cat "$STATE_DIR/last_wake")" = "$TODAY" ]; then
  log "skip: already woke today"
  exit 0
fi
if [ "$HOUR" -lt 6 ]; then
  log "skip: before 06:00 (quiet hours)"
  exit 0
fi
if [ "$HOUR" -ge 12 ]; then
  log "skip: past noon — coalesced fire too late for a morning briefing"
  exit 0
fi
if [ ! -f "$PROJECT_DIR/Launch_Wednesday.command" ]; then
  log "ERROR: launcher not found at $PROJECT_DIR — drive renamed?"
  exit 1
fi

if [ "${WEDNESDAY_DRYRUN:-0}" = "1" ]; then
  log "DRYRUN: would wake into the cockpit pane (no state written)"
  exit 0
fi

# State discipline (review 2026-08-17, findings 3+4): `last_wake` is stamped
# ONLY after a wake action succeeded — stamping first meant any failure exit
# forfeited the whole day's wake to the once-per-day guard. `wake_mode` exists
# ONLY on paths that are about to boot a launcher (which consumes it), and is
# removed on their failure exits — the launcher consumes it on mere presence,
# so a stale marker turns some future evening launch into a "morning wake".
wake_done() { echo "$TODAY" > "$STATE_DIR/last_wake"; }

# ── Wake INTO THE COCKPIT, never into a Terminal window (2026-08-17) ──
# The old `open -a Terminal Launch_Wednesday.command` spawned a coordinator
# OUTSIDE the fleet tmux session: no pane, no monitor row, no watcher
# coverage, nothing that ever reaps it. Found 2026-08-17: FOUR of them alive
# at once (Fri/Sat/Sun/Mon wakes), each a full coordinator — the state Kam's
# one-session rule exists to prevent, leaked by our own scheduler daily.
# A coordinator with no pane is unobservable; the cockpit pane is the ONLY
# place a coordinator may boot. Three cases, one invariant (at most one):
#   1. no fleet session          -> cockpit.sh up (wednesday boots in pane 0)
#   2. wednesday pane idle/dead  -> respawn the launcher in that pane
#   3. live claude in the pane   -> DO NOT spawn or kill; deliver the morning
#      wake as a pane tap (a session going quiet is indistinguishable from
#      working — killing on a guess is destructive; the 05:30 shift change
#      already asked it to wrap). Tap honours the Kam-typing guard
#      (ledger w=3, 2026-08-12: a blind tap SUBMITS his half-typed text).
# Test hooks (never set in production): WAKE_TMUX_SESSION alternate session,
# WAKE_LAUNCH_CMD alternate pane command.
#
# launchd runs this with PATH=/usr/bin:/bin:/usr/sbin:/sbin (the plist sets no
# EnvironmentVariables), and case 1 may START the tmux server — every pane
# would then inherit that stripped env and the launcher's final `exec claude`
# dies command-not-found while the wake logs success (review 2026-08-17,
# finding 2; the old `open -a Terminal` path got a login-shell env for free).
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
FLEET="${WAKE_TMUX_SESSION:-fleet}"
TEST_MODE=0; [ -n "${WAKE_TMUX_SESSION:-}" ] && TEST_MODE=1
# TEST-MODE GUARD (2026-08-17, same hour as the near-miss it prevents): if the
# session is overridden for a test but the launch command is not, the fallback
# would be the REAL launcher — and this script's job is respawning panes, so
# that default boots a REAL second coordinator into a test session. It
# happened, once, for 55 seconds. A test hook must never default to the
# production action: both overrides or neither.
if [ -n "${WAKE_TMUX_SESSION:-}" ] && [ -z "${WAKE_LAUNCH_CMD:-}" ]; then
  log "REFUSED: WAKE_TMUX_SESSION set without WAKE_LAUNCH_CMD — test mode may not default to the real launcher"
  exit 2
fi
LAUNCH_CMD="${WAKE_LAUNCH_CMD:-bash \"$PROJECT_DIR/Launch_Wednesday.command\"}"
COCKPIT="$PROJECT_DIR/2_Project_Files/fleet/cockpit/cockpit.sh"

# All -t targets use tmux exact-match syntax (=name): without it tmux
# prefix-matches when no exact session exists, so a leftover 'fleet-test'
# could satisfy 'fleet' while the real fleet is never created (finding 9).
if ! "$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null; then
  if [ "$TEST_MODE" = "1" ]; then
    # cockpit.sh hardcodes SESSION=fleet, so this branch in test mode would
    # act on the REAL fleet regardless of WAKE_TMUX_SESSION (finding 1).
    log "REFUSED (test mode): session '$FLEET' absent and cockpit.sh only knows the real fleet — create the test session yourself"
    exit 2
  fi
  log "no fleet session — creating cockpit (wednesday boots in pane 0)"
  echo "morning" > "$STATE_DIR/wake_mode"     # consumed (deleted) by the launcher
  if OUT=$("$COCKPIT" up 2>&1); then
    log "cockpit up: $OUT"; wake_done; exit 0
  else
    rm -f "$STATE_DIR/wake_mode"
    log "ERROR: cockpit up failed (day NOT stamped, a later fire may retry): $OUT"; exit 1
  fi
fi

# -s = all panes in the session, no window-index assumption: '$FLEET:0' broke
# under base-index 1 and made 'window missing' look like 'pane missing' (finding 10).
WROW=$("$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{@cockpit_name}|#{pane_id}|#{pane_dead}|#{pane_tty}' 2>/dev/null | awk -F'|' '$1=="wednesday"' | head -1)
if [ -z "$WROW" ]; then
  if [ "$TEST_MODE" = "1" ]; then
    log "REFUSED (test mode): no wednesday pane in '$FLEET' and cockpit.sh add only knows the real fleet — add the pane yourself"
    exit 2
  fi
  log "fleet session up but no wednesday pane — adding it"
  echo "morning" > "$STATE_DIR/wake_mode"
  if OUT=$("$COCKPIT" add wednesday "$LAUNCH_CMD" 2>&1); then
    case "$OUT" in
      *"already present"*)
        # Our pane scan and cockpit's disagree — instruments in conflict is a
        # failure, not a success (the silent-skip half of finding 10).
        rm -f "$STATE_DIR/wake_mode"
        log "ERROR: my pane scan found no wednesday pane but cockpit.sh says 'already present' — instrument disagreement, NO wake delivered, day not stamped"; exit 1 ;;
    esac
    log "added: $OUT"; wake_done; exit 0
  else
    rm -f "$STATE_DIR/wake_mode"
    log "ERROR: add failed (day NOT stamped): $OUT"; exit 1
  fi
fi

PANE_ID=$(echo "$WROW" | cut -d'|' -f2)
PANE_DEAD=$(echo "$WROW" | cut -d'|' -f3)
PANE_TTY=$(echo "$WROW" | cut -d'|' -f4)

# Census of the pane's tty (pane_current_command lies — it reports claude's
# shell children — so ask ps). Three verdicts, not two (findings 6+7):
#   claude anchored as the command word  -> live coordinator (case 3)
#   only bare shells / empty             -> idle, safe to respawn (case 2)
#   anything else (launcher mid-boot, git, vim, less…) -> BUSY: do not kill.
# The anchored match replaces grep '[c]laude', which matched the substring
# anywhere in any argv (`tail -f ~/.claude/...` read as a live coordinator).
PROCS=""
[ "$PANE_DEAD" != "1" ] && [ -n "$PANE_TTY" ] && PROCS=$(ps -t "${PANE_TTY#/dev/}" -o command= 2>/dev/null)
VERDICT="idle"
if [ -n "$PROCS" ]; then
  if printf '%s\n' "$PROCS" | grep -qE '^([^ ]*/)?claude( |$)'; then
    VERDICT="claude"
  elif printf '%s\n' "$PROCS" | grep -qvE '^-?(bash|zsh|sh)$'; then
    VERDICT="busy"
  fi
elif [ "$PANE_DEAD" != "1" ]; then
  # ps returned nothing for a live pane — seen 2026-08-17 (a real process was
  # invisible to ps -t in an unattached session). Ambiguous; proceed as idle
  # but say so, because a silent guess is how instruments lie.
  log "NOTE: ps returned no processes for $PANE_TTY though the pane is live — treating as idle on pane_dead=0"
fi

case "$VERDICT" in
  busy)
    rm -f "$STATE_DIR/wake_mode"
    log "WAKE NOT DELIVERED: wednesday pane $PANE_ID busy with non-claude work ($(printf '%s' "$PROCS" | head -1 | cut -c1-80)) — not killing it (day not stamped; a later fire may retry)"
    exit 1 ;;
  idle)
    log "wednesday pane $PANE_ID has no live coordinator — respawning launcher in place"
    echo "morning" > "$STATE_DIR/wake_mode"
    # Same pane contract as cockpit.sh add_pane: without the trailing
    # inspection shell the pane CLOSES when the coordinator exits, taking the
    # scrollback and the fleet's left column with it (finding 8).
    if "$TMUX_BIN" respawn-pane -k -t "$PANE_ID" "$LAUNCH_CMD; echo; echo '[cockpit] wednesday exited — pane stays for inspection'; exec bash"; then
      log "respawned wednesday pane $PANE_ID (morning wake)"; wake_done; exit 0
    else
      rm -f "$STATE_DIR/wake_mode"
      log "ERROR: respawn-pane failed (day NOT stamped)"; exit 1
    fi ;;
esac

# Case 3: a coordinator is already live. One-coordinator rule: tap, don't spawn.
# The day is stamped whatever the tap outcome — the wake's objective (a live
# morning coordinator) is met, and a re-fire would only re-tap.
MSG="[06:00 wake] Morning wake fired and found you live — you ARE the morning session. Run the morning ritual (briefing, sweep, autostart) now; if you are yesterday's wrapped session, hand over per working-rhythm instead."
PROMPT_LINE=$("$TMUX_BIN" capture-pane -t "$PANE_ID" -p -e 2>/dev/null | grep -a "$(printf '\342\235\257')" | tail -1)
if [ -z "$PROMPT_LINE" ]; then
  # No prompt visible at all (modal dialog open, prompt scrolled away): typing
  # blind would land keystrokes somewhere unknowable — the w=3 tap regression
  # in a new costume. Log-only is the safe failure (finding 5, half-fix; the
  # full fix is a single-pane mode on pane_prompt_check.sh — WED ticket).
  log "WAKE LOG-ONLY: coordinator live in $PANE_ID but no prompt line is visible — not typing blind"
else
  PTXT=$(printf '%s\n' "$PROMPT_LINE" | \
    LC_ALL=C perl -pe 's/\x1b\[2m.*?(?=\x1b|$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//' 2>/dev/null | tr -d '[:space:]')
  if [ -n "$PTXT" ]; then
    log "WAKE LOG-ONLY: coordinator live in $PANE_ID but its prompt is occupied (Kam-typing guard) — no tap sent"
  else
    "$TMUX_BIN" send-keys -t "$PANE_ID" -l "$MSG" && "$TMUX_BIN" send-keys -t "$PANE_ID" Enter \
      && log "coordinator already live in $PANE_ID — morning wake delivered as a tap, no second session spawned" \
      || log "ERROR: tap failed — coordinator live in $PANE_ID, wake NOT delivered"
  fi
fi
wake_done
