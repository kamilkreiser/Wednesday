import json, re
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951/logs'
U=re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
def load(v):
    d={}
    for l in open(f'{G}/probe_{v}.jsonl'):
        r=json.loads(l)
        if r.get('done'): continue
        d[(r['env'],r['site']+('/'+r['provider'] if r.get('provider') else ''),r['kind'])]=r
    return d
B,H=load('base'),load('head')
def resp(r):
    if 'result' in r:
        x=r['result']; return 'REJECT' if x.get('rejected') else f"{x['routeWouldAnswer']} {x['errorCode']} '{x['error'][:60]}'"
    b=json.loads(r['body'])
    if r['status']==201 and 'onChainVerified' in b.get('data',{}): d=b['data']; return f"201 v={d['onChainVerified']} s={d['onChainStatus']}"
    if r['status']==201 and 'nftCertificateId' in b.get('data',{}): d=b['data']; return f"201 minted tx={'y' if d.get('transactionHash') else 'n'} ipfsCid={d.get('ipfsCid')}"
    return f"{r['status']} {json.dumps(b.get('data', b.get('error')))[:90]}"
def rows(r): return ','.join(f"{x['status']}{'/minted_at' if x['minted_at'] else ''}{'/err='+x['error_message'][:50] if x['error_message'] else ''}" for x in r['rows']) or 'none'
def logs(r):
    return ','.join(f"{l['level'][0]}:{l['msg'][:18]}={l.get('errorField','-')[:40]}{'!THREW' if l.get('threw') else ''}" for l in r['logs'] if not l['msg'].startswith('Recorded client') and not l['msg'].startswith('No wallet'))
n=0; nd=0
for k in sorted(B, key=lambda k:(k[0],k[1],k[2])):
    b,h=B[k],H[k]
    rb,rh=resp(b),resp(h); wb,wh=rows(b),rows(h); lb,lh=logs(b),logs(h)
    same = (rb,wb)==(rh,wh); n+=1; nd+= (not same)
    print(f"{'SAME' if same else 'DIFF'} {k[0][:4]} {k[1]:24} {k[2]:20} | resp {rb} || {rh} | rows {wb} || {wh} | unc {b['uncaught']}/{h['uncaught']} ipfs {b['ipfsFetchCalls']}/{h['ipfsFetchCalls']}")
    print(f"      logs base: {lb}\n      logs head: {lh}")
print('cells',n,'outcome(resp+rows) differ',nd)
