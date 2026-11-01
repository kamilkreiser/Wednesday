#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910
R=$W/repo; M=$R/Blockchain/Dev/services/mcp-server; L=$W/logs; P=$M/src/http-server.ts
cp $W/scripts/probe_real.test.ts $M/src/__tests__/zz_probe_real.test.ts
for V in head base; do
  if [ $V = base ]; then git -C $R show origin/develop:Blockchain/Dev/services/mcp-server/src/http-server.ts > $P; else cp $W/http-server.head.ts $P; fi
  (cd $M && PROBE_OUT=$L/probe_$V.json npx vitest run src/__tests__/zz_probe_real.test.ts --dangerouslyIgnoreUnhandledErrors > $L/probe_$V.log 2>&1); echo $V rc=$? >> $L/summary.log
done
cp $W/http-server.head.ts $P
mkdir -p $W/_quarantine_2026-11-02; mv $M/src/__tests__/zz_probe_real.test.ts $W/_quarantine_2026-11-02/
shasum -a 256 $P $W/http-server.head.ts >> $L/summary.log
