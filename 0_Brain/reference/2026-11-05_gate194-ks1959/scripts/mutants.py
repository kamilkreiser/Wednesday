# gate 194 mutants against the COMMITTED head bytes. usage: python3 -I mutants.py
# Each mutant: every anchor count == 1 (else INVALID), apply, run the PR's ks1959 file AND the gate's matrix (json reporter),
# restore from `git show <head>:<path>` and check sha256 equal to the committed blob. One clean run at the end.
# Kill: the PR file red (> 0 failing assertions) and/or the gate matrix differing from the head run in any cell (fields below).
import hashlib, json, os, subprocess
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959"
R = W + "/repo"; V = R + "/Blockchain/Dev/services/vc-issuer"
HEAD = "a968818a0038727399663775722017c130d4cb08"
REPO = "Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts"
ROUTE = "Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts"
PR_TEST = "src/__tests__/ks1959-revoke-write-fails-closed.test.ts"
CATCH_THROW = "      throw new CredentialStoreWriteError();\n    }\n    if (typeof rowCount"
MEM = "  // Update memory\n  memoryStore.set(credential.id, revokedCredential);\n\n  // Update DB"
M = [
    # --- the seat's 7 (tools/mutants_k14.py), same anchors and replacements ---
    ("m1-seat swallow (no throw in catch)", [(REPO, CATCH_THROW, "      // m1: swallowed\n    }\n    if (typeof rowCount")]),
    ("m2-seat rowCount check dropped", [(REPO, "    if (typeof rowCount === 'number' && rowCount < 1) {", "    if (false && typeof rowCount === 'number' && rowCount < 1) {")]),
    ("m3-seat fail closed only for a readable value", [(REPO, "      // KS-1959: fail closed. A fresh error with a fixed message, never the thrown value.", "      if (error === 'unreadable thrown value') return revokedCredential;\n      // KS-1959: fail closed. A fresh error with a fixed message, never the thrown value.")]),
    ("m4-seat raw value rethrown", [(REPO, CATCH_THROW, "      throw err;\n    }\n    if (typeof rowCount")]),
    ("m4b-seat rethrown and echoed by the route", [(REPO, CATCH_THROW, "      throw err;\n    }\n    if (typeof rowCount"), (ROUTE, "      if (err instanceof credentialRepo.CredentialStoreWriteError) {\n        throw new AppError(REVOCATION_NOT_SAVED, 503);\n      }", "      throw new AppError(String((err as any)?.message), 503);")]),
    ("m5-seat typed error mapped to 2xx", [(ROUTE, "        throw new AppError(REVOCATION_NOT_SAVED, 503);", "        res.json({ success: true, message: 'Credential revoked successfully', credentialId: id }); return;")]),
    ("m6-seat memory after DB", [(REPO, MEM, "  // Update DB"), (REPO, "  return revokedCredential;\n}", "  memoryStore.set(credential.id, revokedCredential);\n  return revokedCredential;\n}")]),
    # --- the gate's own ---
    ("ma memory write only on DB success (inside the try, after the UPDATE) or no DB", [(REPO, MEM, "  // Update DB"), (REPO, "      rowCount = result?.rowCount;\n", "      rowCount = result?.rowCount;\n      if (!(typeof rowCount === 'number' && rowCount < 1)) memoryStore.set(credential.id, revokedCredential);\n"), (REPO, "  return revokedCredential;\n}", "  if (!isDbAvailable()) memoryStore.set(credential.id, revokedCredential);\n  return revokedCredential;\n}")]),
    ("mb swallow restored (catch returns success)", [(REPO, CATCH_THROW, "      return revokedCredential;\n    }\n    if (typeof rowCount")]),
    ("mc rowCount never read", [(REPO, "      rowCount = result?.rowCount;\n", "      rowCount = undefined && result;\n")]),
    ("md rowCount < 1 -> < 0", [(REPO, "rowCount < 1) {", "rowCount < 0) {")]),
    ("me route maps ANY error to 503", [(ROUTE, "      if (err instanceof credentialRepo.CredentialStoreWriteError) {", "      if (true) {")]),
    ("mf1 route answers err.message instead of the fixed text", [(ROUTE, "        throw new AppError(REVOCATION_NOT_SAVED, 503);", "        throw new AppError((err as Error).message, 503);")]),
    ("mf2 fresh error carries the thrown message, route answers it", [(REPO, CATCH_THROW, "      { const e = new CredentialStoreWriteError(); e.message = String(error); throw e; }\n    }\n    if (typeof rowCount"), (ROUTE, "        throw new AppError(REVOCATION_NOT_SAVED, 503);", "        throw new AppError((err as Error).message, 503);")]),
    ("mg memory rolled back on a failed write (the rejected (b) outcome)", [(REPO, "      logger.warn('DB revoke update failed", "      memoryStore.set(credential.id, credential);\n      logger.warn('DB revoke update failed"), (REPO, "      logger.warn('DB revoke update matched no row", "      memoryStore.set(credential.id, credential);\n      logger.warn('DB revoke update matched no row")]),
    ("mh HEADER CONTROL: thrown message copied to a response header", [(REPO, CATCH_THROW, "      { const e = new CredentialStoreWriteError(); (e as any).g194 = error; throw e; }\n    }\n    if (typeof rowCount"), (ROUTE, "        throw new AppError(REVOCATION_NOT_SAVED, 503);", "        res.setHeader('x-g194-err', String((err as any).g194)); throw new AppError(REVOCATION_NOT_SAVED, 503);")]),
]
FIELDS = ("revokeStatus", "revokeMsg", "updates", "dbRowRevoked", "memRevoked", "status", "verified", "errors", "revokeBodyLeak", "revokeHeaderLeak", "bodyLeak", "headerLeak", "A", "B", "Z", "statuses")
sha = lambda b: hashlib.sha256(b).hexdigest()
def blob(p): return subprocess.run(["git", "-C", R, "show", f"{HEAD}:{p}"], capture_output=True, check=True).stdout
def load(f):
    d = {}
    for l in open(f):
        x = json.loads(l); d[(x["cell"], x.get("route", ""), x["shape"])] = x
    return d
HEADM = load(W + "/logs/matrix_head.jsonl")
def run(label):
    out = f"{W}/logs/mut_{label}.jsonl"; js = f"{W}/logs/mut_{label}.vitest.json"
    for f in (out, js):
        if os.path.exists(f): os.remove(f)
    subprocess.run(["cp", f"{W}/gate_tests/gate194-matrix.test.ts", f"{V}/src/__tests__/gate194-matrix.test.ts"], check=True)
    env = {"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "HOME": W + "/home", "TMPDIR": W + "/tmp", "G194_OUT": out, "G194_SIDE": label}
    p = subprocess.run([R + "/Blockchain/Dev/node_modules/.bin/vitest", "run", "--root", V, PR_TEST, "src/__tests__/gate194-matrix.test.ts",
                        "--reporter=json", "--outputFile=" + js], cwd=W + "/cwd", env=env, capture_output=True, text=True, timeout=600)
    os.remove(f"{V}/src/__tests__/gate194-matrix.test.ts")
    d = json.load(open(js))
    failed = {"pr": [], "gate": []}; total = {"pr": 0, "gate": 0}
    for f in d["testResults"]:
        k = "pr" if f["name"].endswith("ks1959-revoke-write-fails-closed.test.ts") else "gate"
        if not f["assertionResults"]: failed[k].append(("SUITE FAILED TO LOAD", (f.get("message") or "")[:140]))
        for a in f["assertionResults"]:
            total[k] += 1
            if a["status"] != "passed": failed[k].append((a["title"], (a.get("failureMessages") or [""])[0].split("\n")[0][:140]))
    diffs = []
    if os.path.exists(out):
        mm = load(out)
        for key, hx in HEADM.items():
            mx = mm.get(key)
            if mx is None: diffs.append((key, "missing")); continue
            ch = [f for f in FIELDS if hx.get(f) != mx.get(f)]
            if ch: diffs.append((key, {f: (hx.get(f), mx.get(f)) for f in ch}))
    else:
        diffs.append(("ALL", "no matrix output"))
    return p.returncode, failed, total, diffs
rows = []
detail = open(f"{W}/logs/mutants_detail.txt", "w")
for name, edits in M:
    tag = name.split(" ")[0]
    origs = {}
    bad = None
    for path, a, b in edits:
        if path not in origs: origs[path] = blob(path)
    cur = {p: o.decode() for p, o in origs.items()}
    for path, a, b in edits:
        n = cur[path].count(a)
        if n != 1: bad = f"INVALID anchor count {n} in {path.rsplit('/', 1)[-1]}: {a[:50]!r}"; break
        cur[path] = cur[path].replace(a, b)
    if bad: rows.append((name, bad)); continue
    for p, s in cur.items(): open(f"{R}/{p}", "w").write(s)
    try:
        rc, failed, total, diffs = run(tag)
    finally:
        for p, o in origs.items(): open(f"{R}/{p}", "wb").write(o)
    restored = all(sha(open(f"{R}/{p}", "rb").read()) == sha(o) for p, o in origs.items())
    killed = bool(failed["pr"]) or bool(diffs)
    rows.append((name, f"rc {rc} | PR file red {len(failed['pr'])} of {total['pr']} | gate matrix tests red {len(failed['gate'])} of {total['gate']} | gate cells differing from head {len(diffs)} | {'KILLED' if killed else 'SURVIVED'} | restored sha-equal {restored}"))
    detail.write(f"== {name}\n" + "".join(f"  PR red: {t} :: {m}\n" for t, m in failed["pr"]) + "".join(f"  gate red: {t} :: {m}\n" for t, m in failed["gate"])
                 + "".join(f"  cell diff: {k} :: {json.dumps(v)[:400]}\n" for k, v in diffs))
    detail.flush()
rc, failed, total, diffs = run("clean")
rows.append(("clean", f"rc {rc} | PR file red {len(failed['pr'])} of {total['pr']} | gate tests red {len(failed['gate'])} of {total['gate']} | gate cells differing from head {len(diffs)} {[d[0] for d in diffs]}"))
st = subprocess.run(["git", "-C", R, "status", "--short"], capture_output=True, text=True).stdout
rows.append(("git status after", repr(st)))
open(f"{W}/logs/mutants_table.txt", "w").write("\n".join(f"{a}: {b}" for a, b in rows) + "\n")
print(open(f"{W}/logs/mutants_table.txt").read())
