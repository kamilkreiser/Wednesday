import os,json,urllib.request,re,sys
env=open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env').read()
m=re.search(r'^LINEAR_API_KEY=(.*)$',env,re.M); k=m.group(1).strip().strip('"\'')
def q(query,vars=None):
    r=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':query,'variables':vars or {}}).encode(),headers={'Authorization':k,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=60))
Q='''query($after:String){issues(first:100,after:$after,filter:{team:{key:{eq:"KS"}},state:{type:{in:["backlog","unstarted","started"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title state{name type} assignee{email} labels{nodes{name}} priority estimate createdAt updatedAt description comments(first:50){nodes{createdAt body user{email}}}}}}'''
out=[];after=None;pages=0
while True:
    d=q(Q,{'after':after})
    if 'errors' in d: print(d['errors']);sys.exit(1)
    i=d['data']['issues'];out+=i['nodes'];pages+=1
    if not i['pageInfo']['hasNextPage']:break
    after=i['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'))
print(pages,len(out),len({x['identifier'] for x in out}))
