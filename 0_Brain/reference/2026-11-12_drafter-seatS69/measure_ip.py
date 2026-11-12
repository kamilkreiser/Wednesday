import sys, json, re, collections, urllib.request
sys.path.insert(0, "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatS-68th/tools")
from boot_lib_s68 import load_env, http
REC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatS-68th"
E=load_env(); H={"Content-Type":"application/json","Authorization":E["LINEAR_API_KEY"]}; TEAM=E["LINEAR_TEAM_ID"]
def gql(q,v=None):
    st,d=http("https://api.linear.app/graphql",H,{"query":q,"variables":v or {}},timeout=90)
    if st!=200 or not d or d.get("errors"): print("GQL ERR",st,str(d)[:300]); sys.exit(3)
    return d["data"]
F="identifier title priority updatedAt state{name type} assignee{email} parent{identifier} attachments(first:20){nodes{url sourceType title}} labels{nodes{name}}"
Q="query($f:IssueFilter,$a:String){ issues(first:40, after:$a, includeArchived:false, filter:$f){ nodes{%s} pageInfo{hasNextPage endCursor} } }"%F
def read(filt):
    out=[];a=None
    while True:
        d=gql(Q,{"f":filt,"a":a})["issues"]; out+=d["nodes"]
        if not d["pageInfo"]["hasNextPage"]: return out
        a=d["pageInfo"]["endCursor"]
ctl=read({"team":{"id":{"eq":TEAM}},"state":{"name":{"eq":"zz-no-such-state-xq9"}}})
print("control made-up state:",len(ctl),"(must be 0)")
ip=read({"team":{"id":{"eq":TEAM}},"state":{"name":{"eq":"In Progress"}}})
print("In Progress read live:",len(ip))
# all states census for context
allc=collections.Counter()
json.dump(ip,open(sys.argv[1],"w"))
