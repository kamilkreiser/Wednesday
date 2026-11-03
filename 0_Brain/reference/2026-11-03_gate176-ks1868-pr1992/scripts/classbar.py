# classbar.py: per site, reference = BASE outcome for V01 (ordinary Error). Excluded from the comparison: the sentinel
# count, and fields that carry value-specific text (constant flag, errorHasSentinel, onErrorKinds, polls text).
# Prints per-site tallies, every head cell != base-ordinary, and writes results/table.md (base vs head side by side).
import json, collections, re, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/results/'
qs = sys.argv[1:] or ['Q1', 'Q3', 'Q4']
def load(t): return sorted([json.loads(l) for l in open(W + f'q_{t}.jsonl')], key=lambda r: (r['q'], r['site'], r['value']))
b, h = load('base'), load('head')
assert len(b) == len(h)
IGN = ('tag', 'q', 'site', 'value', 'sentinelLines', 'constant', 'errorHasSentinel', 'onErrorKinds', 'errorType')
def key(r):
    d = {k: v for k, v in r.items() if k not in IGN}
    s = json.dumps(d, sort_keys=True)
    return re.sub(r'\(new: [^)]*\)', '(new)', s)
ref = {(r['q'], r['site']): key(r) for r in b if r['value'].startswith('V01')}
tot = eq = chg = 0; lines = []; by = collections.defaultdict(collections.Counter)
with open(W + 'table.md', 'w') as out:
    out.write('| q | site | value | base | head | same |\n|---|---|---|---|---|---|\n')
    for x, y in zip(b, h):
        assert (x['q'], x['site'], x['value']) == (y['q'], y['site'], y['value'])
        f = lambda r: '; '.join(f'{k}={v}' for k, v in r.items() if k not in ('tag', 'q', 'site', 'value'))
        out.write(f"| {x['q']} | {x['site']} | {x['value']} | {f(x)} | {f(y)} | {'=' if f(x) == f(y) else 'DIFF'} |\n")
        s = (x['q'], x['site'])
        if x['q'] not in qs or s not in ref or x['value'].startswith('V01'): continue
        tot += 1
        he, be, c = key(y) == ref[s], key(x) == ref[s], key(x) != key(y)
        eq += he; chg += c
        by[s][('head=ORD' if he else 'head!=ORD') + (' base=ORD' if be else ' base!=ORD') + (' CHANGED' if c else '')] += 1
        if not he: lines.append(f"  head!=base-ordinary: {s[1]} | {x['value']} | base={key(x)} | head={key(y)} | ref={ref[s]}")
for s, c in by.items(): print(s[0], s[1], dict(c))
print(f'TOTAL non-ordinary cells {tot}; head equals base-ordinary {eq}; base->head changed {chg}')
print('\n'.join(lines))
