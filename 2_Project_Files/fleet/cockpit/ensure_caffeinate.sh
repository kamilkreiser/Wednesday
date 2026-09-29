#!/bin/bash
# ensure_caffeinate.sh — on a LAPTOP, make sure a DETACHED `caffeinate -dims` with at least MIN_LEFT seconds left is running.
# Called by cockpit.sh after it adds a pane (add / launch), so every seat launch carries its own sleep guard.
#
# WHY (Friday ledger, w=2 → mechanism due): the laptop SLEPT with build seats live on 2026-09-25 (two turns cut, ~40 min lost),
# and the rule "arm caffeinate in the same action as the launch" lived in a lesson about drive pointers, so a launch matched
# nothing. It recurred on 2026-09-25 19:37 (the handover said "armed"; the process had died with the old seat's pane) and on
# 2026-09-29 (armed 08:44 for 6 h, expired ~14:44 with seats live; a gate verdict waited ~2 h). A rule a seat must remember
# is not a mechanism (2026-08-09).
#
# What it does: laptop only (a Mac with an internal battery; a Studio or mini never sleeps this way). For every running
# `caffeinate` with -d AND -i AND -s in its flags, remaining = its -t value minus its elapsed time (no -t = never expires).
# If the best remaining is < MIN_LEFT (default 3 h), it starts `caffeinate -dims -t DURATION` (default 6 h) in its OWN
# session (python double fork + setsid), so a pane close cannot SIGHUP it (2026-09-03: ppid 1 is not detachment; the
# session/tty are). Prints one line saying what it found and did. Never fails the caller: always exits 0.
#
# Test hooks: ENSURE_CAFF_PS_FILE (canned `ps -Ao pid=,etime=,args=` output), ENSURE_CAFF_LAPTOP=1|0 (skip the battery
# probe), ENSURE_CAFF_DRY=1 (say what would be armed, arm nothing). Arms: 2_Project_Files/tests/ensure_caffeinate_arms.sh
MIN_LEFT="${ENSURE_CAFF_MIN_LEFT:-10800}"; DURATION="${ENSURE_CAFF_DURATION:-21600}"

laptop="${ENSURE_CAFF_LAPTOP:-}"
if [ -z "$laptop" ]; then
  if [ "$(uname)" = Darwin ] && pmset -g batt 2>/dev/null | /usr/bin/grep -q -i 'InternalBattery'; then laptop=1; else laptop=0; fi
fi
[ "$laptop" = 1 ] || { echo "ensure_caffeinate: not a laptop (no internal battery): nothing to do"; exit 0; }

if [ -n "${ENSURE_CAFF_PS_FILE:-}" ]; then PS_OUT="$(cat "$ENSURE_CAFF_PS_FILE")"; else PS_OUT="$(ps -Ao pid=,etime=,args= 2>&1)"; fi
best="$(printf '%s\n' "$PS_OUT" | python3 -c '
import sys, re
def secs(e):  # [[dd-]hh:]mm:ss
    d = 0
    if "-" in e: dd, e = e.split("-", 1); d = int(dd)
    p = [int(x) for x in e.split(":")]
    while len(p) < 3: p.insert(0, 0)
    return d*86400 + p[0]*3600 + p[1]*60 + p[2]
best = -1; bpid = ""
for line in sys.stdin:
    f = line.split(None, 2)
    if len(f) < 3 or not re.match(r"(\S*/)?caffeinate(\s|$)", f[2]): continue
    args = f[2].split()[1:]
    flags = "".join(a[1:] for a in args if a.startswith("-") and not a.startswith("-t"))
    if not all(c in flags for c in "dis"): continue
    t = None
    for i, a in enumerate(args):
        if a == "-t" and i + 1 < len(args): t = int(args[i+1])
        elif a.startswith("-t") and a[2:].isdigit(): t = int(a[2:])
    try: left = 10**9 if t is None else t - secs(f[1])
    except ValueError: continue
    if left > best: best, bpid = left, f[0]
print(best, bpid)
')"
left="${best%% *}"; pid="${best##* }"
if [ "${left:--1}" -ge "$MIN_LEFT" ] 2>/dev/null; then
  echo "ensure_caffeinate: OK — caffeinate -dims pid $pid has $((left/60)) min left (>= $((MIN_LEFT/60)))"; exit 0
fi
why="none running"; [ "${left:--1}" -ge 0 ] 2>/dev/null && why="best has only $((left/60)) min left (pid $pid)"
if [ "${ENSURE_CAFF_DRY:-0}" = 1 ]; then echo "ensure_caffeinate: WOULD ARM caffeinate -dims -t $DURATION ($why)"; exit 0; fi
python3 -c '
import os, sys
if os.fork(): sys.exit(0)
os.setsid()
if os.fork(): sys.exit(0)
fd = os.open(os.devnull, os.O_RDWR)
for i in (0, 1, 2): os.dup2(fd, i)
os.execvp("caffeinate", ["caffeinate", "-dims", "-t", sys.argv[1]])
' "$DURATION" || { echo "ensure_caffeinate: ⚠ FAILED to arm caffeinate ($why) — arm it by hand: caffeinate -dims -t $DURATION &"; exit 0; }
new="$(pgrep -n -f "caffeinate -dims -t $DURATION")"
echo "ensure_caffeinate: ARMED caffeinate -dims -t $DURATION, pid ${new:-?} ($why); detached: $(ps -o sess=,tty= -p "${new:-0}" 2>/dev/null | tr -s ' ')"
exit 0
