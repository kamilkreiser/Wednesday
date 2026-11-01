import json,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912'
def load(v): return [json.loads(l) for l in open(f'{G}/logs/probe_{v}.jsonl') if l.strip()]
def short(r):
    s=dict(st=r['status'],code=r.get('code'))
    if r['route'].startswith('DELETE'):
        s.update(mem=r['memIsActive'],stored=r['persistedIsActive'],v_same=(r['validateSameProcess']['valid'],r['validateSameProcess']['reason']),v_restart=(r['validateAfterRestart']['valid'],r['validateAfterRestart']['reason']),
                 ks888=[(x.get('fields'),x['values'].get('code'),x['values'].get('infra')) for x in r['ks888']],unh=r['unhandledAtRevoke'])
    elif r['route'].startswith('POST'):
        s.update(key=r['keyIssued'],sk=r['skInText'],mem=r['memKeys'],committed=r['committedKeys'],tail=r['sql'][-1:] ,ks888=[(x.get('fields'),x['values'].get('code'),x['values'].get('infra')) for x in r['ks888']],eh=[x['values'].get('error') for x in r['errorHandlerLines']],unh=r['unhandled'],msg=r.get('message'))
    else:
        s.update(scopes=r['committedScopes'],tail=r['sql'][-1:],infraLine=len(r['infraLines']),eh=[x['values'].get('error') for x in r['errorHandlerLines']],unh=r['unhandled'],msg=r.get('message'))
    return s
vs=sys.argv[1:] or ['base','head']
data={v:load(v) for v in vs}
for v in vs: print(v,'positive control',data[v][0])
rows=zip(*[d[1:] for d in data.values()])
for tup in rows:
    print('##',tup[0]['route'],'|',tup[0]['kind'])
    for v,r in zip(vs,tup): print('   ',v,json.dumps(short(r)))
