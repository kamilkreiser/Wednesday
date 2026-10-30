#!/usr/bin/env python3
"""Gate 31 tamper harness (gate 30's shape). Each mutant: exact-once anchor replace in api-gateway auth.ts, parse check
(TS transpile diagnostics) on a copy kept OUTSIDE src/ and __tests__, vitest json run, restore by byte copy, sha256 assert."""
import hashlib, json, os, shutil, subprocess, sys

GW = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3595961a-a258-453d-996e-1aad78887d58/scratchpad/gate31/clone/Blockchain/Dev/services/api-gateway"
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = f"{HERE}/tamper_out"
AUTH = f"{GW}/src/middleware/auth.ts"
PRFILE = "src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts"
TESTS = os.environ.get("G31_TESTS", PRFILE).split()
TAG = os.environ.get("G31_TAG", "")
VITEST = f"{GW}/../../node_modules/.bin/vitest"

PRED = "  return status >= 500 || status === 408 || status === 429;"
NEG4XX = "      apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });\n      return { outcome: 'rejected' };"
UNAV = "      if (couldNotAnswer(resp.status)) return unavailable(`security service answered ${resp.status}`);"
MUTANTS = {
    "a_author_429_to_403": (PRED, "  return status >= 500 || status === 408 || status === 403; // G31 a"),
    "b_F7_drop_429": (PRED, "  return status >= 500 || status === 408; // G31 b"),
    "c_F8_every_nonok_unavailable": (PRED, "  return status > 0; // G31 c"),
    "d_add_401_retryable": (PRED, "  return status >= 500 || status === 408 || status === 429 || status === 401; // G31 d"),
    "e_add_403_retryable": (PRED, "  return status >= 500 || status === 408 || status === 429 || status === 403; // G31 e"),
    "f_drop_408": (PRED, "  return status >= 500 || status === 429; // G31 f"),
    "g_gt500_not_ge500": (PRED, "  return status > 500 || status === 408 || status === 429; // G31 g"),
    "h_every_4xx_unavailable": (PRED, "  return status >= 400; // G31 h"),
    "i_F18_4xx_not_cached": (NEG4XX, "      return { outcome: 'rejected' }; // G31 i"),
    "j_4xx_neg_ttl_60s": (NEG4XX, NEG4XX.replace("30_000", "60_000") + " // G31 j"),
    "k_4xx_neg_ttl_3s": (NEG4XX, NEG4XX.replace("30_000", "3_000") + " // G31 k"),
    "l_429_negative_cached": (UNAV, "      if (couldNotAnswer(resp.status)) { apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 }); return unavailable(`security service answered ${resp.status}`); } // G31 l"),
    "m_nonok_unavailable_not_logged": (UNAV, "      if (couldNotAnswer(resp.status)) return { outcome: 'unavailable', reason: 'x' }; // G31 m"),
    "n_4xx_branch_returns_unavailable_uncached": (NEG4XX, "      return { outcome: 'unavailable', reason: 'G31 n' };"),
}

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_ok(path):
    js = ("const ts=require('typescript');const s=require('fs').readFileSync(process.argv[1],'utf8');"
          "const r=ts.transpileModule(s,{reportDiagnostics:true,compilerOptions:{module:1,target:99}});"
          "const d=(r.diagnostics||[]).filter(x=>x.category===1);console.log(d.length);process.exit(d.length?1:0)")
    r = subprocess.run(["node", "-e", js, path], cwd=GW, capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip() + r.stderr.strip()[:300]

def run(label):
    out = f"{OUTD}/t{TAG}_{label}.json"
    r = subprocess.run([VITEST, "run", *TESTS, "--maxWorkers=3", "--reporter=json", f"--outputFile={out}"], cwd=GW, capture_output=True, text=True)
    d = json.load(open(out))
    reds = [f["name"].split("/")[-1][:44] + " :: " + a["title"][:70] for f in d["testResults"] for a in f["assertionResults"] if a["status"] == "failed"]
    return d["numPassedTests"], d["numFailedTests"], d["numTotalTests"], reds, r.returncode

def main(names):
    os.makedirs(OUTD, exist_ok=True)
    res = {}
    base = sha(AUTH)
    p, f, t, reds, rc = run("baseline"); print(f"baseline: {p} pass / {f} fail / {t} total rc={rc}", flush=True)
    for r_ in reds: print("    RED", r_)
    for name in names:
        anchor, repl = MUTANTS[name]
        src = open(AUTH).read()
        n = src.count(anchor)
        if n != 1: print(f"{name}: ANCHOR COUNT {n} != 1, skipped"); continue
        mut = src.replace(anchor, repl)
        mpath = f"{OUTD}/mutant_{name}.ts"; open(mpath, "w").write(mut)
        ok, diag = parse_ok(mpath)
        if not ok: print(f"{name}: MUTANT DOES NOT PARSE ({diag}), skipped"); continue
        orig = f"{OUTD}/orig_auth.ts"; shutil.copyfile(AUTH, orig)
        try:
            shutil.copyfile(mpath, AUTH)
            assert sha(AUTH) != base
            p, f, t, reds, rc = run(name)
        finally:
            shutil.copyfile(orig, AUTH)
        restored = sha(AUTH) == base
        print(f"{name}: {p} pass / {f} fail / {t} total rc={rc} | restored sha256 equal={restored} ({base[:16]})", flush=True)
        for r_ in reds: print("    RED", r_)
        res[name] = dict(passed=p, failed=f, total=t, reds=reds, restored=restored)
        if not restored: print("RESTORE FAILED, stopping"); break
    p, f, t, reds, rc = run("final"); print(f"final: {p} pass / {f} fail / {t} total rc={rc} sha256 {sha(AUTH)[:16]}")
    json.dump(res, open(f"{OUTD}/tamper_results{TAG}.json", "w"), indent=1)

if __name__ == "__main__":
    main(sys.argv[1:] or list(MUTANTS))
