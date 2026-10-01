import json,os,sys,urllib.request
key=os.environ["LINEAR_API_KEY"]
for ident in sys.argv[1:]:
    q='{ issue(id:"%s") { identifier history(first:30){ nodes { createdAt actor{name} addedLabels{name} removedLabels{name} fromState{name} toState{name} updatedDescription fromTitle toTitle relationChanges{identifier type} fromAssignee{name} toAssignee{name} } } } }'%ident
    req=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req))
    if "errors" in d: print(ident,d["errors"]); continue
    h=[x for x in d["data"]["issue"]["history"]["nodes"] if x["createdAt"]>"2026-10-01T00:11"]
    print("==",ident,len(h),"history rows since 00:11Z")
    for x in h:
        print("  ",x["createdAt"][:16],(x["actor"] or {}).get("name"),{k:v for k,v in x.items() if v and k not in("createdAt","actor")})
