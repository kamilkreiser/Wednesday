import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
ok=[]
def chk(name,cond,val): ok.append(cond); print(('PASS' if cond else 'FAIL'),name,val)
dv=gh('/branches/develop')['commit']['sha']; chk('develop == f8c7aaa39',dv.startswith('f8c7aaa39'),dv)
c=gh('/commits/'+dv); ps=[p['sha'] for p in c['parents']]
chk('one parent d7e95cd9f',len(ps)==1 and ps[0].startswith('d7e95cd9f'),ps)
chk('tree 4d406fb1c',c['commit']['tree']['sha'].startswith('4d406fb1c'),c['commit']['tree']['sha'])
fs=[(f['filename'],f['additions'],f['deletions']) for f in c['files']]
chk('files = lock-discovery.mjs +5/-1',fs==[('Blockchain/Dev/scripts/audit/lock-discovery.mjs',5,1)],fs)
cont=gh('/contents/Blockchain/Dev/scripts/audit/lock-discovery.mjs?ref='+dv)
chk('blob 3dd903b52',cont['sha'].startswith('3dd903b52'),cont['sha'])
chk('no closing phrase in message','close' not in c['commit']['message'].lower() and 'Refs KS-769' in c['commit']['message'],c['commit']['message'][:80].replace('\n',' | '))
pr=gh('/pulls/1020'); chk('#1020 merged',pr['merged'],pr['merge_commit_sha'])
r=lin('{ i1: issue(id:"KS-769"){ state{name} comments(first:50){nodes{id body}} } i2: issue(id:"KS-1209"){ identifier title state{name} assignee{name} } }')
print('linear errors:',r.get('errors')) if r.get('errors') else None; d=r['data']; st=d['i1']['state']['name']; ids=[n['id'][:8] for n in d['i1']['comments']['nodes']]
chk('KS-769 In Progress',st=='In Progress',st)
chk('KS-769 comment d27a0581 present','d27a0581' in ids,ids)
chk('KS-1209 exists',d['i2'] is not None,d['i2'])
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, str(ctl.get('errors'))[:60])
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok),'/',len(ok))
