#!/usr/bin/env python3
"""drafter_setup.py — #1022 drafter: READ-ONLY git on the Secuura checkout (ls-remote, rev-parse, cat-file, diff, ls-tree); every WRITE verb
(clone, worktree add, merge-tree --write-tree) only inside the drafter's OWN scratch clone under /private/tmp/claude-501/drafter1022/.
Never cd; cwd for every subprocess is the scratch dir. Prints readings; stderr kept."""
import datetime, hashlib, os, subprocess, sys, tempfile
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCR = '/private/tmp/claude-501/drafter1022'
HEAD = '58684e6534b4d420c9fb9ea246d3a32c70c70828'
BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'
DEV = '581c9db0db4201c42cbbf702f339b750989acdb1'
PR1021 = '742e1c6080f2527973268146611930e4a70edef2'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(args, cwd=SCR, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        print('FAILED rc', p.returncode, args, p.stderr[-800:]); sys.exit(1)
    return p
def g(*a): return run(['git', '-C', REPO] + list(a)).stdout.strip()
def readings(tag):
    por = len([l for l in g('status', '--porcelain').splitlines() if l.strip()])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    refs = len(g('for-each-ref').splitlines()); wts = len(os.listdir(REPO + '/.git/worktrees'))
    print('CHECKOUT %s %s: porcelain %d | .git/config sha256 %s | refs %d | .git/worktrees %d | branch %s' % (tag, now(), por, cfg, refs, wts, g('branch', '--show-current')))
readings('start')
print(g('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1022/head', 'refs/pull/1021/head'))
print('merge-base head develop:', g('merge-base', HEAD, DEV), '| is BASE ancestor of DEV:', run(['git', '-C', REPO, 'merge-base', '--is-ancestor', BASE, DEV], check=False).returncode == 0)
print('head parents:', g('rev-list', '--parents', '-n1', HEAD))
print('three-dot files BASE...HEAD:'); print(g('diff', '--numstat', BASE + '...' + HEAD))
print('develop delta BASE..DEV:'); print(g('diff', '--numstat', BASE, DEV)); print(g('log', '--oneline', BASE + '..' + DEV))
print('#1021 files BASE...PR1021:'); print(g('diff', '--numstat', BASE + '...' + PR1021))
F = ['Blockchain/Dev/package-lock.json', 'Blockchain/Dev/scripts/audit/audit-baseline.json', 'Blockchain/Dev/services/mcp-server/package-lock.json',
     'Blockchain/Dev/services/originate/package-lock.json', 'Blockchain/Dev/package.json', 'Blockchain/Dev/services/mcp-server/package.json',
     'Blockchain/Dev/services/originate/package.json', 'Blockchain/Dev/scripts/audit/audit-gate.mjs', 'Blockchain/Dev/scripts/audit/audit-locks.mjs',
     'Blockchain/Dev/scripts/audit/lock-discovery.mjs', 'Blockchain/Dev/scripts/audit/baseline-contract.mjs', 'Blockchain/Dev/scripts/audit/package.json',
     'Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh', 'Blockchain/Dev/services/mcp-server/Dockerfile',
     'Blockchain/Dev/services/originate/Dockerfile', '.githooks/pre-push']
for f in F:
    blobs = []
    for t, sha in (('base', BASE), ('head', HEAD), ('develop', DEV), ('#1021', PR1021)):
        p = run(['git', '-C', REPO, 'rev-parse', sha + ':' + f], check=False)
        blobs.append('%s %s' % (t, p.stdout.strip() if p.returncode == 0 else 'ABSENT'))
    print('BLOB', f, '|', ' | '.join(blobs))
os.makedirs(SCR, exist_ok=True)
clone = tempfile.mkdtemp(prefix='clone-', dir=SCR)
print('clone dir', clone, now())
run(['git', 'clone', '--shared', '--no-checkout', '-q', REPO, clone + '/repo'])
C = clone + '/repo'
for sha in (HEAD, BASE, DEV, PR1021): run(['git', '-C', C, 'cat-file', '-e', sha + '^{commit}'])
for name, sha in (('head', HEAD), ('base', BASE), ('develop', DEV)):
    run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', clone + '/wt-' + name, sha])
    print('worktree', name, run(['git', '-C', clone + '/wt-' + name, 'rev-parse', 'HEAD']).stdout.strip(),
          'porcelain', len(run(['git', '-C', clone + '/wt-' + name, 'status', '--porcelain']).stdout.splitlines()))
def mt(a, b):
    p = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b], check=False)
    return p.returncode, p.stdout.strip().replace('\n', ' || ')
print('merge-tree DEV + HEAD (seat b475cfbe1):', mt(DEV, HEAD))
print('merge-tree HEAD + DEV (order control):', mt(HEAD, DEV))
print('head tree', run(['git', '-C', C, 'rev-parse', HEAD + '^{tree}']).stdout.strip(), '| develop tree', run(['git', '-C', C, 'rev-parse', DEV + '^{tree}']).stdout.strip())
rc, t = mt(DEV, PR1021); print('merge-tree DEV + #1021:', rc, t)
m1021 = t.split(' ')[0]
rc2, t2 = mt(DEV, HEAD); m1022 = t2.split(' ')[0]
# second-merge predictions: develop' = develop + one PR (as a commit), then merge the other
env = dict(os.environ, GIT_AUTHOR_NAME='drafter', GIT_AUTHOR_EMAIL='d@local', GIT_COMMITTER_NAME='drafter', GIT_COMMITTER_EMAIL='d@local',
           GIT_AUTHOR_DATE='2026-09-17T00:00:00Z', GIT_COMMITTER_DATE='2026-09-17T00:00:00Z')
def commit_tree(tree, parent, msg):
    return subprocess.run(['git', '-C', C, 'commit-tree', tree, '-p', parent, '-m', msg], capture_output=True, text=True, env=env, cwd=SCR).stdout.strip()
d_after_1021 = commit_tree(m1021, DEV, 'scratch: squash #1021 onto develop')
d_after_1022 = commit_tree(m1022, DEV, 'scratch: squash #1022 onto develop')
print('scratch squash commits: develop+#1021', d_after_1021, '| develop+#1022', d_after_1022)
print('SECOND: #1022 after #1021 squashed:', mt(d_after_1021, HEAD))
print('SECOND: #1021 after #1022 squashed:', mt(d_after_1022, PR1021))
open(SCR + '/CLONE_PATH', 'w').write(clone + '\n')
readings('close')
print('done', now())
