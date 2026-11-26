# survivors per template: head vs variant (preview, any leak kind); label-boundary oracle vs prefix oracle
import sys, os, json
from collections import Counter, defaultdict
sys.argv = ['x', '/private/tmp/claude-501/qae/corp/c1', '/private/tmp/claude-501/qae/corp/c1.head.out', '/private/tmp/claude-501/qae/corp/c1.pv.out']
src = open('/private/tmp/claude-501/qae/h/qa_analyze.py').read().split('# ---- survivors ----')[0]
exec(src)
rows = defaultdict(Counter)
for raw, m, h, v in zip(raws, meta, old, new):
    if m['section'] not in ('b', 'c', 'd'): continue
    outside = strip(raw)
    for a in m['planted']: outside = outside.replace(a, '')
    for a in m['planted']:
        if '@' not in a: continue
        r = rows[(m['section'], m['template'])]; r['n'] += 1
        if leak_ctx(h['preview'], a, outside): r['head'] += 1
        if leak_ctx(v['preview'], a, outside): r['variant'] += 1
tot = Counter()
for k in sorted(rows):
    r = rows[k]; tot[k[0] + ' n'] += r['n']; tot[k[0] + ' head'] += r['head']; tot[k[0] + ' variant'] += r['variant']
    if r['head'] != r['variant']: print(f"  {k[0]} {k[1]:30} n={r['n']:4} head-surv={r['head']:4} variant-surv={r['variant']:4}")
print('totals', dict(tot))
# label-boundary-only vs longest-prefix, over every input
import importlib
def orc(t, var):
    globals()['VAR'] = var
    return sorted(oracle(t, xn_ci=True, ws='rust'))
diff = 0; ex = []
for raw, m, v in zip(raws, meta, new):
    a, b = orc(v['clean'], 'prefix'), orc(v['clean'], 'label')
    if a != b:
        diff += 1
        if len(ex) < 4: ex.append((m['section'], m['template'], raw[:70], a, b))
print('inputs where label-boundary-only answers differently from longest-prefix:', diff); [print('  ', e) for e in ex]
