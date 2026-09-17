#!/usr/bin/env python3
"""drafter_compare.py — #1019 ROUND 2 drafter: round 1's GATE harness rows. (1) r1 column vs round 1's own rows (rows_head.json, rows_origin_head.json): byte sha
and per-row equality; (2) r2 vs r1, head vs r2: every row diff by stage/id/tok/rep; (3) tallies per class: W no-scope, W with-scope, door, not-door census (N*, O*),
undetermined, grace, urlspy, limiter, originate calls. Fields compared: status, code, hits, location, rlRemaining, originateCalls, headerErr (+ graceSpyCalls)."""
import json, hashlib, datetime, collections
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019r2'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/evidence'
print('drafter_compare', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
L = lambda p: json.load(open(p))
F = ('status', 'code', 'hits', 'location', 'rlRemaining', 'originateCalls', 'headerErr', 'graceSpyCalls', 'finalUrl', 'writes')
def key(stage, r): return (stage, r.get('mode'), r.get('id'), r.get('tok'), r.get('rep'), r.get('method'), r.get('target'), r.get('probe'))
def rows(d, stages):
    out = collections.OrderedDict()
    for st in stages:
        for r in d.get(st, []):
            k = key(st, r); n = 0
            while k + (n,) in out: n += 1
            out[k + (n,)] = {f: r.get(f) for f in F}
    return out
ST = ['verdict', 'test', 'grace', 'prod', 'limiter', 'noemail', 'urlspy']
def vt(d):
    return {v['sub']: (v['ci'], v['cs']) for v in d.get('verdict', [])}
def diff(a, b, la, lb, show=400):
    ks = list(a.keys()); n = 0; lines = []
    missing = [k for k in ks if k not in b] + [k for k in b if k not in a]
    for k in ks:
        if k in b and a[k] != b[k]:
            n += 1
            if len(lines) < show: lines.append('   %s | %s: %s | %s: %s' % (' '.join(str(x) for x in k[:7] if x is not None), la, json.dumps([a[k][f] for f in ('status', 'code', 'hits', 'rlRemaining') ])[:160], lb, json.dumps([b[k][f] for f in ('status', 'code', 'hits', 'rlRemaining')])[:160]))
    return n, missing, lines
g1 = L(R1 + '/rows_head.json'); o1 = L(R1 + '/rows_origin_head.json')
d = {t: L(GS + '/rows/rows_%s_%s.json' % (t, t)) for t in ('r1', 'r2', 'head')}
o = {t: L(GS + '/rows/rows_origin_%s.json' % t) for t in ('r1', 'r2', 'head')}
print('== (1) r1 column vs ROUND 1 GATE rows')
print('  bytes sha: round1 rows_head.json', sha(R1 + '/rows_head.json'), '| drafter rows_r1', sha(GS + '/rows/rows_r1_r1.json'), '| equal:', sha(R1 + '/rows_head.json') == sha(GS + '/rows/rows_r1_r1.json'))
print('  bytes sha: round1 rows_origin_head.json', sha(R1 + '/rows_origin_head.json'), '| drafter rows_origin_r1', sha(GS + '/rows/rows_origin_r1.json'), '| equal:', sha(R1 + '/rows_origin_head.json') == sha(GS + '/rows/rows_origin_r1.json'))
a = rows(g1, ST); b = rows(d['r1'], ST)
n, miss, lines = diff(a, b, 'round1', 'r1'); print('  rows round1', len(a), 'r1', len(b), '| row diffs', n, '| missing keys', len(miss), '| verdict table equal', vt(g1) == vt(d['r1']), '| jwksFetches', g1.get('jwksFetches'), d['r1'].get('jwksFetches'))
for l in lines[:20]: print(l)
a = rows(o1, ['originate']); b = rows(o['r1'], ['originate'])
n, miss, lines = diff(a, b, 'round1', 'r1'); print('  originate rows round1', len(a), 'r1', len(b), '| row diffs', n, '| missing', len(miss))
for l in lines[:20]: print(l)
print('  CONTROL (instrument can see a diff): round1 rows_head vs drafter rows_r2 diffs =', diff(rows(g1, ST), rows(d['r2'], ST), 'a', 'b')[0])
print('== (2) r2 vs r1 (the round-2 delta), every row diff')
n, miss, lines = diff(rows(d['r1'], ST), rows(d['r2'], ST), 'r1', 'r2', 1000); print('  row diffs', n, '| missing', len(miss))
for l in lines: print(l)
vr1, vr2 = vt(d['r1']), vt(d['r2'])
vd = [(s, vr1[s], vr2.get(s)) for s in vr1 if vr1[s] != vr2.get(s)]
print('  verdict table subs', len(vr1), '| r1 != r2:', len(vd))
for s, x, y in vd: print('   verdict', repr(s), '| r1 ci', x[0]['verdict'], 'cs', x[1]['verdict'], '| r2 ci', y[0]['verdict'], 'cs', y[1]['verdict'])
n, miss, lines = diff(rows(o['r1'], ['originate']), rows(o['r2'], ['originate']), 'r1', 'r2', 1000); print('  originate row diffs r1->r2', n)
for l in lines: print(l)
print('== (3) head vs r2 (the develop merge-in)')
n, miss, lines = diff(rows(d['r2'], ST), rows(d['head'], ST), 'r2', 'head', 1000); print('  row diffs', n, '| missing', len(miss), '| verdict table equal', vt(d['r2']) == vt(d['head']))
for l in lines: print(l)
n, miss, lines = diff(rows(o['r2'], ['originate']), rows(o['head'], ['originate']), 'r2', 'head', 1000); print('  originate row diffs r2->head', n)
for l in lines: print(l)
print('== (4) tallies per tree')
for t in ('r1', 'r2', 'head'):
    for st in ('test', 'prod'):
        rs = d[t][st]
        def tally(pred):
            c = collections.Counter()
            for r in rs:
                if pred(r): c[(r['status'], r['code'], len(r['hits']))] += 1
            return dict(c)
        print('  %s %s | W no-scope (noscope/user/noemail_noscope):' % (t, st), tally(lambda r: r['cls'] == 'W' and r['tok'] in ('noscope', 'user', 'noemail_noscope')))
        print('  %s %s | W with scope:' % (t, st), tally(lambda r: r['cls'] == 'W' and r['tok'] == 'scope'))
        print('  %s %s | door no-scope:' % (t, st), tally(lambda r: r['cls'] == 'door' and r['tok'] in ('noscope', 'user', 'noemail_noscope')))
        print('  %s %s | door scope:' % (t, st), tally(lambda r: r['cls'] == 'door' and r['tok'] == 'scope'))
        print('  %s %s | not-door spellings N* (both toks):' % (t, st), tally(lambda r: r['cls'] == 'not-door'))
        print('  %s %s | originate routes O* non-door:' % (t, st), tally(lambda r: r['cls'] == 'originate-route'), '| O* door routes:', tally(lambda r: r['cls'] == 'originate-door-route'))
        print('  %s %s | undetermined:' % (t, st), tally(lambda r: r['cls'] == 'undetermined'))
    print('  %s grace:' % t, [(r['id'][:14], r['status'], r['code'], len(r['hits']), r['graceSpyCalls']) for r in d[t]['grace']])
    print('  %s limiter:' % t, [(r['id'], r['status'], r['code'], r['rlRemaining']) for r in d[t]['limiter']])
    print('  %s urlspy probes:' % t, [(r['method'], r['target'][-24:], r['tok'], r['status'], r['code'], len(r['hits'])) for r in d[t]['urlspy'] if r.get('probe')])
    oc = collections.Counter((r['mode'], r['id'][:12], r['tok'], r['status'], r['code'], tuple(c['fn'] for c in r['originateCalls'])) for r in o[t]['originate'])
    print('  %s originate stage (mode, id, tok, status, code, handler calls) x count:' % t)
    for k, v in sorted(oc.items()): print('     ', k, 'x', v)
print('== (5) head vs r2 ignoring rlRemaining (status, code, hits, location, originateCalls, headerErr, graceSpyCalls equal?)')
def strip(rs):
    return collections.OrderedDict((k, {f: v for f, v in r.items() if f != 'rlRemaining'}) for k, r in rs.items())
n, miss, lines = diff(strip(rows(d['r2'], ST)), strip(rows(d['head'], ST)), 'r2', 'head', 50); print('  non-limiter row diffs r2->head', n, '| missing', len(miss))
for l in lines: print(l)
n, miss, lines = diff(strip(rows(o['r2'], ['originate'])), strip(rows(o['head'], ['originate'])), 'r2', 'head', 50); print('  non-limiter originate row diffs r2->head', n)
for l in lines: print(l)
c = collections.Counter(r['rlRemaining'] is None for st in ('test', 'prod') for r in d['head'][st])
print('  head test+prod rows with an X-RateLimit-Remaining header:', c[False], 'without:', c[True])
nohdr = collections.Counter((r['status'], r['code']) for st in ('test', 'prod') for r in d['head'][st] if r['rlRemaining'] is None)
print('  head rows WITHOUT the header by (status, code):', dict(nohdr))
