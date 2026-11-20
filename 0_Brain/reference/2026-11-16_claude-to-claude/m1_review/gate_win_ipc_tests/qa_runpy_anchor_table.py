#!/usr/bin/env python3
"""QA-WIN-IPC: for every mutation in crates/coagent-relay/red-controls/run.py whose target is under
crates/coagent-ipc/, count the anchor ('old') text in the target at two git revisions.
run.py needs each anchor exactly once (run_one: `if n != 1: PROBLEM`).
Usage: python3 -I qa_runpy_anchor_table.py <clone> <rev_main> <rev_head>"""
import ast, subprocess, sys
clone, rmain, rhead = sys.argv[1:4]
def show(rev, path):
    r = subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None
src = show(rhead, "crates/coagent-relay/red-controls/run.py")
assert src == show(rmain, "crates/coagent-relay/red-controls/run.py"), "run.py differs between revisions"
tree = ast.parse(src)
ns = {}
for node in tree.body:  # evaluate only the simple constant assignments (R, C, ...) and M
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in ("R", "C") or name == "M" or (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            try:
                ns[name] = eval(compile(ast.Expression(node.value), "run.py", "eval"), {"__builtins__": {}}, ns)
            except Exception as e:
                print("skip", name, e)
rows = [m for m in ns["M"] if m[3].startswith("crates/coagent-ipc/")]
print(f"run.py mutations total: {len(ns['M'])}; targeting crates/coagent-ipc/: {len(rows)}")
print(f"{'id':5} {'target':36} {'main':>4} {'head':>4}  anchor (first 60 chars)")
bad = 0
for m in rows:
    mid, _, _, path, old = m[:5]
    a, b = show(rmain, path), show(rhead, path)
    ca = a.count(old) if a is not None else -1
    cb = b.count(old) if b is not None else -1
    flag = "" if ca == cb == 1 else "  <-- DIFFERS/NOT ONCE"
    bad += bool(flag)
    print(f"{mid:5} {path:36} {ca:4} {cb:4}  {old[:60]!r}{flag}")
print("RESULT:", "all anchors found exactly once at both revisions" if not bad else f"{bad} row(s) differ")
sys.exit(1 if bad else 0)
