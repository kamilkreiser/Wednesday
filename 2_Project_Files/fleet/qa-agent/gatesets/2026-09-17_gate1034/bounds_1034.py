#!/usr/bin/env python3
"""bounds_1034.py TAG — checkout readings (read verbs only) + TCP LISTEN census with cwd/argv per node pid + login_stub.mjs count + node listeners
whose cwd or argv is under the drafter workdir (must be 0 at close) + ls-remote head/develop. Appends to out/bounds.out."""
import subprocess, os, sys, hashlib, datetime, json, re
GSD = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
def run(c): p = subprocess.run(c, capture_output=True, text=True); return p.stdout, p.stderr
tag = sys.argv[1]; now = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
por, e1 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
refs, _ = run(['git', '-C', REPO, 'for-each-ref'])
br, _ = run(['git', '-C', REPO, 'branch', '--show-current'])
lsr, e2 = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1034/head'])
cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
vite = os.path.isdir(REPO + '/Blockchain/Dev/services/api-gateway/node_modules/.vite')
ls, e3 = run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'])
rows = [l for l in ls.splitlines()[1:] if l.strip()]
node = sorted({int(l.split()[1]) for l in rows if l.split()[0].lower().startswith('node')})
det = []; mine = 0; stubs = 0
for pid in node:
    cwd, _ = run(['lsof', '-a', '-p', str(pid), '-d', 'cwd', '-Fn']); cwd = [x[1:] for x in cwd.splitlines() if x.startswith('n')]
    argv, _ = run(['ps', '-o', 'command=', '-p', str(pid)])
    if 'login_stub.mjs' in argv: stubs += 1
    if any(W in c for c in cwd) or W in argv: mine += 1
    det.append((pid, (cwd or ['?'])[0][-70:], argv.strip()[:90]))
line = '%s %s | porcelain %d | .git/config %s | refs %d | worktrees %d | branch %s | api-gateway node_modules/.vite exists %s | ls-remote %s | LISTEN rows %d | node listener pids %d | login_stub.mjs %d | node listeners under the drafter workdir %d | stderr %r' % (
    tag, now, len(por.splitlines()), cfg, len(refs.splitlines()), len(os.listdir(REPO + '/.git/worktrees')), br.strip(), vite, lsr.strip().replace('\n', ' | ').replace('\t', ' '), len(rows), len(node), stubs, mine, (e1 + e2 + e3).strip()[:200])
open(GSD + '/out/bounds.out', 'a').write(line + '\n' + ''.join('    node pid %d cwd %s argv %s\n' % d for d in det))
print(line); [print('    node pid %d cwd %s argv %s' % d) for d in det]
