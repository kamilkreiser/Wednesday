#!/usr/bin/env python3
"""drafter_setup_1031.py — #1031 (KS-1213) TIER 1 ROUND 1 drafter substrate. clone --shared --no-checkout into a fresh mktemp -d under
/private/tmp/claude-501/drafter1031; worktrees IN THE CLONE: head be8596a29, dev 75ad0e55c (develop = the head's second parent), fix 450e3429d (read only).
Merge-in proof IN THE CLONE ONLY: merge-tree --write-tree fix x dev (= head tree 75ed56fb4?), head..dev file set, the fix->head delta equals develop's own
19f1e5475..75ad0e55c delta (file list AND patch-id per file), the three KS-1213 files byte-identical fix = head. node_modules farmed PER ENTRY (Dev/node_modules
with @secuura relinked, packages/shared, services/originate), .vite/.vitest/.cache skipped; shared dist per tree; IN TREE asserted from originate.
Never rm. stderr kept. The Secuura checkout: porcelain + .git/worktrees + refs + config sha read BEFORE and AFTER."""
import subprocess, os, tempfile, datetime, json, hashlib
SCR = '/private/tmp/claude-501/drafter1031'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1031'
SHA = dict(head='be8596a29af15477cb0cbf4b8684e35e63c38e9f', dev='75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e', fix='450e3429ddd66a479231d259cd201fcddbe2b5a4',
           base='19f1e54750ce2b65312a687add2db4f5628edb7d')
DEV = 'Blockchain/Dev'; O = DEV + '/services/originate/src/'
PRF = [O + 'routes/documents.ts', O + 'routes/certifications.ts', O + '__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts']
PER_ENTRY = ['packages/shared', 'services/originate']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def run(c, cwd=None, inp=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, input=inp); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    wts = len(os.listdir(REPO + '/.git/worktrees'))
    rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    vite = sorted(os.listdir(REPO + '/' + DEV + '/services/originate/node_modules/.vite'))
    r = dict(worktrees=wts, porcelain=len(o.splitlines()), refs=refs, config=cfg, branch=br, originate_vite=vite)
    P('source checkout', tag, now(), r, '| status stderr', repr(e.strip()[:200])); return r
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
def patch_ids(C, a, b, path):
    rc, d, e = run(['git', '-C', C, 'diff', '--full-index', a, b, '--', path])
    rc2, o, e2 = run(['git', '-C', C, 'patch-id', '--stable'], inp=d)
    return (o.split() or ['EMPTY'])[0]
P('drafter_setup_1031', now())
before = checkout_reading('BEFORE')
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1031_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
trees = {}
for name in ('head', 'dev', 'fix'):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, SHA[name]]); assert rc == 0, e; trees[name] = wt
rc, o, e = run(['git', '-C', C, 'rev-parse', SHA['head'] + '^{tree}', SHA['head'] + '^1', SHA['head'] + '^2', SHA['fix'] + '^1', SHA['fix'] + '^{tree}', SHA['dev'] + '^{tree}'])
P('head tree / head parents / fix parent / fix tree / dev tree', o.split())
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA['fix'], SHA['dev']]); P('merge-tree --write-tree (IN THE CLONE) fix x dev rc', rc, 'tree', o.strip().split('\n')[0], '| conflicts listed', o.strip().split('\n')[1:][:5], e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', SHA['head'], SHA['dev']]); P('merge-tree --write-tree (IN THE CLONE) head x dev rc', rc, 'tree', o.strip().split('\n')[0])
rc, o, e = run(['git', '-C', C, 'merge-base', '--is-ancestor', SHA['dev'], SHA['head']]); P('dev 75ad0e55c ancestor of head: rc', rc, '(0 = yes)')
rc, o, e = run(['git', '-C', C, 'merge-base', SHA['fix'], SHA['dev']]); P('merge-base(fix, dev)', o.strip(), '= 19f1e5475:', o.strip() == SHA['base'])
dev_head = run(['git', '-C', C, 'diff', '--name-only', SHA['dev'], SHA['head']])[1].split()
P('dev..head files (%d):' % len(dev_head), dev_head, '| == the three KS-1213 files:', sorted(dev_head) == sorted(PRF))
fix_head = sorted(run(['git', '-C', C, 'diff', '--name-only', SHA['fix'], SHA['head']])[1].split())
base_dev = sorted(run(['git', '-C', C, 'diff', '--name-only', SHA['base'], SHA['dev']])[1].split())
P('fix..head files (what the merge brought) %d | base 19f1e5475..dev files %d | identical sets: %s' % (len(fix_head), len(base_dev), fix_head == base_dev))
mism = [f for f in fix_head if patch_ids(C, SHA['fix'], SHA['head'], f) != patch_ids(C, SHA['base'], SHA['dev'], f)]
P('patch-id per file (fix->head vs base->dev): files compared', len(fix_head), 'mismatches', len(mism), mism[:5])
P('whole-delta patch-id fix->head', patch_ids(C, SHA['fix'], SHA['head'], '.'), '| base->dev', patch_ids(C, SHA['base'], SHA['dev'], '.'))
P('merged delta touches originate:', [f for f in fix_head if '/services/originate/' in f])
for f in PRF:
    rc, o, e = run(['git', '-C', C, 'diff', '--quiet', SHA['fix'], SHA['head'], '--', f])
    P('  byte-identical fix = head rc', rc, '(0 = identical) blob', run(['git', '-C', C, 'rev-parse', SHA['head'] + ':' + f])[1].strip()[:9], '| develop blob', (run(['git', '-C', C, 'rev-parse', SHA['dev'] + ':' + f])[1].strip() or 'ABSENT')[:9], f.split('/')[-1])
P('fix commit stat:', run(['git', '-C', C, 'diff', '--shortstat', SHA['base'], SHA['fix']])[1].strip(), '| head over dev:', run(['git', '-C', C, 'diff', '--shortstat', SHA['dev'], SHA['head']])[1].strip())
for name in ('head', 'dev'):
    wt = trees[name]
    n, sk = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', name, 'Dev/node_modules entries', n, 'skipped', sk)
    for rel in PER_ENTRY:
        n, sk = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/originate')) if os.path.islink(p)]; P('   wholesale node_modules links:', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + DEV + '/services/originate/src', capture_output=True, text=True); P('  resolve from originate:', p.stdout.strip(), p.stderr.strip()[:300])
after = checkout_reading('AFTER'); P('source checkout equal before/after:', before == after)
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': SHA}, open(GS + '/out/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_1031 end', now('%H:%M:%S %Z'))
