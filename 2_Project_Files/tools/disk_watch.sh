#!/bin/bash
# disk_watch.sh — watch a volume's free space and tell Kam ONCE on the board when it drops
# below a floor. Built 2026-09-29 by the overnight Wednesday seat, when DevMASTER reached
# 100% (1.5 GiB free) and card wed-devmaster-full-secuura-worktree-node-modules promised
# "Wednesday tells you on the board at once if it drops below 1 GB" — a promise is not a
# mechanism (learnings/2026-08-07_a-promise-is-not-a-mechanism.md).
#
# Usage: disk_watch.sh [--volume PATH] [--floor-mib N] [--interval-s N] [--once]
#   Defaults: /Volumes/DevMASTER, 1024 MiB, 300 s. --once checks one time and exits
#   (rc 0 above the floor, rc 3 at/below it). It posts at most ONE board message per
#   crossing; it re-arms only after free space rises back above floor + 512 MiB.
# Runs from THIS seat (nohup); it dies with the machine, not with the seat. A successor
# re-arms it from the pickup. Never discards stderr.
set -u
VOL=/Volumes/DevMASTER; FLOOR=1024; INTERVAL=300; ONCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --volume) VOL="$2"; shift 2 ;;
    --floor-mib) FLOOR="$2"; shift 2 ;;
    --interval-s) INTERVAL="$2"; shift 2 ;;
    --once) ONCE=1; shift ;;
    *) echo "disk_watch: unknown arg $1" >&2; exit 2 ;;
  esac
done
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
free_mib() { df -m "$VOL" | awk 'NR==2{print $4}'; }
armed=1
while :; do
  F=$(free_mib)
  if [ -z "$F" ]; then echo "disk_watch: df returned nothing for $VOL" >&2; exit 2; fi
  echo "$(date '+%Y-%m-%d %H:%M:%S') free_mib=$F floor=$FLOOR armed=$armed"
  if [ "$F" -le "$FLOOR" ]; then
    [ "$ONCE" = 1 ] && exit 3
    if [ "$armed" = 1 ]; then
      bash "$SELF_DIR/chat_reply.sh" --project WED "DevMASTER free space has dropped to ${F} MB, below the ${FLOOR} MB floor. Git writes and installs on that drive can now fail for every seat. The card on freeing space is on your board (wed-devmaster-full-secuura-worktree-node-modules); nothing has been moved or deleted." || echo "disk_watch: board post FAILED rc=$?" >&2
      armed=0
    fi
  elif [ "$F" -gt $((FLOOR + 512)) ]; then
    armed=1
  fi
  [ "$ONCE" = 1 ] && exit 0
  sleep "$INTERVAL"
done
