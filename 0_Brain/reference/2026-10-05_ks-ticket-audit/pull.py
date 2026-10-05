import os,json,urllib.request,sys
key=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if l.startswith('LINEAR_API_KEY='): key=l.split('=',1)[1].strip().strip('"\'')
Q='''query($after:String){ issues(first:100, after:$after, includeArchived:true, filter:{team:{key:{eq:"KS"}}}){ pageInfo{hasNextPage endCursor}
 nodes{ identifier title priority createdAt completedAt canceledAt archivedAt state{name type} creator{name} assignee{name} labels{nodes{name}} parent{identifier} } } }'''
out=[];after=None
while True:
    req=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({"query":Q,"variables":{"after":after}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=60))
    if 'errors' in d: print(d['errors'],file=sys.stderr); sys.exit(2)
    c=d['data']['issues']; out+=c['nodes']
    if not c['pageInfo']['hasNextPage']: break
    after=c['pageInfo']['endCursor']
json.dump(out,open(sys.argv[1],'w'))
print("fetched",len(out),"pages done")
