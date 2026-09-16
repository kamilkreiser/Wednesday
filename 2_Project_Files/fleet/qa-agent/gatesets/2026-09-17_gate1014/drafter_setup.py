#!/usr/bin/env python3
"""drafter_setup.py — #1014 (KS-1176) drafter substrate. Adapted from the #1011 ROUND 2 set's drafter_setup.py, WITHOUT its wholesale-link shortcut:
clone --shared --no-checkout by SHA into a fresh mktemp -d in the drafting scratchpad; worktrees IN THE CLONE: base = e0f41a8fa (the PR parent = merge-base),
head = 616c766a5, merged = head + a LOCAL --no-ff merge of the then-current develop (never pushed). node_modules farmed PER ENTRY ONLY — Dev/node_modules,
services/api-gateway/node_modules, packages/shared/node_modules (`.vite` / `.vitest` / `.cache` skipped); the other 24 package node_modules and the empty root
node_modules are NOT created at all (no wholesale link anywhere; vitest runs only in api-gateway). @secuura relinked INTO each tree. packages/shared dist built
in each tree. Write verbs only inside the clone. Never rm. stderr kept."""
import subprocess, os, tempfile, datetime, json, sys
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/76d545ac-4e62-4400-be44-c9ce11c3c344/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
SHA = dict(base='e0f41a8fafd64fa31524390cfeab320e822f3d15', head='616c766a57a51238450c99bbf1d59bb109e3841c', dev=sys.argv[1])
DEV = 'Blockchain/Dev'
PER_ENTRY = ['packages/shared', 'services/api-gateway']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'develop arg', SHA['dev'])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '), e.strip()[:200])
W = tempfile.mkdtemp(prefix='gate1014_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', C, 'merge-base', SHA['head'], SHA['dev']]); P('merge-base head develop', o.strip(), e.strip()[:200]); assert o.strip() == SHA['base']
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', SHA['head'], SHA['dev']]); P('merge-tree --write-tree head develop (IN THE CLONE) rc', rc, 'tree', o.strip().split()[0] if o.strip() else '', e.strip()[:200])
G = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
for name, at, merges in (('base', 'base', []), ('head', 'head', []), ('merged', 'head', ['dev'])):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[at]]); assert rc == 0, e
    for m in merges:
        rc, o, e = run(G + [wt, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge ' + m, SHA[m]]); P('  merge', name, '<-', m, SHA[m][:9], 'rc', rc, e.strip()[:200]); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway']); P('   root/shared/api-gateway tree hashes', o.split())
    trees[name] = wt
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
for name, wt in trees.items():
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    P('   wholesale node_modules links: 0 (other package dirs left without node_modules)')
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
