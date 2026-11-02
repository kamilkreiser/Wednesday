import json
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951/logs'
def load(v):
    d={}
    for l in open(f'{G}/probe_{v}.jsonl'):
        r=json.loads(l)
        if r.get('done'): continue
        d[(r['env'],r['site']+('/'+r['provider'] if r.get('provider') else ''),r['kind'])]=r
    return d
B,H=load('base'),load('head')
def summ(r):
    if 'result' in r: s=f"fn:{json.dumps(r['result'])}"
    else:
        b=r['body']
        try: b=json.loads(b); b=json.dumps(b.get('data', b.get('error')))
        except Exception: pass
        s=f"{r['status']} {b[:150]}"
    rows=';'.join(f"{x['status']}|tx={'y' if x['transaction_hash'] else 'n'}|minted_at={x['minted_at']}|err={(x['error_message'] or '')[:70]}" for x in r['rows'])
    logs=';'.join(f"{l['level']}:{l['msg'][:40]}:{l.get('errorField','-')[:50]}{':THREW '+l.get('thrownMsg','')[:50] if l.get('threw') else ''}" for l in r['logs'] if l['msg'] not in ('Recorded client mint',) or True)
    return s, rows, logs, r['uncaught'], r['ipfsFetchCalls']
diff=0
for k in sorted(B):
    b=summ(B[k]); h=summ(H[k]); same = b==h
    if not same: diff+=1
    print(('SAME ' if same else 'DIFF ')+' | '.join(k))
    print('   base:',b[0]); 
    if not same: print('   head:',h[0])
    print('   rows base:',b[1]); 
    if not same: print('   rows head:',h[1])
    print('   logs base:',b[2], 'uncaught', b[3], 'ipfsCalls', b[4])
    if not same: print('   logs head:',h[2], 'uncaught', h[3], 'ipfsCalls', h[4])
print('cells',len(B),len(H),'differ',diff)
