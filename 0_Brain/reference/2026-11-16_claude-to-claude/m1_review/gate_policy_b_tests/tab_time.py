# QA-POLICY-B item 5: timing tables from time_drive.py outputs. usage: python3 -B -I tab_time.py <rows_time.jsonl> <tsv> [<tsv> ...]
import json, sys
ids = [json.loads(l)["id"] for l in open(sys.argv[1])]
for p in sys.argv[2:]:
    head = [l for l in open(p) if l.startswith("#")]
    rows = [l.rstrip("\n").split("\t") for l in open(p) if not l.startswith("#")]
    print(f"== {p}\n   {head[0].strip()}\n   {head[-1].strip()}")
    for lst in sorted({r[1] for r in rows}):
        R = [r for r in rows if r[1] == lst]
        d = sorted(R, key=lambda r: -float(r[4]))
        over = [r for r in R if float(r[4]) > 60]
        xs = max(R, key=lambda r: int(r[2])); ys = max(R, key=lambda r: int(r[3]))
        adm_x = [r for r in R if "L" not in r[5].split()]; adm_y = [r for r in R if "L" not in r[6].split()]
        sx = max(adm_x, key=lambda r: int(r[2])) if adm_x else None; sy = max(adm_y, key=lambda r: int(r[3])) if adm_y else None
        print(f"   list {lst}: rows {len(R)}; cells over +60 ms: {len(over)}; largest increase {d[0][4]} ms ({ids[int(d[0][0])]}: {int(d[0][2])/1000:.1f} -> {int(d[0][3])/1000:.1f}); largest decrease {d[-1][4]} ms ({ids[int(d[-1][0])]})")
        if sx: print(f"      slowest admitted X: {int(sx[2])/1000:.1f} ms {ids[int(sx[0])]} [{sx[5]}]")
        if sy: print(f"      slowest admitted Y: {int(sy[3])/1000:.1f} ms {ids[int(sy[0])]} [{sy[6]}]")
        for r in over[:12]: print(f"      OVER +60: {ids[int(r[0])]} {int(r[2])/1000:.1f} -> {int(r[3])/1000:.1f} ({r[4]}) [{r[5]}] -> [{r[6]}]")
        absd = sorted(abs(float(r[4])) for r in R)
        print(f"      |difference| median {absd[len(absd)//2]:.1f} ms, 99th pct {absd[int(len(absd)*0.99)]:.1f} ms, max {absd[-1]:.1f} ms")
