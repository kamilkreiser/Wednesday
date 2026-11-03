#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate155-ks1868-pr1972
for t in head base; do
  if [ $t = head ]; then D=$W/clone/Blockchain/Dev/services/originate; else D=$W/base/Blockchain/Dev/services/originate; fi
  $D/node_modules/.bin/jest --rootDir $D --config $D/jest.config.js > $W/logs/full_$t.log 2>&1; echo "rc=$?" >> $W/logs/full_$t.log
done
echo done > $W/logs/full_done
