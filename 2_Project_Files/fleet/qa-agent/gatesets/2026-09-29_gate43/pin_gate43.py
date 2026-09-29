#!/usr/bin/env python3
"""pin_gate43.py — MEASURE the pins for the gate43 kit (kit.json beside this script) and write pins_gate43.json. FIVE PRs, merged in kit order.
Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g43_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
  (A) heads: refs/pull/<n>/head == the branch (WHOLE-FIELD) for each PR; fetched refs == ls-remote.
  (B) shape: each PR's merge-base, ahead / behind, head parent (== kit expected_parent), file list == kit.json files (the PULLS API's) AND numstat.
  (C) the develop MOVE since each merge-base: the moved paths, and their intersection with that PR's own paths (must be EMPTY — a move that
      reaches a PR's cells refuses; say which move it was).
  (D) the OVERLAP matrix: every pair of PRs, the intersection of their path sets. Prints the pair count, distinct-path count and the total.
      The kit PREDICTS zero overlap (the author's claim). An overlap is NOT a refusal by itself; a chain step that is not clean is.
  (E) each PR ALONE over develop: `git merge-tree --write-tree develop head` clean; diff(develop, that tree) == its own paths; blobs + modes == head's.
  (F) the CHAIN in kit order, each merge a squash on the previous tip (merge-tree then commit-tree with a fixed identity and date, parent = tip):
      every step clean; diff(tip, new tip) == that PR's own paths; every blob + mode == the head's. END_TREE = the last tip's tree.
  (G) END: diff(develop, END) == the union of the own paths; every END blob == its head blob. The REVERSE order is also chained: its tree must
      equal END_TREE (order independence — a property of disjoint paths, measured, not assumed).
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head <n>=<sha> (repeatable): refuse unless that head equals it.
--simulate <name> <n>=<sha>[,<n>=<sha>] (controls): use the given head(s) instead of origin's for those PRs, skip the ls-remote/branch equality
for them, and write pins_gate43.SIM-<name>.json instead (never the real pins).
Usage: pin_gate43.py <scratchpad> [--expect-head n=sha ...] [--simulate name n=sha[,n=sha]]"""
import json, os, subprocess, sys, datetime, itertools
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
CL = os.path.join(SP, 'g43_sp', 'clone'); ORDER = K['order']
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate43 sim', GIT_AUTHOR_EMAIL='sim@gate43.invalid', GIT_COMMITTER_NAME='gate43 sim',
           GIT_COMMITTER_EMAIL='sim@gate43.invalid', GIT_AUTHOR_DATE='2026-09-29T00:00:00Z', GIT_COMMITTER_DATE='2026-09-29T00:00:00Z')
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
print('pin_gate43 %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [K['prs'][n]['branch'] for n in ORDER]
ls = git('ls-remote', 'origin', *refs)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
fetch = ['+refs/heads/develop:refs/remotes/origin/develop'] + ['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in ORDER]
git('fetch', '-q', 'origin', *fetch)
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
H = {}
for n in ORDER:
    ph, bh = R.get('refs/pull/%s/head' % n), R.get(K['prs'][n]['branch'])
    if n in SIMH:
        H[n] = git('rev-parse', SIMH[n] + '^{commit}'); print('    #%s SIMULATED head %s (origin pull/head %s)' % (n, H[n], ph)); continue
    H[n] = ph
    print('    #%s pull/head %s | branch %s | %s' % (n, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER'))
    if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (n, n, ph, bh))
    if git('rev-parse', 'refs/remotes/pr/%s' % n) != ph: bad.append('(A) #%s fetched head != ls-remote' % n)
    if n in EXP and ph != EXP[n]: bad.append('(A) #%s head %s != the expected (pinned) head %s' % (n, ph, EXP[n]))
def tree_entries(t, paths):
    out = {}
    for p in paths:
        l = git('ls-tree', t, '--', p)
        out[p] = tuple(l.split()[0:3:2]) if l else None   # (mode, blob) or None when absent
    return out
S = {}
print('(B) shape per PR')
for n in ORDER:
    h = H[n]; mb = git('merge-base', DEV, h); par = git('rev-parse', h + '^')
    ahead = int(git('rev-list', '--count', '%s..%s' % (mb, h))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
    names = git('diff', '--name-only', mb, h).splitlines(); ns = git('diff', '--numstat', mb, h).splitlines()
    S[n] = dict(head=h, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, head_tree=git('rev-parse', h + '^{tree}'),
                subject_commit=git('log', '-1', '--format=%s', h), blobs={p: list(v) if v else None for p, v in tree_entries(h, names).items()})
    print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files: %s' % (n, h, par[:12], mb[:12], ahead, behind, len(names), ' '.join(names)))
    if n not in SIMH:
        if par != K['prs'][n]['expected_parent']: bad.append('(B) #%s parent %s != kit expected_parent %s' % (n, par, K['prs'][n]['expected_parent']))
        if sorted(names) != sorted(K['prs'][n]['files']): bad.append('(B) #%s git file list %s != the PULLS API list (kit.json) %s' % (n, names, K['prs'][n]['files']))
print('(C) the develop MOVE since each merge-base, against that PR\'s own paths')
for n in ORDER:
    mb = S[n]['merge_base']
    if mb == DEV: print('    #%s merge-base == develop: no move' % n); S[n]['move'] = []; continue
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(S[n]['files'])); S[n]['move'] = mv
    print('    #%s move %s..%s: %d path(s) %s | reaches its own paths: %s' % (n, mb[:12], DEV[:12], len(mv), mv, hit or 'NONE'))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(D) the OVERLAP matrix (every pair)')
allp = [p for n in ORDER for p in S[n]['files']]; union = sorted(set(allp)); pairs = []
for a, b in itertools.combinations(ORDER, 2):
    x = sorted(set(S[a]['files']) & set(S[b]['files']))
    if x: pairs.append((a, b, x)); print('    OVERLAP #%s x #%s: %s' % (a, b, x))
print('    OVERLAP SUMMARY: %d pair(s) checked, %d overlapping | %d path(s) in total, %d distinct | the author claimed %d distinct paths with zero overlap'
      % (len(list(itertools.combinations(ORDER, 2))), len(pairs), len(allp), len(union), K['author_claim_paths']))
print('(E) each PR ALONE over develop %s' % DEV[:12])
for n in ORDER:
    mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H[n]], capture_output=True, text=True)
    t = mt.stdout.split('\n')[0].strip(); d = git('diff', '--name-only', DEV, t).splitlines() if mt.returncode == 0 else []
    eq = tree_entries(t, S[n]['files']) == tree_entries(H[n], S[n]['files']) if mt.returncode == 0 else False
    S[n]['alone_tree'] = t; S[n]['alone_clean'] = mt.returncode == 0
    print('    #%s alone: merge-tree rc %d tree %s | diff(develop, tree) == own paths: %s | blobs+modes == head: %s' % (n, mt.returncode, t, sorted(d) == sorted(S[n]['files']), eq))
    if mt.returncode or sorted(d) != sorted(S[n]['files']) or not eq: bad.append('(E) #%s does not merge ALONE cleanly onto develop' % n)
def chain(order, label):
    tip = DEV; steps = []
    for n in order:
        mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', tip, H[n]], capture_output=True, text=True, env=ENV)
        t = mt.stdout.split('\n')[0].strip()
        if mt.returncode:
            print('    %s step #%s: merge-tree rc %d — CONFLICT: %s' % (label, n, mt.returncode, ' '.join(mt.stdout.split('\n')[1:6])[:240]))
            return None, steps, 'step #%s NOT clean (rc %d)' % (n, mt.returncode)
        sq = git('commit-tree', t, '-p', tip, '-m', 'gate43 simulated squash of #%s' % n)
        d = git('diff', '--name-only', tip, sq).splitlines(); eq = tree_entries(t, S[n]['files']) == tree_entries(H[n], S[n]['files'])
        steps.append(dict(pr=n, tree=t, squash_sim=sq, paths=d, own_equal=sorted(d) == sorted(S[n]['files']), blobs_equal=eq))
        print('    %s step #%s on %s: clean | tree %s | diff(tip, new) == own paths: %s | blobs+modes == head: %s' % (label, n, tip[:12], t, sorted(d) == sorted(S[n]['files']), eq))
        if sorted(d) != sorted(S[n]['files']) or not eq: return None, steps, 'step #%s diff / blob mismatch' % n
        tip = sq
    return git('rev-parse', tip + '^{tree}'), steps, None
print('(F) the CHAIN in kit order %s (each a squash on the previous tip)' % ' -> '.join(ORDER))
END, STEPS, err = chain(ORDER, 'ORDER')
if err: bad.append('(F) chain: ' + err)
print('(G) END')
REV = None
if END:
    d = git('diff', '--name-only', DEV, END).splitlines(); fin = tree_entries(END, union)
    heads = {p: tree_entries(H[n], [p])[p] for n in ORDER for p in S[n]['files']}
    print('    END_TREE %s | diff(develop, END): %d path(s) == the union of the own paths (%d): %s | every END blob+mode == its head\'s: %s'
          % (END, len(d), len(union), sorted(d) == union, all(fin[p] == heads[p] for p in union)))
    if sorted(d) != union or not all(fin[p] == heads[p] for p in union): bad.append('(G) END diff / blobs disagree with the union of the heads')
    REV, _, rerr = chain(list(reversed(ORDER)), 'REVERSE')
    print('    REVERSE-order END %s | == END_TREE: %s' % (REV, REV == END))
    if REV != END: bad.append('(G) the reverse-order END %s != END_TREE %s (%s)' % (REV, END, rerr))
    print('    git diff --shortstat develop END: %s' % git('diff', '--shortstat', DEV, END))
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': S, 'overlap_pairs': pairs,
     'paths_total': len(allp), 'paths_distinct': len(union), 'union': union, 'end_tree': END, 'reverse_end_tree': REV, 'chain': STEPS,
     'simulate': SIM, 'simulated_heads': SIMH}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate43.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate43.SIM-%s.json' % SIM if SIM else 'pins_gate43.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | END_TREE %s | %d PRs, %d distinct paths, %d overlapping pair(s)' % (f, DEV[:12], END, len(ORDER), len(union), len(pairs)))
