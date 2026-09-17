#!/usr/bin/env python3
"""drafter_setup_1029.py — #1029 (KS-1180 part 1) TIER 2 drafter substrate + merge-in re-derivation. Shape: gate1028/drafter_setup_1028.py.
The Secuura checkout gets READ verbs only (status, rev-parse, ls-remote, for-each-ref count). `git clone --shared --no-checkout` into a fresh mktemp -d
under GS/scratch/; merge-tree --write-tree, commit-tree, worktree add run IN THE CLONE only. Worktrees: head = cd3580e1f, dev = the CURRENT develop
(75ad0e55c at draft), merged = commit-tree(merge-tree head x current develop). Farm per ENTRY (head, dev, merged). Never rm, never cd.
Checkout readings before/after."""
import subprocess, os, tempfile, datetime, json, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafter_setup_farm import farm_tree
GS = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SHA = dict(head='cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc', m1='7553821fccea2fc566037dd173ecd0e1d1dea0c0', fix='a4dc0d8ee2527501cac4c3d7305a60cc22355c70',
           fixparent='d7e95cd9f153e9036ed77935a73c93504fa6e3dc', dev1='81ee4b729e86a645fc9098aafa1aaf39035a9950', dev2='20ab16f9a80c5c3c75e613d8c670efefd8f5cafb')
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'; SH = DEV + '/packages/shared'
TF = GW + '/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
BR = 'refs/heads/feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the'
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None, inp=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout, p.stderr
def reading(tag):
    wt = len(os.listdir(REPO + '/.git/worktrees')); rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    lsr = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1029/head', BR])[1].strip().replace('\n', ' | ')
    vite = datetime.datetime.fromtimestamp(os.stat(REPO + '/' + GW + '/node_modules/.vite/vitest').st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    P('source checkout', tag, now(), '| .git/worktrees', wt, '| porcelain lines', len(o.splitlines()), '| .git/config sha256', cfg, '| refs', refs, '| branch', br,
      '| api-gateway .vite/vitest mtime', vite, '| stderr', repr(e.strip()[:200]))
    P('  ls-remote', lsr)
    return wt, len(o.splitlines()), cfg, refs, vite, lsr
P('drafter_setup_1029', now())
before = reading('BEFORE')
CUR = [l.split()[0] for l in before[5].split(' | ') if l.endswith('refs/heads/develop')][0]
os.makedirs(GS + '/scratch', exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1029_draft_', dir=GS + '/scratch'); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone --shared rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', CUR]); P('current develop', CUR, 'object in clone:', o.strip(), e.strip()[:120]); assert o.strip() == 'commit'
SHA['curdev'] = CUR
def rp(x):
    rc, o, e = run(['git', '-C', C, 'rev-parse', '--verify', '--quiet', x]); return o.strip() if rc == 0 else 'ABSENT'
def names(a, b):
    rc, o, e = run(['git', '-C', C, 'diff', '--name-only', a, b]); assert rc == 0, e; return sorted(o.split())
def patchid(a, b, paths=None):
    rc, d, e = run(['git', '-C', C, 'diff', '--no-color', '--full-index', a, b] + (['--'] + paths if paths else [])); assert rc == 0, e
    rc, o, e = run(['git', '-C', C, 'patch-id', '--stable'], inp=d); return (o.split() or ['EMPTY'])[0], len(d)
P('\n== commit graph (first-parent chain + parents)')
for k in ('head', 'm1', 'fix'):
    P('  ', k, run(['git', '-C', C, 'log', '-1', '--format=%H parents %P tree %T | %s', SHA[k]])[1].strip())
P('  rev-list --count curdev..head', run(['git', '-C', C, 'rev-list', '--count', CUR + '..' + SHA['head']])[1].strip(), '| head..curdev', run(['git', '-C', C, 'rev-list', '--count', SHA['head'] + '..' + CUR])[1].strip())
P('  merge-base(head, curdev)', run(['git', '-C', C, 'merge-base', SHA['head'], CUR])[1].strip(), '| dev2 ancestor of curdev:', run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev2'], CUR])[0] == 0)
P('  merge-base(fix, dev1)', run(['git', '-C', C, 'merge-base', SHA['fix'], SHA['dev1']])[1].strip(), '(want fixparent d7e95cd9f)', '| merge-base(m1, dev2)', run(['git', '-C', C, 'merge-base', SHA['m1'], SHA['dev2']])[1].strip(), '(want dev1 81ee4b729)')
P('\n== the fix commit alone carries the PR change')
P('  files fixparent..fix', names(SHA['fixparent'], SHA['fix']))
P('  test blob fixparent', rp(SHA['fixparent'] + ':' + TF)[:9], '| fix', rp(SHA['fix'] + ':' + TF)[:9], '| m1', rp(SHA['m1'] + ':' + TF)[:9], '| head', rp(SHA['head'] + ':' + TF)[:9],
  '| dev1', rp(SHA['dev1'] + ':' + TF)[:9], '| dev2', rp(SHA['dev2'] + ':' + TF)[:9], '| curdev', rp(CUR + ':' + TF)[:9])
P('  patch-id fixparent..fix', patchid(SHA['fixparent'], SHA['fix']), '| dev2..head', patchid(SHA['dev2'], SHA['head']), '| curdev...head (merge-base)', patchid(run(['git', '-C', C, 'merge-base', SHA['head'], CUR])[1].strip(), SHA['head']))
P('\n== merge-ins brought only develop (merge-tree IN THE CLONE; name sets + patch-ids)')
MT = {}
for a, b, merge in (('fix', 'dev1', 'm1'), ('m1', 'dev2', 'head'), ('head', 'curdev', None)):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); lines = o.strip().split('\n') if o.strip() else ['']
    MT[a + 'x' + b] = lines[0]
    P('  merge-tree --write-tree', a, SHA[a][:9], 'x', b, SHA[b][:9], 'rc', rc, 'tree', lines[0], '| conflicted-name lines', len(lines) - 1, e.strip()[:200],
      ('| = tree(' + merge + ') ' + rp(SHA[merge] + '^{tree}') + ' ' + str(lines[0] == rp(SHA[merge] + '^{tree}'))) if merge else '')
for fp, dv, mg in (('fix', 'dev1', 'm1'), ('m1', 'dev2', 'head')):
    mb = run(['git', '-C', C, 'merge-base', SHA[fp], SHA[dv]])[1].strip()
    brought = names(SHA[fp], SHA[mg]); dev_delta = names(mb, SHA[dv])
    pa, la = patchid(SHA[fp], SHA[mg]); pb, lb = patchid(mb, SHA[dv])
    side = names(SHA[dv], SHA[mg])
    blobs_eq = all(rp(SHA[mg] + ':' + f) == rp(SHA[dv] + ':' + f) for f in brought)
    P('  merge', SHA[mg][:9], ': brought (first-parent diff) files', len(brought), '| develop delta', mb[:9], '..', SHA[dv][:9], 'files', len(dev_delta),
      '| SET EQUAL', brought == dev_delta, '| set difference', sorted(set(brought) ^ set(dev_delta))[:5])
    P('     patch-id brought', pa[:16], 'bytes', la, '| develop delta', pb[:16], 'bytes', lb, '| PATCH-ID EQUAL', pa == pb, '| every brought blob = develop blob', blobs_eq)
    P('     second-parent side (develop -> merge) files', side)
P('  CONTROL (must be False): merge-1 develop delta == merge-2 develop delta:', names(SHA['fixparent'], SHA['dev1']) == names(SHA['dev1'], SHA['dev2']))
HT = rp(SHA['head'] + '^{tree}')
M = MT['headxcurdev']
env = dict(os.environ, GIT_AUTHOR_NAME='qa-drafter-1029', GIT_AUTHOR_EMAIL='qa@invalid', GIT_COMMITTER_NAME='qa-drafter-1029', GIT_COMMITTER_EMAIL='qa@invalid',
           GIT_AUTHOR_DATE='2026-09-17T00:00:00Z', GIT_COMMITTER_DATE='2026-09-17T00:00:00Z')
rc, o, e = run(['git', '-C', C, 'commit-tree', M, '-p', SHA['head'], '-p', CUR, '-m', 'qa1029 drafter merged tree (clone only)'], env=env); MC = o.strip(); P('  commit-tree merged (clone only) rc', rc, MC, e.strip()[:120])
SHA['merged'] = MC
P('  MERGED tree over current develop', CUR[:9], '=', M, '| = head tree', HT == M, '| files curdev..merged', names(CUR, MC))
for sub in (GW, GW + '/src', SH, SH + '/src', DEV + '/services/auth'):
    vals = {k: rp(SHA[k] + ':' + sub) for k in ('head', 'dev2', 'curdev', 'merged')}
    P('  subtree', sub.replace(DEV + '/', ''), {k: v[:9] for k, v in vals.items()}, '| merged = head:', vals['merged'] == vals['head'], '| curdev = dev2:', vals['curdev'] == vals['dev2'])
P('  files dev2..curdev', names(SHA['dev2'], CUR))
P('\n== worktrees + farm')
trees = {}
for name in ('head', 'curdev', 'merged'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
    P('  worktree', name, run(['git', '-C', wt, 'rev-parse', 'HEAD'])[1].strip())
for name in ('head', 'curdev', 'merged'):
    farm_tree(trees[name])
after = reading('AFTER'); P('checkout readings equal before/after (worktrees, porcelain, config, refs, vite mtime):', before[:5] == after[:5])
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1029 end', now())
