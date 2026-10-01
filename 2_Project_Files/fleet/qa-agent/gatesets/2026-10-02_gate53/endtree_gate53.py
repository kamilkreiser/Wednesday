#!/usr/bin/env python3
"""endtree_gate53.py — FOUR instruments for END_TREE (#1369 squashed onto develop), in the SCRATCH clone only (writes: a temp index under
<scratchpad>/g53_sp/, objects, the refs/remotes/prm/<n> ref):
  (1) pin_gate53.py (F): merge-tree --write-tree develop head + commit-tree -p develop      (2) the head's own tree (its parent == develop, 0 behind)
  (3) GitHub's test-merge refs/pull/<n>/merge tree (fetched into the scratch clone only; its parents printed)
  (4) INDEPENDENT ASSEMBLY, no merge-tree: `git diff develop head` applied with `git apply --cached` onto develop under a temp index, write-tree
CONTROL that must DIFFER: develop's own tree. The pinned END_TREE must appear on all four instrument lines and equal kit end_tree_predicted.
rc 0 all agree / rc 1. Usage: endtree_gate53.py <scratchpad>"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.json'), encoding='utf-8'))
SP = sys.argv[1]; CL = os.path.join(SP, 'g53_sp', 'clone'); N = K['order'][0]
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
def git(*a, env=None, inp=None):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=env, input=inp)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:80], r.returncode, r.stderr.strip()[:300]))
    return r.stdout
DEV = P['develop']; H = P['pr_pins'][N]['head']; END = P['end_tree']
print('endtree_gate53 %s | develop %s | head %s | pinned END_TREE %s | the seat\'s PREDICTED %s' % (
    datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), DEV[:12], H[:12], END, K['end_tree_predicted']))
git('fetch', '-q', 'origin', '+refs/pull/%s/merge:refs/remotes/prm/%s' % (N, N))
m = git('rev-parse', 'refs/remotes/prm/%s' % N).strip()
idx = os.path.join(SP, 'g53_sp', 'idx.endtree.%d' % os.getpid()); env = dict(os.environ, GIT_INDEX_FILE=idx)
git('read-tree', DEV, env=env); git('apply', '--cached', '--whitespace=nowarn', '-', env=env, inp=git('diff', '--binary', DEV, H)); t4 = git('write-tree', env=env).strip()
L = ['(1) pin_gate53.py (F): merge-tree --write-tree develop #%s + commit-tree -p develop -> %s' % (N, END),
     '(2) #%s head\'s own tree (parent %s == develop: %s, behind %d): %s' % (N, P['pr_pins'][N]['parent'][:12], P['pr_pins'][N]['parent'] == DEV, P['pr_pins'][N]['behind'], git('rev-parse', H + '^{tree}').strip()),
     '(3) GitHub refs/pull/%s/merge %s parents %s: tree %s' % (N, m, git('log', '-1', '--format=%P', m).strip(), git('rev-parse', m + '^{tree}').strip()),
     '(4) INDEPENDENT: git diff develop..head applied --cached onto develop under a temp index, write-tree: %s' % t4]
for l in L: print(l)
dt = git('rev-parse', DEV + '^{tree}').strip()
print('CONTROL develop\'s own tree %s %s END_TREE' % (dt, '!=' if dt != END else '== (the control did NOT differ)'))
n = sum(l.rstrip().endswith(END) for l in L)
ok = n == 4 and dt != END and END == K['end_tree_predicted']
print('ENDTREE %s: END_TREE %s read by %d of 4 instruments | == the seat\'s PREDICTED: %s | develop\'s tree differs: %s' % ('AGREE' if ok else 'DISAGREE', END, n, END == K['end_tree_predicted'], dt != END))
raise SystemExit(0 if ok else 1)
