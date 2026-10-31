#!/usr/bin/env python3
"""Gate 65 own mutants on #1868 round 3 (7ed460cc), adapted from gate 61's mutants.py. Each mutant = list of
(file, old, new[, count]) edits, every `old` asserted to occur exactly `count` times (default 1). Runs W's two
real-Postgres files, W's two unit files and the gate 65 probe with --json, scores PER CELL against the unmutated
baseline (KILLED when a cell green at baseline goes red; INVALID when a file collects 0 tests, i.e. a compile failure),
restores from `git show <head>:<file>` and verifies sha256 after every mutant."""
import subprocess, sys, os, json, hashlib

G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate65-r1r3-1868"
R = f"{G}/repo"
HEAD = "7ed460cc4258d7aee16f9f65ca150d50b22ed453"
REL = "Blockchain/Dev/services/originate/src"
REPO_F = f"{REL}/repositories/documentRepo.ts"
ROUTE_F = f"{REL}/routes/documents.ts"
INF_F = f"{REL}/services/reanchorInFlight.ts"
OUT = f"{G}/evidence/mut"
os.makedirs(OUT, exist_ok=True)

JOBS = [
    ("w_r1r3", "integ", "src/__tests__/ks1384-r1r3-unknown-outcome"),
    ("w_r1r2", "integ", "src/__tests__/ks1384-r1r2-stale-claimant"),
    ("w_unit", "unit", "src/__tests__/ks1384-r1-retry-route"),
    ("w_dead", "unit", "src/__tests__/ks1384-r1r3-post-deadlines"),
    ("probe", "integ", "src/__tests__/gate65-r1r3-probe"),
]
BL = "COALESCE(NULLIF(certification_metadata->'blockchain', 'null'::jsonb), NULLIF(metadata->'blockchain', 'null'::jsonb))"
CONF_HEAD = f"      AND status NOT IN ('revoked', 'deleted')\n      AND {BL}->>'status' IS DISTINCT FROM 'confirmed'\n      AND {BL}->>'retryClaim' = ${{token}}::text\n      AND ({BL}->>'retryClaimedAt')::timestamptz >= "
MARK = "const marked = await markReanchorPostUnknown(id, tenantId, claimToken, undefined, db);"
M = [
 ("G65-M1 route: marker NOT written on the header-timeout ('unknown') branch", [(ROUTE_F, MARK,
   "const marked = posted.kind === 'unknown' ? 0 : await markReanchorPostUnknown(id, tenantId, claimToken, undefined, db);")]),
 ("G65-M2 route: marker NOT written on the 'accepted-body-lost' branch", [(ROUTE_F, MARK,
   "const marked = posted.kind === 'accepted-body-lost' ? 0 : await markReanchorPostUnknown(id, tenantId, claimToken, undefined, db);")]),
 ("G65-M3 route: marker NOT written on the unreadable-2xx branch", [(ROUTE_F, MARK,
   "const marked = posted.kind === 'answered' ? 0 : await markReanchorPostUnknown(id, tenantId, claimToken, undefined, db);")]),
 ("G65-M4 route: marker NOT written into the m7 (2xx JSON, no id) outcome", [(ROUTE_F,
   "...(adId === undefined ? { retryPostUnknownAt: now, retryPostUnknownToken: claimToken } : {}),",
   "...(adId === undefined && process.env.G65_NEVER === 'x' ? { retryPostUnknownAt: now, retryPostUnknownToken: claimToken } : {}),")]),
 ("G65-M5 route: the claimant ignores the marker (postOutcomeUnknown always false)", [(ROUTE_F,
   "postOutcomeUnknown: postUnknownAt !== null,", "postOutcomeUnknown: false && postUnknownAt !== null,")]),
 ("G65-M6 decideInFlight: with the marker, a CONFIRMED row reads absent again (G58-F2 hole reopened)", [(INF_F,
   "if (ctx.postOutcomeUnknown && anchors.length > 0) {",
   "if (ctx.postOutcomeUnknown && anchors.length > 0 && (anchors as Array<{ status?: unknown }>).every((x) => x?.status !== 'confirmed')) {")]),
 ("G65-M7 release: clears the marker too (cleared too early)", [(REPO_F,
   "- 'retryClaim' - 'retryClaimedAt' - 'retryClaimMadeBlob')",
   "- 'retryClaim' - 'retryClaimedAt' - 'retryClaimMadeBlob' - 'retryPostUnknownAt' - 'retryPostUnknownToken')", 2)]),
 ("G65-M8 re-check: marker-equality conjunct dropped", [(REPO_F,
   f"      AND {BL}->>'retryPostUnknownAt' IS NOT DISTINCT FROM ${{expectPostUnknownAt}}::text\n",
   f"      AND (${{expectPostUnknownAt}}::text IS NULL OR ${{expectPostUnknownAt}}::text IS NOT NULL)\n")]),
 ("G65-M9a postReanchor: header timer not cleared (one 10 s deadline over headers+body, round 2's shape)", [(INF_F,
   "    clearTimeout(headerTimer);\n", "    void headerTimer;\n")]),
 ("G65-M9b route: a received 2xx whose body is lost goes down R1's failure path (202 headers discarded)", [(ROUTE_F,
   "if (posted.kind === 'unknown' || posted.kind === 'accepted-body-lost' || unreadable2xx) {",
   "if (posted.kind === 'unknown' || unreadable2xx) {")]),
 ("G65-M10 re-check: revoked/deleted status guard dropped (G61-F3)", [(REPO_F, CONF_HEAD,
   CONF_HEAD.replace("      AND status NOT IN ('revoked', 'deleted')\n", ""))]),
 ("G65-M11 re-check: confirmed-blob guard dropped", [(REPO_F, CONF_HEAD,
   CONF_HEAD.replace(f"      AND {BL}->>'status' IS DISTINCT FROM 'confirmed'\n", ""))]),
 ("G65-M12 claim: m5 edge widened (a marked blob is claimable even under a LIVE claim)", [(REPO_F,
   f"        OR ({BL}->>'retryClaimedAt')::timestamptz < ${{staleBefore}}::timestamptz\n      )\n",
   f"        OR ({BL}->>'retryClaimedAt')::timestamptz < ${{staleBefore}}::timestamptz\n        OR {BL}->>'retryPostUnknownAt' IS NOT NULL\n      )\n")]),
 ("G65-M13 mark: retryClaimMadeBlob NOT dropped", [(REPO_F,
   "'{}'::jsonb) - 'retryClaimMadeBlob')", "'{}'::jsonb))", 2)]),
 ("G65-M14 body deadline 10 min (past the lease)", [(INF_F,
   "export const REANCHOR_POST_BODY_TIMEOUT_MS = 10_000;", "export const REANCHOR_POST_BODY_TIMEOUT_MS = 600_000;")]),
 ("G65-M15 re-check does NOT clear the marker", [(REPO_F,
   " - 'retryPostUnknownAt' - 'retryPostUnknownToken')", ")", 2)]),
 ("G65-M16 m5 disjunct removed (a marked claimless pending blob is not claimable)", [(REPO_F,
   f"            OR {BL}->>'retryPostUnknownAt' IS NOT NULL\n          )\n", "          )\n")]),
 ("G65-M17 mark: also guarded on the caller's token", [(REPO_F,
   f"      AND tenant_id = ${{tenantId}}::uuid\n      AND {BL}->>'status' IS DISTINCT FROM 'confirmed'\n  `;\n}}\n\n/**\n * The holder's outcome write",
   f"      AND tenant_id = ${{tenantId}}::uuid\n      AND {BL}->>'status' IS DISTINCT FROM 'confirmed'\n      AND {BL}->>'retryClaim' = ${{token}}::text\n  `;\n}}\n\n/**\n * The holder's outcome write")]),
]

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def head_bytes(rel):
    return subprocess.run(["git", "-C", R, "show", f"{HEAD}:{rel}"], capture_output=True, check=True).stdout

def run_job(tag, kind, pat):
    js = f"{OUT}/{tag}.json"
    log = f"{OUT}/{tag}.log"
    if os.path.exists(js):
        os.remove(js)
    p = subprocess.run(["bash", f"{G}/scripts/jest_run.sh", kind, "app", log, pat, "--json", f"--outputFile={js}"], capture_output=True, text=True)
    cells, total = {}, 0
    try:
        d = json.load(open(js))
        total = d.get("numTotalTests", 0)
        for f in d["testResults"]:
            for a in f["assertionResults"]:
                cells[a["fullName"]] = a["status"]
    except Exception:
        cells = {}
    return p.returncode, total, cells

def restore_all():
    for rel in (REPO_F, ROUTE_F, INF_F):
        data = head_bytes(rel)
        open(f"{R}/{rel}", "wb").write(data)
        assert sha_bytes(open(f"{R}/{rel}", "rb").read()) == sha_bytes(data), f"restore failed {rel}"

assert subprocess.run(["git", "-C", R, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == R
for rel in (REPO_F, ROUTE_F, INF_F):
    assert sha_bytes(open(f"{R}/{rel}", "rb").read()) == sha_bytes(head_bytes(rel)), f"not at head before start: {rel}"

only = sys.argv[1:]
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
for edits_spec in M:
    mname, edits = edits_spec
    mid = mname.split()[0]
    if only and mid not in only:
        continue
    try:
        for e in edits:
            rel, old, new = e[0], e[1], e[2]
            want = e[3] if len(e) > 3 else 1
            p = f"{R}/{rel}"
            src = open(p).read()
            n = src.count(old)
            assert n == want, f"{mname}: anchor count {n} (want {want}) in {rel}"
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
