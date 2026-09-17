#!/usr/bin/env python3
"""drafter_extra_table.py — tabulate the extra-spelling / mount-prefix / originate rows: r1 vs r2 per row (status code hits) + the verdict per sub (ci)."""
import json, collections, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019r2'
print('drafter_extra_table', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
L = lambda t, k: json.load(open(GS + '/rows/rows_%s_%s.json' % (k, t)))
a, b = L('r1', 'extra'), L('r2', 'extra')
va = {v['sub']: v['ci']['verdict'] for v in a['verdict']}; vb = {v['sub']: v['ci']['verdict'] for v in b['verdict']}
f = lambda r: '%s %s %d' % (r['status'], r['code'] or '-', len(r['hits'])) + ('' if not r['hits'] else ' ' + r['hits'][0][-40:])
for st in ('test', 'prod', 'mount'):
    print('==', st)
    for x, y in zip(a[st], b[st]):
        assert (x['id'], x['tok'], x['target']) == (y['id'], y['tok'], y['target'])
        if st != 'mount' and x['cls'].startswith('originate'): continue
        sub = x['target'].split('/gdpr', 1)[-1] if st != 'mount' else ''
        print('  %-34s %-8s %-7s | verdict r1 %-12s r2 %-12s | r1 %-48s | r2 %-48s %s' % (x['id'][:34], x['tok'], x.get('mode', ''), va.get(sub, ''), vb.get(sub, ''), f(x), f(y), '' if f(x) == f(y) else '<< CHANGED'))
    ro = [(x['id'], x['tok'], f(x)) for x in b[st] if st != 'mount' and x['cls'].startswith('originate') and (x['status'] != 200 or len(x['hits']) != 1) and x['cls'] == 'originate-route']
    print('  non-door originate route rows NOT 200+1 hit at r2:', ro)
oa, ob = L('r1', 'extra_origin'), L('r2', 'extra_origin')
print('== originate (the REAL originate gdprRouter as upstream), rep 1 only')
for x, y in zip(oa['originate'], ob['originate']):
    if x['rep'] != 1: continue
    g = lambda r: '%s %s calls=%s' % (r['status'], r['code'] or '-', [c['fn'] + ':' + (c['args'][0] if c['args'] else '') for c in r['originateCalls']])
    print('  %-10s %-20s %-7s | r1 %-58s | r2 %-58s %s' % (x['mode'], x['id'], x['tok'], g(x)[:58], g(y)[:58], '' if g(x) == g(y) else '<< CHANGED'))
