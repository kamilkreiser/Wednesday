# QA-AUDIT-HOST-NOTES: (a) the differences base -> head as classes; (b) the head's fault classes with the
# docs' row each answer maps to. Usage: python3 -B -I classes.py base.log head.log
import sys, collections, re
sys.path.insert(0, "/private/tmp/claude-501/qahn/bin")
from compare import load, same, FIELDS
import importlib.util
spec = importlib.util.spec_from_file_location("table", "/private/tmp/claude-501/qahn/bin/table.py")
src = open("/private/tmp/claude-501/qahn/bin/table.py").read().replace("\nmain()\n", "\n")
tbl = {}; exec(compile(src, "table.py", "exec"), tbl)
row_of = tbl["row_of"]
base, _, _ = load(sys.argv[1]); head, _, seals = load(sys.argv[2])
def where(fl):
    return "+".join(sorted(set(re.sub(r"[#a-z]*#[#a-z0-9.\-]*", "", x.split(":")[0] + " " + x.split(":")[1].split("/")[0]) for x in fl.split("+")))) if fl else "none hit"
def landed(kind, b, f):
    b = b.strip("()").split(","); f = f.strip("()").split(",")
    if f == ["REFUSED"]: return "?"
    if kind in ("Record", "RecordFor"): return str(int(f[0]) == int(b[0]) + 1).lower()
    if kind == "Checkpoint": return str(int(f[1]) == int(b[1]) + 1).lower()
    if kind == "Receive": return str(int(f[4]) >= 2 and int(f[4]) > int(b[4])).lower()
    if kind == "Seal": return str(int(f[2]) == int(b[2]) + 1).lower()
    return "-"
print("(a) DIFFERENCES")
print("| Operation | Where it failed (head; most frequent) | Old answer | New answer | Fresh open landed old → new | Other fields that differ | n | Item | Judgement |")
print("|---|---|---|---|---|---|---|---|---|")
g = collections.OrderedDict()
for k in base:
    if k in head and not same(base[k], head[k]):
        b, h = base[k], head[k]
        fs = tuple(f for f in FIELDS if f not in ("short", "detail") and b.get(f) != h.get(f))
        key = (b["short"], h["short"], fs)
        e = g.setdefault(key, [0, collections.Counter(), collections.Counter(), 0, collections.Counter()])
        e[0] += 1; e[1][where(h.get("failed", ""))] += 1
        e[2][f'{landed("Seal", b["before"], b["fresh"])} → {landed("Seal", h["before"], h["fresh"])}'] += 1
        e[3] += int(h.get("problems", "0")) + int(b.get("problems", "0"))
        row, dec = row_of("Seal", h["short"], h["detail"], h["member"], seals.get(k))
        e[4][str(row)] += 1
for (bo, ho, fs), (n, w, fl, pr, rows) in sorted(g.items(), key=lambda x: -x[1][0]):
    ws = "; ".join(f"{a} x{c}" for a, c in w.most_common(2))
    print(f"| Seal | {ws} | {bo} | {ho} | {', '.join(f'{a} x{c}' for a,c in fl.items())} | {', '.join(fs) or '-'} | {n} | 5 (N-d) | harness problems {pr}; head answer's table row {dict(rows)} |")
print()
print("(b) HEAD FAULT CLASSES")
print("| Operation | Where it failed (most frequent) | Answer | Member | Fresh open: landed | Caller's retry | Docs row | n |")
print("|---|---|---|---|---|---|---|---|")
c = collections.OrderedDict()
for k, r in sorted(head.items(), key=lambda x: x[1]["kind"]):
    row, dec = row_of(r["kind"], r["short"], r["detail"], r["member"], seals.get(k))
    rk = r["retry"] if r["retry"] == "-" else "retry " + r["retry"]
    key = (r["kind"], r["short"], r["member"], landed(r["kind"], r["before"], r["fresh"]), rk, str(row) if row is not None else "NONE")
    e = c.setdefault(key, [0, collections.Counter()]); e[0] += 1; e[1][where(r.get("failed", ""))] += 1
for (kind, sh, mem, fl, rk, row), (n, w) in c.items():
    print(f"| {kind} | {'; '.join(f'{a} x{b}' for a,b in w.most_common(3))} | {sh} | {mem} | {fl} | {rk} | {row} | {n} |")
