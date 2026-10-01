#!/usr/bin/env python3
"""pin_gate53.py — MEASURE the pins for the gate53 kit (kit.json beside this script) and write pins_gate53.json. ONE PR (#1369, KS-530, T1):
a scoped npm override `"@prisma/dev": { "@hono/node-server": "^1.19.15" }` in the root manifest, the one nested lock entry
`node_modules/@prisma/dev/node_modules/@hono/node-server` (1.19.11) pruned from the root lock, and the GHSA-frvp-7c67-39w9 baseline row removed.
Reads origin by `git ls-remote` (Secuura deploy key, in the SCRATCH clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g53_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
  (A) head: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched == ls-remote; == kit.json prs.<n>.head (the head Wednesday named).
  (B) shape: merge-base, ahead / behind, head parent (in kit expected_parent_any), file list == kit.json files (3) == kit.json allowed_paths
      EXACTLY, and the numstat per path == kit.json numstat_expect (+3/-0, 0/-11, 0/-7; the seat claimed +3/-18 — PRINTED beside the sum).
  (C) the develop MOVE since the merge-base, against the PR's own paths (must be EMPTY).
  (E) ALONE over develop: merge-tree clean; diff(develop, tree) == own paths; blobs + modes == head's.
  (F) the SQUASH simulated (commit-tree, fixed identity and date, parent = develop) -> END_TREE; diff(develop, END) == own paths; END_TREE ==
      kit.json end_tree_predicted (the seat's PREDICTED tree) — REFUSED otherwise (a develop move changes it: that is a re-draft).
  (H) MODE PINS: the RECORDED mode (`git ls-tree`) of every PR path at head / alone / END (all 3 100644); kit.json mode_controls names a path
      OUTSIDE the PR recorded 100755 (scripts/run-migrations.sh), read at develop / head / END (the control that discriminates).
  (I) THE HOOK and THE PREFLIGHT (kit.json hook_paths): blob+mode per tree.
  (K) UNCHANGED PINS (kit.json unchanged_pins): the blob at develop == head == END — leg 6 / leg 7 / the baseline contract and its test and
      case count, lock discovery, originate's manifest + STANDALONE lock + Dockerfile, mcp-server's lock, the prisma schema.
Refuses rc 1 on any disagreement; writes pins only on PASS. --simulate <name> <n>=<sha> (controls / dry tests): use that head, skip the
ls-remote/branch equality for it, write pins_gate53.SIM-<name>.json (never the real pins). --develop <sha> (controls, needs --simulate).
A NEW COPY of gate51a's pin (one PR), re-keyed by hand for a lock + baseline PR. Usage: pin_gate53.py <scratchpad> [--simulate name n=sha] [--develop sha]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
N = K['order'][0]
CL = os.path.join(SP, 'g53_sp', 'clone'); k = K['prs'][N]
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate53 sim', GIT_AUTHOR_EMAIL='sim@gate53.invalid', GIT_COMMITTER_NAME='gate53 sim',
           GIT_COMMITTER_EMAIL='sim@gate53.invalid', GIT_AUTHOR_DATE='2026-10-02T00:00:00Z', GIT_COMMITTER_DATE='2026-10-02T00:00:00Z')
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
print('pin_gate53 %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
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
outside = [p for p in names if p not in K['allowed_paths']]
nsd = {x.split('\t')[2]: [int(x.split('\t')[0]), int(x.split('\t')[1])] for x in ns if x.split('\t')[0].isdigit()}
S = dict(head=H, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, adds=adds, dels=dels, head_tree=git('rev-parse', H + '^{tree}'),
         subject_commit=git('log', '-1', '--format=%s', H), blobs={p: list(ent(H, p)) if ent(H, p) else None for p in names})
print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files | numstat sum +%d/-%d (the seat claimed %s) | paths outside the 3 allowed paths %d' % (
    N, H, par[:12], mb[:12], ahead, behind, len(names), adds, dels, k['claimed_numstat'], len(outside)))
for x in ns: print('    numstat %s' % x.replace('\t', ' '))
if N not in SIMH and par not in k['expected_parent_any']: bad.append('(B) #%s parent %s is not one of kit expected parents %s' % (N, par, k['expected_parent_any']))
if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list != kit.json files: extra %s missing %s' % (N, sorted(set(names) - set(k['files'])), sorted(set(k['files']) - set(names))))
if outside: bad.append('(B) paths outside the allowed paths %s' % outside)
for p, want in sorted(k['numstat_expect'].items()):
    if nsd.get(p) != want: bad.append('(B) numstat %s %s != expected %s' % (p, nsd.get(p), want))
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
    SQ = git('commit-tree', T, '-p', DEV, '-m', 'gate53 simulated squash of #%s' % N); END = git('rev-parse', SQ + '^{tree}')
    print('(F) squash_sim %s | END_TREE %s | git diff --shortstat develop END: %s' % (SQ, END, git('diff', '--shortstat', DEV, END)))
    print('    END_TREE %s the seat\'s PREDICTED %s' % ('==' if END == K['end_tree_predicted'] else '!=', K['end_tree_predicted']))
    if END != K['end_tree_predicted']: bad.append('(F) END_TREE %s != the seat\'s PREDICTED %s (a develop move or a new head: a re-draft)' % (END, K['end_tree_predicted']))
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
print('(I) THE HOOK and THE PREFLIGHT — blob+mode per tree')
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
P = {'measured_at': now(), 'pr': N, 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'pr_pins': {N: S}, 'alone_tree': T, 'end_tree': END, 'squash_sim': SQ,
     'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH}
f = 'pins_gate53.SIM-%s.json' % SIM if SIM else 'pins_gate53.json'
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
    raise SystemExit(1)
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | head %s | END_TREE %s | %d paths +%d/-%d' % (f, DEV[:12], H[:12], END, len(names), adds, dels))
