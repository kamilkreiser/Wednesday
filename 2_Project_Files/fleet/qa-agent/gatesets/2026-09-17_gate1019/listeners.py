#!/usr/bin/env python3
"""listeners.py LABEL — TCP LISTEN census (lsof, stderr kept) + cwd and argv for every node pid; processes with cwd inside the #1019 drafter
workdir (from drafter_paths.json when present) with a positive control (any cwd under /Volumes/DevMASTER). login_stub.mjs processes named by argv."""
import subprocess, sys, datetime, json, os, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
lab = sys.argv[1]
print('listeners', lab, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
p = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
print('lsof rc', p.returncode, '| stderr:', repr(p.stderr.strip()[:300]))
print(p.stdout.rstrip())
lines = p.stdout.splitlines()[1:]
print('LISTEN lines', len(lines))
pids = sorted({int(l.split()[1]) for l in lines if l.split()[0] == 'node'})
print('--- node listener pids with cwd + argv:', len(pids))
def cwd(pid):
    q = subprocess.run(['lsof', '-a', '-p', str(pid), '-d', 'cwd', '-Fn'], capture_output=True, text=True)
    return ([x[1:] for x in q.stdout.splitlines() if x.startswith('n')] or ['?'])[0], q.stderr.strip()[:200]
for pid in pids:
    c, e = cwd(pid)
    a = subprocess.run(['ps', '-o', 'ppid=,lstart=,command=', '-p', str(pid)], capture_output=True, text=True)
    print('pid', pid, 'cwd', c, '| ps', a.stdout.strip()[:300], '| stderr', repr(e + a.stderr.strip()[:100]))
ps = subprocess.run(['ps', '-axo', 'pid=,ppid=,command='], capture_output=True, text=True)
stubs = [l.strip() for l in ps.stdout.splitlines() if 'login_stub.mjs' in l and 'ps -axo' not in l]
print('--- processes whose argv names login_stub.mjs:', len(stubs), '| ps stderr', repr(ps.stderr.strip()[:100]))
for s in stubs: print('   ', s[:300])
W = ''
if os.path.exists(GS + '/drafter_paths.json'): W = json.load(open(GS + '/drafter_paths.json'))['W']
allp = [l.split()[0] for l in ps.stdout.splitlines() if l.strip()]
mine = 0; ctl = 0
if W:
    for pid in allp:
        c, _ = cwd(pid)
        if c.startswith(W): mine += 1; print('   cwd in drafter workdir: pid', pid, c)
        if c.startswith('/Volumes/DevMASTER'): ctl += 1
    print('processes with cwd inside the drafter workdir', W.split('/')[-1], ':', mine, '| control (cwd under /Volumes/DevMASTER):', ctl)
else:
    print('drafter workdir not yet created: cwd census skipped (before setup)')
