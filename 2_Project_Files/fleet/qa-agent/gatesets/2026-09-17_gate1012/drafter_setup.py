#!/usr/bin/env python3
"""drafter_setup.py — #1012 (KS-745) drafter substrate, adapted from the #1010 set. Clone --shared by SHA into a fresh mktemp -d in the drafting
scratchpad; two worktrees IN THE CLONE: base = d067725ff (develop = the PR parent = merge-base), head = e225a4948. merged = head while develop is
unmoved (head is a direct child of develop; recorded, not built). node_modules farmed per ENTRY (.vite skipped); packages/shared,
services/api-gateway AND services/security per entry (vitest runs in the last two); @secuura relinked INTO each tree; shared dist built per tree.
Write verbs only inside the clone. Never rm."""
import subprocess, os, tempfile, datetime, json, glob
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8cbf758d-cbd5-4880-9064-4f71c8077706/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012'
SHA = dict(base='d067725ff1c7f036dbf0f726b9bf12f4daefebe7', head='e225a49480e16bb77251a5d7cbd16afdf2929550')
DEV = 'Blockchain/Dev'
PER_ENTRY = {'packages/shared', 'services/api-gateway', 'services/security'}
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
vite = os.path.join(REPO, DEV, 'services/api-gateway/node_modules/.vite')
def vite_list():
    out = []
    for d, _, fs in os.walk(vite):
        for f in fs:
            st = os.stat(os.path.join(d, f)); out.append('%s %d %s' % (os.path.relpath(os.path.join(d, f), vite), st.st_size, datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')))
    return out
P('checkout api-gateway .vite BEFORE', vite_list())
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1012_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'merge-base', SHA['head'], SHA['base']]); P('merge-base head develop', o.strip()); assert o.strip() == SHA['base']
trees = {}
for name in ('base', 'head'):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
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
    for pkg in ('services/api-gateway/src', 'services/security/src'):
        rc, o, e = run(['node', '-e', "const p=require.resolve('@secuura/shared');const r=require('fs').realpathSync(p);console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/' + pkg)
        P('  resolve from', name, pkg, ':', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
