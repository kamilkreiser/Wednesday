# classbar.py: per (q, site), the reference is BASE's outcome for V01 (ordinary Error). Value-specific TEXT is excluded
# (sentinel counts, the message text after a known "<prefix>: "), so a constant vs an ordinary message compare equal;
# the outcome, booleans, types and shapes are compared. Prints per-site tallies, every head cell != base-ordinary, the
# Q1 permissive bar, and writes results/table.md (base vs head side by side, all fields).
import json, collections, re
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/results/'
def load(t): return sorted([json.loads(l) for l in open(W + f'q_{t}.jsonl')], key=lambda r: (r['q'], r['site'], r['value']))
b, h = load('base'), load('head')
assert len(b) == len(h), (len(b), len(h))
def coll(s): return re.sub(r'(Signature verification error|Ed25519 verification error|Failed to resolve DID did:example:gate177-issuer): .*', r'\1: <msg>', s)
F = {
  'Q1': lambda r: (r['outcome'], r.get('verified'), r.get('signature'), r.get('issuerDID'), tuple(coll(e) for e in (r.get('errors') or []))),
  'Q3': lambda r: (r['outcome'], r.get('docNull'), r.get('error'), r.get('errorMessageType')),
  'Q3callers': lambda r: (r['outcome'], re.sub(r'"errorMessage":"[^"]*"', '"errorMessage":<msg>', r.get('shape') or ''), (r.get('rejectKind') or '').split(' (')[0]),
  'Q4a': lambda r: (r['outcome'], r.get('healthy'), r.get('errorType')),
  'Q4b': lambda r: (r['http'], r['status'], r['summary'], r['badPresent'], r.get('badStatus'), r['keys'], r.get('badErrorType')),
}
ref = {(r['q'], r['site']): F[r['q']](r) for r in b if r['value'].startswith('V01') and r['q'] in F}
tot = eq = chg = 0; lines = []; by = collections.defaultdict(collections.Counter); extra = collections.Counter()
with open(W + 'table.md', 'w') as out:
    out.write('| q | site | value | base | head | same |\n|---|---|---|---|---|---|\n')
    for x, y in zip(b, h):
        assert (x['q'], x['site'], x['value']) == (y['q'], y['site'], y['value'])
        f = lambda r: '; '.join(f'{k}={v}' for k, v in r.items() if k not in ('tag', 'q', 'site', 'value'))
        out.write(f"| {x['q']} | {x['site']} | {x['value']} | {f(x)} | {f(y)} | {'=' if f(x) == f(y) else 'DIFF'} |\n")
        s = (x['q'], x['site'])
        if s not in ref or x['value'].startswith('V01') or not x['value'].startswith('V'): continue
        isx = x['value'][:3] in ('V18', 'V19')
        tot += 1
        he, be, c = F[x['q']](y) == ref[s], F[x['q']](x) == ref[s], F[x['q']](x) != F[x['q']](y)
        eq += he; chg += c
        if isx: extra[('head=ORD' if he else 'head!=ORD') + (' CHANGED' if c else '')] += 1
        by[s][('head=ORD' if he else 'head!=ORD') + (' base=ORD' if be else ' base!=ORD') + (' CHANGED' if c else '')] += 1
        if not he: lines.append(f"  head!=base-ordinary: {s[0]} | {s[1]} | {x['value']} | base={F[x['q']](x)} | head={F[x['q']](y)} | ref={ref[s]}")
for s, c in sorted(by.items()): print(s[0], '|', s[1], dict(c))
print(f'TOTAL non-ordinary cells {tot} (incl. V18/V19 extra: {sum(extra.values())}); head equals base-ordinary {eq}; base->head changed {chg}; extra classes {dict(extra)}')
print('\n'.join(lines))
# Q1 permissive bar
q1 = [(x, y) for x, y in zip(b, h) if x['q'] == 'Q1']
perm = [(x['site'], x['value']) for x, y in q1 if (y.get('verified') is True or y.get('signature') is True) and x.get('verified') is not True]
print(f"Q1 cells {len(q1)} per tree; head verified:true or signature:true where base did not verify: {len(perm)} {perm}")
print(f"Q1 verified:true cells base {sum(x.get('verified') is True for x,_ in q1)} head {sum(y.get('verified') is True for _,y in q1)}; signature:true base {sum(x.get('signature') is True for x,_ in q1)} head {sum(y.get('signature') is True for _,y in q1)}")
print(f"Q1 REJECTED base {sum(x['outcome']=='REJECTED' for x,_ in q1)} head {sum(y['outcome']=='REJECTED' for _,y in q1)}")
q3 = [(x, y) for x, y in zip(b, h) if x['q'] == 'Q3']
print(f"Q3 cells {len(q3)}; non-null didDocument base {sum(bool(x.get('docNonNull')) for x,_ in q3)} head {sum(bool(y.get('docNonNull')) for _,y in q3)}; REJECTED base {sum(x['outcome']=='REJECTED' for x,_ in q3)} head {sum(y['outcome']=='REJECTED' for _,y in q3)}")
q4 = [(x, y) for x, y in zip(b, h) if x['q'] == 'Q4a']
print(f"Q4a cells {len(q4)}; healthy:true base {sum(x.get('healthy') is True for x,_ in q4)} head {sum(y.get('healthy') is True for _,y in q4)}; REJECTED base {sum(x['outcome']=='REJECTED' for x,_ in q4)} head {sum(y['outcome']=='REJECTED' for _,y in q4)}")
q4b = [(x, y) for x, y in zip(b, h) if x['q'] == 'Q4b']
print(f"Q4b cells {len(q4b)}; bad reported up/degraded base {sum(x.get('badStatus') in ('up','degraded') for x,_ in q4b)} head {sum(y.get('badStatus') in ('up','degraded') for _,y in q4b)}; overall status differs base->head {sum(x['status']!=y['status'] for x,y in q4b)}; http differs {sum(x['http']!=y['http'] for x,y in q4b)}; healthy count differs {sum(json.loads(x['summary'])['healthy']!=json.loads(y['summary'])['healthy'] for x,y in q4b)}; bad ABSENT base {sum(not x['badPresent'] for x,_ in q4b)} head {sum(not y['badPresent'] for _,y in q4b)}")
