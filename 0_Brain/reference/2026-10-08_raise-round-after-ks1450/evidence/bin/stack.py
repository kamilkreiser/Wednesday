import os, subprocess, sys, hashlib
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
CLONE = S + "/clone"
RUNS = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs"
BRIEFS = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs"
DEV = sys.argv[1]
name = sys.argv[2]
specs = sys.argv[3:]
os.makedirs(S + "/sidx", exist_ok=True)


def path(spec):
    if spec.startswith("Y:"):
        return f"{BRIEFS}/{spec[2:]}/openapi-yaml.companion.diff"
    return f"{RUNS}/spark_secuura_{spec}/out.md.checker/patch.diff"


def git(args, idx):
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    p = subprocess.run(["git", "-C", CLONE] + args, capture_output=True, text=True, env=env)
    return p.returncode, (p.stdout + p.stderr).strip()


def run(order, tag):
    idx = f"{S}/sidx/{name}_{tag}"
    if os.path.exists(idx):
        os.rename(idx, idx + ".prev")
    rc, o = git(["read-tree", DEV], idx)
    assert rc == 0, o
    for sp in order:
        p = path(sp)
        rc, o = git(["apply", "--cached", "--check", p], idx)
        if rc != 0:
            return f"FAIL at {sp}: {o[:200]}", None
        rc, o = git(["apply", "--cached", p], idx)
        assert rc == 0, o
    rc, t = git(["write-tree"], idx)
    # control: re-applying the FIRST patch on the stacked index must fail
    rc2, o2 = git(["apply", "--cached", "--check", path(order[0])], idx)
    return f"OK tree {t[:12]} (re-apply of first: rc {rc2})", t


for sp in specs:
    assert os.path.exists(path(sp)), path(sp)
a, ta = run(specs, "fwd")
b, tb = run(list(reversed(specs)), "rev")
print(f"STACK {name} ({len(specs)} patches): forward {a} | reverse {b} | trees equal: {ta is not None and ta == tb}")
