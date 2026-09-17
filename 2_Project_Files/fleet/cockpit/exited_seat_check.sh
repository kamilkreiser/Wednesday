#!/bin/bash
# exited_seat_check.sh — has the Claude session in this coordinator pane EXITED, leaving a shell?
#   usage: exited_seat_check.sh <tmux pane id>     rc 0 = EXITED, rc 1 = not (alive, or cannot tell)
#
# WHY (2026-09-17, Tuesday on the Mac mini): her session ended ~09:05 and the pane fell to the
# `exec bash` the cockpit leaves behind. The DEAD leg (dead_banner_check.sh) only recognises
# Claude's "Context limit reached" banner, which an exited session never shows — so the
# watcher kept TYPING wake lines into bash for ~1.5 h (`syntax error near unexpected token`),
# nothing alarmed, and Kam found it from a screenshot. (The 2026-09-02 WED-140 gap: "a seat
# that dies leaves a bare shell, not the literal — the DEAD leg must recognise that shape too".)
#
# THE PREDICATE — EXITED only when BOTH independent sources agree (a guard refuses on agreement
# of two things that both KNOW, never on one representation — 2026-09-09 guard lesson):
#   1. PANE TEXT: the cockpit's own marker `exited — pane stays for inspection` is on screen.
#      cockpit.sh (new-session) and wednesday_rotate.sh (respawn) print it exactly when the seat
#      command returns, then `exec bash`.
#   2. PROCESS TREE: no process named `claude` (or a node running claude-code) descends from the
#      pane's pid. A live seat that merely PRINTS the marker (a diagnosis, a cat'd log) still has
#      its claude process — so the text alone can never kill a live seat.
# Anything it cannot read (no pane, no pid, ps failure) answers rc 1: cannot tell = not exited.
# Red-proof: fleet/tests/exited_seat_arms.sh (scratch tmux session only).
set -u
PANE="${1:?usage: exited_seat_check.sh <pane-id>}"
TMUX_BIN="${TMUX_BIN:-tmux}"

txt="$("$TMUX_BIN" capture-pane -p -t "$PANE" -S -60 2>/dev/null)" || exit 1
printf '%s\n' "$txt" | /usr/bin/grep -F -q 'exited — pane stays for inspection' || exit 1

ppid_root="$("$TMUX_BIN" display-message -p -t "$PANE" '#{pane_pid}' 2>/dev/null)"
case "$ppid_root" in ''|*[!0-9]*) exit 1 ;; esac

# Walk every descendant of the pane's pid; any claude process means the session is alive.
tree="$(ps -A -o pid= -o ppid= -o comm= -o args= 2>/dev/null)" || exit 1
printf '%s\n' "$tree" | ROOT="$ppid_root" python3 -c '
import os, sys
root = os.environ["ROOT"]
kids = {}; info = {}
for line in sys.stdin:
    parts = line.split(None, 3)
    if len(parts) < 3: continue
    pid, ppid, comm = parts[0], parts[1], parts[2]
    args = parts[3] if len(parts) > 3 else ""
    kids.setdefault(ppid, []).append(pid); info[pid] = (comm, args)
def is_claude(pid):
    comm, args = info.get(pid, ("", ""))
    return os.path.basename(comm) == "claude" or "claude-code" in args or args.split()[:1] == ["claude"]
if is_claude(root): sys.exit(3)
stack = [root]; seen = set()
while stack:
    p = stack.pop()
    if p in seen: continue
    seen.add(p)
    for c in kids.get(p, []):
        if is_claude(c):
            sys.exit(3)   # a live claude under the pane
        stack.append(c)
sys.exit(0)
'
rc=$?
[ "$rc" -eq 0 ] && exit 0
exit 1
