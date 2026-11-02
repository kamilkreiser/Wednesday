W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/vc-issuer
for lab in head base; do
  if [ $lab = base ]; then git -C $R checkout -q 2f9f7db313b3 -- Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts Blockchain/Dev/services/vc-issuer/src/db.ts; fi
  printf '{"extends":"./tsconfig.json","compilerOptions":{"noEmit":true,"declaration":false,"declarationMap":false,"sourceMap":false,"rootDir":"./src"},"include":["src/**/*"],"exclude":["node_modules","dist"]}\n' > $S/tsconfig.gate.json
  nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.gate.json > $W/logs/tsc_tests_$lab.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$lab.log
  echo "$lab tsc with tests: $(/usr/bin/grep -c 'error TS' $W/logs/tsc_tests_$lab.log) errors; $(tail -1 $W/logs/tsc_tests_$lab.log)"
  if [ $lab = base ]; then git -C $R checkout -q pr1968 -- Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts Blockchain/Dev/services/vc-issuer/src/db.ts; fi
done
mv $S/tsconfig.gate.json $W/logs/_quarantine/tsconfig.gate.json
nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/tsc_own.log 2>&1; echo "own tsconfig rc=$?"
