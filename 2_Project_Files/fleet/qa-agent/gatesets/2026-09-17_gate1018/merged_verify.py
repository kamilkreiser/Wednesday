import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1018'); chk('#1018 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash e02515f8f',sq.startswith('e02515f8f'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 19f1e5475',len(ps)==1 and ps[0].startswith('19f1e5475'),ps)
chk('tree ce49c7bfd',c['commit']['tree']['sha'].startswith('ce49c7bfd'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('2 files',len(fs)==2,sorted(fs))
chk('users.ts blob c723a68af',any(k.endswith('services/auth/src/routes/users.ts') and v.startswith('c723a68af') for k,v in fs.items()),fs)
chk('ks1050 test blob ffb3e801a',any('ks1050' in k and v.startswith('ffb3e801a') for k,v in fs.items()),fs)
m=c['commit']['message']; chk('no closing phrase',not any(w in m.lower() for w in ('closes','fixes','resolves')),'')
chk('Refs KS-1050 present','KS-1050' in m,'')
d=lin('{ a: issue(id:"KS-1050"){ state{name} comments(first:50){nodes{id}} } }')['data']
chk('KS-1050 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1050 comment d856751d',any(n['id'].startswith('d856751d') for n in d['a']['comments']['nodes']),'')
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
