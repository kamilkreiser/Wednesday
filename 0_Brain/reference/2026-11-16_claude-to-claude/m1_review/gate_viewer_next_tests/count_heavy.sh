#!/bin/bash
# Count heavy jobs of OTHER seats: a process matching the heavy patterns whose parent is not itself one (QA-VIEWER-NEXT).
ps -axo pid=,ppid=,etime=,command= > /private/tmp/claude-501/qvx/out/ps_now.txt
python3 -B - <<'PY'
import re
rows=[l.split(None,3) for l in open('/private/tmp/claude-501/qvx/out/ps_now.txt') if l.strip()]
pat=re.compile(r'bash .*(check\.sh|red-controls[^ ]*\.sh|test-p1p\.sh|test-daemon\.sh)')
heavy={r[0]:r for r in rows if len(r)==4 and pat.search(r[3]) and 'qvx' not in r[3]}
jobs=[r for p,r in heavy.items() if r[1] not in heavy]
for r in jobs: print('JOB', r[0], r[2], r[3][:160])
print('count', len(jobs))
PY
