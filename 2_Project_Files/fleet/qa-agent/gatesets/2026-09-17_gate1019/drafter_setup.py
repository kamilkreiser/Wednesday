#!/usr/bin/env python3
"""drafter_setup.py — #1019 (KS-1187) ROUND 1 drafter substrate. Derived from the #1017 set's drafter_setup.py (same farm, no wholesale link):
clone --shared --no-checkout by SHA into a fresh mktemp -d in THIS session's scratchpad; worktrees IN THE CLONE: base = fa887f382 (develop = PR parent),
c1 = 50a4b749a (product + new test, pre ks843 pin), head = 8b8996f8b, sq17 = a LOCAL squash of #1017's cbe29597d onto fa887f382 (predicts develop if #1017
lands first), merged17 = head + a LOCAL --no-ff merge of sq17. merge-tree --write-tree ONLY in the clone. node_modules farmed PER ENTRY ONLY (Dev,
api-gateway, packages/shared; .vite/.vitest/.cache skipped), @secuura relinked INTO each tree; shared dist built per tree; IN TREE asserted. Never rm.
stderr kept. The Secuura checkout: porcelain + worktree count read BEFORE and AFTER (read verbs only)."""
import subprocess, os, tempfile, datetime, json
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/804c11ac-1249-4d9f-837c-27ce44211d2f/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
SHA = dict(base='fa887f382b212b8da4a0a4a556bacb05ea34daaa', c1='50a4b749ad83bac865dd4216d56b19dd7bdf50b5', head='8b8996f8b290ef55c35721c30f8671f982fa5a91',
           pr1017='cbe29597d11e59f2e1a14519e9ba3dbf6de9a756')
DEV = 'Blockchain/Dev'
PER_ENTRY = ['packages/shared', 'services/api-gateway']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain'])
    rc2, o2, e2 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    P('source checkout', tag, '| worktree entries', o.count('worktree '), '| porcelain lines', len(o2.splitlines()), '| stderr', repr((e + e2).strip()[:200]))
    return o.count('worktree '), len(o2.splitlines())
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = checkout_reading('BEFORE')
W = tempfile.mkdtemp(prefix='gate1019_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
GI = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
trees = {}
def add(name, at):
    wt = W + '/wt_' + name
    rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, at]); assert rc == 0, e
    trees[name] = wt; return wt
for name in ('base', 'c1', 'head'):
    add(name, SHA[name])
sq = add('sq17', SHA['base'])
rc, o, e = run(GI + [sq, 'merge', '--squash', SHA['pr1017']]); P('squash #1017 onto develop fa887f382 rc', rc, (o + e).strip()[-300:]); assert rc == 0
rc, o, e = run(GI + [sq, 'commit', '--quiet', '-m', 'qa drafter local squash of #1017 cbe29597d onto fa887f382']); P('squash commit rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', sq, 'rev-parse', 'HEAD', 'HEAD^{tree}']); SQ, SQT = o.split(); P('sq17 commit', SQ, 'tree', SQT, '(#1017 drafter merged tree for head x fa887f382 was 135b07468)')
MT = {}
for a, b in ((SHA['head'], SHA['base']), (SHA['head'], SQ), (SHA['head'], SHA['pr1017'])):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b]); k = a[:9] + 'x' + b[:9]; MT[k] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', k, 'rc', rc, 'tree', MT[k], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
mw = add('merged17', SHA['head'])
rc, o, e = run(GI + [mw, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge of the #1017 squash', SQ]); P('merge merged17 <- sq17 rc', rc, e.strip()[:200]); assert rc == 0
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
    if name == 'sq17': P('farm', name, 'SKIPPED — nothing runs in the squash tree'); continue
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    sh = wt + '/' + DEV + '/packages/shared'; t0 = datetime.datetime.now()
    rc, o, e = run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=sh); P('  shared dist build', name, 'rc', rc, 'secs', (datetime.datetime.now() - t0).seconds, (o + e).strip()[-300:])
    rc, o, e = run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| vitest', require('vitest/package.json').version, '| ts', require('typescript/package.json').version, '| express', require('express/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src')
    P('  resolve from', name, 'api-gateway/src:', o.strip(), e.strip()[:300])
after = checkout_reading('AFTER')
P('source checkout worktree entries + porcelain equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': dict(SHA, sq17=SQ), 'sq17_tree': SQT, 'merge_tree': MT}, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
