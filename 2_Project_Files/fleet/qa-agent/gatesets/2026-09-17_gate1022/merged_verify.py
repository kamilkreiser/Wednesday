import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1022'); chk('#1022 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash ee40d3099',sq.startswith('ee40d3099'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash (ahead/identical, behind 0)',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 79933c798',len(ps)==1 and ps[0].startswith('79933c798'),ps)
chk('tree cfb7dd1b3',c['commit']['tree']['sha'].startswith('cfb7dd1b3'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('4 files',len(fs)==4,sorted(fs))
for suf,b in (('Blockchain/Dev/package-lock.json','99db3e7c2'),('scripts/audit/audit-baseline.json','45ef8220f'),('services/mcp-server/package-lock.json','f942d659b'),('services/originate/package-lock.json','d91d746ef')):
    chk('blob '+b,any(k.endswith(suf) and v.startswith(b) for k,v in fs.items()),suf)
m=c['commit']['message'].lower(); chk('no closing phrase',not any(w in m for w in ('closes','fixes','resolves')),'')
d=lin('{ a: issue(id:"KS-1211"){ state{name} comments(first:50){nodes{id}} } b: issue(id:"KS-1214"){ title state{name} } }')['data']
chk('KS-1211 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1211 comment 0baa2c0e',any(n['id'].startswith('0baa2c0e') for n in d['a']['comments']['nodes']),'')
chk('KS-1214 exists',d['b'] is not None,d['b'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
