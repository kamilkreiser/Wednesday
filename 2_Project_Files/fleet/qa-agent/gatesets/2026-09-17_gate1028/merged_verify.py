import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1028'); chk('#1028 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 0a2b1603f',sq.startswith('0a2b1603f'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 75ad0e55c',len(ps)==1 and ps[0].startswith('75ad0e55c'),ps)
chk('tree 557aa4de8',c['commit']['tree']['sha'].startswith('557aa4de8'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('2 files',len(fs)==2,sorted(fs))
chk('auth.ts blob 6e1668362',any(k.endswith('api-gateway/src/middleware/auth.ts') and v.startswith('6e1668362') for k,v in fs.items()),fs)
chk('ks744 test blob 2ed41a338',any('ks744' in k and v.startswith('2ed41a338') for k,v in fs.items()),fs)
m=c['commit']['message']; chk('no closing phrase',not any(w in m.lower() for w in ('closes','fixes','resolves')),'')
q='{ a: issue(id:"KS-744"){ state{name} comments(first:80){nodes{id}} } b: issue(id:"KS-1208"){ comments(first:80){nodes{id}} } c: issue(id:"KS-1221"){ title state{name} } d: issue(id:"KS-1222"){ title state{name} } e: issue(id:"KS-1223"){ title state{name} } }'
d=lin(q)['data']
chk('KS-744 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-744 comment 71474b10',any(n['id'].startswith('71474b10') for n in d['a']['comments']['nodes']),'')
chk('KS-1208 comment 5eec75a6',any(n['id'].startswith('5eec75a6') for n in d['b']['comments']['nodes']),'')
for k,t in (('c','KS-1221'),('d','KS-1222'),('e','KS-1223')): chk(t+' exists',d[k] is not None,d[k])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
