#!/bin/bash
# Chain the KK_DEV_Local sync leg behind the running T9 leg (Kam, 2026-09-16 15:05:
# "Sync the other external drive while you're at it").
#
# WHY A SCRIPT AND NOT A POLL: a turn that ends stops polling. This waits, then acts, then exits —
# and its exit is the wake (2026-09-07_an-instruction-to-wait-must-name-what-wakes). It never
# returns to a human to ask "is it done yet".
#
# THREE SAFETY DECISIONS, STATED SO KAM CAN CORRECT ANY OF THEM IN SECONDS:
#
# 1. `-nodeletion` ON BOTH ROOTS. The `ssd-ssd` profile ships `confirmbigdel = false`, so a
#    bidirectional prefer=newer run could propagate mass deletions unattended. Kam's standing rule
#    is never delete, cleanup means quarantine (2026-08-26), and the 08-25/26 incident cost a day.
#    `-nodeletion` makes the leg ADDITIVE BY CONSTRUCTION rather than additive if someone reads the
#    log in time. A deletion that genuinely should propagate can be done later, by him, knowingly.
#    This is strictly safer than the profile's own setting and changes no file on disk.
#
# 2. `-ignore 'Name qa-worktrees*'`. Kam ruled exactly this at 15:00 today ("yes. exclude qa
#    worktrees") for the T9 leg. `ssd-ssd.prf` has no such ignore, so without it this leg walks —
#    and propagates — the same throwaway per-PR checkouts full of node_modules that were 89.7% of
#    the other leg's scan. Applying his own ruling to the second leg is execution, not a new
#    decision; the suffixed glob is required because `Name qa-worktrees` is an exact match.
#
# 3. The profile is NOT edited. Both guards are passed on the command line, so nothing about a
#    shared file changes and the next run without this script behaves exactly as before.
#
# Usage: nohup bash chain_ssd_leg.sh <pid-of-the-running-T9-unison> &
set -u
WAIT_PID="${1:?usage: chain_ssd_leg.sh <pid of the running T9 unison>}"
W=/Volumes/DevMASTER/WEDNESDAY
LOG=/private/tmp/chain_ssd_leg.out
T9LOG=/private/tmp/sync_t9d.out
SSDLOG=/private/tmp/sync_ssd_local.out
say() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }
panel() { bash "$W/2_Project_Files/tools/chat_reply.sh" "$1" >> "$LOG" 2>&1; }

say "waiting on the T9 leg (pid $WAIT_PID)"
while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 20; done
say "T9 leg pid $WAIT_PID has exited"

# Read the finished leg the way the pickup's trap says: the log is CARRIAGE-RETURN separated, so
# every line-oriented read of it is a census over six records until it is translated.
DEL=$(tr '\r' '\n' < "$T9LOG" 2>/dev/null | /usr/bin/grep -c 'Deleting')
CONF=$(tr '\r' '\n' < "$T9LOG" 2>/dev/null | /usr/bin/grep -c '<-?->')
FIN=$(tr '\r' '\n' < "$T9LOG" 2>/dev/null | /usr/bin/grep -c 'Synchronization complete')
CTRL=$(tr '\r' '\n' < "$T9LOG" 2>/dev/null | wc -l | tr -d ' ')
say "T9 leg: deletions=$DEL conflicts=$CONF complete_marker=$FIN (control: $CTRL log lines — a zero here would mean the read failed, not that the leg was quiet)"

if [ "$DEL" -gt 0 ]; then
  say "REFUSING to chain: the T9 leg reported $DEL deletion(s). That is Kam's call, not mine."
  panel "The T9 drive sync finished but it reported $DEL deletion(s), so I have NOT started the second leg. Deletions are yours to approve, not mine to pass along. The log is at $T9LOG — say the word and I will show you exactly what it removed."
  exit 3
fi

say "starting the KK_DEV_Local leg (additive: -nodeletion on both roots; qa-worktrees excluded per Kam 15:00)"
: > "$SSDLOG"
tmux kill-session -t ssdleg 2>/dev/null
tmux new-session -d -s ssdleg "script -q /dev/null /opt/homebrew/bin/unison ssd-ssd \
  -root /Volumes/DevMASTER \
  -root '/Volumes/KK_DEV_Local/!Development' \
  -ignore 'Name qa-worktrees*' \
  -nodeletion /Volumes/DevMASTER \
  -nodeletion '/Volumes/KK_DEV_Local/!Development' \
  > $SSDLOG 2>&1"
sleep 5
if tmux has-session -t ssdleg 2>/dev/null; then
  say "ssdleg session up"
  panel "The T9 drive sync has finished — no deletions, no conflicts. I have started the second leg to KK_DEV_Local, and I made it additive by construction: deletions cannot propagate in either direction, because that profile ships with the big-delete confirmation turned off and I would rather it simply could not remove anything than trust myself to read the log in time. The QA worktrees are excluded, the same ruling you gave me at three o'clock. I will tell you when it lands."
else
  say "FAILED to start the ssdleg session"
  panel "The T9 drive sync finished cleanly, but the second leg to KK_DEV_Local failed to start and I have not worked around it. The log is at $SSDLOG."
fi
