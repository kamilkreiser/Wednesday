# QA-POLICY-AT: the differential's difference classes, both seeds, as markdown tables. usage: dist_tables.py cmp_s1.txt cmp_s2.txt
import re, sys
def parse(f):
    t = open(f).read()
    dist = re.search(r'--- distribution.*?\n(.*?)--- deny', t, re.S).group(1)
    d2d = re.search(r'--- deny -> other deny.*?\n(.*?)--- bound', t, re.S).group(1)
    bc = re.search(r'--- bound crossings.*?\n(.*?)--- per state', t, re.S).group(1)
    D, E = {}, {}
    for l in dist.strip().split('\n'):
        m = re.match(r'\s*(\d+)\s+(.*?)\s+->\s+(.*?)\s+\[([\w-]+)\]', l); D[(m.group(2), m.group(3), m.group(4))] = int(m.group(1))
    for l in d2d.strip().split('\n'):
        m = re.match(r'\s*(\d+)\s+(.*?)\s+->\s+(.*?)\s+\[([\w-]+)\]\s+e\.g\. (.*)', l)
        ex = re.match(r"\[\('([^']*)', '([^']*)', '([^']*)'", m.group(5))
        E[(m.group(2), m.group(3))] = (int(m.group(1)), ex.groups() if ex else ())
    return D, E, sum(int(l.split()[0]) for l in bc.strip().split('\n') if l.strip())
D1, E1, B1 = parse(sys.argv[1]); D2, E2, B2 = parse(sys.argv[2])
print("| base answer | head answer | verdict | cells seed 1 | cells seed 2 |"); print("|---|---|---|---|---|")
for k in sorted(set(D1) | set(D2), key=lambda k: -(D1.get(k, 0) + D2.get(k, 0))):
    if k[2] == 'DENY2DENY': continue
    print(f"| {k[0]} | {k[1]} | {k[2]} | {D1.get(k, 0)} | {D2.get(k, 0)} |")
print("\n| base deny | head deny | cells seed 1 | cells seed 2 | an example (row id, state, column) |"); print("|---|---|---|---|---|")
for k in sorted(set(E1) | set(E2), key=lambda k: -(E1.get(k, (0,))[0] + E2.get(k, (0,))[0])):
    ex = (E1.get(k) or E2.get(k))[1]
    print(f"| {k[0]} | {k[1]} | {E1.get(k, (0,))[0]} | {E2.get(k, (0,))[0]} | {', '.join(ex)} |")
print(f"\nbound-crossing cells (to too large, from any answer): seed 1 {B1}, seed 2 {B2}")
