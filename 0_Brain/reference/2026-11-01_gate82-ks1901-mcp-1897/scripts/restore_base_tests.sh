#!/bin/bash
# restore the 3 edited tests in wt_base from develop; move the 2 new ones to a quarantine dir (never delete)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate82-ks1901-mcp-1897
T=Blockchain/Dev/services/mcp-server/src/__tests__
for f in ks1410-mcp-http-500-part-a-never-echoes-the-thrown-text.test.ts ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts ks1868-hash-tool-unreadable-throw.test.ts; do
  git -C $W/repo show refs/gate/develop:$T/$f > $W/wt_base/$T/$f
done
mkdir -p $W/quarantine
for f in ks1893-hash-tool-never-returns-the-fs-error-text.test.ts ks1901-mcp-http-batch-items-never-echo-the-thrown-text.test.ts; do
  [ -e $W/wt_base/$T/$f ] && mv $W/wt_base/$T/$f $W/quarantine/$f.$(date +%s)
done
git -C $W/wt_base status --short
