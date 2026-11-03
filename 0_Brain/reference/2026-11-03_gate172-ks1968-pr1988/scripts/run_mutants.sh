#!/bin/bash
# For each mutant: apply it, run (a) the PR's two test files, (b) the gate recorder; record failed/passed/total; restore head.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate172-ks1968-pr1988; A=$W/repo/Blockchain/Dev/services/auth
PR="src/__tests__/ks1968-breached-password-refused-at-register-and-reset.test.ts src/__tests__/ks1868-password-verify-hibp-catches-unreadable-throw.test.ts"
: > $W/runs/mutants_raw.tsv
cp $W/scripts/gate172-recorder.test.ts $A/src/__tests__/gate172-recorder.test.ts
for d in $W/mut/m*/; do
  id=$(basename $d)
  bash $W/scripts/swap.sh head > /dev/null
  for f in $d*; do b=$(basename $f); cp $f $A/${b//__//}; done
  bash $W/scripts/vt.sh mut_pr_$id $PR --reporter=json --outputFile=$W/runs/mut_pr_$id.json > /dev/null
  GATE_EXTRA_ENV="GATE_REC=/dev/null" bash $W/scripts/vt.sh mut_rec_$id src/__tests__/gate172-recorder.test.ts --reporter=json --outputFile=$W/runs/mut_rec_$id.json > /dev/null
  python3 -I -c "
import json
def c(p):
  try: d=json.load(open(p)); return d['numFailedTests'], d['numTotalTests']
  except Exception as e: return 'ERR','ERR'
a=c('$W/runs/mut_pr_$id.json'); b=c('$W/runs/mut_rec_$id.json')
g=sum(1 for l in open('$W/runs/guard_mut_pr_$id.log'))+sum(1 for l in open('$W/runs/guard_mut_rec_$id.log'))
print('$id', a[0], a[1], b[0], b[1], g, sep='\t')" >> $W/runs/mutants_raw.tsv
done
bash $W/scripts/swap.sh head > /dev/null
mv $A/src/__tests__/gate172-recorder.test.ts $W/tmp/gate172-recorder.mut.ts
git -C $W/repo status --porcelain -- Blockchain/Dev/services/auth | grep -v node_modules
echo done
