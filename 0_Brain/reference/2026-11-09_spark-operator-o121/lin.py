import json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']
def q(query,var=None):
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':query,'variables':var or {}}).encode(),{'Authorization':key,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
for t in sys.argv[1:]:
    n=int(t.split('-')[1])
    d=q('query($n:Float){issues(filter:{team:{key:{eq:"KS"}},number:{eq:$n}}){nodes{identifier title description priority state{name} comments(first:40){nodes{body createdAt}}}}}',{'n':n})
    for i in d['data']['issues']['nodes']:
        print('#####',i['identifier'],i['title'],'prio',i['priority'],i['state']['name']);print(i['description']);
        for c in sorted(i['comments']['nodes'],key=lambda c:c['createdAt'],reverse=True): print('--- comment',c['createdAt']);print(c['body'][:2500])
