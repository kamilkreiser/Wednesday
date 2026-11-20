#!/bin/bash
L=/private/tmp/b1818-gate/logs/chain
ADDED=$(tr '\n' ' ' < /private/tmp/b1818-gate/logs/pr_added.txt)
docker run --rm -i --network none -w /repo -e ADDED="$ADDED" --entrypoint sh pc-b1803-node:merged -c '
mkdir -p /tmp/q; n=0; for p in $ADDED; do mkdir -p "/tmp/q/$(dirname "$p")"; mv "/repo/$p" "/tmp/q/$p" && n=$((n+1)); done; echo "moved aside $n"
tar -x -C /repo -f -
npm run build >/tmp/build.log 2>&1; echo "build rc=$?"
cat /repo/content/release-draft/CONTENT_HASH
cat > /repo/tsconfig.gate-tests.json <<JSON
{ "extends": "./tsconfig.base.json",
  "compilerOptions": { "noEmit": true, "composite": false, "declaration": false, "declarationMap": false, "sourceMap": false, "incremental": false },
  "include": ["packages/engine/test/**/*.ts", "packages/content/test/**/*.ts", "packages/content/src/**/*.test.ts", "packages/renderers/test/**/*.ts", "packages/canonical/test/**/*.ts", "apps/api/test/**/*.ts"] }
JSON
npx tsc -p /repo/tsconfig.gate-tests.json --pretty false; echo "tsc rc=$?"
' < /private/tmp/b1818-gate/data/main.tar > $L/tsc_tests_main.log 2>&1
echo "tsc_tests_main done" >> $L/RCS.txt
