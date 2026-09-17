import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1021'); chk('#1021 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 81ee4b729',sq.startswith('81ee4b729'),sq)
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 581c9db0d',len(ps)==1 and ps[0].startswith('581c9db0d'),ps)
chk('tree 207ba797c',c['commit']['tree']['sha'].startswith('207ba797c'),c['commit']['tree']['sha'])
chk('3 files',sorted(f['filename'] for f in c['files'])==['Blockchain/Dev/scripts/audit/audit-baseline.json','systemTest/akto/package-lock.json','systemTest/api-explorer/package-lock.json'],[f['filename'] for f in c['files']])
for pth,b in (('Blockchain/Dev/scripts/audit/audit-baseline.json','c73fcebed'),('systemTest/akto/package-lock.json','c4d30077f'),('systemTest/api-explorer/package-lock.json','78589de7e')):
    chk('blob '+b,gh('/contents/'+pth+'?ref='+sq)['sha'].startswith(b),pth)
chk('no closing phrase','close' not in c['commit']['message'].lower() and 'fixes' not in c['commit']['message'].lower(),c['commit']['message'][-60:].replace('\n',' | '))
d=lin('{ a: issue(id:"KS-1211"){ state{name} comments(first:50){nodes{id}} } }')['data']
chk('KS-1211 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1211 comment 73bd43f2',any(n['id'].startswith('73bd43f2') for n in d['a']['comments']['nodes']),'')
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
