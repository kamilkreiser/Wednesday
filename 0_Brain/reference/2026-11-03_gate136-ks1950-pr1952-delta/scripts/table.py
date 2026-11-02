import json, sys
# usage: table.py <jsonl>  -- one line per cell: status, hook, U-row deltas (before -> after) for changed columns, pwrites
def rows(s): return {p['id']: p for p in s['participants']}
for line in open(sys.argv[1]):
    r = json.loads(line)
    if 'rounds' in r:
        print(f"## {r['cell']} rounds={r['rounds']} rowsOk={r['rowsOk']} hist={r['hist']} errLogs={r['errLogs']} bad={r['bad']}"); continue
    if 'before' not in r: print('##', r); continue
    b, a = rows(r['before']), rows(r['after'])
    d = []
    for i in sorted(set(b) | set(a)):
        if i not in a: d.append(f"{i[:8]} DELETED"); continue
        if i not in b: x = a[i]; d.append(f"{i[:8]} NEW {x['wallet_address']} {x['stake']}/{x['tier']}/{x['vp']}/drep={x['is_drep']}/cc={x['cc']}/did={x['did']}/pc={x['pc']}/vc={x['vc']}"); continue
        ch = [f"{k}:{b[i][k]}->{a[i][k]}" for k in a[i] if a[i][k] != b[i][k]]
        if ch: d.append(f"{i[:8]} " + ' '.join(ch))
    pr = r['after']['proposals'] - r['before']['proposals']
    w = [x for x in r['pwrites']]
    lg = [f"{l['lv']}:{l['msg']}{sorted((l.get('meta') or {}).keys())}" for l in r['logs'] if l['lv'] != 'info']
    data = r.get('data') or {}
    dd = f" data(stake={data.get('stakedAmount')},drep={data.get('isDRep')},cc={data.get('isConstitutionalCommittee')},did={data.get('did')},wallet={data.get('walletAddress')})" if data and 'stakedAmount' in data and data.get('stakedAmount') is not None else ''
    print(f"{r['cell']} | {r['status']} {(r.get('message') or '')[:60]} | hook={r['hookFiredBefore']} | +proposals={pr} | {'; '.join(d) or 'no participant change'}{dd} | writes={[x[:60] for x in w]} | logs={lg} | unhandled={r['unhandled']}")
