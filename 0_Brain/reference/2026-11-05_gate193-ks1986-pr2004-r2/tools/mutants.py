# Gate 192: mutants on the gate's OWN clone. For each: anchor count must be 1; the tampered file must parse (TypeScript
# transpileModule syntactic diagnostics = 0); then (a) the three unit files are run with the service's jest config, and (b) the
# PG15 harness is run (pgrun.sh m<k>); then the file is restored with `git checkout --` and its blob id checked equal to the
# head blob. m1-m5 anchors/replacements are copied byte-for-byte from Seat F 31st's mutants_b_f31.py; m6 and m7 are the gate's.
# usage: python3 -I mutants.py
import json, re, subprocess

W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004"
R = W + "/repo"
REL = "Blockchain/Dev/services/originate/src/routes/verification.ts"
F = R + "/" + REL
SVC = R + "/Blockchain/Dev/services/originate"
JEST = R + "/Blockchain/Dev/node_modules/.bin/jest"
TS = R + "/Blockchain/Dev/node_modules/typescript"
TESTS = ["src/__tests__/ks1986-v1-original-across-tenants.test.ts",
         "src/__tests__/ks1561-g188-f1-original-outside-the-fetched-row-set.test.ts",
         "src/__tests__/ks1561-verify-original-registrant-certifier.test.ts"]
ENV = {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": W + "/home", "TMPDIR": W + "/tmp"}

M = [
    ("m1", "restore tenant-local-first: the foreign originals are read but left out of the judgment",
     "    ? bothEligible(certificationEligibility(localRows), certificationEligibility([...localRows, ...foreign.rows]))\n",
     "    ? bothEligible(certificationEligibility(localRows), certificationEligibility([...localRows]))\n"),
    ("m2", "drop the scrub: the foreign original carries no tenant marker",
     "        out.push({ ...row, _tenantId: t.tenant_id, _tenantSlug: t.tenant_slug });\n",
     "        out.push({ ...row, tenant_id: null, _tenantSlug: t.tenant_slug });\n"),
    ("m3", "take each foreign tenant's rows as a LIMIT-ed row-set fetch instead of its originals read",
     "queryWithTenantGuc(mgr.getPool(t.tenant_id), ORIGINAL_ROWS_POOL_SQL, params)",
     "queryWithTenantGuc(mgr.getPool(t.tenant_id), `SELECT d.* FROM documents d WHERE d.content_hash = $1 OR d.content_hash = $2 OR d.content_hash = $3 ORDER BY d.certified_at DESC NULLS LAST LIMIT ${VERIFY_ROWSET_LIMIT}`, params)"),
    ("m4", "dedupe the caller's own rows by object identity instead of row id",
     "        if (id !== null && local.has(id)) continue;\n",
     "        if (id !== null && local.has(id) && (localRows || []).includes(row)) continue;\n"),
    ("m5", "swallow the lookup failure: judge as if no other tenant held the bytes",
     "    return { ok: false };\n  }\n}",
     "    return { ok: true, rows: [] };\n  }\n}"),
    ("m6", "GATE: drop D-B3 on the selected foreign row (keep issuerId, so certifierOrganizationId is the foreign issuer's)",
     "      certification_metadata: { ...certMeta, issuerId: null }, // D-B3",
     "      certification_metadata: { ...certMeta }, // D-B3"),
    ("m7", "GATE: present the foreign original's certification under the LOCAL rule only (selectVerifiableRow without crossRule)",
     "  const selected = selectVerifiableRow(originals, crossRule);\n",
     "  const selected = selectVerifiableRow(originals);\n"),
]

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)

head_blob = sh(["git", "-C", R, "rev-parse", "577f668f:" + REL]).stdout.strip()

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
    tserr = txt.count("error TS") + txt.count("Test suite failed to run")
    exp = txt.count("Expected") + txt.count("Received")
    return {"rc": r.returncode, "red": failed, "green": passed, "total": total, "tsErrors": tserr, "expectedReceivedMarkers": exp}

rows = []
print("head clean unit:", json.dumps(unit("head")))
for name, what, anchor, repl in M:
    src = open(F).read()
    n = src.count(anchor)
    row = {"mutant": name, "what": what, "anchor_count": n}
    if n != 1:
        row["result"] = "INVALID"; rows.append(row); print(json.dumps(row)); continue
    row["line"] = src[: src.index(anchor)].count("\n") + 1
    new = src.replace(anchor, repl)
    if not parses(new):
        row["result"] = "INVALID (parse)"; rows.append(row); print(json.dumps(row)); continue
    open(F, "w").write(new)
    try:
        row["unit"] = unit(name)
        subprocess.run(["bash", W + "/tools/pgrun.sh", name], env=ENV)
    finally:
        sh(["git", "-C", R, "checkout", "--", REL])
        row["restored_blob_equal"] = sh(["git", "-C", R, "hash-object", F]).stdout.strip() == head_blob
    rows.append(row); print(json.dumps(row))
json.dump(rows, open(W + "/runs/mutants.json", "w"), indent=1)
print("final blob equal head:", sh(["git", "-C", R, "hash-object", F]).stdout.strip() == head_blob)
