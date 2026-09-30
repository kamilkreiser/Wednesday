#!/usr/bin/env python3
"""pin_gate48b.py — MEASURE the pins for the gate48b kit (kit.json beside this script) and write pins_gate48b.json. TWO PRs in kit order:
#1354 (T2, KS-470: the GHSA-r53p row made PERMANENT on Kam's ruling + GRANDFATHERED_NO_EXPIRY +1 + js-yaml 5.4.2) THEN #1355 (T1, KS-1378: the
undici override bump). Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/<n>/head INTO THE
SCRATCH CLONE ONLY (<scratchpad>/g48b_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout). Then:
  (A) heads: refs/pull/<n>/head == the branch (WHOLE-FIELD); fetched refs == ls-remote; a head listed in kit.json superseded_heads is PRINTED
      as SUPERSEDED and recorded in the pins (the launcher refuses rc 35 on it; the pin itself does not refuse, so the kit can be drafted).
  (B) shape: merge-base, ahead / behind, head parent (in kit expected_parent_any, or == expected_parent), file list == kit.json files AND numstat.
  (C) the develop MOVE since each merge-base, against that PR's own paths (must be EMPTY).
  (D) the OVERLAP matrix (every pair): the intersection of their path sets, and for each shared path whether the two heads carry the SAME blob.
  (E) each PR ALONE over develop: merge-tree clean; diff(develop, tree) == its own paths; blobs + modes == head's.
  (F) the CHAIN in kit order, each a squash on the previous tip (merge-tree then commit-tree, fixed identity and date, parent = tip): every step
      clean; diff(tip, new tip) == that PR's own paths MINUS its NO-OP paths (a path whose blob+mode at the tip already equals the head's —
      #1355's systemTest/performance lock after #1354, the shared js-yaml blob), each NO-OP printed by name; every own blob + mode == the head's.
  (G) END = the last tip's tree: diff(develop, END) == the union of the own paths; every END blob == its head's. The REVERSE order is chained too
      and must give the same tree (the shared path carries one blob, so order independence is expected — measured, not assumed).
  (H) MODE PINS: the RECORDED mode (`git ls-tree`) of every pinned path at head / alone / chain step / END; kit.json mode_controls names a
      path OUTSIDE the PRs recorded 100755, read at develop / heads / END (all PR paths are 100644: the control shows the instrument discriminates).
  (I) THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE AUDIT LEGS, THE ISSUER DOCKERFILE (kit.json hook_paths): blob+mode per tree.
  (K) UNCHANGED PINS (kit.json unchanged_pins): the issuer Dockerfile's blob at develop == each head == END.
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head <n>=<sha> (repeatable): refuse unless that head equals it.
--simulate <name> <n>=<sha>[,<n>=<sha>] (controls): use the given head(s), skip the ls-remote/branch equality for them, write
pins_gate48b.SIM-<name>.json (never the real pins). --develop <sha> (controls, needs --simulate): judge against that develop.
Usage: pin_gate48b.py <scratchpad> [--expect-head n=sha ...] [--simulate name n=sha[,n=sha]] [--develop sha]"""
import json, os, subprocess, sys, datetime, itertools
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
DEVOVR = A[A.index('--develop') + 1] if '--develop' in A else None
if DEVOVR and not SIM: raise SystemExit('REFUSING: --develop is a controls-only override and needs --simulate <name> (it never writes the real pins)')
CL = os.path.join(SP, 'g48b_sp', 'clone'); ORDER = K['order']
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
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [K['prs'][n]['branch'] for n in ORDER]
R = {l.split('\t')[1]: l.split('\t')[0] for l in git('ls-remote', 'origin', *refs).splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in ORDER])
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
if DEVOVR: DEV = git('rev-parse', DEVOVR + '^{commit}'); print('    develop OVERRIDDEN (controls) -> %s' % DEV)
H = {}; SUPER = {}
for n in ORDER:
    ph, bh = R.get('refs/pull/%s/head' % n), R.get(K['prs'][n]['branch'])
    if n in SIMH:
        H[n] = git('rev-parse', SIMH[n] + '^{commit}'); print('    #%s SIMULATED head %s (origin pull/head %s)' % (n, H[n], ph))
    else:
        H[n] = ph
        print('    #%s pull/head %s | branch %s | %s' % (n, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER'))
        if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (n, n, ph, bh))
        if git('rev-parse', 'refs/remotes/pr/%s' % n) != ph: bad.append('(A) #%s fetched head != ls-remote' % n)
        if n in EXP and ph != EXP[n]: bad.append('(A) #%s head %s != the expected (pinned) head %s' % (n, ph, EXP[n]))
    SUPER[n] = H[n] in (K.get('superseded_heads') or {}).get(n, [])
    if SUPER[n]: print('    #%s head %s is SUPERSEDED (kit.json superseded_heads): the ruled head has NOT landed — the launcher refuses rc 35 on this pin' % (n, H[n]))
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None
S = {}
print('(B) shape per PR')
for n in ORDER:
    h = H[n]; k = K['prs'][n]; mb = git('merge-base', DEV, h); par = git('rev-parse', h + '^')
    ahead = int(git('rev-list', '--count', '%s..%s' % (mb, h))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
    names = git('diff', '--name-only', mb, h).splitlines(); ns = git('diff', '--numstat', mb, h).splitlines()
    S[n] = dict(head=h, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, head_tree=git('rev-parse', h + '^{tree}'),
                subject_commit=git('log', '-1', '--format=%s', h), superseded=SUPER[n], blobs={p: list(ent(h, p)) if ent(h, p) else None for p in names})
    print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files: %s' % (n, h, par[:12], mb[:12], ahead, behind, len(names), ' '.join(names)))
    print('    #%s numstat: %s' % (n, ' ; '.join(x.replace('\t', ' ') for x in ns)))
    if n not in SIMH:
        okp = k.get('expected_parent_any') or [k.get('expected_parent')]
        if par not in okp: bad.append('(B) #%s parent %s is not one of kit expected parents %s' % (n, par, okp))
        if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list %s != kit.json files %s' % (n, names, k['files']))
print('(C) the develop MOVE since each merge-base, against that PR\'s own paths')
for n in ORDER:
    mb = S[n]['merge_base']
    if mb == DEV: print('    #%s merge-base == develop: no move' % n); S[n]['move'] = []; continue
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(S[n]['files'])); S[n]['move'] = mv
    print('    #%s move %s..%s: %d path(s) | reaches its own paths: %s' % (n, mb[:12], DEV[:12], len(mv), hit or 'NONE'))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(D) the OVERLAP matrix (every pair) and whether each shared path carries the SAME blob')
allp = [p for n in ORDER for p in S[n]['files']]; union = sorted(set(allp)); pairs = []
for a, b in itertools.combinations(ORDER, 2):
    x = sorted(set(S[a]['files']) & set(S[b]['files']))
    for p in x:
        same = ent(H[a], p) == ent(H[b], p); pairs.append(dict(a=a, b=b, path=p, same_blob=same))
        print('    OVERLAP #%s x #%s: %s | #%s %s | #%s %s | SAME blob+mode: %s' % (a, b, p, a, (ent(H[a], p) or ('', 'ABSENT'))[1][:12], b, (ent(H[b], p) or ('', 'ABSENT'))[1][:12], same))
print('    OVERLAP SUMMARY: %d pair(s) checked, %d shared path(s) (%d with the SAME blob) | %d path(s) in total, %d distinct' % (
    len(list(itertools.combinations(ORDER, 2))), len(pairs), sum(p['same_blob'] for p in pairs), len(allp), len(union)))
print('(E) each PR ALONE over develop %s' % DEV[:12])
for n in ORDER:
    mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H[n]], capture_output=True, text=True, env=ENV)
    t = mt.stdout.split('\n')[0].strip(); d = git('diff', '--name-only', DEV, t).splitlines() if mt.returncode == 0 else []
    eq = mt.returncode == 0 and all(ent(t, p) == ent(H[n], p) for p in S[n]['files'])
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
        noop = sorted(p for p in S[n]['files'] if ent(tip, p) == ent(H[n], p))
        sq = git('commit-tree', t, '-p', tip, '-m', 'gate48b simulated squash of #%s' % n)
        d = git('diff', '--name-only', tip, sq).splitlines(); eq = all(ent(t, p) == ent(H[n], p) for p in S[n]['files'])
        want = sorted(set(S[n]['files']) - set(noop))
        steps.append(dict(pr=n, tree=t, squash_sim=sq, paths=d, noop=noop, own_equal=sorted(d) == want, blobs_equal=eq))
        print('    %s step #%s on %s: clean | tree %s | squash %s | diff(tip, new) %d path(s) == own paths minus NO-OP: %s | NO-OP (already at the tip): %s | blobs+modes == head: %s' % (
            label, n, tip[:12], t, sq[:12], len(d), sorted(d) == want, noop or 'none', eq))
        if sorted(d) != want or not eq: return None, steps, 'step #%s diff / blob mismatch' % n
        tip = sq
    return git('rev-parse', tip + '^{tree}'), steps, None
print('(F) the CHAIN in kit order %s (each a squash on the previous tip)' % ' -> '.join('#' + n for n in ORDER))
END, STEPS, err = chain(ORDER, 'ORDER')
if err: bad.append('(F) chain: ' + err)
print('(G) END')
REV = None
if END:
    d = git('diff', '--name-only', DEV, END).splitlines()
    ok = sorted(d) == union and all(ent(END, p) == ent(H[n], p) for n in ORDER for p in S[n]['files'])
    print('    END_TREE %s | diff(develop, END): %d path(s) == the union of the own paths (%d): %s | every END blob+mode == its head\'s: %s' % (END, len(d), len(union), sorted(d) == union, ok))
    if not ok: bad.append('(G) END diff / blobs disagree with the union of the heads')
    REV, _, rerr = chain(list(reversed(ORDER)), 'REVERSE')
    print('    REVERSE-order END %s | == END_TREE: %s' % (REV, REV == END))
    if REV != END: bad.append('(G) the reverse-order END %s != END_TREE %s (%s)' % (REV, END, rerr))
    print('    git diff --shortstat develop END: %s' % git('diff', '--shortstat', DEV, END))
else: bad.append('(F) no END: the chain could not be simulated')
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / alone / chain step / END, and the control path at develop / heads / END')
MODES = []; stepn = {st['pr']: st['tree'] for st in STEPS}
g = lambda t, p: (ent(t, p) or ('ABSENT',))[0]
for n in ORDER:
    for p, want in sorted(K['prs'][n].get('mode_pins', {}).items()):
        got = {'head': g(H[n], p), 'alone': g(S[n]['alone_tree'], p) if S[n].get('alone_clean') else 'n/a', 'chain': g(stepn[n], p) if n in stepn else 'n/a', 'END': g(END, p) if END else 'n/a'}
        ok = all(v == want for v in got.values()); MODES.append(dict(pr=n, path=p, want=want, got=got, ok=ok, control=False))
        print('    #%s %s: want %s | head %s | alone %s | chain %s | END %s | %s' % (n, p, want, got['head'], got['alone'], got['chain'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
        if not ok: bad.append('(H) #%s %s recorded mode %s != the pin %s' % (n, p, got, want))
for p, want in sorted(K.get('mode_controls', {}).items()):
    got = dict([('develop', g(DEV, p))] + [('#%s' % n, g(H[n], p)) for n in ORDER] + ([('END', g(END, p))] if END else []))
    ok = all(v == want for v in got.values()); MODES.append(dict(pr='control', path=p, want=want, got=got, ok=ok, control=True))
    print('    CONTROL (not a PR path) %s: want %s | %s | %s' % (p, want, ' | '.join('%s %s' % x for x in got.items()), 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) control path %s recorded mode %s != %s' % (p, got, want))
print('    MODE SUMMARY: %d path(s) pinned (%d PR, %d control), %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (
    len(MODES), sum(not m['control'] for m in MODES), sum(m['control'] for m in MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
print('(I) THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE AUDIT LEGS, THE ISSUER DOCKERFILE — blob+mode per tree')
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
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': S, 'overlap_pairs': pairs,
     'paths_total': len(allp), 'paths_distinct': len(union), 'union': union, 'end_tree': END, 'reverse_end_tree': REV, 'chain': STEPS,
     'squash_sim': STEPS[-1]['squash_sim'] if END else None, 'simulate': SIM, 'simulated_heads': SIMH, 'develop_override': DEVOVR,
     'superseded': SUPER, 'modes': MODES, 'hooks': HOOKS, 'unchanged': UNCH}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate48b.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate48b.SIM-%s.json' % SIM if SIM else 'pins_gate48b.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | END_TREE %s | %d PRs, %d distinct paths | SUPERSEDED heads pinned: %s' % (f, DEV[:12], END, len(ORDER), len(union), [n for n in ORDER if SUPER[n]] or 'none'))
