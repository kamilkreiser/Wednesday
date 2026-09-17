#!/usr/bin/env python3
"""listeners.py LABEL — TCP LISTEN census (lsof, stderr kept) + cwd/ppid/argv per node pid; count of processes whose cwd or argv names THIS drafter's scratchpad
(positive control: processes with cwd under /Volumes/DevMASTER)."""
import subprocess, sys, datetime, re
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/804c11ac-1249-4d9f-837c-27ce44211d2f/scratchpad'
lab = sys.argv[1]
print('listeners', lab, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
p = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
print('lsof rc', p.returncode, '| stderr:', p.stderr.strip()[:300] or '(empty)')
print(p.stdout.rstrip())
lines = p.stdout.splitlines()[1:]
print('LISTEN lines', len(lines))
nodepids = sorted({l.split()[1] for l in lines if l.split()[0] == 'node'})
print('node LISTEN pids', nodepids, 'count', len(nodepids))
for pid in nodepids:
    c = subprocess.run(['lsof', '-a', '-p', pid, '-d', 'cwd', '-Fn'], capture_output=True, text=True)
    cwd = [x[1:] for x in c.stdout.splitlines() if x.startswith('n')]
    a = subprocess.run(['ps', '-o', 'ppid=,lstart=,command=', '-p', pid], capture_output=True, text=True)
    print(' pid', pid, 'cwd', cwd, '| ps', a.stdout.strip()[:400], '| stderr', (c.stderr + a.stderr).strip()[:200])
ps = subprocess.run(['ps', '-axo', 'pid=,command='], capture_output=True, text=True)
mine_argv = [l.strip()[:200] for l in ps.stdout.splitlines() if SCR in l and 'listeners.py' not in l]
print('processes whose argv names my scratchpad (excluding this census):', len(mine_argv), mine_argv[:10], '| ps stderr', ps.stderr.strip()[:200])
cw = subprocess.run(['lsof', '-d', 'cwd', '-Fpn'], capture_output=True, text=True)
pid = None; mine = 0; ctl = 0
for x in cw.stdout.splitlines():
    if x.startswith('p'): pid = x[1:]
    elif x.startswith('n'):
        if x[1:].startswith(SCR): mine += 1
        if x[1:].startswith('/Volumes/DevMASTER'): ctl += 1
print('processes with cwd inside my scratchpad:', mine, '| positive control, cwd under /Volumes/DevMASTER:', ctl, '| lsof cwd rc', cw.returncode, 'stderr bytes', len(cw.stderr))
