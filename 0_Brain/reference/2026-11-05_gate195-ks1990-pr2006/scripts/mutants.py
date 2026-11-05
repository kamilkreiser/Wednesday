# gate 195 mutants on the COMMITTED head bytes of adminConfig.ts. usage: python3 -I mutants.py
# anchor count must be 1 (else INVALID), apply, run seat files ks1990 + ks1802 (20 cells) AND the gate matrix; restore from git blob, sha256-check.
import hashlib, json, os, subprocess, shutil
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006"
R = W + "/repo"; S = R + "/Blockchain/Dev/services/originate"
HEAD = "6311c141f99e5ade8d94e60ee15b0c80006a52cd"
P = "Blockchain/Dev/services/originate/src/routes/adminConfig.ts"
A = "const nothingCreatedAndSomethingFailed = created === 0 && failed > 0;"
B = "res.status(nothingCreatedAndSomethingFailed ? 500 : 200).json({"
C = "      success: failed === 0,"
M = [
 ("m1 success true unconditionally", [(C, "      success: true,")]),
 ("m2 partial reads true", [(C, "      success: failed === 0 || created > 0,")]),
 ("m3 drop the nothing-created check", [(A, "const nothingCreatedAndSomethingFailed = false && created === 0 && failed > 0;")]),
 ("m4 raw error message in the body", [("        failed++;\n", "        failed++; (globalThis as any).__g195e = err;\n"), (C, "      success: failed === 0, error: String((globalThis as any).__g195e?.message),")]),
 ("m5 500 mapped to 2xx", [(B, "res.status(nothingCreatedAndSomethingFailed ? 202 : 200).json({")]),
 ("m6 boundary: one failure not enough (failed > 1)", [(A, "const nothingCreatedAndSomethingFailed = created === 0 && failed > 1;")]),
 ("m7 already-present counted as created", [("        else alreadyPresent++;", "        else created++;")]),
 ("m8 any failure answers 500", [(A, "const nothingCreatedAndSomethingFailed = failed > 0;")]),
 ("g1 own: created === 0 -> created < 2 (500 boundary)", [(A, "const nothingCreatedAndSomethingFailed = created < 2 && failed > 0;")]),
 ("g2 own: created === 0 -> created <= 0 (expected EQUIVALENT)", [(A, "const nothingCreatedAndSomethingFailed = created <= 0 && failed > 0;")]),
 ("g3 own: success failed === 0 -> failed < 2", [(C, "      success: failed < 2,")]),
 ("g4 own: 500 -> 503 (status value)", [(B, "res.status(nothingCreatedAndSomethingFailed ? 503 : 200).json({")]),
]
sha = lambda b: hashlib.sha256(b).hexdigest()
def blob(): return subprocess.run(["git", "-C", R, "show", f"{HEAD}:{P}"], capture_output=True, check=True).stdout
HB = blob(); FP = R + "/" + P
shutil.copy(W + "/gate_tests/gate195-matrix.test.ts", S + "/src/__tests__/gate195-matrix.test.ts")
FILES = ["ks1990-seed-demo-users-success-follows-the-counts", "ks1802-seed-demo-users-survives", "gate195-matrix"]
def run(label):
    out = f"{W}/runs/mut_{label}.jsonl"; js = f"{W}/runs/mut_{label}.json"
    open(out, "w").close()
    env = {"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "HOME": W + "/home", "TMPDIR": W + "/tmp", "G195_OUT": out, "G195_SIDE": label}
    subprocess.run([R + "/Blockchain/Dev/node_modules/.bin/jest", "--rootDir", S, "-c", S + "/jest.config.js", *FILES, "--json", "--outputFile=" + js],
                   cwd=W + "/cwd", env=env, capture_output=True, text=True, timeout=900)
    d = json.load(open(js)); tot = {"seat": 0, "gate": 0}; fail = {"seat": [], "gate": []}; loadfail = 0
    for f in d["testResults"]:
        k = "gate" if f["name"].endswith("gate195-matrix.test.ts") else "seat"
        if not f["assertionResults"]: loadfail += 1
        for a in f["assertionResults"]:
            tot[k] += 1
            if a["status"] != "passed": fail[k].append(a["title"][:60])
    # gate-side: leak hits / matrix differ from head
    lk = {}
    for l in open(out):
        r = json.loads(l)
        if r["cell"].startswith("leak"): lk[r["cell"]] = r["leakHits"]
    return tot, fail, loadfail, lk
rows = []
try:
    base_tot, base_fail, lf, lk = run("clean0")
    print("clean0", base_tot, {k: len(v) for k, v in base_fail.items()}, "loadfail", lf, "leak", lk, flush=True)
    for name, edits in M:
        s = HB.decode(); ok = True; cnts = []
        for old, new in edits:
            c = s.count(old); cnts.append(c)
            if c != 1: ok = False
            s = s.replace(old, new, 1)
        if not ok:
            rows.append((name, "INVALID", cnts)); print(name, "INVALID anchors", cnts, flush=True); continue
        open(FP, "w").write(s)
        tot, fail, lf, lk = run(name.split()[0])
        open(FP, "wb").write(HB)
        restored = sha(open(FP, "rb").read()) == sha(HB)
        rows.append((name, cnts, tot, len(fail["seat"]), len(fail["gate"]), lf, lk, restored))
        print(name, "anchors", cnts, "seat", tot["seat"], "red", len(fail["seat"]), "| gate cells", tot["gate"], "red", len(fail["gate"]), "loadfail", lf, "leak", lk, "restored", restored, flush=True)
    t, f, lf, lk = run("clean1")
    print("clean1", t, {k: len(v) for k, v in f.items()}, "loadfail", lf, flush=True)
finally:
    open(FP, "wb").write(HB)
    os.replace(S + "/src/__tests__/gate195-matrix.test.ts", W + "/scratch/_quarantine/gate195-matrix.mut.test.ts")
    print("final blob equal head:", sha(open(FP, "rb").read()) == sha(HB))
