#!/usr/bin/env python3
"""drafter_table_1034.py — grade the real-gateway probe rows (out/rows_probe_{head,dev}.json).
BLOCKER axis (lead Q1): a cell whose key takes the CONNECTOR branch (OK / REFUSED / DROPPED / NONJSON: valid key) with a caller Authorization, where ANY
upstream hit carries an Authorization byte-equal to the caller's. Per tree, per mode, per route, per key outcome.
PLANTED CONTROL: the grader must flag a synthetic head row copied from a develop N-1 row (proves the grader can see a forward).
Also: head vs develop cell-by-cell differences (status, forwarded classes) keyed by (mode, prefix, route, key, caller, occurrence); /api/batch rows;
the unversioned 307; exchange-HANG rows; client-error (-1) rows."""
import json, collections, copy, sys
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1034/out/'
R = {t: json.load(open(G + 'rows_probe_%s.json' % t)) for t in ('head', 'dev')}
CONN = {'OK', 'REFUSED', 'DROPPED', 'NONJSON'}
def blockers(rows): return [r for r in rows if r['key'] in CONN and r['caller'] != 'NONE' and any(h.get('eqCaller') for h in r['fwd'])]
def keyed(rows):
    seen = collections.Counter(); out = {}
    for r in rows:
        k = (r['mode'], r['prefix'], r['route'], r['key'], r['caller']); seen[k] += 1; out[k + (seen[k],)] = r
    return out
for t in ('head', 'dev'):
    rows = R[t]['rows']; b = blockers(rows)
    print('== %s: rows %d | connector-branch cells forwarding the caller Authorization: %d' % (t, len(rows), len(b)))
    agg = collections.Counter((r['mode'], r['prefix'], r['route'], r['key']) for r in b)
    per_route = collections.Counter((r['route'], r['src']) for r in b)
    print('   by route:', dict(per_route))
    print('   by (mode, prefix, key):', dict(collections.Counter((r['mode'], r['prefix'], r['key']) for r in b)))
    print('   upstream urls receiving it:', dict(collections.Counter(h['url'].split('?')[0] for r in b for h in r['fwd'] if h.get('eqCaller'))))
    print('   callers:', dict(collections.Counter(r['caller'] for r in b)), '| statuses:', dict(collections.Counter(r['status'] for r in b)))
dev_n1 = [r for r in R['dev']['rows'] if r['route'] == 'GET /api/credentials' and r['key'] == 'REFUSED' and r['caller'] == 'REVOKED']
plant = copy.deepcopy(dev_n1[0]) if dev_n1 else None
print('PLANTED CONTROL: a develop N-1 row (/api/credentials REFUSED REVOKED) appended to head rows is flagged:', bool(plant) and len(blockers(R['head']['rows'] + [plant])) == len(blockers(R['head']['rows'])) + 1, '| its forwarded classes', [h['cls'] for h in plant['fwd']] if plant else None)
kh, kd = keyed(R['head']['rows']), keyed(R['dev']['rows'])
print('== head vs develop: keys head %d dev %d common %d' % (len(kh), len(kd), len(set(kh) & set(kd))))
diff = []
for k in sorted(set(kh) & set(kd)):
    a, b_ = kh[k], kd[k]
    sa = (a['status'], tuple(sorted((h['cls'], h['eqCaller']) for h in a['fwd'])))
    sb = (b_['status'], tuple(sorted((h['cls'], h['eqCaller']) for h in b_['fwd'])))
    if sa != sb: diff.append((k, sb, sa))
print('cells that differ head vs develop:', len(diff))
cls = collections.Counter((k[3], k[4], str(sb[1]), str(sa[1]), sb[0] == sa[0]) for k, sb, sa in diff)
for c, n in sorted(cls.items(), key=lambda x: -x[1]): print('   %4d key=%s caller=%s | dev fwd %s -> head fwd %s | status equal %s' % (n, c[0], c[1], c[2], c[3], c[4]))
print('   differing cells on a NON-connector key (NOKEY/JUNK):', sum(1 for k, _, _ in diff if k[3] not in CONN), '| on caller NONE:', sum(1 for k, _, _ in diff if k[4] == 'NONE'))
status_diff = [(k, sb[0], sa[0]) for k, sb, sa in diff if sb[0] != sa[0]]
print('   status differences:', len(status_diff), status_diff[:10])
for t in ('head', 'dev'):
    rows = R[t]['rows']
    bt = [r for r in rows if r['route'] == 'POST /api/batch/verify']
    print('== %s /api/batch/verify: %d rows | statuses %s | codes %s | hits %d | connector-branch evidence (x-user-id connector:*) %d' % (t, len(bt), dict(collections.Counter(r['status'] for r in bt)), dict(collections.Counter(r['code'] for r in bt)), sum(len(r['fwd']) for r in bt), sum(1 for r in bt for h in r['fwd'] if str(h.get('userId') or '').startswith('connector:'))))
    print('   %s client-error rows (-1): %s' % (t, dict(collections.Counter((r['mode'], r['route'], r['code']) for r in rows if r['status'] == -1))))
    print('   %s 307 unversioned production: %s' % (t, R[t]['meta'].get('prod307', {}).get('status')))
    for h in R[t]['hang']: print('   %s HANG row: %s %s -> %s %s fwd %s' % (t, h['path'], h['what'][:50], h['status'], h['code'], [x['cls'] for x in h['fwd']]))
    ok = [r for r in rows if r['key'] == 'OK' and r['caller'] == 'NONE']
    print('   %s key-only OK cells: %d | forwarded connector-jwt on every hit: %s' % (t, len(ok), all(h['cls'] == 'connector-jwt' for r in ok for h in r['fwd'])))
    live = [r for r in rows if r['key'] == 'NOKEY' and r['caller'] == 'LIVE']
    print('   %s live JWT alone cells: %d | every hit carries the caller Bearer: %s | hits %d' % (t, len(live), all(h['eqCaller'] for r in live for h in r['fwd']), sum(len(r['fwd']) for r in live)))
    rv = [r for r in rows if r['key'] in ('NOKEY', 'JUNK') and r['caller'] == 'REVOKED']
    print('   %s revoked JWT without a valid key: %d cells | forwarded: %d | statuses %s' % (t, len(rv), sum(len(r['fwd']) for r in rv), dict(collections.Counter(r['status'] for r in rv))))
