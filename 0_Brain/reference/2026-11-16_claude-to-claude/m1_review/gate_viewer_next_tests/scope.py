#!/usr/bin/env python3
"""QA-VIEWER-NEXT item 1: scope of 9145840...64c74ae against the brief's owned set, with controls."""
import re, subprocess, sys
R = "/private/tmp/claude-501/qvx/r"; B = "9145840f24f23aff5b589044ce8aa8776283bdac"; H = "64c74ae7bb01e644a688a7c7144576e591edc840"
def g(*a): return subprocess.run(["git", "-C", R, *a], capture_output=True, text=True, check=True).stdout
OWNED = re.compile(r"^(crates/coagent-daemon/src/watch\.rs|crates/coagent-daemon/tests/la_[^/]*\.rs|crates/coagent-daemon/tests/la_support/mod\.rs|crates/coagent-daemon/build\.rs|scripts/red-controls-daemon\.sh|docs/DAEMON\.md|BACKLOG\.md|docs/M0-OUTCOMES\.md)$")
def outside(names): return [n for n in names if not OWNED.match(n)]
names = g("diff", "--name-only", f"{B}...{H}").split()
print("lane paths:", len(names)); print("outside owned set:", outside(names))
ctrl = g("diff", "--name-only", "734cf6e", B).split()
print("CONTROL (main's own 734cf6e..9145840 paths):", len(ctrl), "outside owned set:", len(outside(ctrl)))
# blob-for-blob: every path at the base vs head that is not owned
def tree(c): return dict((l.split("\t")[1], l.split()[2]) for l in g("ls-tree", "-r", c).splitlines())
tb, th = tree(B), tree(H)
diff_unowned = [p for p in set(tb) | set(th) if tb.get(p) != th.get(p) and not OWNED.match(p)]
print("non-owned paths whose blob differs base->head:", diff_unowned)
for p in ["Cargo.toml", "Cargo.lock"] + [f"crates/coagent-daemon/src/{f}.rs" for f in "activity gate engine ipc main lib link relay_child invite datadir store recovery".split()]:
    print(f"  {p}: {'IDENTICAL' if tb.get(p) == th.get(p) else 'DIFFERS'} {tb.get(p,'-')[:10]} {th.get(p,'-')[:10]}")
tests = [p for p in tb if re.match(r"^crates/[^/]+/tests/", p) and not re.match(r"^crates/coagent-daemon/tests/la_", p)]
same = sum(1 for p in tests if tb[p] == th.get(p))
print(f"test files outside tests/la_*: {len(tests)} at base, identical at head: {same}")
print("Cargo.toml files changed:", [p for p in diff_unowned + names if p.endswith("Cargo.toml") or p.endswith("Cargo.lock")])
# appended-only check for BACKLOG.md and M0-OUTCOMES.md
for p in ["BACKLOG.md", "docs/M0-OUTCOMES.md", "crates/coagent-daemon/build.rs"]:
    d = g("diff", "-U0", f"{B}...{H}", "--", p)
    rem = [l for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    add = [l for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
    print(f"{p}: +{len(add)} -{len(rem)}; removed: {rem}")
    if p == "BACKLOG.md":
        for r in rem:
            print("   its replacement present:", ("+" + r[1:].replace("- [ ]", "- [x]", 1)) in add)
# lines of base kept in order in head (subsequence) for the two docs
for p in ["BACKLOG.md", "docs/M0-OUTCOMES.md"]:
    a = g("show", f"{B}:{p}").splitlines(); b = g("show", f"{H}:{p}").splitlines()
    i = 0
    for x in b:
        if i < len(a) and (x == a[i] or (x == a[i].replace("- [ ]", "- [x]", 1) and "N-3" in x)): i += 1
    print(f"{p}: base lines {len(a)}, matched in order {i}; head lines {len(b)}")
# DAEMON.md hunks inside section 8
dm = g("show", f"{H}:docs/DAEMON.md").splitlines()
s8 = [i + 1 for i, l in enumerate(dm) if re.match(r"^## 8\b", l)]; nxt = [i + 1 for i, l in enumerate(dm) if re.match(r"^## \d", l) and s8 and i + 1 > s8[0]]
print("DAEMON.md §8 starts at head line", s8, "next ## section after it:", nxt[:1], "head lines", len(dm))
for l in g("diff", "-U0", f"{B}...{H}", "--", "docs/DAEMON.md").splitlines():
    if l.startswith("@@"):
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", l); print("  hunk", l.split("@@")[1].strip(), "inside §8:", int(m.group(3)) >= s8[0] and int(m.group(1)) >= [i + 1 for i, x in enumerate(g('show', f'{B}:docs/DAEMON.md').splitlines()) if re.match(r'^## 8\b', x)][0])
add_all = [l for l in g("diff", "-U0", f"{B}...{H}").splitlines() if l.startswith("+") and not l.startswith("+++")]
print("added lines:", len(add_all), "with 'unsafe':", [l for l in add_all if re.search(r"\bunsafe\b", l)])
