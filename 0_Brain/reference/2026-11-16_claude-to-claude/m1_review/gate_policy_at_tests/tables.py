# QA-POLICY-AT: tables of the probe rows (the fixed corpus) from one seed's base and head outputs.
# usage: python3 -B -I tables.py <base.jsonl> <head.jsonl> <out.md>
import sys, json
COLS = ["decide", "would", "m:live", "m:live_shell", "m:expired", "m:other", "m:nobody",
        "o:none", "o:StillAsk", "o:Allowed", "o:Allowed_other", "o:Allowed_nobody"]
SHOW = [("o:none", 7), ("o:StillAsk", 8), ("o:Allowed", 9), ("both-agree", 3)]

def code(c):
    k = c["k"]
    if k == "A":
        return "U" if "OwnerChoseAllow" in c["w"] else ("B" if "Bypass" in c["w"] else "allow(grant)")
    if k == "Q":
        rs = c["rs"]
        extra = [r for r in rs if r != "ShellExpansion"]
        return "a" + c["tier"][1:] + ("+" + ",".join(sorted(set(r.split('(')[0] for r in extra))) if extra else "")
    r = c["r"]
    if r.startswith("TooLarge"): return "L"
    if r == "Excluded": return "X"
    if r.startswith("HardDeny"): return "H"
    if r.startswith("RefusedInAllow") or r.startswith("BypassRefused"):
        t = r[r.find('"') + 1:r.rfind('"')]
        cls = {"a credential store, or a folder that holds one": "C", "names CoAgent's own programs or an agent program": "P",
               "a tool the gate has not been taught": "T", "privilege escalation": "Pv"}.get(t, t[:20])
        return ("r" if r.startswith("Refused") else "b") + cls
    return r[:20]

def cols4(row, st):
    c = row["cols"][st]
    return " ".join(code(c[i]) for _, i in SHOW) + " | d=" + code(c[0])

if __name__ != "__main__": raise SystemExit
b = [json.loads(l) for l in open(sys.argv[1]) if '"full":' in l or True]
h = [json.loads(l) for l in open(sys.argv[2])]
out = []
P = out.append
fixed = [(x, y) for x, y in zip(b, h) if not x["id"].startswith(("c2", "c3"))]
GROUPS = {}
for x, y in fixed:
    GROUPS.setdefault(x["grp"], []).append((x, y))
STATES = ["nothing", "**/.env*", "**/secret/**", ".env*", "default", "grant-only", "sandboxOn+**/.env*", "**/example.com/**", "*.com", "**/.env*+**/secret/**"]
for g, rows in GROUPS.items():
    P(f"\n### {g} ({len(rows)} rows)\n")
    P("| id | tool | cwd | command / input | state | base: no view / StillAsk / Allowed / both-agree, decide | head: same | changed |")
    P("|---|---|---|---|---|---|---|---|")
    for x, y in rows:
        inp = x["input"]
        try:
            j = json.loads(inp); txt = j.get("command") if isinstance(j, dict) and isinstance(j.get("command"), str) else inp
        except Exception:
            txt = inp
        txt = txt if len(txt) <= 90 else txt[:60] + f"…({len(txt)} chars)"
        txt = txt.replace("|", "\\|").replace("\n", "\\n")
        for st in STATES:
            cb, ch = cols4(x, st), cols4(y, st)
            same = x["cols"][st] == y["cols"][st]
            if st in ("nothing", "**/.env*", "**/secret/**") or not same:
                P(f"| {x['id']} | {x['tool']} | {x['cwd'].replace('<root>/', '')} | `{txt}` | {st} | {cb} | {ch} | {'=' if same else '**CHANGED**'} |")
open(sys.argv[3], "w").write("\n".join(out) + "\n")
print("fixed rows", len(fixed), "groups", {g: len(r) for g, r in GROUPS.items()})
