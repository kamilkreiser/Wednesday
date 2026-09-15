#!/usr/bin/env python3
"""derive_candidates.py — the board → tiered CANDIDATE list for Ornith briefs (read-only; Kam 2026-09-15 18:19 / 18:23).

Reads every KS Backlog/Todo ticket (paginated, no cap — `board_count.sh` rules), applies the contract's
cheap predicates from the ticket TEXT, and writes `night/candidates.md`: tickets grouped by TIER (easy → hard,
Kam 16:40 order) with, per ticket, the product-file guess, the runner kind, and the reason a ticket is
EXCLUDED. It is a CENSUS for the coordinator to write briefs from — never an instruction to the model
(a classification list is a representation of the items, 2026-09-07). Tickets already held as READY_*,
already in done.md as PASS, or set aside with a recorded reason are carried in their own sections so a
successor does not re-read them.

Usage: LINEAR_API_KEY from the Secuura .env (sourced by the caller — never printed), then
       python3 derive_candidates.py [--out night/candidates.md]
"""
import json, os, re, sys, glob, urllib.request, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "candidates.md")
KEY = os.environ.get("LINEAR_API_KEY") or sys.exit("derive_candidates: LINEAR_API_KEY unset — source the Secuura .env first")

# Set-aside register: id → reason (recorded the day it was read; a successor re-reads a ticket only when its updatedAt moves).
SET_ASIDE = {
    "KS-1112": "two files: option 1 reds ks1029's A1 cell (2026-09-15 18:45)",
    "KS-1113": "an e2e spec under tests/e2e — no Playwright checker yet",
    "KS-1142": "a test refactor with no product tamper", "KS-1132": "services/auth — security surface (Kam 16:40: auth LAST)",
    "KS-849": "kyc has no in-process driver (app.listen at import)", "KS-1128": "the seed's pg is a require inside the function",
    "KS-979": "comment-only: no cell can red it", "KS-980": "decision-class (a second DB role or a claim correction)",
    "KS-1159": "a guard widening with three fixture files — later tier", "KS-757": "blocked by the ticket's own measurement",
    "KS-1114": "decision-class (spec vs implementation of a title strategy)", "KS-1129": "three services, anchoring index.ts listens on import",
    "KS-590": "verification.ts, security-adjacent", "KS-1119": "multi-tenant security surface",
    "KS-1111": "a masking guard with an unruled fix-shape (a)/(b), security-adjacent", "KS-755": "diagnosis-first (which side is wrong is unmeasured)",
    "KS-981": "lives only on the frozen #892 branch", "KS-777": "tracker ticket — all four findings FIXED on #795; a board close",
    "KS-1076": "likely already fixed at M55 (docblock present since ec61abf8e/0882f7661) — measure with eslint in a tool-mode clone; item 2 is a Claude seat's",
    "KS-880": "two-file refactor (Claude seat)", "KS-889": "a measurement/ruling ticket, not a patch",
}
AUTH = re.compile(r"\b(auth|mfa|oauth|login|session|jwt|password|csrf|rbac|permission|lockout|token)\b", re.I)
PATH = re.compile(r"(?:Blockchain/Dev/)?((?:services/[a-z0-9\-]+|packages/shared)/src/[\w./\-]+\.ts|systemTest/(?:performance|akto|playwright|fixtures)/[\w./\-]+\.ts)(?::(\d+))?")
FIX = re.compile(r"^##+\s*(fix[- ]shape|recommendation|fix:|acceptance|the fix|what needs doing)", re.I | re.M)

def q(query, variables=None):
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Authorization": KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))

nodes, cursor = [], None
while True:
    r = q("""query($c:String){ issues(first:100, after:$c, filter:{ team:{key:{eq:"KS"}}, state:{type:{in:["backlog","unstarted"]}} }){
          pageInfo{hasNextPage endCursor} nodes{ identifier title priority updatedAt state{name} assignee{email} description attachments{nodes{url}} } } }""", {"c": cursor})
    d = r["data"]["issues"]; nodes += d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    cursor = d["pageInfo"]["endCursor"]

ready = sorted({re.match(r"READY_(KS-\d+)", os.path.basename(f)).group(1) for f in glob.glob(os.path.join(HERE, "READY_*")) if re.match(r"READY_(KS-\d+)", os.path.basename(f))})
done_pass = set()
try:
    for l in open(os.path.join(HERE, "done.md"), encoding="utf-8"):
        m = re.match(r"(KS-\d+) .*verdict RESULT: PASS", l)
        if m: done_pass.add(m.group(1))
except FileNotFoundError: pass

tiers = {"T1 services (vitest, one file)": [], "T2 tooling (systemTest/*, one file)": [], "T3 jest services (originate, governance)": [], "T4 docs (doc_patch)": [], "T5 multi-file / later": []}
excluded, held, aside = [], [], []
for n in nodes:
    ident, title, desc = n["identifier"], n["title"], n["description"] or ""
    if ident in ready or ident in done_pass: held.append((ident, title[:80])); continue
    if ident in SET_ASIDE: aside.append((ident, SET_ASIDE[ident], n["updatedAt"][:10])); continue
    if any(x in (n["assignee"] or {}).get("email", "") for x in ("peter", "stuart")): excluded.append((ident, "on Peter/Stuart")); continue
    if any("/pull/" in (a["url"] or "") for a in n["attachments"]["nodes"]): excluded.append((ident, "has a PR attached")); continue
    if AUTH.search(title): excluded.append((ident, "auth-shaped title (LAST, Kam 16:40)")); continue
    files = []
    for m in PATH.finditer(desc):
        p = m.group(1)
        if "__tests__" in p or p.endswith(".test.ts") or "/tests/" in p: continue
        if p not in files: files.append(p)
    if not files: excluded.append((ident, "names no product file")); continue
    if "docs/" in desc and not files: tiers["T4 docs (doc_patch)"].append((ident, n["priority"], title[:80], files)); continue
    if len(files) > 1: tiers["T5 multi-file / later"].append((ident, n["priority"], title[:80], files[:3])); continue
    f = files[0]
    if f.startswith("systemTest/"): tiers["T2 tooling (systemTest/*, one file)"].append((ident, n["priority"], title[:80], [f]))
    elif f.startswith("services/originate/") or f.startswith("services/governance/"): tiers["T3 jest services (originate, governance)"].append((ident, n["priority"], title[:80], [f]))
    else: tiers["T1 services (vitest, one file)"].append((ident, n["priority"], title[:80], [f]))

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
with open(OUT, "w", encoding="utf-8") as o:
    o.write(f"# Ornith candidates — derived {now} from {len(nodes)} KS Backlog/Todo tickets (read-only, unpaginated)\n\n")
    o.write("A CENSUS for the coordinator to brief from, easy → hard (Kam 2026-09-15 16:40 / 18:19). A ticket here is a candidate, not a task: read it, read the file at the tip, write `night/briefs/<id>.md`, then queue it. Auth-shaped titles are excluded (LAST); Peter/Stuart tickets and PR-attached tickets are excluded outright.\n\n")
    for t, rows in tiers.items():
        rows.sort(key=lambda r: (r[1] or 9, r[0]))
        o.write(f"## {t} — {len(rows)}\n")
        for r in rows: o.write(f"- {r[0]} (P{r[1]}) {r[2]} — `{'`, `'.join(r[3])}`\n")
        o.write("\n")
    o.write(f"## HELD (READY_* or done.md PASS) — {len(held)}\n" + "".join(f"- {i} {t}\n" for i, t in sorted(held)) + "\n")
    o.write(f"## SET ASIDE with a recorded reason — {len(aside)} (re-read only if the ticket's updatedAt moved)\n" + "".join(f"- {i} — {r} (updated {u})\n" for i, r, u in sorted(aside)) + "\n")
    o.write(f"## EXCLUDED by predicate — {len(excluded)}\n" + "".join(f"- {i} — {r}\n" for i, r in sorted(excluded)) + "\n")
print(f"wrote {OUT}: " + " · ".join(f"{t.split(' ')[0]} {len(r)}" for t, r in tiers.items()) + f" · held {len(held)} · set-aside {len(aside)} · excluded {len(excluded)} (total {len(nodes)})")
