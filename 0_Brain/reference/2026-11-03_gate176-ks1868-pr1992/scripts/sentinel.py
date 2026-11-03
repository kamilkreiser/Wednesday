# sentinel.py: per cell, log lines carrying SNTL176 (captured console/stdout/stderr/winston) and answers carrying it
# (Q1: the returned error string; Q4: the Error handed to onError). Base vs head; lists every cell where head > base.
import json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/results/'
def load(t): return sorted([json.loads(l) for l in open(W + f'q_{t}.jsonl')], key=lambda r: (r['q'], r['site'], r['value']))
b, h = load('base'), load('head')
ans = lambda r: int(bool(r.get('errorHasSentinel'))) + r.get('onErrorKinds', '').count('SENTINEL')
tot = {'base': [0, 0], 'head': [0, 0]}; more = []; less = []; perq = {}
for x, y in zip(b, h):
    for t, r in (('base', x), ('head', y)):
        tot[t][0] += r['sentinelLines']; tot[t][1] += ans(r)
        pq = perq.setdefault((r['q'], t), [0, 0]); pq[0] += r['sentinelLines']; pq[1] += ans(r)
    if y['sentinelLines'] > x['sentinelLines'] or ans(y) > ans(x): more.append((x['site'], x['value'], x['sentinelLines'], y['sentinelLines'], ans(x), ans(y)))
    if y['sentinelLines'] < x['sentinelLines'] or ans(y) < ans(x): less.append((x['site'], x['value'], x['sentinelLines'], y['sentinelLines'], ans(x), ans(y)))
print('cells', len(b))
for k, v in sorted(perq.items()): print(k, 'log lines', v[0], 'answers', v[1])
print('TOTAL base log', tot['base'][0], 'answers', tot['base'][1], '| head log', tot['head'][0], 'answers', tot['head'][1])
print('cells where head carries MORE:', len(more)); [print('  ', m) for m in more]
print('cells where head carries less:', len(less)); [print('  ', m) for m in less]
