#!/usr/bin/env python3
"""Round 3: give the ROOT CAUSE, not the symptom. How much guidance does it need?"""
import sys, traceback
sys.path.insert(0, "/home/datasec-rd/spark-eval")
from complex_task import TASK, ask, strip_fences, run_tests

PRIOR = open("/home/datasec-rd/spark-eval/generated_repaired.py").read()

FEEDBACK = '''Your implementation scores 24/26. Two tests still fail. I have diagnosed
the exact root cause for you.

ROOT CAUSE
----------
In __init__ you declare:
    self.dependencies = {}   # ref -> set of refs it depends on
    self.dependents   = {}   # ref -> set of refs that depend on it

`_invalidate` reads self.dependents to recurse into dependent cells. But NOTHING
IN YOUR CODE EVER WRITES TO EITHER MAP. They stay empty forever, so _invalidate
only ever evicts the single cell passed to it and never its dependents.

Proven at runtime:
    s.set_cell("A1", 1); s.set_cell("B1", "=A1*10")
    s.get_value("B1")   -> 10.0
    s.dependencies      -> {}     (empty!)
    s.dependents        -> {}     (empty!)
    s.set_cell("A1", 5)
    s.get_value("B1")   -> 10.0   (stale; should be 50.0)

THE FIX
-------
While evaluating a formula you must RECORD which cells it read. When cell X is
evaluated and reads cell Y, record:
    self.dependencies.setdefault(X, set()).add(Y)
    self.dependents.setdefault(Y, set()).add(X)
Range functions must record EVERY cell in the block, not just the endpoints.
When re-evaluating a cell, clear its old dependencies first and unregister it
from the dependents sets of the cells it previously read, so stale edges do not
accumulate.

Then _invalidate(ref) will correctly cascade to every transitive dependent.

FULL CURRENT SOURCE
-------------------
''' + PRIOR + '''

Rewrite the COMPLETE module with this fixed. Keep all 24 currently-passing
behaviours intact. Output ONLY the Python module source, no fences, no commentary.
'''

def main():
    print("=== REPAIR ROUND 2 — root cause supplied ===", flush=True)
    text, finish, usage, dt = ask(FEEDBACK, 8192, False)
    print(f"  finish={finish}  completion={usage['completion_tokens']}  "
          f"prompt={usage['prompt_tokens']}  wall={dt:.1f}s "
          f"({usage['completion_tokens']/dt:.1f} tok/s)", flush=True)
    if finish == "length":
        print("  TRUNCATED"); return
    code = strip_fences(text)
    open("/home/datasec-rd/spark-eval/generated_final.py", "w").write(code)
    ns = {}
    try:
        exec(compile(code, "<final>", "exec"), ns)
    except Exception:
        print("  IMPORT FAILED:"); traceback.print_exc(limit=3); return
    try:
        res = run_tests(ns)
    except Exception:
        print("  SUITE CRASHED:"); traceback.print_exc(limit=3); return
    passed = sum(1 for _, ok, _ in res if ok)
    print(f"\n  --- {passed}/{len(res)} passed (16 -> 24 -> {passed}) ---")
    for name, ok, detail in res:
        if not ok: print(f"    [FAIL] {name:42s} {detail}")
    print(f"\n  FINAL SCORE: {passed}/{len(res)}", flush=True)

if __name__ == "__main__":
    main()
