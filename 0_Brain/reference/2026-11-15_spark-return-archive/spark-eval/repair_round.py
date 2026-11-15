#!/usr/bin/env python3
"""Round 2: feed the model its own failures and ask it to repair. Agentic loop test."""
import json, time, urllib.request, traceback, sys
sys.path.insert(0, "/home/datasec-rd/spark-eval")
from complex_task import TASK, ask, strip_fences, run_tests

PRIOR = open("/home/datasec-rd/spark-eval/generated_plain.py").read()

FEEDBACK = '''Your previous implementation of this task scored 16/26 on a hidden test suite.

ORIGINAL TASK
-------------
''' + TASK + '''

YOUR PREVIOUS IMPLEMENTATION
----------------------------
''' + PRIOR + '''

TEST FAILURES
-------------
1. Every range test fails with: FormulaError: Unexpected character: :
   Your tokenizer does not handle the ':' character, so range functions
   SUM(A1:A3), MIN(A1:B2), MAX(A1:B2), AVG(A1:B2) cannot parse at all.
   Failing cases:
     SUM(A1:A3) over A1=1,A2=2,A3=3          should be 6
     SUM(A1:B2) over A1=1,B1=2,A2=3,B2=4     should be 10
     MIN(A1:B2) same data                     should be 1
     MAX(A1:B2) same data                     should be 4
     AVG(A1:B2) same data                     should be 2.5
     SUM(B2:A1) reversed corners, same data   should be 10
     sum(a1:b2) lowercase                     should be 10
     SUM(A1:A2)*MAX(B1:B2) + (3 - -2)         should be 30

2. Cache invalidation is broken. You cache results but never invalidate them.
   Failing cases:
     set A1=1; set B1="=A1*10"; get B1 -> 10; then set A1=5; get B1
       returned 10, should be 50
     set A1=1, B1="=A1+1", C1="=B1+1"; get C1; then set A1=10; get C1
       returned 3, should be 12
   Any set_cell must invalidate the cached value of every cell that transitively
   depends on the changed cell.

Rewrite the COMPLETE module fixing both problems. Keep everything that already
works: precedence, parentheses, unary minus, cell references, multi-letter
columns, circular reference detection, division-by-zero and malformed-formula
errors.

Output ONLY the Python module source. No markdown fences, no commentary.
'''

def main():
    print("=== REPAIR ROUND (thinking off, max_tokens=6144) ===", flush=True)
    print(f"  feedback prompt chars: {len(FEEDBACK)}", flush=True)
    text, finish, usage, dt = ask(FEEDBACK, 6144, False)
    print(f"  finish_reason={finish}  completion={usage['completion_tokens']}  "
          f"prompt={usage['prompt_tokens']}  wall={dt:.1f}s  "
          f"({usage['completion_tokens']/dt:.1f} tok/s)", flush=True)
    if finish == "length":
        print("  TRUNCATED"); return
    code = strip_fences(text)
    open("/home/datasec-rd/spark-eval/generated_repaired.py", "w").write(code)
    ns = {}
    try:
        exec(compile(code, "<repaired>", "exec"), ns)
    except Exception:
        print("  MODULE FAILED TO IMPORT:"); traceback.print_exc(limit=3); return
    missing = [n for n in ("Sheet", "CircularReference", "FormulaError") if n not in ns]
    if missing:
        print(f"  MISSING NAMES: {missing}"); return
    try:
        res = run_tests(ns)
    except Exception:
        print("  SUITE CRASHED:"); traceback.print_exc(limit=3); return
    passed = sum(1 for _, ok, _ in res if ok)
    print(f"\n  --- {passed}/{len(res)} tests passed (was 16/26) ---")
    for name, ok, detail in res:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name:42s} {'' if ok else detail}")
    print(f"\n  REPAIR SCORE: {passed}/{len(res)}", flush=True)

if __name__ == "__main__":
    main()
