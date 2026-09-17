#!/usr/bin/env python3
"""drafter_merged_1032.py — develop moved 0a2b1603f -> bb848b828 during drafting (KS-1211 vitest lock bumps). In the drafter CLONE only (bb848b828 is present in the
shared object store; nothing fetched): merge-tree --write-tree head x bb848b828 (the merged-tree OID), conflicts, what the merge would bring, services/auth/src and
packages/shared subtree equality merged = head, the users.ts + ks1194 test blobs in the merged tree; the vitest version in bb848b828's root and auth locks vs the
farm's installed vitest; then a worktree of the merged TREE (a commit-tree in the clone) farmed PER ENTRY and the whole auth vitest at 60 s ceilings + project tsc."""
import json, subprocess, datetime, os
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
paths = json.load(open(GS + '/out/drafter_paths.json')); C = paths['C']; W = paths['W']
H = '70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039'; NEWDEV = 'bb848b8283eb5ee6a6180067315b76f1321e7b6b'
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def g(*a, inp=None): p = subprocess.run(['git', '-C', C] + list(a), capture_output=True, text=True, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
P('drafter_merged_1032', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
P('newdev object in clone:', g('cat-file', '-t', NEWDEV)[1], '| parent', g('rev-parse', NEWDEV + '^')[1][:9], '| head ancestor-of newdev rc', g('merge-base', '--is-ancestor', H, NEWDEV)[0], '| merge-base', g('merge-base', H, NEWDEV)[1][:9])
rc, o, e = g('merge-tree', '--write-tree', '--name-only', H, NEWDEV); MT = o.split('\n')[0]
P('merge-tree --write-tree head x bb848b828 rc', rc, 'MERGED TREE', MT, '| conflicts listed', o.split('\n')[1:][:4], e[:200])
P('merged vs head tree: files differing', len(g('diff', '--name-only', H + '^{tree}', MT)[1].split()), '| = develop 0a2b1603f..bb848b828 files', len(g('diff', '--name-only', '0a2b1603fe52f0f3b8152588af78bbeab0237be7', NEWDEV)[1].split()),
  '| set equal', sorted(g('diff', '--name-only', H + '^{tree}', MT)[1].split()) == sorted(g('diff', '--name-only', '0a2b1603fe52f0f3b8152588af78bbeab0237be7', NEWDEV)[1].split()))
for sub in (A + '/src', DEV + '/packages/shared', A):
    P('subtree', sub, '| head', g('rev-parse', H + ':' + sub)[1][:9], '| merged', g('rev-parse', MT + ':' + sub)[1][:9], '| equal', g('rev-parse', H + ':' + sub)[1] == g('rev-parse', MT + ':' + sub)[1])
for f in (A + '/src/routes/users.ts', A + '/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts', A + '/package.json', A + '/package-lock.json'):
    P('blob', f.split('/')[-1], '| head', g('rev-parse', H + ':' + f)[1][:9], '| merged', g('rev-parse', MT + ':' + f)[1][:9])
for lock in (DEV + '/package-lock.json', A + '/package-lock.json'):
    rc, o, e = g('show', NEWDEV + ':' + lock)
    try:
        d = json.loads(o); P('lock', lock, 'bb848b828 vitest', d['packages'].get('node_modules/vitest', {}).get('version'))
    except Exception as ex: P('lock', lock, 'unreadable', type(ex).__name__)
P('farm installed vitest (checkout Dev/node_modules):', json.load(open(REPO + '/' + DEV + '/node_modules/vitest/package.json'))['version'])
rc, CM, e = g('commit-tree', MT, '-p', H, '-p', NEWDEV, '-m', 'qa1032 drafter: merged-tree probe commit (clone only)'); P('commit-tree in clone rc', rc, CM[:9], e[:120])
wt = W + '/wt_merged'; rc, o, e = g('worktree', 'add', '--detach', '--quiet', wt, CM); P('worktree merged rc', rc, e[:120])
def farm_dir(src, dst, rewrite):
    os.mkdir(dst); n = 0
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): continue
        s = os.path.join(src, ent)
        if rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)): os.symlink(os.path.normpath(os.path.join(dst, ent, os.readlink(os.path.join(s, sub)))), os.path.join(dst, ent, sub))
        else: os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n
n = [farm_dir(os.path.join(REPO, DEV, r, 'node_modules'), os.path.join(wt, DEV, r, 'node_modules'), r == '') for r in ('', 'packages/shared', 'services/auth')]
b = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True).returncode
r = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + A + '/src', capture_output=True, text=True).stdout.strip()
P('merged farm per entry', n, '| wholesale links', sum(os.path.islink(os.path.join(wt, DEV, x, 'node_modules')) for x in ('', 'packages/shared', 'services/auth')), '| shared dist rc', b, '| @secuura/shared from auth', r)
out = GS + '/out/suite_merged_t60.json'
with open(GS + '/out/suite_merged_t60.stderr', 'w') as fe:
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--testTimeout=60000', '--hookTimeout=60000', '--reporter=json', '--outputFile=' + out], cwd=wt + '/' + A, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1'))
j = json.load(open(out)); P('SUITE merged t60 rc', p.returncode, '| files', len(j['testResults']), 'tests', j['numTotalTests'], 'failed', j['numFailedTests'], 'pending', j['numPendingTests'])
P('PROJECT tsc merged rc', subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=wt + '/' + A, capture_output=True, text=True).returncode)
P('drafter_merged_1032 end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
