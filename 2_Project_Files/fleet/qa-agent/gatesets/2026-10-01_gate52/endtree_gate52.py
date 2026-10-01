#!/usr/bin/env python3
"""endtree_gate52.py — THREE instruments per END_TREE, in the SCRATCH clone only (writes: a temp index under <scratchpad>/g52_sp/, objects).
END_TREE_A (#1367 squashed onto develop):
  (1) pin_gate52.py (F): merge-tree --write-tree develop A + commit-tree -p develop      (2) A's own tree (its parent == develop, 0 behind)
  (3) GitHub's test-merge refs/pull/<A>/merge tree (fetched into the scratch clone only)
END_TREE_B (#1368 merged after A):
  (1) pin_gate52.py (F): merge-tree --write-tree SQ_A B + commit-tree -p SQ_A          (2) merge-tree --write-tree A B (the seat's way)
  (3) INDEPENDENT ASSEMBLY: `git diff develop B` applied with `git apply --cached` onto END_TREE_A under a temp index, write-tree
CONTROLS that must DIFFER: develop's own tree; GitHub's refs/pull/<B>/merge tree (B ALONE on develop, not after A).
Prints each tree; the pinned END_TREE_A and END_TREE_B must each appear exactly three times on the instrument lines. rc 0 all agree / rc 1.
Usage: endtree_gate52.py <scratchpad>"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate52.json'), encoding='utf-8'))
SP = sys.argv[1]; CL = os.path.join(SP, 'g52_sp', 'clone'); NA, NB = K['order']
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
def git(*a, env=None, inp=None):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=env, input=inp)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:80], r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()
DEV = P['develop']; HA = P['pr_pins'][NA]['head']; HB = P['pr_pins'][NB]['head']; EA = P['end_tree_a']; EB = P['end_tree_b']
print(datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
git('fetch', '-q', 'origin', '+refs/pull/%s/merge:refs/remotes/prm/%s' % (NA, NA), '+refs/pull/%s/merge:refs/remotes/prm/%s' % (NB, NB))
ma = git('rev-parse', 'refs/remotes/prm/%s' % NA); mb = git('rev-parse', 'refs/remotes/prm/%s' % NB)
lines = []
lines.append('A(1) pin_gate52.py (F): merge-tree --write-tree develop #%s + commit-tree -p develop -> %s' % (NA, EA))
lines.append('A(2) #%s head\'s own tree (parent %s == develop: %s, behind %d): %s' % (NA, P['pr_pins'][NA]['parent'][:12], P['pr_pins'][NA]['parent'] == DEV, P['pr_pins'][NA]['behind'], git('rev-parse', HA + '^{tree}')))
lines.append('A(3) GitHub refs/pull/%s/merge %s parents %s: tree %s' % (NA, ma, git('log', '-1', '--format=%P', ma), git('rev-parse', ma + '^{tree}')))
lines.append('B(1) pin_gate52.py (F): merge-tree --write-tree SQ_A #%s + commit-tree -p SQ_A -> %s' % (NB, EB))
lines.append('B(2) merge-tree --write-tree #%s #%s (the seat\'s way): %s' % (NA, NB, git('merge-tree', '--write-tree', HA, HB).split('\n')[0]))
idx = os.path.join(SP, 'g52_sp', 'idx.endtree.%d' % os.getpid()); env = dict(os.environ, GIT_INDEX_FILE=idx)
git('read-tree', EA, env=env); d = git('diff', '--binary', DEV, HB) + '\n'
git('apply', '--cached', env=env, inp=d)
lines.append('B(3) INDEPENDENT ASSEMBLY: git diff develop #%s applied --cached onto END_TREE_A under a temp index, write-tree: %s' % (NB, git('write-tree', env=env)))
for l in lines: print(l)
print('CONTROL develop\'s own tree differs: %s' % git('rev-parse', DEV + '^{tree}'))
print('CONTROL GitHub refs/pull/%s/merge %s (#%s ALONE on develop) tree differs: %s' % (NB, mb[:12], NB, git('rev-parse', mb + '^{tree}')))
ca = sum(l.count(EA) for l in lines if l.startswith('A(')); cb = sum(l.count(EB) for l in lines if l.startswith('B('))
ok = ca == 3 and cb == 3 and git('rev-parse', DEV + '^{tree}') not in (EA, EB) and git('rev-parse', mb + '^{tree}') != EB and EB == K['end_tree_after_b_predicted']
print('ENDTREE %s: END_TREE_A %s read by %d of 3 instruments | END_TREE_B %s read by %d of 3 | == the seat\'s PREDICTED %s: %s' % (
    'AGREE' if ok else 'DISAGREE', EA, ca, EB, cb, K['end_tree_after_b_predicted'], EB == K['end_tree_after_b_predicted']))
raise SystemExit(0 if ok else 1)
