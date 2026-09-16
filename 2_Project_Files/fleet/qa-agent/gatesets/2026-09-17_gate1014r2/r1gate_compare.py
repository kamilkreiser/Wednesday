#!/usr/bin/env python3
"""compare.py A B [label] — compare census rows of two trees against an oracle written from Wednesday's RULING's words:
 'an UNRECOGNISED user level satisfies a none requirement and nothing higher; known levels unchanged; the unknown-REQUIRED
 fail-open unchanged'. A base->head create-row difference is PERMITTED only when the principal's claimed level is an
 unrecognised STRING and the type's creator level ranks none ('none' any case, '' or absent) and the base answer was
 403 INSUFFICIENT_VERIFICATION_LEVEL. Everything else that differs is a VIOLATION (Blocker class). Verify rows: ANY diff is a violation.
 Planted controls are injected into a copy and must be flagged (and a legit diff must not)."""
import json, sys, collections, copy
E = sys.argv[0].rsplit('/', 1)[0]
A, B = sys.argv[1], sys.argv[2]; LAB = sys.argv[3] if len(sys.argv) > 3 else A + '_vs_' + B
KNOWN = ['none', 'basic', 'social', 'standard', 'enhanced', 'high', 'government']  # ruling / spec vocabulary, independent copy
da = json.load(open(f'{E}/rows_{A}.json')); db = json.load(open(f'{E}/rows_{B}.json'))
cat = {t['code']: t for t in db['meta']['catalogue']}
def claim_class(c):
    if c in ('<anon>', '<invalid>'): return 'no-principal'
    if c in ('<number>', '<array>'): return 'nonstring'
    if c == '<absent>': return 'known'
    return 'known' if (c or 'none').lower() in KNOWN else 'unknown'
def type_class(code):
    if code is None: return 'untyped'
    t = cat.get(code) or cat.get(code.upper())
    if not t: return 'unregistered'
    lv = t['creator']; lv = '' if lv == '<absent>' else lv
    n = (lv or 'none').lower()
    if n == 'none': return 'none-rank'
    return 'known-above' if n in KNOWN else 'unknown-required'
def key(r): return (r['principal'], r.get('key'), r['type'])
def outcome(r): return (r['status'], r['code'], r['forwarded'], r['workflow'], r.get('pending'))
def judge(ra, rb):
    cc, tc = claim_class(ra['claim']), type_class(ra['type'])
    if cc == 'unknown' and tc == 'none-rank' and ra['status'] == 403 and ra['code'] == 'INSUFFICIENT_VERIFICATION_LEVEL' and rb['code'] != 'INSUFFICIENT_VERIFICATION_LEVEL':
        return 'PERMITTED'
    return 'VIOLATION'
def run(rows_a, rows_b):
    ia = {key(r): r for r in rows_a}; ib = {key(r): r for r in rows_b}
    assert set(ia) == set(ib), ('row sets differ', len(set(ia) ^ set(ib)))
    diffs = []
    for k in ia:
        if outcome(ia[k]) != outcome(ib[k]):
            diffs.append((k, outcome(ia[k]), outcome(ib[k]), judge(ia[k], ib[k]), claim_class(ia[k]['claim']), type_class(k[2])))
    return diffs
print('compare', LAB, 'rows', len(da['rows']), len(db['rows']), 'verify', len(da['verify']), len(db['verify']))
diffs = run(da['rows'], db['rows'])
viol = [d for d in diffs if d[3] == 'VIOLATION']; perm = [d for d in diffs if d[3] == 'PERMITTED']
print('CREATE diffs', len(diffs), 'PERMITTED', len(perm), 'VIOLATION', len(viol))
print('  by (claim_class,type_class,verdict):', dict(collections.Counter((d[4], d[5], d[3]) for d in diffs)))
print('  by transition:', dict(collections.Counter((d[1][:2], d[2][:2], d[2][2], d[2][3]) for d in diffs)))
print('  principals with diffs:', dict(collections.Counter(d[0][0] for d in diffs)))
print('  types with diffs:', dict(collections.Counter(d[0][2] for d in diffs)))
for d in viol: print('  VIOLATION', d)
# verify rows: any diff is a violation
iv = {(r['principal'], r['type']): r for r in da['verify']}; jv = {(r['principal'], r['type']): r for r in db['verify']}
vd = [(k, (iv[k]['status'], iv[k]['code'], iv[k]['requiredLevel']), (jv[k]['status'], jv[k]['code'], jv[k]['requiredLevel'])) for k in iv if (iv[k]['status'], iv[k]['code'], iv[k]['requiredLevel'], iv[k]['currentLevel']) != (jv[k]['status'], jv[k]['code'], jv[k]['requiredLevel'], jv[k]['currentLevel'])]
print('VERIFY diffs', len(vd)); [print('  VERIFY-DIFF', x) for x in vd[:20]]
# pure function
pa = {(json.dumps(r['u']), json.dumps(r['q'])): r['res'] for r in da['pure']}; pb = {(json.dumps(r['u']), json.dumps(r['q'])): r['res'] for r in db['pure']}
pflip = [(k, pa[k], pb[k]) for k in pa if pa[k] != pb[k]]
def pclass(v):
    if v is None or v == '<undefined>' or v == '' or v is False or v == 0: return 'known'
    if not isinstance(v, str): return 'nonstring'
    return 'known' if v.lower() in KNOWN else 'unknown'
def qnone(v):
    if v is None or v == '<undefined>' or v == '': return True
    return isinstance(v, str) and v.lower() == 'none'
bad_p = [f for f in pflip if not (pclass(json.loads(f[0][0])) == 'unknown' and qnone(json.loads(f[0][1])) and f[1] is False and f[2] is True)]
print('PURE rows', len(pa), 'flips', len(pflip), 'flips outside (unknown user x none-rank required, false->true):', len(bad_p))
print('  flip users:', sorted(set(json.loads(f[0][0]) for f in pflip), key=str)); print('  flip required:', sorted(set(str(json.loads(f[0][1])) for f in pflip)))
for f in bad_p[:10]: print('  PURE-VIOLATION', f)
# independent oracle on B's pure rows (the tree named 'head'-like when B is head/merged; base-like otherwise)
def oracle(u, q, mode):
    if not (u is None or u == '<undefined>' or isinstance(u, str) or u is False or u == 0): return 'nonstring'
    un = 'none' if (u in (None, '<undefined>', '', False, 0)) else u.lower()
    qn = 'none' if (q in (None, '<undefined>', '')) else q.lower()
    if qn not in KNOWN: return True
    if un in KNOWN: return KNOWN.index(un) >= KNOWN.index(qn)
    return (0 >= KNOWN.index(qn)) if mode == 'head' else False
for tree, dd in ((A, da), (B, db)):
    mode = 'base' if tree.startswith('base') or tree.endswith('TA') else 'head'
    mism = [(r['u'], r['q'], r['res']) for r in dd['pure'] if oracle(r['u'], r['q'], mode) != 'nonstring' and oracle(r['u'], r['q'], mode) != r['res']]
    ns = collections.Counter(str(r['res']) for r in dd['pure'] if oracle(r['u'], r['q'], mode) == 'nonstring')
    print(f'ORACLE({mode}) on {tree}: mismatches {len(mism)}; non-string user results {dict(ns)}'); [print('   MISMATCH', m) for m in mism[:8]]
# planted controls
if A.startswith('base') and B in ('head', 'merged'):
    pb2 = copy.deepcopy(db['rows']); ib2 = {key(r): r for r in pb2}
    k1 = ('jwt_BASIC', 'documentType', 'SSD_DOCUMENT'); ib2[k1].update(status=403, code='INSUFFICIENT_VERIFICATION_LEVEL', forwarded=False)
    k2 = ('sk_write', 'documentType', 'QA_BASIC'); ib2[k2].update(status=201, code=None, forwarded=True)
    k3 = ('sk_write', 'documentType', 'REFERENCE'); ib2[k3].update(status=201, code=None, forwarded=True)
    d2 = run(da['rows'], pb2); flagged = {d[0] for d in d2 if d[3] == 'VIOLATION'}
    print('PLANTED CONTROLS: known-level change flagged', k1 in flagged, '| unknown user passing basic flagged', k2 in flagged, '| unknown user passing standard flagged', k3 in flagged,
          '| legit (sk_write, DOCUMENT) not flagged', ('sk_write', 'documentType', 'DOCUMENT') not in flagged and any(d[0] == ('sk_write', 'documentType', 'DOCUMENT') for d in d2))
    # coverage: unknown-string principals that clear the scope gates on none-rank types
    cov = [(r['principal'], r['type']) for r in da['rows'] if claim_class(r['claim']) == 'unknown' and type_class(r['type']) == 'none-rank' and r['key'] == 'documentType']
    print('coverage: unknown-claim x none-rank create rows (documentType key):', len(cov))
# parity: connector (sk_write) vs lowest human (jwt_NONE), and jwt_connector_noscope vs sk_noscope
for tree, dd in ((A, da), (B, db)):
    for p1, p2 in (('sk_write', 'jwt_NONE'), ('jwt_connector_noscope', 'jwt_NONE'), ('sk_bypass_workflow', 'jwt_NONE'), ('jwt_connector_noscope', 'sk_noscope')):
        r1 = {(r['key'], r['type']): r for r in dd['rows'] if r['principal'] == p1}; r2 = {(r['key'], r['type']): r for r in dd['rows'] if r['principal'] == p2}
        dif = [(k, outcome(r1[k])[:3], outcome(r2[k])[:3]) for k in r1 if outcome(r1[k]) != outcome(r2[k])]
        v1 = {r['type']: r for r in dd['verify'] if r['principal'] == p1}; v2 = {r['type']: r for r in dd['verify'] if r['principal'] == p2}
        vdif = [(k, v1[k]['status'], v2[k]['status']) for k in v1 if (v1[k]['status'], v1[k]['code']) != (v2[k]['status'], v2[k]['code'])]
        print(f'PARITY {tree} {p1} vs {p2}: create rows {len(r1)} differing {len(dif)}; verify rows {len(v1)} differing {len(vdif)}')
        for x in dif[:12]: print('    ', x)
        for x in vdif[:6]: print('     v', x)
