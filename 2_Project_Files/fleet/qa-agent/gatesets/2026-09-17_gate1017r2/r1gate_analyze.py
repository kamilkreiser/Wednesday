#!/usr/bin/env python3
"""analyze.py LABEL [LABEL2] — summarise a rows file; with LABEL2, diff census/stages row by row. Oracle (census, per route):
FIRES = K[0] carries X-RateLimit-Limit. Expected when FIRES: K statuses [x, x, 429], Remaining ['1','0','0'], Khits[2] == Khits[1] (refused request not forwarded),
D Remaining '999' (counted once; '998' = twice). FAIL-unlimited = K[0..2] all non-429 with no header while K[0] not 401/403/404/405/400 at the gateway
(a key admitted and never counted) — listed for READ, graded by family. Non-machine: any P header or 429 = Major/Blocker; N/I/M header = Major."""
import json, sys, os, collections
EV = os.path.dirname(os.path.abspath(__file__))
def load(l): return json.load(open(EV + '/rows/%s.json' % l))
a = load(sys.argv[1])
C = a['census']
fires = [r for r in C if r['K'][0][2] is not None]
print('LABEL', sys.argv[1], 'routes', len(C), 'fires', len(fires))
print('fires by file', dict(collections.Counter(r['file'] for r in fires)))
trip = collections.Counter(tuple(x[0] for x in r['K']) for r in fires); print('K status triples (fires)', dict(trip))
bad = [(r['verb'], r['path'], [x[3] for x in r['K']], r['Khits']) for r in fires if [x[3] for x in r['K']] != ['1', '0', '0'] or r['K'][2][0] != 429 or r['Khits'][2] != r['Khits'][1]]
print('fires but NOT [1,0,0]/429/refused-not-forwarded:', len(bad)); [print('   ', b) for b in bad]
dd = collections.Counter(r['D'][3] for r in C); print('D Remaining histogram', dict(dd))
twice = [(r['verb'], r['path'], r['file'], r['line'], r['D'][3], r['D'][0]) for r in C if r['D'][3] not in (None, '999')]
print('D not 999 (double or other):', len(twice)); [print('   ', t) for t in twice]
hitsh = collections.Counter(r['Khits'][2] for r in fires); print('K upstream hits after 3 (fires)', dict(hitsh))
nf = [r for r in C if r['K'][0][2] is None]
nfcls = collections.Counter((r['file'], tuple(x[0] for x in r['K']), r['Khits'][2] > 0) for r in nf)
print('NOT firing: (file, statuses, forwarded?) ->count'); [print('   ', k, v) for k, v in sorted(nfcls.items(), key=lambda x: -x[1])]
adm = [(r['verb'], r['path'], r['file'], r['line'], [x[0] for x in r['K']], r['Khits']) for r in nf if all(x[0] not in (401, 403, 404, 405, 400, 429, -1, -2) for x in r['K'])]
print('NOT firing yet ADMITTED a key (non-4xx x3):', len(adm)); [print('   ', x) for x in adm]
ph = collections.Counter(); p429 = []
for r in C:
    for n, v in r['P'].items():
        if v[1] is not None: ph[n] += 1
        if v[0] == 429: p429.append((n, r['verb'], r['path']))
print('non-machine principal routes WITH X-RateLimit-Limit', dict(ph), '| 429s', len(p429), p429[:5])
print('N/I/M with header:', sum(1 for r in C if r['N'][1] or r['I'][1] or r['M'][1]), '| N forwarded routes', sum(1 for r in C if r['Nhits']), '| I forwarded routes', sum(1 for r in C if r['Ihits']))
ctl = collections.Counter((r['C'][1] is not None, r['K'][0][2] is not None) for r in C); print('machine JWT control header vs key fires (ctl, key)->n', dict(ctl))
opt = [(r['verb'], r['path'], r['N'][0], r['Nhits'], r['I'][0], r['Ihits']) for r in C if r['optional']]
print('optional-auth statement routes:', len(opt)); [print('   ', o) for o in opt]
tf = collections.Counter(tuple(r['KtenantFwd']) == (('t-qa1017-c%d' % r['idx']),) for r in fires if r['Khits'][2]); print('fires+forwarded: x-tenant-id == key tenant ->', dict(tf))
for s in ('principals', 'a4', 'keyscope', 'erasure', 'bare', 'plant', 'order', 'redisthrow', 'perip'):
    if a.get(s): print('--', s); [print('   ', json.dumps(x)[:700]) for x in a[s]]
print('meta', json.dumps({k: v for k, v in a['meta'].items() if k != 'stages'})[:1500])
if len(sys.argv) > 2:
    b = load(sys.argv[2]); key = lambda r: (r['verb'], r['url'])
    bm = {key(r): r for r in b['census']}; diffs = 0
    strip = lambda r: {k: v for k, v in r.items() if k not in ('line',)}
    for r in C:
        o = bm.get(key(r))
        if o is None: print('ONLY IN', sys.argv[1], key(r)); diffs += 1; continue
        norm = lambda x: json.dumps({k: (v if k not in ('K', 'D') else [[y[0], y[1], y[2], y[3], y[4] is not None] for y in (v if k == 'K' else [v])]) for k, v in strip(x).items()}, sort_keys=True)
        if norm(r) != norm(o): diffs += 1; print('DIFF', key(r), '\n   A', norm(r)[:600], '\n   B', norm(o)[:600]) if diffs <= 12 else None
    print('only in', sys.argv[2], len(set(bm) - set(key(r) for r in C)))
    print('CENSUS ROW DIFFS', sys.argv[1], 'vs', sys.argv[2], diffs)
    for s in ('principals', 'a4', 'keyscope', 'erasure', 'bare', 'plant'):
        x = json.dumps(a.get(s), sort_keys=True); y = json.dumps(b.get(s), sort_keys=True); print('stage', s, 'identical' if x == y else 'DIFFERENT')
