#!/usr/bin/env python3
"""derive_linear_read.py — writes linear_read.py for the #1008 set from the sibling set's linear_read.py by asserted replacements. Reads only."""
import sys, re
s = open(sys.argv[1]).read()
reps = [
 ('for the #1006 set (KS-844, KS-727, KS-832)', 'for the #1008 set (KS-1087)', 1),
 ('attachmentsForURL on pull/1006', 'attachmentsForURL on pull/1008', 1),
 ("['https://github.com/Secuura/Distributed_Secuura/pull/1006', 'https://github.com/Secuura/Distributed_Secuura/pull/1005']", "['https://github.com/Secuura/Distributed_Secuura/pull/1008']", 1),
]
for a, b, n in reps:
    c = s.count(a); assert c == n, (a[:60], c)
    s = s.replace(a, b)
left = [s[m.start()-30:m.start()+10] for m in re.finditer(r'1006|1005|KS-844|KS-727|KS-832', s)]
assert not left, ('residual', left)
open(sys.argv[2], 'w').write(s); print('linear_read.py written, replacements', len(reps))
