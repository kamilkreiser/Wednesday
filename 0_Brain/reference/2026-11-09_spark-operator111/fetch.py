import os,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']; team=env.get('LINEAR_TEAM_ID')
def q(query,var=None):
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':query,'variables':var or {}}).encode(),{'Authorization':key,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
out=[];after=None
while True:
    d=q('query($a:String){issues(first:100,after:$a,filter:{number:{gte:2127}}){pageInfo{hasNextPage endCursor} nodes{identifier title description state{name} labels{nodes{name}} comments{nodes{body}}}}}',{'a':after})
    n=d['data']['issues'];out+=n['nodes']
    if not n['pageInfo']['hasNextPage']:break
    after=n['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'),indent=1)
for i in sorted(out,key=lambda x:int(x['identifier'][3:])):
    print(i['identifier'],i['state']['name'],len(i['comments']['nodes']),i['title'][:110])
