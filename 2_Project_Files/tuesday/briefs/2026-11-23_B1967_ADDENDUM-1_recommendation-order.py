#!/usr/bin/env python3
# B1967 ADDENDUM-1 patch (Tuesday, s315): reorders the coordinator's recommendation in mkdoc.py so that the darker brand-token
# values (what the product owner asked to see: "An agent proposes darker values for each fill from the brand tokens") come FIRST,
# and the outline comes second as the keep-today's-colours alternative. Prose only: no figure, table, measurement or screenshot
# changes. Usage: python3 -I <this> <frozen mkdoc.py> <new mkdoc_a1.py>   (writes a NEW file; refuses if any anchor is not found once)
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf8').read()
R = [
    ("In short, the outline on the fill if you want the toner colours to keep their identity; otherwise the three graphic-kind tokens named there.')",
     "In short, the three graphic-kind tokens named there, which are the darker values you asked to see; if you would rather keep today\\'s toner colours, the outline on the fill.')"),
    ("A('1. **First choice: N2b, a 1px outline on the fill in `%s`.**",
     "A('2. **If you would rather keep today\\'s toner colours: N2b, a 1px outline on the fill in `%s`.**"),
    ("A('2. **If you want the colour itself to clear:** cyan",
     "A('1. **First choice, the darker values you asked to see:** cyan"),
]
for old, new in R:
    n = t.count(old)
    if n != 1:
        sys.exit('ANCHOR COUNT %d (must be 1): %s' % (n, old[:60]))
    t = t.replace(old, new)
L = t.split('\n')
i = [k for k, l in enumerate(L) if l.startswith("A('2. **If you would rather keep today")]
j = [k for k, l in enumerate(L) if l.startswith("A('1. **First choice, the darker values")]
if len(i) != 1 or len(j) != 1 or j[0] != i[0] + 1 or not L[j[0] + 1].rstrip().endswith(']))'):
    sys.exit('SWAP SHAPE NOT AS EXPECTED: %s %s' % (i, j))
a = i[0]
L[a:a + 3] = [L[a + 1], L[a + 2], L[a]]
open(dst, 'x', encoding='utf8').write('\n'.join(L))
print('OK: 3 replacements, 1 swap; wrote', dst)
