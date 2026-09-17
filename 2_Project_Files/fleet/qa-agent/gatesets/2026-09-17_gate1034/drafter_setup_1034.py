#!/usr/bin/env python3
"""drafter_setup_1034.py WORKDIR — #1034 (KS-1215) TIER 1 drafter substrate + merge-in re-derivation. Derived from gate1028/drafter_setup_1028.py.
The Secuura checkout gets READ verbs only (status --porcelain, ls-remote, branch --show-current, for-each-ref; objects are read through the clone's
alternates). `git clone --shared --no-checkout` into WORKDIR (a fresh mktemp -d under /private/tmp/claude-501/drafter1034/); worktrees,
merge-tree --write-tree, patch-id and every other write verb run IN THE CLONE only.
Worktrees: head = fd81a75f0, dev = 27e53ec3a (the head's second parent = merge-base), pre = 0a2b1603f (develop before #1030/#1029; the fix's parent,
blob source, not farmed), fix = 6c6fdc94e (not farmed).
Farm per ENTRY (head, dev) from the checkout install (vitest 4.1.10), then the EIGHT hoisted entries whose version differs in develop 27e53ec3a's
Dev lock (vitest + 7 @vitest/*: 4.1.10 -> 4.1.11) are pointed at a side install (WORKDIR/vitest41111, exact lock pins, --ignore-scripts).
Never rm, never cd. Checkout readings before/after."""
import subprocess, os, datetime, json, sys, hashlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
GS = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
W = sys.argv[1]; assert W.startswith('/private/tmp/claude-501/drafter1034/') and os.path.isdir(W) and not os.listdir(W), 'WORKDIR must be a fresh empty mktemp -d'
SHA = dict(head='fd81a75f0688f6cbe1e5f79b061bb1369c88f477', dev='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d', pre='0a2b1603fe52f0f3b8152588af78bbeab0237be7',
           fix='6c6fdc94e869c98a73e6ffaa1b66be1d3b20d7b3')
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'; SH = DEV + '/packages/shared'; AU = GW + '/src/middleware/auth.ts'
T1215 = GW + '/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, inp=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, input=inp); return p.returncode, p.stdout, p.stderr
def reading(tag):
    wt = len(os.listdir(REPO + '/.git/worktrees')); rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    P('source checkout', tag, now(), '| .git/worktrees', wt, '| porcelain lines', len(o.splitlines()), '| .git/config sha256', cfg, '| refs', refs, '| branch', br, '| stderr', repr(e.strip()[:200]))
    return wt, len(o.splitlines()), cfg
P('drafter_setup_1034', now(), 'load', '%.1f/%.1f/%.1f' % os.getloadavg())
before = reading('BEFORE')
rc, lsr, e = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1034/head']); P('ls-remote rc', rc, lsr.strip().replace('\n', ' | '), e.strip()[:200])
CUR = [l.split()[0] for l in lsr.splitlines() if l.endswith('refs/heads/develop')][0]
PRH = [l.split()[0] for l in lsr.splitlines() if l.endswith('refs/pull/1034/head')][0]
assert PRH == SHA['head'], 'HEAD MOVED — STOP'
C = W + '/clone'
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone --shared rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', CUR]); P('current develop', CUR, 'object in clone:', o.strip(), e.strip()[:120]); assert o.strip() == 'commit'
SHA['curdev'] = CUR
def rp(x):
    rc, o, e = run(['git', '-C', C, 'rev-parse', '--verify', '-q', x]); return o.strip() if rc == 0 else 'ABSENT'
def names(a, b):
    rc, o, e = run(['git', '-C', C, 'diff', '--name-only', a, b]); assert rc == 0, e; return sorted(o.split('\n')[:-1] if o else [])
def patchid(a, b, path=None):
    rc, o, e = run(['git', '-C', C, 'diff', a, b] + (['--', path] if path else [])); rc2, o2, e2 = run(['git', '-C', C, 'patch-id', '--stable'], inp=o); return (o2.split() or ['EMPTY'])[0][:12]
P('\n== commit graph')
for k in ('head', 'fix'):
    P('  ', k, run(['git', '-C', C, 'log', '-1', '--format=%H parents %P | %s', SHA[k]])[1].strip())
mb = run(['git', '-C', C, 'merge-base', SHA['fix'], SHA['dev']])[1].strip(); P('  merge-base(fix, dev)', mb, '= pre 0a2b1603f:', mb == SHA['pre'])
P('  merge-base(head, dev)', run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']])[1].strip(), '| head^2 = dev:', rp(SHA['head'] + '^2') == SHA['dev'], '| head^1 = fix:', rp(SHA['head'] + '^1') == SHA['fix'])
P('  dev is ancestor of head (merge-base --is-ancestor rc 0):', run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']])[0] == 0, '| curdev ancestor of head:', run(['git', '-C', C, 'merge-base', '--is-ancestor', CUR, SHA['head']])[0] == 0)
P('\n== merge-in by content (the builder claims; re-derived)')
MT = {}
for a, b in (('fix', 'dev'), ('head', 'curdev'), ('fix', 'pre')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); lines = o.strip().split('\n') if o.strip() else ['']
    MT[a + 'x' + b] = lines[0]; P('  merge-tree --write-tree (IN THE CLONE)', a, 'x', b, 'rc', rc, 'tree', lines[0], '| conflicted-name lines', len(lines) - 1, e.strip()[:200])
HT = rp(SHA['head'] + '^{tree}')
P('  head tree', HT, '| = merge-tree fix x dev:', HT == MT['fixxdev'], '| READY 6339c404c prefix:', HT.startswith('6339c404c'), '| merged over current develop', CUR[:9], '=', MT['headxcurdev'], '= head tree:', MT['headxcurdev'] == HT)
dd = names(SHA['pre'], SHA['dev']); fh = names(SHA['fix'], SHA['head'])
P('  develop own delta pre..dev files', len(dd), '| brought fix..head files', len(fh), '| equal name sets:', dd == fh)
blob_eq = all(rp(SHA['head'] + ':' + f) == rp(SHA['dev'] + ':' + f) for f in fh)
P('  every brought file blob at head == at develop 27e53ec3a:', blob_eq, '| CONTROL (must be False): every brought file head == pre:', all(rp(SHA['head'] + ':' + f) == rp(SHA['pre'] + ':' + f) for f in fh))
P('  brought - develop delta =', sorted(set(fh) - set(dd)), '| develop delta - brought =', sorted(set(dd) - set(fh)))
pd = names(SHA['dev'], SHA['head']); P('  dev..head files', pd, '| CONTROL pre..head count', len(names(SHA['pre'], SHA['head'])))
P('  pre..dev touches auth.ts or the ks1215 test:', [f for f in dd if f in (AU, T1215)], '| api-gateway files in develop delta:', [f for f in dd if f.startswith(GW)])
P('  patch-id pre..fix', patchid(SHA['pre'], SHA['fix']), '= dev..head', patchid(SHA['dev'], SHA['head']), '| CONTROL pre..dev', patchid(SHA['pre'], SHA['dev']))
for k in ('pre', 'fix', 'dev', 'head', 'curdev'):
    P('  blobs @', k, SHA[k][:9], 'auth.ts', rp(SHA[k] + ':' + AU)[:9], '| ks1215 test', rp(SHA[k] + ':' + T1215)[:9], '| index.ts', rp(SHA[k] + ':' + GW + '/src/index.ts')[:9])
for sub in (GW, GW + '/src', SH, SH + '/src', DEV + '/services/auth'):
    vals = {k: rp(SHA[k] + ':' + sub)[:9] for k in ('pre', 'dev', 'head', 'curdev')}; vals['merged'] = rp(MT['headxcurdev'] + ':' + sub)[:9]
    P('  subtree', sub.replace(DEV + '/', ''), vals)
P('  files dev..curdev', names(SHA['dev'], CUR))
P('\n== worktrees')
trees = {}
for name in ('head', 'dev', 'pre'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
    P('  worktree', name, run(['git', '-C', wt, 'rev-parse', 'HEAD'])[1].strip())
after = reading('AFTER'); P('checkout readings equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1034 end', now())
