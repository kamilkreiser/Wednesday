#!/usr/bin/env python3
"""pin_gate52.py — MEASURE the pins for the gate52 kit (kit.json beside this script) and write pins_gate52.json. TWO PRs, SIBLINGS on one develop,
merged A (#1367, KS-1015) THEN B (#1368, KS-1364); both T2 OpenAPI annotations + spec-rendering tests + the generated yaml, no runtime change.
Reads origin by `git ls-remote` (Secuura deploy key, in the SCRATCH clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g52_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then, per PR:
  (A) head: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched == ls-remote; == kit.json prs.<n>.head (the head Wednesday named).
  (B) shape: merge-base, ahead / behind, head parent (in kit expected_parent_any), file list == kit.json files AND numstat (summed; the seat's
      claim PRINTED beside it); 0 paths outside kit.json allowed_prefixes; 0 package.json / lock paths.
  (C) the develop MOVE since the merge-base, against the PR's own paths (must be EMPTY).
  (E) EACH ALONE over develop: merge-tree clean; diff(develop, tree) == own paths; blobs + modes == head's (siblings both stay mergeable).
And over the pair:
  (F) THE CHAIN, simulated: A squashed onto develop (commit-tree, fixed identity/date, parent develop) -> END_TREE_A; B merged onto that squash
      (merge-tree --write-tree SQ_A B; commit-tree -p SQ_A) -> END_TREE_B. diff(END_A, END_B) == B's paths; diff(develop, END_B) == the union;
      every B blob at END_B == B's head EXCEPT the shared yaml; END_TREE_B == kit end_tree_after_b_predicted (the seat's PREDICTED tree).
      Second instrument: merge-tree --write-tree A B (the seat's own way) must give the same tree.
  (H) MODE PINS: the RECORDED mode (`git ls-tree`) of every PR path at its head / alone / END_B (all 100644); kit.json mode_controls names a path
      OUTSIDE the PRs recorded 100755, read at develop / both heads / END_B (the control that discriminates).
  (I) THE HOOK, THE PREFLIGHT, THE GENERATOR, THE SPEC-EXAMPLES CHECK, package.json (kit.json hook_paths): blob+mode per tree.
  (K) UNCHANGED PINS (kit.json unchanged_pins): the blob at develop == A == B == END_A == END_B — the handler, service, error-handler, mount and
      shared response files, the generator, package.json and the four lockfiles (the no-runtime-change proof by blob).
Refuses rc 1 on any disagreement; writes pins only on PASS. --simulate <name> <n>=<sha>[,<n>=<sha>] (controls / dry tests): use those heads, skip
the ls-remote/branch equality for them, write pins_gate52.SIM-<name>.json (never the real pins). --develop <sha> (controls, needs --simulate).
Usage: pin_gate52.py <scratchpad> [--simulate name n=sha[,n=sha]] [--develop sha]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
ORDER = K['order']; NA, NB = ORDER
CL = os.path.join(SP, 'g52_sp', 'clone')
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate52 sim', GIT_AUTHOR_EMAIL='sim@gate52.invalid', GIT_COMMITTER_NAME='gate52 sim',
           GIT_COMMITTER_EMAIL='sim@gate52.invalid', GIT_AUTHOR_DATE='2026-10-01T00:00:00Z', GIT_COMMITTER_DATE='2026-10-01T00:00:00Z')
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
print('pin_gate52 %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
refs = ['refs/heads/develop']
for n in ORDER:
    if n not in SIMH: refs += ['refs/pull/%s/head' % n, K['prs'][n]['branch']]
R = {l.split('\t')[1]: l.split('\t')[0] for l in git('ls-remote', 'origin', *refs).splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in ORDER if n not in SIMH])
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
if DEVOVR: DEV = git('rev-parse', DEVOVR + '^{commit}'); print('    develop OVERRIDDEN (controls) -> %s' % DEV)
H = {}
for n in ORDER:
    k = K['prs'][n]
    if n in SIMH:
        H[n] = git('rev-parse', SIMH[n] + '^{commit}'); print('    #%s SIMULATED head %s' % (n, H[n])); continue
    ph, bh = R.get('refs/pull/%s/head' % n), R.get(k['branch']); H[n] = ph
    print('    #%s pull/head %s | branch %s | %s | kit head %s' % (n, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER', k['head']))
    if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (n, n, ph, bh))
    if git('rev-parse', 'refs/remotes/pr/%s' % n) != ph: bad.append('(A) #%s fetched head != ls-remote' % n)
    if ph != k['head']: bad.append('(A) #%s head %s != kit.json head %s (the head Wednesday named) — a new head is a re-draft' % (n, ph, k['head']))
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None
S = {}; ALONE = {}
print('(B) shape')
for n in ORDER:
    k = K['prs'][n]; h = H[n]
    mb = git('merge-base', DEV, h); par = git('rev-parse', h + '^')
    ahead = int(git('rev-list', '--count', '%s..%s' % (mb, h))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
    names = git('diff', '--name-only', mb, h).splitlines(); ns = git('diff', '--numstat', mb, h).splitlines()
    adds = sum(int(x.split('\t')[0]) for x in ns if x.split('\t')[0].isdigit()); dels = sum(int(x.split('\t')[1]) for x in ns if x.split('\t')[1].isdigit())
    nonlock = [p for p in names if not any(p.startswith(x) for x in K['allowed_prefixes'])]; manif = [p for p in names if p.endswith('package.json') or p.endswith('package-lock.json')]
    S[n] = dict(head=h, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, adds=adds, dels=dels, head_tree=git('rev-parse', h + '^{tree}'),
                subject_commit=git('log', '-1', '--format=%s', h), blobs={p: list(ent(h, p)) if ent(h, p) else None for p in names})
    print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files | numstat sum +%d/-%d (the seat claimed %s) | outside prefixes %d | manifest/lock %d' % (
        n, h, par[:12], mb[:12], ahead, behind, len(names), adds, dels, k['claimed_numstat'], len(nonlock), len(manif)))
    for x in ns: print('    numstat #%s %s' % (n, x.replace('\t', ' ')))
    if n not in SIMH and par not in k['expected_parent_any']: bad.append('(B) #%s parent %s is not one of kit expected parents %s' % (n, par, k['expected_parent_any']))
    if sorted(names) != sorted(k['files']): bad.append('(B) #%s file list != kit.json files: extra %s missing %s' % (n, sorted(set(names) - set(k['files'])), sorted(set(k['files']) - set(names))))
    if nonlock or manif: bad.append('(B) #%s paths outside the allowed prefixes %s / manifest or lock paths %s' % (n, nonlock, manif))
print('(B2) SIBLINGS: neither head is an ancestor of the other; both cut from the same develop')
ab = subprocess.run(['git', '-C', CL, 'merge-base', '--is-ancestor', H[NA], H[NB]], env=ENV).returncode
ba = subprocess.run(['git', '-C', CL, 'merge-base', '--is-ancestor', H[NB], H[NA]], env=ENV).returncode
same_base = S[NA]['merge_base'] == S[NB]['merge_base']
print('    #%s ancestor of #%s: %s | #%s ancestor of #%s: %s | same merge-base with develop: %s (%s)' % (NA, NB, ab == 0, NB, NA, ba == 0, same_base, S[NA]['merge_base'][:12]))
if ab == 0 or ba == 0 or not same_base: bad.append('(B2) the two PRs are not siblings on one base (A anc B %s, B anc A %s, same base %s)' % (ab == 0, ba == 0, same_base))
print('(C) the develop MOVE since each merge-base, against the PR\'s own paths')
for n in ORDER:
    mb = S[n]['merge_base']; names = S[n]['files']
    if mb == DEV: print('    #%s merge-base == develop: no move' % n); S[n]['move'] = []
    else:
        mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(names)); S[n]['move'] = mv
        print('    #%s move %s..%s: %d path(s) | reaches its own paths: %s' % (n, mb[:12], DEV[:12], len(mv), hit or 'NONE'))
        if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(E) EACH ALONE over develop %s' % DEV[:12])
def mtree(a, b):
    r = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', a, b], capture_output=True, text=True, env=ENV)
    return r.returncode, r.stdout.split('\n')[0].strip(), r.stdout
for n in ORDER:
    rc, T, _ = mtree(DEV, H[n]); names = S[n]['files']
    d = git('diff', '--name-only', DEV, T).splitlines() if rc == 0 else []
    eq = rc == 0 and all(ent(T, p) == ent(H[n], p) for p in names); ALONE[n] = T if rc == 0 else None
    print('    #%s merge-tree rc %d tree %s | diff(develop, tree) == own paths: %s | blobs+modes == head: %s' % (n, rc, T, sorted(d) == sorted(names), eq))
    if rc or sorted(d) != sorted(names) or not eq: bad.append('(E) #%s does not merge cleanly ALONE onto develop' % n)
END_A = END_B = SQA = SQB = None; CHAIN = {}
if ALONE[NA]:
    SQA = git('commit-tree', ALONE[NA], '-p', DEV, '-m', 'gate52 simulated squash of #%s' % NA); END_A = git('rev-parse', SQA + '^{tree}')
    print('(F) A: squash_sim %s | END_TREE_A %s | git diff --shortstat develop END_A: %s' % (SQA, END_A, git('diff', '--shortstat', DEV, END_A)))
    rc, TB, raw = mtree(SQA, H[NB])
    CHAIN['b_onto_a_rc'] = rc; CHAIN['b_onto_a_conflict_lines'] = [l for l in raw.splitlines()[1:] if l.strip()][:20]
    if rc == 0:
        SQB = git('commit-tree', TB, '-p', SQA, '-m', 'gate52 simulated squash of #%s after #%s' % (NB, NA)); END_B = git('rev-parse', SQB + '^{tree}')
        dab = git('diff', '--name-only', END_A, END_B).splitlines(); dub = git('diff', '--name-only', DEV, END_B).splitlines()
        union = sorted(set(S[NA]['files']) | set(S[NB]['files']))
        nonyaml = [p for p in S[NB]['files'] if p != K['yaml']]; beq = all(ent(END_B, p) == ent(H[NB], p) for p in nonyaml)
        aeq = all(ent(END_B, p) == ent(H[NA], p) for p in S[NA]['files'] if p != K['yaml'])
        rc2, TAB, _ = mtree(H[NA], H[NB])
        print('(F) B onto A\'s squash: merge-tree rc %d (no conflict) | squash_sim %s | END_TREE_B %s | git diff --shortstat develop END_B: %s' % (rc, SQB, END_B, git('diff', '--shortstat', DEV, END_B)))
        print('    diff(END_A, END_B) == B\'s %d paths: %s | diff(develop, END_B) == the union of %d paths: %s | B\'s non-yaml blobs == B head: %s | A\'s non-yaml blobs == A head: %s' % (
            len(S[NB]['files']), sorted(dab) == sorted(S[NB]['files']), len(union), sorted(dub) == union, beq, aeq))
        print('    SECOND INSTRUMENT merge-tree --write-tree A B (the seat\'s way): rc %d tree %s | == END_TREE_B: %s' % (rc2, TAB, TAB == END_B))
        print('    PREDICTED (the seat, kit end_tree_after_b_predicted) %s | END_TREE_B == predicted: %s' % (K['end_tree_after_b_predicted'], END_B == K['end_tree_after_b_predicted']))
        CHAIN.update(merge_tree_a_b=TAB, merge_tree_a_b_rc=rc2)
        if sorted(dab) != sorted(S[NB]['files']) or sorted(dub) != union or not beq or not aeq: bad.append('(F) the chained END_B does not carry exactly the two PRs\' changes')
        if rc2 or TAB != END_B: bad.append('(F) merge-tree A B (%s, rc %d) != the chained END_TREE_B %s' % (TAB, rc2, END_B))
        if END_B != K['end_tree_after_b_predicted']: bad.append('(F) END_TREE_B %s != the seat\'s PREDICTED %s' % (END_B, K['end_tree_after_b_predicted']))
    else: bad.append('(F) #%s does NOT merge cleanly onto #%s\'s simulated squash (rc %d): %s' % (NB, NA, rc, CHAIN['b_onto_a_conflict_lines'][:3]))
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone / END_B, and the control path at develop / heads / END_B')
MODES = []; g = lambda t, p: (ent(t, p) or ('ABSENT',))[0] if t else 'n/a'
for n in ORDER:
    for p, want in sorted(K['prs'][n].get('mode_pins', {}).items()):
        got = {'head': g(H[n], p), 'alone': g(ALONE[n], p), 'END_B': g(END_B, p)}
        ok = all(v == want for v in got.values()); MODES.append(dict(pr=n, path=p, want=want, got=got, ok=ok, control=False))
        if not ok: print('    #%s %s: want %s | %s | MODE MISMATCH' % (n, p, want, got)); bad.append('(H) #%s %s recorded mode %s != the pin %s' % (n, p, got, want))
for p, want in sorted(K.get('mode_controls', {}).items()):
    got = {'develop': g(DEV, p), 'head_' + NA: g(H[NA], p), 'head_' + NB: g(H[NB], p), 'END_B': g(END_B, p)}
    ok = all(v == want for v in got.values()); MODES.append(dict(pr=None, path=p, want=want, got=got, ok=ok, control=True))
    print('    CONTROL (not a PR path) %s: want %s | %s | %s' % (p, want, ' | '.join('%s %s' % x for x in got.items()), 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) control path %s recorded mode %s != %s' % (p, got, want))
print('    MODE SUMMARY: %d path-pin(s) (%d PR, %d control), %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (
    len(MODES), sum(not m['control'] for m in MODES), sum(m['control'] for m in MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
print('(I) THE HOOK, THE PREFLIGHT, THE GENERATOR, THE SPEC-EXAMPLES CHECK, package.json — blob+mode per tree')
trees = [('develop', DEV), ('head_' + NA, H[NA]), ('head_' + NB, H[NB])] + ([('END_A', END_A)] if END_A else []) + ([('END_B', END_B)] if END_B else []); HOOKS = {}
for p in K.get('hook_paths', []):
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1
    HOOKS[p] = {lab: list(v) if v else None for lab, v in es.items()}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, (v[0] + ' ' + v[1][:12]) if v else 'ABSENT') for lab, v in es.items()), 'IDENTICAL in every tree' if same else 'DIFFERS between trees'))
print('(K) UNCHANGED PINS (blob at develop == both heads == END_A == END_B)')
UNCH = {}
for p, why in K.get('unchanged_pins', {}).items():
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1 and None not in es.values()
    UNCH[p] = {'same': same, 'blobs': {lab: list(v) if v else None for lab, v in es.items()}}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, v[1][:12] if v else 'ABSENT') for lab, v in es.items()), 'BYTE-EQUAL in every tree' if same else 'CHANGED'))
    if not same: bad.append('(K) %s is not byte-equal in every tree (%s)' % (p, why))
P = {'measured_at': now(), 'order': ORDER, 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'pr_pins': S, 'alone_trees': ALONE,
     'end_tree_a': END_A, 'squash_sim_a': SQA, 'end_tree_b': END_B, 'squash_sim_b': SQB, 'chain': CHAIN,
     'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH}
f = 'pins_gate52.SIM-%s.json' % SIM if SIM else 'pins_gate52.json'
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
    raise SystemExit(1)
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | #%s %s END_TREE_A %s | #%s %s END_TREE_B %s | %d + %d paths' % (
    f, DEV[:12], NA, H[NA][:12], END_A, NB, H[NB][:12], END_B, len(S[NA]['files']), len(S[NB]['files'])))
