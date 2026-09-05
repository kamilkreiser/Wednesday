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
# Usage: pane_close.sh <pane-id-or-name> [port ...]
#   Ports named are curled before and after. Every TCP listener on the box whose
#   tty OR whose parent's tty equals the pane's tty is a blocker.
# Exit: 0 closed · 5 REFUSED (a listener or its parent would die) · 2 usage.
set -u
PANE="${1:?usage: pane_close.sh <pane> [port ...]}"; shift || true
PTTY="$(tmux display -p -t "$PANE" '#{pane_tty}' 2>/dev/null)" || { echo "pane_close: no such pane $PANE" >&2; exit 2; }
SHORT="${PTTY#/dev/}"
BLOCK=0
for pid in $(lsof -nP -iTCP -sTCP:LISTEN -t 2>/dev/null | sort -u); do
  ltty="$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')"
  ppid="$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')"
  ptty="$(ps -o tty= -p "${ppid:-1}" 2>/dev/null | tr -d ' ')"
  if [ "$ltty" = "$SHORT" ] || [ "$ptty" = "$SHORT" ]; then
    echo "pane_close: REFUSED — listener pid $pid (tty ${ltty:-?}) parent $ppid (tty ${ptty:-?}) shares $PTTY and would die with the pane" >&2
    BLOCK=1
  fi
done
[ "$BLOCK" = 1 ] && exit 5
for p in "$@"; do echo "before: port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
BEFORE=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
tmux kill-pane -t "$PANE" || { echo "pane_close: kill-pane failed" >&2; exit 2; }
sleep 2
AFTER=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
echo "closed $PANE; listeners $BEFORE -> $AFTER"
for p in "$@"; do echo "after:  port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
exit 0
