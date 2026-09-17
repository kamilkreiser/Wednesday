#!/usr/bin/env python3
"""drafter_setup.py — #1018 (KS-1050) TIER 2 ROUND 1 drafter substrate. clone --shared --no-checkout by SHA into a fresh mktemp -d under
/private/tmp/claude-501/drafter1018; worktrees IN THE CLONE: head 267bd8624, base 7e89318bc (the PR parent), dev 81ee4b729 (origin develop).
merge-tree --write-tree ONLY in the clone (head x dev), plus the merged-vs-head delta and the auth-subtree identity. node_modules farmed PER ENTRY
(Dev/node_modules with @secuura relinked, packages/shared, services/auth), .vite/.vitest/.cache skipped; shared dist built per tree; @secuura/shared
IN TREE asserted from auth. Never rm. stderr kept. The Secuura checkout: .git/worktrees entry count + porcelain read BEFORE and AFTER."""
import subprocess, os, tempfile, datetime, json
SCR = '/private/tmp/claude-501/drafter1018'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
SHA = dict(head='267bd8624ce276ca62160216d042b8477bac52f1', base='7e89318bcedbc9a35757d4298ace54a6a23020bd', dev='81ee4b729e86a645fc9098aafa1aaf39035a9950')
DEV = 'Blockchain/Dev'; PER_ENTRY = ['packages/shared', 'services/auth']
PR_FILES = [DEV + '/services/auth/src/routes/users.ts', DEV + '/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    wts = len(os.listdir(REPO + '/.git/worktrees'))
    rc2, o2, e2 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    P('source checkout', tag, '| .git/worktrees entries', wts, '| porcelain lines', len(o2.splitlines()), '| stderr', repr(e2.strip()[:200])); return wts, len(o2.splitlines())
def farm_dir(src, dst, rewrite):
    os.mkdir(dst); n = 0; sk = []
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): sk.append(ent); continue
        s = os.path.join(src, ent)
        if rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        else:
            os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n, sk
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = checkout_reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1018_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for k, v in SHA.items():
    rc, o, e = run(['git', '-C', C, 'cat-file', '-t', v]); P('object', k, v[:9], o.strip(), e.strip()[:100])
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', '--messages', SHA['head'], SHA['dev']])
P('merge-tree --write-tree (IN THE CLONE) head x dev rc', rc, '(0 clean, 1 conflicts)'); P('  stdout:', o.strip().replace('\n', ' | ')[:1500]); P('  stderr:', e.strip()[:300])
merged = o.strip().split('\n')[0] if rc == 0 else None
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', SHA['dev'], SHA['dev']]); P('control dev x dev tree', o.strip().split('\n')[0], '| dev tree', run(['git', '-C', C, 'rev-parse', SHA['dev'] + '^{tree}'])[1].strip())
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}', SHA['head'] + '^1']); P('head tree / parent', o.split())
rc, o, e = run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']]); P('merge-base head dev', o.strip())
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['base'], SHA['head']]); P('base..head files:', o.strip().replace('\n', ' | '))
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['base'], SHA['dev'], '--', DEV + '/services/auth', DEV + '/packages/shared/src', DEV + '/package.json', DEV + '/package-lock.json']); P('base..dev under auth / shared src / Dev manifest+lock:', repr(o.strip()))
if merged:
    rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['head'], merged]); P('head..merged files:', o.strip().replace('\n', ' | '))
    rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['dev'], merged]); P('dev..merged files (must be exactly the PR files):', o.strip().replace('\n', ' | '))
    for sub in (DEV + '/services/auth', DEV + '/packages/shared'):
        a = run(['git', '-C', C, 'rev-parse', SHA['head'] + ':' + sub])[1].strip(); b = run(['git', '-C', C, 'rev-parse', merged + ':' + sub])[1].strip()
        P('subtree', sub, 'head', a[:9], 'merged', b[:9], 'EQUAL' if a == b else 'DIFFER')
    for f in PR_FILES:
        a = run(['git', '-C', C, 'rev-parse', SHA['head'] + ':' + f])[1].strip(); b = run(['git', '-C', C, 'rev-parse', merged + ':' + f])[1].strip()
        P('blob', f.rsplit('/', 1)[1], 'head', a[:9], 'merged', b[:9], 'EQUAL' if a == b else 'DIFFER')
trees = {}
for name in ('head', 'base'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        src = os.path.join(REPO, DEV, rel, 'node_modules')
        if not os.path.isdir(src): P('   per-entry farm', rel, 'NO node_modules in the checkout'); continue
        n, sk = farm_dir(src, os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + DEV + '/services/auth/src', capture_output=True, text=True); P('  resolve from auth:', p.stdout.strip(), p.stderr.strip()[:300])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merged': merged}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
