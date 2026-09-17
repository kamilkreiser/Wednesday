import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1027'); chk('#1027 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 20ab16f9a',sq.startswith('20ab16f9a'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent e02515f8f',len(ps)==1 and ps[0].startswith('e02515f8f'),ps)
chk('tree f62662d93',c['commit']['tree']['sha'].startswith('f62662d93'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('10 files',len(fs)==10,len(fs))
targets={'scripts/audit/audit-baseline.json':'017f52bb5','Blockchain/Dev/package-lock.json':'4831bf207'}
for suf,b in [('audit-baseline.json','017f52bb5')]:
    chk('blob '+suf+' '+b,any(k.endswith(suf) and v.startswith(b) for k,v in fs.items()),[ (k,v[:9]) for k,v in fs.items() if k.endswith(suf)])
blobs=['4831bf207','3d9acadaf','b0c47af71','c71cfe57a','0a13fe2b7','5fae8f62c','040908e22','725d5d2c2','05dff4ebb']
got={v[:9] for v in fs.values()}
chk('9 lock blob targets present',all(b in got for b in blobs),sorted(set(blobs)-got))
chk('control e6f2184d2 absent','e6f2184d2' not in got,'')
chk('mobile lock not in diff',not any('mobile' in k for k in fs),'')
m=c['commit']['message']; chk('no closing phrase',not any(w in m.lower() for w in ('closes','fixes','resolves')),'')
d=lin('{ a: issue(id:"KS-1211"){ state{name} comments(first:80){nodes{id}} } b: issue(id:"KS-1216"){ title state{name} assignee{name} } }')['data']
chk('KS-1211 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1211 comment f0479af5',any(n['id'].startswith('f0479af5') for n in d['a']['comments']['nodes']),'')
chk('KS-1216 exists (js-yaml blind spot)',d['b'] and 'js-yaml' in d['b']['title'],d['b'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
