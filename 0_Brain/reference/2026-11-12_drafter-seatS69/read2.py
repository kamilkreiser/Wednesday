import sys
sys.path.insert(0, "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatS-68th/tools")
from boot_lib_s68 import load_env, http
E=load_env(); H={"Content-Type":"application/json","Authorization":E["LINEAR_API_KEY"]}
Q="query($t:String!){ issue(id:$t){ identifier title priority createdAt updatedAt state{name} assignee{email} parent{identifier} description comments(first:50){nodes{id createdAt user{email} body}} attachments(first:20){nodes{url title}} history(first:10){nodes{createdAt fromState{name} toState{name}}} } }"
for k in sys.argv[1:]:
    st,d=http("https://api.linear.app/graphql",H,{"query":Q,"variables":{"t":k}},timeout=60)
    i=d["data"]["issue"]
    print("=====",i["identifier"],i["state"]["name"],"p",i["priority"],"created",i["createdAt"],"updated",i["updatedAt"],"assignee",i["assignee"],"parent",i["parent"])
    print("TITLE",i["title"]); print("ATT",i["attachments"]["nodes"])
    print("STATE HISTORY",[(h["createdAt"],(h["fromState"] or {}).get("name"),(h["toState"] or {}).get("name")) for h in i["history"]["nodes"]])
    print("DESC",len(i["description"] or ""),"B"); print((i["description"] or "")[:1800])
    cs=i["comments"]["nodes"]; print("COMMENTS",len(cs))
    for c in cs[-3:]: print("--",c["id"][:8],c["createdAt"],(c["user"] or {}).get("email"),len(c["body"]),"B:",c["body"][:500].replace("\n"," "))
