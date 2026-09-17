#!/usr/bin/env python3
"""repin_setup_1034.py WORKDIR — RE-PIN of the #1034 (KS-1215) gate set from fd81a75f0 to e4624218b (develop 3961c2add). Derived from drafter_setup_1034.py.
Checkout: READ verbs only (status --porcelain, ls-remote, branch --show-current, for-each-ref, rev-parse). `git clone --shared --no-checkout` into WORKDIR
(a fresh mktemp -d under the re-pinner's scratch gate1034r/); worktrees + merge-tree --write-tree + patch-id IN THE CLONE only. Never rm, never cd."""
import subprocess, os, datetime, json, sys, hashlib
GS = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
W = sys.argv[1]; assert '/scratchpad/gate1034r/wd_' in W and os.path.isdir(W) and not os.listdir(W), 'WORKDIR must be a fresh empty mktemp -d'
SHA = dict(head='e4624218bc29cda4c07b2d31ca18bba422cfbc3e', dev='3961c2add8e1637b32e638f8f0952c328c00833e', mergein='96d859467f32658c9d0f58283bb6fea13ca6f4d4',
           old='fd81a75f0688f6cbe1e5f79b061bb1369c88f477', olddev='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d', fix='6c6fdc94e869c98a73e6ffaa1b66be1d3b20d7b3', pre='0a2b1603fe52f0f3b8152588af78bbeab0237be7')
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'; SH = DEV + '/packages/shared'
AU = GW + '/src/middleware/auth.ts'; PL = GW + '/src/routes/platform.ts'; IX = GW + '/src/index.ts'
T1215 = GW + '/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, inp=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, input=inp); return p.returncode, p.stdout, p.stderr
def reading(tag):
    wt = len(os.listdir(REPO + '/.git/worktrees')); rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    vite = os.path.isdir(REPO + '/' + GW + '/node_modules/.vite')
    P('source checkout', tag, now(), '| .git/worktrees', wt, '| porcelain lines', len(o.splitlines()), '| .git/config sha256', cfg, '| refs', refs, '| branch', br, '| api-gateway node_modules/.vite present', vite, '| stderr', repr(e.strip()[:200]))
    return wt, len(o.splitlines()), cfg
P('repin_setup_1034', now(), 'load', '%.1f/%.1f/%.1f' % os.getloadavg())
before = reading('BEFORE')
rc, lsr, e = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1034/head']); P('ls-remote', now(), 'rc', rc, lsr.strip().replace('\n', ' | '), e.strip()[:200])
CUR = [l.split()[0] for l in lsr.splitlines() if l.endswith('refs/heads/develop')][0]
PRH = [l.split()[0] for l in lsr.splitlines() if l.endswith('refs/pull/1034/head')][0]
assert PRH == SHA['head'], 'HEAD MOVED AGAIN — STOP'
assert CUR == SHA['dev'], 'develop moved from 3961c2add — judge before re-pinning'
C = W + '/clone'
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone --shared rc', rc, e.strip()[:200]); assert rc == 0
def rp(x):
    rc, o, e = run(['git', '-C', C, 'rev-parse', '--verify', '-q', x]); return o.strip() if rc == 0 else 'ABSENT'
def names(a, b):
    rc, o, e = run(['git', '-C', C, 'diff', '--name-only', a, b]); assert rc == 0, e; return sorted(o.split('\n')[:-1] if o else [])
def patchid(a, b, *paths):
    rc, o, e = run(['git', '-C', C, 'diff', a, b] + (['--'] + list(paths) if paths else [])); rc2, o2, e2 = run(['git', '-C', C, 'patch-id', '--stable'], inp=o); return (o2.split() or ['EMPTY'])[0][:12]
P('\n== commit graph')
for k in ('head', 'mergein', 'old', 'fix'):
    P('  ', k, run(['git', '-C', C, 'log', '-1', '--format=%H parents %P tree %T | %s', SHA[k]])[1].strip())
P('  first-parent chain head^1 = mergein:', rp(SHA['head'] + '^1') == SHA['mergein'], '| head has 1 parent:', rp(SHA['head'] + '^2') == 'ABSENT', '| mergein^1 = old fd81a75f0:', rp(SHA['mergein'] + '^1') == SHA['old'], '| mergein^2 = develop 3961c2add:', rp(SHA['mergein'] + '^2') == SHA['dev'])
mb = run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']])[1].strip(); P('  merge-base(head, develop)', mb, '= develop 3961c2add:', mb == SHA['dev'], '= origin develop now:', mb == CUR)
P('  develop ancestor of head (is-ancestor rc 0):', run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']])[0] == 0, '| old head fd81a75f0 ancestor of head (fast-forward):', run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['old'], SHA['head']])[0] == 0)
P('  rev-list --count develop..head', run(['git', '-C', C, 'rev-list', '--count', SHA['dev'] + '..' + SHA['head']])[1].strip(), '| head..develop', run(['git', '-C', C, 'rev-list', '--count', SHA['head'] + '..' + SHA['dev']])[1].strip())
P('\n== three-dot delta develop...head (= two-dot, develop is the merge-base)')
dd = names(SHA['dev'], SHA['head']); P('  files', len(dd), dd)
P('  numstat', run(['git', '-C', C, 'diff', '--numstat', SHA['dev'], SHA['head']])[1].strip().replace('\n', ' | '))
P('  CONTROL old pin 27e53ec3a..fd81a75f0 files', len(names(SHA['olddev'], SHA['old'])), '| CONTROL 27e53ec3a..head files', len(names(SHA['olddev'], SHA['head'])))
P('\n== merge-in by content')
MT = {}
for a, b in (('old', 'dev'), ('head', 'dev')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); lines = o.strip().split('\n') if o.strip() else ['']
    MT[a + 'x' + b] = lines[0]; P('  merge-tree --write-tree (IN THE CLONE)', a, SHA[a][:9], 'x', b, SHA[b][:9], 'rc', rc, 'tree', lines[0], '| conflicted-name lines', len(lines) - 1, e.strip()[:200])
HT = rp(SHA['head'] + '^{tree}'); MIT = rp(SHA['mergein'] + '^{tree}')
P('  mergein 96d859467 tree', MIT, '= merge-tree fd81a75f0 x 3961c2add:', MIT == MT['oldxdev'], '| = drafter prediction 92256f2df:', MIT.startswith('92256f2df'))
P('  head tree', HT, '| merged tree over current develop = merge-tree head x develop', MT['headxdev'], '= head tree:', MT['headxdev'] == HT)
bro = names(SHA['old'], SHA['mergein']); devd = names(SHA['olddev'], SHA['dev'])
P('  brought fd81a75f0..96d859467 files', len(bro), '| develop own delta 27e53ec3a..3961c2add files', len(devd), '| equal name sets:', bro == devd)
P('  every brought blob at mergein == at develop 3961c2add:', all(rp(SHA['mergein'] + ':' + f) == rp(SHA['dev'] + ':' + f) for f in bro), '| CONTROL (must be False) every brought blob == at fd81a75f0:', all(rp(SHA['mergein'] + ':' + f) == rp(SHA['old'] + ':' + f) for f in bro))
P('  api-gateway or packages/shared files in develop delta:', [f for f in devd if f.startswith(GW) or f.startswith(SH)])
fixd = names(SHA['mergein'], SHA['head']); P('  the pre-gate fix 96d859467..head files', fixd)
P('  patch-id auth.ts: 0a2b1603f..6c6fdc94e', patchid(SHA['pre'], SHA['fix'], AU), '= develop..head', patchid(SHA['dev'], SHA['head'], AU), '| platform.ts: mergein..head', patchid(SHA['mergein'], SHA['head'], PL), '= develop..head', patchid(SHA['dev'], SHA['head'], PL), '| CONTROL auth.ts develop..head vs platform', patchid(SHA['dev'], SHA['head'], PL) != patchid(SHA['dev'], SHA['head'], AU))
for k in ('olddev', 'dev', 'old', 'mergein', 'head'):
    P('  blobs @', k, SHA[k][:9], '| auth.ts', rp(SHA[k] + ':' + AU)[:9], '| platform.ts', rp(SHA[k] + ':' + PL)[:9], '| ks1215 test', rp(SHA[k] + ':' + T1215)[:9], '| index.ts', rp(SHA[k] + ':' + IX)[:9])
for sub in (GW, GW + '/src', SH, SH + '/src'):
    P('  subtree', sub.replace(DEV + '/', ''), {k: rp(SHA[k] + ':' + sub)[:9] for k in ('olddev', 'dev', 'old', 'mergein', 'head')})
P('\n== worktrees')
trees = {}
for name in ('head', 'dev'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
    P('  worktree', name, run(['git', '-C', wt, 'rev-parse', 'HEAD'])[1].strip())
after = reading('AFTER'); P('checkout readings equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/repin_paths.json', 'w'), indent=1)
P('repin_setup_1034 end', now())
