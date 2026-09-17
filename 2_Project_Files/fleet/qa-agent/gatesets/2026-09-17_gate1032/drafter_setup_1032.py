#!/usr/bin/env python3
"""drafter_setup_1032.py — #1032 (KS-1194) TIER 1 ROUND 1 drafter substrate (shape: drafter_setup_1031.py, services/auth instead of originate).
clone --shared --no-checkout into a fresh mktemp -d under /private/tmp/claude-501/drafter1032; worktrees IN THE CLONE: head 70ee7b6c0, dev 0a2b1603f.
Merge-in proof IN THE CLONE ONLY: each of the three merges on the branch (29d9f90fa, c82f5edd5, 70ee7b6c0) re-derived with merge-tree --write-tree of its
own parents (a mechanical merge carries no hand edit); develop..head file set = users.ts + the ks1194 test; numstat; the merge-tree prediction 1111602c4;
the fix commit's users.ts patch-id vs the develop..head users.ts patch-id; the ks1194 test blob fix = head; auth + shared subtrees before/after the last merge.
node_modules farmed PER ENTRY (Dev/node_modules with @secuura relinked, packages/shared, services/auth), .vite/.vitest/.cache skipped; shared dist per tree;
IN TREE asserted from auth. Never rm. stderr kept. The Secuura checkout: porcelain + .git/worktrees + refs + config sha + branch + auth .vite read BEFORE/AFTER."""
import subprocess, os, tempfile, datetime, json, hashlib
SCR = '/private/tmp/claude-501/drafter1032'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
SHA = dict(head='70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039', dev='0a2b1603fe52f0f3b8152588af78bbeab0237be7', fix='00236c10bc9c237e64e008f6bb927c816a8bb29c',
           m1='29d9f90fae31ebb8a53dac508648f49fbb20db77', m2='c82f5edd530ce9d602dfc63ffcbd5f9ad944a083')
PRED_TREE = '1111602c4ef8a8ca08b3f500ee241ec5fc1c0577'
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
USERS = A + '/src/routes/users.ts'; TEST = A + '/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts'
PER_ENTRY = ['packages/shared', 'services/auth']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def run(c, cwd=None, inp=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, input=inp); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    wts = len(os.listdir(REPO + '/.git/worktrees'))
    rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    vd = REPO + '/' + A + '/node_modules/.vite'
    vite = sorted(os.listdir(vd)) if os.path.isdir(vd) else 'ABSENT'
    r = dict(worktrees=wts, porcelain=len(o.splitlines()), refs=refs, config=cfg, branch=br, auth_vite=vite)
    P('source checkout', tag, now(), r, '| status stderr', repr(e.strip()[:200])); return r
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
def patch_id(C, a, b, path):
    rc, d, e = run(['git', '-C', C, 'diff', '--full-index', a, b, '--', path])
    rc2, o, e2 = run(['git', '-C', C, 'patch-id', '--stable'], inp=d)
    return (o.split() or ['EMPTY'])[0]
P('drafter_setup_1032', now())
before = checkout_reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1032_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for k, v in SHA.items():
    P('object', k, v[:9], run(['git', '-C', C, 'cat-file', '-t', v])[1].strip(), '| parents', run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', v])[1].split()[1:], '| tree', run(['git', '-C', C, 'rev-parse', v + '^{tree}'])[1].strip()[:9])
trees = {}
for name in ('head', 'dev'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
# the three merges, each re-derived from its own parents
for tag in ('m1', 'm2', 'head'):
    ps = run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', SHA[tag]])[1].split()[1:]
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', ps[0], ps[1]])
    mt = o.strip().split('\n')[0]; tr = run(['git', '-C', C, 'rev-parse', SHA[tag] + '^{tree}'])[1].strip()
    brought = run(['git', '-C', C, 'diff', '--name-only', ps[0], SHA[tag]])[1].split()
    mb = run(['git', '-C', C, 'merge-base', ps[0], ps[1]])[1].strip()
    devdelta = run(['git', '-C', C, 'diff', '--name-only', mb, ps[1]])[1].split()
    P('merge %s %s = merge-tree %s x %s rc %d -> %s | tree %s %s | brought %d files, develop delta %s..%s %d files, brought - develop delta = %s | conflicts %s'
      % (tag, SHA[tag][:9], ps[0][:9], ps[1][:9], rc, mt[:9], tr[:9], 'EQUAL' if mt == tr else 'DIFFER', len(brought), mb[:9], ps[1][:9], len(devdelta),
         sorted(set(brought) - set(devdelta)), o.strip().split('\n')[1:][:4]))
P('head tree', run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}'])[1].strip(), '= builder prediction 1111602c4:', run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}'])[1].strip() == PRED_TREE)
rc, o, e = run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']]); P('develop 0a2b1603f ancestor of head: rc', rc, '(0 = yes)')
P('develop..head numstat:', run(['git', '-C', C, 'diff', '--numstat', SHA['dev'], SHA['head']])[1].strip().replace('\n', ' | '))
dh = sorted(run(['git', '-C', C, 'diff', '--name-only', SHA['dev'], SHA['head']])[1].split()); P('develop..head files == {users.ts, ks1194 test}:', dh == sorted([USERS, TEST]), dh)
P('head^1 (c82f5edd5) -> head brought:', run(['git', '-C', C, 'diff', '--name-only', SHA['m2'], SHA['head']])[1].split())
P('fix commit 00236c10b numstat:', run(['git', '-C', C, 'diff', '--numstat', SHA['fix'] + '^', SHA['fix']])[1].strip().replace('\n', ' | '))
pf = patch_id(C, SHA['fix'] + '^', SHA['fix'], USERS); ph = patch_id(C, SHA['dev'], SHA['head'], USERS)
P('users.ts patch-id fix^..fix', pf[:12], '| develop..head', ph[:12], '| equal:', pf == ph)
tf = run(['git', '-C', C, 'diff', '--quiet', SHA['fix'], SHA['head'], '--', TEST])[0]; P('ks1194 test byte-identical fix = head rc', tf, '(0 = identical)')
# the users.ts content outside the KS-1194 hunks: head users.ts with the fix commit's own hunks reverse-applied equals develop users.ts?
rc, d, e = run(['git', '-C', C, 'diff', SHA['fix'] + '^', SHA['fix'], '--', USERS])
rc2, o2, e2 = run(['git', '-C', trees['head'], 'apply', '--check', '-R', '--recount', '-'], inp=d)
P('fix-commit users.ts hunks reverse-apply cleanly onto head (git apply --check -R, in the clone worktree) rc', rc2, e2.strip()[:200])
for sub in (A, DEV + '/packages/shared'):
    P('subtree', sub.split('/')[-1], {k: run(['git', '-C', C, 'rev-parse', SHA[k] + ':' + sub])[1].strip()[:9] for k in ('dev', 'm2', 'head')})
P('blobs: users.ts develop', run(['git', '-C', C, 'rev-parse', SHA['dev'] + ':' + USERS])[1].strip(), 'head', run(['git', '-C', C, 'rev-parse', SHA['head'] + ':' + USERS])[1].strip(),
  '| test head', run(['git', '-C', C, 'rev-parse', SHA['head'] + ':' + TEST])[1].strip(), '| test at develop cat-file -e rc', run(['git', '-C', C, 'cat-file', '-e', SHA['dev'] + ':' + TEST])[0])
for name in ('head', 'dev'):
    wt = trees[name]
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/auth')) if os.path.islink(p)]; P('   wholesale node_modules links:', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + A + '/src', capture_output=True, text=True); P('  resolve from auth:', p.stdout.strip(), p.stderr.strip()[:300])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1032 end', now('%H:%M:%S %Z'))
