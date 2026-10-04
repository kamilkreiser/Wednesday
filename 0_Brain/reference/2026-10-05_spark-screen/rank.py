import json,re,collections
B=json.load(open("/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8e88f5e9-abc4-4750-a2ee-28cce52428dd/scratchpad/spark1005/board.json"))
EXCL={1015,1404,1382,1355,1406,1402,623,938,1009,1219,1250}
SEC=re.compile(r"auth|token|credential|secret|password|mfa|oauth|jwt|csrf|xss|injection|rls|security|vuln|cve|advisor|tenant|permission|privilege|bypass|sign(ature|ed)|encrypt|crypt|key vault|keyvault|session|cookie|cors|ssrf|rbac|admin|lockout|login|ddos|rate.?limit|audit",re.I)
DEC=re.compile(r"decide|decision|ruling|your view|kam's call|kamil's call|needs kam|choose|which (one|way)|not prescribed|whoever picks it up should decide",re.I)
FILE=re.compile(r"`([A-Za-z0-9_./\-]+\.(?:ts|tsx|js|mjs|cjs|sh|py|ya?ml|json|md|env\.example|example|sql|conf|toml))(?::\d+)?")
rows=[]
for n in B:
    num=int(n["identifier"].split("-")[1]); a=(n["assignee"] or {}).get("name") or ""
    t=n["title"]; d=n["description"] or ""
    why=[]
    if num in EXCL: why.append("commission")
    if re.search(r"peter|stuart",a,re.I): why.append("assignee:"+a)
    if SEC.search(t): why.append("sec-title")
    labs=[l["name"] for l in n["labels"]["nodes"]]
    files=set(FILE.findall(d))
    dec=bool(DEC.search(d))
    rows.append((num,n["state"]["name"][:4],a.split("@")[0][:8],len(files),dec,";".join(why),t[:95],labs))
rows.sort(key=lambda r:(bool(r[5]),r[4],r[3] if r[3] else 99))
ok=[r for r in rows if not r[5]]
print("total",len(rows),"excluded",len(rows)-len(ok),"remaining",len(ok))
c=collections.Counter(w for r in rows for w in r[5].split(";") if w); print(c.most_common(12))
for r in ok: print(f"KS-{r[0]} {r[1]} {r[2]:8} files={r[3]:2} dec={int(r[4])} {r[6]}")
