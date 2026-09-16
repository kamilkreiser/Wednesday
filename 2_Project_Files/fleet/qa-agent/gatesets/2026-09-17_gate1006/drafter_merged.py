#!/usr/bin/env python3
"""drafter_merged.py — develop MOVED during drafting (40fe4db69 -> 93629700c, #1005's squash; develop_move_read.out 00:49:13). Build
the MERGED tree in the drafter's clone: a worktree at head 86fe59e6b + a LOCAL merge of 93629700c (never pushed; the object is
reachable through the --shared alternates), farm node_modules the same way, build the shared dist, run the whole packages/shared and
demo-service suites. Write verbs only inside the clone. Never rm."""
import sys, os, subprocess, json, glob
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
import drafterlib as L
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
NEWDEV = '93629700c3d219c1d8ca61d69150bb9b623fc1be'
D = 'Blockchain/Dev'
def run(c, cwd=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
L.P('drafter_merged start', L.ts())
C = L.PATHS['C']; wt = L.W + '/wt_merged'
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', NEWDEV]); L.P('new develop object in clone:', o.strip(), rc); assert o.strip() == 'commit'
rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, L.PATHS['sha']['head']]); assert rc == 0, e
G = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C', wt]
rc, o, e = run(G + ['merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge of develop 93629700c', NEWDEV]); L.P('merge rc', rc, (o.strip().splitlines() or [''])[-1][:160], e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); L.P('merged HEAD+parents', o.strip())
rc, o, e = run(['git', '-C', wt, 'diff', '--stat', L.PATHS['sha']['head'], 'HEAD']); L.P('merged vs head:', o.strip().replace('\n', ' | '))
rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD:' + D + '/packages/shared', 'HEAD:' + D + '/services/demo-service']); L.P('shared/demo-service tree hashes (head: 89afd4b9d / d26b5ce4a)', o.split())
# farm exactly as drafter_setup.py does (import its helper by exec of the function source would re-run setup; replicate minimal)
src_dev_nm = os.path.join(REPO, D, 'node_modules')
def farm_dir(src, dst, rewrite):
    os.mkdir(dst)
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): continue
        s = os.path.join(src, ent)
        if rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        elif os.path.islink(s) and not os.path.isabs(os.readlink(s)) and rewrite and ent != '.bin':
            os.symlink(os.path.normpath(os.path.join(dst, os.readlink(s))), os.path.join(dst, ent))
        else:
            os.symlink(s, os.path.join(dst, ent))
if os.path.isdir(os.path.join(REPO, 'node_modules')): os.symlink(os.path.join(REPO, 'node_modules'), os.path.join(wt, 'node_modules'))
farm_dir(src_dev_nm, os.path.join(wt, D, 'node_modules'), True)
for pkg_nm in sorted(glob.glob(os.path.join(REPO, D, 'services', '*', 'node_modules')) + glob.glob(os.path.join(REPO, D, 'packages', '*', 'node_modules'))):
    rel = os.path.relpath(os.path.dirname(pkg_nm), os.path.join(REPO, D))
    if not os.path.isdir(os.path.join(wt, D, rel)): continue
    dst = os.path.join(wt, D, rel, 'node_modules')
    if rel in ('packages/shared', 'services/demo-service'): farm_dir(pkg_nm, dst, False)
    else: os.symlink(pkg_nm, dst)
rc, o, e = run([wt + '/' + D + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + D + '/packages/shared'); L.P('shared dist build rc', rc)
rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.startsWith(process.argv[1])?'IN TREE':'OUTSIDE TREE', r)", wt], cwd=wt + '/' + D + '/services/demo-service/src'); L.P('resolve @secuura/shared:', o.strip())
paths = L.PATHS; paths['trees']['merged'] = wt; paths['sha']['develop_moved'] = NEWDEV
json.dump(paths, open(L.GS + '/drafter_paths.json', 'w'), indent=1)
L.T['merged'] = wt
L.P('porcelain merged', len(L.porcelain('merged')), 'lines; non-node_modules:', [x for x in L.porcelain('merged') if not x.endswith('node_modules')])
L.vitest('demo_suite_merged', 'merged', 'demo'); L.vitest('shared_suite_merged', 'merged', 'shared')
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); L.P('source checkout worktree entries', o.count('worktree '))
L.P('drafter_merged end', L.ts())
