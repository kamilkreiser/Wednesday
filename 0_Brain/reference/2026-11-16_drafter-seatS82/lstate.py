import sys
sys.path.insert(0, "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatS-81st/tools")
import boot_lib_s81 as b
env=b.load_env(); H={"Authorization":env["LINEAR_API_KEY"],"Content-Type":"application/json"}
Q="""query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}},number:{eq:$n}},includeArchived:true){nodes{identifier state{name} assignee{displayName} comments(first:100){nodes{createdAt}}}}}"""
for k in sys.argv[1:]:
    s,r=b.http("https://api.linear.app/graphql",H,{"query":Q,"variables":{"n":float(k)}})
    for n in r["data"]["issues"]["nodes"]:
        cs=[c["createdAt"] for c in n["comments"]["nodes"]]
        a=(n["assignee"] or {}).get("displayName") or "unassigned"
        print("- KS-%s %s, %s, %d comments, newest %s | Linear GraphQL issues(filter number=%s, team KS, includeArchived) read live | read 2026-11-16"%(k,n["state"]["name"],a,len(cs),max(cs) if cs else "none",k))
