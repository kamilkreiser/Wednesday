import json,sys
def load(p): return {(r['route'],r['fault'],r['v']):r for r in map(json.loads,open(p))}
h=load(sys.argv[1]); b=load(sys.argv[2]); plant=len(sys.argv)>3
if plant:
    k=('revoke','repo save post','msgtostr'); h[k]=dict(h[k]); h[k]['state']=json.loads(json.dumps(h[k]['state'])); h[k]['state']['documents'][0]['status']='certified'
    k=('share','saveShare#1 post','msgobj'); h[k]=dict(h[k]); h[k]['status']='NO ANSWER'
ok=diff=0
for k,r in sorted(h.items()):
    o=h[(k[0],k[1],'ord')]
    for f in ['status','body','state','sql','anchorCalls','notifies','disposition','fired']:
        if r[f]!=o[f]: diff+=1; print('DIFF vs ord',k,f,str(r[f])[:80],'|',str(o[f])[:80])
        else: ok+=1
    if len(r['routeErr'])!=1 or not isinstance(r['routeErr'][0],dict) or not isinstance(r['routeErr'][0].get('error'),str): diff+=1; print('DIFF reason not one string',k,r['routeErr'])
    else: ok+=1
    if r['state']!=b[k]['state']: diff+=1; print('DIFF state vs c415',k)
    else: ok+=1
print(f'OK {ok} DIFF {diff}')
