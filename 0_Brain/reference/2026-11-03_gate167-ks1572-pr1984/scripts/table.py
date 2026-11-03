"""Gate 167: print base vs head per cell from logs/probe/{base,head}.json (reads only what g167.cjs wrote)."""
import json, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate167-ks1572-pr1984'
b = json.load(open(W + '/logs/probe/base.json')); h = json.load(open(W + '/logs/probe/head.json'))
print('base boot:', b.get('bootLine'), '| head boot:', h.get('bootLine'), '| errs:', b.get('driverError'), h.get('driverError'))
def s(r):
    ref = ';'.join(f"{x['u']}/{x['status']}/w={x['w']}/ok={x['ok']}/{x['flags']}" for x in r['referrals']) or '-'
    rew = ';'.join(f"{x['u']}:{x['amount']}" for x in r['rewards']) or '-'
    fl = ';'.join(f"{x['flag']}/ip={x['ip']}/dev={x['dev']}" for x in r['fraudLog']) or '-'
    return f"{r['status']} {r.get('code') or ''} bonus={r.get('bonus')} | ref={ref} | rew={rew} | uses={r['codeUses']} | flog={fl} | writes={r['writeRows']} stmts={r['appStatements']}"
for rb, rh in zip(b['rows'], h['rows']):
    assert rb['label'] == rh['label']
    print(f"[{rb['i']:2}] {rb['label']}\n     BASE {s(rb)}\n     HEAD {s(rh)}")
    if '--log' in sys.argv:
        for l in rh['svcLog']: print('       hlog', l)
