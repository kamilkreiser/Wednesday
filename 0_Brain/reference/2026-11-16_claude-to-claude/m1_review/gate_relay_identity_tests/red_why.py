#!/usr/bin/env python3
"""QA gate: for each red-control row M80..M106 of run.py, apply it alone in a scratch worktree, run
exactly that row's cargo args, and print the failing tests and their panic message, so the reader
can judge whether the row is red on its NAMED property (the runner itself only matches test names).
usage: red_why.py <worktree>"""
import os, re, subprocess, sys, hashlib

WT = sys.argv[1]
src = open(os.path.join(WT, "crates/coagent-relay/red-controls/run.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(WT, "crates/coagent-relay/red-controls/run.py")}
exec(src.split("\ndef sh(")[0], ns)  # defines R, C, M (and DEP) only
rows = [m for m in ns["M"] if m[0].startswith("M") and m[0][1:].isdigit() and int(m[0][1:]) >= 80]
for (mid, tno, prop, rel, old, new, args) in rows:
    p = os.path.join(WT, rel)
    orig = open(p, encoding="utf-8").read()
    assert orig.count(old) == 1, mid
    try:
        open(p, "w", encoding="utf-8").write(orig.replace(old, new, 1))
        r = subprocess.run(["cargo", "test", "--locked", "--offline"] + args, cwd=WT, capture_output=True, text=True, timeout=1800)
        out = r.stdout + r.stderr
    finally:
        open(p, "w", encoding="utf-8").write(orig)
    failed = re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)
    panics = re.findall(r"panicked at [^\n]*\n([^\n]*)", out)
    print(f"{mid} rc={r.returncode} prop: {prop}")
    print("   failed: " + "; ".join(failed[:4]))
    for pm in panics[:2]:
        print("   says: " + pm.strip()[:260])
    sys.stdout.flush()
print("restored:", hashlib.sha256(open(os.path.join(WT, "crates/coagent-cli/src/identity_file.rs"), "rb").read()).hexdigest()[:16])
