import json, sys
# gate 194 (adapted from gate 191's compare.py). usage: python3 -I compare.py <left.jsonl> <right.jsonl>  (left = base, right = head or mutant)
L = [json.loads(l) for l in open(sys.argv[1])]
R = [json.loads(l) for l in open(sys.argv[2])]
key = lambda r: (r['cell'], r.get('route', ''), r['shape'])
lm = {key(r): r for r in L}; rm = {key(r): r for r in R}
assert len(lm) == len(L) and len(rm) == len(R) and set(lm) == set(rm), 'cell sets differ'
mat = sorted(k for k in lm if 'verified' in lm[k] and k[0] not in ('UNK', 'LAT', 'RESTART'))
ok2xx = lambda s: s is not None and 200 <= s < 300
# (a) revoke outcome more permissive: head 2xx where base non-2xx, or head leaves verify TRUE where base FALSE
a = [k for k in mat if (ok2xx(rm[k]['revokeStatus']) and not ok2xx(lm[k]['revokeStatus']))]
# (b) verify more permissive
b = [k for k in mat if lm[k]['verified'] is False and rm[k]['verified'] is True]
stricter = [k for k in mat if lm[k]['verified'] is True and rm[k]['verified'] is False]
vdiff = [k for k in mat if (lm[k]['status'], lm[k]['verified'], lm[k]['errors']) != (rm[k]['status'], rm[k]['verified'], rm[k]['errors'])]
rdiff = [k for k in mat + [('UNK', '-', '-')] if lm[k]['revokeStatus'] != rm[k]['revokeStatus']]
print(f"cells with a verify read: {len(mat)}  (+ UNK revoke-only)")
print(f"(a) revoke more permissive (2xx where left non-2xx): {len(a)} of {len(mat) + 1}   {a}")
print(f"(a') verify TRUE at right where left FALSE (same as b): {len(b)} of {len(mat)}")
print(f"(b) verify more permissive: {len(b)} of {len(mat)}; stricter: {len(stricter)}; verify (status,verified,errors) differ: {len(vdiff)} of {len(mat)}; equal {len(mat) - len(vdiff)} of {len(mat)}")
for k in vdiff: print('   VERIFY DIFF', k, (lm[k]['status'], lm[k]['verified'], lm[k]['errors']), '->', (rm[k]['status'], rm[k]['verified'], rm[k]['errors']))
print(f"(c) revoke status differs: {len(rdiff)} of {len(mat) + 1}")
for k in rdiff: print('   REVOKE DIFF', k, lm[k]['revokeStatus'], '->', rm[k]['revokeStatus'], '|', rm[k].get('revokeMsg'))
print(f"{'cell':14} {'route':13} {'shape':8} | L rv upd db   mem  ver   | R rv upd db   mem  ver   | R revoke msg")
for k in mat + [('UNK', '-', '-')]:
    x, y = lm[k], rm[k]
    f = lambda r: f"{str(r['revokeStatus']):3} {str(r.get('updates')):3} {str(r.get('dbRowRevoked'))[:5]:5} {str(r.get('memRevoked'))[:5]:5} {str(r.get('verified')):5}"
    print(f"{k[0]:14} {k[1]:13} {k[2]:8} | {f(x)} | {f(y)} | {str(y.get('revokeMsg'))[:60]}")
for side, m in (('L', lm), ('R', rm)):
    allk = mat + [('UNK', '-', '-')]
    print(f"{side}: revoke 500s {[k for k in allk if m[k]['revokeStatus'] == 500]}; verify non-200 {[k for k in mat if m[k]['status'] != 200]}")
    print(f"{side}: body leak hits: revoke {[(k, m[k]['revokeBodyLeak']) for k in allk if m[k].get('revokeBodyLeak')]}, verify {[(k, m[k]['bodyLeak']) for k in mat if m[k].get('bodyLeak')]}")
    print(f"{side}: header leak hits: revoke {[(k, m[k]['revokeHeaderLeak']) for k in allk if m[k].get('revokeHeaderLeak')]}, verify {[(k, m[k]['headerLeak']) for k in mat if m[k].get('headerLeak')]}")
    print(f"{side}: warn-at-revoke carries the planted token (control): {sum(1 for k in mat if m[k].get('warnAtRevokeHasToken'))} cells: {[k for k in mat if m[k].get('warnAtRevokeHasToken')]}")
    print(f"{side}: 503 bodies: fixed wording {sum(1 for k in allk if m[k].get('revokeFixed503') is True)} of {sum(1 for k in allk if m[k]['revokeStatus'] == 503)}; schema {sorted(set(str(m[k].get('schema503')) for k in allk if m[k]['revokeStatus'] == 503))}; codes {sorted(set(str(m[k].get('revokeCode')) for k in allk if m[k]['revokeStatus'] == 503))}")
    print(f"{side}: x-g194 headers seen: {[(k, m[k]['revokeHeaders']) for k in allk if m[k].get('revokeHeaders')]}")
print('LAT L', {x: y for x, y in lm[('LAT', '-', '-')].items() if x not in ('side', 'cell', 'route', 'shape')})
print('LAT R', {x: y for x, y in rm[('LAT', '-', '-')].items() if x not in ('side', 'cell', 'route', 'shape')})
for side, m in (('L', lm), ('R', rm)):
    r = m[('RESTART', '-', 'ordinary')]
    print(f'RESTART {side}: fresh module instance {r["freshModuleInstance"]}; p2 memory before load (A) {r["p2MemBeforeLoad_A"]}')
    for c in 'ABZ':
        print(f'   {c}:', json.dumps(r[c]))
