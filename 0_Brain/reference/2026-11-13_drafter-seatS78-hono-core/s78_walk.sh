#!/bin/bash
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; M=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate349-tier1-ks2194-hono/scratch/iso-head/Blockchain/Dev/services/mcp-server
echo "installed hono: $(grep '"version"' $M/node_modules/hono/package.json) node-server: $(grep '"version"' $M/node_modules/@hono/node-server/package.json)"
timeout_none=1
node $F/s78_importwalk_hono.mjs $M dist/http-server.js dist/index.js > $F/s78_walk.out 2>&1 < /dev/null &
P=$!; sleep 8; kill $P 2>/dev/null; cat $F/s78_walk.out
echo "--- control: SDK streamableHttp.js"
node $F/s78_importwalk_hono.mjs $M node_modules/@modelcontextprotocol/sdk/dist/esm/server/streamableHttp.js 2>&1 < /dev/null | tail -3
echo "--- static: imports of hono in mcp-server dist+src (excluding node_modules)"
/usr/bin/grep -rnE "from ['\"]hono|require\(['\"]hono|import\(['\"]hono|@hono/" $M/dist $M/src --include=*.js --include=*.ts -l | head; echo "grep rc=$?"
echo "--- control: express import count in dist"; /usr/bin/grep -rl "from 'express'\|from \"express\"" $M/dist --include=*.js | wc -l
echo "--- SDK files importing hono pkg or node-server (dist/esm)"
/usr/bin/grep -rlE "from ['\"]hono['\"/]|from ['\"]@hono/" $M/node_modules/@modelcontextprotocol/sdk/dist/esm --include=*.js
