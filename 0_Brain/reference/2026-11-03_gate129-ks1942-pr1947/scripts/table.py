import json, sys
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947/logs/'
def load(v): return {r['cell']: r for r in map(json.loads, open(G + f'probe_{v}.jsonl'))}
B, Hd = load('base'), load('head')
U1='11111111-1111-4111-8111-111111111111'; U2='22222222-2222-4222-8222-222222222222'
def row(r, pid):
    for p in r['after']['participants']:
        if p['id'] == pid: return p
def rowW(r, w):
    for p in r['after']['participants']:
        if p['wallet_address'] == w: return p
def nochange(r): return r['unchanged']
def written(r): return [s for s in r['sql'] if s.startswith('SAVE') or s.startswith('DELETE')]
# head expectations per approved design (Appendix B, D1a/D2a/D3a)
E = {
 'a0': lambda r: r['status']==201 and (p:=row(r,U1)) and p['stake']=='0' and p['tier']=='basic' and p['vp']=='0' and not p['is_drep'] and not p['cc'] and p['wallet_address']=='addr_test1_gate129_w1',
 'a1': lambda r: r['status']==403 and nochange(r) and not written(r),
 'a2': lambda r: r['status']==403 and nochange(r) and not written(r),
 'a3': lambda r: r['status']==403 and nochange(r) and not written(r),
 'a4': lambda r: r['status']==201 and (p:=row(r,U1)) and p['stake']=='0' and p['vp']=='0' and p['tier']=='basic' and p['pc']==0 and row(r,'forged') is None,
 'a5': lambda r: r['status']==201 and (p:=row(r,U1)) and p['did']=='did:gate129:u1' and p['stake']=='0',
 'a6': lambda r: r['status']==403 and nochange(r),
 'b1': lambda r: r['status']==403 and nochange(r) and not written(r) and 'byAddress' not in r['sql'],
 'b2': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b3': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b4': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b5': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b6': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b7': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b8': lambda r: r['status']==403 and nochange(r) and not written(r),
 'b9': lambda r: r['status']==201 and (p:=row(r,'44444444-4444-4444-8444-444444444444')) and p['stake']=='0',
 'c1': lambda r: r['status']==201 and (p:=row(r,U2)) and p['stake']=='50000' and p['is_drep'] and p['cc'] and p['did']=='did:gate129:u2' and p['vp']=='75000' and len(r['after']['participants'])==1,
 'c2': lambda r: r['status']==403 and nochange(r) and not written(r),
 'c3': lambda r: r['status']==403 and nochange(r) and not written(r),
 'c4': lambda r: r['status']==409 and nochange(r) and not written(r),
 'c5': lambda r: r['status']==201 and (p:=row(r,U1)) and p['wallet_address']=='addr_test1_gate129_w1' and p['stake']=='1000',
 'c6': lambda r: r['status']==403 and nochange(r) and not written(r),
 'd1': lambda r: r['status']==201 and (p:=row(r,U2)) and p['stake']=='200000' and not p['is_drep'],
 'd2': lambda r: r['status']==201 and (p:=rowW(r,'addr_test1_gate129_unregistered')) and p['stake']=='5000' and p['cc'],
 'd3': lambda r: r['status']==201 and (p:=row(r,U2)) and p['is_drep'] and p['cc'] and p['did']=='did:gate129:u2',
 'd4': lambda r: r['status']==201 and (p:=rowW(r,'addr_test1_gate129_w1')) and p['stake']=='3000',
 'e': lambda r: r['status']==503 and nochange(r) and not written(r),
 'f1': lambda r: r['status']==400 and (p:=row(r,U1)) and p['stake']=='0' and p['wallet_address']=='addr_test1_gate129_w1' and r['after']['proposals']==0,
 'f2': lambda r: r['status']==201 and r['after']['proposals']==1 and row(r,U2)['stake']=='50000' and row(r,U2)['pc']==3,
 'f3': lambda r: r['status']==403 and nochange(r) and not written(r),
 'f4': lambda r: r['status']==409 and nochange(r) and not written(r),
 'f5': lambda r: r['status']==503 and nochange(r) and not written(r),
 'f6': lambda r: r['status']==503 and nochange(r) and not written(r),
 'f7': lambda r: r['status']==503 and nochange(r) and not written(r),
 'f8': None,
}
def short(r):
    s = f"{r['status']}"
    if r.get('message'): s += f" \"{r['message'][:48]}\""
    ch = 'unchanged' if r['unchanged'] else 'CHANGED'
    w = ','.join(x for x in r['sql'] if x.startswith('SAVE') or x.startswith('DELETE')) or 'no write'
    return f"{s}; {ch}; {w}"
def desc(r, cell):
    k = cell.split()[0]
    pid = U2 if k in ('c1','c2','c3','d1','d3','f2','f5','f8','e1','e2') else U1
    p = row(r, pid)
    return f"{pid[:4]}: " + (f"w={p['wallet_address'][-6:]} stake={p['stake']} tier={p['tier']} vp={p['vp']} drep={p['is_drep']} cc={p['cc']} pc={p['pc']}" if p else 'no row')
ok = fail = 0
print('| cell | base | head | head row | head vs design |'); print('|---|---|---|---|---|')
for cell in Hd:
    if cell == 'initDb':
        print(f"| initDb | {B[cell]} | {Hd[cell]} | | |"); continue
    k = cell.split()[0]; e = E.get(k) if k in E else E.get(k[0]) if k[0]=='e' else None
    h = Hd[cell]; v = 'n/a (finding probe)' if e is None else ('PASS' if e(h) else 'FAIL')
    if e is not None: ok += v=='PASS'; fail += v=='FAIL'
    print(f"| {cell} | {short(B[cell])} | {short(h)} | {desc(h, cell)} | {v} |")
print(f"\nhead vs design: {ok} PASS, {fail} FAIL; unhandled base={sum(r.get('unhandled',0) for r in B.values())} head={sum(r.get('unhandled',0) for r in Hd.values())}")
