#!/usr/bin/env python3
"""tdz_inline.py <test-section.diff> <out.diff> — inline file-scope string constants used inside vi.hoisted() blocks.

WHY (2026-09-15, KS-1050 ×2 and KS-1018 ×3): the model declares `const SEED_USER_ID = '…';` at file scope and reads
it inside `vi.hoisted(() => ({ … }))`. vitest lifts the hoisted block above every declaration, so the file dies with
`Cannot access 'SEED_USER_ID' before initialization` before a single test runs — five runs today, three of them AFTER
the rule was written into task.md and the brief. A rule the model cannot obey is repaired by the harness where the
repair is mechanical: for every `const NAME = '<string literal>';` in the new test file, every bare `NAME` token inside
a `vi.hoisted(` … `)` span is replaced by the literal. Nothing else is touched; the note names every replacement.
Exit 0 always; prints `inlined N` (N=0 means the section is byte-identical).
"""
import re
import sys

sec = open(sys.argv[1], encoding="utf-8").read().split("\n")
# the '+' lines of the new file, as text (keep index mapping)
consts = {}
for ln in sec:
    m = re.match(r"^\+\s*(?:export\s+)?const\s+([A-Z][A-Z0-9_]*)\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")\s*;?\s*(?://.*)?$", ln)
    if m:
        consts[m.group(1)] = m.group(2)
if not consts:
    open(sys.argv[2], "w", encoding="utf-8").write("\n".join(sec)); print("inlined 0 (no file-scope string constants)"); sys.exit(0)

out = []; depth = 0; in_hoisted = False; n = 0; notes = []
for i, ln in enumerate(sec):
    body = ln[1:] if ln.startswith("+") else None
    if body is None:
        out.append(ln); continue
    if not in_hoisted and "vi.hoisted(" in body:
        in_hoisted = True
        depth = 0
        # count parens from the call onward
        start = body.index("vi.hoisted(") + len("vi.hoisted")
        seg = body[start:]
    else:
        seg = body
    if in_hoisted:
        new = body
        for name, lit in consts.items():
            # never touch the declaration line itself
            if re.match(r"^\s*(?:export\s+)?const\s+" + name + r"\s*=", body):
                continue
            if re.search(r"(?<![\w$.])" + name + r"(?![\w$])", body):
                new = re.sub(r"(?<![\w$.])" + name + r"(?![\w$])", lit, new)
        if new != body:
            n += 1; notes.append(f"line {i+1}: {body.strip()[:70]!r} -> literal(s) inlined")
        out.append("+" + new)
        depth += seg.count("(") - seg.count(")")
        if depth <= 0:
            in_hoisted = False
    else:
        out.append(ln)
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
for x in notes:
    print(x)
print(f"inlined {n}")
