import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1025'); chk('#1025 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 19f1e5475',sq.startswith('19f1e5475'),sq)
cmp=gh('/compare/'+sq+'...develop'); chk('develop contains squash',cmp['behind_by']==0,(cmp['status'],cmp['ahead_by'],cmp['behind_by']))
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent efaaa6034',len(ps)==1 and ps[0].startswith('efaaa6034'),ps)
chk('tree 23b56bac0',c['commit']['tree']['sha'].startswith('23b56bac0'),c['commit']['tree']['sha'])
fs={f['filename']:f['sha'] for f in c['files']}; chk('1 file',len(fs)==1,sorted(fs))
chk('blob e6f2184d2',any(k.endswith('scripts/audit/audit-baseline.json') and v.startswith('e6f2184d2') for k,v in fs.items()),fs)
m=c['commit']['message']; chk('no closing phrase',not any(w in m.lower() for w in ('closes','fixes','resolves')),'')
chk('R6 reword present','were due to lapse 2026-09-30' in m,'')
d=lin('{ a: issue(id:"KS-528"){ state{name} comments(first:50){nodes{id}} } }')['data']
chk('KS-528 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-528 comment 77f02686',any(n['id'].startswith('77f02686') for n in d['a']['comments']['nodes']),'')
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
