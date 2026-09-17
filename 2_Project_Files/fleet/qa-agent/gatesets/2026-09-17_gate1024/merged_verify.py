import json,os,urllib.request
tok=os.environ['GH_TOKEN']; lk=os.environ['LINEAR_API_KEY']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':q}).encode(),headers={'Authorization':lk,'Content-Type':'application/json'}); return json.load(urllib.request.urlopen(r))
ok=[]
def chk(n,c,v): ok.append(c); print('PASS' if c else 'FAIL',n,str(v)[:150])
pr=gh('/pulls/1024'); chk('#1024 merged',pr['merged'],pr['merge_commit_sha']); sq=pr['merge_commit_sha']
chk('squash 79933c798',sq.startswith('79933c798'),sq)
br=gh('/branches/develop'); chk('develop == squash (or descends)',br['commit']['sha']==sq,br['commit']['sha'])
c=gh('/commits/'+sq); ps=[p['sha'] for p in c['parents']]
chk('one parent 81ee4b729',len(ps)==1 and ps[0].startswith('81ee4b729'),ps)
chk('tree ccd3f2819',c['commit']['tree']['sha'].startswith('ccd3f2819'),c['commit']['tree']['sha'])
fs=sorted(f['filename'] for f in c['files']); chk('2 files, originate only',len(fs)==2 and all('services/originate/' in f for f in fs),fs)
blobs={f['filename']:f['sha'] for f in c['files']}
chk('blob de9b5ae25 documents.ts',any(k.endswith('routes/documents.ts') and v.startswith('de9b5ae25') for k,v in blobs.items()),blobs)
chk('blob ada07f053 ks1202 test',any('ks1202' in k and v.startswith('ada07f053') for k,v in blobs.items()),'')
m=c['commit']['message'].lower(); chk('no closing phrase',not any(w in m for w in ('closes','fixes','resolves')),c['commit']['message'][-60:].replace('\n',' | '))
d=lin('{ a: issue(id:"KS-1202"){ state{name} comments(first:50){nodes{id}} } b: issue(id:"KS-1213"){ title state{name} assignee{name} priority } c: issue(id:"KS-1203"){ comments(first:50){nodes{id}} } }')['data']
chk('KS-1202 In Progress',d['a']['state']['name']=='In Progress',d['a']['state'])
chk('KS-1202 comment be343842',any(n['id'].startswith('be343842') for n in d['a']['comments']['nodes']),'')
chk('KS-1213 exists',d['b'] is not None,d['b'])
chk('KS-1203 comment 81a9546a',any(n['id'].startswith('81a9546a') for n in d['c']['comments']['nodes']),'')
ctl=lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found',ctl.get('data') is None or ctl['data'].get('issue') is None,'')
print('ALL','PASS' if all(ok) else 'FAIL',sum(ok),'/',len(ok))
