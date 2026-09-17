import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1019'); chk('#1019 merged',pr['merged'],pr['merge_commit_sha'])
sq=pr['merge_commit_sha']; chk('squash sha 581c9db0d',sq.startswith('581c9db0d'),sq)
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent f8c7aaa39',len(ps)==1 and ps[0].startswith('f8c7aaa39'),ps)
chk('tree 99df1503e',c['commit']['tree']['sha'].startswith('99df1503e'),c['commit']['tree']['sha'])
fs=sorted(f['filename'].split('/')[-1] for f in c['files']); chk('3 files',fs==['ks1187-erasure-door-judges-the-canonical-path.test.ts','ks843-erasure-scope-gate.test.ts','proxy.ts'],fs)
base='/contents/Blockchain/Dev/services/api-gateway/src/'
for pth,b in (('routes/proxy.ts','795ae7ca3'),('__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts','76c0137ee'),('__tests__/ks843-erasure-scope-gate.test.ts','06b499605')):
    chk('blob '+b,gh(base+pth+'?ref='+sq)['sha'].startswith(b),pth)
chk('no closing phrase','close' not in c['commit']['message'].lower() and 'fixes' not in c['commit']['message'].lower(),c['commit']['message'][-80:].replace('\n',' | '))
d=lin('{ a: issue(id:"KS-1187"){ state{name} comments(first:50){nodes{id}} } b: issue(id:"KS-843"){ state{name} } }')['data']
chk('KS-1187 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1187 comment ade784a9',any(n['id'].startswith('ade784a9') for n in d['a']['comments']['nodes']),'')
chk('KS-843 In Progress',d['b']['state']['name']=='In Progress',d['b']['state'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
