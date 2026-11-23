#!/usr/bin/env python3
r"""R2: can a wrap split the doubled backslash of literal text `\\u{1b}` so the next row shows `\u{1b}` (what a REAL
escaped ESC looks like)? Real hook, real viewer. usage: python3 -B bsplit.py <bin dir> <root (new, short)> <out dir>"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "forge2.py")).read().split("\ndef main():")[0])
d = start("h"); v = viewer(d, "bs"); time.sleep(0.8)
expect = []
def decide(label, e, payload=None):
    hook(d, e); expect.append(label)
# literal text: backslash, u, {, 1, b, } ; shown by the gate as \\u{1b}. Aim the SECOND backslash at column 6
# (right after the mark): needle = "\u{1b}ZZ" with ONE backslash.
def build(k):
    return "echo " + "." * k + "\\u{1b}ZZ literal text, no ESC", "\\u{1b}ZZ"
def esc(c): return c.replace("\\", "\\\\")
hit = False; k = 0
for t in range(6):
    cmd, nd = build(k); decide("split", ev("Bash", {"command": cmd}))
    lines, _ = all_lines(d); e = render(lines[-1])
    for k2 in range(0, 300):
        c2, _ = build(k2); e2 = e.replace(esc(cmd), esc(c2))
        ok = any(r.startswith(MARK + nd) for r in wrap(e2))
        if ok: break
    if any(r.startswith(MARK + nd) for r in wrap(e)):
        hit = True; break
    k = k2
time.sleep(1.2); v.terminate(); v.wait()
rows = open(os.path.join(OUTD, "bs.out")).read().split("\n")
for i, r in enumerate(rows):
    if r.startswith(MARK + "\\u{1b}ZZ"):
        print("aimed:", hit); print("  row:", repr(rows[i - 1][-20:])); print("  row:", repr(r[:40]))
        break
else:
    print("aimed:", hit, "(not found)")
lines, _ = all_lines(d)
print("daemon's reason holds the doubled form:", "\\\\u{1b}ZZ" in lines[-1]["reason"], "| a real ESC escape would read:", repr("\\u{1b}"))
procs.pop("h").terminate()
