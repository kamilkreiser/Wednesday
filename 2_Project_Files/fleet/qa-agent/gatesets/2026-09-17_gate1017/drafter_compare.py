#!/usr/bin/env python3
"""drafter_compare.py LABEL... — summarise rows_probe_<label>.json: census classes per file (limiter absent / counted once / counted twice),
the K status triples, J/N/I leaks, plus every non-census stage verbatim. Same instrument for every tree and tamper."""
import json, sys, collections
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
for label in sys.argv[1:]:
    d = json.load(open(G + '/rows_probe_%s.json' % label))
    print('=' * 3, label, json.dumps(d['meta'])[:700])
    c = d['census']
    if c:
        cls = collections.Counter(); twice = []; trip = collections.Counter(); leaks = []
        for r in c:
            K = r['K']
            k = 'limiter-absent' if all(x[2] is None for x in K) else ('counted-once' if K[0][3] == '1' else ('COUNTED-TWICE' if K[0][3] == '0' else 'remaining=' + str(K[0][3])))
            cls[(r['file'], k)] += 1
            if k == 'COUNTED-TWICE': twice.append((r['file'], r['line'], r['verb'], r['path'], [x[0] for x in K], r['Khits']))
            if k != 'limiter-absent': trip[tuple(x[0] for x in K)] += 1
            if any(j[1] for j in r['J']) or r['N'][1] or r['I'][1]: leaks.append((r['path'], r['J'], r['N'], r['I']))
        print('routes', len(c), '| classes', sorted(cls.items()))
        print('limited K status triples', trip.most_common())
        print('counted-twice', len(twice)); [print('   ', t) for t in twice]
        print('J/N/I carrying X-RateLimit-Limit', len(leaks), leaks[:5])
        tf = collections.Counter(tuple(r['KtenantFwd']) == ('t-qa1017-c%d' % r['idx'],) for r in c if r['KtenantFwd'])
        print('forwarded x-tenant-id == key tenant (routes with forwards):', dict(tf))
        allowed_hits = collections.Counter((r['Khits']) for r in c if r['K'][0][2] is not None and r['K'][2][0] == 429)
        print('limited routes with request 3 = 429: upstream hits distribution', dict(allowed_hits))
    for s in ('principals', 'a4', 'keyscope', 'erasure', 'bare', 'order'):
        for x in d.get(s, []): print('  ', s, json.dumps(x)[:330])
