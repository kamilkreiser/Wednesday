#!/usr/bin/env python3
"""Complex coding task -> Spark model -> execute + verify against a hidden suite."""
import json, time, urllib.request, traceback

BASE  = "http://127.0.0.1:8888/v1"
MODEL = "deepseek-v4-flash-0731"

TASK = '''Implement a spreadsheet formula engine in pure Python (standard library only).

Define exactly these public names at module level:

    class CircularReference(Exception): pass
    class FormulaError(Exception): pass

    class Sheet:
        def set_cell(self, ref: str, content) -> None: ...
        def get_value(self, ref: str) -> float: ...

SPECIFICATION

1. `set_cell(ref, content)`: `ref` is a cell reference like "A1", "B12", "AA3"
   (column letters are case-insensitive, one or more; row is a positive integer).
   `content` is either a number (int/float) or a string.
   A string beginning with "=" is a FORMULA. Any other string is a literal
   that should be stored and treated as 0 when used numerically.

2. `get_value(ref)` returns a float. A cell never set, or set to empty string,
   evaluates to 0.0.

3. Formula grammar (after the leading "="):
   - Binary operators + - * / with standard precedence (* and / bind tighter
     than + and -), left-associative.
   - Parentheses for grouping.
   - Unary minus, e.g. =-5+3 is -2.
   - Numeric literals, integer or decimal.
   - Cell references, e.g. =A1*2.
   - Range functions over a RECTANGULAR block: SUM, MIN, MAX, AVG.
     Written as SUM(A1:B3). Function names are case-insensitive.
     AVG is the arithmetic mean of every cell in the block.
     The range endpoints may be given in any corner order, e.g. B3:A1
     must mean the same block as A1:B3.
   - Arbitrary nesting, e.g. =SUM(A1:A2)*MAX(B1:B2) + (3 - -2).

4. Column letters work like spreadsheets: A..Z, then AA, AB, ... Multi-letter
   columns MUST work.

5. A formula that depends on itself, directly or through a chain of other
   cells, must raise `CircularReference` when `get_value` is called on it.

6. Division by zero must raise `FormulaError`. A malformed formula must also
   raise `FormulaError`.

7. Results must be cached so repeated `get_value` calls do not recompute, BUT
   the cache must be invalidated correctly when any cell is changed with
   `set_cell` — including cells that the changed cell is depended upon by,
   transitively.

Output ONLY the Python module source. No markdown fences, no commentary.
'''


def ask(prompt, max_tokens, thinking):
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "max_tokens": max_tokens, "temperature": 0.0,
               "chat_template_kwargs": {"thinking": thinking}}
    req = urllib.request.Request(BASE + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    body = json.loads(urllib.request.urlopen(req, timeout=3600).read().decode())
    dt = time.time() - t0
    ch = body["choices"][0]; msg = ch["message"]
    text = msg.get("content") or msg.get("reasoning_content") or msg.get("reasoning") or ""
    return text, ch["finish_reason"], body["usage"], dt


def strip_fences(code):
    if "```" in code:
        parts = code.split("```")
        # take the largest fenced block
        cand = max((p for i, p in enumerate(parts) if i % 2 == 1), key=len, default=code)
        code = cand
        if code.lstrip().lower().startswith("python"):
            code = code.lstrip()[6:]
    return code


# ----------------------------------------------------------------- test suite
def run_tests(ns):
    Sheet = ns["Sheet"]; Circ = ns["CircularReference"]; FErr = ns["FormulaError"]
    results = []

    def check(name, fn, expect):
        try:
            got = fn()
            ok = (abs(got - expect) < 1e-9) if isinstance(expect, (int, float)) else (got == expect)
            results.append((name, ok, f"got {got!r}, expected {expect!r}"))
        except Exception as e:
            results.append((name, False, f"raised {type(e).__name__}: {e}"))

    def check_raises(name, fn, exc):
        try:
            got = fn()
            results.append((name, False, f"returned {got!r}, expected {exc.__name__}"))
        except exc:
            results.append((name, True, f"raised {exc.__name__}"))
        except Exception as e:
            results.append((name, False, f"raised {type(e).__name__}: {e}, expected {exc.__name__}"))

    s = Sheet()
    s.set_cell("A1", 5)
    check("literal number", lambda: s.get_value("A1"), 5)

    s.set_cell("B1", "=2+3*4")
    check("precedence 2+3*4", lambda: s.get_value("B1"), 14)

    s.set_cell("B2", "=(2+3)*4")
    check("parentheses (2+3)*4", lambda: s.get_value("B2"), 20)

    s.set_cell("B3", "=-5+3")
    check("unary minus -5+3", lambda: s.get_value("B3"), -2)

    s.set_cell("B4", "=3 - -2")
    check("binary minus then unary 3--2", lambda: s.get_value("B4"), 5)

    s.set_cell("C1", "=A1*2")
    check("cell reference A1*2", lambda: s.get_value("C1"), 10)

    s.set_cell("D1", 1); s.set_cell("D2", "=D1+1"); s.set_cell("D3", "=D2+1")
    check("transitive chain", lambda: s.get_value("D3"), 3)

    check("unset cell is 0", lambda: s.get_value("Z9"), 0)
    s.set_cell("E1", "=Z9+5")
    check("formula over unset cell", lambda: s.get_value("E1"), 5)

    t = Sheet()
    for i, v in enumerate([1, 2, 3], start=1):
        t.set_cell(f"A{i}", v)
    t.set_cell("C1", "=SUM(A1:A3)")
    check("SUM column range", lambda: t.get_value("C1"), 6)

    u = Sheet()
    u.set_cell("A1", 1); u.set_cell("B1", 2); u.set_cell("A2", 3); u.set_cell("B2", 4)
    u.set_cell("D1", "=SUM(A1:B2)")
    check("SUM rectangular block", lambda: u.get_value("D1"), 10)
    u.set_cell("D2", "=MIN(A1:B2)")
    check("MIN block", lambda: u.get_value("D2"), 1)
    u.set_cell("D3", "=MAX(A1:B2)")
    check("MAX block", lambda: u.get_value("D3"), 4)
    u.set_cell("D4", "=AVG(A1:B2)")
    check("AVG block", lambda: u.get_value("D4"), 2.5)
    u.set_cell("D5", "=SUM(B2:A1)")
    check("reversed-corner range B2:A1", lambda: u.get_value("D5"), 10)
    u.set_cell("D6", "=sum(a1:b2)")
    check("case-insensitive fn + refs", lambda: u.get_value("D6"), 10)

    v = Sheet()
    v.set_cell("AA1", 7)
    v.set_cell("AB1", "=AA1*2")
    check("multi-letter column AA1", lambda: v.get_value("AB1"), 14)

    w = Sheet()
    w.set_cell("A1", 2); w.set_cell("A2", 3); w.set_cell("B1", 4); w.set_cell("B2", 5)
    w.set_cell("C1", "=SUM(A1:A2)*MAX(B1:B2) + (3 - -2)")
    check("nested fns + arithmetic", lambda: w.get_value("C1"), 30)

    x = Sheet()
    x.set_cell("A1", "=B1"); x.set_cell("B1", "=A1")
    check_raises("mutual circular ref", lambda: x.get_value("A1"), Circ)
    y = Sheet(); y.set_cell("A1", "=A1")
    check_raises("self circular ref", lambda: y.get_value("A1"), Circ)
    y2 = Sheet()
    y2.set_cell("A1", "=B1"); y2.set_cell("B1", "=C1"); y2.set_cell("C1", "=A1")
    check_raises("3-cell circular chain", lambda: y2.get_value("A1"), Circ)

    z = Sheet(); z.set_cell("A1", "=1/0")
    check_raises("division by zero", lambda: z.get_value("A1"), FErr)
    z2 = Sheet(); z2.set_cell("A1", "=2+*3")
    check_raises("malformed formula", lambda: z2.get_value("A1"), FErr)

    c = Sheet()
    c.set_cell("A1", 1); c.set_cell("B1", "=A1*10")
    first = c.get_value("B1")
    c.set_cell("A1", 5)
    check("cache invalidation on dependency change",
          lambda: c.get_value("B1"), 50)
    results.append(("cache warm read before change", abs(first - 10) < 1e-9, f"got {first}"))

    c2 = Sheet()
    c2.set_cell("A1", 1); c2.set_cell("B1", "=A1+1"); c2.set_cell("C1", "=B1+1")
    c2.get_value("C1")
    c2.set_cell("A1", 10)
    check("transitive cache invalidation", lambda: c2.get_value("C1"), 12)

    return results


def main():
    for thinking, budget in ((False, 4096), (True, 16384)):
        label = "THINKING ON" if thinking else "THINKING OFF"
        print(f"\n{'='*70}\n=== ATTEMPT: {label} (max_tokens={budget})\n{'='*70}", flush=True)
        try:
            text, finish, usage, dt = ask(TASK, budget, thinking)
        except Exception as e:
            print(f"  request failed: {e!r}"); continue
        print(f"  finish_reason={finish}  completion_tokens={usage['completion_tokens']}  "
              f"prompt_tokens={usage['prompt_tokens']}  wall={dt:.1f}s  "
              f"({usage['completion_tokens']/dt:.1f} tok/s)", flush=True)
        if finish == "length":
            print("  TRUNCATED - skipping execution"); continue
        code = strip_fences(text)
        open(f"/home/datasec-rd/spark-eval/generated_{'thinking' if thinking else 'plain'}.py",
             "w").write(code)
        ns = {}
        try:
            exec(compile(code, "<generated>", "exec"), ns)
        except Exception:
            print("  MODULE FAILED TO IMPORT:"); traceback.print_exc(limit=3); continue
        missing = [n for n in ("Sheet", "CircularReference", "FormulaError") if n not in ns]
        if missing:
            print(f"  MISSING REQUIRED NAMES: {missing}"); continue
        try:
            res = run_tests(ns)
        except Exception:
            print("  SUITE CRASHED:"); traceback.print_exc(limit=3); continue
        passed = sum(1 for _, ok, _ in res if ok)
        print(f"\n  --- {passed}/{len(res)} tests passed ---")
        for name, ok, detail in res:
            print(f"    [{'PASS' if ok else 'FAIL'}] {name:42s} {'' if ok else detail}")
        print(f"\n  SCORE ({label}): {passed}/{len(res)}", flush=True)


if __name__ == "__main__":
    main()
