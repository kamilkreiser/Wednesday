#!/usr/bin/env python3
import json, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948/logs'
def load(v, f):
    try: return {(r['site'], r['state'], r['kind']): r for r in map(json.loads, open(f'{W}/probe_{v}_{f}.jsonl'))}
    except FileNotFoundError: return {}
def ans(r):
    if r is None: return 'MISSING'
    if r['status'] == 0: return 'NO RESPONSE'
    a = r['answer']
    if isinstance(a, dict) and 'valid' in a: return f"{r['status']} valid:{str(a['valid']).lower()}" + (f" {a.get('reason')}" if a.get('reason') else '')
    if isinstance(a, dict) and 'code' in a: return f"{r['status']} {a['code']}"
    if isinstance(a, dict) and 'success' in a: return f"{r['status']} success:{a['success']}"
    return f"{r['status']} {a}"
def shape(r):  # everything a caller sees, minus volatile values
    return None if r is None else (r['status'], json.dumps(r['answer'], sort_keys=True), r['bodyKeys'], r['hdr'], r['bodyLen'] if r['site'] != 'audit' and r['site'] != 'event' else 'x')
def state(r): return None if r is None else (r['usageWrites'], r['auditEventWrites'], json.dumps(r['keyMem']))
bad = []
for f in ['test', 'production']:
    B, H = load('base', f), load('head', f)
    print(f'\n## NODE_ENV={f}  (cells: base {len(B)}, head {len(H)})')
    print('| site | key | kind | base answer | head answer | head == ordinary (answer, body shape, headers, state) | base unhandled/uncaught | head unhandled/uncaught | head logged | base logged | canary b/h |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for k in sorted(H, key=lambda k: (k[0], k[1], k[2] != 'none', k[2] != 'ordinary', k[2])):
        h, b = H.get(k), B.get(k); o = H.get((k[0], k[1], 'ordinary'))
        same = (shape(h) == shape(o) and state(h) == state(o)) if k[2] not in ('none', 'ordinary') else '-'
        if same is False and k[2] != 'plainString': bad.append((f, k))
        if h and h['answer'] and isinstance(h['answer'], dict) and h['answer'].get('valid') is True and k[1] != 'active': bad.append((f, k, 'VALID ON NON-ACTIVE'))
        lg = lambda r: '; '.join(x.split(': ', 1)[-1][-60:] for x in r['logged']) if r else ''
        print(f"| {k[0]} | {k[1]} | {k[2]} | {ans(b)} | {ans(h)} | {same} | {b and str(b['unhandled'])+'/'+str(b['uncaught'])} | {h['unhandled']}/{h['uncaught']} | {lg(h)} | {lg(b)} | {b and b['canary']}/{h['canary']} |")
print('\nhead cells that differ from the ordinary-Error cell (plainString excluded) or answer valid on a non-active key:', bad)
