#!/usr/bin/env python3
"""drafter_setup_devmove.py — develop moved DURING drafting: #1016 (KS-1072) landed as 7e89318bc (08:01 --check saw it; tree e09ede17e = the drafter's own
predicted merge-tree eb1051fd3 x a226d94fe). Adds to the SAME drafter clone: merge-tree --write-tree head x 7e89318bc (IN THE CLONE); worktrees dev2 = 7e89318bc and
merged2 = head + a LOCAL --no-ff merge of 7e89318bc (never pushed); per-ENTRY farm (same function as drafter_setup.py), shared dist per tree, IN TREE asserted.
Updates drafter_paths.json with the two trees (the old ones kept). Never rm; write verbs only in the clone."""
import subprocess, os, json, datetime, sys
sys.argv = [sys.argv[0]]
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PA = json.load(open(GS + '/drafter_paths.json')); W = PA['W']; C = PA['C']
DEV2 = '7e89318bcedbc9a35757d4298ace54a6a23020bd'; HEAD = PA['sha']['head']; DEV = 'Blockchain/Dev'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
P('drafter_setup_devmove', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', DEV2]); P('clone sees', DEV2[:9], o.strip(), e.strip()[:200]); assert o.strip() == 'commit'
rc, o, e = run(['git', '-C', C, 'rev-parse', DEV2 + '^{tree}', DEV2 + '^']); P('dev2 tree + parent', o.split())
rc, o, e = run(['git', '-C', C, 'merge-base', HEAD, DEV2]); P('merge-base head dev2', o.strip())
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', HEAD, DEV2]); MT = o.strip().split('\n')[0]; P('merge-tree --write-tree (IN THE CLONE) head x dev2 rc', rc, 'tree', MT, '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
G = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
new = {}
for name, at, merge in (('dev2', DEV2, None), ('merged2', HEAD, DEV2)):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, at]); assert rc == 0, e
    if merge:
        rc, o, e = run(G + [wt, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge dev2', merge]); P('  merge', name, '<-', merge[:9], 'rc', rc, e.strip()[:200]); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway', 'HEAD:' + DEV + '/services/api-gateway/src/routes/verification.ts', 'HEAD:' + DEV + '/services/api-gateway/src/services/enforcement.ts']); P('   root/shared/api-gateway trees + verification.ts / enforcement.ts blobs', o.split())
    new[name] = wt
def farm_dir(src, dst, dev_nm_rewrite):
    os.mkdir(dst); n = 0; skipped = []
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): skipped.append(ent); continue
        s = os.path.join(src, ent)
        if dev_nm_rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        else:
            os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n, skipped
for name, wt in new.items():
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in ('packages/shared', 'services/api-gateway'):
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared'); P('  shared dist build', name, 'rc', rc, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', r)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src'); P('  resolve from', name, o.strip(), e.strip()[:200])
PA['trees'].update(new); PA['sha']['dev2'] = DEV2; PA.setdefault('merge_tree', {})['headxdev2'] = MT
json.dump(PA, open(GS + '/drafter_paths.json', 'w'), indent=1)
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
P('drafter_setup_devmove end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
