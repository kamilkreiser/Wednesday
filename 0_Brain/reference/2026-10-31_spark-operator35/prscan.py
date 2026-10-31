import os,re,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    m=re.match(r'\s*(?:export\s+)?GH_TOKEN=(.*)',l)
    if m: env['t']=m.group(1).strip().strip('"\'')
tok=env['t']
def get(u):
    r=urllib.request.Request('https://api.github.com'+u,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r))
prs=[];p=1
while True:
    b=get(f'/repos/Secuura/Distributed_Secuura/pulls?state=open&per_page=100&page={p}')
    prs+=b
    if len(b)<100:break
    p+=1
out={}
for pr in prs:
    fs=[];q=1
    while True:
        b=get(f"/repos/Secuura/Distributed_Secuura/pulls/{pr['number']}/files?per_page=100&page={q}")
        fs+=[f['filename'] for f in b]
        if len(b)<100:break
        q+=1
    out[pr['number']]={'title':pr['title'],'base':pr['base']['ref'],'files':fs}
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(out),'PRs',sum(len(v['files']) for v in out.values()),'files')
