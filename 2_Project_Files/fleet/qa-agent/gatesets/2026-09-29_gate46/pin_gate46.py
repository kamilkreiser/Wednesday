#!/usr/bin/env python3
"""pin_gate46.py — MEASURE the pins for the gate46 kit (kit.json beside this script) and write pins_gate46.json. ONE PR (#1348 round 2, T1).
Reads origin by `git ls-remote` (Secuura deploy key, in a scratch clone), fetches develop + refs/pull/1348/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g46_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or the checkout, when absent). Then:
  (A) heads: refs/pull/1348/head == the branch (WHOLE-FIELD); fetched refs == ls-remote.
  (B) shape: merge-base, ahead / behind, head parent (== kit expected_parent = round 1), file list == kit.json files (the PULLS API's) AND numstat.
  (R) ROUND-2 DELTA: diff(round 1, head) names == kit round2_files (the test file ONLY); every other own path (deploy.sh) is BYTE-EQUAL between round 1
      and the head — the product gate45 measured correct is the product under test now.
  (C) the develop MOVE since the merge-base: the moved paths, and their intersection with the PR's own paths (must be EMPTY — a move that reaches
      the PR's cells refuses).
  (E) the PR over develop: `git merge-tree --write-tree develop head` clean; then a simulated squash (commit-tree, fixed identity and date, parent =
      develop); diff(develop, squash) == its own paths; every blob + mode == the head's. END_TREE = that squash's tree.
  (H) MODE PINS (kit.json mode_pins; core.filemode is false in the Secuura repo, so a disk bit proves nothing): the RECORDED mode by `git ls-tree`
      of every pinned path == the pin at the HEAD, at ROUND 1 and at END. Both directions are pinned (deploy.sh 100755, the test 100644), so the
      instrument is shown to discriminate.
Refuses rc 1 on any disagreement; writes pins only on PASS. --expect-head 1348=<sha>: refuse unless the head equals it.
--simulate <name> 1348=<sha> (controls): use the given head instead of origin's, skip the ls-remote/branch equality and the parent/file-list checks
for it, and write pins_gate46.SIM-<name>.json instead (never the real pins).
Usage: pin_gate46.py <scratchpad> [--expect-head 1348=sha] [--simulate name 1348=sha]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
EXP = dict(a.split('=', 1) for i, a in enumerate(A) if i and A[i - 1] == '--expect-head')
SIM = None; SIMH = {}
if '--simulate' in A:
    i = A.index('--simulate'); SIM = A[i + 1]; SIMH = dict(x.split('=', 1) for x in A[i + 2].split(',') if x)
CL = os.path.join(SP, 'g46_sp', 'clone'); ORDER = K['order']; n = ORDER[0]; k = K['prs'][n]
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate46 sim', GIT_AUTHOR_EMAIL='sim@gate46.invalid', GIT_COMMITTER_NAME='gate46 sim',
           GIT_COMMITTER_EMAIL='sim@gate46.invalid', GIT_AUTHOR_DATE='2026-09-29T00:00:00Z', GIT_COMMITTER_DATE='2026-09-29T00:00:00Z')
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
print('pin_gate46 %s%s | clone %s' % (now(), ' SIMULATE ' + SIM + ' ' + str(SIMH) if SIM else '', CL))
refs = ['refs/heads/develop', 'refs/pull/%s/head' % n, k['branch']]
ls = git('ls-remote', 'origin', *refs)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines()}
DEV = R.get('refs/heads/develop')
print('(A) ls-remote at %s: develop %s' % (now(), DEV))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', '+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n))
if git('rev-parse', 'refs/remotes/origin/develop') != DEV: bad.append('(A) fetched develop != ls-remote develop')
ph, bh = R.get('refs/pull/%s/head' % n), R.get(k['branch'])
if n in SIMH:
    H = git('rev-parse', SIMH[n] + '^{commit}'); print('    #%s SIMULATED head %s (origin pull/head %s)' % (n, H, ph))
else:
    H = ph
    print('    #%s pull/head %s | branch %s | %s' % (n, ph, bh, 'EQUAL' if ph and ph == bh else 'DIFFER'))
    if not (ph and ph == bh): bad.append('(A) #%s head at refs/pull/%s/head (%s) != at the branch (%s)' % (n, n, ph, bh))
    if git('rev-parse', 'refs/remotes/pr/%s' % n) != ph: bad.append('(A) #%s fetched head != ls-remote' % n)
    if n in EXP and ph != EXP[n]: bad.append('(A) #%s head %s != the expected (pinned) head %s' % (n, ph, EXP[n]))
def ent(t, p):
    l = git('ls-tree', t, '--', p)
    return tuple(l.split()[0:3:2]) if l else None   # (mode, blob) or None when absent
print('(B) shape')
mb = git('merge-base', DEV, H); par = git('rev-parse', H + '^')
ahead = int(git('rev-list', '--count', '%s..%s' % (mb, H))); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)))
names = git('diff', '--name-only', mb, H).splitlines(); ns = git('diff', '--numstat', mb, H).splitlines()
S = dict(head=H, merge_base=mb, parent=par, ahead=ahead, behind=behind, files=names, numstat=ns, head_tree=git('rev-parse', H + '^{tree}'),
         subject_commit=git('log', '-1', '--format=%s', H), blobs={p: list(ent(H, p)) if ent(H, p) else None for p in names})
print('    #%s head %s | parent %s | merge-base %s | ahead %d behind %d | %d files: %s' % (n, H, par[:12], mb[:12], ahead, behind, len(names), ' '.join(names)))
for l in ns: print('      numstat %s' % l)
if n not in SIMH:
    if par != k['expected_parent']: bad.append('(B) #%s parent %s != kit expected_parent (round 1) %s' % (n, par, k['expected_parent']))
    if sorted(names) != sorted(k['files']): bad.append('(B) #%s git file list %s != the PULLS API list (kit.json) %s' % (n, names, k['files']))
print('(R) ROUND-2 DELTA: round 1 %s -> head %s' % (k['round1_head'][:12], H[:12]))
r2 = git('diff', '--name-only', k['round1_head'], H).splitlines()
print('    diff(round 1, head) names: %s | == kit round2_files %s: %s' % (r2, k['round2_files'], sorted(r2) == sorted(k['round2_files'])))
print('    diff(round 1, head) --numstat: %s' % ' ; '.join(git('diff', '--numstat', k['round1_head'], H).splitlines()))
if sorted(r2) != sorted(k['round2_files']): bad.append('(R) the round-2 delta %s != the declared %s (a product file moved since gate45 measured it)' % (r2, k['round2_files']))
unch = {}
for p in k['files']:
    if p in k['round2_files']: continue
    a, b = ent(k['round1_head'], p), ent(H, p); unch[p] = a == b
    print('    %s round 1 %s | head %s | BYTE-EQUAL (blob+mode): %s' % (p, a, b, a == b))
    if a != b: bad.append('(R) %s changed between round 1 and the head' % p)
S['round2_delta'] = r2; S['unchanged_since_round1'] = unch
print('(C) the develop MOVE since the merge-base, against the PR\'s own paths')
if mb == DEV: print('    merge-base == develop: no move'); S['move'] = []
else:
    mv = git('diff', '--name-only', mb, DEV).splitlines(); hit = sorted(set(mv) & set(names)); S['move'] = mv
    print('    move %s..%s: %d path(s) %s | reaches its own paths: %s' % (mb[:12], DEV[:12], len(mv), mv, hit or 'NONE'))
    print('    move log: %s' % ' ; '.join(git('log', '--format=%h %s', '%s..%s' % (mb, DEV)).splitlines()))
    if hit: bad.append('(C) #%s: the develop move touches its own path(s) %s — a rebase / re-draft decides' % (n, hit))
print('(E) #%s squashed over develop %s' % (n, DEV[:12]))
mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, H], capture_output=True, text=True, env=ENV)
t = mt.stdout.split('\n')[0].strip(); END = None; SQ = None
if mt.returncode:
    print('    merge-tree rc %d — CONFLICT: %s' % (mt.returncode, ' '.join(mt.stdout.split('\n')[1:6])[:240])); bad.append('(E) #%s NOT clean over develop (rc %d)' % (n, mt.returncode))
else:
    SQ = git('commit-tree', t, '-p', DEV, '-m', 'gate46 simulated squash of #%s' % n)
    d = git('diff', '--name-only', DEV, SQ).splitlines(); eq = all(ent(t, p) == ent(H, p) for p in names)
    END = git('rev-parse', SQ + '^{tree}')
    print('    merge-tree rc 0 | tree %s | diff(develop, squash) == own paths: %s | every blob+mode == head: %s' % (t, sorted(d) == sorted(names), eq))
    print('    END_TREE %s | git diff --shortstat develop END: %s' % (END, git('diff', '--shortstat', DEV, SQ)))
    if sorted(d) != sorted(names) or not eq: bad.append('(E) diff / blob mismatch after the simulated squash'); END = None
print('(H) MODE PINS — the RECORDED mode (git ls-tree) at head / round 1 / END')
MODES = []
for p, want in sorted(k.get('mode_pins', {}).items()):
    got = {'head': (ent(H, p) or ('ABSENT',))[0], 'round1': (ent(k['round1_head'], p) or ('ABSENT',))[0], 'END': (ent(END, p) or ('ABSENT',))[0] if END else 'n/a'}
    ok = all(v == want for v in got.values())
    MODES.append(dict(pr=n, path=p, want=want, got=got, ok=ok))
    print('    #%s %s: want %s | head %s | round1 %s | END %s | %s' % (n, p, want, got['head'], got['round1'], got['END'], 'OK' if ok else 'MODE MISMATCH'))
    if not ok: bad.append('(H) #%s %s recorded mode %s != the pin %s' % (n, p, got, want))
print('    MODE SUMMARY: %d path(s) pinned, %d OK | pins seen: %s (a pin set with only one mode value could not discriminate)' % (len(MODES), sum(m['ok'] for m in MODES), sorted(set(m['want'] for m in MODES))))
P = {'measured_at': now(), 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'order': ORDER, 'prs': {n: S}, 'union': sorted(names),
     'paths_total': len(names), 'paths_distinct': len(set(names)), 'end_tree': END, 'squash_sim': SQ, 'simulate': SIM, 'simulated_heads': SIMH, 'modes': MODES}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]
    if SIM: json.dump(P, open(os.path.join(G, 'pins_gate46.SIM-%s.json' % SIM), 'w'), indent=1)
    raise SystemExit(1)
f = 'pins_gate46.SIM-%s.json' % SIM if SIM else 'pins_gate46.json'
json.dump(P, open(os.path.join(G, f), 'w'), indent=1)
print('PASS: FAIL=0 -> %s | develop %s | head %s | END_TREE %s | %d paths, round-2 delta %s' % (f, DEV[:12], H[:12], END, len(names), r2))
