import collections, json, re, sys, urllib.request, datetime
REC = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-12_seatS-69th"
D = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS70"
sys.path.insert(0, REC + "/tools")
from boot_lib_s69 import load_env, http
E = load_env(); H = {"Content-Type": "application/json", "Authorization": E["LINEAR_API_KEY"]}; TEAM = E["LINEAR_TEAM_ID"]
print("now", datetime.datetime.now().isoformat())
def gql(q, v=None):
    st, d = http("https://api.linear.app/graphql", H, {"query": q, "variables": v or {}}, timeout=90)
    if st != 200 or not d or d.get("errors"):
        print("GQL ERR", st, str(d)[:300]); sys.exit(3)
    return d["data"]
F = "identifier title priority updatedAt state{name type} assignee{email} attachments(first:50){nodes{url sourceType title} pageInfo{hasNextPage}}"
Q = "query($f:IssueFilter,$a:String){ issues(first:40, after:$a, includeArchived:false, filter:$f){ nodes{%s} pageInfo{hasNextPage endCursor} } }" % F
def read(filt):
    out, a = [], None
    while True:
        d = gql(Q, {"f": filt, "a": a})["issues"]; out += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]: return out
        a = d["pageInfo"]["endCursor"]
ctl = read({"team": {"id": {"eq": TEAM}}, "state": {"name": {"eq": "zz-no-such-state-xq9"}}})
print("control made-up state: %d (must be 0)" % len(ctl))
ip = read({"team": {"id": {"eq": TEAM}}, "state": {"name": {"eq": "In Progress"}}})
print("In Progress live: %d" % len(ip))
json.dump(ip, open(D + "/ip_live.json", "w"))
txt = open(REC + "/ROUTING_2026-11-12.md", encoding="utf-8").read()
rows = re.findall(r"^\| (KS-\d+) \|", txt, re.M)
print("ROUTING rows %d distinct %d" % (len(rows), len(set(rows))))
rr = re.findall(r"^\| (KS-\d+) \|.*\[S 69th re-read\]", txt, re.M)
print("rows tagged [S 69th re-read]: %d distinct %d" % (len(rr), len(set(rr))))
done69 = set(rr)
part = set(l.strip() for l in open(REC + "/evidence/partition_s69.txt") if l.strip())
print("partition", len(part))
TOK = None
for l in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env", encoding="utf-8", errors="replace"):
    m = re.match(r"\s*(?:export\s+)?GH_TOKEN=(.*)$", l.rstrip("\n"))
    if m: TOK = m.group(1).strip().strip("\"'")
def prs_of(i):
    return [int(m.group(1)) for a in i["attachments"]["nodes"] for m in [re.fullmatch(r"https://github.com/Secuura/Distributed_Secuura/pull/(\d+)", a["url"])] if m]
prs = set()
for i in ip: prs |= set(prs_of(i))
WAIT = [2176,2123,2124,2136,2138,2139,2140,2142,2143,2145,2146,2170,2169,2187,2188,2190,2191,2192,2193,2195,2197,2198,2157,2205,2203,2206,2207]
CT = [2184,2185,2194,2200,2201,2204,2199,2186,2173,2175,2109,2208,2209,2210,2211]
allp = sorted(prs | set(WAIT) | set(CT))
state = {}; heads = {}
for k in range(0, len(allp), 80):
    ch = allp[k:k+80]
    q = "query { repository(owner:\"Secuura\", name:\"Distributed_Secuura\") { %s } rateLimit{remaining} }" % " ".join("p%d: pullRequest(number:%d){number state merged mergedAt mergeCommit{oid} headRefOid title}" % (n, n) for n in ch)
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q}).encode(), headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json", "User-Agent": "board-reader/1.0"})
    js = json.load(urllib.request.urlopen(req, timeout=120))
    for e in js.get("errors") or []: print("GH ERR", json.dumps(e)[:160])
    for n in ch:
        d = js["data"]["repository"].get("p%d" % n)
        state[n] = None if d is None else ("MERGED" if d["merged"] else d["state"])
        if d: heads[n] = (d["headRefOid"][:12], d["mergedAt"], (d["mergeCommit"] or {}).get("oid", "")[:12] if d["mergeCommit"] else "", d["title"][:70])
    print("rate", js["data"]["rateLimit"])
json.dump({str(k): [state[k]] + list(heads.get(k, [])) for k in state}, open(D + "/pr_states.json", "w"))
print("states", dict(collections.Counter(state.values())))
for n in WAIT + CT: print(n, state[n], heads.get(n, "-"))
HUM = {"peter@obeden.com", "stuart.jamieson@secuura.ai"}
rowset = set(rows)
A = {i["identifier"] for i in ip if i["identifier"] not in rowset}
B = {i["identifier"] for i in ip if not any(state.get(n) == "OPEN" for n in prs_of(i))}
C = {i["identifier"] for i in ip if i["identifier"] not in part}
Dd = {i["identifier"] for i in ip if (i["assignee"] or {}).get("email") not in HUM}
print("alone a,b,c,d", len(A), len(B), len(C), len(Dd), "cum", len(A), len(A&B), len(A&B&C), len(A&B&C&Dd), sorted(A&B&C&Dd))
print("In Progress keys without a row:", sorted(A))
allm = [i for i in ip if prs_of(i) and all(state.get(n) == "MERGED" for n in prs_of(i))]
coh = sorted([i for i in allm if i["identifier"] in rowset and i["identifier"] not in part and (i["assignee"] or {}).get("email") not in HUM], key=lambda i: int(i["identifier"][3:]))
print("COHORT now", len(coh))
old = [l.split("\t")[0] for l in open(REC + "/evidence/reread_cohort_s69.txt")]
now = [i["identifier"] for i in coh]
print("old cohort", len(old), "in now", len(set(old) & set(now)), "left cohort", sorted(set(old) - set(now), key=lambda k: int(k[3:])), "new in cohort", sorted(set(now) - set(old), key=lambda k: int(k[3:])))
unread = [k for k in now if k not in done69]
print("UNREAD (cohort now minus S69 re-read rows)", len(unread), "first 8", unread[:8])
old_unread = [k for k in old if int(k[3:]) >= 1336]
print("old cohort from KS-1336:", len(old_unread), "of which with an S69 re-read row", [k for k in old_unread if k in done69], "not in now:", [k for k in old_unread if k not in now])
with open(D + "/cohort_s70.txt", "w") as f:
    for i in coh: f.write("%s\t%s\t%s\n" % (i["identifier"], ",".join(map(str, prs_of(i))), i["title"][:90].replace("\t", " ")))
print("humans in allm:", [(i["identifier"], i["assignee"]["email"]) for i in allm if (i["assignee"] or {}).get("email") in HUM])
