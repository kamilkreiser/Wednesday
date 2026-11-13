#!/bin/bash
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; W=$F/s78_work2
for T in merged after; do
  test -d $W/$T/.git || { git -C $W/$T init -q; git -C $W/$T add -A >/dev/null 2>&1; }
  echo "== $T tracked locks: $(git -C $W/$T ls-files '*package-lock.json' | wc -l)"
  npm --prefix $W/$T/Blockchain/Dev run audit:gate > $F/s78_gate_$T.out 2>&1; echo "gate $T rc=$?"
  npm --prefix $W/$T/Blockchain/Dev run audit:locks > $F/s78_locks_$T.out 2>&1; echo "locks $T rc=$?"
done
