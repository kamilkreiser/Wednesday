#!/usr/bin/env python3
"""Gate 70 own mutants on #1884 R2b (ecfe4f07), adapted from gate 68's mutants.py. Each mutant = list of (file, old, new[, count])
edits, every `old` asserted to occur exactly `count` times (default 1), the mutated text asserted PRESENT on disk before any job
runs. Jobs run with --json and are scored PER CELL against the unmutated baseline (KILLED when a cell green at baseline goes red;
INVALID when a file collects 0 tests). Every product file is restored from `git show <head>:<file>` and its sha256 checked after
every mutant. probe70 is placed in src/__tests__ for this session only and moved to the scratchpad quarantine at the end.
Jobs run ONE AT A TIME through jest_run.sh (nice 10; waits while load1 > 8)."""
import subprocess, sys, os, json, hashlib, shutil, time

G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884"
R = f"{G}/repo"
HEAD = "ecfe4f07fdcec78b8d45d897bd4dccd4be829be7"
REL = "Blockchain/Dev/services/originate/src"
ROUTE_F = f"{REL}/routes/documents.ts"
INF_F = f"{REL}/services/reanchorInFlight.ts"
REPO_F = f"{REL}/repositories/documentRepo.ts"
RES_F = f"{REL}/services/anchorResolution.ts"
PRODUCT = (ROUTE_F, INF_F, REPO_F, RES_F)
OUT = f"{G}/evidence/mut"
PROBE_SRC = f"{G}/evidence/probe/gate70-r2b-probe.integration.test.ts"
PROBE_DST = f"{R}/{REL}/__tests__/gate70-r2b-probe.integration.test.ts"
Q = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g70/_quarantine_2026-11-01"
os.makedirs(OUT, exist_ok=True); os.makedirs(Q, exist_ok=True)

JOBS = [
    ("probe70", "integ", "src/__tests__/gate70-r2b-probe"),
    ("w_r2a", "integ", "src/__tests__/ks1384-r2a-landed-anchor-and-closed-read"),
    ("w_resolver", "unit", "src/__tests__/ks1384-r2b-resolver"),
    ("w_readers", "unit", "src/__tests__/ks1384-r2b-readers"),
]

RESTORE_NET = ("export function isLandedForThisContent(row: { contentHash?: unknown }, ctx: Pick<InFlightContext, 'documentContentHash'>): boolean {\n",
               "export function isLandedForThisContent(row: { contentHash?: unknown; network?: unknown }, ctx: Pick<InFlightContext, 'documentContentHash' | 'network'>): boolean {\n"
               "  const rn = typeof row.network === 'string' && row.network.trim() ? row.network.trim().toLowerCase() : null;\n"
               "  const cn = typeof ctx.network === 'string' && ctx.network.trim() ? ctx.network.trim().toLowerCase() : null;\n"
               "  if (rn !== null && cn !== null && rn !== cn) return false;\n")
M = [
 ("G70-M1 the network leg restored (R2a's rule)", [(INF_F, RESTORE_NET[0], RESTORE_NET[1])]),
 ("G70-M2 G65-F1's restore dropped (both copies)", [(REPO_F, "THEN jsonb_build_object('retryClaimMadeBlob', true) ELSE '{}'::jsonb END),",
   "THEN '{}'::jsonb ELSE '{}'::jsonb END),", 2)]),
 ("G70-M3 step 3 not-answered falls through to step 4", [(ROUTE_F, "      if (ownCreate.outcome === 'not-answered') {\n",
   "      if (ownCreate.outcome === 'not-answered' && process.env.G70_NEVER === 'x') {\n")]),
 ("G70-M4 step 3 loose mint guard removed", [(ROUTE_F, "      if ((ownCreate.loose ?? []).length > 0) {\n",
   "      if ((ownCreate.loose ?? []).length > 0 && process.env.G70_NEVER === 'x') {\n")]),
 ("G70-M5 step 3 found branch removed (falls to the loose guard / step 4)", [(ROUTE_F, "      if (ownCreate.outcome === 'found') {\n",
   "      if (ownCreate.outcome === 'found' && process.env.G70_NEVER === 'x') {\n")]),
 ("G70-M6 resolver: own-create found ignored (pre-R2b reading: a failed row fails the document)", [(RES_F, "  if (ans.outcome === 'found') {\n",
   "  if (ans.outcome === 'found' && process.env.G70_NEVER === 'x') {\n")]),
 ("G70-M6b resolver: own-create found answers as if none (compiling form of M6)", [(RES_F,
   "    return { write: 'confirmed', tx: ans.tx, blockNumber: ans.blockNumber ?? null, via: 'own-create', reason: 'own-create found a create-bound transaction' };\n",
   "    return lookupIfNone === 'anchor_failed' ? { write: 'anchor_failed', reason: 'G70-M6b' } : { write: 'none', reason: 'G70-M6b' };\n")]),
]

def sha(b): return hashlib.sha256(b).hexdigest()
def head_bytes(rel): return subprocess.run(["git", "-C", R, "show", f"{HEAD}:{rel}"], capture_output=True, check=True).stdout

def run_job(tag, kind, pat):
    js, log = f"{OUT}/{tag}.json", f"{OUT}/{tag}.log"
    if os.path.exists(js): os.rename(js, js + ".prev")
    p = subprocess.run(["bash", f"{G}/scripts/jest_run.sh", kind, "app", log, pat, "--json", f"--outputFile={js}"], capture_output=True, text=True)
    cells, total = {}, 0
    try:
        d = json.load(open(js)); total = d.get("numTotalTests", 0)
        for f in d["testResults"]:
            for a in f["assertionResults"]: cells[a["fullName"]] = a["status"]
    except Exception:
        cells = {}
    return p.returncode, total, cells

def restore_all():
    for rel in PRODUCT:
        data = head_bytes(rel); open(f"{R}/{rel}", "wb").write(data)
        assert sha(open(f"{R}/{rel}", "rb").read()) == sha(data), f"restore failed {rel}"

assert subprocess.run(["git", "-C", R, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == R
for rel in PRODUCT:
    assert sha(open(f"{R}/{rel}", "rb").read()) == sha(head_bytes(rel)), f"not at head before start: {rel}"
assert not os.path.exists(PROBE_DST), "probe already placed"
shutil.copy(PROBE_SRC, PROBE_DST)
print(json.dumps({"probe70_sha256": sha(open(PROBE_DST, "rb").read())}), flush=True)
try:
    only = sys.argv[1:]
    bfile = f"{OUT}/baseline.json"
    baseline = json.load(open(bfile)) if os.path.exists(bfile) else {}
    for name, kind, pat in JOBS:
        if name in baseline: continue
        rc, total, cells = run_job(f"BASELINE.{name}", kind, pat)
        baseline[name] = cells
        print(json.dumps({"baseline": name, "rc": rc, "total": total, "red": [k for k, v in cells.items() if v != "passed"]}), flush=True)
        json.dump(baseline, open(bfile, "w"), indent=1)
    results = []
    for mname, edits in M:
        mid = mname.split()[0]
        if only and mid not in only: continue
        rec = {"mutant": mname, "jobs": {}}
        try:
            for e in edits:
                rel, old, new = e[0], e[1], e[2]; want = e[3] if len(e) > 3 else 1
                p = f"{R}/{rel}"; src = open(p).read(); n = src.count(old)
                assert n == want, f"{mname}: anchor count {n} (want {want}) in {rel}"
                open(p, "w").write(src.replace(old, new))
                assert new in open(p).read() and sha(open(p, "rb").read()) != sha(head_bytes(rel)), f"{mname}: mutation did not land"
            rec["landed"] = True
            for name, kind, pat in JOBS:
                rc, total, cells = run_job(f"{mid}.{name}", kind, pat)
                newly_red = [k for k, v in cells.items() if v != "passed" and baseline[name].get(k) == "passed"]
                rec["jobs"][name] = {"rc": rc, "total": total, "invalid": total == 0, "killed_by": newly_red}
            valid = [j for j in rec["jobs"].values() if not j["invalid"]]
            rec["killed"] = any(j["killed_by"] for j in valid)
        finally:
            restore_all()
        rec["restored_sha256_ok"] = True
        results.append(rec)
        print(json.dumps(rec), flush=True)
        json.dump(results, open(f"{OUT}/own_mutants{'_' + '_'.join(only) if only else ''}.json", "w"), indent=1)
finally:
    shutil.move(PROBE_DST, f"{Q}/{time.strftime('%H%M%S')}_mut_gate70-r2b-probe.integration.test.ts")
    print(json.dumps({"probe_quarantined": True}), flush=True)
