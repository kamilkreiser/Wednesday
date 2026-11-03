#!/usr/bin/env python3
# analyse.py <base.jsonl> <head.jsonl>  -- class-bar table: head[value] vs base[ordinary], plus base[value]
import json, re, sys

def load(p):
    return [json.loads(l) for l in open(p)]

def msgs(lines):
    out = []
    for l in lines:
        m = re.search(r'"message":"([^"]*)"', l)
        if m:
            out.append(m.group(1))
            continue
        m = re.search(r'\] (\w+): (.*?)( \{.*)?$', l)
        out.append(f"{m.group(1)}:{m.group(2)}" if m else l[:80])
    return out

def err_field(lines):
    out = []
    for l in lines:
        m = re.search(r'"error":("(?:[^"\\]|\\.)*"|null|\d+)', l)
        out.append(m.group(1) if m else '-')
    return out

def reg_sig(r):
    if r['settled'] == 'resolved':
        res = 'resolved ' + json.dumps(r['value'])
    else:
        res = 'rejected ' + ('ORIGINAL' if r['sameAsThrown'] else 'OTHER(' + r['error'] + ')')
    return f"{res} | lines={msgs(r['lines'])} | ur={len(r['unhandled'])} ue={len(r['uncaught'])}"

def rec_sig(r):
    p = ';'.join(x['settled'] + ('' if x['settled'] == 'resolved' else '(' + x['error'] + ')') + ('' if x['settled'] != 'resolved' else json.dumps(x['value'], separators=(',', ':'))) for x in r['passes'])
    u = ','.join(f"{x['id']}={x['status']}" for x in r['updates'])
    return f"passes={p} | updates=[{u}] | lines={msgs(r['lines'])} | ur={len(r['unhandled'])} ue={len(r['uncaught'])}"

base, head = load(sys.argv[1]), load(sys.argv[2])
def key(r):
    if r['kind'] == 'registry':
        return ('registry', r['fn'], r['strict'], r['nodeEnv'], r['db'], r['thrown'])
    return ('reconciler', r['where'], r['thrown'])
B = {key(r): r for r in base}
H = {key(r): r for r in head}
assert len(B) == len(base) and len(H) == len(head) and set(B) == set(H)

diverge = 0
print('=== REGISTRY (sig excludes the logged error text; error text shown separately) ===')
for k in sorted(H, key=lambda k: str(k)):
    if k[0] != 'registry':
        continue
    _, fn, strict, env, db, val = k
    sig = reg_sig
    bord = B[('registry', fn, strict, env, 'throw', 'ordinary')]
    hv, bv = H[k], B[k]
    eq = sig(hv) == sig(bord) if db == 'throw' else sig(hv) == sig(bv)
    if not eq:
        diverge += 1
    print(f"{'OK ' if eq else 'DIFF'} {fn:22} strict={str(strict):5} env={env:10} db={db:9} val={str(val):20} HEAD: {sig(hv)} err={err_field(hv['lines'])}")
    if db == 'throw' and sig(bv) != sig(bord):
        print(f"      base[{val}] differs from base[ordinary]: {sig(bv)} err={err_field(bv['lines'])}")
    if not eq:
        print(f"      base[ordinary]: {sig(bord)}")
print('=== RECONCILER ===')
for k in sorted(H, key=lambda k: str(k)):
    if k[0] != 'reconciler':
        continue
    _, where, val = k
    bord = B[('reconciler', where, 'ordinary')] if where not in ('none', 'giveupNone') else B[k]
    hv, bv = H[k], B[k]
    eq = rec_sig(hv) == rec_sig(bord)
    if not eq:
        diverge += 1
    print(f"{'OK ' if eq else 'DIFF'} where={where:12} val={str(val):20} HEAD: {rec_sig(hv)} err={err_field(hv['lines'])}")
    if rec_sig(bv) != rec_sig(bord):
        print(f"      base[{val}]: {rec_sig(bv)} err={err_field(bv['lines'])}")
    if not eq:
        print(f"      base[ordinary]: {rec_sig(bord)}")
print('DIVERGENT head-vs-base-ordinary cells:', diverge)
