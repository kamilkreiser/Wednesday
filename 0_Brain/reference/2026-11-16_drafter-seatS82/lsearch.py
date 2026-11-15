import sys, json
sys.path.insert(0, "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatS-81st/tools")
import boot_lib_s81 as b
env = b.load_env()
H = {"Authorization": env["LINEAR_API_KEY"], "Content-Type": "application/json"}
def q(query, variables):
    s, r = b.http("https://api.linear.app/graphql", H, {"query": query, "variables": variables}, timeout=90)
    return r
QI = """query($t:String!,$a:String){ issues(first:100, after:$a, includeArchived:true, filter:{team:{key:{eq:"KS"}}, or:[{title:{containsIgnoreCase:$t}},{description:{containsIgnoreCase:$t}}]}){ nodes{identifier state{name} assignee{displayName}} pageInfo{hasNextPage endCursor}}}"""
QC = """query($t:String!,$a:String){ comments(first:100, after:$a, filter:{body:{containsIgnoreCase:$t}, issue:{team:{key:{eq:"KS"}}}}){ nodes{createdAt issue{identifier state{name}}} pageInfo{hasNextPage endCursor}}}"""
def allp(Q, key, t):
    out=[]; a=None
    while True:
        r=q(Q,{"t":t,"a":a})
        if not r or "errors" in r or not r.get("data"):
            return ["ERR "+json.dumps(r)[:200]]
        d=r["data"][key]; out+=d["nodes"]
        if not d["pageInfo"]["hasNextPage"]: return out
        a=d["pageInfo"]["endCursor"]
for t in sys.argv[1:]:
    i=allp(QI,"issues",t); c=allp(QC,"comments",t)
    if i and isinstance(i[0],str): print(t,"->",i[0]); continue
    ids=sorted(set(n["identifier"]+"("+n["state"]["name"]+")" for n in i))
    cids=sorted(set(n["issue"]["identifier"]+"("+n["issue"]["state"]["name"]+")" for n in c))
    print("SEARCH %r: issues %d, comments %d | I: %s | C: %s" % (t,len(ids),len(cids)," ".join(ids[:14]), " ".join(cids[:14])))
