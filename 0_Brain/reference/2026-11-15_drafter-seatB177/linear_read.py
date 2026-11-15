import json, sys, urllib.request
ENVF="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key=[l.split("=",1)[1].strip().strip('"').strip("'") for l in open(ENVF) if l.startswith("LINEAR_API_KEY=")][0]
def gq(q,v=None):
    req=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":v or {}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=60))
    assert not d.get("errors"),str(d["errors"])[:300]
    return d["data"]
Q="""query($id:String!){issue(id:$id){identifier title updatedAt archivedAt state{name type} team{id key name} assignee{name} labels{nodes{name}} attachments{nodes{title url}} comments(first:50){pageInfo{hasNextPage} nodes{id createdAt user{name} body}}}}"""
team=None
for k in sys.argv[1:]:
    i=gq(Q,{"id":k})["issue"]
    team=team or i["team"]["id"]
    cs=sorted(i["comments"]["nodes"],key=lambda c:c["createdAt"])
    print(f"{i['identifier']} [{i['state']['name']}/{i['state']['type']}] updatedAt {i['updatedAt']} assignee {i['assignee']['name'] if i['assignee'] else None} labels {[l['name'] for l in i['labels']['nodes']]} | {i['title'][:90]}")
    print(f"   comments {len(cs)} more={i['comments']['pageInfo']['hasNextPage']} oldest {cs[0]['createdAt'][:19] if cs else None} newest {cs[-1]['createdAt'][:19] if cs else None} newest-author {(cs[-1]['user'] or {}).get('name') if cs else None}")
    print("   attachments:",[(a['title'][:40],a['url'][-45:]) for a in i['attachments']['nodes']][:6])
    if k in ("KS-1699",) and cs:
        for c in cs[-3:]:
            print("   --",c["createdAt"][:19],(c["user"] or {}).get("name"),"|",c["body"][:500].replace("\n"," / "))
