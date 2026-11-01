# Operator 47: list OPEN PRs of Secuura/Distributed_Secuura and their files; print hits for services/auth/src/routes/auth.ts and a planted control (services/auth).
import os, re, json, sys, urllib.request
tok=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?GH_TOKEN=(.*)$',l.rstrip('\n'))
    if m: tok=m.group(1).strip().strip('"\'')
assert tok, 'GH_TOKEN not found'
def get(u):
    rq=urllib.request.Request(u,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json','User-Agent':'op51'})
    with urllib.request.urlopen(rq,timeout=30) as r: return json.loads(r.read())
R='https://api.github.com/repos/Secuura/Distributed_Secuura'
prs=[];p=1
while True:
    b=get(f'{R}/pulls?state=open&per_page=100&page={p}')
    prs+=b
    if len(b)<100: break
    p+=1
out={};tot=0
for pr in prs:
    n=pr['number'];fs=[];q=1
    while True:
        b=get(f'{R}/pulls/{n}/files?per_page=100&page={q}')
        fs+=[f['filename'] for f in b]
        if len(b)<100: break
        q+=1
    out[n]={'title':pr['title'],'base':pr['base']['ref'],'files':fs};tot+=len(fs)
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(prs),'PRs',tot,'files')
for n,v in out.items():
    for f in v['files']:
        if 'nft-certificate/src/services/minting.service.ts' in f: print('MINT-HIT',n,f)
ctl=[(n,f) for n,v in out.items() for f in v['files'] if 'services/nft-certificate' in f]
print('planted control services/nft-certificate entries:',len(ctl))
ks=[(n,v['title'][:70]) for n,v in out.items() if 'KS-1868' in v['title']]
print('KS-1868-titled PRs:',ks)
