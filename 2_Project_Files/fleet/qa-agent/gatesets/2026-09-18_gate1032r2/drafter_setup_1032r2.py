#!/usr/bin/env python3
"""drafter_setup_1032r2.py — #1032 (KS-1194) TIER 1 ROUND 2 drafter substrate (from ../2026-09-17_gate1032/drafter_setup_1032.py, re-pinned).
clone --shared --no-checkout into a fresh mktemp -d under the session scratchpad gate1032r2/; worktrees IN THE CLONE: head 430672697, r1 70ee7b6c0,
dev 3961c2add. Merge-in proof IN THE CLONE ONLY: 5d55a72bd = merge-tree 70ee7b6c0 x 3961c2add; what the merge brought vs develop's own delta; the
services/auth part of that merge; develop an ancestor of head and merge-tree head x develop = head tree; develop..head file set; 5d55a72bd..head;
blobs; subtrees. node_modules farmed PER ENTRY (Dev/node_modules with @secuura relinked, packages/shared, services/auth), .vite/.vitest/.cache skipped;
shared dist per tree; IN TREE asserted from auth. Never rm. stderr kept. The Secuura checkout: read BEFORE/AFTER (read verbs only)."""
import subprocess, os, tempfile, datetime, json, hashlib
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8f7ffae4-dc85-433a-8a53-4d87581eb627/scratchpad/gate1032r2'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
SHA = dict(head='4306726977b55171a7c8c0eb5e42de078587a725', mergein='5d55a72bd59dcac88a9b5bc59c9c387bfcbc1540',
           r1='70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039', dev='3961c2add8e1637b32e638f8f0952c328c00833e', oldpin='0a2b1603fe52f0f3b8152588af78bbeab0237be7')
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
USERS = A + '/src/routes/users.ts'
T1 = A + '/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts'
T2 = A + '/src/__tests__/ks1194-approve-never-restores-pending-over-a-raised-level.test.ts'
PER_ENTRY = ['packages/shared', 'services/auth']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def run(c, cwd=None, inp=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, input=inp); return p.returncode, p.stdout, p.stderr
def g(C, *a): return run(['git', '-C', C] + list(a))[1].strip()
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
P('drafter_setup_1032r2', now())
before = checkout_reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1032r2_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for k, v in SHA.items():
    P('object', k, v[:9], g(C, 'cat-file', '-t', v), '| parents', [x[:9] for x in g(C, 'rev-list', '--parents', '-n', '1', v).split()[1:]], '| tree', g(C, 'rev-parse', v + '^{tree}')[:9])
# 1. the merge-in commit 5d55a72bd, re-derived from its own parents
ps = g(C, 'rev-list', '--parents', '-n', '1', SHA['mergein']).split()[1:]
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', ps[0], ps[1]])
mt = o.strip().split('\n')[0]; tr = g(C, 'rev-parse', SHA['mergein'] + '^{tree}')
brought = g(C, 'diff', '--name-only', ps[0], SHA['mergein']).split()
mb = g(C, 'merge-base', ps[0], ps[1]); devdelta = g(C, 'diff', '--name-only', mb, ps[1]).split()
P('MERGE-IN 5d55a72bd = merge-tree %s x %s rc %d -> %s | commit tree %s %s | brought %d files; develop delta %s..%s %d files; brought - delta = %s; delta - brought = %s | conflict lines %s'
  % (ps[0][:9], ps[1][:9], rc, mt[:9], tr[:9], 'EQUAL' if mt == tr else 'DIFFER', len(brought), mb[:9], ps[1][:9], len(devdelta), sorted(set(brought) - set(devdelta)), sorted(set(devdelta) - set(brought))[:5], o.strip().split('\n')[1:][:4]))
P('   brought under services/auth:', [x for x in brought if x.startswith(A + '/')], '| under packages/shared/src:', [x for x in brought if x.startswith(DEV + '/packages/shared/src/')], '| docs/openapi:', [x for x in brought if x.startswith(DEV + '/docs/openapi/')])
P('   develop merges between the round-1 pin and 3961c2add:', g(C, 'log', '--format=%h %s', '--first-parent', SHA['oldpin'] + '..' + SHA['dev']).replace('\n', ' || '))
# 2. the fix commit
P('FIX 5d55a72bd..head numstat:', g(C, 'diff', '--numstat', SHA['mergein'], SHA['head']).replace('\n', ' | '))
# 3. develop..head
P('develop 3961c2add ancestor of head rc', run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']])[0], '(0 = yes)')
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', SHA['head'], SHA['dev']])
P('merge-tree head x develop 3961c2add rc', rc, '->', o.strip().split('\n')[0][:9], '| head tree', g(C, 'rev-parse', SHA['head'] + '^{tree}')[:9], '| equal:', o.strip().split('\n')[0] == g(C, 'rev-parse', SHA['head'] + '^{tree}'))
dh = sorted(g(C, 'diff', '--name-only', SHA['dev'], SHA['head']).split())
P('develop..head files == {users.ts, ks1194 test, ks1194 r2 test}:', dh == sorted([USERS, T1, T2]), '| numstat', g(C, 'diff', '--numstat', SHA['dev'], SHA['head']).replace('\n', ' | '))
P('services/auth diff r1 70ee7b6c0..head:', g(C, 'diff', '--name-only', SHA['r1'], SHA['head'], '--', A).split())
P('whole-repo diff r1..mergein file count:', len(g(C, 'diff', '--name-only', SHA['r1'], SHA['mergein']).split()), '| r1..head services/auth/src count', len(g(C, 'diff', '--name-only', SHA['r1'], SHA['head'], '--', A + '/src').split()))
for f in (USERS, T1, T2):
    P('blob', f.split('/')[-1][:60], {k: (g(C, 'rev-parse', SHA[k] + ':' + f)[:9] if run(['git', '-C', C, 'cat-file', '-e', SHA[k] + ':' + f])[0] == 0 else 'ABSENT') for k in ('oldpin', 'dev', 'r1', 'mergein', 'head')})
for sub in (A + '/src', A, DEV + '/packages/shared'):
    P('subtree', sub.replace(DEV + '/', ''), {k: g(C, 'rev-parse', SHA[k] + ':' + sub)[:9] for k in ('oldpin', 'dev', 'r1', 'mergein', 'head')})
trees = {}
for name in ('head', 'r1', 'dev'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
for name, wt in trees.items():
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/auth')) if os.path.islink(p)]; P('   wholesale node_modules links:', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('   shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + A + '/src', capture_output=True, text=True); P('   resolve from auth:', p.stdout.strip(), p.stderr.strip()[:300])
P('toolchain: node', run(['node', '--version'])[1].strip(), '| vitest (farm)', json.load(open(REPO + '/' + DEV + '/node_modules/vitest/package.json'))['version'], '| typescript (farm)', json.load(open(REPO + '/' + DEV + '/node_modules/typescript/package.json'))['version'])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1032r2 end', now('%H:%M:%S %Z'))
