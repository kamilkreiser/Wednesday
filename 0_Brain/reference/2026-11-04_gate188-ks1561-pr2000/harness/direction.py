"""Gate 188 base-vs-head direction. Predicate: a (cell, path) is MORE PERMISSIVE on head when head presents a certification
(v1: checks.isCertified; v2: any match certified) and base presented none. Prints the ratio and every changed cell.
Control: run with --plant to flip one head row to certified where base was not; the predicate must flag it."""
import json, sys

def load(p):
    out = {}
    for line in open(p):
        r = json.loads(line)
        if r['path'] in ('plant-visible', 'raw-miss'):
            continue
        presents = r.get('anyCert', r['certified']) if r['path'] == 'v2' else r['certified']
        out[(r['cell'], r['path'])] = (bool(presents), r.get('certId'), r.get('documentId'), r.get('count'))
    return out

base, head = load(sys.argv[1]), load(sys.argv[2])
if '--plant' in sys.argv:
    k = next(k for k in sorted(head) if not base.get(k, (True,))[0])
    head[k] = (True,) + head[k][1:]
    print('PLANTED wrong head on', k)
keys = sorted(set(base) & set(head))
worse = [k for k in keys if head[k][0] and not base[k][0]]
changed = [k for k in keys if head[k] != base[k]]
print(f'cells compared: {len(keys)} (base {len(base)}, head {len(head)})')
print(f'head MORE permissive than base: {len(worse)}/{len(keys)} {worse}')
print(f'head equal to base: {len(keys) - len(changed)}/{len(keys)}; changed: {len(changed)}')
for k in changed:
    print('  ', k, 'base', base[k], '-> head', head[k])
