#!/usr/bin/env python3
"""drafter_compare.py A B [C] — rows_probe_<label>.json side by side: per (stage, id, method, target, tok): status/code/upstream-hits per tree,
DIFF flag, class summaries (refusal oracle: door shapes without scope -> 403/400 with 0 hits), the grace and limiter stages, and the verdict table."""
import json, sys, collections
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
labs = sys.argv[1:]; J = {l: json.load(open(G + '/rows_probe_%s.json' % l)) for l in labs}
def cell(r): return '%s%s h%d%s' % (r['status'], ('/' + r['code']) if r.get('code') else '', len(r['hits']), (' ' + '|'.join(r['hits'])) if r['hits'] else '')
for l in labs: print(l, 'verdictExported', J[l].get('verdictExported'), 'jwksFetches', J[l].get('jwksFetches'), 'captured', J[l].get('capturedLines'), 'rows test/prod/grace/limiter', len(J[l]['test']), len(J[l]['prod']), len(J[l]['grace']), len(J[l]['limiter']))
for st in ('test', 'prod'):
    print('=' * 3, st)
    keys = []; idx = {}
    for l in labs:
        for r in J[l][st]:
            k = (r['id'], r['method'], r['target'], r['tok'])
            if k not in keys: keys.append(k)
            idx[(l, k)] = r
    ndiff = collections.Counter()
    for k in keys:
        cells = [cell(idx[(l, k)]) if (l, k) in idx else 'MISSING' for l in labs]
        d = ' DIFF' if len(set(cells)) > 1 else ''
        for i in range(1, len(labs)):
            if cells[i] != cells[0]: ndiff[labs[0] + '->' + labs[i]] += 1
        print('%-34s %-5s %-44s %-15s | %s%s' % (k[0][:34], k[1], k[2][:44], k[3], ' || '.join(cells), d))
    print('row diffs', dict(ndiff), 'of', len(keys))
    for l in labs:
        rows = J[l][st]
        bad = [r for r in rows if r['cls'] in ('door', 'undetermined') and r['tok'] in ('noscope', 'user', 'noemail_noscope') and (r['status'] not in (400, 403) or r['hits'])]
        byc = collections.Counter((r['cls'], r['tok'], r['status'], len(r['hits'])) for r in rows)
        print(' ', l, st, 'refusal-oracle breaches (door/undetermined shape, no-scope token, not 400/403 or any upstream hit):', len(bad), [(r['id'], r['status'], r['hits']) for r in bad][:40])
        w = [(r['id'], r['tok'], r['status'], r['hits']) for r in rows if r['cls'] == 'raw-erasures-canon-not-door']
        print(' ', l, st, 'W rows:', w)
        o400 = [(r['id'], r['tok'], r['status'], r['code']) for r in rows if r['cls'] in ('originate-route', 'not-door') and r['status'] == 400]
        print(' ', l, st, '400s on originate routes / not-door spellings:', o400)
print('=' * 3, 'grace')
for l in labs: print(l, [(r['id'], r['status'], r.get('code'), r['hits'], 'grace', r['graceLines']) for r in J[l]['grace']])
print('=' * 3, 'limiter')
for l in labs: print(l, [(r['id'], r['status'], r.get('code'), len(r['hits']), r['rlLimit'], r['rlRemaining']) for r in J[l]['limiter']])
print('=' * 3, 'verdict table')
for l in labs:
    if J[l]['verdict']:
        for v in J[l]['verdict']: print(' ', l, '%-52s ci=%-13s %-18s cs=%s' % (v['sub'][:52], v['ci']['verdict'], v['ci']['canonicalPath'], v['cs']['verdict']))
        break
