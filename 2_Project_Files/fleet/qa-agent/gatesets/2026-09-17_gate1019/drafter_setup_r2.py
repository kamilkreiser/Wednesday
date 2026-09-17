#!/usr/bin/env python3
"""drafter_setup_r2.py — #1017's head MOVED during drafting (cbe29597d -> a067d4e3e, its round 2, bounds_end.out 09:50:05, pr1017_move_read.out).
IN THE DRAFTER CLONE ONLY: object presence (through the --shared alternates; nothing fetched), a LOCAL squash of a067d4e3e onto develop fa887f382 (sq17r2),
merge-tree --write-tree head x sq17r2 and head x a067d4e3e, merged17r2 = head + a local --no-ff merge of sq17r2; per-entry farm + shared dist + IN TREE on
merged17r2; the checkout's worktree count + porcelain before/after (read verbs). Updates drafter_paths.json (a .pre copy kept). Never rm."""
import subprocess, os, json, datetime, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PA = json.load(open(GS + '/drafter_paths.json')); W = PA['W']; C = PA['C']; H = PA['sha']['head']; BASE = PA['sha']['base']
R2 = 'a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66'; DEV = 'Blockchain/Dev'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c, cwd=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    rc, o, e = run(['git', '-C', REPO, 'worktree', 'list', '--porcelain']); rc2, o2, e2 = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    P('source checkout', tag, '| worktree entries', o.count('worktree '), '| porcelain lines', len(o2.splitlines()), '| stderr', repr((e + e2).strip()[:200])); return o.count('worktree '), len(o2.splitlines())
P('drafter_setup_r2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
before = checkout_reading('BEFORE')
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', R2]); P('cat-file', R2[:9], 'in clone (alternates):', rc, o.strip(), e.strip()[:200])
if rc != 0: P('OBJECT ABSENT — NOT MEASURED (no fetch is allowed)'); sys.exit(2)
rc, o, e = run(['git', '-C', C, 'log', '-3', '--format=%H %P %s', R2]); P(o.strip())
GI = ['git', '-c', 'user.name=qa-drafter', '-c', 'user.email=qa-drafter@invalid', '-C']
sq = W + '/wt_sq17r2'; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', sq, BASE]); assert rc == 0, e
rc, o, e = run(GI + [sq, 'merge', '--squash', R2]); P('squash #1017 round 2 onto fa887f382 rc', rc, (o + e).strip()[-300:]); assert rc == 0
rc, o, e = run(GI + [sq, 'commit', '--quiet', '-m', 'qa drafter local squash of #1017 a067d4e3e onto fa887f382']); assert rc == 0, e
rc, o, e = run(['git', '-C', sq, 'rev-parse', 'HEAD', 'HEAD^{tree}']); SQ, SQT = o.split(); P('sq17r2 commit', SQ, 'tree', SQT)
MT = {}
for b in (SQ, R2):
    rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', H, b]); k = H[:9] + 'x' + b[:9]; MT[k] = o.strip().split('\n')[0] if o.strip() else ''
    P('merge-tree --write-tree (IN THE CLONE)', k, 'rc', rc, 'tree', MT[k], '| conflicted-name lines', len(o.strip().split('\n')) - 1, e.strip()[:200])
mw = W + '/wt_merged17r2'; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', mw, H]); assert rc == 0, e
rc, o, e = run(GI + [mw, 'merge', '--no-ff', '--no-edit', '-m', 'qa drafter local merge of the #1017 round-2 squash', SQ]); P('merge merged17r2 <- sq17r2 rc', rc, e.strip()[:200]); assert rc == 0
rc, o, e = run(['git', '-C', mw, 'rev-parse', 'HEAD', 'HEAD^{tree}', 'HEAD:' + DEV + '/services/api-gateway', 'HEAD:' + DEV + '/packages/shared']); P('merged17r2 HEAD / tree / api-gateway / shared', o.split())
import drafter_setup_farm as F
F.farm_tree(mw)
after = checkout_reading('AFTER'); P('source checkout worktree entries + porcelain equal before/after:', before == after, before, after)
shutil.copyfile(GS + '/drafter_paths.json', GS + '/drafter_paths.pre-r2.json')
PA['trees']['sq17r2'] = sq; PA['trees']['merged17r2'] = mw; PA['sha']['pr1017r2'] = R2; PA['sha']['sq17r2'] = SQ; PA['sq17r2_tree'] = SQT; PA['merge_tree'].update(MT)
json.dump(PA, open(GS + '/drafter_paths.json', 'w'), indent=1)
P('drafter_setup_r2 end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
