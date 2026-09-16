#!/usr/bin/env python3
"""drafter_parity.py — at base and head: each connector/unknown-level principal vs the lowest authenticated human (jwt_NONE), create + verify rows (status, code, forwarded, workflow instances). Anonymous rows listed separately."""
import json
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
for t in ('base', 'head'):
    R = json.load(open('%s/probe_rows_%s.json' % (GS, t)))['rows']
    idx = {(x['kind'], x['principal'], x['type']): x for x in R if x['kind'] in ('create', 'verify')}
    ref = 'jwt_NONE'
    for p in ('sk_write', 'sk_noscope', 'sk_restricted_to_DOCUMENT', 'sk_bypass_workflow', 'cjwt_bearer_write', 'cjwt_bearer_noscope', 'tt_api_key', 'anon'):
        d = []
        for (k, pp, ty), x in idx.items():
            if pp != p: continue
            y = idx[(k, ref, ty)]
            a = (x['status'], x['code'], x.get('forwarded'), x.get('workflowInstances')); b = (y['status'], y['code'], y.get('forwarded'), y.get('workflowInstances'))
            if a != b: d.append('%s %s: %s vs NONE-human %s' % (k, ty, a, b))
        print(t, p, 'differs from jwt_NONE on', len(d), 'rows')
        for s in sorted(d): print('    ', s)
    print(t, 'untyped create (no documentType):', {p: idx[('create', p, None)]['status'] for p in ('sk_noscope', 'cjwt_bearer_noscope', 'cjwt_bearer_write', 'sk_write', 'anon')})
