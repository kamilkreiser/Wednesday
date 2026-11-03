# Gate 173 leak sweep: every generated value found in any env file the gate produced, searched in every carrier.
# Prints counts and carrier paths only, never a value.
import os, re, sys, pathlib, random
W = pathlib.Path("/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989")
R = W / "repo/Blockchain/Dev"
tmpl = set()
for t in (R / "env.example", R / ".env.example", R / ".env.local.example", R / "env.local.example"):
    if t.exists():
        for line in t.read_text(errors="replace").splitlines():
            m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
            if m: tmpl.add(m.group(2).strip().strip('"\''))
LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
def env_like(p):
    n = p.name
    return n in (".env", ".env.local") or n.startswith(".env-ks915.") or n.startswith(".env.ks915.") or n.endswith(".env.bin") or n.endswith(".env")
vals = set(); nfiles = 0
for base in (W / "scratch", W / "runs"):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for f in files:
            p = pathlib.Path(root) / f
            if p.is_symlink() or not env_like(p): continue
            nfiles += 1
            for line in p.read_text(errors="replace").splitlines():
                m = LINE.match(line)
                if not m: continue
                v = m.group(2).strip().strip('"\'')
                if len(v) < 12 or v in tmpl or "gate173" in v or "BEGIN" in v or "END" in v: continue
                if not re.fullmatch(r"[A-Za-z0-9+/=_.:@%-]+", v): continue
                vals.add(v)
print(f"generated values collected: {len(vals)} from {nfiles} env files")
def carriers():
    # 1. every script/suite output under runs/ (logs and .bin outputs that are not env copies)
    for root, dirs, files in os.walk(W / "runs"):
        for f in files:
            p = pathlib.Path(root) / f
            if not env_like(p): yield "runs-output", p
    # 2. everything git would TRACK in this workdir (not ignored): results/, harness/, top-level files
    for sub in ("results", "harness"):
        for root, dirs, files in os.walk(W / sub):
            for f in files: yield "tracked-" + sub, pathlib.Path(root) / f
    for f in W.iterdir():
        if f.is_file(): yield "tracked-top", f
    # 3. TMPDIR trees (bash-reader sandboxes, leftovers) and HOME
    for base in (W / "tmp", W / "home"):
        for root, dirs, files in os.walk(base):
            for f in files:
                p = pathlib.Path(root) / f
                if not p.is_symlink(): yield "tmp/home", p
CTRL = W / "runs" / "leak_control_planted.log"
if vals: CTRL.write_text("planted " + sorted(vals)[0] + "\n")
hits = {}; scanned = {}
for kind, p in carriers():
    try: data = p.read_bytes().decode("utf-8", "replace")
    except Exception: continue
    scanned[kind] = scanned.get(kind, 0) + 1
    for v in vals:
        if v in data:
            hits.setdefault((kind, str(p).replace(str(W), "<W>")), 0); hits[(kind, str(p).replace(str(W), "<W>"))] += 1
print("carriers scanned:", scanned)
ctl = [(k, p) for (k, p) in hits if p.endswith("leak_control_planted.log")]
print("planted control (same scan path) found:", len(ctl))
for kp in ctl: hits.pop(kp)
if CTRL.exists(): CTRL.unlink()
print("hits (excluding the planted control):", sum(hits.values()))
for (k, p), n in sorted(hits.items()): print(f"  HIT {k} {p} values={n}")
