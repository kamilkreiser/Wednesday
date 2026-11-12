import collections, json, sys
REC = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatS-69th"
sys.path.insert(0, REC + "/tools")
from boot_lib_s69 import load_env, http
E = load_env(); H = {"Content-Type": "application/json", "Authorization": E["LINEAR_API_KEY"]}; T = E["LINEAR_TEAM_ID"]
Q = "query($f:IssueFilter,$a:String){ issues(first:50, after:$a, includeArchived:false, filter:$f){ nodes{identifier state{name} updatedAt} pageInfo{hasNextPage endCursor} } }"
def rd(f):
    out, a = [], None
    while True:
        st, d = http("https://api.linear.app/graphql", H, {"query": Q, "variables": {"f": f, "a": a}}, timeout=90)
        assert st == 200 and not d.get("errors")
        x = d["data"]["issues"]; out += x["nodes"]
        if not x["pageInfo"]["hasNextPage"]: return out
        a = x["pageInfo"]["endCursor"]
print("control", len(rd({"team": {"id": {"eq": T}}, "state": {"name": {"eq": "zz-none-xq9"}}})))
cur = rd({"team": {"id": {"eq": T}}})
old = {i["identifier"]: i for i in json.load(open(REC + "/evidence/board_all_after_s69.json"))["issues"]}
print("live", len(cur), "S69 after", len(old), dict(collections.Counter(i["state"]["name"] for i in cur)))
now = {i["identifier"]: i for i in cur}
print("only live:", sorted(set(now) - set(old))); print("only S69:", sorted(set(old) - set(now)))
ch = [(k, old[k]["state"]["name"], now[k]["state"]["name"]) for k in now if k in old and old[k]["state"]["name"] != now[k]["state"]["name"]]
print("state changes", ch)
print("updatedAt changed", sorted(k for k in now if k in old and old[k]["updatedAt"] != now[k]["updatedAt"]))
