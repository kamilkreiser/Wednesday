#!/usr/bin/env python3
"""drafter_setup.py — #1014 ROUND 2 (KS-1176) drafter substrate. Derived from the round-1 set's drafter_setup.py (same farm, no wholesale link):
clone --shared --no-checkout by SHA into a fresh mktemp -d in THIS session's scratchpad; worktrees IN THE CLONE: base = e0f41a8fa, r1 = 616c766a5 (round-1 head),
head = 9ba0caf78 (round-2 head), dev = eb1051fd3 (develop, #1015's squash), merged = head + a LOCAL --no-ff merge of dev (never pushed).
merge-tree --write-tree ONLY in the clone: head x dev, head x pull/1016 (a226d94fe), and (head x dev) x pull/1016 (the #1014-then-#1016 and #1016-then-#1014 orders).
node_modules farmed PER ENTRY ONLY — Dev/node_modules, services/api-gateway/node_modules, packages/shared/node_modules (.vite/.vitest/.cache skipped);
no other package gets a node_modules. @secuura relinked INTO each tree. packages/shared dist built in each tree. Write verbs only inside the clone. Never rm. stderr kept."""
import subprocess, os, tempfile, datetime, json
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/1e211184-c0a0-4757-a7c5-e9b4a44dcab4/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
SHA = dict(base='e0f41a8fafd64fa31524390cfeab320e822f3d15', r1='616c766a57a51238450c99bbf1d59bb109e3841c', head='9ba0caf78b8ddb737541df38303b776c982521d2',
           dev='eb1051fd39fe3edab4e0b1d1967515b758d4ba3f', pr1016='a226d94fe8c6fbfecb81de415feb645302cdd166')
DEV = 'Blockchain/Dev'
PER_ENTRY = ['packages/shared', 'services/api-gateway']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '), e.strip()[:200])
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1014r2_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for a, b in (('head', 'dev'), ('head', 'pr1016'), ('dev', 'pr1016')):
    rc, o, e = run(['git', '-C', C, 'merge-base', SHA[a], SHA[b]]); P('merge-base', a, b, o.strip(), e.strip()[:200])
MT = {}
for a, b in (('head', 'dev'), ('head', 'pr1016'), ('dev', 'pr1016')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); MT[a + 'x' + b] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', a, 'x', b, 'rc', rc, 'tree', MT[a + 'x' + b], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
G = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
for name, at, merges in (('base', 'base', []), ('r1', 'r1', []), ('head', 'head', []), ('dev', 'dev', []), ('merged', 'head', ['dev'])):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[at]]); assert rc == 0, e
    for m in merges:
        rc, o, e = run(G + [wt, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge ' + m, SHA[m]]); P('  merge', name, '<-', m, SHA[m][:9], 'rc', rc, e.strip()[:200]); assert rc == 0, e
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway']); P('   root/shared/api-gateway tree hashes', o.split())
    trees[name] = wt
# the local merge of (head x dev) then pull/1016, in a scratch worktree with NO node_modules (merge-tree only on the merged commit)
rc, o, e = run(['git', '-C', trees['merged'], 'rev-parse', 'HEAD']); mhead = o.strip()
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', mhead, SHA['pr1016']]); MT['mergedx1016'] = o.strip().split('\n')[0] if o.strip() else ''
P('merge-tree --write-tree (IN THE CLONE) merged', mhead[:9], 'x pr1016 rc', rc, 'tree', MT['mergedx1016'], e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', MT['devxpr1016'] and SHA['pr1016'], SHA['head']]); P('merge-tree pr1016 x head (order check) rc', rc, 'tree', o.strip().split('\n')[0])
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
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
