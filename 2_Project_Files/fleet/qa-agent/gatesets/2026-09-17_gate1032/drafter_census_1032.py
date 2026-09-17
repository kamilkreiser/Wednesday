#!/usr/bin/env python3
"""drafter_census_1032.py <tag> — listener census: lsof TCP LISTEN rows; per node pid its cwd and argv (truncated); node login_stub.mjs count; load."""
import subprocess, sys, datetime, re
def run(c): p = subprocess.run(c, capture_output=True, text=True); return p.stdout, p.stderr
tag = sys.argv[1] if len(sys.argv) > 1 else '?'
o, e = run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'])
rows = o.splitlines()[1:]
print('census', tag, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| LISTEN rows', len(rows), '| lsof stderr', repr(e.strip()[:120]))
pids = sorted({r.split()[1] for r in rows if r.split()[0].startswith('node')})
for pid in pids:
    cwd = [l for l in run(['lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'])[0].splitlines() if l.startswith('n')]
    argv = run(['ps', '-o', 'command=', '-p', pid])[0].strip()
    print('   node pid', pid, 'cwd', (cwd[0][1:] if cwd else '?')[:140], '| argv', argv[:160], '| drafter1032 cwd:', bool(cwd and 'drafter1032' in cwd[0]))
stubs = [l for l in run(['ps', '-ax', '-o', 'pid=,command='])[0].splitlines() if re.search(r'login_stub\.mjs', l) and 'grep' not in l]
print('   login_stub.mjs processes', len(stubs), '| load', run(['uptime'])[0].strip().split('load averages:')[-1].strip())
