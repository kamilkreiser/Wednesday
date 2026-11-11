import glob, re, os, json, collections
N = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/"
files = sorted(glob.glob(N + "READY_*"))
pat = re.compile(r'^(?:\+\+\+ b/|--- a/|diff --git a/)(.+?)(?: b/.*)?\s*$')
m = collections.defaultdict(set); nohdr = []
for f in files:
    found = False
    for ln in open(f, encoding="utf-8", errors="replace"):
        g = pat.match(ln.rstrip("\n"))
        if g:
            m[g.group(1)].add(os.path.basename(f)); found = True
    if not found: nohdr.append(os.path.basename(f))
json.dump({k: sorted(v) for k, v in m.items()}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence", "ready_paths.json"), "w"), indent=0)
print("READY files:", len(files), "with diff headers:", len(files) - len(nohdr), "without:", len(nohdr), "distinct paths:", len(m))
