import os,json,urllib.request,sys
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
    d=q('query($a:String){issues(first:100,after:$a,filter:{state:{type:{in:["backlog","unstarted","started"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title description state{name} estimate labels{nodes{name}} comments{nodes{body}}}}}',{'a':after})
    n=d['data']['issues'];out+=n['nodes']
    if not n['pageInfo']['hasNextPage']:break
    after=n['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(out))
