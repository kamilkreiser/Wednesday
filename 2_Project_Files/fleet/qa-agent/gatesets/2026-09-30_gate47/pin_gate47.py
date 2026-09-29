#!/usr/bin/env python3
"""pin_gate47.py — MEASURE the pins for the gate47 kit (kit.json beside this script) and write pins_gate47.json. TWO PRs (#1349 T2 KS-1374, #1350 T1 KS-1054), merged in kit order
(#1349 first: it is ONE commit behind develop, raised on 8c810023f9c9 before #1348's squash a72149a1a803 landed; #1350 sits on a72149a1a803).
Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g47_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
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
  (H) MODE PINS (kit.json prs.<n>.mode_pins; core.filemode is false in the Secuura repo, so a disk bit proves nothing): the RECORDED mode by
      `git ls-tree` of every pinned path == the pin at the HEAD, at the PR-alone tree, at the PR's chain step and at END. Both directions are
      pinned (#1350: the three scripts 100755, its test file 100644 in the SAME commit; #1349: both paths 100644), so the instrument is shown to
      discriminate.
  (I) THE HOOK AND THE PREFLIGHT (kit.json hook_paths): blob + mode of each at develop, at each head and at END — the gate reads the hook AT THE
      HEAD; a hook that differs between trees is printed, not refused.
  (J) THE HOOK'S PATH CLASS (a path-prefix READING, not the hook's own logic — the gate drives the hook): per PR, how many of its paths sit under
      Blockchain/Dev/ (the hook's preflight trigger) and how many under systemTest/ (the formatting gate only). #1349 is expected 0 of 2 under
      Blockchain/Dev (the seat: the push fast-skipped the preflight); #1350 4 of 4 (its push ran 12 of 15 legs) — the control in the same run.
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head <n>=<sha> (repeatable): refuse unless that head equals it.
--simulate <name> <n>=<sha>[,<n>=<sha>] (controls): use the given head(s) instead of origin's for those PRs, skip the ls-remote/branch equality
for them, and write pins_gate47.SIM-<name>.json instead (never the real pins).
Usage: pin_gate47.py <scratchpad> [--expect-head n=sha ...] [--simulate name n=sha[,n=sha]]"""
import json, os, subprocess, sys, datetime, itertools
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
CL = os.path.join(SP, 'g47_sp', 'clone'); ORDER = K['order']
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate47 sim', GIT_AUTHOR_EMAIL='sim@gate47.invalid', GIT_COMMITTER_NAME='gate47 sim',
           GIT_COMMITTER_EMAIL='sim@gate47.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
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
print('pin_gate47 %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
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
    print('    #%s move log: %s' % (n, ' ; '.join(git('log', '--format=%h %s', '%s..%s' % (mb, DEV)).splitlines())))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(D) the OVERLAP matrix (every pair)')
allp = [p for n in ORDER for p in S[n]['files']]; union = sorted(set(allp)); pairs = []
for a, b in itertools.combinations(ORDER, 2):
    x = sorted(set(S[a]['files']) & set(S[b]['files']))
    if x: pairs.append((a, b, x)); print('    OVERLAP #%s x #%s: %s' % (a, b, x))
print('    OVERLAP SUMMARY: %d pair(s) checked, %d overlapping | %d path(s) in total, %d distinct'
      % (len(list(itertools.combinations(ORDER, 2))), len(pairs), len(allp), len(union)))
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
        sq = git('commit-tree', t, '-p', tip, '-m', 'gate47 simulated squash of #%s' % n)
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
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone tree / chain step / END')
MODES = []
stepn = {st['pr']: st['tree'] for st in STEPS}
for n in ORDER:
    for p, want in sorted(K['prs'][n].get('mode_pins', {}).items()):
        got = {'head': (tree_entries(H[n], [p])[p] or ('ABSENT',))[0], 'alone': (tree_entries(S[n]['alone_tree'], [p])[p] or ('ABSENT',))[0] if S[n].get('alone_clean') else 'n/a',
               'chain': (tree_entries(stepn[n], [p])[p] or ('ABSENT',))[0] if n in stepn else 'n/a', 'END': (tree_entries(END, [p])[p] or ('ABSENT',))[0] if END else 'n/a'}
        ok = all(v == want for v in got.values())
        MODES.append(dict(pr=n, path=p, want=want, got=got, ok=ok))
        print('    #%s %s: want %s | head %s | alone %s | chain %s | END %s | %s' % (n, p, want, got['head'], got['alone'], got['chain'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
        if not ok: bad.append('(H) #%s %s recorded mode %s != the pin %s' % (n, p, got, want))
nm = [m['want'] for m in MODES]
print('    MODE SUMMARY: %d path(s) pinned, %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (len(MODES), sum(m['ok'] for m in MODES), sorted(set(nm))))
print('(I) THE HOOK AND THE PREFLIGHT, blob+mode per tree (the gate reads the hook AT THE HEAD)')
HOOKS = {}
trees = [('develop', DEV)] + [('#%s head' % n, H[n]) for n in ORDER] + ([('END', END)] if END else [])
for p in K.get('hook_paths', []):
    ents = {lab: tree_entries(t, [p])[p] for lab, t in trees}; same = len(set(ents.values())) == 1
    HOOKS[p] = {lab: list(v) if v else None for lab, v in ents.items()}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, (v[0] + ' ' + v[1][:12]) if v else 'ABSENT') for lab, v in ents.items()), 'IDENTICAL in every tree' if same else 'DIFFERS between trees'))
print('(J) THE HOOK\'S PATH CLASS per PR (a path-prefix reading; the hook\'s own `changed` logic is the gate\'s to drive)')
HCLASS = {}
for n in ORDER:
    fs = S[n]['files']; bd = [f for f in fs if f.startswith('Blockchain/Dev/')]; st = [f for f in fs if f.startswith('systemTest/')]
    HCLASS[n] = {'blockchain_dev': len(bd), 'systemTest': len(st), 'total': len(fs)}
    print('    #%s: %d of %d path(s) under Blockchain/Dev/ | %d under systemTest/ -> %s' % (n, len(bd), len(fs), len(st), 'the preflight TRIGGERS' if bd else 'the preflight FAST-SKIPS (formatting gate only)'))
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': S, 'overlap_pairs': pairs,
     'paths_total': len(allp), 'paths_distinct': len(union), 'union': union, 'end_tree': END, 'reverse_end_tree': REV, 'chain': STEPS,
     'simulate': SIM, 'simulated_heads': SIMH, 'modes': MODES, 'hooks': HOOKS, 'hook_class': HCLASS}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate47.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate47.SIM-%s.json' % SIM if SIM else 'pins_gate47.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | END_TREE %s | %d PRs, %d distinct paths, %d overlapping pair(s)' % (f, DEV[:12], END, len(ORDER), len(union), len(pairs)))
