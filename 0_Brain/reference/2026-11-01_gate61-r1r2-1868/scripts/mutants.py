#!/usr/bin/env python3
"""Gate 61 own mutants on #1868 round 2 (a46c251e). Each mutant = list of (file, old, new) edits, every `old` asserted
unique (count == 1). Runs W's real-Postgres file, W's unit file and the gate 61 probe with --json, scores PER CELL
against the unmutated baseline (a mutant is KILLED when a cell green at baseline goes red; INVALID when a file
collects 0 tests, i.e. a compile failure), restores from `git show <head>:<file>` and verifies sha256."""
import subprocess, sys, os, json, hashlib

G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate61-r1r2-1868"
R = f"{G}/repo"
HEAD = "a46c251e1419d48bb8a50519e7ee0e306ad2fbe1"
REL = "Blockchain/Dev/services/originate/src"
REPO_F = f"{REL}/repositories/documentRepo.ts"
ROUTE_F = f"{REL}/routes/documents.ts"
INF_F = f"{REL}/services/reanchorInFlight.ts"
OUT = f"{G}/evidence/mut"
os.makedirs(OUT, exist_ok=True)

JOBS = [
    ("w_integ", "integ", "src/__tests__/ks1384-r1r2-stale-claimant"),
    ("w_unit", "unit", "src/__tests__/ks1384-r1-retry-route"),
    ("probe", "integ", "src/__tests__/gate61-r1r2-probe"),
]
BL = "COALESCE(NULLIF(certification_metadata->'blockchain', 'null'::jsonb), NULLIF(metadata->'blockchain', 'null'::jsonb))"
CONFIRM_BLOCK = """      const stillMine = await confirmReanchorClaim(id, tenantId, claimToken, undefined, db);
      if (stillMine !== 1) {
        await release('the claim was no longer this call\\'s, or its lease had lapsed, at the re-check before the POST');
        return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'A re-anchor for this document is already in progress, or it is anchored' } });
      }
"""
M = [
 ("G61-M1 (=MR3) confirm: token conjunct dropped", [(REPO_F,
   f"      AND {BL}->>'retryClaim' = ${{token}}::text\n      AND ({BL}->>'retryClaimedAt')::timestamptz >= ",
   f"      AND ${{token}}::text IS NOT NULL\n      AND ({BL}->>'retryClaimedAt')::timestamptz >= ")]),
 ("G61-M2 confirm: lease conjunct neutralised (lease effectively 100 years)", [(REPO_F,
   ")::timestamptz >= ${staleBefore}::timestamptz",
   ")::timestamptz >= (${staleBefore}::timestamptz - interval '100 years')")]),
 ("G61-M3 confirm: lease boundary doubled (20 min)", [(REPO_F,
   "const staleBefore = new Date(now.getTime() - REANCHOR_CLAIM_TTL_MS).toISOString();\n  return (db || prisma).$executeRaw`\n    UPDATE documents SET\n      metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('blockchain',\n",
   "const staleBefore = new Date(now.getTime() - 2 * REANCHOR_CLAIM_TTL_MS).toISOString();\n  return (db || prisma).$executeRaw`\n    UPDATE documents SET\n      metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('blockchain',\n")]),
 ("G61-M4 confirm: lease NOT renewed (both copies keep the old retryClaimedAt)", [
   (REPO_F,
    f"      metadata = COALESCE(metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', ${{refreshedAt}}::text)),",
    f"      metadata = COALESCE(metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', COALESCE({BL}->>'retryClaimedAt', ${{refreshedAt}}::text))),"),
   (REPO_F,
    f"      certification_metadata = COALESCE(certification_metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', ${{refreshedAt}}::text)),",
    f"      certification_metadata = COALESCE(certification_metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', COALESCE({BL}->>'retryClaimedAt', ${{refreshedAt}}::text))),"),
 ]),
 ("G61-M5 confirm: lease renewed in metadata only, not the authoritative certification_metadata copy", [
   (REPO_F,
    f"      certification_metadata = COALESCE(certification_metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', ${{refreshedAt}}::text)),",
    f"      certification_metadata = COALESCE(certification_metadata, '{{}}'::jsonb) || jsonb_build_object('blockchain',\n        {BL}\n          || jsonb_build_object('retryClaimedAt', COALESCE({BL}->>'retryClaimedAt', ${{refreshedAt}}::text))),"),
 ]),
 ("G61-M6 route: re-check result ignored", [(ROUTE_F,
   "      if (stillMine !== 1) {\n", "      if (stillMine !== 1 && stillMine === -1) {\n")]),
 ("G61-M7 route: re-check moved BEFORE the in-flight read", [
   (ROUTE_F, CONFIRM_BLOCK, ""),
   (ROUTE_F, "      const anchoringBaseForRead = process.env.ANCHORING_SERVICE_URL",
    CONFIRM_BLOCK + "      const anchoringBaseForRead = process.env.ANCHORING_SERVICE_URL"),
 ]),
 ("G61-M8 route: a timed-out POST releases the claim", [(ROUTE_F,
   "          res.set('Retry-After', String(Math.round(REANCHOR_CLAIM_TTL_MS / 1000)));\n",
   "          await release('timeout');\n          res.set('Retry-After', String(Math.round(REANCHOR_CLAIM_TTL_MS / 1000)));\n")]),
 ("G61-M9 route: a timed-out POST goes down R1's failure path", [(ROUTE_F,
   "        if (isTimeoutError(anchorErr)) {\n", "        if (isTimeoutError(anchorErr) && process.env.G61_NEVER === 'x') {\n")]),
 ("G61-M10 route: the POST's signal removed", [(ROUTE_F,
   "          signal: AbortSignal.timeout(REANCHOR_POST_TIMEOUT_MS),\n        });\n", "        });\n")]),
 ("G61-M11 route: timed-out POST answers Retry-After 60 (inside the lease)", [(ROUTE_F,
   "String(Math.round(REANCHOR_CLAIM_TTL_MS / 1000))", "String(Math.round(REANCHOR_CLAIM_TTL_MS / 10000))")]),
 ("G61-M12 route: re-check failure does not release", [(ROUTE_F,
   "        await release('the claim was no longer this call\\'s, or its lease had lapsed, at the re-check before the POST');\n", "")]),
 ("G61-M13 in-flight read: signal removed", [(INF_F,
   "      signal: AbortSignal.timeout(REANCHOR_READ_TIMEOUT_MS),\n    });\n", "    });\n")]),
 ("G61-M14 isTimeoutError: TimeoutError not recognised", [(INF_F,
   "return name === 'TimeoutError' || name === 'AbortError';", "return name === 'AbortError';")]),
 ("G61-M15 POST timeout 11 min (longer than the lease)", [(INF_F,
   "export const REANCHOR_POST_TIMEOUT_MS = 10_000;", "export const REANCHOR_POST_TIMEOUT_MS = 660_000;")]),
 ("G61-M16 confirm: tenant conjunct dropped", [(REPO_F,
   f"      AND tenant_id = ${{tenantId}}::uuid\n      AND {BL}->>'retryClaim' = ${{token}}::text\n      AND ({BL}->>'retryClaimedAt')::timestamptz >= ",
   f"      AND ${{tenantId}}::text IS NOT NULL\n      AND {BL}->>'retryClaim' = ${{token}}::text\n      AND ({BL}->>'retryClaimedAt')::timestamptz >= ")]),
]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def head_sha(rel):
    return hashlib.sha256(subprocess.run(["git", "-C", R, "show", f"{HEAD}:{rel}"], capture_output=True, check=True).stdout).hexdigest()

def run_job(tag, kind, pat):
    js = f"{OUT}/{tag}.json"
    log = f"{OUT}/{tag}.log"
    if os.path.exists(js):
        os.remove(js)
    p = subprocess.run(["bash", f"{G}/scripts/jest_run.sh", kind, "app", log, pat, "--json", f"--outputFile={js}"], capture_output=True, text=True)
    cells = {}
    total = 0
    try:
        d = json.load(open(js))
        total = d.get("numTotalTests", 0)
        for f in d["testResults"]:
            for a in f["assertionResults"]:
                cells[a["title"][:60]] = a["status"]
    except Exception as e:  # no json: treat as no tests collected
        cells = {}
    return p.returncode, total, cells

def restore_all():
    for rel in (REPO_F, ROUTE_F, INF_F):
        data = subprocess.run(["git", "-C", R, "show", f"{HEAD}:{rel}"], capture_output=True, check=True).stdout
        open(f"{R}/{rel}", "wb").write(data)
        assert sha(f"{R}/{rel}") == head_sha(rel), f"restore failed {rel}"

assert subprocess.run(["git", "-C", R, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == R
for rel in (REPO_F, ROUTE_F, INF_F):
    assert sha(f"{R}/{rel}") == head_sha(rel), f"not at head before start: {rel}"

only = sys.argv[1:]  # optional mutant-id filter
baseline = {}
bfile = f"{OUT}/baseline.json"
if os.path.exists(bfile):
    baseline = json.load(open(bfile))
else:
    for name, kind, pat in JOBS:
        rc, total, cells = run_job(f"BASELINE.{name}", kind, pat)
        baseline[name] = cells
        print(json.dumps({"baseline": name, "rc": rc, "total": total, "failed": [k for k, v in cells.items() if v != "passed"]}), flush=True)
    json.dump(baseline, open(bfile, "w"), indent=1)

results = []
for mname, edits in M:
    mid = mname.split()[0]
    if only and mid not in only:
        continue
    try:
        for rel, old, new in edits:
            p = f"{R}/{rel}"
            src = open(p).read()
            n = src.count(old)
            assert n == 1, f"{mname}: anchor count {n} in {rel}"
            open(p, "w").write(src.replace(old, new))
        rec = {"mutant": mname, "jobs": {}}
        for name, kind, pat in JOBS:
            rc, total, cells = run_job(f"{mid}.{name}", kind, pat)
            newly_red = [k for k, v in cells.items() if v != "passed" and baseline[name].get(k) == "passed"]
            rec["jobs"][name] = {"rc": rc, "total": total, "invalid": total == 0, "killed_by": newly_red}
        valid = [j for j in rec["jobs"].values() if not j["invalid"]]
        rec["invalid_everywhere"] = len(valid) == 0
        rec["killed"] = any(j["killed_by"] for j in valid)
    finally:
        restore_all()
    rec["restored_sha256_ok"] = True
    results.append(rec)
    print(json.dumps(rec), flush=True)
    json.dump(results, open(f"{OUT}/own_mutants{'_' + '_'.join(only) if only else ''}.json", "w"), indent=1)
