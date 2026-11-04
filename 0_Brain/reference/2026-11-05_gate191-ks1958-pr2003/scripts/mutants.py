# gate 191 mutants against the COMMITTED head bytes. usage: python3 -I mutants.py
# Each mutant: anchor count == 1, apply, run the PR's ks1958 file AND the gate's matrix file (json reporter),
# restore from `git show <head>:<path>` and check sha256 equal to the committed blob. One clean run at the end.
import hashlib, json, os, subprocess
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003"
R = W + "/repo"; V = R + "/Blockchain/Dev/services/vc-issuer"
HEAD = "8b140178276457116714892fe0cf73b9f1e92c8c"
P_REPO = "Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts"
P_RES = "Blockchain/Dev/services/vc-issuer/src/services/revocationResolvers.ts"
PR_TEST = "src/__tests__/ks1958-revocation-read-fails-closed.test.ts"
M = [  # seat's anchors (tools/mutants_a_f31.py), copied verbatim, plus the gate's own m5 / m6
    ("m1", P_REPO, "      if (options.failClosedOnReadError) {\n", "      if (false && options.failClosedOnReadError) {\n"),
    ("m2", P_REPO, "        [id],\n      );\n      if (result.rows.length > 0) return result.rows[0].credential;\n",
     "        [id],\n      );\n      if (result.rows.length > 0) return result.rows[0].credential;\n      if (options.failClosedOnReadError) throw new CredentialStoreReadError();\n"),
    ("m3", P_REPO, "      if (options.failClosedOnReadError) {\n", "      if (options.failClosedOnReadError && reason !== 'unreadable thrown value') {\n"),
    ("m4", P_REPO, "  const credential = await getById(id);\n", "  const credential = await getById(id, { failClosedOnReadError: true });\n"),
    ("m5-gate-rethrow", P_REPO, "        throw new CredentialStoreReadError();\n", "        throw err;\n"),
    ("m6-gate-resolver-drops-option", P_RES, "credentialRepo.getById(credentialId, { failClosedOnReadError: true })", "credentialRepo.getById(credentialId)"),
]
sha = lambda b: hashlib.sha256(b).hexdigest()
def blob(p): return subprocess.run(["git", "-C", R, "show", f"{HEAD}:{p}"], capture_output=True, check=True).stdout
def run(label):
    out = f"{W}/logs/mut_{label}.jsonl"; js = f"{W}/logs/mut_{label}.vitest.json"
    for f in (out, js):
        if os.path.exists(f): os.remove(f)
    subprocess.run(["cp", f"{W}/gate_tests/gate191-matrix.test.ts", f"{V}/src/__tests__/gate191-matrix.test.ts"], check=True)
    env = {"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "HOME": W + "/home", "TMPDIR": W + "/tmp", "G191_OUT": out, "G191_SIDE": label}
    p = subprocess.run([R + "/Blockchain/Dev/node_modules/.bin/vitest", "run", "--root", V, PR_TEST, "src/__tests__/gate191-matrix.test.ts",
                        "--reporter=json", "--outputFile=" + js], cwd=W + "/cwd", env=env, capture_output=True, text=True, timeout=600)
    os.remove(f"{V}/src/__tests__/gate191-matrix.test.ts")
    d = json.load(open(js))
    failed = {"pr": [], "gate": []}; total = {"pr": 0, "gate": 0}
    for f in d["testResults"]:
        k = "pr" if f["name"].endswith("ks1958-revocation-read-fails-closed.test.ts") else "gate"
        for a in f["assertionResults"]:
            total[k] += 1
            if a["status"] != "passed": failed[k].append((a["title"], (a.get("failureMessages") or [""])[0].split("\n")[0][:140]))
    return p.returncode, failed, total, out
rows = []
for name, path, anchor, repl in M:
    orig = blob(path); src = orig.decode()
    n = src.count(anchor)
    if n != 1: rows.append((name, "INVALID anchor count %d" % n)); continue
    open(f"{R}/{path}", "w").write(src.replace(anchor, repl))
    try:
        rc, failed, total, out = run(name)
    finally:
        open(f"{R}/{path}", "wb").write(orig)
    restored = sha(open(f"{R}/{path}", "rb").read()) == sha(orig)
    killed = bool(failed["pr"])
    rows.append((name, f"rc {rc} | PR file red {len(failed['pr'])} of {total['pr']} | gate matrix red {len(failed['gate'])} of {total['gate']} | {'KILLED by the PR file' if killed else 'SURVIVED the PR file'} | restored sha-equal {restored}"))
    with open(f"{W}/logs/mutants_detail.txt", "a") as fh:
        fh.write(f"== {name}\n" + "".join(f"  PR red: {t} :: {m}\n" for t, m in failed["pr"]) + "".join(f"  gate red: {t} :: {m}\n" for t, m in failed["gate"]))
rc, failed, total, _ = run("clean")
rows.append(("clean", f"rc {rc} | PR file red {len(failed['pr'])} of {total['pr']} | gate red {len(failed['gate'])} of {total['gate']}"))
st = subprocess.run(["git", "-C", R, "status", "--short"], capture_output=True, text=True).stdout
rows.append(("git status after", repr(st)))
open(f"{W}/logs/mutants_table.txt", "w").write("\n".join(f"{a}: {b}" for a, b in rows) + "\n")
print(open(f"{W}/logs/mutants_table.txt").read())
