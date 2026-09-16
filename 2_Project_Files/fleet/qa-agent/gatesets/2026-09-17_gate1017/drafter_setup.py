#!/usr/bin/env python3
"""drafter_setup.py — #1017 (KS-1195) ROUND 1 drafter substrate. Derived from the #1014 round-2 set's drafter_setup.py (same farm, no wholesale link):
clone --shared --no-checkout by SHA into a fresh mktemp -d in THIS session's scratchpad; worktrees IN THE CLONE: base = 7e89318bc (develop = PR parent),
c1 = 973eb49ef (product commit, pre line-pin), head = cbe29597d, sq14 = a LOCAL squash of #1014's 9ba0caf78 onto 7e89318bc (predicts develop if #1014 lands
first), merged14 = head + a LOCAL --no-ff merge of sq14. merge-tree --write-tree ONLY in the clone. node_modules farmed PER ENTRY ONLY (Dev, api-gateway,
packages/shared; .vite/.vitest/.cache skipped), @secuura relinked INTO each tree; shared dist built per tree; IN TREE asserted. Never rm. stderr kept."""
import subprocess, os, tempfile, datetime, json
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/1e211184-c0a0-4757-a7c5-e9b4a44dcab4/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
SHA = dict(base='7e89318bcedbc9a35757d4298ace54a6a23020bd', c1='973eb49ef602ceee4bf2134ddb9405e00663e86f', head='cbe29597d11e59f2e1a14519e9ba3dbf6de9a756',
           pr1014='9ba0caf78b8ddb737541df38303b776c982521d2')
DEV = 'Blockchain/Dev'
PER_ENTRY = ['packages/shared', 'services/api-gateway']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '), e.strip()[:200])
W = tempfile.mkdtemp(prefix='gate1017_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
GI = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
def add(name, at):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, at]); assert rc == 0, e
    trees[name] = wt; return wt
for name in ('base', 'c1', 'head'):
    add(name, SHA[name])
# local squash of #1014 onto develop (never pushed)
sq = add('sq14', SHA['base'])
rc, o, e = run(GI + [sq, 'merge', '--squash', SHA['pr1014']]); P('squash #1014 onto base rc', rc, (o + e).strip()[-300:]); assert rc == 0
rc, o, e = run(GI + [sq, 'commit', '--quiet', '-m', 'qa drafter local squash of #1014 9ba0caf78 onto 7e89318bc']); P('squash commit rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', sq, 'rev-parse', 'HEAD', 'HEAD^{tree}']); SQ, SQT = o.split(); P('sq14 commit', SQ, 'tree', SQT, '(#1014r2 drafter predicted 5748a1d68 for #1014 x 7e89318bc)')
MT = {}
for a, b in ((SHA['head'], SHA['base']), (SHA['head'], SQ), (SHA['head'], SHA['pr1014'])):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b]); k = a[:9] + 'x' + b[:9]; MT[k] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', k, 'rc', rc, 'tree', MT[k], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
mw = add('merged14', SHA['head'])
rc, o, e = run(GI + [mw, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge of the #1014 squash', SQ]); P('merge merged14 <- sq14 rc', rc, e.strip()[:200]); assert rc == 0
for name, wt in trees.items():
    rc, o, e = run(['git', '-C', wt, 'rev-list', '--parents', '-n', '1', 'HEAD']); P('tree', name, 'HEAD+parents', o.strip())
    rc, o, e = run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}', 'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway']); P('   root/shared/api-gateway tree hashes', o.split())
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
    if name == 'sq14': P('farm', name, 'SKIPPED — nothing runs in the squash tree'); continue
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, '| ioredis', require('ioredis/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': dict(SHA, sq14=SQ), 'sq14_tree': SQT, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
