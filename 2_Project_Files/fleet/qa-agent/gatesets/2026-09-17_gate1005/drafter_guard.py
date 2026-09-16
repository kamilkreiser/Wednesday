#!/usr/bin/env python3
"""drafter_guard.py — #1005: is the seat's tier guard (`expect(body.blockchain.source).toBe('persisted')`, ks1073 test :157) a tier witness?
GT1: the harness answers from TIER 1 with NO blob (tier1Absent stays false) -> predicted: the guard reds ('none'), all 3 cells.
GT2: the harness answers from TIER 1 WITH the same row as a tier-1 blob (a copy-paste slip) -> predicted: the guard stays GREEN
('persisted'); the 2 red-proof cells then go red on the VERDICT (tier-1 statusless keeps the carve-out), not at the guard.
Seat file SOLO per row; anchors by str.count; sha-asserted restore."""
import sys
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1005')
from drafterlib import *
F=GWR+'/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts'; pn=sha(T['head']+'/'+F)
P('drafter_guard start', ts(), 'pristine', pn[:16])
A="  currentBlob = undefined;\n  liveAnchorReply = null;\n  tier1Absent = true;                       // tier 1 misses -> fall through to tier 2\n  anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];\n"
for label,new in (('GT1_tier1_answers_no_blob', A.replace('tier1Absent = true;','tier1Absent = false;')),
                  ('GT2_tier1_answers_same_row_as_blob', "  currentBlob = { txHash: row.transactionHash, blockHeight: row.blockNumber, ...(('status' in row) ? { status: row.status } : {}) };\n  liveAnchorReply = null;\n  tier1Absent = false;                      // QA GT2: tier 1 answers with the row\n  anchorStoreRows = [{ contentHash: CONTENT_HASH, ...row }];\n")):
    P('== ROW', label)
    edit(T['head']+'/'+F, A, new)
    r=vitest('g_'+label,'head',files=['src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts'])
    restore('head', F, pn)
P('porcelain', porcelain('head')); P('drafter_guard end', ts())
