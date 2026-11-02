import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/logs'
def load(v):
    return {(j['route'],j['scenario']):j for j in map(json.loads,open(f'{W}/probe_{v}.jsonl')) if 'route' in j}
B,H=load('base'),load('head')
print('# POST unreadable vs ordinary at head: body with error.message masked')
for s in ['afterInsert:configInsert','afterInsert:activeUpdate','beforeInsert:slugSelect']:
    o=json.loads(H[('POST',s+'/ordinary')]['body']); o['error']['message']='M'
    for k in ('revokedProxy','throwingGetter','throwingToString'):
        if ('POST',s+'/'+k) in H:
            u=json.loads(H[('POST',s+'/'+k)]['body']); msg=u['error']['message']; u['error']['message']='M'
            print(s,k,'equal-modulo-message:',u==o,'message:',msg)
print('\n# ZodError 400 bodies, base vs head bytes')
for k in [('POST','badBody'),('POST','afterInsert:configInsert/zod'),('POST','beforeInsert:slugSelect/zod'),('GET list','zod'),('PATCH :id','zod'),('PATCH :id','badBody')]:
    b,h=B[k],H[k]; print(k,b['status'],h['status'],'bytes',len(b['body'].encode()),len(h['body'].encode()),'sha',b['bodySha'],h['bodySha'],'IDENTICAL' if b['body']==h['body'] else 'DIFF')
print('  sample:',H[('PATCH :id','zod')]['body'])
print('\n# console.error lines, base | head (selected)')
for k in sorted(H):
    if any(x in k[1] for x in ('revokedProxy','throwingGetter','ordinary','stackGetter','throwingToString')):
        print(k, '\n   base:',B[k]['errLines'],'\n   head:',H[k]['errLines'])
