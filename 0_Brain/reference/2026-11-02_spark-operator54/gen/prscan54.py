# Operator 54: open PRs and their files; hits for security/src/index.ts, auth/src/routes/users.ts; planted control services/auth.
import re, json, sys, urllib.request
tok=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?GH_TOKEN=(.*)$',l.rstrip('\n'))
    if m: tok=m.group(1).strip().strip('"\'')
assert tok
def get(u):
    rq=urllib.request.Request(u,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json','User-Agent':'op54'})
    with urllib.request.urlopen(rq,timeout=30) as r: return json.loads(r.read())
R='https://api.github.com/repos/Secuura/Distributed_Secuura'
prs=[];p=1
while True:
    b=get(f'{R}/pulls?state=open&per_page=100&page={p}'); prs+=b
    if len(b)<100: break
    p+=1
out={};tot=0
for pr in prs:
    n=pr['number'];fs=[];q=1
    while True:
        b=get(f'{R}/pulls/{n}/files?per_page=100&page={q}'); fs+=[f['filename'] for f in b]
        if len(b)<100: break
        q+=1
    out[n]={'title':pr['title'],'base':pr['base']['ref'],'files':fs};tot+=len(fs)
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(prs),'PRs',tot,'files')
for n,v in out.items():
    for f in v['files']:
        if 'services/security/src/index.ts' in f: print('SEC-INDEX-HIT',n,f)
        if 'services/auth/src/routes/users.ts' in f: print('USERS-HIT',n,f)
        if 'services/auth/src/routes/auth.ts' in f: print('(not mine) auth.ts',n,f)
print('planted control services/auth entries:',sum(1 for v in out.values() for f in v['files'] if 'services/auth' in f))
print('planted control services/security entries:',sum(1 for v in out.values() for f in v['files'] if 'services/security' in f))
print('KS-1868-titled PRs:',[(n,v['title'][:70]) for n,v in out.items() if 'KS-1868' in v['title']])
