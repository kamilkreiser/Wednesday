#!/usr/bin/env python3
"""Gate 68 own mutants on #1874 R2a (31d146678), adapted from gate 65's mutants.py. Each mutant = list of
(file, old, new[, count]) edits, every `old` asserted to occur exactly `count` times (default 1), and the mutated text
asserted PRESENT on disk before any job runs (a mutant that did not land is reported, never scored). Jobs run with --json,
scored PER CELL against the unmutated baseline (KILLED when a cell green at baseline goes red; INVALID when a file collects
0 tests). Every product file is restored from `git show <head>:<file>` and its sha256 checked after every mutant."""
import subprocess, sys, os, json, hashlib

G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874"
R = f"{G}/repo"
HEAD = "31d1466788bea96f6175b595c8fb3078229668be"
REL = "Blockchain/Dev/services/originate/src"
ROUTE_F = f"{REL}/routes/documents.ts"
INF_F = f"{REL}/services/reanchorInFlight.ts"
OUT = f"{G}/evidence/mut"
os.makedirs(OUT, exist_ok=True)

JOBS = [
    ("w_r2a", "integ", "src/__tests__/ks1384-r2a-landed-anchor-and-closed-read"),
    ("w_r1r3", "integ", "src/__tests__/ks1384-r1r3-unknown-outcome"),
    ("w_infl", "unit", "src/__tests__/ks1384-r1-in-flight-decision"),
    ("w_route", "unit", "src/__tests__/ks1384-r1-retry-route"),
    ("probe68", "integ", "src/__tests__/gate68-r2a-probe"),
]
PROBE65 = ("probe65", "integ", "src/__tests__/gate65-r1r3-probe")

LANDED = ("  for (const a of anchors as Array<{ id?: unknown; status?: unknown; contentHash?: unknown; network?: unknown }>) {\n"
          "    if (a?.status === 'confirmed' && isLandedForThisContent(a, ctx)) {\n"
          "      return { kind: 'anchored', anchorId: String(a.id ?? ''), reason: 'a confirmed anchor for this content on this network' };\n"
          "    }\n  }\n")
MARKER = ("  if (ctx.postOutcomeUnknown && anchors.length > 0) {\n"
          "    const a = anchors[0] as { id?: unknown; status?: unknown };\n"
          "    return { kind: 'maybe-landed', anchorId: String(a?.id ?? ''), status: typeof a?.status === 'string' ? a.status : '' };\n"
          "  }\n")
INFL = ("  for (const a of anchors as Array<{ id?: unknown; status?: unknown }>) {\n"
        "    if (typeof a?.status === 'string' && IN_FLIGHT_STATUSES.includes(a.status)) {\n"
        "      return { kind: 'in-flight', anchorId: String(a.id ?? ''), status: a.status };\n"
        "    }\n  }\n")
SRC = open(f"{R}/{INF_F}").read()
i_l, i_m, i_f = SRC.find(LANDED), SRC.find(MARKER), SRC.find(INFL)
assert -1 not in (i_l, i_m, i_f), (i_l, i_m, i_f)
BETWEEN_LM = SRC[i_l + len(LANDED):i_m]   # the comment block between the landed loop and the marker rule
BETWEEN_FL = SRC[i_f + len(INFL):i_l]     # the comment line between the in-flight loop and the landed loop

M = [
 ("G68-M1 (W's order mutant) marker rule BEFORE the landed check", [(INF_F, LANDED + BETWEEN_LM + MARKER, MARKER + BETWEEN_LM + LANDED)], False),
 ("G68-M2 merge resolution in documents.ts loses round 3's postOutcomeUnknown", [(ROUTE_F,
   "postOutcomeUnknown: postUnknownAt !== null,", "postOutcomeUnknown: false && postUnknownAt !== null,")], True),
 ("G68-M3 merge resolution in documents.ts loses R2a's hash and network (both undefined)", [(ROUTE_F,
   "        documentContentHash: document.contentHash,\n        network: process.env.CARDANO_NETWORK || 'preprod',\n",
   "        documentContentHash: undefined,\n        network: undefined,\n")], False),
 ("G68-M4 merge resolution in documents.ts drops R2a's 'anchored' branch (falls through to the re-check and POST)", [(ROUTE_F,
   "      if (inFlight.kind === 'anchored') {", "      if (inFlight.kind === 'anchored' && process.env.G68_NEVER === 'x') {")], True),
 ("G68-M5 landed check BEFORE the in-flight loop", [(INF_F, INFL + BETWEEN_FL + LANDED, LANDED + BETWEEN_FL + INFL)], False),
 ("G68-M6 network compared case-sensitively", [(INF_F, "const n = v.trim().toLowerCase();", "const n = v.trim();")], False),
 ("G68-M7 document hash 'sha256:' prefix not stripped", [(INF_F,
   "const h = v.trim().replace(/^sha256:/i, '').toLowerCase();", "const h = v.trim().toLowerCase();")], False),
 ("G68-M8 landed check accepts any non-in-flight status (a FAILED row reads anchored)", [(INF_F,
   "if (a?.status === 'confirmed' && isLandedForThisContent(a, ctx)) {", "if (typeof a?.status === 'string' && isLandedForThisContent(a, ctx)) {")], False),
 ("G68-M9 marker rule takes only a non-confirmed row (merge kept the pre-round-3 confirmed-absent reading under the marker)", [(INF_F,
   "  if (ctx.postOutcomeUnknown && anchors.length > 0) {\n",
   "  if (ctx.postOutcomeUnknown && anchors.length > 0 && (anchors as Array<{ status?: unknown }>).every((x) => x?.status !== 'confirmed')) {\n")], False),
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
    for rel in (ROUTE_F, INF_F):
        data = head_bytes(rel); open(f"{R}/{rel}", "wb").write(data)
        assert sha(open(f"{R}/{rel}", "rb").read()) == sha(data), f"restore failed {rel}"

assert subprocess.run(["git", "-C", R, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == R
for rel in (ROUTE_F, INF_F):
    assert sha(open(f"{R}/{rel}", "rb").read()) == sha(head_bytes(rel)), f"not at head before start: {rel}"

only = sys.argv[1:]
bfile = f"{OUT}/baseline.json"
baseline = json.load(open(bfile)) if os.path.exists(bfile) else {}
for name, kind, pat in JOBS + [PROBE65]:
    if name in baseline: continue
    rc, total, cells = run_job(f"BASELINE.{name}", kind, pat)
    baseline[name] = cells
    print(json.dumps({"baseline": name, "rc": rc, "total": total, "red": [k for k, v in cells.items() if v != "passed"]}), flush=True)
    json.dump(baseline, open(bfile, "w"), indent=1)

results = []
for mname, edits, with65 in M:
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
        for name, kind, pat in JOBS + ([PROBE65] if with65 else []):
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
