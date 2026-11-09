import json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']
def q(query,var=None):
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':query,'variables':var or {}}).encode(),{'Authorization':key,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
for n in (1960,1739,1712):
    d=q('query($n:Float){issues(filter:{team:{key:{eq:"KS"}},number:{eq:$n}}){nodes{identifier title description priority url state{name} labels{nodes{name}} comments(first:50){nodes{body createdAt}}}}}',{'n':n})
    json.dump(d['data']['issues']['nodes'],open(f'{sys.argv[1]}/ks_{n}.json','w'),indent=1)
    for i in d['data']['issues']['nodes']:
        print('#####',i['identifier'],i['title'],i['state']['name'],[l['name'] for l in i['labels']['nodes']]); print(i['description']); 
        for c in i['comments']['nodes']: print('--- comment',c['createdAt']); print(c['body'])
