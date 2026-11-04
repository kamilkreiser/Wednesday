# Gate 193: mutants on the new flag and guard, run on the committed bytes in the gate's OWN clone.
# LINEAGE: gate 192's tools/mutants.py (structure: anchor count 1, transpile parse check, unit files + PG harness, restore + blob check),
# re-keyed to head 4432db22 and the round-2 mutant list (commission question 5). Every anchor must occur exactly once.
# Kill judgement: unit red > 0, OR any PG row (v1 or v2) whose (http, body, chainCalls) differs from the clean head run.
# usage: python3 -I mutants193.py [names...]
import json, re, subprocess, sys

W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2"
R = W + "/repo"
HEADC = "4432db224a5867fdb6afaabf56df08cdf640d067"
REL = "Blockchain/Dev/services/originate/src/routes/verification.ts"
F = R + "/" + REL
SVC = R + "/Blockchain/Dev/services/originate"
JEST = R + "/Blockchain/Dev/node_modules/.bin/jest"
TS = R + "/Blockchain/Dev/node_modules/typescript"
TESTS = ["src/__tests__/ks1986-v1-original-across-tenants.test.ts",
         "src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts",
         "src/__tests__/ks1561-verify-original-registrant-certifier.test.ts"]
ENV = {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": W + "/home", "TMPDIR": W + "/tmp"}

SET = "  if (!foreign.ok) return { rows: [], skipCrossTenantLookup: true, crossTenantReadFailed: true };\n"
G_VF = "\n    if (rows.length === 0 && !crossTenantReadFailed) {\n"
G_V = "\n          if (rows.length === 0 && !crossTenantReadFailed) {\n"
HDR = "export async function judgeAcrossTenants(localRows: any[], hash: string, hashNorm: string): Promise<V1CrossTenantJudgment> {\n"
STAGE = [
    ("  try {\n    const reg = await mgr.getPlatformPool().query(", "  let g193Stage = 'registry';\n  try {\n    const reg = await mgr.getPlatformPool().query("),
    ("    const local = new Set((localRows || []).map(", "    g193Stage = 'tenant';\n    const local = new Set((localRows || []).map("),
    ("    return { ok: false };\n  }\n}", "    return { ok: false, g193Stage } as any;\n  }\n}"),
]
M = [
    ("m1", "flag never set (read-failure return sets false)", [(SET, SET.replace("crossTenantReadFailed: true", "crossTenantReadFailed: false"))]),
    ("m2", "guard reverts to rows.length === 0 in verify-file only", [(G_VF, "\n    if (rows.length === 0) {\n")]),
    ("m3", "guard reverts to rows.length === 0 in /verify only", [(G_V, "\n          if (rows.length === 0) {\n")]),
    ("m2v", "valid form of m2 (flag still read, guard behaves as rows.length === 0), verify-file only",
        [(G_VF, "\n    if (rows.length === 0 && (crossTenantReadFailed || !crossTenantReadFailed)) {\n")]),
    ("m3v", "valid form of m3 (flag still read, guard behaves as rows.length === 0), /verify only",
        [(G_V, "\n          if (rows.length === 0 && (crossTenantReadFailed || !crossTenantReadFailed)) {\n")]),
    ("m4", "flag true on EVERY judgeAcrossTenants return (wrapper)", [(HDR,
        "export async function judgeAcrossTenants(localRows: any[], hash: string, hashNorm: string): Promise<V1CrossTenantJudgment> {\n"
        "  const g193 = await g193JudgeInner(localRows, hash, hashNorm);\n  return { ...g193, crossTenantReadFailed: true };\n}\n"
        "async function g193JudgeInner(localRows: any[], hash: string, hashNorm: string): Promise<V1CrossTenantJudgment> {\n")]),
    ("m5a", "flag set on the REGISTRY-read failure only (tenant-read failures unflagged)",
        STAGE + [(SET, SET.replace("crossTenantReadFailed: true", "crossTenantReadFailed: (foreign as any).g193Stage === 'registry'"))]),
    ("m5b", "flag set on the TENANT-read failure only (registry-read failure unflagged)",
        STAGE + [(SET, SET.replace("crossTenantReadFailed: true", "crossTenantReadFailed: (foreign as any).g193Stage === 'tenant'"))]),
    ("m6", "guard inverted as written in the commission: rows.length === 0 || crossTenantReadFailed (both callers)",
        [(G_VF, "\n    if (rows.length === 0 || crossTenantReadFailed) {\n"), (G_V, "\n          if (rows.length === 0 || crossTenantReadFailed) {\n")]),
    ("m6b", "GATE: guard negation dropped: rows.length === 0 && crossTenantReadFailed (both callers)",
        [(G_VF, "\n    if (rows.length === 0 && crossTenantReadFailed) {\n"), (G_V, "\n          if (rows.length === 0 && crossTenantReadFailed) {\n")]),
    ("m7a", "not-found body altered, verify-file", [("error: 'This document is NOT in the Secuura registry.", "error: 'G193 MUTANT not found.")]),
    ("m7b", "not-found body altered, /verify", [("error: 'This document hash is not registered.", "error: 'G193 MUTANT not registered.")]),
]

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)

head_blob = sh(["git", "-C", R, "rev-parse", HEADC + ":" + REL]).stdout.strip()

def parses(src):
    js = ("const ts=require(%s);const s=require('fs').readFileSync(0,'utf8');"
          "const o=ts.transpileModule(s,{reportDiagnostics:true,compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}});"
          "console.log((o.diagnostics||[]).length)") % json.dumps(TS)
    r = subprocess.run(["node", "-e", js], input=src, capture_output=True, text=True, env=ENV, cwd=W + "/cwd")
    return r.stdout.strip() == "0"

def unit(tag):
    out = W + f"/runs/unit_{tag}.out"
    r = subprocess.run([JEST, "-c", SVC + "/jest.config.js", "--rootDir", SVC, "--cacheDirectory", W + "/tmp/jestcache", "--runTestsByPath", *[SVC + "/" + t for t in TESTS]],
                       cwd=W + "/cwd", env=ENV, stdout=open(out, "w"), stderr=subprocess.STDOUT)
    txt = open(out).read()
    m = re.search(r"Tests:\s+(?:(\d+) failed, )?(?:(\d+) passed, )?(\d+) total", txt)
    failed = int(m.group(1) or 0) if m else -1
    passed = int(m.group(2) or 0) if m else -1
    total = int(m.group(3)) if m else -1
    return {"rc": r.returncode, "red": failed, "green": passed, "total": total,
            "errorTS": len(re.findall(r"error TS|TS[0-9]{4}", txt)), "TypeError": txt.count("TypeError"),
            "suiteFailedToRun": txt.count("Test suite failed to run")}

def load(p):
    return {(r["cell"], r["path"]): r for r in map(json.loads, open(p))}

def pgdiff(tag):
    h, m = load(W + "/runs/pg_head.jsonl"), load(W + f"/runs/pg_{tag}.jsonl")
    diff = []
    for k in h:
        a, b = h[k], m.get(k)
        if b is None or (a["http"], a["body"], a["chainCalls"]) != (b["http"], b["body"], b["chainCalls"]):
            diff.append(f"{k[0]} {k[1]}")
    return {"rows": len(h), "rowsInMutant": len(m), "differ": len(diff), "cells": diff}

names = sys.argv[1:]
rows = []
if not names:
    print("head clean unit:", json.dumps(unit("head")))
for name, what, edits in M:
    if names and name not in names: continue
    src = open(F).read()
    row = {"mutant": name, "what": what, "anchor_counts": [src.count(a) for a, _ in edits]}
    if any(c != 1 for c in row["anchor_counts"]):
        row["result"] = "INVALID (anchor)"; rows.append(row); print(json.dumps(row)); continue
    new = src
    for a, b in edits:
        new = new.replace(a, b)
    if not parses(new):
        row["result"] = "INVALID (parse)"; rows.append(row); print(json.dumps(row)); continue
    open(F, "w").write(new)
    try:
        row["unit"] = unit(name)
        subprocess.run(["bash", W + "/tools/pgrun.sh", "m_" + name], env=ENV)
        row["pg"] = pgdiff("m_" + name)
    finally:
        sh(["git", "-C", R, "checkout", "--", REL])
        row["restored_blob_equal"] = sh(["git", "-C", R, "hash-object", F]).stdout.strip() == head_blob
    row["result"] = "KILLED" if (row["unit"]["red"] > 0 or row["pg"]["differ"] > 0) else "SURVIVED"
    rows.append(row); print(json.dumps(row))
json.dump(rows, open(W + "/runs/mutants193" + ("_" + "_".join(names) if names else "") + ".json", "w"), indent=1)
print("final blob equal head:", sh(["git", "-C", R, "hash-object", F]).stdout.strip() == head_blob)
