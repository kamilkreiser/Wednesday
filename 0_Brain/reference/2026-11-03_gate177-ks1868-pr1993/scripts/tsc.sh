#!/bin/bash
# tsc.sh : Q7. tsc --noEmit with tests, packages/shared (workdir tsconfig extending the package's, tests included) and
# services/api-gateway (its own tsconfig.test.json), base (mut/base) and head (repo). Normalised error lists -> results/tsc_*.norm
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
for t in base head; do
  case $t in base) D=$W/mut/base/Blockchain/Dev;; head) D=$W/repo/Blockchain/Dev;; esac
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp $D/packages/shared/node_modules/.bin/tsc -p $W/scratch/tsc/tsconfig.shared.$t.json > $W/runs/tsc_shared_$t.txt 2>&1; r1=$?
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp $D/services/api-gateway/node_modules/.bin/tsc -p $D/services/api-gateway/tsconfig.test.json > $W/runs/tsc_agw_$t.txt 2>&1; r2=$?
  for k in shared agw; do grep -E 'error TS[0-9]+' $W/runs/tsc_${k}_$t.txt | sed -E 's#^.*/Blockchain/Dev/##' | sort > $W/results/tsc_${k}_$t.norm; done
  echo "$t shared rc=$r1 errors=$(wc -l < $W/results/tsc_shared_$t.norm | tr -d ' ')  agw rc=$r2 errors=$(wc -l < $W/results/tsc_agw_$t.norm | tr -d ' ')"
done
for k in shared agw; do echo "diff $k base->head:"; diff $W/results/tsc_${k}_base.norm $W/results/tsc_${k}_head.norm && echo "  (byte-equal)"; done
echo "tsc versions: shared $($W/repo/Blockchain/Dev/packages/shared/node_modules/.bin/tsc -v) agw $($W/repo/Blockchain/Dev/services/api-gateway/node_modules/.bin/tsc -v)"
