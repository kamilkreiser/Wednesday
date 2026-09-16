#!/usr/bin/env python3
"""drafter_probe.py — #1011: place qa1011-drafter-probe.test.ts in the base and head clone worktrees (never the checkout), run it alone,
save probe_rows_<tree>.json, move the scratch test out by rename (never rm), then diff the audit rows base vs head per request."""
import sys, os, json, shutil, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011')
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'
os.makedirs(W + '/_quarantine', exist_ok=True)
P('drafter_probe start', ts())
for t in ('base', 'head'):
    dst = T[t] + '/' + GWR + '/src/__tests__/qa1011-drafter-probe.test.ts'
    shutil.copyfile(GS + '/qa1011-drafter-probe.test.ts', dst)
    out = GS + '/probe_rows_%s.json' % t
    r = vitest('probe_' + t, t, 'gw', files=['src/__tests__/qa1011-drafter-probe.test.ts'], env_extra={'QA1011_PROBE_OUT': out})
    os.rename(dst, W + '/_quarantine/qa1011-drafter-probe.%s.%d.test.ts' % (t, len(os.listdir(W + '/_quarantine'))))
    if r is None or r['failed']: P('stderr tail', (r or {}).get('stderr_tail', '')[-1500:])
B = json.load(open(GS + '/probe_rows_base.json'))['rows']; H = json.load(open(GS + '/probe_rows_head.json'))['rows']
P('rows base %d head %d' % (len(B), len(H)))
same = diff = 0
for b, h in zip(B, H):
    if b.get('label') == 'NESTED fixture':
        P('NESTED base', json.dumps(b['out'])); P('NESTED head', json.dumps(h['out'])); continue
    eq = b['status'] == h['status'] and b['audits'] == h['audits']
    same += eq; diff += (not eq)
    P('%-5s %-48s status %s/%s audits %d/%d' % ('SAME' if eq else 'DIFF', b['label'][:48], b['status'], h['status'], len(b['audits']), len(h['audits'])))
    for tag, row in (('base', b), ('head', h)):
        for a in row['audits']:
            d = a['details'] if isinstance(a['details'], dict) else {}
            P('      %s action=%s rtype=%s rid=%s path=%s status=%s success=%s email=%s' % (tag, a['action'], a['resourceType'], a['resourceId'], d.get('path'), d.get('status'), a['success'], d.get('attemptedEmail')))
    if b['body'] != h['body']: P('      BODY differs:', b['body'][:80], '|', h['body'][:80])
P('SAME %d DIFF %d' % (same, diff))
P('porcelain base', [l for l in porcelain('base') if not l.rstrip('/').endswith('node_modules')], 'head', [l for l in porcelain('head') if not l.rstrip('/').endswith('node_modules')])
P('drafter_probe end', ts())
