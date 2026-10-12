#!/bin/bash
# usage: run.sh <service> [runner args]   (governance=jest, staking/transfer=vitest)
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
svc=$1; shift
cd "$S/${TREE:-repo2}/Blockchain/Dev/services/$svc" || exit 99
if [ "$svc" = governance ]; then
  ../../node_modules/.bin/jest --no-cache "$@" 2>&1
else
  ../../node_modules/.bin/vitest run "$@" 2>&1
fi
echo "RC=$?"
