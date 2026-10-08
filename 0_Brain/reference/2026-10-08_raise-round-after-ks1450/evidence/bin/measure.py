import json, os, subprocess, sys, hashlib
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
CLONE = S + "/clone"
RUNS = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs"
DEV = sys.argv[1]
items = [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith('#')]
IDX = S + "/idx"
n_idx = [0]


def git(args, idx=None):
    env = dict(os.environ)
    if idx:
        env["GIT_INDEX_FILE"] = idx
    p = subprocess.run(["git", "-C", CLONE] + args, capture_output=True, text=True, env=env)
    return p.returncode, (p.stdout + p.stderr).strip()


def fresh():
    n_idx[0] += 1
    idx = f"{IDX}/i{n_idx[0]}"
    rc, out = git(["read-tree", DEV], idx)
    assert rc == 0, out
    return idx


os.makedirs(IDX, exist_ok=True)
out = {}
for run in items:
    d = f"{RUNS}/spark_secuura_{run}/out.md.checker"
    patch = d + "/patch.diff"
    rec = {"run": run}
    if not os.path.exists(patch):
        rec["error"] = "no patch.diff"
        out[run] = rec
        continue
    b = open(patch, "rb").read()
    rec["bytes"] = len(b)
    rec["sha16"] = hashlib.sha256(b).hexdigest()[:16]
    secs = json.load(open(d + "/sections.json"))
    rec["files"] = [s["path"] for s in secs]
    srec = []
    for k, s in enumerate(secs, 1):
        s.setdefault("n", k)
        opts_f = f"{d}/section_{s['n']}.opts"
        lines = open(opts_f).read().split("\n") if os.path.exists(opts_f) else [s["file"], ""]
        f = lines[0] or s["file"]
        o = lines[1].split() if len(lines) > 1 else []
        idx = fresh()
        fr, fo = git(["apply", "--cached", "--check"] + o + [f], idx)
        rr, ro = git(["apply", "--cached", "--check", "-R"] + o + [f], idx)
        srec.append({"n": s["n"], "path": s["path"], "file": os.path.basename(f),
                     "opts": " ".join(o) or "strict", "fwd": fr, "rev": rr,
                     "fwd_err": fo[:200], "rev_err": ro[:200]})
    rec["sections"] = srec
    idx = fresh()
    fr, fo = git(["apply", "--cached", "--check", patch], idx)
    rr, ro = git(["apply", "--cached", "--check", "-R", patch], idx)
    rec["whole_fwd"] = fr
    rec["whole_rev"] = rr
    rec["whole_fwd_err"] = fo[:300]
    if fr == 0:
        ar, ao = git(["apply", "--cached", patch], idx)
        tr, to = git(["write-tree"], idx)
        rec["tree"] = to[:12]
        cr, co = git(["apply", "--cached", "--check", patch], idx)
        rec["twice_rc"] = cr
    out[run] = rec
json.dump(out, open(sys.argv[3], "w"), indent=1)
for run, r in out.items():
    secs = " ".join(("F" if x["fwd"] == 0 else "f") + ("R" if x["rev"] == 0 else "r") + ("" if x["opts"] == "strict" else "*") for x in r.get("sections", []))
    print(f'{run} | {r.get("bytes")} {r.get("sha16")} | secs {secs} | whole fwd={r.get("whole_fwd")} rev={r.get("whole_rev")} tree={r.get("tree")} twice={r.get("twice_rc")} | {len(r.get("files", []))} files {r.get("error", "")}')
