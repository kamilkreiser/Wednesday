import json, os, subprocess, sys
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
CLONE = S + "/clone"
DEV = sys.argv[1]
m = json.load(open(S + "/measure_0a6177.json"))
item_files = {}
for run, r in m.items():
    for f in r.get("files", []):
        item_files.setdefault(f, []).append(run)
EXTRA = ["Blockchain/Dev/docs/openapi/secuura-api.yaml",
         "Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html",
         "Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html"]


def git(*a, idx=None):
    env = dict(os.environ)
    if idx:
        env["GIT_INDEX_FILE"] = idx
    p = subprocess.run(["git", "-C", CLONE] + list(a), capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


rows = []
os.makedirs(S + "/pidx", exist_ok=True)
for line in open(S + "/pulls_1300.txt"):
    n, sha = line.split()
    rc, mb, err = git("merge-base", DEV, sha)
    if rc != 0:
        rows.append((n, sha[:12], "NO-MERGE-BASE " + err.strip()[:80], [], ""))
        continue
    mb = mb.strip()
    rc, files, err = git("diff", "--name-only", mb, sha)
    files = [f for f in files.splitlines() if f]
    # is the PR's own diff still forward-applicable at develop (i.e. NOT landed)?
    rc, patch, err = git("diff", "--binary", mb, sha)
    pf = f"{S}/pidx/p{n}.diff"
    open(pf, "w").write(patch)
    idx = f"{S}/pidx/i{n}"
    git("read-tree", DEV, idx=idx)
    frc, _, ferr = git("apply", "--cached", "--check", pf, idx=idx)
    rrc, _, rerr = git("apply", "--cached", "--check", "-R", pf, idx=idx)
    state = ("fwd-OK" if frc == 0 else "fwd-FAIL") + "/" + ("rev-OK" if rrc == 0 else "rev-FAIL")
    hits = sorted({f for f in files if f in item_files or f in EXTRA})
    rows.append((n, sha[:12], state, hits, len(files)))
for n, sha, state, hits, nf in rows:
    if hits or "fwd-OK" in state:
        print(n, sha, state, nf, "files; overlap:", [h.split("/")[-1] for h in hits])
print("pulls checked:", len(rows))
