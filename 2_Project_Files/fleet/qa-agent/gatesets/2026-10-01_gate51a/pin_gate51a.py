#!/usr/bin/env python3
"""pin_gate51a.py — MEASURE the pins for the gate51a kit (kit.json beside this script) and write pins_gate51a.json. ONE PR (#1365, KS-1364, T2):
`required: true` on 11 request bodies in 4 *.openapi.ts files, 6 new spec-rendering tests, the generated docs/openapi yaml. No runtime handler change.
Reads origin by `git ls-remote` (Secuura deploy key, in the SCRATCH clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g51a_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
  (A) head: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched == ls-remote; == kit.json prs.<n>.head (the head Wednesday named).
  (B) shape: merge-base, ahead / behind, head parent (in kit expected_parent_any), file list == kit.json files (11) AND numstat (summed; the seat
      claimed +316/-6 — PRINTED beside the measured sum); 0 paths outside kit.json allowed_prefixes; 0 package.json / lock paths.
  (C) the develop MOVE since the merge-base, against the PR's own paths (must be EMPTY).
  (E) ALONE over develop: merge-tree clean; diff(develop, tree) == own paths; blobs + modes == head's.
  (F) the SQUASH simulated (commit-tree, fixed identity and date, parent = develop) -> END_TREE; diff(develop, END) == own paths.
  (H) MODE PINS: the RECORDED mode (`git ls-tree`) of every PR path at head / alone / END (all 11 100644); kit.json mode_controls names a path
      OUTSIDE the PR recorded 100755 (scripts/run-migrations.sh), read at develop / head / END (the control that discriminates).
  (I) THE HOOK, THE PREFLIGHT, THE GENERATOR, THE SPEC-EXAMPLES CHECK, package.json (kit.json hook_paths): blob+mode per tree.
  (K) UNCHANGED PINS (kit.json unchanged_pins): the blob at develop == head == END — the 11 operations' HANDLER files, the schema file, the four
      express.json mounts, the generator, package.json and the lock (the no-runtime-change proof by blob).
Refuses rc 1 on any disagreement; writes pins only on PASS. --simulate <name> <n>=<sha> (controls / dry tests): use that head, skip the
ls-remote/branch equality for it, write pins_gate51a.SIM-<name>.json (never the real pins). --develop <sha> (controls, needs --simulate).
Usage: pin_gate51a.py <scratchpad> [--simulate name n=sha] [--develop sha]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
N = K['order'][0]
if N == '<PR>' and not SIM: raise SystemExit('REFUSING: kit.json is UNPINNED (<PR>) — run pinpr_gate51a.py <PR> <HEAD> first (a --simulate run is allowed)')
CL = os.path.join(SP, 'g51a_sp', 'clone'); k = K['prs'][N]
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate51a sim', GIT_AUTHOR_EMAIL='sim@gate51a.invalid', GIT_COMMITTER_NAME='gate51a sim',
           GIT_COMMITTER_EMAIL='sim@gate51a.invalid', GIT_AUTHOR_DATE='2026-10-01T00:00:00Z', GIT_COMMITTER_DATE='2026-10-01T00:00:00Z')
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
print('pin_gate51a %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
refs = ['refs/heads/develop'] + ([] if N in SIMH else ['refs/pull/%s/head' % N, k['branch']])
R = {l.split('\t')[1]: l.split('\t')[0] for l in git('ls-remote', 'origin', *refs).splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', *([] if N in SIMH else ['+refs/pull/%s/head:refs/remotes/pr/%s' % (N, N)]))
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
if DEVOVR: DEV = git('rev-parse', DEVOVR + '^{commit}'); print('    develop OVERRIDDEN (controls) -> %s' % DEV)
if N in SIMH:
    H = git('rev-parse', SIMH[N] + '^{commit}'); print('    #%s SIMULATED head %s' % (N, H))
else:
    ph, bh = R.get('refs/pull/%s/head' % N), R.get(k['branch'])
    H = ph
    print('    #%s pull/head %s | branch %s | %s | kit head %s' % (N, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER', k['head']))
    if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (N, N, ph, bh))
    if git('rev-parse', 'refs/remotes/pr/%s' % N) != ph: bad.append('(A) #%s fetched head != ls-remote' % N)
    if ph != k['head']: bad.append('(A) #%s head %s != kit.json head %s (the head Wednesday named) — a new head is a re-draft' % (N, ph, k['head']))
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None
print('(B) shape')
mb = git('merge-base', DEV, H); par = git('rev-parse', H + '^')
ahead = int(git('rev-list', '--count', '%s..%s' % (mb, H))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
names = git('diff', '--name-only', mb, H).splitlines(); ns = git('diff', '--numstat', mb, H).splitlines()
adds = sum(int(x.split('\t')[0]) for x in ns if x.split('\t')[0].isdigit()); dels = sum(int(x.split('\t')[1]) for x in ns if x.split('\t')[1].isdigit())
nonlock = [p for p in names if not any(p.startswith(x) for x in K['allowed_prefixes'])]; manif = [p for p in names if p.endswith('package.json') or p.endswith('package-lock.json')]
S = dict(head=H, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, adds=adds, dels=dels, head_tree=git('rev-parse', H + '^{tree}'),
         subject_commit=git('log', '-1', '--format=%s', H), blobs={p: list(ent(H, p)) if ent(H, p) else None for p in names})
print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files | numstat sum +%d/-%d (the seat claimed %s) | paths outside the allowed prefixes %d | manifest/lock paths %d' % (
    N, H, par[:12], mb[:12], ahead, behind, len(names), adds, dels, k['claimed_numstat'], len(nonlock), len(manif)))
for x in ns: print('    numstat %s' % x.replace('\t', ' '))
if N not in SIMH and par not in k['expected_parent_any']: bad.append('(B) #%s parent %s is not one of kit expected parents %s' % (N, par, k['expected_parent_any']))
if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list != kit.json files: extra %s missing %s' % (N, sorted(set(names) - set(k['files'])), sorted(set(k['files']) - set(names))))
if nonlock or manif: bad.append('(B) paths outside the allowed prefixes %s / manifest or lock paths %s in a spec-annotation PR' % (nonlock, manif))
print('(C) the develop MOVE since the merge-base, against the PR\'s own paths')
if mb == DEV: print('    merge-base == develop: no move'); S['move'] = []
else:
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(names)); S['move'] = mv
    print('    #%s move %s..%s: %d path(s) | reaches its own paths: %s' % (N, mb[:12], DEV[:12], len(mv), hit or 'NONE'))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (N, hit))
print('(E) ALONE over develop %s' % DEV[:12])
mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H], capture_output=True, text=True, env=ENV)
T = mt.stdout.split('\n')[0].strip(); d = git('diff', '--name-only', DEV, T).splitlines() if mt.returncode == 0 else []
eq = mt.returncode == 0 and all(ent(T, p) == ent(H, p) for p in names)
print('    merge-tree rc %d tree %s | diff(develop, tree) == own paths: %s | blobs+modes == head: %s' % (mt.returncode, T, sorted(d) == sorted(names), eq))
if mt.returncode or sorted(d) != sorted(names) or not eq: bad.append('(E) #%s does not merge cleanly onto develop' % N)
END = SQ = None
if mt.returncode == 0:
    SQ = git('commit-tree', T, '-p', DEV, '-m', 'gate51a simulated squash of #%s' % N); END = git('rev-parse', SQ + '^{tree}')
    print('(F) squash_sim %s | END_TREE %s | git diff --shortstat develop END: %s' % (SQ, END, git('diff', '--shortstat', DEV, END)))
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone / END, and the control path at develop / head / END')
MODES = []; g = lambda t, p: (ent(t, p) or ('ABSENT',))[0]
for p, want in sorted(k.get('mode_pins', {}).items()):
    got = {'head': g(H, p), 'alone': g(T, p) if mt.returncode == 0 else 'n/a', 'END': g(END, p) if END else 'n/a'}
    ok = all(v == want for v in got.values()); MODES.append(dict(path=p, want=want, got=got, ok=ok, control=False))
    if not ok: print('    %s: want %s | %s | MODE MISMATCH' % (p, want, got)); bad.append('(H) %s recorded mode %s != the pin %s' % (p, got, want))
for p, want in sorted(K.get('mode_controls', {}).items()):
    got = {'develop': g(DEV, p), 'head': g(H, p), 'END': g(END, p) if END else 'n/a'}
    ok = all(v == want for v in got.values()); MODES.append(dict(path=p, want=want, got=got, ok=ok, control=True))
    print('    CONTROL (not a PR path) %s: want %s | %s | %s' % (p, want, ' | '.join('%s %s' % x for x in got.items()), 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) control path %s recorded mode %s != %s' % (p, got, want))
print('    MODE SUMMARY: %d path(s) pinned (%d PR, %d control), %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (
    len(MODES), sum(not m['control'] for m in MODES), sum(m['control'] for m in MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
print('(I) THE HOOK, THE PREFLIGHT, THE GENERATOR, THE SPEC-EXAMPLES CHECK, package.json — blob+mode per tree')
trees = [('develop', DEV), ('head', H)] + ([('END', END)] if END else []); HOOKS = {}
for p in K.get('hook_paths', []):
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1
    HOOKS[p] = {lab: list(v) if v else None for lab, v in es.items()}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, (v[0] + ' ' + v[1][:12]) if v else 'ABSENT') for lab, v in es.items()), 'IDENTICAL in every tree' if same else 'DIFFERS between trees'))
print('(K) UNCHANGED PINS (blob at develop == head == END)')
UNCH = {}
for p, why in K.get('unchanged_pins', {}).items():
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1 and None not in es.values()
    UNCH[p] = {'same': same, 'blobs': {lab: list(v) if v else None for lab, v in es.items()}}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, v[1][:12] if v else 'ABSENT') for lab, v in es.items()), 'BYTE-EQUAL in every tree' if same else 'CHANGED'))
    if not same: bad.append('(K) %s is not byte-equal in every tree (%s)' % (p, why))
P = {'measured_at': now(), 'pr': N, 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'pr_pins': S, 'alone_tree': T, 'end_tree': END, 'squash_sim': SQ,
     'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH}
f = 'pins_gate51a.SIM-%s.json' % SIM if SIM else 'pins_gate51a.json'
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
    raise SystemExit(1)
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | head %s | END_TREE %s | %d paths +%d/-%d' % (f, DEV[:12], H[:12], END, len(names), adds, dels))
