#!/bin/bash
set -u
L=/private/tmp/b1818-gate/logs/chain; mkdir -p $L; : > $L/RCS.txt
ctr=b1818-gate-merged
docker rm -f $ctr >/dev/null 2>&1
docker run -d --network none --name $ctr --entrypoint sleep pc-b1803-node:merged infinity > $L/ctr.txt 2>&1
docker inspect --format '{{.HostConfig.NetworkMode}} mounts={{len .Mounts}}' $ctr > $L/ctr_net.txt
docker exec $ctr sh -c 'env | grep -c -i sow; ls /repo | head -50' > $L/env_sow.txt 2>&1
step(){ n=$1; shift; s=$SECONDS; echo "=== $(date +%T) $n load $(sysctl -n vm.loadavg)" >> $L/CHAIN.log; docker exec $ctr "$@" > $L/$n.log 2>&1; rc=$?; echo "$n rc=$rc ($((SECONDS-s))s)" >> $L/RCS.txt; }
step node_version node --version
step vitest_version npx vitest --version
step lint npm run lint
step format_check npm run format:check
step typecheck npm run typecheck
step build npm run build
step vitest_renderers npx vitest run --project renderers --reporter=verbose
step vitest_workspace npx vitest run --project workspace --reporter=verbose
step content_check npm run content:check
step demo_check node packages/content/dist/cli/build-demo-content.js --check
docker rm -f $ctr >/dev/null 2>&1
echo "left: $(docker ps -a --format '{{.Names}}' | grep -c b1818)" >> $L/RCS.txt
