#!/bin/bash
# pane_close.sh — close a cockpit pane ONLY when no surface dies with it.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=2, 2026-09-05. The 09-03
# lesson says a listener survives a pane close only if the listener AND its
# immediate parent both have tty `??`. Twice the check was run by hand and once
# the parent half was dropped: closing S33's pane killed the 3111 surface that
# read `??` on the listener alone. A two-part check done by hand loses a part,
# so the check is in the path now.
#
# HARDENED 2026-09-05 11:1x (ledger w=3 — the guard itself let two listeners die).
# Closing the retired QA pane %11 moved the listener count 24 -> 22 with NO
# refusal. Two holes, both of the check-that-cannot-fail family, in the tool
# built that morning to enforce the check:
#   (a) an UNRESOLVABLE pane name left PTTY empty and the guard passed
#       vacuously — `tmux display` printed its error, returned 0, and every
#       comparison ran against "". Now: an empty tty is a hard refusal.
#   (b) it walked ONE parent level, so a listener two or more levels below the
#       pane's shell was invisible to it. Now: the FULL ancestor chain is
#       walked to pid 1, and the process SESSION id is compared as well — which
#       is what the 09-03 lesson actually names (`ps -o sess,tty`). A session
#       match is the authoritative test; the tty walk is belt and braces.
#
# Usage: pane_close.sh <pane-id-or-name> [port ...]
#   Ports named are curled before and after.
# Exit: 0 closed · 5 REFUSED (a listener would die with the pane) · 6 REFUSED (caller's own
#       pane or the coordinator's pane) · 2 usage. Every call logged to logs/pane_close.log.
set -u
PANE="${1:?usage: pane_close.sh <pane> [port ...]}"; shift || true

PTTY="$(tmux display -p -t "$PANE" '#{pane_tty}' 2>/dev/null)"
PPID_PANE="$(tmux display -p -t "$PANE" '#{pane_pid}' 2>/dev/null)"
# (a) an unresolvable pane must NEVER reach the comparisons as an empty string.
[ -n "$PTTY" ] || { echo "pane_close: REFUSED — pane '$PANE' did not resolve to a tty (use the %ID from tmux list-panes; a name that does not resolve would make every check below vacuous)" >&2; exit 2; }
SHORT="${PTTY#/dev/}"
# SELF-GUARD (2026-09-05 13:2x): the 11:06 coordinator seat VANISHED between 11:15
# and 11:29 while it was exercising this very tool (pane_close.sh.pre-1115-sess is
# its backup; no note line, no log line survived). Cause unproven — but a kill-pane
# tool that will take its caller's own pane, or the coordinator's, is a blast
# radius nobody should have to remember. Both are refused here (rc 6), and every
# invocation now leaves a line in logs/pane_close.log so the next post-mortem has
# evidence instead of a guess.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PCLOG="$HERE/logs/pane_close.log"; mkdir -p "$HERE/logs"
TARGET_ID="$(tmux display -p -t "$PANE" '#{pane_id}' 2>/dev/null)"
TARGET_NAME="$(tmux display -p -t "$PANE" '#{@cockpit_name}' 2>/dev/null)"
echo "$(date '+%Y-%m-%d %H:%M:%S') invoked: target=$PANE id=$TARGET_ID name=${TARGET_NAME:--} tty=$PTTY caller_pane=${TMUX_PANE:--} ports=[$*]" >> "$PCLOG"
if [ -n "${TMUX_PANE:-}" ] && [ "$TARGET_ID" = "$TMUX_PANE" ]; then
  echo "pane_close: REFUSED — $PANE ($TARGET_ID) is the CALLER's own pane" >&2
  echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc6: target is the caller's own pane" >> "$PCLOG"; exit 6
fi
if [ "$TARGET_NAME" = "wednesday" ]; then
  echo "pane_close: REFUSED — $PANE ($TARGET_ID) is the coordinator's pane (@cockpit_name=wednesday); rotate it with wednesday_rotate.sh, never close it" >&2
  echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc6: target is the wednesday pane" >> "$PCLOG"; exit 6
fi
PSESS=""
[ -n "$PPID_PANE" ] && PSESS="$(ps -o sess= -p "$PPID_PANE" 2>/dev/null | tr -d ' ')"

# Walk a pid's ancestry to 1 (bounded), echoing "pid:tty" for each hop.
ancestry() {
  local p="$1" hops=0 t a
  while [ -n "$p" ] && [ "$p" != "0" ] && [ "$p" != "1" ] && [ "$hops" -lt 25 ]; do
    t="$(ps -o tty= -p "$p" 2>/dev/null | tr -d ' ')"
    echo "$p:${t:-?}"
    a="$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')"
    p="$a"; hops=$((hops+1))
  done
}

BLOCK=0
for pid in $(lsof -nP -iTCP -sTCP:LISTEN -t 2>/dev/null | sort -u); do
  lsess="$(ps -o sess= -p "$pid" 2>/dev/null | tr -d ' ')"
  chain="$(ancestry "$pid")"
  why=""
  if [ -n "$PSESS" ] && [ "$PSESS" != "0" ] && [ "$lsess" = "$PSESS" ]; then
    why="shares the pane's process session ($PSESS)"
  else
    for hop in $chain; do
      case "$hop" in
        *:"$SHORT") why="ancestor ${hop%%:*} is on the pane's tty $PTTY"; break ;;
      esac
    done
  fi
  if [ -n "$why" ]; then
    echo "pane_close: REFUSED — listener pid $pid $why and would die with the pane" >&2
    echo "pane_close:   chain: $(echo $chain | tr '\n' ' ')" >&2
    BLOCK=1
  fi
done
[ "$BLOCK" = 1 ] && { echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc5: a listener would die with $PANE" >> "$PCLOG"; exit 5; }

for p in "$@"; do echo "before: port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
BEFORE=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
tmux kill-pane -t "$PANE" || { echo "pane_close: kill-pane failed" >&2; exit 2; }
sleep 2
AFTER=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
echo "closed $PANE; listeners $BEFORE -> $AFTER"
echo "$(date '+%Y-%m-%d %H:%M:%S') CLOSED $PANE ($TARGET_ID name=${TARGET_NAME:--}); listeners $BEFORE -> $AFTER" >> "$PCLOG"
[ "$BEFORE" != "$AFTER" ] && echo "pane_close: WARNING — the listener count MOVED across this close ($BEFORE -> $AFTER) despite no refusal. Identify what died before treating this close as clean." >&2
for p in "$@"; do echo "after:  port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
exit 0
