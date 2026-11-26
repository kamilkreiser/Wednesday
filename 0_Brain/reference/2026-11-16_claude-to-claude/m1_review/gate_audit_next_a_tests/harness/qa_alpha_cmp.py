# (b2): every item (fn/struct/impl/static/const) in an_after.rs lines 47-317 vs the same item in aw_answers.rs (both at the head)
import re, subprocess, sys
C = sys.argv[1]; H = "d79ae1c"
def src(p): return subprocess.run(["git","-C",C,"show",f"{H}:crates/coagent-daemon/tests/{p}"],capture_output=True,check=True).stdout.decode()
an, aw = src("an_after.rs"), src("aw_answers.rs")
seg = "\n".join(an.split("\n")[46:317])
def items(s):
    # top-level items: start at a column-0 line that begins an item (with preceding doc/attr lines), end at the next such start
    lines = s.split("\n"); out = {}; cur = None; buf = []
    start = re.compile(r"^(pub )?(fn|struct|impl|static|const|enum)\s+([A-Za-z_0-9<>]+)")
    pend = []
    for l in lines:
        m = start.match(l)
        if m:
            if cur: out[cur] = "\n".join(buf).rstrip()
            cur = f"{m.group(2)} {re.sub(r'<.*','',m.group(3))}"; buf = pend + [l]; pend = []
        elif l.startswith(("///", "#[")) and (not buf or buf[-1].strip() in ("}", "") or cur is None):
            pend.append(l)
        else:
            if pend: buf += pend; pend = []
            buf.append(l)
    if cur: out[cur] = "\n".join(buf).rstrip()
    return out
A, W = items(seg), items(aw)
same = diff = 0
for k, v in A.items():
    w = W.get(k)
    if w is None: print("NOT IN aw_answers:", k); diff += 1; continue
    # compare up to the end of the item's closing brace
    def cut(x):
        ls = x.split("\n"); 
        for i in range(len(ls)-1, -1, -1):
            if ls[i].startswith("}") or ls[i].endswith(";"): return "\n".join(ls[:i+1])
        return x
    if cut(v) == cut(w): same += 1
    else:
        diff += 1; print("DIFF:", k)
        import difflib
        for d in difflib.unified_diff(cut(w).split("\n"), cut(v).split("\n"), "aw_answers", "an_after", lineterm="", n=0): print("   ", d)
print(f"items in an_after 47-317: {len(A)}; byte-identical {same}; different or missing {diff}")
print("items:", ", ".join(A))
