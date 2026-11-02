import json, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935'
H = json.load(open(W + '/logs/probe_head.json')); B = json.load(open(W + '/logs/probe_base.json'))
print('unhandled head', H['unhandled'], 'base', B['unhandled'], 'cells', len(H['cells']), len(B['cells']))
def idx(d): return {(c['via'], c['kind'], c['point']): c for c in d['cells']}
h, b = idx(H), idx(B)
READ = ['error', 'string']; UNR = ['revokedProxy', 'getterThrowsError', 'getterThrowsRevoked', 'protoTrapThrows', 'toStringThrows']
def sig(c):  # statements exactly as issued: fn + full sql + values + whether it was the failing one
    return [(s['fn'], s['sql'], s['values'], s['failed']) for s in c['stmts']]
def writes(c):  # destructive/persisting statements that SUCCEEDED
    return [s['label'] + ' ' + s['values'] for s in c['stmts'] if not s['failed'] and s['label'] != 'SELECT policies']
def outcome(c):
    return (c.get('settled'), c.get('ret')) if c['via'] == 'function' else (c['status'], c['body'])
points = sorted({k[2] for k in h})
checks = fails = 0
def chk(name, ok):
    global checks, fails
    checks += 1
    if not ok: fails += 1; print('FAIL', name)
# A: readable values unchanged base->head (statements, outcome)
for via in ['function', 'route']:
    for k in READ:
        for p in points:
            key = (via, k, p)
            if key not in h: continue
            chk(f'A {key} stmts', sig(h[key]) == sig(b[key]))
            chk(f'A {key} outcome', outcome(h[key]) == outcome(b[key]))
# B: head unreadable == ordinary Error (base AND head): statements, rows written, outcome
for via in ['function', 'route']:
    for k in UNR:
        for p in points:
            key = (via, k, p)
            if key not in h: continue
            ref = b[(via, 'error', p)]
            chk(f'B {key} stmts==baseError', sig(h[key]) == sig(ref))
            chk(f'B {key} writes==baseError', writes(h[key]) == writes(ref))
            chk(f'B {key} outcome==baseError', outcome(h[key]) == outcome(ref))
            # headline: never more writes than base had for the same value
            chk(f'B {key} writes(head) superset-only-of-Error', set(writes(h[key])) <= set(writes(ref)))
print('checks', checks, 'fails', fails)
# Table: base vs head for each value class at each point (function), + route status
rows = []
for k in ['error', 'string'] + UNR:
    for p in points:
        if ('function', k, p) not in h: continue
        fb, fh = b[('function', k, p)], h[('function', k, p)]
        rb, rh = b[('route', k, p)], h[('route', k, p)]
        rows.append(f"{k:20s} | {p:26s} | base: {fb['settled'][:3]} writes={len(writes(fb))} route={rb['status']} | head: {fh['settled'][:3]} writes={len(writes(fh))} route={rh['status']} | errlog base={fb['errs']} head={fh['errs']}")
open(W + '/logs/probe_table.log', 'w').write('\n'.join(rows) + '\n')
# extra: did base vs head change the SET of writes, per value
for k in UNR:
    for p in points:
        if ('function', k, p) not in h: continue
        fb, fh = b[('function', k, p)], h[('function', k, p)]
        extra = [w for w in writes(fh) if w not in writes(fb)]
        if extra: print('HEAD-ONLY writes', k, p, '->', [e.split(' ')[0] + ' ' + e.split(' ')[1] for e in extra])
