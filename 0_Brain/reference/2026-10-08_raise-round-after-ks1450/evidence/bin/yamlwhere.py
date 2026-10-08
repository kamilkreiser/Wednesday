"""For each YAML companion: where does it INTEND to add `required: true` (path+method in the
companion's own base blob 52310cab1) and where does `git apply` actually PUT it at develop
(alone, and inside the 12-stack)? A mismatch = the generic-context trap."""
import os, re, subprocess, sys
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
CLONE = S + "/clone"
BR = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs"
Y = "Blockchain/Dev/docs/openapi/secuura-api.yaml"
DEV = sys.argv[1]
names = sys.argv[2:]


def git(args, idx=None, inp=None):
    env = dict(os.environ)
    if idx:
        env["GIT_INDEX_FILE"] = idx
    p = subprocess.run(["git", "-C", CLONE] + args, capture_output=True, text=True, env=env, input=inp)
    return p.returncode, p.stdout, p.stderr


def where(lines, i):
    """enclosing path (indent 2, under paths:) and method (indent 4) for 0-based line i"""
    path = meth = None
    for j in range(i, -1, -1):
        l = lines[j]
        if meth is None and re.match(r"^    (get|post|put|patch|delete):\s*$", l):
            meth = l.strip()[:-1]
        m = re.match(r"^  (/\S+):\s*$", l)
        if m:
            path = m.group(1)
            break
    return f"{meth} {path}"


def added(before, after):
    """0-based indices in `after` of lines that are `required: true` and were added"""
    rc, out, err = git(["diff", "--no-index", "-U0", "--", before, after])
    res = []
    for h in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start = int(h.group(1)); n = int(h.group(2) or 1)
        res += list(range(start - 1, start - 1 + n))
    return res


os.makedirs(S + "/ywhere", exist_ok=True)
_, base_old, _ = git(["cat-file", "blob", "52310cab1"])
_, base_dev, _ = git(["show", f"{DEV}:{Y}"])
open(S + "/ywhere/old.yaml", "w").write(base_old)
open(S + "/ywhere/dev.yaml", "w").write(base_dev)
# intended: apply companion to the OLD blob with `git apply` on a temp file tree
stack_idx = S + "/ywhere/stack_idx"
if os.path.exists(stack_idx):
    os.rename(stack_idx, stack_idx + ".prev")
git(["read-tree", DEV], stack_idx)
intended_all, actual_all = {}, {}
for n in names:
    c = f"{BR}/{n}/openapi-yaml.companion.diff"
    # intended: hunk target lines in OLD blob (new-side line numbers in the companion)
    txt = open(c).read()
    old_lines = base_old.split("\n")
    intended = []
    shift = 0
    for h in re.finditer(r"^@@ -(\d+),\d+ \+(\d+),\d+ @@", txt, re.M):
        o = int(h.group(1))
        # the '+' line is the 4th line of the hunk (3 context lines before it) in these companions
        intended.append(where(old_lines, o - 1 + 3))
    # actual alone at develop
    idx = S + f"/ywhere/i_{n}"
    if os.path.exists(idx):
        os.rename(idx, idx + ".prev")
    git(["read-tree", DEV], idx)
    rc, _, err = git(["apply", "--cached", c], idx)
    _, ls, _ = git(["ls-files", "-s", Y], idx)
    blob = ls.split()[1]
    _, after, _ = git(["cat-file", "blob", blob])
    open(S + f"/ywhere/a_{n}.yaml", "w").write(after)
    al = after.split("\n")
    act = [where(al, i) for i in added(S + "/ywhere/dev.yaml", S + f"/ywhere/a_{n}.yaml")]
    # actual inside the stack
    rc2, _, err2 = git(["apply", "--cached", c], stack_idx)
    ok = sorted(intended) == sorted(act)
    print(f"{'OK  ' if ok else 'MISMATCH'} {n}: intended {intended} | at develop alone {act} | stack apply rc {rc2}")
_, ls, _ = git(["ls-files", "-s", Y], stack_idx)
_, after, _ = git(["cat-file", "blob", ls.split()[1]])
open(S + "/ywhere/stack.yaml", "w").write(after)
al = after.split("\n")
act = sorted(where(al, i) for i in added(S + "/ywhere/dev.yaml", S + "/ywhere/stack.yaml"))
print("STACK of all:", len(act), "added lines at", act)
# control: a deliberately shifted companion must be detected as a mismatch by where()
print("CONTROL where() discriminates:", where(base_old.split("\n"), 21663 - 1 + 3), "vs", where(base_old.split("\n"), 13474 - 1 + 3))
