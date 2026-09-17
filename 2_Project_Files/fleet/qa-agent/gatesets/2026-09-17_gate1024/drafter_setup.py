#!/usr/bin/env python3
"""drafter_setup.py — #1024 (KS-1202) TIER 1 ROUND 1 drafter substrate. clone --shared --no-checkout by SHA into a fresh mktemp -d under
/private/tmp/claude-501/drafter1024; worktrees IN THE CLONE: head d1a328088, dev 581c9db0d (develop = the head's second parent), fix 86b11045c (nothing runs).
merge-tree --write-tree ONLY in the clone. node_modules farmed PER ENTRY (Dev/node_modules with @secuura relinked, packages/shared, services/originate), .vite/.vitest/.cache
skipped; shared dist per tree; IN TREE asserted from originate. Never rm. stderr kept. The Secuura checkout: .git/worktrees entry count + porcelain read BEFORE and AFTER."""
import subprocess, os, tempfile, datetime, json, sys
SCR = '/private/tmp/claude-501/drafter1024'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'
SHA = dict(head='d1a3280880d85ff31fd409aa1b5a16c428c4bb9a', dev='581c9db0db4201c42cbbf702f339b750989acdb1', fix='86b11045cd2202c14af55437aed26d094b5d74a7',
           m1='1f8763f9f', devold='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed')
DEV = 'Blockchain/Dev'; PER_ENTRY = ['packages/shared', 'services/originate']
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
W = tempfile.mkdtemp(prefix='gate1024_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
trees = {}
for name in ('head', 'dev', 'fix'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
for a, b in (('fix', 'dev'), ('head', 'dev')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); P('merge-tree --write-tree (IN THE CLONE)', a, 'x', b, 'rc', rc, 'tree', o.strip().split('\n')[0], e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}', SHA['head'] + '^1', SHA['head'] + '^2', SHA['fix'] + '^1']); P('head tree / parents / fix parent', o.split())
rc, o, e = run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']]); P('dev 581c9db0d ancestor of head: rc', rc, '(0 = yes)')
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['dev'], SHA['head']]); P('dev..head files:', o.strip().replace('\n', ' | '))
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['dev'] + '...' + SHA['fix']]); P('merge-base(dev,fix)..fix files:', o.strip().replace('\n', ' | '))
rc, o, e = run(['git', '-C', C, 'diff', '--quiet', SHA['fix'], SHA['head'], '--', DEV + '/services/originate/src/routes/documents.ts', DEV + '/services/originate/src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts']); P('PR files byte-identical fix vs head: rc', rc, '(0 = identical)')
for name in ('head', 'dev'):
    wt = trees[name]
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/originate')) if os.path.islink(p)]; P('   wholesale node_modules links:', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + DEV + '/services/originate/src', capture_output=True, text=True); P('  resolve from originate:', p.stdout.strip(), p.stderr.strip()[:300])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
