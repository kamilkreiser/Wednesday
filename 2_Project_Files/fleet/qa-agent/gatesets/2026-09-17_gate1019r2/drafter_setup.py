#!/usr/bin/env python3
"""drafter_setup.py — #1019 (KS-1187) ROUND 2 delta drafter substrate. Derived from round 1's drafter_setup.py (the same per-ENTRY farm, via drafter_setup_farm.py).
clone --shared --no-checkout by SHA into a fresh mktemp -d under /private/tmp/claude-501/drafter1019r2; worktrees IN THE CLONE: r1 = 8b8996f8b (round-1 head),
r2 = 4d551f104 (the round-2 commit), head = 82f09c8bd (the merge of develop f8c7aaa39 into r2), dev = f8c7aaa39 (develop = merge-base of head), and
merged_local = r2 + a LOCAL --no-ff merge of f8c7aaa39 (re-predicts the seat's merge commit tree; nothing runs there, no farm). merge-tree --write-tree ONLY in the
clone. node_modules farmed PER ENTRY ONLY where something runs; shared dist per tree; IN TREE asserted. Never rm. stderr kept. The Secuura checkout: worktree
entries + porcelain read BEFORE and AFTER (read verbs only)."""
import subprocess, os, tempfile, datetime, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafter_setup_farm import farm_tree
SCR = '/private/tmp/claude-501/drafter1019r2'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019r2'
SHA = dict(r1='8b8996f8b290ef55c35721c30f8671f982fa5a91', r2='4d551f1046b55209b9ca5e4281e2cb9a868f67c2', head='82f09c8bd1bfab28e4d23c180cbaffea251685be',
           dev='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed', oldbase='fa887f382b212b8da4a0a4a556bacb05ea34daaa', pr1020='71bd80a35b406b9c99c7b96955a7521032d33c20',
           sq1017='d7e95cd9f153e9036ed77935a73c93504fa6e3dc')
DEV = 'Blockchain/Dev'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain'])
    rc2, o2, e2 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    P('source checkout', tag, '| worktree entries', o.count('worktree '), '| porcelain lines', len(o2.splitlines()), '| stderr', repr((e + e2).strip()[:200]))
    return o.count('worktree '), len(o2.splitlines())
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = checkout_reading('BEFORE')
W = tempfile.mkdtemp(prefix='gate1019r2_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
GI = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
def add(name, at):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, at]); assert rc == 0, e
    trees[name] = wt; return wt
for name in ('r1', 'r2', 'head', 'dev'):
    add(name, SHA[name])
MT = {}
for a, b in (('r2', 'dev'), ('head', 'dev'), ('r1', 'dev'), ('r2', 'pr1020'), ('r2', 'oldbase')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); k = a + 'x' + b; MT[k] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', k, SHA[a][:9], SHA[b][:9], 'rc', rc, 'tree', MT[k], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}']); P('head commit tree', o.strip(), '| = merge-tree r2 x dev:', o.strip() == MT['r2xdev'], '| = merge-tree head x dev:', o.strip() == MT['headxdev'])
mw = add('merged_local', SHA['r2'])
rc, o, e = run(GI + [mw, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge of develop f8c7aaa39 into 4d551f104', SHA['dev']]); P('local merge r2 <- dev rc', rc, (o + e).strip()[-300:]); assert rc == 0
rc, o, e = run(['git', '-C', mw, 'rev-parse', 'HEAD', 'HEAD^{tree}']); P('merged_local commit + tree', o.split())
for name, wt in trees.items():
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway', 'HEAD:' + DEV + '/services/api-gateway/src/routes/proxy.ts']); P('   root/shared/api-gateway tree, proxy blob', o.split())
for name, wt in trees.items():
    if name == 'merged_local': P('farm', name, 'SKIPPED — nothing runs in the local merge tree'); continue
    farm_tree(wt)
after = checkout_reading('AFTER')
P('source checkout worktree entries + porcelain equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
