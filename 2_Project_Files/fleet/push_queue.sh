#!/bin/bash
# push_queue.sh — first-come order for the Secuura push-window lock.
#
# WHY THIS EXISTS: the push lock is a bare `mkdir`, so whichever waiter polls
# first after a release wins. On 2026-10-27 Seat X 1st lost the handoff three
# times in a row (W -> Z -> AA) and its 20-minute waiter exited with no push;
# Seat Y 1st waited 40+ minutes while later seats went ahead. This adds ORDER
# beside the lock. The lock itself is unchanged: a seat still takes it only by
# its own `mkdir`, and still releases holder-then-rmdir.
#
# Usage (QUEUE defaults to the Secuura worktrees dir; override with PUSH_QUEUE_DIR):
#   push_queue.sh join  <seat-label>   # prints your ticket path; join ONCE per push
#   push_queue.sh turn  <ticket-path>  # rc 0 = you are first among LIVE tickets; rc 1 = wait
#   push_queue.sh leave <ticket-path>  # remove YOUR ticket (after release, or on giving up)
#   push_queue.sh list                 # show the queue, oldest first, LIVE/DEAD per ticket
#
# The loop a seat runs:
#   T=$(push_queue.sh join "Seat X 1st")
#   until push_queue.sh turn "$T"; do sleep 3; done
#   ...acquire the lock by your own mkdir (as before), push, ls-remote, release...
#   push_queue.sh leave "$T"
#
# A ticket whose recorded pid is no longer alive is SKIPPED by `turn` (not
# removed — nobody deletes another seat's ticket). Record the pid of the
# process that will stay alive for the whole push (your waiter/driver), via
# PUSH_QUEUE_PID; default is this script's parent.
#
# Exit codes: 0 ok / your turn · 1 not your turn · 2 usage or filesystem error.

set -u
Q="${PUSH_QUEUE_DIR:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-queue}"

die() { echo "push_queue: $*" >&2; exit 2; }

alive() { kill -0 "$1" 2>/dev/null; }

# Tickets are named <epoch-seconds>.<nanos>-<pid>; sort -n on the name is arrival order.
tickets() { ls -1 "$Q" 2>/dev/null | grep -E '^[0-9]+\.[0-9]+-[0-9]+$' | sort -t- -k1,1n; }

case "${1:-}" in
  join)
    [ $# -eq 2 ] || die "usage: join <seat-label>"
    mkdir -p "$Q" || die "cannot create $Q"
    pid="${PUSH_QUEUE_PID:-$PPID}"
    alive "$pid" || die "pid $pid is not alive; set PUSH_QUEUE_PID to your waiter's pid"
    now=$(python3 -c 'import time;print("%.9f"%time.time())') || die "python3 clock failed"
    t="$Q/$now-$pid"
    printf '%s | pid %s | joined %s\n' "$2" "$pid" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$t" || die "cannot write $t"
    echo "$t"
    ;;
  turn)
    [ $# -eq 2 ] || die "usage: turn <ticket-path>"
    [ -f "$2" ] || die "ticket $2 does not exist (joined? left already?)"
    mine=$(basename "$2")
    for n in $(tickets); do
      p="${n##*-}"
      if [ "$n" = "$mine" ]; then exit 0; fi
      alive "$p" && exit 1      # an older LIVE ticket is ahead of you
    done
    die "ticket $mine not found in the listing of $Q"
    ;;
  leave)
    [ $# -eq 2 ] || die "usage: leave <ticket-path>"
    [ -f "$2" ] || die "ticket $2 does not exist"
    case "$2" in "$Q"/*) ;; *) die "refusing: $2 is not inside $Q" ;; esac
    rm "$2"; rc=$?
    echo "leave rc=$rc"
    [ $rc -eq 0 ] || exit 2
    ;;
  list)
    for n in $(tickets); do
      p="${n##*-}"; st=DEAD; alive "$p" && st=LIVE
      printf '%s  %s  %s\n' "$st" "$n" "$(cat "$Q/$n" 2>&1)"
    done
    ;;
  *) die "usage: push_queue.sh join|turn|leave|list ..." ;;
esac
