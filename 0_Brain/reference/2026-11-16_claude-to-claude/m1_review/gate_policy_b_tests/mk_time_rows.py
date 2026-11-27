# QA-POLICY-B: timing rows. Every row of the builder's head-against-base table re-made from its description
# (STATUS A3.2 / A4.1 / §2: the t29 corpus kinds, the P-0 (4) families, the A-heavy and B-heavy shapes, the fifteen
# refused families; five tools), plus the check's own item 3 corpus (filled), the 64 KiB `@x ` command field and the
# million-word prompt. python3 -B mk_time_rows.py <rows dir>
import json, sys
D = sys.argv[1]
T5 = ["WebSearch", "Agent", "mcp__github__create_issue", "MadeUpTool", "WebFetch"]
rows = []
def add(rid, tool, text=None, inp=None):
    r = {"id": rid, "tool": tool}
    if inp is not None: r["input"] = inp
    else: r["text"] = text
    rows.append(r)
c1 = [json.loads(l) for l in open(f"{D}/rows_c1.jsonl")]
it = [json.loads(l) for l in open(f"{D}/rows_items.jsonl")]
for r in c1:
    if r["id"].startswith("t29corp:") or r["id"].startswith("fam:"):
        add("T:" + r["id"], r["tool"], r.get("text"), r.get("input"))
for r in it:
    if r["id"].startswith("ord:") and r["id"].endswith(":filled"):
        add("T:" + r["id"], r["tool"], r.get("text"), r.get("input"))
    if r["id"].startswith("ord:") and "distinct CJK" in r["id"] and r["id"].split(":")[1][0].isdigit():
        add("T:" + r["id"], r["tool"], r.get("text"), r.get("input"))
# P-0 (4) families (1 200-character windows), the builder's descriptions
def to1300(unit, sep=" "):
    s, i = "", 0
    while len(s) < 1300:
        if i: s += sep
        s += unit(i); i += 1
    return s
P04 = {
    "one-letter words": to1300(lambda i: "abcdefghijklmnopqrstuvwxyz"[i % 26]),
    "w<i> words": to1300(lambda i: f"w{i}"),
    "-/a/a/ option word": "-" + "/a" * 650,
    "-/~@a option word": "-" + "/~@a" * 330,
    "two -/~@a words": "-" + "/~@a" * 170 + " -" + "/~@b" * 160,
    "a@b@c": "@".join("abcdefghijklmnopqrstuvwxyz"[i % 26] for i in range(650)),
    "@a/@a/": "@a/" * 440,
    "quoted strings": to1300(lambda i: f"'q{i} x'"),
    "$'\\x2e<i>'": to1300(lambda i: f"$'\\x2e{i}'"),
    "-/~@a + $' copy": "-" + "/~@a" * 150 + " $'\\x2d" + "/~@b" * 140 + "'",
    "brace groups x<i>{a..h}": to1300(lambda i: f"x{i}{{a,b,c,d,e,f,g,h}}"),
    "-/@a/{1..8}": "-" + "/@a" * 380 + "{1,2,3,4,5,6,7,8}",
    "words -/a<i>/b/c{1..8}": to1300(lambda i: f"-/a{i}/b/c{{1,2,3,4,5,6,7,8}}"),
    "k<i>=v<i>": to1300(lambda i: f"k{i}=v{i}"),
    # A-heavy (scan A's cost, B light): the builder's A2.3 point 4 shapes
    "A-heavy: - then one /a x50 word repeated": "- " + " ".join(["/a" * 50] * 24),
    "A-heavy: - /a/a/a/a repeated": "- " + " ".join(["/a/a/a/a"] * 140),
    "A-heavy: - /a<i>/a/a/a words": "- " + " ".join(f"/a{i}/a/a/a" for i in range(120)),
    "A-heavy: - distinct deep words": "- " + " ".join(f"/d{i}/e/f/g/h/i/j/k" for i in range(70)),
    # B-heavy (through the web fetch prompt, which scan A does not read)
    "B-heavy: distinct short words": to1300(lambda i: f"x{i}"),
    "B-heavy: -/a/a at 0.4": "-" + "/a" * 240,
    "B-heavy: -/a/a at 0.5": "-" + "/a" * 300,
    "B-heavy: -/a/a at 0.7": "-" + "/a" * 420,
    "B-heavy: -//// at 0.4": "-" + "/" * 480,
    "B-heavy: /a<i>/b/c/d words": to1300(lambda i: f"/a{i}/b/c/d"),
}
for k, txt in P04.items():
    for t in T5:
        add(f"T:p04:{k}:{t}", t, txt)
add("T:64k @x command field", "MadeUpTool", inp={"command": "@x " * 21845})
add("T:64k @x Agent prompt", "Agent", "@x " * 21845)
add("T:million words Agent", "Agent", " ".join(f"w{i}" for i in range(1_000_000)))
with open(f"{D}/rows_time.jsonl", "w") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("time rows", len(rows))
