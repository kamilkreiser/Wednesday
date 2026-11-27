#!/bin/bash
# analyse planted control N against the base on each corpus: unattributed, (vi) oracle differences, (b0), first report
Q=/private/tmp/claude-501/qae3
for N in "$@"; do
  for c in own c2 c1 c3 lit; do
    python3 -I -B $Q/h/qa3_diff.py $Q/corp/$c $Q/corp/$c.base.out $Q/corp/$c.pl_$N.out ${N}_$c > $Q/logs/pldiff_${N}_$c.txt 2>&1
  done
  python3 -I -B - "$N" <<'PY'
import re, sys
N = sys.argv[1]; Q = '/private/tmp/claude-501/qae3'; row = []; firsts = []
for c in ['own', 'c2', 'c1', 'c3', 'lit']:
    t = open(f'{Q}/logs/pldiff_{N}_{c}.txt').read()
    u = re.search(r"'unattributed': (\d+)", t); u = int(u.group(1)) if u else 0
    v = re.search(r'\(vi\) every input, head emails vs my oracle \(code xn-- reading\): (\{.*?\}|0)', t).group(1)
    vo = re.search(r"'OTHER': (\d+)", v); vn = int(vo.group(1)) if vo else 0
    b0 = int(re.search(r'\(b0\) inputs where a byte the base masked is not masked at the head: (\d+)', t).group(1))
    row.append(f'{c} {u}/{vn}/{b0}')
    m = re.search(r'FIRST UNATTRIBUTED: (.*)', t) or re.search(r'   first (?:OTHER|D-W5b[^:]*): (.*)', t)
    if m and len(firsts) < 1: firsts.append(f'[{c}] ' + m.group(1)[:330])
    b = re.search(r'\(b0\) .*first: (.*)', t).group(1)
    if b != 'None' and not any('b0' in f for f in firsts): firsts.append(f'[{c}] b0 first: ' + b[:300])
print(f'{N}: (unattributed / oracle differences other than D-W5b / b0) ' + '; '.join(row))
for f in firsts: print('    ' + f)
PY
done
