#!/bin/bash
# Run the PR suite (head copy) against every mutant in mut/ (4 at a time); one line per mutant in results/q4_mutants_raw.txt.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2
one() { local f="$1" id; id=$(basename "$f" .sh)
  bash $W/harness/q0_suite.sh "mut-$id" "$f" > $W/runs/q4/$id.bin 2>&1
  local r; r=$(grep -E '^Results' $W/runs/q4/$id.bin | tail -1)
  printf '%s\t%s\t%s\tfails=%s\thex48_in_output=%s\n' "$id" "$( [[ "$r" == *" 0 failed"* ]] && echo SURVIVED || { [[ -z "$r" ]] && echo NO-RESULT || echo KILLED; } )" "$r" "$(grep '^FAIL' $W/runs/q4/$id.bin | cut -c6-60 | tr '\n' ';' | cut -c1-300)" "$(grep -cE '[0-9a-f]{48}' $W/runs/q4/$id.bin)"; }
export -f one; export W
mkdir -p $W/runs/q4
ls $W/mut/*.sh | xargs -P 4 -I{} bash -c 'one {}' > $W/results/q4_mutants_raw.txt
echo done >> $W/results/q4_mutants_raw.txt
