#!/bin/bash
# Compare each mutant fingerprint against the real 058's. Behaviour = every line except the 'T pol' text lines; text = 'T pol' lines.
# L (lock) scenario exists only for REAL and M7; it is compared only for M7.
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/runs
beh(){ grep -v '^T pol' "$1" | grep -v '^## L' | grep -v '^rec=' ; }
txt(){ grep '^T pol' "$1"; }
printf '%-24s %-9s %-6s %s\n' MUTANT BEHAVIOUR TEXT "scenarios whose behaviour differs"
k=0; s=0
for f in $R/mut_*.fp; do id=$(basename $f .fp | sed 's/^mut_//'); [ $id = REAL ] && continue
  bd=$(diff <(beh $R/mut_REAL.fp) <(beh $f) | grep '^[<>]' | sed -E 's/^[<>] (##? ?)?([A-Z]+).*/\2/' | sort -u | tr '\n' ' ')
  if [ $id = M7 ]; then ld=$(diff <(grep -A1 '^## L' $R/mut_REAL.fp) <(grep -A1 '^## L' $f) | grep -c '^[<>]'); [ "$ld" -gt 0 ] && bd="$bd L"; fi
  td=$(diff <(txt $R/mut_REAL.fp) <(txt $f) | grep -c '^[<>]')
  b=$([ -n "$bd" ] && echo KILLED || echo survived); t=$([ "$td" -gt 0 ] && echo differs || echo same)
  if [ -n "$bd" ] || [ "$td" -gt 0 ]; then k=$((k+1)); else s=$((s+1)); fi
  printf '%-24s %-9s %-6s %s\n' $id $b $t "$bd"
done
echo "TOTAL mutants=$((k+s)) killed(behaviour or text)=$k survived=$s"
