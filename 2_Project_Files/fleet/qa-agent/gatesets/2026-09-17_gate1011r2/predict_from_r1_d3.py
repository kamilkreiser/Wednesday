#!/usr/bin/env python3
"""predict_from_r1_d3.py — DRAFTER PREDICTIONS (not measurements of 6dc825644). Reads the round-1 gate's census JSONs for base d067725ff and the D3
counterfactual (entry-time req.path into both fields), which the round-2 head implements. Classes every base->D3 row change against an
INDEPENDENT oracle computed from the request target alone (never from either tree's output): canonical(target) = drop absolute-form scheme+host,
drop #frag and ?query, collapse repeated slashes, /api/v1/ -> /api/ (index.ts:561 strip), following the recorded 307 hop. Plus a spelling-
invariance oracle: every user spelling of one route (c, v1, dbl, q, frag, abs, trail) should yield ONE (action, resource_type).
Read-only over the round-1 evidence; writes only to stdout."""
import json, re, collections, datetime
E = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-0a1f8900c-tier1-r1/evidence'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def canon(t):
    t = re.sub(r'^https?://[^/]*', '', t); t = t.split('#')[0].split('?')[0]; t = re.sub(r'/{2,}', '/', t)
    if t.startswith('/api/v1/'): t = '/api/' + t[len('/api/v1/'):]
    return t
def load(env, tree):
    o = json.load(open('%s/census_%s_%s.json' % (E, env, tree))); by = collections.defaultdict(list)
    for a in o['inserts']: by[a['ua'].split('~')[0]].append(a)
    return o, by
def key(rows): return [(x['action'], x['resourceType'], x['details'].get('path') if isinstance(x['details'], dict) else None) for x in rows]
P('predict_from_r1_d3', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
# oracle self-control: canon of planted targets
for t, want in (('http://h/api/v1/logs?x=1#f', '/api/logs'), ('//api//gdpr//erasures', '/api/gdpr/erasures'), ('/api/logs/', '/api/logs/'), ('/api/v2/verification/verify', '/api/v2/verification/verify')):
    assert canon(t) == want, (t, canon(t), want)
P('oracle controls: 4/4 planted targets canonicalise as expected')
D3ROWS = {}
for env in ('test', 'production'):
    ob, bb = load(env, 'base'); od, bd = load(env, 'd3'); D3ROWS[env] = (od, bd)
    c = collections.Counter(); ex = collections.defaultdict(list)
    for rb, rd in zip(ob['results'], od['results']):
        assert rb['ua'] == rd['ua']
        cls = rb['label'].split(' ')[0]; gd = 'gdpr' if ('/gdpr' in rb['target'].lower() or cls in ('GDPR', 'GET-CLAUSE')) else 'non-gdpr'
        adm = 'adm' if 0 < rd['hops'][-1]['status'] < 400 else 'ref'
        B, D = bb[rb['ua']], bd[rd['ua']]
        ct = canon(rd['hops'][-1]['target'])
        dpath_ok = all((x['details'].get('path') if isinstance(x['details'], dict) else None) == ct for x in D)
        bpath_ok = all((x['details'].get('path') if isinstance(x['details'], dict) else None) == ct for x in B)
        c['rows d3 path==canon %s' % dpath_ok] += len(D)
        if key(B) == key(D) and B == D: c['SAME/%s' % gd] += 1; continue
        k = 'DIFF/%s/%s' % (gd, adm) + ('/path:base-noncanon->d3-canon' if (dpath_ok and not bpath_ok) else '/path:both-canon' if (dpath_ok and bpath_ok) else '/path:d3-NONCANON')
        c[k] += 1; ex[k].append((rb['label'][:60], rb['target'][:48], [h['status'] for h in rd['hops']], key(B), key(D)))
    P('\n== %s: base d067725ff vs D3 (predicted head 6dc825644 rows) ==' % env)
    for k in sorted(c): P('  %-60s %d' % (k, c[k]))
    for k in sorted(ex):
        if 'both-canon' in k or 'NONCANON' in k:
            for e in ex[k][:6]: P('   ex', k, '|', e)
# spelling invariance on D3 and on base
for env in ('test', 'production'):
    for tree in ('base', 'd3'):
        o, by = load(env, tree); groups = collections.defaultdict(set); n = collections.Counter()
        for r in o['results']:
            m = re.match(r'^(c-user|v1-user|dbl-user|q-user|frag-user|abs-user|trail-user) (.*)$', r['label'])
            if not m: continue
            rows = by[r['ua']]; groups[m.group(2)].add(tuple((x['action'], x['resourceType']) for x in rows))
        inv = sum(1 for g in groups.values() if len(g) == 1)
        P('spelling invariance %-10s %-5s routes %d, one (action,resource_type) across the 7 user spellings: %d, split: %d' % (env, tree, len(groups), inv, len(groups) - inv))
        if tree == 'd3':
            for name, g in list((k, v) for k, v in groups.items() if len(v) > 1)[:8]: P('   split', name[:70], sorted(g)[:4])
# test vs production for D3 (same request, final-hop row)
(ot, bt), (op, bp) = D3ROWS['test'], D3ROWS['production']
same = diff = 0; exd = []
for rt, rp in zip(ot['results'], op['results']):
    if key(bt[rt['ua']]) == key(bp[rp['ua']]): same += 1
    else: diff += 1; exd.append((rt['label'][:60], key(bt[rt['ua']]), key(bp[rp['ua']]), [h['status'] for h in rt['hops']], [h['status'] for h in rp['hops']]))
P('\nD3 test-vs-production (action, resource_type, path) per request: same %d, differ %d' % (same, diff))
for e in exd[:12]: P('   ', e)
P('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
