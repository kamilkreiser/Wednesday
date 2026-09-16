#!/usr/bin/env python3
"""drafter_setup.py — #1013 (KS-999) drafter substrate, adapted from the #1010 set. Clone --shared by SHA into a fresh mktemp -d in the drafting
scratchpad; worktrees IN THE CLONE: base = 1125607e9 (the PR parent = merge-base = develop at drafting), head = 5fbfb66a9. develop == base at
drafting (ls-remote 04:44), so the merged tree is content-identical to head: NO merged worktree is built (stated in the report; the gate
merges the then-current develop if it moved). node_modules farmed per ENTRY (.vite skipped): Blockchain/Dev/node_modules with @secuura relinked
INTO each tree; services/auth and packages/shared per entry. Shared dist built in each tree. Write verbs only inside the clone. Never rm."""
import subprocess, os, tempfile, datetime, json, glob
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8cbf758d-cbd5-4880-9064-4f71c8077706/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013'
SHA = dict(base='1125607e978d6ad637720c985e43e3d79fecdf88', head='5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2')
DEV = 'Blockchain/Dev'
PER_ENTRY = {'packages/shared', 'services/auth'}
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
W = tempfile.mkdtemp(prefix='gate1013_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
trees = {}
for name in ('base', 'head'):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD', 'HEAD:' + DEV + '/services/auth', 'HEAD:' + DEV + '/packages/shared']); P('tree', name, o.split())
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
    P('   wholesale package node_modules links (vitest never runs there)', links)
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const p=require.resolve('@secuura/shared');const r=require('fs').realpathSync(p);console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/auth/src')
    P('  resolve from', name, 'auth/src:', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
