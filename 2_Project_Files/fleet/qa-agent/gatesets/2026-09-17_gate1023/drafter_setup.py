#!/usr/bin/env python3
"""drafter_setup.py — #1023 (KS-1207) TIER 1 ROUND 1 drafter substrate. Derived from the #1019r2 drafter_setup.py (same per-ENTRY farm via drafter_setup_farm.py, copied).
clone --shared --no-checkout by SHA into a fresh mktemp -d under /private/tmp/claude-501/drafter1023; worktrees IN THE CLONE: head = 2f74491eb, fix = 0f8b699b4,
dev = 581c9db0d (develop at drafting). merge-tree --write-tree ONLY in the clone. Farm per ENTRY where something runs (head, dev). Never rm. Checkout read-only readings before/after."""
import subprocess, os, tempfile, datetime, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafter_setup_farm import farm_tree
SCR = '/private/tmp/claude-501/drafter1023'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = os.path.dirname(os.path.abspath(__file__))
SHA = dict(head='2f74491ebd6211e722f778838339c55e8add008d', fix='0f8b699b41f26e1f4f688c93ba9b2ea595d6f207', m1='9bd0fd33356ab3a7d875420b5e7029f6ee9bbae2',
           dev='581c9db0db4201c42cbbf702f339b750989acdb1', olddev='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed', fixparent='d7e95cd9f153e9036ed77935a73c93504fa6e3dc')
DEV = 'Blockchain/Dev'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def reading(tag):
    wt = len(os.listdir(REPO + '/.git/worktrees')); rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    P('source checkout', tag, '| .git/worktrees entries', wt, '| porcelain lines', len(o.splitlines()), '| stderr', repr(e.strip()[:200])); return wt, len(o.splitlines())
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1023_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
trees = {}
for name in ('head', 'fix', 'dev'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
MT = {}
for a, b in (('fix', 'dev'), ('head', 'dev'), ('fix', 'olddev')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); k = a + 'x' + b; MT[k] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', k, 'rc', rc, 'tree', MT[k], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}', SHA['m1'] + '^{tree}']); ht, m1t = o.split()
P('head tree', ht, '= merge-tree fix x dev:', ht == MT['fixxdev'], '= merge-tree head x dev:', ht == MT['headxdev'], '| 9bd0fd333 tree', m1t, '= fix x olddev:', m1t == MT['fixxolddev'])
for name, wt in trees.items():
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD', 'HEAD:' + DEV + '/services/api-gateway/src/middleware/auth.ts']); P('tree', name, o.split())
for name in ('head', 'dev'):
    farm_tree(trees[name])
P('farm fix SKIPPED — the PR files at fix = head (asserted by the gate); nothing runs there in the drafter')
after = reading('AFTER'); P('checkout readings equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
