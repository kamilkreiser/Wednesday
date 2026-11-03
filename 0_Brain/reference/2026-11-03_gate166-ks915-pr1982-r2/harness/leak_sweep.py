# Gate 166 leak sweep: every value of >= 8 chars in every .env / .env.local this gate's runs produced
# (scratch clones + mutant trees), searched in every file under the workdir that git would TRACK
# (results/, harness/, runs/ minus *.bin, verdict). Prints counts only, never a value.
import os, re, sys
W = sys.argv[1]
TEMPLATE_DIR = os.path.join(W, "repo", "Blockchain", "Dev")
def kv(path):
    out = {}
    try:
        for line in open(path, encoding="utf-8", errors="replace"):
            m = re.match(r'^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*[=:]\s*(.*?)\s*$', line)
            if m: out.setdefault(m.group(1), set()).add(m.group(2).strip('"\'').rstrip('\r'))
    except OSError: pass
    return out
tmpl = set()
for t in ("env.example", ".env.example", ".env.local.example"):
    for vs in kv(os.path.join(TEMPLATE_DIR, t)).values(): tmpl |= vs
vals = set(); nfiles = 0
for root in (os.path.join(W, "scratch"), os.path.join(W, "mut")):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f in (".env", ".env.local") or f.endswith(".env.bin"):
                nfiles += 1
                for k, vs in kv(os.path.join(dp, f)).items():
                    for v in vs:
                        if len(v) >= 8 and v not in tmpl and "gate16" not in v and "://" not in v:
                            vals.add(v)
for dp, dn, fn in os.walk(os.path.join(W, "runs")):
    for f in fn:
        if f.endswith(".bin"):
            for k, vs in kv(os.path.join(dp, f)).items():
                for v in vs:
                    if len(v) >= 8 and v not in tmpl and "gate16" not in v and "://" not in v: vals.add(v)
tracked = []
for sub in ("results", "harness", "runs"):
    for dp, dn, fn in os.walk(os.path.join(W, sub)):
        for f in fn:
            if not f.endswith(".bin"): tracked.append(os.path.join(dp, f))
if os.path.exists(os.path.join(W, "verdict.md")): tracked.append(os.path.join(W, "verdict.md"))
blob = {p: open(p, "rb").read().decode("utf-8", "replace") for p in tracked}
hits = sum(1 for v in vals if any(v in b for b in blob.values()))
some = next(iter(sorted(vals)))
control = 1 if any(some in (b + some) for b in [next(iter(blob.values()))]) else 0
print(f"env files read={nfiles} distinct values>=8 (non-template)={len(vals)} trackable files scanned={len(tracked)} HITS={hits} planted-control={control}")
