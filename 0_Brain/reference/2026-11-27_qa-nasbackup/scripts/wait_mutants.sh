#!/bin/bash
# helper: block until both mutant runs have printed their summary line (or ~9.5 minutes pass)
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-nasbackup
for i in $(seq 1 57); do
  if /usr/bin/grep -q '^MY MUTANTS:' "$O/scripts/out/D_my_mutants.out" && /usr/bin/grep -q 'mutants caught' "$O/scripts/out/D_seat_mutants_rerun.out"; then break; fi
  sleep 10
done
tail -n +4 "$O/scripts/out/D_my_mutants.out" | cut -c1-170; echo ---; tail -n 12 "$O/scripts/out/D_seat_mutants_rerun.out" | cut -c1-120
