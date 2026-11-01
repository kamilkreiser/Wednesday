import re,json,urllib.request,sys
key=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?(LINEAR_API_KEY)=(.*)$',l.rstrip('\n'))
    if m: key=m.group(2).strip().strip('"\'')
assert key,'no linear key'
Q='''query($after:String){issues(first:100,after:$after,filter:{state:{type:{in:["backlog","unstarted","started"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title description priority createdAt state{name type} team{key} labels{nodes{name}} comments{nodes{id}}}}}'''
out=[];after=None
while True:
    rq=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':Q,'variables':{'after':after}}).encode(),headers={'Authorization':key,'Content-Type':'application/json'})
    r=json.loads(urllib.request.urlopen(rq,timeout=60).read())
    if 'errors' in r: print(r['errors'][0]['message'][:200]); break
    d=r['data']['issues']; out+=d['nodes']
    if not d['pageInfo']['hasNextPage']: break
    after=d['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'))
print(len(out))
