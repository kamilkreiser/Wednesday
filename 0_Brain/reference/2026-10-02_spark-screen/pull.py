import json,os,sys,urllib.request
key=os.environ["LINEAR_API_KEY"]
flt=sys.argv[1]; out=sys.argv[2]
q='''query($after:String){ issues(first:50, after:$after, filter:%s) { nodes { identifier title createdAt updatedAt priority state{name type} assignee{name} creator{name} labels{nodes{name}} description comments(first:50){nodes{createdAt user{name} body}} attachments{nodes{url title}} } pageInfo{hasNextPage endCursor} } }'''%flt
nodes=[];after=None
while True:
    req=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":{"after":after}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req))
    if "errors" in d: print(d["errors"],file=sys.stderr); sys.exit(3)
    i=d["data"]["issues"]; nodes+=i["nodes"]
    if not i["pageInfo"]["hasNextPage"]: break
    after=i["pageInfo"]["endCursor"]
json.dump(nodes,open(out,"w"),indent=1)
print(len(nodes),"nodes")
for n in sorted(nodes,key=lambda n:n["identifier"]):
    print(n["identifier"],"|",n["state"]["name"],"|",(n["assignee"] or {}).get("name"),"|",n["createdAt"][:16],"|",n["updatedAt"][:16],"|",n["title"][:110])
