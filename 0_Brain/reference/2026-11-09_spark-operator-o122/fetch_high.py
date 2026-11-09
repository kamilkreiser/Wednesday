import json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']
def q(query,var=None):
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':query,'variables':var or {}}).encode(),{'Authorization':key,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
out=[];after=None
while True:
    d=q('query($a:String){issues(first:50,after:$a,filter:{team:{key:{eq:"KS"}},priority:{lte:2,gte:1},state:{type:{in:["backlog","unstarted"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title description priority state{name} labels{nodes{name}}}}}',{'a':after})
    iss=d['data']['issues']; out+=iss['nodes']
    if not iss['pageInfo']['hasNextPage']: break
    after=iss['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'))
print(len(out))
