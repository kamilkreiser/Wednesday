# Gate 188 r2: tabulate runs_r2/pg_{base,r1,r2}.jsonl and count direction (X presents a certification where Y presented none).
# usage: python3 -I table.py <runs_r2 dir> [swap]
import json, sys, os
D = sys.argv[1]; swap = len(sys.argv) > 2
recs = {}
for v in ('base', 'r1', 'r2'):
    for line in open(os.path.join(D, f'pg_{v}.jsonl')):
        r = json.loads(line); recs[(v, r['cell'], r['path'], r['n'])] = r
keys = sorted({k[1:] for k in recs}, key=lambda k: (k[0], str(k[2]), k[1]))
def show(r):
    if r is None: return '-'
    if isinstance(r['winner'], list):
        w = r['winner']; ws = ','.join(x.replace('g-', '') for x in w) if len(w) <= 3 else f"{len(w)} rows [{w[0].replace('g-','')}..]"
        c = [x for x in r['certIds'] if x]
        return f"cnt={r['count']} {ws} certs={len(c)}{('('+c[0]+')') if c else ''} oR={r['originalsReads']}{' WARN' if r['warnKS1561'] else ''}"
    return f"{(r['winner'] or 'null').replace('g-','')} cert={r['isCertified']} {r['certId'] or ''} oR={r['originalsReads']}{' WARN' if r['warnKS1561'] else ''}"
print(f"{'cell':18} {'path':13} {'n':>3} | base | r1 | r2")
for k in keys:
    print(f"{k[0]:18} {k[1]:13} {str(k[2]):>3} | {show(recs.get(('base',)+k))} | {show(recs.get(('r1',)+k))} | {show(recs.get(('r2',)+k))}")
def more(x, y):
    out = []
    for k in keys:
        a, b = recs.get((x,)+k), recs.get((y,)+k)
        if a and b and a['presentsCert'] and not b['presentsCert']: out.append(k)
    return out
pairs = [('r2', 'base'), ('r2', 'r1')] if not swap else [('base', 'r2'), ('r1', 'r2')]
for x, y in pairs:
    m = more(x, y)
    print(f"\n{x} presents a certification where {y} presented none: {len(m)} of {len(keys)} cells")
    for k in m: print('   ', k)
# also: certification presented on both but a DIFFERENT certification id
diff = []
for k in keys:
    a, b = recs.get(('r2',)+k), recs.get(('base',)+k)
    ca = a.get('certId') if 'certId' in a else tuple(x for x in a['certIds'] if x)
    cb = b.get('certId') if 'certId' in b else tuple(x for x in b['certIds'] if x)
    if a['presentsCert'] and b['presentsCert'] and ca != cb: diff.append((k, cb, ca))
print(f"\nr2 vs base: both present a certification but a different one: {len(diff)}")
for d in diff: print('   ', d)
