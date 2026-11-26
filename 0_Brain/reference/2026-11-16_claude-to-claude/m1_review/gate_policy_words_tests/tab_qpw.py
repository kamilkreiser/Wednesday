# QA-POLICY-WORDS: tabulate probe outputs. python3 -B -I tab_qpw.py
import json, collections
O = "/private/tmp/claude-501/qpw/out/"
def load(tree, s, pl):
    L = [json.loads(l) for l in open(f"{O}{tree}_{s}_{pl}.jsonl")]
    meta = L[0]; rows = {(r["id"], r["st"]): r for r in L[1:]}
    return meta, rows
bad_nov = 0
print("== nov == decide, and place equality (tmp vs plain) per tree and set")
for tree in ("p184", "phead"):
    for s in ("cross", "free", "misc"):
        _, a = load(tree, s, "tmp"); _, b = load(tree, s, "plain")
        bad_nov += sum(not r["nov_eq_decide"] for r in list(a.values()) + list(b.values()))
        diff = [k for k in a if a[k]["cols"] != b[k]["cols"]]
        print(f"{tree} {s}: {len(a)} lines; differ between places: {len(diff)} {[ (k, a[k]['cols'], b[k]['cols']) for k in diff]}")
print("nov != decide lines:", bad_nov)
print("== crossings (nothing excluded): first N with L L L L; every N above it L?; below the head crossing head == 184b35e?")
res = {}
for pl in ("tmp", "plain"):
    _, h = load("phead", "cross", pl); _, b = load("p184", "cross", pl)
    for shape, top in [("author", 82), ("ab", 82), ("mail", 82), ("scp", 82), ("kv", 82), ("udir", 82), ("dom_echo", 161), ("dom_author", 161)]:
        def first(rows):
            f = next((n for n in range(1, top + 1) if rows[(f"x:{shape}:{n}", "o")]["cols"] == "L L L L"), None)
            above_ok = f is None or all(rows[(f"x:{shape}:{n}", "o")]["cols"] == "L L L L" for n in range(f, top + 1))
            return f, above_ok
        fh, okh = first(h); fb, okb = first(b)
        lim = fh or top + 1
        below_diff = [n for n in range(1, lim) if h[(f"x:{shape}:{n}", "o")]["cols"] != b[(f"x:{shape}:{n}", "o")]["cols"]]
        below_codes = sorted(set(h[(f"x:{shape}:{n}", "o")]["cols"] for n in range(1, lim)))
        def rowtxt(rows, n):
            if n < 1 or n > top: return "-"
            r = rows[(f"x:{shape}:{n}", "o")]; return f"{n}: {r['cols']} ({r['cmd_pieces'][0]} pieces)"
        print(f"[{pl}] {shape}: head first L = {fh} (all above L: {okh}); 184b35e first L = {fb} (all above L: {okb}); "
              f"below head crossing: codes {below_codes}, head!=184 at {below_diff}")
        print(f"      head  {rowtxt(h, fh-1 if fh else top)} | {rowtxt(h, fh) if fh else 'not crossed'}")
        print(f"      184   {rowtxt(b, (fh-1) if fh else top)} | {rowtxt(b, fh) if fh else '-'} || 184 own: {rowtxt(b, fb-1 if fb else top)} | {rowtxt(b, fb) if fb else 'not crossed at %d' % top}")
        res[(pl, shape)] = (fh, fb)
print("same figures in both places:", all(res[("tmp", s)] == res[("plain", s)] for (_, s) in res))
print("== free text, **/.env* excluded: last n X X X X (env piece position) / first n not checked")
for pl in ("tmp", "plain"):
    _, h = load("phead", "free", pl); _, b = load("p184", "free", pl)
    for tool in ("WebSearch", "Agent"):
        for k, top in (("plain", 165), ("kv", 85), ("colon", 85), ("comma", 85)):
            def cut(rows):
                xs = [n for n in range(1, top + 1) if rows[(f"f:{tool}:{k}:{n}", "e")]["cols"] == "X X X X"]
                last = max(xs); mono = xs == list(range(1, last + 1))
                return last, mono
            lh, mh = cut(h); lb, mb = cut(b)
            r1, r2 = h[(f"f:{tool}:{k}:{lh}", "e")], h[(f"f:{tool}:{k}:{lh+1}", "e")]
            q1, q2 = b[(f"f:{tool}:{k}:{lh}", "e")], b[(f"f:{tool}:{k}:{lh+1}", "e")]
            same = all(h[(f"f:{tool}:{k}:{n}", "e")]["cols"] == b[(f"f:{tool}:{k}:{n}", "e")]["cols"] for n in range(1, top + 1))
            print(f"[{pl}] {tool} {k}: head last checked {lh} (monotone {mh}) / 184 {lb} (monotone {mb}); head==184 every n: {same}")
            print(f"      head n={lh}: {r1['cols']} intext={r1['intext']} env_pos={r1['env_pos']} | n={lh+1}: {r2['cols']} intext={r2['intext']} env_pos={r2['env_pos']}")
            print(f"      184  n={lh}: {q1['cols']} intext={q1['intext']} env_pos={q1['env_pos']} | n={lh+1}: {q2['cols']} intext={q2['intext']} env_pos={q2['env_pos']}")
