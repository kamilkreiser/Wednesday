# READ-ONLY GitHub GETs: PR 1944 (body, files) and every OPEN PR's file list. Token from the Secuura .env, never printed.
import json, os, sys, urllib.request, datetime
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944'
tok=''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
api='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r=urllib.request.urlopen(urllib.request.Request(api+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=60)
    return json.load(r)
def files(n):
    out=[];page=1
    while True:
        f=get(f'/pulls/{n}/files?per_page=100&page={page}')
        out+=f
        if len(f)<100: break
        page+=1
    return out
print('read at', datetime.datetime.utcnow().isoformat()+'Z')
pr=get('/pulls/1944')
open(W+'/evidence/pr1944_body.md','w').write(pr['body'] or '')
print('pr1944 state',pr['state'],'draft',pr['draft'],'head',pr['head']['sha'],'base',pr['base']['ref'],'title',pr['title'],'body chars',len(pr['body'] or ''))
mine=files(1944)
myfiles={f['filename']:f for f in mine}
print('pr1944 files',len(mine),'+',sum(f['additions'] for f in mine),'-',sum(f['deletions'] for f in mine))
opens=[];page=1
while True:
    p=get(f'/pulls?state=open&per_page=100&page={page}')
    opens+=p
    if len(p)<100: break
    page+=1
print('open PRs',len(opens),[o['number'] for o in opens])
res={}
for o in opens:
    if o['number']==1944: continue
    fl=files(o['number'])
    shared=[f['filename'] for f in fl if f['filename'] in myfiles]
    res[o['number']]={'title':o['title'],'head':o['head']['sha'],'created':o['created_at'],'files':[ {'f':f['filename'],'patch':f.get('patch','')} for f in fl if f['filename'] in myfiles]}
    print(o['number'],len(fl),'files; shared with 1944:',shared,'|',o['title'][:90])
json.dump(res,open(W+'/logs/open_pr_overlap.json','w'),indent=1)
