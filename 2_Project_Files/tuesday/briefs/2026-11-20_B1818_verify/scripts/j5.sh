#!/bin/bash
L=/private/tmp/b1818-gate/logs/chain
docker run --rm -i --network none -w /repo --entrypoint sh pc-b1803-node:merged -c '
npm run build >/tmp/build.log 2>&1; echo "build rc=$?"
cat > /repo/tsconfig.gate-tests.json <<JSON
{ "extends": "./tsconfig.base.json",
  "compilerOptions": { "noEmit": true, "composite": false, "declaration": false, "declarationMap": false, "sourceMap": false, "incremental": false },
  "include": ["packages/engine/test/**/*.ts", "packages/content/test/**/*.ts", "packages/content/src/**/*.test.ts", "packages/renderers/test/**/*.ts", "packages/canonical/test/**/*.ts", "apps/api/test/**/*.ts"] }
JSON
npx tsc -p /repo/tsconfig.gate-tests.json --pretty false; echo "tsc rc=$?"
' > $L/tsc_tests.log 2>&1
echo "tsc_tests done" >> $L/RCS.txt
