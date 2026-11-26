# Map each -U0 hunk of audit.rs (head side; base side for pure removals) to its enclosing item.
import re, subprocess, sys
C = sys.argv[1]; B="5e11609"; H="d79ae1c"; P="crates/coagent-daemon/src/audit.rs"
d = subprocess.run(["git","-C",C,"diff","-U0",B,H,"--",P],capture_output=True,check=True).stdout.decode()
def lines(sha): return subprocess.run(["git","-C",C,"show",f"{sha}:{P}"],capture_output=True,check=True).stdout.decode().split("\n")
hl, bl = lines(H), lines(B)
item = re.compile(r"^\s*(pub(\([a-z]+\))? )?(fn|struct|const|impl|enum)\s+([A-Za-z_][A-Za-z_0-9]*)?")
def enclosing(L, n):
    for i in range(n-1, -1, -1):
        m = item.match(L[i])
        if m and not L[i].lstrip().startswith("//"):
            # an item closed before n? (a top-level `}` between) -> report as "between items"
            return f"{m.group(3)} {m.group(4) or ''} (:{i+1})"
    return "top"
for h in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$", d, re.M):
    bs, bc, hs, hc = int(h[1]), int(h[2] or 1), int(h[3]), int(h[4] or 1)
    if hc: where = [enclosing(hl, n) for n in range(hs, hs+hc)]
    else: where = [enclosing(bl, bs)]
    first_line = hl[hs-1].strip()[:60] if hc else bl[bs-1].strip()[:60]
    print(f"-{bs},{bc} +{hs},{hc}: {sorted(set(where))} | {first_line}")
