import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1026'); chk('#1026 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 75ad0e55c',sq.startswith('75ad0e55c'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 20ab16f9a',len(ps)==1 and ps[0].startswith('20ab16f9a'),ps)
chk('tree bad1cbf5f',c['commit']['tree']['sha'].startswith('bad1cbf5f'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('2 files',len(fs)==2,sorted(fs))
chk('oauth.ts blob 8995edec6',any(k.endswith('services/auth/src/services/oauth.ts') and v.startswith('8995edec6') for k,v in fs.items()),fs)
chk('ks839 test blob 7853f210e',any('ks839' in k and v.startswith('7853f210e') for k,v in fs.items()),fs)
m=c['commit']['message']; chk('no closing phrase',not any(w in m.lower() for w in ('closes','fixes','resolves')),'')
d=lin('{ a: issue(id:"KS-839"){ state{name} comments(first:80){nodes{id}} } b: issue(id:"KS-1219"){ title state{name} } c: issue(id:"KS-1220"){ title state{name} } }')['data']
chk('KS-839 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-839 comment ac3cf66c',any(n['id'].startswith('ac3cf66c') for n in d['a']['comments']['nodes']),'')
chk('KS-1219 exists (array scope 500)',d['b'] is not None and ('500' in d['b']['title'] or 'array' in d['b']['title'].lower()),d['b'])
chk('KS-1220 exists (F-4 test-only)',d['c'] is not None,d['c'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
