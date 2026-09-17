#!/usr/bin/env python3
"""drafter_setup_1028.py — #1028 (KS-744) TIER 1 drafter substrate + merge-by-content re-derivation. Derived from gate1023/drafter_setup.py.
The Secuura checkout gets READ verbs only (status, rev-parse via the clone's alternates). `git clone --shared --no-checkout` into a fresh mktemp -d under
GS/scratch/; worktrees, merge-tree --write-tree and every other write verb run IN THE CLONE only. Worktrees: head = e39521cfb, dev = 19f1e5475 (the PR
merge-base; develop's api-gateway + shared subtrees asserted equal at the current develop), pre = fb503741a (not farmed; blob source). Farm per ENTRY
(head, dev). Never rm, never cd. Checkout readings before/after."""
import subprocess, os, tempfile, datetime, json, sys, hashlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafter_setup_farm import farm_tree
GS = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SHA = dict(head='e39521cfb54cb5fd47c6bdae64ce707b3c9befce', pre='fb503741a7481bf659705cfcfa661f64b8e4ab4d', fix='6252f06ac7c913619888cb20e07cc5a0c846043d',
           dev='19f1e54750ce2b65312a687add2db4f5628edb7d', olddev='81ee4b729e86a645fc9098aafa1aaf39035a9950', fixparent='d7e95cd9f153e9036ed77935a73c93504fa6e3dc')
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'; SH = DEV + '/packages/shared'; AU = GW + '/src/middleware/auth.ts'
T744 = GW + '/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts'
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def reading(tag):
    wt = len(os.listdir(REPO + '/.git/worktrees')); rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    rc2, br, _ = run(['git', '-C', REPO, 'branch', '--show-current'])
    P('source checkout', tag, now(), '| .git/worktrees', wt, '| porcelain lines', len(o.splitlines()), '| .git/config sha256', cfg, '| branch', br.strip(), '| stderr', repr(e.strip()[:200]))
    return wt, len(o.splitlines()), cfg
P('drafter_setup_1028', now())
before = reading('BEFORE')
rc, lsr, e = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1028/head']); P('ls-remote rc', rc, lsr.strip().replace('\n', ' | '), e.strip()[:200])
CUR = [l.split()[0] for l in lsr.splitlines() if l.endswith('refs/heads/develop')][0]
os.makedirs(GS + '/scratch', exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1028_draft_', dir=GS + '/scratch'); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone --shared rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', CUR]); P('current develop', CUR, 'object in clone:', o.strip(), e.strip()[:120]); assert o.strip() == 'commit'
SHA['curdev'] = CUR
def rp(x): rc, o, e = run(['git', '-C', C, 'rev-parse', x]); assert rc == 0, (x, e); return o.strip()
def plusminus(a, b, path):
    rc, o, e = run(['git', '-C', C, 'diff', '--no-color', '-U0', a, b, '--', path]); assert rc == 0, e
    return sorted(l for l in o.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith('+++') and not l.startswith('---'))
def names(a, b):
    rc, o, e = run(['git', '-C', C, 'diff', '--name-only', a, b]); assert rc == 0, e; return sorted(o.split())
P('\n== commit graph')
for k in ('head', 'pre', 'fix'):
    rc, o, e = run(['git', '-C', C, 'log', '-1', '--format=%H parents %P | %s', SHA[k]]); P('  ', k, o.strip())
P('  merge-base(head, dev)', rp_mb := run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']])[1].strip(), '= dev:', rp_mb == SHA['dev'])
P('  merge-base(head, curdev)', run(['git', '-C', C, 'merge-base', SHA['head'], CUR])[1].strip())
P('  merge-base(pre, dev)', run(['git', '-C', C, 'merge-base', SHA['pre'], SHA['dev']])[1].strip(), '(want olddev 81ee4b729)')
P('\n== merge-by-content (the builder claims; re-derived here)')
MT = {}
for a, b in (('pre', 'dev'), ('head', 'dev'), ('head', 'curdev'), ('fix', 'olddev')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); lines = o.strip().split('\n') if o.strip() else ['']
    MT[a + 'x' + b] = lines[0]; P('  merge-tree --write-tree (IN THE CLONE)', a, 'x', b, 'rc', rc, 'tree', lines[0], '| conflicted-name lines', len(lines) - 1, e.strip()[:200])
HT = rp(SHA['head'] + '^{tree}'); PT = rp(SHA['pre'] + '^{tree}')
P('  head tree', HT, '| = merge-tree pre x dev:', HT == MT['prexdev'], '| = merge-tree head x dev:', HT == MT['headxdev'], '| READY prediction b61ed1776 prefix match:', HT.startswith('b61ed1776'))
P('  pre (fb503741a) tree', PT, '| = merge-tree fix x olddev:', PT == MT['fixxolddev'])
P('  MERGED over current develop', CUR[:9], '=', MT['headxcurdev'])
for sub in (GW, SH, DEV + '/services/auth'):
    vals = {k: rp(SHA[k] + ':' + sub) for k in ('head', 'dev', 'curdev', 'pre')}; vals['merged'] = rp(MT['headxcurdev'] + ':' + sub)
    P('  subtree', sub.replace(DEV + '/', ''), {k: v[:9] for k, v in vals.items()}, '| merged = head:', vals['merged'] == vals['head'], '| curdev = dev:', vals['curdev'] == vals['dev'])
A = plusminus(SHA['olddev'], SHA['pre'], AU); B = plusminus(SHA['olddev'], SHA['dev'], AU)
Cc = plusminus(SHA['dev'], SHA['head'], AU); Dd = plusminus(SHA['pre'], SHA['head'], AU)
P('  auth.ts branch change 81ee4b729..fb503741a: +%d -%d' % (sum(l[0] == '+' for l in A), sum(l[0] == '-' for l in A)), '| develop change 81ee4b729..19f1e5475: +%d -%d' % (sum(l[0] == '+' for l in B), sum(l[0] == '-' for l in B)))
P('  SET-EQUALITY 19f1e5475..head (auth.ts) == branch change:', Cc == A, '| fb503741a..head (auth.ts) == develop change (KS-1207):', Dd == B, '| overlap branch/develop line sets:', len(set(A) & set(B)))
P('  CONTROL (must be False): develop change == branch change:', A == B, '| planted: branch change + one extra line equal:', A + ['+planted'] == Cc)
rc, o, e = run(['git', '-C', C, 'diff', '-U0', SHA['olddev'], SHA['pre'], '--', AU]); P('  branch hunk headers', re.findall(r'^@@[^@]*@@', o, re.M))
rc, o, e = run(['git', '-C', C, 'diff', '-U0', SHA['olddev'], SHA['dev'], '--', AU]); P('  develop hunk headers', re.findall(r'^@@[^@]*@@', o, re.M))
P('  files dev..head', names(SHA['dev'], SHA['head']), '| CONTROL files fixparent..head count', len(names(SHA['fixparent'], SHA['head'])))
P('  files olddev..pre', names(SHA['olddev'], SHA['pre']))
for k in ('fix', 'pre', 'head', 'dev', 'olddev', 'curdev'):
    try: t = rp(SHA[k] + ':' + T744)
    except AssertionError: t = 'ABSENT'
    P('  blobs @', k, SHA[k][:9], 'auth.ts', rp(SHA[k] + ':' + AU)[:9], '| ks744 test', t[:9])
P('  files dev..curdev', names(SHA['dev'], CUR))
P('\n== worktrees + farm')
trees = {}
for name in ('head', 'dev', 'pre'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
    P('  worktree', name, run(['git', '-C', wt, 'rev-parse', 'HEAD'])[1].strip())
for name in ('head', 'dev'):
    farm_tree(trees[name])
P('  farm pre SKIPPED (blob source only)')
after = reading('AFTER'); P('checkout readings equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1028 end', now())
