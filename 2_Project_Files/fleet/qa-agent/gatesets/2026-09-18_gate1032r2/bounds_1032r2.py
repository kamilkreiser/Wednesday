#!/usr/bin/env python3
"""bounds_1032r2.py <tag> (from the round-1 bounds_1032.py) — the Secuura checkout reading (read verbs only): porcelain count, .git/config sha256, for-each-ref count, .git/worktrees count, branch,
auth node_modules/.vite listing; origin develop + refs/pull/1032/head by ls-remote."""
import subprocess, hashlib, os, sys, datetime
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
def run(c): p = subprocess.run(c, capture_output=True, text=True); return p.stdout, p.stderr
o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
lsr = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1032/head'])[0].split()
vd = REPO + '/Blockchain/Dev/services/auth/node_modules/.vite'
print('bounds', sys.argv[1] if len(sys.argv) > 1 else '?', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| porcelain', len(o.splitlines()), '| config', hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16],
      '| refs', len(run(['git', '-C', REPO, 'for-each-ref'])[0].splitlines()), '| worktrees', len(os.listdir(REPO + '/.git/worktrees')), '| branch', run(['git', '-C', REPO, 'branch', '--show-current'])[0].strip(),
      '| auth .vite', sorted(os.listdir(vd)) if os.path.isdir(vd) else 'ABSENT', '| ls-remote', dict(zip(lsr[1::2], [x[:9] for x in lsr[0::2]])), '| status stderr', repr(e.strip()[:100]))
