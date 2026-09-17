#!/usr/bin/env python3
"""drafter_census_1035.py TAG — lsof TCP LISTEN census (rows, node pids with cwd + argv, login_stub.mjs count, rows under the drafter workdir). Read only."""
import subprocess, sys, json, os, datetime
PA = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/out/drafter_paths.json')); W = PA['W']
ls = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
rows = [l for l in ls.stdout.splitlines()[1:] if l.strip()]
pids = sorted({int(l.split()[1]) for l in rows if l.split()[0].startswith('node')})
det = []
for p in pids:
    cwd = subprocess.run(['lsof', '-a', '-p', str(p), '-d', 'cwd', '-Fn'], capture_output=True, text=True).stdout.split('\nn')[-1].strip()
    argv = subprocess.run(['ps', '-o', 'command=', '-p', str(p)], capture_output=True, text=True).stdout.strip()[:160]
    det.append((p, cwd[-90:], argv))
print(sys.argv[1], datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| LISTEN rows', len(rows), '| node listener pids', len(pids),
      '| login_stub.mjs', sum('login_stub.mjs' in d[2] for d in det), '| under drafter workdir', sum(W in d[1] or W in d[2] for d in det), '| lsof stderr', repr(ls.stderr.strip()[:120]))
for d in det: print('  node pid', d[0], 'cwd', d[1], 'argv', d[2])
