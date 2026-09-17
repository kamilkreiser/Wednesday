#!/usr/bin/env python3
"""repin_table_1034.py — grade the RE-PIN census at head e4624218b (out_repin/rows_probe_head.json) against the drafter's rows at fd81a75f0
(out/rows_probe_head.json) and at develop 27e53ec3a (out/rows_probe_dev.json; develop 3961c2add has the SAME api-gateway + shared subtrees: dea998d3f / dbd72dea0,
out_repin/repin_setup.out). Same BLOCKER axis and planted control as drafter_table_1034.py. Plus the admin register-connector cells (OUT.admin)."""
import json, collections, copy
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1034/'
R = {'e4624218b': json.load(open(G + 'out_repin/rows_probe_head.json')), 'fd81a75f0': json.load(open(G + 'out/rows_probe_head.json')), 'dev27e53ec3a': json.load(open(G + 'out/rows_probe_dev.json'))}
CONN = {'OK', 'REFUSED', 'DROPPED', 'NONJSON'}
def blockers(rows): return [r for r in rows if r['key'] in CONN and r['caller'] != 'NONE' and any(h.get('eqCaller') for h in r['fwd'])]
def keyed(rows):
    seen = collections.Counter(); out = {}
    for r in rows:
        k = (r['mode'], r['prefix'], r['route'], r['key'], r['caller']); seen[k] += 1; out[k + (seen[k],)] = r
    return out
for t, d in R.items():
    rows = d['rows']; b = blockers(rows)
    print('== %s: rows %d | connector-branch cells forwarding the caller Authorization: %d | by route %s | upstream urls %s' % (t, len(rows), len(b), dict(collections.Counter(r['route'] for r in b)), dict(collections.Counter(h['url'].split('?')[0] for r in b for h in r['fwd'] if h.get('eqCaller')))))
H = R['e4624218b']['rows']
dev_n1 = [r for r in R['dev27e53ec3a']['rows'] if r['route'] == 'GET /api/credentials' and r['key'] == 'REFUSED' and r['caller'] == 'REVOKED']
print('PLANTED CONTROL: develop N-1 row appended to e4624218b rows is flagged:', len(blockers(H + [copy.deepcopy(dev_n1[0])])) == len(blockers(H)) + 1)
reg_old = [r for r in blockers(R['fd81a75f0']['rows'])]
print('PLANTED CONTROL 2: an fd81a75f0 register-connector forward row appended is flagged:', len(blockers(H + [copy.deepcopy(reg_old[0])])) == len(blockers(H)) + 1)
def compare(a, b, label):
    ka, kb = keyed(R[a]['rows']), keyed(R[b]['rows']); diff = []
    for k in sorted(set(ka) & set(kb)):
        x, y = ka[k], kb[k]
        sx = (x['status'], tuple(sorted((h['cls'], h['eqCaller']) for h in x['fwd']))); sy = (y['status'], tuple(sorted((h['cls'], h['eqCaller']) for h in y['fwd'])))
        if sx != sy: diff.append((k, sx, sy))
    print('== %s: keys %d / %d common %d | cells differing %d | status differences %d | on NOKEY/JUNK %d | on caller NONE %d' % (label, len(ka), len(kb), len(set(ka) & set(kb)), len(diff), sum(1 for _, sx, sy in diff if sx[0] != sy[0]), sum(1 for k, _, _ in diff if k[3] not in CONN), sum(1 for k, _, _ in diff if k[4] == 'NONE')))
    print('   by route:', dict(collections.Counter(k[2] for k, _, _ in diff)))
    cls = collections.Counter((k[3], k[4], str(sx[1]), str(sy[1])) for k, sx, sy in diff)
    for c, n in sorted(cls.items(), key=lambda x: -x[1])[:12]: print('   %4d key=%s caller=%s | %s -> %s' % (n, c[0], c[1], c[2][:110], c[3][:110]))
    return diff
compare('fd81a75f0', 'e4624218b', 'fd81a75f0 -> e4624218b')
compare('dev27e53ec3a', 'e4624218b', 'develop (27e53ec3a = 3961c2add by subtree) -> e4624218b')
rc = [r for r in H if r['route'].endswith('register-connector')]
print('== e4624218b register-connector cells:', len(rc), '| by (key, caller) -> status, forwarded classes (first of each):')
seen = set()
for r in rc:
    k = (r['mode'], r['prefix'], r['key'], r['caller'])
    if (r['key'], r['caller']) in seen: continue
    seen.add((r['key'], r['caller'])); print('   %-8s %-7s %s %s' % (r['key'], r['caller'], r['status'], [(h['url'], h['cls'], h['eqCaller']) for h in r['fwd']]))
plat = [r for r in H if 'platform' in r['src']]
print('== e4624218b platform.ts routes: cells', len(plat), '| routes', len({r['route'] for r in plat}), '| caller-forward on connector branch', len(blockers(plat)))
print('== admin cells (JWT-only SYSTEM_ADMIN; OUT.admin):')
for a in R['e4624218b'].get('admin', []): print('   %-10s %-8s %-28s -> %s %s fwd %s' % (a['mode'], a['prefix'], a['what'], a['status'], a['code'], [(h['url'], h['cls'], h['eqCaller']) for h in a['fwd']]))
for t in ('e4624218b',):
    rows = R[t]['rows']
    bt = [r for r in rows if r['route'] == 'POST /api/batch/verify']
    print('== %s /api/batch/verify: %d rows statuses %s hits %d' % (t, len(bt), dict(collections.Counter(r['status'] for r in bt)), sum(len(r['fwd']) for r in bt)))
    print('   client-error rows (-1):', dict(collections.Counter((r['mode'], r['route'], r['code']) for r in rows if r['status'] == -1)))
    print('   307 unversioned production:', R[t]['meta'].get('prod307', {}).get('status'))
    for h in R[t]['hang']: print('   HANG row: %s %s -> %s %s fwd %s' % (h['path'], h['what'][:50], h['status'], h['code'], [x['cls'] for x in h['fwd']]))
    ok = [r for r in rows if r['key'] == 'OK' and r['caller'] == 'NONE']
    print('   key-only OK cells: %d | connector-jwt on every hit: %s | hits %d' % (len(ok), all(h['cls'] == 'connector-jwt' for r in ok for h in r['fwd']), sum(len(r['fwd']) for r in ok)))
    live = [r for r in rows if r['key'] == 'NOKEY' and r['caller'] == 'LIVE']
    print('   live JWT alone: %d cells | every hit carries the caller Bearer: %s | hits %d' % (len(live), all(h['eqCaller'] for r in live for h in r['fwd']), sum(len(r['fwd']) for r in live)))
    rv = [r for r in rows if r['key'] in ('NOKEY', 'JUNK') and r['caller'] == 'REVOKED']
    print('   revoked JWT without a valid key: %d cells | forwarded %d | statuses %s' % (len(rv), sum(len(r['fwd']) for r in rv), dict(collections.Counter(r['status'] for r in rv))))
