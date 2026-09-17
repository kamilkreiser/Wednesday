#!/usr/bin/env python3
"""drafter_setup_1035.py — #1035 (KS-1204) TIER 1 ROUND 1 drafter substrate (shape: drafter_setup_1032.py, services/api-gateway instead of auth).
clone --shared --no-checkout into a fresh mktemp -d under /private/tmp/claude-501/drafter1035; worktrees IN THE CLONE: head 4b1fb0621, dev 732c13459.
Merge-in IN THE CLONE ONLY: head is ONE commit whose parent is develop 732c13459; merge-tree --write-tree head x develop (= the head tree when develop is
unmoved); develop..head file set = verification.ts + the ks1204 test; numstat. node_modules farmed PER ENTRY (Dev/node_modules with @secuura relinked,
packages/shared, services/api-gateway), .vite/.vitest/.cache skipped; shared dist per tree; IN TREE asserted from api-gateway. Never rm. stderr kept.
The Secuura checkout: porcelain + .git/worktrees + refs + config sha + branch + api-gateway .vite read BEFORE/AFTER."""
import subprocess, os, tempfile, datetime, json, hashlib
SCR = '/private/tmp/claude-501/drafter1035'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1035'
SHA = dict(head='4b1fb0621e58ff00bba096751130bc6e53df4714', dev='732c13459d76f5b05ade94bb91de7e47585b0e7d')
DEV = 'Blockchain/Dev'; G = DEV + '/services/api-gateway'
VER = G + '/src/routes/verification.ts'; TEST = G + '/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts'
PER_ENTRY = ['packages/shared', 'services/api-gateway']
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
    vd = REPO + '/' + G + '/node_modules/.vite'
    vite = sorted(os.listdir(vd)) if os.path.isdir(vd) else 'ABSENT'
    r = dict(worktrees=wts, porcelain=len(o.splitlines()), refs=refs, config=cfg, branch=br, gateway_vite=vite)
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
P('drafter_setup_1035', now())
before = checkout_reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1035_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for k, v in SHA.items():
    P('object', k, v[:9], run(['git', '-C', C, 'cat-file', '-t', v])[1].strip(), '| parents', run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', v])[1].split()[1:], '| tree', run(['git', '-C', C, 'rev-parse', v + '^{tree}'])[1].strip())
trees = {}
for name in ('head', 'dev'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
parents = run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', SHA['head']])[1].split()[1:]
P('head parents', parents, '| one parent = develop 732c13459:', parents == [SHA['dev']])
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA['head'], SHA['dev']])
mt = o.strip().split('\n')[0]; ht = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}'])[1].strip()
P('merge-tree --write-tree (IN THE CLONE) head x develop rc', rc, 'tree', mt, '| head tree', ht, '| EQUAL' if mt == ht else '| DIFFER', '| extra lines', o.strip().split('\n')[1:][:4], e.strip()[:200])
dh = sorted(run(['git', '-C', C, 'diff', '--name-only', SHA['dev'], SHA['head']])[1].split()); P('develop..head files == {verification.ts, ks1204 test}:', dh == sorted([VER, TEST]), dh)
P('develop..head numstat:', run(['git', '-C', C, 'diff', '--numstat', SHA['dev'], SHA['head']])[1].strip().replace('\n', ' | '))
for p in (VER, TEST, G + '/src/services/enforcement.ts', G + '/src/routes/admin.ts', G + '/src/services/health.ts', G + '/src/services/redis.ts', G + '/src/index.ts',
          G + '/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts', G + '/vitest.config.ts', G + '/vitest.setup.ts', G + '/tsconfig.json', G + '/package.json',
          DEV + '/eslint.config.mjs', DEV + '/package-lock.json'):
    bd = run(['git', '-C', C, 'rev-parse', '--verify', '-q', SHA['dev'] + ':' + p])[1].strip() or 'ABSENT'
    bh = run(['git', '-C', C, 'rev-parse', '--verify', '-q', SHA['head'] + ':' + p])[1].strip() or 'ABSENT'
    P('blob', p.replace(DEV + '/', ''), 'develop', bd, 'head', bh, 'same' if bd == bh else 'CHANGED')
for name, wt in trees.items():
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, process.version)", wt], cwd=wt + '/' + G + '/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
after = checkout_reading('AFTER')
P('checkout bounds equal (porcelain, worktrees, branch):', (before['porcelain'], before['worktrees'], before['branch']) == (after['porcelain'], after['worktrees'], after['branch']))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree_head_x_dev': mt, 'head_tree': ht}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1035 end', now())
