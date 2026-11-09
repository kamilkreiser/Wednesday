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
    d=q('query($a:String){issues(first:50,after:$a,filter:{team:{key:{eq:"KS"}},state:{type:{in:["backlog","unstarted","started"]}},priority:{lte:2,gte:1}}){pageInfo{hasNextPage endCursor} nodes{identifier title description priority url state{name type} estimate createdAt updatedAt labels{nodes{name}} comments(first:30){nodes{body createdAt}}}}}',{'a':after})
    if 'errors' in d: print(d['errors']);break
    n=d['data']['issues'];out+=n['nodes']
    if not n['pageInfo']['hasNextPage']:break
    after=n['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(out))
