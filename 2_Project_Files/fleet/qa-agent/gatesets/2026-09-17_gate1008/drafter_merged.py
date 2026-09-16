#!/usr/bin/env python3
"""drafter_merged.py — develop moved to 0308b7a04 (#1007's squash, 3 api-gateway files) while this set was drafted. In the drafter's
--shared clone ONLY: a third worktree at head, a local merge of 0308b7a04 (never pushed), the same node_modules farm as drafter_setup.py,
the shared dist built, and the WHOLE api-gateway suite on the merged tree. Blob equality of the two #1008 files asserted vs head."""
import sys, os, json, subprocess, glob, datetime
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008')
import drafterlib as dl
from drafterlib import P, ts, W, T, GS
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
C = json.load(open(GS + '/drafter_paths.json'))['C']
DEV_NEW = '0308b7a0447a2c01c12aad358c9b4d04a5178210'; HEAD = 'dd7086d5aa574285beffc515f9371a438621f25d'; DEV = 'Blockchain/Dev'
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_merged', ts())
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
wt = W + '/wt_merged'
rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, HEAD]); assert rc == 0, e
env = dict(os.environ, GIT_AUTHOR_NAME='qa-drafter', GIT_AUTHOR_EMAIL='qa-drafter@localhost', GIT_COMMITTER_NAME='qa-drafter', GIT_COMMITTER_EMAIL='qa-drafter@localhost')
rc, o, e = run(['git', '-C', wt, 'merge', '--no-edit', '--no-ff', DEV_NEW], env=env); P('merge rc', rc, (o + e).strip()[-300:]); assert rc == 0
rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('merged HEAD+parents', o.strip())
for rel in ('services/api-gateway/src/routes/verification.ts', 'services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts', 'services/api-gateway/src/routes/system-status.ts'):
    a = run(['git', '-C', wt, 'rev-parse', 'HEAD:' + DEV + '/' + rel])[1].strip(); b = run(['git', '-C', wt, 'rev-parse', HEAD + ':' + DEV + '/' + rel])[1].strip()
    P('  blob', rel.split('/')[-1], 'merged', a[:9], 'head', b[:9], 'EQUAL' if a == b else 'DIFFERS')
rc, o, e = run(['git', '-C', wt, 'diff', '--stat', HEAD, 'HEAD']); P('merged vs head diff --stat:', o.strip().replace('\n', ' | '))
# farm, as drafter_setup.py
src_dev_nm = os.path.join(REPO, DEV, 'node_modules')
def farm_dir(src, dst, dev_nm_rewrite):
    os.mkdir(dst); n = 0
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): continue
        s = os.path.join(src, ent)
        if dev_nm_rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        elif os.path.islink(s) and not os.path.isabs(os.readlink(s)) and dev_nm_rewrite and ent != '.bin':
            os.symlink(os.path.normpath(os.path.join(dst, os.readlink(s))), os.path.join(dst, ent))
        else:
            os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n
if os.path.isdir(os.path.join(REPO, 'node_modules')): os.symlink(os.path.join(REPO, 'node_modules'), os.path.join(wt, 'node_modules'))
P('farm merged Dev/node_modules entries', farm_dir(src_dev_nm, os.path.join(wt, DEV, 'node_modules'), True))
for pkg_nm in sorted(glob.glob(os.path.join(REPO, DEV, 'services', '*', 'node_modules')) + glob.glob(os.path.join(REPO, DEV, 'packages', '*', 'node_modules'))):
    rel = os.path.relpath(os.path.dirname(pkg_nm), os.path.join(REPO, DEV))
    if not os.path.isdir(os.path.join(wt, DEV, rel)): continue
    dst = os.path.join(wt, DEV, rel, 'node_modules')
    if rel in ('packages/shared', 'services/api-gateway'): farm_dir(pkg_nm, dst, False)
    else: os.symlink(pkg_nm, dst)
rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared'); P('shared dist build merged rc', rc)
rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.startsWith(process.argv[1])?'IN TREE':'OUTSIDE TREE', r)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src'); P('realpath @secuura/shared from merged api-gateway/src:', o.strip(), e.strip()[:200])
T['merged'] = wt
paths = json.load(open(GS + '/drafter_paths.json')); paths['trees']['merged'] = wt; json.dump(paths, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('porcelain merged', len(dl.porcelain('merged')))
dl.vitest('gw_suite_merged', 'merged', 'gw')
dl.vitest('ks1087_merged', 'merged', 'gw', files=['src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts'])
P('porcelain merged', len(dl.porcelain('merged')))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
P('end', ts())
