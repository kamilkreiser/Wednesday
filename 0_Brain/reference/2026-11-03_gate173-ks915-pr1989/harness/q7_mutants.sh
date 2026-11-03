#!/bin/bash
# Run the PR suite against every mutant in mut/ (3 at a time); one line per mutant in results/q7_raw.txt.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989
one() { local f="$1" id; id=$(basename "$f" .sh)
  bash $W/harness/q0_suite.sh "mut-$id" "$f" > $W/runs/q7/$id.bin 2>&1
  local r; r=$(grep -E '^Results' $W/runs/q7/$id.bin | tail -1)
  printf '%s\t%s\t%s\thex48_in_output=%s\n' "$id" "$( [[ "$r" == *" 0 failed"* ]] && echo SURVIVED || echo KILLED)" "$r" "$(grep -cE '[0-9a-f]{48}' $W/runs/q7/$id.bin)"; }
export -f one; export W
mkdir -p $W/runs/q7
ls $W/mut/m*.sh | xargs -P 3 -I{} bash -c 'one {}' > $W/results/q7_raw.txt
echo done >> $W/results/q7_raw.txt
