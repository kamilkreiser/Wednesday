#!/usr/bin/env python3
"""drafter_probe_entrypath.py — #1011 COUNTERFACTUAL (not a fix; never leaves the drafter's clone): on head, capture the CANONICAL
req.path at entry (after the normaliser and the /api/v1 strip) for BOTH details.path and deriveAction, then re-run the real-app probe and
diff against base. Question: does the entry-time req.path shape carry the KS-871 fix (refused gdpr rows correct) with parity elsewhere?
Also the whole api-gateway suite on that variant (denominator asserted). Restored sha-identical."""
import sys, os, json, shutil
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011')
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'; AUD = GWR + '/src/middleware/audit.ts'
P('drafter_probe_entrypath start', ts())
pristine = sha(T['head'] + '/' + AUD)
edit(T['head'] + '/' + AUD, "    const auditPath = req.originalUrl.split('?')[0];\n", "    const auditPath = req.path;\n    (req as unknown as { qaAuditPath: string }).qaAuditPath = auditPath;\n", [('qaAuditPath', 2)])
edit(T['head'] + '/' + AUD, "  const segments = req.originalUrl.split('?')[0].replace(/\\/+$/, '').split('/').filter(Boolean);\n", "  const segments = ((req as unknown as { qaAuditPath?: string }).qaAuditPath ?? req.path).replace(/\\/+$/, '').split('/').filter(Boolean);\n", [('qaAuditPath', 4)])
dst = T['head'] + '/' + GWR + '/src/__tests__/qa1011-drafter-probe.test.ts'
shutil.copyfile(GS + '/qa1011-drafter-probe.test.ts', dst)
out = GS + '/probe_rows_head_entrypath.json'
r = vitest('probe_head_entrypath', 'head', 'gw', files=['src/__tests__/qa1011-drafter-probe.test.ts'], env_extra={'QA1011_PROBE_OUT': out})
os.rename(dst, W + '/_quarantine/qa1011-drafter-probe.entrypath.%d.test.ts' % len(os.listdir(W + '/_quarantine')))
s = vitest('gw_suite_head_entrypath', 'head', 'gw')
P('whole suite on the entry-path variant: files %d tests %d failed %d pending %d' % (s['files'], s['tests'], s['failed'], s['pending']))
restore('head', AUD, pristine)
B = json.load(open(GS + '/probe_rows_base.json'))['rows']; H = json.load(open(out))['rows']
same = diff = 0
for b, h in zip(B, H):
    if b.get('label') == 'NESTED fixture': continue
    eq = b['status'] == h['status'] and b['audits'] == h['audits']; same += eq; diff += (not eq)
    if not eq:
        P('DIFF  %-48s' % b['label'][:48])
        for tag, row in (('base', b), ('entry', h)):
            for a in row['audits']:
                d = a['details'] if isinstance(a['details'], dict) else {}
                P('      %s action=%s rtype=%s path=%s status=%s' % (tag, a['action'], a['resourceType'], d.get('path'), d.get('status')))
P('base vs entry-path variant: SAME %d DIFF %d' % (same, diff))
P('porcelain head', [l for l in porcelain('head') if not l.rstrip('/').endswith('node_modules')])
P('drafter_probe_entrypath end', ts())
