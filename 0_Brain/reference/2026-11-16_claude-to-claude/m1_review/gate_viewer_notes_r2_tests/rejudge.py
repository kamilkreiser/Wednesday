"""Re-judge a vn2 run's recorded viewer output with the reader (m2.reader) without a new run.
usage: python3 -B rejudge.py <out dir of vn2>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2
D = sys.argv[1]
rec = json.load(open(os.path.join(D, "record.json")))
out = open(os.path.join(D, "viewer.out"), encoding="utf-8").read()
print("model == viewer:", m2.screen(rec["lines"]) == out)
groups, cur = [], None
for r in out.split("\n")[:-1][4:]:
    if r == m2.NOTICE: continue
    if re.match(r"^#\d+ ", r): cur = [r]; groups.append(cur)
    else: cur.append(r)
bad = 0
for lab, l, g in zip(rec["labels"], rec["lines"], groups):
    probs, flds = m2.reader(g)
    want = {"mode": "not reported" if not isinstance(l.get("mode"), str) else m2.field(l["mode"])}
    if l.get("event") == "PreToolUse" and isinstance(l.get("tool"), str): want["tool"] = m2.field(l["tool"])
    got = {f[0]: f[1] for f in flds}
    for k, v in want.items():
        if got.get(k) != v: probs.append(f"{k} read {got.get(k)!r} != sent {v!r}")
    if probs:
        bad += 1; print(f"#{l['seq']} [{lab}] {probs}\n   " + "\n   ".join(g))
print(f"entries {len(groups)}, with a reader problem: {bad}")
