#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910
R=$W/repo; M=$R/Blockchain/Dev/services/mcp-server; L=$W/logs; Q=$W/_quarantine_2026-11-02
cat > $M/tsconfig.gate92.json <<'EOT'
{ "extends": "./tsconfig.json", "compilerOptions": {"noEmit": true, "rootDir": ".", "declaration": false, "declarationMap": false, "sourceMap": false}, "include": ["src/**/*"], "exclude": ["node_modules","dist"] }
EOT
T() { (cd $M && npx tsc -p tsconfig.gate92.json "$@"); }
T > $L/tsc_head.log 2>&1; echo tsc head rc=$? lines=$(wc -l < $L/tsc_head.log) >> $L/summary.log
echo "files head: $(T --listFilesOnly | /usr/bin/grep -c '/mcp-server/src/')" >> $L/summary.log
git -C $R show origin/develop:Blockchain/Dev/services/mcp-server/src/http-server.ts > $M/src/http-server.ts
mkdir -p $Q/newtests; mv $M/src/__tests__/ks1868-mcp-http-route-catches-p*.ts $Q/newtests/
T > $L/tsc_base.log 2>&1; echo tsc base rc=$? lines=$(wc -l < $L/tsc_base.log) >> $L/summary.log
echo "files base: $(T --listFilesOnly | /usr/bin/grep -c '/mcp-server/src/')" >> $L/summary.log
cp $W/http-server.head.ts $M/src/http-server.ts; mv $Q/newtests/* $M/src/__tests__/
git -C $R status --short >> $L/summary.log
shasum -a 256 $M/src/http-server.ts >> $L/summary.log
echo "const z: number = 'x'; export default z;" > $M/src/zz_planted.ts
T > $L/tsc_planted.log 2>&1; echo tsc planted rc=$? >> $L/summary.log; mv $M/src/zz_planted.ts $Q/
(cd $M && npx eslint src/http-server.ts src/__tests__/ks1868-mcp-http-route-catches-p1-unreadable-throw.test.ts src/__tests__/ks1868-mcp-http-route-catches-p2-unreadable-throw.test.ts src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts > $L/eslint.log 2>&1; echo eslint rc=$? >> $L/summary.log); tail -4 $L/eslint.log >> $L/summary.log
