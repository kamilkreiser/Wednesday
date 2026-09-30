#!/usr/bin/env python3
"""pin_gate48b.py — MEASURE the pins for the gate48b kit (kit.json beside this script) and write pins_gate48b.json. ONE PR, #1355 (T1, KS-1378).
Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/1355/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g48b_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
  (A) heads: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched refs == ls-remote.
  (B) shape: merge-base, ahead / behind, head parent (== kit expected_parent), file list == kit.json files AND numstat.
  (C) the develop MOVE since the merge-base: the moved paths and their intersection with the PR's own paths (must be EMPTY).
  (D) ONE PR: no pair to overlap — printed as `OVERLAP SUMMARY: 0 pair(s) checked (ONE PR)`; the out-of-kit census is the launch action's (2b).
  (E) the PR ALONE over develop: `git merge-tree --write-tree develop head` clean; diff(develop, tree) == its own paths; blobs + modes == head's.
  (F) its squash on develop (merge-tree then commit-tree with a fixed identity and date, parent = develop). END_TREE = that tree.
  (G) END: diff(develop, END) == the own paths; every END blob+mode == the head's; when the merge-base IS develop, END_TREE == the head's tree.
  (H) MODE PINS (core.filemode is false in the Secuura repo, so a disk bit proves nothing): the RECORDED mode by `git ls-tree` of each pinned
      path == the pin at the HEAD, the alone tree and END. All five PR paths are 100644, so kit.json mode_controls names a path OUTSIDE the PR
      recorded 100755, read by the same instrument at develop / head / END: the instrument is shown to discriminate in the same run.
  (I) THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE TWO AUDIT LEGS AND THE ISSUER DOCKERFILE (kit.json hook_paths): blob + mode at develop, the head and END.
  (K) UNCHANGED PINS (kit.json unchanged_pins): audit-baseline.json (NO baseline row), baseline-contract.mjs and the issuer Dockerfile: blob at develop == head == END.
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head <n>=<sha> (repeatable): refuse unless that head equals it.
--simulate <name> <n>=<sha> (controls): use the given head instead of origin's, skip the ls-remote/branch equality for it, and write
pins_gate48b.SIM-<name>.json instead (never the real pins). --develop <sha> (controls): judge against that develop instead of origin's.
Usage: pin_gate48b.py <scratchpad> [--expect-head n=sha ...] [--simulate name n=sha] [--develop sha]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
CL = os.path.join(SP, 'g48b_sp', 'clone'); ORDER = K['order']; N = ORDER[0]
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate48b sim', GIT_AUTHOR_EMAIL='sim@gate48b.invalid', GIT_COMMITTER_NAME='gate48b sim',
           GIT_COMMITTER_EMAIL='sim@gate48b.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
def git(*a, check=True):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=ENV)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if not os.path.isdir(CL):
    src = K['base_clone'] if os.path.isdir(K['base_clone']) else K['checkout']
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', src, CL], check=True)
    subprocess.run(['git', '-C', CL, 'remote', 'set-url', 'origin', 'git@github.com:Secuura/Distributed_Secuura.git'], check=True)
    print('built scratch clone %s (--shared from %s)' % (CL, src))
bad = []
print('pin_gate48b %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
k = K['prs'][N]
refs = ['refs/heads/develop', 'refs/pull/%s/head' % N, k['branch']]
R = {l.split('\t')[1]: l.split('\t')[0] for l in git('ls-remote', 'origin', *refs).splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', '+refs/pull/%s/head:refs/remotes/pr/%s' % (N, N), '+refs/pull/1354/head:refs/remotes/pr/1354')   # #1354 only as the js-yaml blob reference (lockdelta D6)
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
if DEVOVR:
    DEV = git('rev-parse', DEVOVR + '^{commit}'); print('    develop OVERRIDDEN (controls) -> %s' % DEV)
ph, bh = R.get('refs/pull/%s/head' % N), R.get(k['branch'])
if N in SIMH:
    H = git('rev-parse', SIMH[N] + '^{commit}'); print('    #%s SIMULATED head %s (origin pull/head %s)' % (N, H, ph))
else:
    H = ph
    print('    #%s pull/head %s | branch %s | %s' % (N, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER'))
    if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (N, N, ph, bh))
    if git('rev-parse', 'refs/remotes/pr/%s' % N) != ph: bad.append('(A) #%s fetched head != ls-remote' % N)
    if N in EXP and ph != EXP[N]: bad.append('(A) #%s head %s != the expected (pinned) head %s' % (N, ph, EXP[N]))
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None   # (mode, blob) or None when absent
print('(B) shape')
mb = git('merge-base', DEV, H); par = git('rev-parse', H + '^')
ahead = int(git('rev-list', '--count', '%s..%s' % (mb, H))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
names = git('diff', '--name-only', mb, H).splitlines(); ns = git('diff', '--numstat', mb, H).splitlines()
S = dict(head=H, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, head_tree=git('rev-parse', H + '^{tree}'),
         subject_commit=git('log', '-1', '--format=%s', H), blobs={p: list(ent(H, p)) if ent(H, p) else None for p in names})
print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files: %s' % (N, H, par[:12], mb[:12], ahead, behind, len(names), ' '.join(names)))
print('    numstat: %s' % ' ; '.join(x.replace('\t', ' ') for x in ns))
if N not in SIMH:
    if par != k['expected_parent']: bad.append('(B) #%s parent %s != kit expected_parent %s' % (N, par, k['expected_parent']))
    if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list %s != the PULLS API list (kit.json) %s' % (N, names, k['files']))
print('(C) the develop MOVE since the merge-base, against the PR\'s own paths')
if mb == DEV: print('    #%s merge-base == develop: no move' % N); S['move'] = []
else:
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(names)); S['move'] = mv
    print('    #%s move %s..%s: %d path(s) | reaches its own paths: %s' % (N, mb[:12], DEV[:12], len(mv), hit or 'NONE'))
    print('    #%s move log: %s' % (N, ' ; '.join(git('log', '--format=%h %s', '%s..%s' % (mb, DEV)).splitlines()[:12])))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (N, hit))
print('(D) OVERLAP SUMMARY: 0 pair(s) checked (ONE PR) | %d path(s) in total, %d distinct' % (len(names), len(set(names))))
print('(E) the PR ALONE over develop %s' % DEV[:12])
mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H], capture_output=True, text=True, env=ENV)
t = mt.stdout.split('\n')[0].strip(); d = git('diff', '--name-only', DEV, t).splitlines() if mt.returncode == 0 else []
eq = mt.returncode == 0 and all(ent(t, p) == ent(H, p) for p in names)
S['alone_tree'] = t; S['alone_clean'] = mt.returncode == 0
print('    #%s alone: merge-tree rc %d tree %s | diff(develop, tree) == own paths: %s | blobs+modes == head: %s' % (N, mt.returncode, t, sorted(d) == sorted(names), eq))
if mt.returncode or sorted(d) != sorted(names) or not eq: bad.append('(E) #%s does not merge ALONE cleanly onto develop' % N)
print('(F) the squash on develop (commit-tree -p develop)')
END = None; SQ = None
if mt.returncode == 0:
    SQ = git('commit-tree', t, '-p', DEV, '-m', 'gate48b simulated squash of #%s' % N); END = git('rev-parse', SQ + '^{tree}')
    print('    squash_sim %s | tree %s' % (SQ, END))
print('(G) END')
if END:
    d = git('diff', '--name-only', DEV, END).splitlines(); ok = sorted(d) == sorted(names) and all(ent(END, p) == ent(H, p) for p in names)
    print('    END_TREE %s | diff(develop, END): %d path(s) == the own paths (%d): %s | every END blob+mode == the head\'s: %s' % (END, len(d), len(names), sorted(d) == sorted(names), ok))
    print('    END_TREE == the head\'s own tree %s: %s (%s)' % (S['head_tree'][:12], END == S['head_tree'], 'expected True: the merge-base IS develop' if mb == DEV else 'the head is behind develop: False is expected'))
    if not ok: bad.append('(G) END diff / blobs disagree with the head')
    if mb == DEV and END != S['head_tree']: bad.append('(G) merge-base == develop but END_TREE != the head tree')
    print('    git diff --shortstat develop END: %s' % git('diff', '--shortstat', DEV, END))
else: bad.append('(F) no END: the squash could not be simulated')
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone tree / END, and the control path at develop / head / END')
MODES = []
for p, want in sorted(k.get('mode_pins', {}).items()):
    got = {'head': (ent(H, p) or ('ABSENT',))[0], 'alone': (ent(t, p) or ('ABSENT',))[0] if S['alone_clean'] else 'n/a', 'END': (ent(END, p) or ('ABSENT',))[0] if END else 'n/a'}
    ok = all(v == want for v in got.values()); MODES.append(dict(pr=N, path=p, want=want, got=got, ok=ok, control=False))
    print('    #%s %s: want %s | head %s | alone %s | END %s | %s' % (N, p, want, got['head'], got['alone'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) #%s %s recorded mode %s != the pin %s' % (N, p, got, want))
for p, want in sorted(K.get('mode_controls', {}).items()):
    got = {'develop': (ent(DEV, p) or ('ABSENT',))[0], 'head': (ent(H, p) or ('ABSENT',))[0], 'END': (ent(END, p) or ('ABSENT',))[0] if END else 'n/a'}
    ok = all(v == want for v in got.values()); MODES.append(dict(pr='control', path=p, want=want, got=got, ok=ok, control=True))
    print('    CONTROL (not a PR path) %s: want %s | develop %s | head %s | END %s | %s' % (p, want, got['develop'], got['head'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) control path %s recorded mode %s != %s' % (p, got, want))
print('    MODE SUMMARY: %d path(s) pinned (%d PR, %d control), %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (
    len(MODES), sum(not m['control'] for m in MODES), sum(m['control'] for m in MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
print('(I) THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE AUDIT LEGS, THE ISSUER DOCKERFILE — blob+mode per tree')
HOOKS = {}; trees = [('develop', DEV), ('#%s head' % N, H)] + ([('END', END)] if END else [])
for p in K.get('hook_paths', []):
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1
    HOOKS[p] = {lab: list(v) if v else None for lab, v in es.items()}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, (v[0] + ' ' + v[1][:12]) if v else 'ABSENT') for lab, v in es.items()), 'IDENTICAL in every tree' if same else 'DIFFERS between trees'))
print('(K) UNCHANGED PINS (blob at develop == head == END)')
UNCH = {}
for p, why in K.get('unchanged_pins', {}).items():
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1 and None not in es.values()
    UNCH[p] = {'same': same, 'blobs': {lab: list(v) if v else None for lab, v in es.items()}}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, v[1][:12] if v else 'ABSENT') for lab, v in es.items()), 'BYTE-EQUAL at develop, head and END' if same else 'CHANGED'))
    if not same: bad.append('(K) %s is not byte-equal at develop / head / END (%s)' % (p, why))
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': {N: S}, 'overlap_pairs': [],
     'paths_total': len(names), 'paths_distinct': len(set(names)), 'union': sorted(names), 'end_tree': END, 'squash_sim': SQ,
     'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate48b.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate48b.SIM-%s.json' % SIM if SIM else 'pins_gate48b.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | END_TREE %s | 1 PR, %d paths' % (f, DEV[:12], END, len(names)))
