#!/usr/bin/env python3
"""drafter_table.py — head vs develop rows of qa1023-drafter-probe (rows/rows_head_head.json, rows/rows_dev_dev.json): per (mode, prefix, mount, case) a compact cell
status/code/fwd-userId/bearerSub/validates/sessions/tenants, the diff list, and the classifications Wednesday's lead questions need."""
import json, os, collections
GS = os.path.dirname(os.path.abspath(__file__))
H = json.load(open(GS + '/rows/rows_head_head.json')); D = json.load(open(GS + '/rows/rows_dev_dev.json'))
def cell(r):
    f = r.get('fwd') or []
    return '%s %s fwd=%s bearer=%s key-fwd=%s val=%s sess=%s ten=%s' % (r['status'], r['code'], [x['userId'] for x in f], [x['bearerSub'] for x in f], [x['apiKeyFwd'] for x in f],
        r.get('validates'), len(r.get('sessions') or []), [ (t or 'null')[:8] for t in (r.get('tenants') or [])])
for mode in ('test', 'prod'):
    print('=' * 3, mode, 'rows head', len(H[mode]), 'dev', len(D[mode]))
    diffs = 0; bycase = collections.Counter(); samecase = collections.Counter()
    for h, d in zip(H[mode], D[mode]):
        assert (h['mount'], h['prefix'], h['case']) == (d['mount'], d['prefix'], d['case'])
        ch, cd = cell(h), cell(d)
        if ch != cd:
            diffs += 1; bycase[(h['case'])] += 1
            print('DIFF %-8s %-24s %-16s | dev: %s\n%57s head: %s' % (h['prefix'], h['mount'], h['case'], cd, '', ch))
        else: samecase[h['case']] += 1
    print(mode, 'diff rows', diffs, 'by case', dict(bycase))
    print(mode, 'identical rows by case', dict(samecase))
    # STILL OPEN oracle: any revoked-session JWT row forwarded or 2xx at head
    bad = [(h['prefix'], h['mount'], h['case'], h['status'], h['code']) for h in H[mode] if 'REVOKED' in h['case'] and (h['fwd'] or (200 <= (h['status'] or 0) < 300))]
    print(mode, 'HEAD revoked-session rows forwarded or 2xx (STILL OPEN oracle):', len(bad), bad[:12])
    badd = [(h['prefix'], h['mount'], h['case'], h['status']) for h in D[mode] if 'REVOKED' in h['case'] and (h['fwd'] or (200 <= (h['status'] or 0) < 300))]
    print(mode, 'DEV revoked-session rows forwarded or 2xx:', len(badd), sorted(collections.Counter((x[2]) for x in badd).items()))
    print(mode, 'HEAD sample per case on credentials /api%s:' % ('/v1' if mode == 'prod' else ''))
    for h in H[mode]:
        if h['mount'] in ('credentials', 'certifications', 'settings-notifications', 'documents') and h['prefix'] == ('/api/v1' if mode == 'prod' else '/api'):
            print('   %-22s %-16s %s' % (h['mount'], h['case'], cell(h)))
print('=== limiter')
for tag, R in (('head', H), ('dev', D)):
    for r in R['limiter']:
        print('  %-4s %-36s %s %s rlRem=%s incr=%s tenants=%s fwd=%s' % (tag, r['id'], r['status'], r['code'], r['rlRemaining'], r.get('incr'), [(t or 'null')[:8] for t in r.get('tenants') or []], [x['userId'] for x in r['fwd']]))
