#!/usr/bin/env python3
"""drafter_setup.py — #1026 (KS-839) TIER 1 ROUND 1 drafter substrate. clone --shared --no-checkout by SHA into a fresh mktemp -d under
/private/tmp/claude-501/drafter1026; worktrees IN THE CLONE: head 8ab493354, dev efaaa6034 (develop = the head's second parent), fix cb2ed18d9 (nothing runs).
merge-tree --write-tree ONLY in the clone (head x develop; head x #1025's head, the disjoint sibling). node_modules farmed PER ENTRY (Dev/node_modules with
@secuura relinked, packages/shared, services/auth), .vite/.vitest/.cache skipped; shared dist per tree; IN TREE asserted from auth. Never rm. stderr kept.
The Secuura checkout: .git/worktrees count + porcelain read BEFORE and AFTER."""
import subprocess, os, tempfile, datetime, json
SCR = '/private/tmp/claude-501/drafter1026'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026'
SHA = dict(head='8ab493354bbdb3fa52d2eb14654492db1a891e4a', dev='efaaa6034f036dd9538ee35b189217b1d08b90a9', fix='cb2ed18d9503acfdc096caef789f7856daa6a35d',
           m1='83588c2bb99eac7a36377c00e654dbd4df7af967', pr1025='9954a7069a16987da140654337555c9a13268b1f')
DEV = 'Blockchain/Dev'; PER_ENTRY = ['packages/shared', 'services/auth']
PRF = [DEV + '/services/auth/src/services/oauth.ts', DEV + '/services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    wts = len(os.listdir(REPO + '/.git/worktrees'))
    rc2, o2, e2 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain', '--untracked-files=no'])
    P('source checkout', tag, '| .git/worktrees entries', wts, '| porcelain lines', len(o2.splitlines()), '| stderr', repr(e2.strip()[:200])); return wts, len(o2.splitlines())
def farm_dir(src, dst, rewrite):
    os.mkdir(dst); n = 0; sk = []
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): sk.append(ent); continue
        s = os.path.join(src, ent)
        if rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        else:
            os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n, sk
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = checkout_reading('BEFORE')
W = tempfile.mkdtemp(prefix='gate1026_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
trees = {}
for name in ('head', 'dev', 'fix'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}', SHA['head'] + '^1', SHA['head'] + '^2', SHA['fix'] + '^1', SHA['m1'] + '^2']); P('head tree / head parents / fix parent / m1 2nd parent', o.split())
for a, b in (('head', 'dev'), ('fix', 'dev'), ('head', 'pr1025')):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA[a], SHA[b]]); P('merge-tree --write-tree (IN THE CLONE)', a, 'x', b, 'rc', rc, 'tree', o.strip().split('\n')[0], '| conflicts/names', o.strip().split('\n')[1:6], e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']]); P('develop efaaa6034 ancestor of head: rc', rc, '(0 = yes)')
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['dev'], SHA['head']]); P('dev..head files:', o.strip().replace('\n', ' | '))
rc, o, e = run(['git', '-C', C, 'diff', '--name-status', SHA['dev'], SHA['pr1025']]); P('dev..#1025 head files:', o.strip().replace('\n', ' | ')[:600])
rc, o, e = run(['git', '-C', C, 'diff', '--quiet', SHA['fix'], SHA['head'], '--'] + PRF); P('PR files byte-identical fix vs head: rc', rc, '(0 = identical)')
rc, o, e = run(['git', '-C', C, 'diff', '--stat', SHA['fix'] + '^1', SHA['dev'], '--', DEV + '/services/auth/']); P('services/auth changes fix-parent..develop:', repr(o.strip()[-300:]))
for f in PRF:
    for nm in ('dev', 'head'):
        rc, o, e = run(['git', '-C', C, 'rev-parse', SHA[nm] + ':' + f]); P('  blob', nm, f.split('/')[-1], o.strip() or ('ABSENT ' + e.strip()[:80]))
for name in ('head', 'dev'):
    wt = trees[name]
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/auth')) if os.path.islink(p)]; P('   wholesale node_modules links:', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + DEV + '/services/auth/src', capture_output=True, text=True); P('  resolve from auth:', p.stdout.strip(), p.stderr.strip()[:300])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after, before, after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
