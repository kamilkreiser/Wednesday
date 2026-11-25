# QA-POLICY-AT item 7: compare the instrumented generator outputs of the base and head trees (the draw signature),
# the fixture root masked in every case (upper-cased commands included). usage: flags_cmp.py flags_dbase.txt flags_dhead.txt
import sys, re
from collections import Counter
R = re.compile(r'/private/tmp/claude-501/qpa/tt_d(base|head)/testtmp/m2-policy/qpa-flags-\d+', re.I)
def rd(p): return [R.sub('<ROOT>', l.rstrip('\n')).split('\t') for l in open(p) if l.startswith('ITEM')]
b, h = rd(sys.argv[1]), rd(sys.argv[2])
d = [x[1] for x, y in zip(b, h) if (x[2], x[3], x[5]) != (y[2], y[3], y[5])]
print('items', len(b), len(h), '| draw signatures differing with the flag and the root masked:', len(d), d[:5])
print('base flags', dict(Counter(x[4] for x in b))); print('head flags', dict(Counter(y[4] for y in h)))
print('base true -> head not true:', sum(1 for x, y in zip(b, h) if x[4] == 'true' and y[4] != 'true'),
      '| base not-true -> head true:', sum(1 for x, y in zip(b, h) if x[4] != 'true' and y[4] == 'true'),
      '| absent changed:', sum(1 for x, y in zip(b, h) if (x[4] == 'absent') != (y[4] == 'absent')))
print('base false -> head:', dict(Counter(y[4] for x, y in zip(b, h) if x[4] == 'false')))
print('control (flag column NOT masked):', sum(1 for x, y in zip(b, h) if (x[4], x[5]) != (y[4], y[5])))
