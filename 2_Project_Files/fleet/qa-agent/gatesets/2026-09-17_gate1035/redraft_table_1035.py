#!/usr/bin/env python3
"""redraft_table_1035.py — grades out/r2/probe/rows_*.json (the real-app census) with an ORACLE written from the rulings, not from verification.ts:
KS-1204 + the accepted veto defaults: a connector whose stored allowedDocumentTypes is present, not null and not an array -> EVERY create 403 FORBIDDEN (typed or untyped),
before enforcement, nothing forwarded; absent / null / array -> exactly develop's answer. Planted controls must be flagged. Also: head vs develop vs merged, test vs
production, the dead drafter's 23:53 rows vs these, the connector-info reader, the container shapes, the path controls, the array-like rows. Read only."""
import json, os, collections, datetime
GS = os.path.dirname(os.path.abspath(__file__)); N = GS + '/out/r2/probe/'; O = GS + '/out/probe/'
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
def load(p): return json.load(open(p))
U = load(N + 'universe.json'); NONARR = {}
for lab, cid, named in U['configs']:
    NONARR[cid] = None
print('redraft_table_1035', now())
def shape_of(cid):  # the STORED shape per the probe's CONFIGS (re-derived from the admin echo of the first PUT)
    return SH.get(cid)
def key(r): return (r['group'], r.get('config_label'), r['connector'], r['shape'], r.get('path'))
def cls(r): return (r.get('status'), r.get('layer'), r.get('forwarded'))
R = {}
for tree in ('head', 'dev', 'merged'):
    for ne in ('test', 'production'):
        R[(tree, ne)] = load(N + 'rows_%s_%s_census.json' % (tree, ne))
first = R[('head', 'test')]['admin'][0]; cids = [c[1] for c in U['configs'] if c[1] != 'c-obj-arraylike']
SH = dict(zip(cids, first['stored_allow_shapes']))
print('stored shapes (admin echo of the ONE SYSTEM_ADMIN PUT, head test):', SH)
def oracle(tree, r, devrow):
    if r['group'] != 'A': return None
    sh = SH[r['connector']]
    if sh in ('undefined', 'null', 'array'):
        return ('SAME-AS-DEVELOP', cls(devrow))
    return ('REFUSE', (403, 'ALLOWLIST-NONARRAY-403', 0))
for ne in ('test', 'production'):
    for tree in ('head', 'merged', 'dev'):
        rows = R[(tree, ne)]['rows']; dev = {key(x): x for x in R[('dev', ne)]['rows']}
        cr = [r for r in rows if r['group'] != 'info']
        dist = collections.Counter('%s %s%s' % (r['status'], r['layer'], ' fwd' if r['forwarded'] else '') for r in cr)
        bad = []; n_or = 0
        for r in cr:
            o = oracle(tree, r, dev[key(r)])
            if not o: continue
            n_or += 1
            if tree == 'dev': continue
            if cls(r) != o[1]: bad.append((r['connector'], r['shape'], cls(r), o))
        print('\n[%s %s] meta pre=%s seed=%s | create rows %d | %s' % (tree, ne, R[(tree, ne)]['meta']['pre'], R[(tree, ne)]['meta']['seed']['status'], len(cr), dict(dist)))
        if tree != 'dev':
            print('   ORACLE (group A, %d rows): violations %d %s' % (n_or, len(bad), bad[:6]))
            msgs = collections.Counter((r['code'], r['msg']) for r in cr if r['layer'] == 'ALLOWLIST-NONARRAY-403'); print('   non-array refusals by (code, message):', dict(msgs))
            arr_rows = [r for r in cr if r['group'] == 'A' and SH[r['connector']] in ('undefined', 'null', 'array')]
            print('   absent/null/array-configured rows %d, differing from develop %d' % (len(arr_rows), sum(cls(r) != cls(dev[key(r)]) for r in arr_rows)))
            diff = [r for r in cr if cls(r) != cls(dev[key(r)])]
            print('   rows differing from develop: %d | by config %s' % (len(diff), dict(collections.Counter(r['config_label'] for r in diff))))
            wid = [r for r in diff if r['forwarded'] and not dev[key(r)]['forwarded']]; print('   rows that FORWARD at %s but not at develop (a widening): %d %s' % (tree, len(wid), [(r['config_label'], r['shape']) for r in wid][:5]))
# planted controls for the grader
dev = {key(x): x for x in R[('dev', 'test')]['rows']}
h = [dict(r) for r in R[('head', 'test')]['rows']]
p1 = next(r for r in h if r['group'] == 'A' and r['connector'] == 'c-str-empty' and r['shape'] == 'untyped'); p1.update(status=201, layer='FORWARDED', forwarded=1)
p2 = next(r for r in h if r['group'] == 'A' and r['connector'] == 'c-arr-ssd' and r['shape'] == 'dt:SSD_DOCUMENT'); p2.update(status=403, layer='ALLOWLIST-NONARRAY-403', forwarded=0)
fl = [(r['connector'], r['shape']) for r in h if oracle('head', r, dev[key(r)]) and cls(r) != oracle('head', r, dev[key(r)])[1]]
print('\nPLANTED CONTROLS (empty string untyped forwarded; an array connector refused as non-array): grader flags', fl, '| both flagged:', len(fl) == 2)
# head vs merged identical; test vs production identical per row (group A/B/D, excluding the path controls)
for ne in ('test', 'production'):
    a = {key(x): cls(x) for x in R[('head', ne)]['rows'] if x['group'] != 'info'}; b = {key(x): cls(x) for x in R[('merged', ne)]['rows'] if x['group'] != 'info'}
    print('head vs merged (%s): rows %d / %d, differing %d' % (ne, len(a), len(b), sum(a[k] != b.get(k) for k in a)))
for tree in ('head', 'dev', 'merged'):
    t = {key(x)[:4]: cls(x) for x in R[(tree, 'test')]['rows'] if x['group'] in ('A', 'B', 'D')}; p = {key(x)[:4]: cls(x) for x in R[(tree, 'production')]['rows'] if x['group'] in ('A', 'B', 'D')}
    print('test vs production (%s, groups A/B/D): rows %d / %d, differing %d %s' % (tree, len(t), len(p), sum(t[k] != p.get(k) for k in t), [k for k in t if t[k] != p.get(k)][:4]))
# the dead drafter's 23:53 rows vs these (test census, head and develop 732c13459)
for tree in ('head', 'dev'):
    old = {key(x)[:4]: cls(x) for x in load(O + 'rows_%s_test_census.json' % tree)['rows'] if x['group'] != 'P'}
    new = {key(x)[:4]: cls(x) for x in R[(tree, 'test')]['rows'] if x['group'] != 'P'}
    print('dead drafter 23:53 (%s, develop then 732c13459) vs re-run (%s): rows %d / %d, differing %d' % (tree, 'develop 3961c2add' if tree == 'dev' else 'head', len(old), len(new), sum(old[k] != new.get(k) for k in old)))
# the connector-info reader (health.ts) vs the create refusal
print('\nGET /api/connector/info (what the connector is TOLD) vs create at head (test):')
hr = R[('head', 'test')]['rows']
for lab, cid, named in U['configs']:
    if cid == 'c-obj-arraylike': continue
    info = next((r for r in hr if r['group'] == 'info' and r['connector'] == cid), None)
    creates = [r for r in hr if r['group'] == 'A' and r['connector'] == cid]
    ref = sum(r['layer'] == 'ALLOWLIST-NONARRAY-403' for r in creates)
    iv = info['info_allowedDocumentTypes'] if info else None
    flag = 'DISAGREES (told [] = all types permitted, every create refused)' if ref == len(creates) and iv == [] else ('told a non-list, every create refused' if ref == len(creates) else '')
    print('   %-45s stored %-9s info %-32s creates refused %2d/%d %s' % (lab[:45], SH[cid], json.dumps(iv)[:32], ref, len(creates), flag))
for ne in ('test', 'production'):
    for tree in ('head', 'dev'):
        a = [x for x in R[(tree, ne)]['admin']]
        print('\n[%s %s] admin writes:' % (tree, ne)); [print('   ', {k: v for k, v in x.items() if k not in ('stored_allow_shapes',)}) for x in a]
        rows = [x for x in R[(tree, ne)]['rows'] if x['group'] in ('B', 'D', 'P')]
        for x in rows: print('    %s | %-55s | %-18s | %s %s %s | %s' % (x['group'], x['config_label'][:55], x['shape'], x['status'], x['layer'], 'fwd' if x['forwarded'] else '', x.get('ctype')))
for tree in ('head', 'dev', 'merged'):
    for ne in ('test', 'production'):
        for mode in ('unset', 'survive'):
            j = load(N + 'rows_%s_%s_arraylike_%s.json' % (tree, ne, mode))
            print('arraylike %-6s %-10s %-7s' % (tree, ne, mode), [(x['config_label'][:20], x['status'], x['code'], x['layer']) for x in j['rows']])
