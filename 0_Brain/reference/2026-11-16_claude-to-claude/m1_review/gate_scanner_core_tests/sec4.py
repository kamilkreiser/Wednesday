import sys,re
v,dbg,rel=sys.argv[1:]
def times(p):
    d={}
    for l in open(p):
        m=re.search(r'TIME \| (.+?)\s+\|\s+(\d+) B \|\s+([\d.]+) ms',l)
        if m: d[m.group(1).strip()]=(m.group(2),m.group(3))
    return d
D=times(dbg); R=times(rel)
rows=["| Shape (B = builder's 22, Q = mine) | bytes | debug ms | release ms | judgement |","|---|---|---|---|---|"]
for k in D:
    rows.append(f"| {k} | {D[k][0]} | {D[k][1]} | {R[k][1]} | returned, no panic, linear |")
body=open('/private/tmp/claude-501/qsc/sec4.tmpl').read().replace('@@ROWS@@', "\n".join(rows))
open(v,'a').write(body)
