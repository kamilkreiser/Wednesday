import sys, json
sys.path.insert(0, "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatS-81st/tools")
import boot_lib_s81 as b
env = b.load_env()
H = {"Authorization": env["LINEAR_API_KEY"], "Content-Type": "application/json"}
def q(query, variables=None):
    s, r = b.http("https://api.linear.app/graphql", H, {"query": query, "variables": variables or {}})
    return r
Q = """query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true){ nodes{ identifier title state{name} assignee{displayName} priority archivedAt updatedAt description
 comments(first:50){ nodes{ createdAt user{displayName} body } } } } }"""
for k in sys.argv[1:]:
    r = q(Q, {"n": float(k)})
    for n in r["data"]["issues"]["nodes"]:
        cs = n["comments"]["nodes"]
        print("=== %s | %s | %s | %s | prio %s | archived %s | comments %d | newest %s" % (n["identifier"], n["title"], n["state"]["name"], (n["assignee"] or {}).get("displayName"), n["priority"], n["archivedAt"], len(cs), max([c["createdAt"] for c in cs], default="none")))
        print("DESC:", (n["description"] or "")[:7000].replace("\n", " / "))
        for c in cs:
            print("  C %s %s: %s" % (c["createdAt"], (c["user"] or {}).get("displayName"), c["body"][:3500].replace("\n", " / ")))
