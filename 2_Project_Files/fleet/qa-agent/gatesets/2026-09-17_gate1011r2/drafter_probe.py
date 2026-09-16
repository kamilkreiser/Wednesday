#!/usr/bin/env python3
"""drafter_probe.py — #1011 ROUND 2: the round-1 drafter's 29-request real-app probe (qa1011-drafter-probe.test.ts, copied unchanged) placed in the
drafter clone's base 1125607e9 / head 6dc825644 / merged (head + no-ff 79432c797) worktrees, NODE_ENV=test. Compares base vs head, head vs merged, and
head vs the ROUND-1 drafter's entry-path counterfactual rows (probe_rows_head_entrypath.json on 0a1f8900c + D3). PREDICTIONS for the gate. Never rm."""
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafterlib import *
R1 = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011'
GWR = 'Blockchain/Dev/services/api-gateway'
os.makedirs(W + '/_quarantine', exist_ok=True)
P('drafter_probe r2 start', ts())
for t in ('base', 'head', 'merged'):
    dst = T[t] + '/' + GWR + '/src/__tests__/qa1011-drafter-probe.test.ts'
    shutil.copyfile(GS + '/qa1011-drafter-probe.test.ts', dst)
    out = GS + '/probe_rows_%s.json' % t
    r = vitest('probe_' + t, t, 'gw', files=['src/__tests__/qa1011-drafter-probe.test.ts'], env_extra={'QA1011_PROBE_OUT': out})
    os.rename(dst, W + '/_quarantine/qa1011-drafter-probe.%s.%d.test.ts' % (t, len(os.listdir(W + '/_quarantine'))))
    if r is None or r['failed']: P('stderr tail', (r or {}).get('stderr_tail', '')[-1500:])
def rows(p): return json.load(open(p))['rows']
def strip(a):
    a = json.loads(json.dumps(a))
    if isinstance(a.get('details'), dict): a['details'].pop('durationMs', None)
    return a
def cmp(nameA, A, nameB, B, show):
    same = diff = 0
    for a, b in zip(A, B):
        if a.get('label') == 'NESTED fixture':
            P('  NESTED %s' % nameA, json.dumps(a['out'])[:400]); P('  NESTED %s' % nameB, json.dumps(b['out'])[:400]); continue
        eq = a['status'] == b['status'] and [strip(x) for x in a['audits']] == [strip(x) for x in b['audits']]
        same += eq; diff += (not eq)
        if not eq or show:
            P('  %-5s %-50s status %s/%s' % ('SAME' if eq else 'DIFF', a['label'][:50], a['status'], b['status']))
            for tag, row in ((nameA, a), (nameB, b)):
                for x in row['audits']:
                    d = x['details'] if isinstance(x['details'], dict) else {}
                    P('        %-9s action=%s rtype=%s path=%s' % (tag, x['action'], x['resourceType'], d.get('path')))
    P('  == %s vs %s: rows %d/%d SAME %d DIFF %d' % (nameA, nameB, len(A), len(B), same, diff))
B, H, M, E = rows(GS + '/probe_rows_base.json'), rows(GS + '/probe_rows_head.json'), rows(GS + '/probe_rows_merged.json'), rows(R1 + '/probe_rows_head_entrypath.json')
assert [x['label'] for x in B] == [x['label'] for x in E], 'probe label lists differ from round 1'
P('-- base 1125607e9 vs head 6dc825644'); cmp('base', B, 'head', H, False)
P('-- head vs merged (noise pair + develop 79432c797 move)'); cmp('head', H, 'merged', M, False)
P('-- head vs ROUND-1 drafter entry-path counterfactual (0a1f8900c + D3)'); cmp('head', H, 'r1-D3', E, False)
P('drafter_probe r2 end', ts())
