#!/usr/bin/env python3
"""drafter_setup.py — #1009 (KS-864 F-1007-1 follow-up) drafter substrate, adapted from the #1008 set. Clone --shared by SHA into a fresh mktemp -d
in the drafting scratchpad; three worktrees IN THE CLONE: base = 0308b7a04 (the PR parent = merge-base), head = 6ec0cb198, merged = head + a LOCAL
--no-ff merge of CURRENT develop 73d3fcb90 (never pushed; api-gateway tree hash compared). node_modules farmed per ENTRY (never a
wholesale link to a directory vitest writes a cache into: `.vite` is skipped, and the packages vitest may run in — packages/shared and
services/api-gateway — are farmed per entry too); @secuura relinked INTO each tree; packages/shared dist built in each tree.
Write verbs only inside the clone. Never rm."""
import subprocess, os, tempfile, datetime, json, glob
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fa385b47-2d6c-4cbd-b671-2860bf4a1518/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009'
SHA = dict(base='0308b7a0447a2c01c12aad358c9b4d04a5178210', head='6ec0cb19834407887daa7bf5994f2da169abd30e', dev='73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5')
DEV = 'Blockchain/Dev'
PER_ENTRY = {'packages/shared', 'services/api-gateway'}
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1009_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']]); P('merge-base head develop', o.strip()); assert o.strip() == SHA['base']
G = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
for name, at, merges in (('base', 'base', []), ('head', 'head', []), ('merged', 'head', ['dev'])):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[at]]); assert rc == 0, e
    for m in merges:
        rc, o, e = run(G + [wt, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge ' + m, SHA[m]]); P('  merge', name, '<-', m, SHA[m][:9], 'rc', rc); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway']); P('   shared/api-gateway tree hashes', o.split())
    trees[name] = wt
src_dev_nm = os.path.join(REPO, DEV, 'node_modules')
def farm_dir(src, dst, dev_nm_rewrite):
    os.mkdir(dst); n = 0; skipped = []
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): skipped.append(ent); continue
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
    return n, skipped
for name, wt in trees.items():
    if os.path.isdir(os.path.join(REPO, 'node_modules')): os.symlink(os.path.join(REPO, 'node_modules'), os.path.join(wt, 'node_modules'))
    n, sk = farm_dir(src_dev_nm, os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    links = 0
    for pkg_nm in sorted(glob.glob(os.path.join(REPO, DEV, 'services', '*', 'node_modules')) + glob.glob(os.path.join(REPO, DEV, 'packages', '*', 'node_modules'))):
        rel = os.path.relpath(os.path.dirname(pkg_nm), os.path.join(REPO, DEV))
        if not os.path.isdir(os.path.join(wt, DEV, rel)): continue
        dst = os.path.join(wt, DEV, rel, 'node_modules')
        if rel in PER_ENTRY:
            n, sk = farm_dir(pkg_nm, dst, False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
        else:
            os.symlink(pkg_nm, dst); links += 1
    P('   wholesale package node_modules links', links)
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const p=require.resolve('@secuura/shared');const r=require('fs').realpathSync(p);const x=require.resolve('express');console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| express', require(require('path').join(require('path').dirname(x),'package.json')).version, require('fs').realpathSync(x).startsWith(process.argv[1]) ? 'express in-tree-link' : 'express via checkout node_modules (read-only)', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
