import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908/logs'
def load(p,v):
    out={}
    for l in open(f'{W}/probe_{p}_{v}.jsonl'):
        r=json.loads(l)
        if 'cell' in r: out[r['cell']]=r
        else: print(p,v,'positive control',r)
    return out
for p in ('p2','p1'):
    b,h=load(p,'base'),load(p,'head')
    for c in b:
        for v,r in (('base',b[c]),('head',h[c])):
            rows=r.get('committedRows',r.get('dbPriorRow'))
            sql=[s for s in r['sql'] if s not in('SET TRANSACTION ISOLATION LEVEL READ COMMITTED','set_config(tenant GUC)','advisory_xact_lock')]
            print(f"{p} {c:24s} {v}: status={r['status']} priorKeysRevoked={r['priorKeysRevoked']} keyIssued={r['keyIssued']} err={r['errorMessage']!r}")
            print(f"    sql={sql}")
            print(f"    rows={rows} mem={r['memApiKeys']} ks577={r['log_ks577']} ks888={r['log_ks888']} created={r['log_created']} unhandled={r['unhandled']}" + (f" avail={r['availCalls']}" if 'availCalls' in r else ''))
