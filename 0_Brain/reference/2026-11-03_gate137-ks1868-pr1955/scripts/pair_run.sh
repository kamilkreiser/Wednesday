#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955; D=$W/merged/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/anchoring --maxWorkers=3 --reporter=json --outputFile.json=$W/logs/pair_anchoring_suite.json > $W/logs/pair_anchoring_suite.log 2>&1; echo "anch suite rc=$?"
nice -n 10 $D/node_modules/.bin/jest --rootDir $D/services/originate --config $D/services/originate/jest.config.js --forceExit --json --outputFile=$W/logs/pair_originate_new.json --runTestsByPath $D/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts > $W/logs/pair_originate_new.log 2>&1; echo "orig new rc=$?"
(cd_=1; nice -n 10 $D/node_modules/.bin/tsc -p $D/services/anchoring/tsconfig.json --noEmit > $W/logs/pair_tsc_anchoring.log 2>&1; echo "tsc anchoring rc=$?")
git -C $W/merged status --short | head
