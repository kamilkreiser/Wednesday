# QA-AUDIT-HOST-NOTES-R2 item 6: the P-4 table's header, separator and rows of 52ad858 against the
# head, as RAW bytes (no whitespace collapsed), in order. Usage: python3 -B -I rawrows.py old.md new.md
import sys
def table(p):
    lines = open(p, "rb").read().split(b"\n")
    start = next(i for i, l in enumerate(lines) if l.strip().startswith(b"| Case | The answer |"))
    end = start
    while end < len(lines) and lines[end].strip().startswith(b"|"):
        end += 1
    return start, lines[start:end]
so, old = table(sys.argv[1]); sn, new = table(sys.argv[2])
print(f"old: table at line {so+1}, {len(old)} lines ({len(old)-2} rows); new: line {sn+1}, {len(new)} lines ({len(new)-2} rows)")
same = all(o == n for o, n in zip(old, new))
bad = [i + 1 for i, (o, n) in enumerate(zip(old, new)) if o != n]
print(f"the first {len(old)} lines byte-identical and in order: {same}; differing line indexes: {bad}")
for i, l in enumerate(new[len(old):]):
    print(f"added line {len(old)+i+1} (row {len(old)+i-1}): {l[:110].decode()}…")
