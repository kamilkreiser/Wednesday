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
#                                 instructions still go by mail for the record).
#                                 VERIFIES delivery by reading the prompt back:
#                                 exit 3 = prompt occupied by typed text (refused,
#                                 nothing sent) · exit 2 = still at the prompt
#                                 after two Enters (NOT delivered) · exit 0 only
#                                 when the text left the prompt.
#   cockpit.sh rotate <Client/Project> [--timeout-min N]
#                                 working-rhythm §3 session rotation: tap the
#                                 pane with the wrap instruction, wait for its
#                                 "Session wrap" mail on the bus (default 10
#                                 min), then kill + relaunch fresh from
#                                 launchers.conf. Timeout = force path: kill
#                                 anyway, LOUD notice, exit 2 — never silent.
#                                 'rotate wednesday' is refused: the
#                                 coordinator rotates via her own ritual.
#   cockpit.sh down               kill the whole fleet session (asks first via -f)
#
# cockpit.conf format (same dir):  <pane-name>|<command to run>
# Lines starting with # ignored. Wednesday's pane is defined there too.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# WEDNESDAY root — conf commands reference it as the literal token
# ${PROJECT_DIR} so the cockpit is volume-portable (PORTABILITY 3: the drive
# may mount under any name; hardcoded /Volumes/... paths broke on KK_DEV_Local
# 2026-08-05).
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CONF="$SCRIPT_DIR/cockpit.conf"
# COCKPIT_SESSION: test hook ONLY — points every subcommand at another tmux
# session (a scratch one) so `say` can be exercised without touching a live
# agent. One variable, applied to everything; default is the real fleet.
SESSION="${COCKPIT_SESSION:-fleet}"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

die() { echo "cockpit: $*" >&2; exit 1; }
[ -x "$TMUX_BIN" ] || die "tmux not found (PORTABILITY: brew install tmux)"

# Prompt readers (same extraction as pane_prompt_check.sh: strip SGR, take the
# last ❯ line that is not Claude Code's own chrome, drop the U+00A0 after ❯).
prompt_text() { # $1 = pane id → text at the input prompt ("" = clear)
  local line cand text=""
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    cand="$(printf '%s' "$line" | LC_ALL=C sed 's/\x1b\[[0-9;]*m//g' \
            | LC_ALL=C sed 's/^.*❯//' | LC_ALL=C sed 's/^\xc2\xa0*//' | LC_ALL=C sed 's/^ *//')"
    case "$cand" in "Press up to edit queued messages"*|"Try "*|"for shortcuts"*) continue ;; esac
    text="$cand"
  done < <("$TMUX_BIN" capture-pane -t "$1" -p -e 2>/dev/null | LC_ALL=C grep -a '❯' || true)
  printf '%s' "$text"
}
prompt_is_ghost() { # $1 = pane id → 0 if the last prompt line is dim (Claude's suggestion)
  local raw
  raw="$("$TMUX_BIN" capture-pane -t "$1" -p -e 2>/dev/null | LC_ALL=C grep -a '❯' | LC_ALL=C grep -av 'Press up to edit queued\|Try \|for shortcuts' | LC_ALL=C tail -1 || true)"
  printf '%s' "$raw" | LC_ALL=C grep -q $'\x1b\\[2m'
}
pane_has_queue() { # $1 = pane id → 0 if Claude Code shows a queued message
  "$TMUX_BIN" capture-pane -t "$1" -p 2>/dev/null | LC_ALL=C grep -aq 'Press up to edit queued messages'
}

pane_exists() { # by @cockpit_name
  "$TMUX_BIN" list-panes -t "$SESSION" -F '#{@cockpit_name}' 2>/dev/null | grep -qx "$1"
}

apply_layout() {
  # THE default view (Kam, 2026-08-05): Wednesday = left column (main pane,
  # 45%), every agent + the monitor = stacked rows on the right. Enforced,
  # not assumed: main-vertical makes pane index 0 the left main pane, so if
  # the wednesday pane isn't index 0 (pane churn), swap it there first.
  local wed_id first_id
  wed_id=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_id}|#{@cockpit_name}' | awk -F'|' '$2=="wednesday"{print $1}' | head -1)
  first_id=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_index}|#{pane_id}' | awk -F'|' '$1==0{print $2}')
  if [ -n "$wed_id" ] && [ -n "$first_id" ] && [ "$wed_id" != "$first_id" ]; then
    "$TMUX_BIN" swap-pane -d -s "$wed_id" -t "$first_id"
  fi
  "$TMUX_BIN" set-option -t "$SESSION:0" main-pane-width "45%" 2>/dev/null
  "$TMUX_BIN" select-layout -t "$SESSION:0" main-vertical >/dev/null
  # Liveness borders (Kam, 2026-08-05: silence must not look like death) —
  # each pane border carries its name + a clock that ticks every 5s, so a
  # frozen VIEW is instantly distinguishable from a quiet AGENT.
  "$TMUX_BIN" set-option -t "$SESSION:0" pane-border-status top 2>/dev/null
  "$TMUX_BIN" set-option -t "$SESSION:0" pane-border-format ' #{?#{@cockpit_name},#{@cockpit_name},-} · #{?#{pane_dead},DEAD,live} #(date +%H:%M:%S) ' 2>/dev/null
  "$TMUX_BIN" set-option -t "$SESSION" status-interval 5 2>/dev/null
}

add_pane() { # name, cmd
  local name="$1" cmd="$2"
  if pane_exists "$name"; then echo "pane '$name' already present — skip"; return 0; fi
  local pane_id
  pane_id=$("$TMUX_BIN" split-window -t "$SESSION:0" -P -F '#{pane_id}' -d "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash")
  "$TMUX_BIN" set-option -p -t "$pane_id" @cockpit_name "$name"
  apply_layout
  echo "pane '$name' added ($pane_id)"
}

rotate_wrap_mail_ts() { # <name> <start-ts-utc-seconds> — print wrap-mail ts + exit 0 when a
  # NEW "[<name> -> Wednesday] Session wrap" mail (timestamp > start) is on the
  # bus inbox wednesday-agent@; exit 1 otherwise. Test hook: if
  # COCKPIT_ROTATE_MAIL_CHECK is set it is run instead, as: <cmd> <name> <start-ts>.
  if [ -n "${COCKPIT_ROTATE_MAIL_CHECK:-}" ]; then
    "$COCKPIT_ROTATE_MAIL_CHECK" "$1" "$2"
    return $?
  fi
  # key stays inside the subshell; never echoed (workspace hard rule #3)
  ( set -a; . "$PROJECT_DIR/4_Credentials/.env" 2>/dev/null; set +a
    curl -s -m 15 "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=20" \
      -H "Authorization: Bearer ${AGENTMAIL_API_KEY:-}" ) | \
  ROTATE_NAME="$1" ROTATE_START="$2" python3 -c '
import json, os, sys
name = os.environ["ROTATE_NAME"]; start = os.environ["ROTATE_START"]
want = "[%s -> Wednesday] Session wrap" % name
try:
    ms = json.load(sys.stdin).get("messages", [])
except Exception:
    sys.exit(1)
hits = [str(m.get("timestamp",""))[:19] for m in ms
        if str(m.get("subject","")).startswith(want)]
hits = [t for t in hits if t and t > start]
if hits:
    print(max(hits)); sys.exit(0)
sys.exit(1)'
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
        cmd="${cmd//'${PROJECT_DIR}'/$PROJECT_DIR}"
        if [ $first -eq 1 ]; then
          "$TMUX_BIN" new-session -d -s "$SESSION" -n main "$cmd; echo; echo '[cockpit] $name exited — pane stays for inspection'; exec bash"
          pid=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{pane_id}' | head -1)
          "$TMUX_BIN" set-option -p -t "$pid" @cockpit_name "$name"
          first=0
        else
          add_pane "$name" "$cmd"
        fi
      done < "$CONF"
      apply_layout
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
    if [ ! -f "$LPATH" ]; then
      # Travel-drive fallback (2026-08-25): the registry pins DevMASTER paths;
      # when Wednesday runs from another drive carrying the same tree (the
      # KK_DEV_Local travel copy), retry with THIS drive's root swapped in.
      DRIVE_ROOT="${SCRIPT_DIR%/WEDNESDAY/*}"
      ALT="$DRIVE_ROOT${LPATH#/Volumes/DevMASTER}"
      if [ "$ALT" != "$LPATH" ] && [ -f "$ALT" ]; then
        echo "launcher volume not mounted — using this drive's copy: $ALT" >&2
        LPATH="$ALT"
      else
        die "registered launcher missing on disk: $LPATH (registry stale — fix launchers.conf)"
      fi
    fi
    if [ "$1" = resolve ]; then echo "would launch pane '$2': bash \"$LPATH\""; exit 0; fi
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session — run 'cockpit.sh up' first"
    add_pane "$2" "bash \"$LPATH\""
    ;;
  layout)
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session"
    apply_layout
    echo "layout applied: wednesday left column (45%), agents+monitor rows right"
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
    # DELIVERY IS VERIFIED, NOT ASSUMED (ledger w=4, 2026-08-28). This used to
    # send text + Enter and print "sent" — send-keys rc=0 echoed as delivery, a
    # check that cannot fail. Twice that morning the Enter was swallowed (Claude
    # Code drops the first Enter after a Ctrl-C) and the pointer sat TYPED-UNSENT
    # at the agent's prompt; Secuura s83 idled 41 minutes on a confirmed plan.
    # Now: refuse an occupied prompt (someone's line is there — Kam typing, or an
    # earlier undelivered tap) · send text · Enter · read the prompt back · if the
    # text is still there, Enter ONCE more · still there → exit 2, loudly.
    [ $# -eq 3 ] || die "usage: cockpit.sh say <pane-name> <text>"
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session"
    PANE=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}' | awk -F'|' -v n="$2" '$1==n{print $2}')
    [ -n "$PANE" ] || die "no pane named '$2'"
    PRE="$(prompt_text "$PANE")"
    if [ -n "$PRE" ] && ! prompt_is_ghost "$PANE"; then
      echo "cockpit: REFUSED — '$2' prompt is occupied by typed text (not sent): $PRE" >&2
      exit 3
    fi
    "$TMUX_BIN" send-keys -t "$PANE" -l "$3"
    "$TMUX_BIN" send-keys -t "$PANE" Enter
    KEY="$(printf '%s' "$3" | cut -c1-30)"
    tries=1
    while :; do
      sleep 2
      # A QUEUED message (agent mid-turn) is still rendered as "❯ <text>" above
      # the "Press up to edit queued messages" footer — so check the queue
      # marker BEFORE reading "text still visible" as "not submitted". Found
      # live 2026-08-28 11:29: the first real busy tap was reported NOT
      # DELIVERED while the pane showed it queued.
      if pane_has_queue "$PANE"; then echo "delivered to '$2' (queued behind a running turn)"; exit 0; fi
      NOW_TXT="$(prompt_text "$PANE")"
      case "$NOW_TXT" in
        "$KEY"*) ;;                       # still at the prompt
        *) echo "delivered to '$2' (prompt clear)"; exit 0 ;;
      esac
      if [ $tries -ge 2 ]; then
        echo "cockpit: NOT DELIVERED to '$2' after 2 Enters — text still at the prompt: $NOW_TXT" >&2
        exit 2
      fi
      tries=$((tries+1))
      echo "cockpit: text still at '$2' prompt after Enter — re-sending Enter once (swallowed-Enter trap)" >&2
      "$TMUX_BIN" send-keys -t "$PANE" Enter   # once, never a third
    done
    ;;
  rotate)
    # Session rotation (working-rhythm §3, built 2026-08-10): tap → wrap mail
    # → kill → relaunch. The unit of continuity is the DISK; a restart is as
    # safe as the wrap ritual is enforced. Force path only on deadline, NEVER
    # silent. Test hooks (disposable-pane tests only; unset in production):
    #   COCKPIT_LAUNCHERS_CONF   alternate registry file
    #   COCKPIT_ROTATE_MAIL_CHECK  replacement for the bus poll (see function)
    #   COCKPIT_ROTATE_POLL_S    poll interval seconds (default 30)
    shift
    [ $# -ge 1 ] || die "usage: cockpit.sh rotate <Client/Project> [--timeout-min N]"
    NAME="$1"; shift
    TIMEOUT_MIN=10
    while [ $# -gt 0 ]; do
      case "$1" in
        --timeout-min)
          [ $# -ge 2 ] || die "--timeout-min needs a value (minutes)"
          TIMEOUT_MIN="$2"; shift 2 ;;
        *) die "unknown rotate flag: $1" ;;
      esac
    done
    [ "$TIMEOUT_MIN" -ge 1 ] 2>/dev/null || die "--timeout-min must be a positive integer (minutes)"
    if [ "$NAME" = "wednesday" ]; then
      die "refusing to rotate 'wednesday' — the coordinator rotates via her own checkpoint ritual, tapped from outside (working-rhythm §3); rotate is for agent panes only"
    fi
    "$TMUX_BIN" has-session -t "$SESSION" 2>/dev/null || die "no fleet session — nothing to rotate"
    REG="${COCKPIT_LAUNCHERS_CONF:-$SCRIPT_DIR/launchers.conf}"
    [ -f "$REG" ] || die "no launchers registry at $REG"
    LPATH=$(awk -F'|' -v n="$NAME" '$1==n{print $2}' "$REG" | head -1)
    [ -n "$LPATH" ] || die "'$NAME' not in $REG — rotate needs a registered relaunch path (no relaunch path = no rotation, use say+manual instead)"
    [ -f "$LPATH" ] || die "registered launcher missing on disk: $LPATH (registry stale — fix it before rotating)"
    PANE=$("$TMUX_BIN" list-panes -t "$SESSION:0" -F '#{@cockpit_name}|#{pane_id}' | awk -F'|' -v n="$NAME" '$1==n{print $2}' | head -1)
    [ -n "$PANE" ] || die "no pane named '$NAME'"
    mkdir -p "$SCRIPT_DIR/logs"
    RLOG="$SCRIPT_DIR/logs/rotate.log"
    START_TS=$(date -u +%Y-%m-%dT%H:%M:%S)
    POLL="${COCKPIT_ROTATE_POLL_S:-30}"
    # (a) the tap — same text/mechanism as the daily-proven 05:30 shift change
    WRAP_MSG="[Wednesday, session rotation] Please wrap up and finish this session now: complete or safely checkpoint the current step, then run your end-of-session ritual (commit+push, history entry, wrap email to wednesday-agent@agentmail.to). Do not start new work — a fresh session relaunches when your wrap mail lands."
    "$TMUX_BIN" send-keys -t "$PANE" -l "$WRAP_MSG"
    "$TMUX_BIN" send-keys -t "$PANE" Enter
    echo "$(date '+%F %T') rotate '$NAME' ($PANE): tapped, waiting ${TIMEOUT_MIN}m for wrap mail (poll ${POLL}s)" >> "$RLOG"
    echo "rotate: tapped '$NAME' ($PANE); waiting up to ${TIMEOUT_MIN}m for its Session wrap mail (poll ${POLL}s)"
    # (b) poll the bus for a wrap mail NEWER than the rotate start
    WRAPPED=""
    DEADLINE=$((SECONDS + TIMEOUT_MIN * 60))
    while [ "$SECONDS" -lt "$DEADLINE" ]; do
      sleep "$POLL"
      if TS=$(rotate_wrap_mail_ts "$NAME" "$START_TS"); then
        WRAPPED="$TS"
        break
      fi
    done
    # (c)/(d) kill either way — then relaunch fresh via the registered launcher
    "$TMUX_BIN" kill-pane -t "$PANE"
    add_pane "$NAME" "bash \"$LPATH\""
    if [ -n "$WRAPPED" ]; then
      echo "$(date '+%F %T') rotate '$NAME': wrap mail at $WRAPPED UTC — clean rotation" >> "$RLOG"
      echo "rotate: '$NAME' wrapped (mail at $WRAPPED UTC) — old pane killed, fresh session launched"
    else
      {
        echo "!!!! ROTATE FORCED WITHOUT WRAP !!!! pane '$NAME' produced NO Session wrap mail within ${TIMEOUT_MIN}m of the tap (start $START_TS UTC)."
        echo "!!!! An unwrapped session was force-rotated: its work may be uncommitted and its record incomplete."
        echo "!!!! Check NOW: that project's repo status + 5_Project_History/history.md, the bus for a late wrap mail, today's daily note. Logged to $RLOG for the close bell."
      } | tee -a "$RLOG" >&2
      exit 2
    fi
    ;;
  down)
    "$TMUX_BIN" kill-session -t "$SESSION" 2>/dev/null && echo "fleet session killed" || echo "no fleet session"
    ;;
  *)
    die "usage: cockpit.sh up|launch|resolve|add|layout|status|say|rotate|down"
    ;;
esac
