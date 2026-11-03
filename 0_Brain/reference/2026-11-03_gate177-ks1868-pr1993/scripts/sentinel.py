# sentinel.py: Q5. Per q, total log lines and answers carrying SNTL177 at base and head, and every cell where head
# prints or answers MORE than base. The V01 ordinary-Error rows are the positive control (they carry it by design).
import json, collections
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/results/'
def load(t): return sorted([json.loads(l) for l in open(W + f'q_{t}.jsonl')], key=lambda r: (r['q'], r['site'], r['value']))
b, h = load('base'), load('head')
tot = collections.defaultdict(lambda: [0, 0, 0, 0, 0]); more = []; ctrl = collections.Counter()
for x, y in zip(b, h):
    if 'answerSentinel' not in x: continue
    t = tot[x['q']]; t[0] += 1
    t[1] += x['logSentinel']; t[2] += y['logSentinel']; t[3] += max(x['answerSentinel'], 0); t[4] += max(y['answerSentinel'], 0)
    if x['value'].startswith('V01'): ctrl[(x['q'], 'answer', x['answerSentinel'], y['answerSentinel'])] += 1
    if y['logSentinel'] > x['logSentinel'] or y['answerSentinel'] > x['answerSentinel']:
        more.append((x['q'], x['site'], x['value'], x['logSentinel'], y['logSentinel'], x['answerSentinel'], y['answerSentinel']))
    if y['answerSentinel'] < 0 or x['answerSentinel'] < 0: print('unserialisable answer', x['q'], x['site'], x['value'])
print('q | cells | log lines base | log lines head | answers base | answers head')
for q, t in sorted(tot.items()): print(q, '|', ' | '.join(map(str, t)))
print('cells where head prints or answers MORE than base:', len(more))
for m in more: print('  ', m)
print('positive control (V01 rows, answer base/head):', dict(ctrl))
less = [(x['q'], x['site'], x['value'], x['answerSentinel'], y['answerSentinel']) for x, y in zip(b, h) if 'answerSentinel' in x and (y['answerSentinel'] < x['answerSentinel'] or y['logSentinel'] < x['logSentinel'])]
print('cells where head prints or answers LESS:', len(less))
for m in less: print('  ', m)
# which non-ordinary classes answer the sentinel at head
ans = collections.Counter((y['q'], y['value'][:3]) for y in h if y.get('answerSentinel') == 1 and not y['value'].startswith('V01'))
print('head non-ordinary answers carrying it, by (q, class):', dict(sorted(ans.items())))
