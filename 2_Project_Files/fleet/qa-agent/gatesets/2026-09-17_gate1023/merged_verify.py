import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1023'); chk('#1023 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash efaaa6034',sq.startswith('efaaa6034'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash (ahead/identical, behind 0)',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent ee40d3099',len(ps)==1 and ps[0].startswith('ee40d3099'),ps)
chk('tree 38ea11907',c['commit']['tree']['sha'].startswith('38ea11907'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('2 files',len(fs)==2,sorted(fs))
for suf,b in (('services/api-gateway/src/middleware/auth.ts','b8fce678a'),('ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts','f56bd48b9')):
    chk('blob '+b,any(k.endswith(suf) and v.startswith(b) for k,v in fs.items()),suf)
m=c['commit']['message'].lower(); chk('no closing phrase',not any(w in m for w in ('closes','fixes','resolves')),'')
d=lin('{ a: issue(id:"KS-1207"){ state{name} comments(first:50){nodes{id}} } b: issue(id:"KS-1215"){ title state{name} } }')['data']
chk('KS-1207 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1207 comment 39b00f27',any(n['id'].startswith('39b00f27') for n in d['a']['comments']['nodes']),'')
chk('KS-1215 exists',d['b'] is not None,d['b'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
