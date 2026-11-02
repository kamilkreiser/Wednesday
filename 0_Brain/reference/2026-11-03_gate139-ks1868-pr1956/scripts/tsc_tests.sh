#!/bin/bash
# tsc with tests, per service; ad hoc tsconfig.gate.json (untracked) extends the service tsconfig and includes the tests.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate139-ks1868-pr1956
D=$W/repo/Blockchain/Dev
label=$1
for s in analytics api-gateway anchoring kyc; do
  printf '{"extends":"./tsconfig.json","compilerOptions":{"noEmit":true,"declaration":false,"declarationMap":false,"sourceMap":false,"rootDir":"./src"},"include":["src/**/*"],"exclude":["node_modules","dist"]}\n' > $D/services/$s/tsconfig.gate.json
  nice -n 10 $D/node_modules/.bin/tsc -p $D/services/$s/tsconfig.gate.json > $W/logs/tsc_${label}_$s.log 2>&1; echo "rc=$?" >> $W/logs/tsc_${label}_$s.log
  echo "$label $s: $(grep -c 'error TS' $W/logs/tsc_${label}_$s.log) errors; $(tail -1 $W/logs/tsc_${label}_$s.log)"
done
