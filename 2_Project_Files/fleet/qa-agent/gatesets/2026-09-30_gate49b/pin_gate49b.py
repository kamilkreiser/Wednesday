#!/usr/bin/env python3
"""pin_gate49b.py — MEASURE the pins for the gate49b kit (kit.json beside this script) and write pins_gate49b.json. THREE PRs from TWO seats in
kit order: #1357 (Seat B 49th, T1, KS-1054 ITEM 1a), #1359 (Seat B 49th, T1, KS-1054 ITEM 1c), THEN #1358 (Seat D 1st, T2, KS-1380). Shape copied
from gate48b's multi-PR pin. Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/<n>/head INTO THE
SCRATCH CLONE ONLY (<scratchpad>/g49b_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout). Then:
  (A) heads: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched refs == ls-remote; == kit.json's head (or --expect-head); SUPERSEDED heads
      (kit.json superseded_heads) are printed and recorded (the launcher refuses rc 35), never refused here.
  (B) shape: merge-base, ahead / behind, head parent in kit expected_parent_any, file list == kit.json files AND numstat.
  (C) the develop MOVE since each merge-base, against that PR's own paths (must be EMPTY).
  (D) DISJOINTNESS (every pair): the intersection of their path sets MUST be EMPTY — this batch is sold as disjoint, so a shared path REFUSES.
      Printed with a count per pair and a CONTROL: the same intersection taken against the PR's OWN path set is non-empty (the instrument fires).
  (E) each PR ALONE over develop: merge-tree clean; diff(develop, tree) == its own paths; blobs + modes == head's.
  (F) the CHAIN in kit order, each a squash on the previous tip (merge-tree then commit-tree, fixed identity and date, parent = tip).
  (G) END = the last tip's tree: diff(develop, END) == the union; every END blob == its head's. The REVERSE order must give the same tree.
  (G2) EVERY permutation of the PRs chained: all must give END_TREE (disjoint paths => order independence — measured, not assumed). Also the
      PER-SEAT subsets (Seat B 49th's alone, Seat D 1st's alone) are chained and their trees recorded (a GO for one seat only lands that tree).
  (H) MODE PINS: kit prs.<n>.mode_pins at head / alone / chain step / END; (H2) every path of a PR with NO mode_pins (#1358's 15 locks) is 100644
      at head and END; kit.json mode_controls (one 100755 + one 100644 path outside the PRs) at develop / heads / END.
  (I) HOOK PATHS (kit.json hook_paths): blob+mode per tree.   (K) UNCHANGED PINS: blob at develop == each head == END.
  (L) CLAIMED BLOBS (kit prs.<n>.claimed_blobs, 12-hex prefixes from the READY): the head's blob starts with each.
  (M) GOLDENS (kit prs.<n>.goldens): each golden.diff (sha256 prefix checked) applied with `git apply --cached` under a TEMP index to the golden
      base AND to develop; every path it names must equal the head's blob BYTE FOR BYTE (the recorded mode is (H)'s job). CONTROL: the head blob
      compared with the develop blob of the same path must DIFFER (the comparison can fail).
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head <n>=<sha> (repeatable).
--simulate <name> <n>=<sha>[,<n>=<sha>] (controls): use the given head(s), skip the ls-remote/branch/kit equality for them, write
pins_gate49b.SIM-<name>.json (never the real pins). --develop <sha> (controls, needs --simulate): judge against that develop.
Usage: pin_gate49b.py <scratchpad> [--expect-head n=sha ...] [--simulate name n=sha[,n=sha]] [--develop sha]"""
import json, os, subprocess, sys, datetime, itertools, hashlib, tempfile
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
CL = os.path.join(SP, 'g49b_sp', 'clone'); ORDER = K['order']
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate49b sim', GIT_AUTHOR_EMAIL='sim@gate49b.invalid', GIT_COMMITTER_NAME='gate49b sim',
           GIT_COMMITTER_EMAIL='sim@gate49b.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
def git(*a, check=True, env=None, inp=None):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=env or ENV, input=inp)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:200], r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if not os.path.isdir(CL):
    src = K['base_clone'] if os.path.isdir(K['base_clone']) else K['checkout']
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', src, CL], check=True)
    subprocess.run(['git', '-C', CL, 'remote', 'set-url', 'origin', 'git@github.com:Secuura/Distributed_Secuura.git'], check=True)
    print('built scratch clone %s (--shared from %s)' % (CL, src))
bad = []
print('pin_gate49b %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [K['prs'][n]['branch'] for n in ORDER]
R = {l.split('\t')[1]: l.split('\t')[0] for l in git('ls-remote', 'origin', *refs).splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in ORDER if R.get('refs/pull/%s/head' % n)])
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
if DEVOVR: DEV = git('rev-parse', DEVOVR + '^{commit}'); print('    develop OVERRIDDEN (controls) -> %s' % DEV)
H = {}; SUPER = {}
for n in ORDER:
    ph, bh = R.get('refs/pull/%s/head' % n), R.get(K['prs'][n]['branch'])
    if n in SIMH:
        H[n] = git('rev-parse', SIMH[n] + '^{commit}'); print('    #%s SIMULATED head %s (origin pull/head %s)' % (n, H[n], ph))
    else:
        H[n] = ph
        print('    #%s pull/head %s | branch %s | %s | kit head %s' % (n, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER', K['prs'][n]['head'][:12]))
        if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (n, n, ph, bh))
        elif git('rev-parse', 'refs/remotes/pr/%s' % n) != ph: bad.append('(A) #%s fetched head != ls-remote' % n)
        if ph != K['prs'][n]['head']: bad.append('(A) #%s origin head %s != kit.json head %s (a new head is a re-pin: README section 8)' % (n, ph, K['prs'][n]['head']))
        if n in EXP and ph != EXP[n]: bad.append('(A) #%s head %s != the expected head %s' % (n, ph, EXP[n]))
    SUPER[n] = H[n] in (K.get('superseded_heads') or {}).get(n, [])
    if SUPER[n]: print('    #%s head %s is SUPERSEDED (kit.json superseded_heads): the launcher refuses rc 35 on this pin' % (n, H[n]))
if bad and any(not H.get(n) for n in ORDER):
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]; raise SystemExit(1)
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None
S = {}
print('(B) shape per PR')
for n in ORDER:
    h = H[n]; k = K['prs'][n]; mb = git('merge-base', DEV, h); par = git('rev-parse', h + '^')
    ahead = int(git('rev-list', '--count', '%s..%s' % (mb, h))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
    names = git('diff', '--name-only', mb, h).splitlines(); ns = git('diff', '--numstat', mb, h).splitlines()
    adds = sum(int(x.split('\t')[0]) for x in ns); dels = sum(int(x.split('\t')[1]) for x in ns)
    S[n] = dict(head=h, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, adds=adds, dels=dels, head_tree=git('rev-parse', h + '^{tree}'),
                subject_commit=git('log', '-1', '--format=%s', h), superseded=SUPER[n], seat=k['seat'], blobs={p: list(ent(h, p)) if ent(h, p) else None for p in names})
    print('    #%s (%s, %s) head %s | parent %s | merge-base %s | ahead %d behind %d | %d files +%d/-%d (claimed %s) | subject %d chars' % (
        n, k['seat'], k['tier'], h, par[:12], mb[:12], ahead, behind, len(names), adds, dels, k.get('claimed', {}).get('numstat'), len(S[n]['subject_commit'])))
    print('    #%s numstat: %s' % (n, ' ; '.join(x.replace('\t', ' ') for x in ns)))
    if n not in SIMH:
        if par not in k['expected_parent_any']: bad.append('(B) #%s parent %s is not one of kit expected parents %s' % (n, par, k['expected_parent_any']))
        if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list %s != kit.json files %s' % (n, names, k['files']))
print('(C) the develop MOVE since each merge-base, against that PR\'s own paths')
for n in ORDER:
    mb = S[n]['merge_base']
    if mb == DEV: print('    #%s merge-base == develop: no move' % n); S[n]['move'] = []; continue
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(S[n]['files'])); S[n]['move'] = mv
    print('    #%s move %s..%s: %d path(s) | reaches its own paths: %s' % (n, mb[:12], DEV[:12], len(mv), hit or 'NONE'))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(D) DISJOINTNESS — every pair\'s shared paths (must be EMPTY), with the self-intersection as the control that the instrument fires')
allp = [p for n in ORDER for p in S[n]['files']]; union = sorted(set(allp)); pairs = []
for a, b in itertools.combinations(ORDER, 2):
    x = sorted(set(S[a]['files']) & set(S[b]['files'])); pairs.append(dict(a=a, b=b, shared=x))
    print('    PAIR #%s x #%s: %d shared path(s)%s' % (a, b, len(x), (': ' + ' '.join(x)) if x else ''))
    if x: bad.append('(D) #%s and #%s share %s — the batch is not disjoint; a re-draft decides the order' % (a, b, x))
    dirs = sorted(set(os.path.dirname(p) for p in S[a]['files']) & set(os.path.dirname(p) for p in S[b]['files']))
    if dirs: print('    PAIR #%s x #%s: same DIRECTORY (not a shared path; reported): %s' % (a, b, dirs))
for n in ORDER: print('    CONTROL #%s x itself: %d shared path(s) (== its %d files: the intersection fires)' % (n, len(set(S[n]['files']) & set(S[n]['files'])), len(S[n]['files'])))
print('    DISJOINT SUMMARY: %d pair(s), %d shared path(s) | %d paths in total, %d distinct' % (len(pairs), sum(len(p['shared']) for p in pairs), len(allp), len(union)))
if len(allp) != len(union): bad.append('(D) %d paths but %d distinct' % (len(allp), len(union)))
print('(E) each PR ALONE over develop %s' % DEV[:12])
for n in ORDER:
    mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H[n]], capture_output=True, text=True, env=ENV)
    t = mt.stdout.split('\n')[0].strip(); d = git('diff', '--name-only', DEV, t).splitlines() if mt.returncode == 0 else []
    eq = mt.returncode == 0 and all(ent(t, p) == ent(H[n], p) for p in S[n]['files'])
    S[n]['alone_tree'] = t; S[n]['alone_clean'] = mt.returncode == 0
    print('    #%s alone: merge-tree rc %d tree %s | diff(develop, tree) == own paths: %s | blobs+modes == head: %s' % (n, mt.returncode, t, sorted(d) == sorted(S[n]['files']), eq))
    if mt.returncode or sorted(d) != sorted(S[n]['files']) or not eq: bad.append('(E) #%s does not merge ALONE cleanly onto develop' % n)
def chain(order, label, quiet=False):
    tip = DEV; steps = []
    for n in order:
        mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', tip, H[n]], capture_output=True, text=True, env=ENV)
        t = mt.stdout.split('\n')[0].strip()
        if mt.returncode:
            print('    %s step #%s: merge-tree rc %d — CONFLICT: %s' % (label, n, mt.returncode, ' '.join(mt.stdout.split('\n')[1:6])[:240]))
            return None, steps, 'step #%s NOT clean (rc %d)' % (n, mt.returncode)
        noop = sorted(p for p in S[n]['files'] if ent(tip, p) == ent(H[n], p))
        sq = git('commit-tree', t, '-p', tip, '-m', 'gate49b simulated squash of #%s' % n)
        d = git('diff', '--name-only', tip, sq).splitlines(); eq = all(ent(t, p) == ent(H[n], p) for p in S[n]['files'])
        want = sorted(set(S[n]['files']) - set(noop))
        steps.append(dict(pr=n, tree=t, squash_sim=sq, paths=d, noop=noop, own_equal=sorted(d) == want, blobs_equal=eq))
        if not quiet:
            print('    %s step #%s on %s: clean | tree %s | squash %s | diff(tip, new) %d path(s) == own paths minus NO-OP: %s | NO-OP: %s | blobs+modes == head: %s' % (
                label, n, tip[:12], t, sq[:12], len(d), sorted(d) == want, noop or 'none', eq))
        if sorted(d) != want or not eq: return None, steps, 'step #%s diff / blob mismatch' % n
        tip = sq
    return git('rev-parse', tip + '^{tree}'), steps, None
print('(F) the CHAIN in kit order %s (each a squash on the previous tip)' % ' -> '.join('#' + n for n in ORDER))
END, STEPS, err = chain(ORDER, 'ORDER')
if err: bad.append('(F) chain: ' + err)
print('(G) END')
REV = None; PERMS = {}; SUBSETS = {}
if END:
    d = git('diff', '--name-only', DEV, END).splitlines()
    ok = sorted(d) == union and all(ent(END, p) == ent(H[n], p) for n in ORDER for p in S[n]['files'])
    print('    END_TREE %s | diff(develop, END): %d path(s) == the union of the own paths (%d): %s | every END blob+mode == its head\'s: %s' % (END, len(d), len(union), sorted(d) == union, ok))
    if not ok: bad.append('(G) END diff / blobs disagree with the union of the heads')
    REV, _, rerr = chain(list(reversed(ORDER)), 'REVERSE')
    print('    REVERSE-order END %s | == END_TREE: %s' % (REV, REV == END))
    if REV != END: bad.append('(G) the reverse-order END %s != END_TREE %s (%s)' % (REV, END, rerr))
    print('(G2) EVERY permutation, and the per-seat subsets')
    for perm in itertools.permutations(ORDER):
        t, _, e = chain(list(perm), 'PERM', quiet=True); PERMS[' '.join(perm)] = t
        print('    PERM %s -> %s | == END_TREE: %s%s' % (' -> '.join('#' + x for x in perm), t, t == END, (' (%s)' % e) if e else ''))
        if t != END: bad.append('(G2) permutation %s gives %s != END_TREE' % (perm, t))
    for seat, v in K['authors'].items():   # the AUTHOR subsets (one merger merges all three; a subset is what one author's PRs alone land)
        sub = [n for n in ORDER if n in v['prs']]; t, _, e = chain(sub, 'SUBSET', quiet=True); SUBSETS[seat] = {'prs': sub, 'tree': t}
        dd = git('diff', '--name-only', DEV, t).splitlines() if t else []
        own = sorted(p for n in sub for p in S[n]['files'])
        print('    SUBSET %s only (%s) -> tree %s | diff(develop, tree) == its own %d path(s): %s' % (seat, ' '.join('#' + x for x in sub), t, len(own), sorted(dd) == own))
        if not t or sorted(dd) != own: bad.append('(G2) the %s subset does not land exactly its own paths' % seat)
    print('    git diff --shortstat develop END: %s' % git('diff', '--shortstat', DEV, END))
else: bad.append('(F) no END: the chain could not be simulated')
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone / chain step / END, the #1358 all-100644 rule, and the controls')
MODES = []; stepn = {st['pr']: st['tree'] for st in STEPS}
g = lambda t, p: (ent(t, p) or ('ABSENT',))[0]
for n in ORDER:
    mp = K['prs'][n].get('mode_pins') or {}
    items = sorted(mp.items()) if mp else [(p, '100644') for p in sorted(S[n]['files'])]
    for p, want in items:
        got = {'head': g(H[n], p), 'alone': g(S[n]['alone_tree'], p) if S[n].get('alone_clean') else 'n/a', 'chain': g(stepn[n], p) if n in stepn else 'n/a', 'END': g(END, p) if END else 'n/a'}
        ok = all(v == want for v in got.values()); MODES.append(dict(pr=n, path=p, want=want, got=got, ok=ok, control=False, rule='pin' if mp else 'H2 all-100644'))
        print('    #%s %s: want %s (%s) | head %s | alone %s | chain %s | END %s | %s' % (n, p, want, 'pin' if mp else 'H2', got['head'], got['alone'], got['chain'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
        if not ok: bad.append('(H) #%s %s recorded mode %s != %s' % (n, p, got, want))
for p, want in sorted(K.get('mode_controls', {}).items()):
    got = dict([('develop', g(DEV, p))] + [('#%s' % n, g(H[n], p)) for n in ORDER] + ([('END', g(END, p))] if END else []))
    ok = all(v == want for v in got.values()); MODES.append(dict(pr='control', path=p, want=want, got=got, ok=ok, control=True))
    print('    CONTROL (not a PR path) %s: want %s | %s | %s' % (p, want, ' | '.join('%s %s' % x for x in got.items()), 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) control path %s recorded mode %s != %s' % (p, got, want))
print('    MODE SUMMARY: %d path(s) pinned (%d PR, %d control), %d OK | modes pinned: %s' % (
    len(MODES), sum(not m['control'] for m in MODES), sum(m['control'] for m in MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
print('(I) HOOK PATHS — blob+mode per tree')
HOOKS = {}; trees = [('develop', DEV)] + [('#%s head' % n, H[n]) for n in ORDER] + ([('END', END)] if END else [])
for p in K.get('hook_paths', []):
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1
    HOOKS[p] = {lab: list(v) if v else None for lab, v in es.items()}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, (v[0] + ' ' + v[1][:12]) if v else 'ABSENT') for lab, v in es.items()), 'IDENTICAL in every tree' if same else 'DIFFERS between trees'))
print('(K) UNCHANGED PINS (blob at develop == each head == END)')
UNCH = {}
for p, why in K.get('unchanged_pins', {}).items():
    es = {lab: ent(tr, p) for lab, tr in trees}; same = len(set(es.values())) == 1 and None not in es.values()
    UNCH[p] = {'same': same, 'blobs': {lab: list(v) if v else None for lab, v in es.items()}}
    print('    %s: %s | %s' % (p, ' | '.join('%s %s' % (lab, v[1][:12] if v else 'ABSENT') for lab, v in es.items()), 'BYTE-EQUAL in every tree' if same else 'CHANGED'))
    if not same: bad.append('(K) %s is not byte-equal in every tree (%s)' % (p, why))
print('(L) CLAIMED BLOBS (the READY\'s 12-hex prefixes)')
for n in ORDER:
    for p, pre in sorted((K['prs'][n].get('claimed_blobs') or {}).items()):
        b = (ent(H[n], p) or ('', ''))[1]; ok = b.startswith(pre)
        print('    #%s %s: head blob %s | claimed %s | %s' % (n, p, b[:12], pre, 'MATCH' if ok else 'DIFFERS'))
        if not ok: bad.append('(L) #%s %s blob %s != claimed %s' % (n, p, b[:12], pre))
print('(M) GOLDENS — each golden.diff applied under a TEMP index to its base AND to develop; every named path == the head blob')
GOLD = {}
for n in ORDER:
    gd = K['prs'][n].get('goldens')
    if not gd: continue
    for f, paths in sorted(gd['diffs'].items()):
        raw = open(f, 'rb').read(); sha = hashlib.sha256(raw).hexdigest(); pre = gd['sha256_prefix'][f]
        print('    #%s golden %s: sha256 %s | recorded prefix %s | %s' % (n, f, sha[:12], pre, 'MATCH' if sha.startswith(pre) else 'DIFFERS'))
        if not sha.startswith(pre): bad.append('(M) golden %s sha256 %s != recorded %s' % (f, sha[:12], pre))
        for lab, base in (('golden base', gd['golden_base']), ('develop', DEV)):
            idx = tempfile.mktemp(prefix='g49b_idx_', dir=os.path.join(SP, 'g49b_sp')); e2 = dict(ENV, GIT_INDEX_FILE=idx)
            git('read-tree', base, env=e2)
            r = subprocess.run(['git', '-C', CL, 'apply', '--cached', f], capture_output=True, text=True, env=e2)
            if r.returncode: print('    #%s golden %s on %s %s: git apply --cached rc %d %s' % (n, os.path.basename(os.path.dirname(f)), lab, base[:12], r.returncode, r.stderr.strip()[:160])); bad.append('(M) golden %s does not apply to %s' % (f, lab)); continue
            t = git('write-tree', env=e2)
            for p in paths:
                gb = (ent(t, p) or ('', ''))[1]; hb = (ent(H[n], p) or ('', ''))[1]; db = (ent(DEV, p) or ('', 'ABSENT'))[1]
                ok = gb == hb and hb != ''; GOLD['%s|%s|%s' % (n, lab, p)] = dict(golden_blob=gb, head_blob=hb, ok=ok)
                print('    #%s golden %s on %s %s: %s golden-applied blob %s | head blob %s | %s | CONTROL develop blob %s %s' % (
                    n, os.path.basename(os.path.dirname(f)), lab, base[:12], p, gb[:12], hb[:12], 'BYTE-EQUAL' if ok else 'DIFFERS', db[:12], 'differs from head (the compare can fail)' if db != hb else 'SAME AS HEAD (control did not fire)'))
                if not ok: bad.append('(M) #%s %s: golden (%s) blob %s != head blob %s' % (n, p, lab, gb[:12], hb[:12]))
                if db == hb: bad.append('(M) #%s %s: the develop control equals the head (cannot discriminate)' % (n, p))
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': S, 'disjoint_pairs': pairs,
     'paths_total': len(allp), 'paths_distinct': len(union), 'union': union, 'end_tree': END, 'reverse_end_tree': REV, 'permutations': PERMS, 'subsets': SUBSETS,
     'chain': STEPS, 'squash_sim': STEPS[-1]['squash_sim'] if END else None, 'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR,
     'superseded': SUPER, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH, 'goldens': GOLD}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate49b.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate49b.SIM-%s.json' % SIM if SIM else 'pins_gate49b.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | END_TREE %s | %d PRs, %d distinct paths, 0 shared | %d permutations agree | SUPERSEDED heads pinned: %s' % (
    f, DEV[:12], END, len(ORDER), len(union), len(PERMS), [n for n in ORDER if SUPER[n]] or 'none'))
