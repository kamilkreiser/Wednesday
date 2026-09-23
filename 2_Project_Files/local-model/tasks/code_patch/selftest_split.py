#!/usr/bin/env python3
"""selftest_split.py <section.diff> <test_hunks e.g. "2" or "2,3"> <out.test.diff> <out.prod.diff> [input.json]

code_patch SELF-TESTING mode (2026-09-23, IMPROVEMENTS 14:23 + 14:24 rows; KS-1143 is the first case): the
product file IS a test file, so the fix and the cell that pins it land in ONE file, as separate hunks. The
checker cannot sequence red-first by FILE, so it sequences by HUNK: the hunks the brief declares as TEST
(`## Self-testing — test hunks: N`, 1-based ordinals in the section as applied) go into <out.test.diff>,
applied ALONE at the tip for A4 (must go RED); every other hunk goes into <out.prod.diff>, applied on top
for A5 (must go GREEN). Both halves carry the section's file headers unchanged.

The section given is the one the checker will APPLY (line 1 of section_<k>.opts — it may be a REANCHORED,
CONTEXT-WS or TDZ/DECL rebuilt copy), so the ordinals index the hunks that will really be applied.

REFUSES (rc 2, reason on stdout) — never guesses:
  - a declared ordinal outside 1..N (N = hunks in the section);
  - the split leaves either half with NO hunk (nothing to red, or nothing that fixes);
  - [input.json given] a declared red cell (defect_line.red_cells) is NOT named on a '+' line of the TEST half,
    or IS named on a '+' line of the PROD half — the ordinals point at the wrong hunk (the model may order
    hunks differently from the brief), and splitting by a wrong ordinal would grade the fix as the test.
rc 0 ok (one summary line) · 2 refused · 1 usage/IO error.
"""
import json
import re
import sys


def main() -> int:
    if len(sys.argv) not in (5, 6):
        print(__doc__.split("\n")[0])
        return 1
    sec_path, ords_s, out_test, out_prod = sys.argv[1:5]
    inp = sys.argv[5] if len(sys.argv) == 6 else None
    try:
        ords = sorted({int(x) for x in re.split(r"[,\s]+", ords_s.strip()) if x})
    except ValueError:
        print(f"REFUSED: test hunk ordinals {ords_s!r} are not integers")
        return 2
    lines = open(sec_path, encoding="utf-8").read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    first = next((i for i, l in enumerate(lines) if l.startswith("@@ ")), None)
    if first is None:
        print("REFUSED: the section carries no @@ hunk")
        return 2
    header = lines[:first]
    hunks, cur = [], None
    for l in lines[first:]:
        if l.startswith("@@ "):
            cur = [l]
            hunks.append(cur)
        else:
            cur.append(l)
    n = len(hunks)
    bad = [k for k in ords if k < 1 or k > n]
    if not ords or bad:
        print(f"REFUSED: declared test hunk(s) {ords} but the section has {n} hunk(s) — out of range: {bad or 'none declared'}")
        return 2
    test = [h for i, h in enumerate(hunks, 1) if i in ords]
    prod = [h for i, h in enumerate(hunks, 1) if i not in ords]
    if not prod:
        print(f"REFUSED: every hunk ({n}) is declared TEST — no product hunk is left to turn the red green")
        return 2
    if inp:
        cells = ((json.load(open(inp, encoding="utf-8")).get("defect_line") or {}).get("red_cells")) or []
        plus = lambda hs: "\n".join(l[1:] for h in hs for l in h[1:] if l.startswith("+"))
        tp, pp = plus(test), plus(prod)
        miss = [c for c in cells if c and c not in tp]
        wrong = [c for c in cells if c and c in pp]
        if miss or wrong:
            print(f"REFUSED: the declared red cell(s) do not sit in the declared TEST hunk(s) {ords} of {n} — "
                  f"absent from the test half: {miss} · present in the prod half: {wrong} — the ordinals point at "
                  f"the wrong hunk (the model's hunk order differs from the brief's)")
            return 2
    with open(out_test, "w", encoding="utf-8") as f:
        f.write("\n".join(header + [l for h in test for l in h]) + "\n")
    with open(out_prod, "w", encoding="utf-8") as f:
        f.write("\n".join(header + [l for h in prod for l in h]) + "\n")
    print(f"split {n} hunk(s): TEST {ords} ({sum(len(h) for h in test)} lines) -> {out_test} · "
          f"PROD {[i for i in range(1, n + 1) if i not in ords]} ({sum(len(h) for h in prod)} lines) -> {out_prod}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
