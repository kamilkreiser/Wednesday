#!/usr/bin/env python3
"""predict_merge_gate1036.py — the ONLY place a git write verb runs: a `git clone --shared --no-checkout` of the Secuura checkout into the
drafter's scratchpad (never a worktree of the checkout, never fetch/checkout/merge IN the checkout), then `git merge-tree --write-tree` of #1036's
head onto the CURRENT develop, in both orders; the merged tree's audit-baseline.json row count vs develop's and the head's (conservation); the merged
tree's delta to the head tree and to develop; optionally a fetch of refs/pull/1036/merge BY REF from origin INTO THE SCRATCH CLONE (the checkout's
deploy key, read-only ssh) to compare GitHub's own merge commit tree with the prediction. count-objects on the checkout before/after must be identical.
Usage: predict_merge_gate1036.py <scratchpad dir> <head> <develop>"""
import datetime, json, os, subprocess, sys, tempfile
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SP, HEAD, DEV = sys.argv[1], sys.argv[2], sys.argv[3]
D = 'Blockchain/Dev/'; BASELINE = D + 'scripts/audit/audit-baseline.json'
def run(args, cwd=None, check=True):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if check and p.returncode != 0: raise SystemExit('%r rc %d\n%s' % (args[:4], p.returncode, p.stderr[-500:]))
    return p
def git(*a, check=True): return run(['git', '-C', REPO] + list(a), check=check).stdout
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_merge_gate1036.py at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', now())
co_before = git('count-objects', '-v'); print('$ git -C REPO count-objects -v (BEFORE)\n' + co_before.rstrip())
clone = tempfile.mkdtemp(prefix='predict1036.', dir=SP) + '_c'
print('$ git clone --shared --no-checkout REPO', clone)
run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, clone])
def sg(*a, check=True): return run(['git', '-C', clone] + list(a), check=check)
print('  clone objects (count-objects -v in the clone; --shared = alternates, expect count 0):\n' + '\n'.join('    ' + l for l in sg('count-objects', '-v').stdout.splitlines()))
print('  alternates:', open(os.path.join(clone, '.git', 'objects', 'info', 'alternates')).read().strip())
for s in (HEAD, DEV):
    print('  cat-file -e %s^{commit} rc' % s[:9], sg('cat-file', '-e', s + '^{commit}', check=False).returncode)
mb = sg('merge-base', HEAD, DEV).stdout.strip(); print('$ git merge-base HEAD DEV =', mb)

# 1. merge-tree --write-tree, both orders
res = {}
for label, a, b in (('DEV<-HEAD', DEV, HEAD), ('HEAD<-DEV', HEAD, DEV)):
    p = sg('merge-tree', '--write-tree', '--name-only', a, b, check=False)
    lines = p.stdout.splitlines()
    tree = lines[0] if lines else ''
    conflicts = [l for l in lines[1:] if l.strip()]
    res[label] = (p.returncode, tree, conflicts)
    print('$ git merge-tree --write-tree --name-only %s %s -> rc %d tree %s conflicts %d %s' % (a[:9], b[:9], p.returncode, tree, len(conflicts), conflicts[:10]))
    if p.stderr.strip(): print('  stderr:', p.stderr.strip()[:300])
merged = res['DEV<-HEAD'][1]
print('  both orders give the same tree?', res['DEV<-HEAD'][1] == res['HEAD<-DEV'][1], '| rc both 0 (clean)?', res['DEV<-HEAD'][0] == 0 == res['HEAD<-DEV'][0])
head_tree = sg('rev-parse', HEAD + '^{tree}').stdout.strip(); dev_tree = sg('rev-parse', DEV + '^{tree}').stdout.strip()
print('  head tree', head_tree, '| develop tree', dev_tree, '| merged tree', merged)

# 2. the merged tree's audit-baseline vs develop's and the head's
def rows(treeish):
    return json.loads(sg('show', treeish + ':' + BASELINE).stdout)['accepted']
rd, rh, rm = rows(DEV), rows(HEAD), rows(merged)
bd, bh, bm = (sg('rev-parse', t + ':' + BASELINE).stdout.strip() for t in (DEV, HEAD, merged))
print('$ audit-baseline.json rows: develop %d (blob %s) | head %d (blob %s) | merged %d (blob %s)' % (len(rd), bd[:9], len(rh), bh[:9], len(rm), bm[:9]))
print('  merged == head blob?', bm == bh, '| develop minus merged =', sorted(set(rd) - set(rm)), '| merged minus develop =', sorted(set(rm) - set(rd)),
      '| CONSERVATION develop %d -> merged %d = exactly %d removed, %d added' % (len(rd), len(rm), len(set(rd) - set(rm)), len(set(rm) - set(rd))))

# 3. deltas: merged vs head (= develop's delta since mb), merged vs develop (= the PR's 50 paths at head blobs)
def names(a, b): return [x for x in sg('diff-tree', '-r', '--name-only', '-z', a, b).stdout.split('\0') if x]
m_vs_h = names(head_tree, merged); m_vs_d = names(dev_tree, merged); d_delta = names(mb + '^{tree}', dev_tree); pr = names(mb + '^{tree}', head_tree)
print('$ diff-tree head..merged | count', len(m_vs_h), '| == develop delta mb..DEV (%d) as a set?' % len(d_delta), sorted(m_vs_h) == sorted(d_delta))
print('$ diff-tree develop..merged | count', len(m_vs_d), '| == the PR paths mb..HEAD (%d) as a set?' % len(pr), sorted(m_vs_d) == sorted(pr))
raw_m = {l.split('\t')[1]: l.split()[3] for l in sg('diff-tree', '-r', '--abbrev=40', dev_tree, merged).stdout.splitlines()}
raw_h = {l.split('\t')[1]: l.split()[3] for l in sg('diff-tree', '-r', '--abbrev=40', mb + '^{tree}', head_tree).stdout.splitlines()}
print('  every PR path at its HEAD blob in the merged tree?', all(raw_m.get(p) == raw_h[p] for p in raw_h), '| mismatches:', [p for p in raw_h if raw_m.get(p) != raw_h[p]])
print('  develop-delta INTERSECT PR paths:', sorted(set(d_delta) & set(pr)))

# 4. GitHub's own merge ref, fetched BY REF into the SCRATCH clone only (read-only ssh with the checkout's deploy key); compare trees
ssh = git('config', '--get', 'core.sshCommand').strip()
p = run(['git', '-C', clone, '-c', 'core.sshCommand=' + ssh, 'fetch', '--quiet', '--no-tags', 'origin', '+refs/pull/1036/merge:refs/scratch/pull1036merge', '+refs/pull/1036/head:refs/scratch/pull1036head'], check=False)
print('$ (scratch clone) git fetch origin refs/pull/1036/merge refs/pull/1036/head -> rc', p.returncode, p.stderr.strip()[-200:])
if p.returncode == 0:
    gm = sg('rev-parse', 'refs/scratch/pull1036merge').stdout.strip(); gh = sg('rev-parse', 'refs/scratch/pull1036head').stdout.strip()
    gtree = sg('rev-parse', gm + '^{tree}').stdout.strip(); parents = sg('log', '-1', '--format=%P', gm).stdout.split()
    print('  refs/pull/1036/merge =', gm, 'tree', gtree, 'parents', parents)
    print('  refs/pull/1036/head =', gh, '| == HEAD pin?', gh == HEAD)
    print('  GitHub merge commit parents == {develop %s, head %s}?' % (DEV[:9], HEAD[:9]), set(parents) == {DEV, HEAD}, '| its tree == my merged tree?', gtree == merged,
          '(if the parents differ, GitHub computed it over an OLDER develop — its tree is then not comparable; say which develop)')
    if set(parents) != {DEV, HEAD}:
        for par in parents:
            if par != HEAD: print('  the merge ref\'s other parent', par, sg('log', '-1', '--format=%ci %s', par).stdout.strip()[:120])
co_after = git('count-objects', '-v'); print('$ git -C REPO count-objects -v (AFTER)\n' + co_after.rstrip())
print('  checkout count-objects identical before/after?', co_before == co_after)
print('  scratch clone kept at', clone, '(never deleted by the drafter)')
print('done', now())
