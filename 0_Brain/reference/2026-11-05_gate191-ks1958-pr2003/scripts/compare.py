import json, sys
# usage: python3 -I compare.py <left.jsonl> <right.jsonl>   (left = base, right = head or mutant)
L = [json.loads(l) for l in open(sys.argv[1])]
R = [json.loads(l) for l in open(sys.argv[2])]
key = lambda r: (r['cell'], r.get('route', ''), r['shape'])
lm = {key(r): r for r in L}; rm = {key(r): r for r in R}
assert len(lm) == len(L) and len(rm) == len(R) and set(lm) == set(rm), 'cell sets differ'
mat = [k for k in lm if k[0] in ('A', 'B', 'Bctrl', 'C', 'D', 'U', 'Uhealthy')]
gq = [k for k in mat if k[0] in ('A', 'B', 'Bctrl', 'C', 'D')]
more_perm = [k for k in gq if lm[k].get('verified') is False and rm[k].get('verified') is True]
stricter = [k for k in gq if lm[k].get('verified') is True and rm[k].get('verified') is False]
same = [k for k in gq if lm[k].get('verified') == rm[k].get('verified')]
print(f"Q2 matrix (A,B,Bctrl,C,D x 3 shapes x 2 routes): {len(gq)} cells; right more permissive than left: {len(more_perm)}; stricter: {len(stricter)}; same verified: {len(same)}")
for k in more_perm: print('  MORE PERMISSIVE', k)
for k in stricter: print('  stricter', k)
print(f"{'cell':9} {'route':13} {'shape':8} | L ver st ms sel | R ver st ms sel | R errors")
for k in sorted(mat):
    a, b = lm[k], rm[k]
    print(f"{k[0]:9} {k[1]:13} {k[2]:8} | {str(a.get('verified')):5} {a['status']} {a.get('ms', -1):3} {a.get('selects')} | {str(b.get('verified')):5} {b['status']} {b.get('ms', -1):3} {b.get('selects')} | {json.dumps(b.get('errors'))[:110]}")
print('non-200 verify statuses L:', [k for k in mat if lm[k]['status'] != 200], ' R:', [k for k in mat if rm[k]['status'] != 200])
print('body leak hits L:', [(k, lm[k]['bodyLeak']) for k in mat if lm[k]['bodyLeak']], ' R:', [(k, rm[k]['bodyLeak']) for k in mat if rm[k]['bodyLeak']])
print('header leak hits L:', [k for k in mat if lm[k]['headerLeak']], ' R:', [k for k in mat if rm[k]['headerLeak']])
print('warns carrying the planted token (positive control) L:', sum(1 for k in mat if lm[k]['warnHasToken']), ' R:', sum(1 for k in mat if rm[k]['warnHasToken']))
for k in sorted(lm):
    if k[0].startswith('Q4'):
        a = {x: y for x, y in lm[k].items() if x != 'side'}; b = {x: y for x, y in rm[k].items() if x != 'side'}
        print(('SAME ' if a == b else 'DIFF ') + str(k), json.dumps(a)[:240] if a == b else ('\n   L ' + json.dumps(a) + '\n   R ' + json.dumps(b)))
