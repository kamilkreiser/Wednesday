"""Rows AFTER the mode field (the gate's reason, continuation rows) that end with ' >>' or ' |', or that start
(after the mark) like a field: 'Claude Code mode: ' / 'tool '. A naive join that strips every row-final ' >>'
is compared with the render. usage: python3 -B reason_rows.py <vn2 out dir>"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import m2
D = sys.argv[1]
rec = json.load(open(D + '/record.json')); out = open(D + '/viewer.out').read()
groups, cur = [], None
for r in out.split('\n')[:-1][4:]:
    if r == m2.NOTICE: continue
    if re.match(r'^#\d+ ', r): cur = [r]; groups.append(cur)
    else: cur.append(r)
cnt = {"cut": 0, "bar": 0, "modefield": 0, "naive": 0}; shown = {"cut": 0, "bar": 0, "modefield": 0}
for lab, l, g in zip(rec['labels'], rec['lines'], groups):
    probs, flds = m2.reader(g)
    mrow = [f for f in flds if f[0] == 'mode'][0][2]
    for k, r in enumerate(g):
        if k <= mrow: continue
        body = r[6:]
        kinds = []
        if k < len(g) - 1 and r.endswith(' >>'): kinds.append("cut")
        if r.endswith(' |'): kinds.append("bar")
        if body.startswith('Claude Code mode: ') or body.startswith('tool '): kinds.append("modefield")
        for kd in kinds:
            cnt[kd] += 1
            if shown[kd] < 2:
                shown[kd] += 1
                print(f"[{kd}] #{l['seq']} [{lab}]:\n   " + "\n   ".join(g[:k + 2]))
    naive = "".join([g[0][:-3] if g[0].endswith(' >>') else g[0]] + [(r[6:-3] if (r.endswith(' >>') and i < len(g) - 2) else r[6:]) for i, r in enumerate(g[1:])])
    if naive != m2.render(l):
        cnt["naive"] += 1
print("reason rows ending ' >>':", cnt["cut"], "| ending ' |':", cnt["bar"], "| starting like a field after the mark:", cnt["modefield"],
      "| entries where stripping EVERY row-final ' >>' drops text:", cnt["naive"])
