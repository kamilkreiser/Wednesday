import json,sys
L='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1525_logs/'
tags=sys.argv[1:]
runs={t:json.load(open(L+'probe_'+t+'.json')) for t in tags}
def key(r): return (r.get('cell'), r.get('who'))
order=[key(r) for r in runs[tags[0]]['results']]
def fmt(r):
    if r is None: return '-'
    c=r.get('cell','')
    if 'status' in r and 'after' in r and 'saved' in r:
        a=r['after'] or {}
        return f"{r['status']} saved={r['saved']} row={'CHANGED' if r['rowChanged'] else 'same'}{' st='+str(a.get('status')) if a else ''}"
    if c=='ORACLE': return f"ext{r['unkExt']} uuid{r['unkUuid']} conn{r['unkConn']} notYours{r['notYours']} notYoursConn{r['notYoursConn']} identical={r['bodiesIdentical']}"
    if c.startswith('ITEM5 lineage'): return f"{r['status']} derived={len(r['derived'])} verifyCertBefore={bool(r['vBefore'].get('certification'))} after={ (r['vAfter'].get('certification') or {}).get('certifiedBy')} anon={(r['vAnon'].get('certification') or {}).get('certifiedBy')} bRowChanged={r['bRowBefore']!=r['bRowAfter']}"
    if c.startswith('ITEM5b'): return f"{r['status']} bRowChanged={r['bRowBefore']!=r['bRowAfter']}"
    if c.startswith('ITEM5c'): return f"{r['status']} certBefore={r['vBeforeCert']} certAfterBy={(r['vAfterCert'] or {}).get('certifiedBy')}"
    if c.startswith('ITEM4'): return f"{r['status']} landedOnBsDoc={r['updateLandedOnBsDocument']}"
    if c.startswith('ITEM1 constructed'): return f"{r['status']} bChanged={r['bDocBefore']!=r['bDocAfter']} aChanged={r['aDocBefore']!=r['aDocAfter']}"
    if c=='SETUP': return f"role={r['role']} su={r['su']} bp={r['bp']} tenantManager={r['tenantManager']}"
    return json.dumps({k:v for k,v in r.items() if k not in ('cell','who')})[:160]
print('| cell | who | '+' | '.join(tags)+' |'); print('|'+'---|'*(len(tags)+2))
for k in order:
    if k[0] in ('TARGETS',): continue
    vals=[]
    for t in tags:
        m=[r for r in runs[t]['results'] if key(r)==k]
        vals.append(fmt(m[0]) if m else '-')
    print(f"| {k[0]} | {k[1] or ''} | "+' | '.join(vals)+' |')
