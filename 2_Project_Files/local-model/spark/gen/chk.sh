#!/bin/bash
# usage: chk.sh <dir-name> ; runs lint, dry-run, control (waiting out BUSY), prints verdict lines
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
D=$B/night/briefs/$1
python3 -I $B/spark/brief_lint.py $D >/dev/null 2>$D/../.lint_$1.err; echo "lint rc=$?"
for mode in --dry-run --control; do
  for i in $(seq 1 60); do
    out=$(bash $B/spark/round.sh $D $mode 2>&1 | tail -1)
    case "$out" in *BUSY*) sleep 30;; *) break;; esac
  done
  echo "$mode: $out" | cut -c1-330
done
