import json,urllib.request,os,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']; team=env['LINEAR_TEAM_ID']
Q='''query($team:ID!,$after:String){issues(first:100,after:$after,filter:{team:{id:{eq:$team}},state:{type:{in:["backlog","unstarted"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title priority state{name} labels{nodes{name}} description}}}'''
out=[];after=None
while True:
    req=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':Q,'variables':{'team':team,'after':after}}).encode(),{'Content-Type':'application/json','Authorization':key})
    d=json.load(urllib.request.urlopen(req))
    if 'errors' in d: print(d['errors']); sys.exit(1)
    r=d['data']['issues']; out+=r['nodes']
    if not r['pageInfo']['hasNextPage']: break
    after=r['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'))
print(len(out))
