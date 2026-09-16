#!/usr/bin/env python3
"""drafter_compare.py — compare probe_rows_{base,head,merged}.json (drafter probe) against an INDEPENDENT oracle written here from the ruling's words,
not from enforcement.ts: rank(level) = index in the 7 known lowercase levels after (level or 'none').lower(), else UNKNOWN. Ruling: an UNKNOWN user level ranks
as 'none'; known levels unchanged; UNKNOWN required unchanged (passes every authenticated principal). Planted controls: the classifier must flag a planted
wider-opening row and a planted known-level change. Prints every base != head row."""
import json, collections, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
L = {t: json.load(open('%s/probe_rows_%s.json' % (GS, t))) for t in ('base', 'head', 'merged')}
K = ['none', 'basic', 'social', 'standard', 'enhanced', 'high', 'government']
def rank(x):
    s = (x or 'none').lower()
    return K.index(s) if s in K else None
def oracle_base(u, r):
    ui, ri = rank(u), rank(r)
    return (-1 if ui is None else ui) >= (-1 if ri is None else ri)
def oracle_head(u, r):
    ui, ri = rank(u), rank(r)
    if ri is None: return True
    return (0 if ui is None else ui) >= ri
# 1. pure function vs oracle
for t in ('base', 'head', 'merged'):
    orc = oracle_base if t == 'base' else oracle_head
    fn = [x for x in L[t]['rows'] if x['kind'] == 'fn']
    bad = [x for x in fn if x['result'] != orc(x['user'], x['required'])]
    print('fn %-6s rows %d oracle-mismatch %d %s' % (t, len(fn), len(bad), bad[:5]))
bh = [(b, h) for b, h in zip([x for x in L['base']['rows'] if x['kind'] == 'fn'], [x for x in L['head']['rows'] if x['kind'] == 'fn'])]
assert all(b['user'] == h['user'] and b['required'] == h['required'] for b, h in bh)
flips = [(b['user'], b['required'], b['result'], h['result']) for b, h in bh if b['result'] != h['result']]
print('fn base->head flips', len(flips))
cls = collections.Counter()
for u, r, bres, hres in flips:
    cls[('user-unknown' if rank(u) is None else 'user-KNOWN', 'req=' + (K[rank(r)] if rank(r) is not None else 'UNKNOWN'), '%s->%s' % (bres, hres))] += 1
for k, v in sorted(cls.items()): print('   flip class', k, v)
print('   known-user flips (must be 0):', sum(v for k, v in cls.items() if k[0] == 'user-KNOWN'), '| flips above none (must be 0):', sum(v for k, v in cls.items() if k[1] not in ('req=none',)))
print('   nonstring base', [(x['user'], x['required'], x['result']) for x in L['base']['rows'] if x['kind'] == 'fn-nonstring'])
print('   nonstring head', [(x['user'], x['required'], x['result']) for x in L['head']['rows'] if x['kind'] == 'fn-nonstring'])
# planted controls for the flip classifier
planted = [('api_key', 'basic', False, True), ('standard', 'standard', True, False)]
pc = [('user-unknown' if rank(u) is None else 'user-KNOWN', 'req=' + (K[rank(r)] if rank(r) is not None else 'UNKNOWN')) for u, r, _, _ in planted]
print('   planted controls classify as', pc, '(want one above-none, one KNOWN)')
# 2. HTTP rows
def key(x): return (x['kind'], x['principal'], x['type'])
for a, b in (('base', 'head'), ('head', 'merged')):
    A = {key(x): x for x in L[a]['rows'] if x['kind'] in ('create', 'verify')}
    B = {key(x): x for x in L[b]['rows'] if x['kind'] in ('create', 'verify')}
    assert A.keys() == B.keys(), (a, b)
    diff = [(k, A[k]['status'], A[k]['code'], B[k]['status'], B[k]['code'], B[k].get('forwarded'), B[k].get('workflowInstances')) for k in sorted(A, key=str) if (A[k]['status'], A[k]['code'], A[k].get('forwarded'), A[k].get('workflowInstances')) != (B[k]['status'], B[k]['code'], B[k].get('forwarded'), B[k].get('workflowInstances'))]
    print('HTTP %s vs %s: rows %d (create %d, verify %d) DIFF %d' % (a, b, len(A), sum(1 for k in A if k[0] == 'create'), sum(1 for k in A if k[0] == 'verify'), len(diff)))
    byp = collections.defaultdict(list)
    for d in diff: byp[(d[0][0], d[0][1])].append('%s %s/%s->%s/%s fwd%s wf%s' % (d[0][2], d[1], d[2], d[3], d[4], d[5], d[6]))
    for k, v in byp.items(): print('   ', k, len(v), v)
types = {x['type']: x.get('verifierLevel') for x in L['head']['rows'] if x['kind'] == 'verify'}
print('verify DIFF base vs head by construction: see above (0 expected: verifierLevel lowercased, none skipped, unknown passes both)')
# 3. what a forwarded connector-created document carries vs a human one (head)
H = [x for x in L['head']['rows'] if x['kind'] == 'create' and x['type'] == 'SSD_DOCUMENT' and x['forwardedHit']]
for x in H: print('   head SSD_DOCUMENT forwarded', x['principal'], x['forwardedHit'])
