#!/usr/bin/env python3
"""predict_batch_scratch_gate20T1.py — every git WRITE verb of the gate20T1 drafter (and of the launch-time re-pin) lives here, in a scratch clone made
FROM ORIGIN (`git clone --bare --filter=blob:none` of git@github.com:Secuura/Distributed_Secuura.git over the checkout's own ssh road — its remote URL +
repo-local core.sshCommand, read with `config --get`, never printed) under a Claude scratchpad (argv[1]). NEVER `--shared` from the checkout. The Secuura
checkout is only READ (count-objects before/after printed). The gate20T2 predict script re-keyed to the SIX tier-1 heads, plus THE BASE MOVE:
PR 11 (KS-1143, AMENDMENT 18:1x) while PENDING (no READY 11 captured): a PREDICTED PR-11 commit is built in the scratch clone from its canonical over
BASE (commit-tree; a write verb in the scratch clone only) and every tree below uses it, labelled PREDICTED; newdev_tree.txt then says
t1sub_kind PREDICTED and fill / gen REFUSE. Once READY 11 lands its real head is fetched and its
file blob must equal the canonical-at-BASE blob; its PARENT must be BASE like the other six (Wednesday's 18:1x CORRECTION to the amendment).
(a) THE HEADS: develop + refs/pull/N/head for the six (seven) (+ the four tier-2 heads, for the ALL-10 cross-check) fetched by ref INTO the scratch clone; each
    head's parent == BASE 2bc5ccf63; per head: name-status / numstat vs the pins, every blob's 12-hex prefix + lines + MODE (read, not assumed).
(b) THE TREES OVER BASE: the six heads chained by REAL `merge-tree --write-tree` over BASE in THREE orders -> ONE tree == the seat's TIER-1 SUB-TREE
    655c450d8f3e (READY 10); shortstat; 13 rows; 0 bytes under services/auth/ (diff-tree over the whole dir, not the path list); the tier-2 four paths
    untouched; T2-then-T1 == T1-then-T2 == the seat's ALL-10 513390fde5d2.
(c) THE DEVELOP AT THIS READ (DEV_LAUNCH = origin develop, fetched in this run): BASE must be an ancestor (else rc 4); the move BASE..DEV_LAUNCH listed
    commit by commit; its paths ∩ the 13 tier-1 paths MUST be EMPTY and ∩ the tamper file EMPTY and 0 bytes under services/auth/ (else rc 4); every
    tier-2 path that moved is judged against the tier-2 heads' blobs (LANDED / OTHER). Per-PR merged tree over DEV_LAUNCH (real merge-tree), every
    PR path at its head blob in it, every moved path at DEV_LAUNCH's blob; END_TREE = the six chained over DEV_LAUNCH in THREE orders -> ONE tree;
    shortstat DEV_LAUNCH..END_TREE == the sub-tree's `13 files changed, 498 insertions(+), 25 deletions(-)` (disjointness makes it so — measured, not
    assumed); CONTROL: when DEV_LAUNCH's tree == the tier-2 END_TREE d13a26e19c8d, END_TREE MUST == the seat's ALL-10 513390fde5d2.
(d) CANONICAL-PATCH IDENTITY at BASE: every canonical section applied (with its recorded opts) with `git apply --cached` into a temp index; strict /
    -R / --recount --check rcs; blobs == the READY 12-hex after each PR; PR 10's intermediate blob after its first stage == 8a67471cef2c / 1266; per-PR
    write-tree == the head tree (PR 6: canonical + the head's generated YAML blob == the head tree; the YAML is NOT a canonical — its diff at the head is
    printed: exactly `required: false` -> `required: true`, +1/-1).
(e) READS the gate leans on: PR 9 `git grep -c rawAuthorization` at BASE and head (writes vs comments); PR 8 callers of check-no-demo-mutation at the
    head; PR 3 the tamper line kyc/src/index.ts:303 at BASE and at DEV_LAUNCH (it must not have moved).
Writes newdev_tree.txt (+ devmove.txt) ONLY when every hard assertion holds (rc 0); on a refusal the previous newdev_tree.txt is kept beside as
newdev_tree.txt.pre-HHMMSS and NO new one is written — so fill / gen refuse on a stale reading.
Usage: predict_batch_scratch_gate20T1.py <scratchpad dir under /private/tmp/claude-501/> (the guard refuses rc 9 otherwise)."""
import hashlib, json, os, random, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T1 as R
SCRATCH_ROOT = '/private/tmp/claude-501/'
S = os.path.realpath(sys.argv[1]) if len(sys.argv) > 1 else ''
if not (S.startswith(os.path.realpath(SCRATCH_ROOT)) and '/scratchpad' in S and os.path.isdir(S)):
    print('REFUSING: argv[1] is not a scratchpad under', SCRATCH_ROOT, '->', S); sys.exit(9)
if S.startswith(os.path.realpath(R.REPO)): print('REFUSING: the scratchpad is inside the Secuura checkout'); sys.exit(9)
WRITE_VERBS = {'apply', 'read-tree', 'write-tree', 'merge-tree', 'commit-tree', 'fetch', 'update-ref', 'update-index', 'hash-object', 'init', 'clone', 'worktree', 'checkout', 'merge', 'commit'}
FAIL = []
def hard(cond, what):
    if not cond: FAIL.append(what); print('  !! HARD ASSERTION FAILED:', what)
    return cond
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None, inp=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate20T1', now())
co_before = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
sshc = sh(['git', '-C', R.REPO, 'config', '--get', 'core.sshCommand'])[1]; print('checkout core.sshCommand read:', 'yes (not printed)' if sshc else 'NO')
url = sh(['git', '-C', R.REPO, 'config', '--get', 'remote.origin.url'])[1]; print('checkout remote.origin.url:', url, '== round20T1:', url == R.ORIGIN_URL)
Cdir = tempfile.mkdtemp(prefix='predict20T1.', dir=S); CL = Cdir + '/origin.git'; WT = Cdir + '/wt'; os.makedirs(WT)
ENV = dict(os.environ, GIT_SSH_COMMAND=sshc) if sshc else dict(os.environ)
os.chdir(Cdir); print('cwd now', os.getcwd(), '| under the scratchpad:', os.path.realpath(os.getcwd()).startswith(S))
def assert_in_scratch(verb):
    if verb in WRITE_VERBS and not os.path.realpath(os.getcwd()).startswith(S):
        print('REFUSING write verb', verb, 'outside the scratchpad: cwd', os.getcwd()); sys.exit(9)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN (bare, blob:none) rc=%d %s -> %s' % (rc, e[:120], CL)); assert rc == 0
def g(*a, env=None, inp=None):
    assert_in_scratch(a[0]); return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
print('PR11_PENDING', R.PR11_PENDING, '| PR 11', R.PRS['11']['n'], R.PRS['11']['head'], R.PRS['11']['branch'])
T1N = [R.PRS[p]['n'] for p in R.PUSH if R.PRS[p]['n']]; T2N = sorted(R.T2_PRS)
lsr = sh(['git', '-C', R.REPO, 'ls-remote', 'origin', 'refs/heads/develop', R.PRS['11']['branch_glob']] + ['refs/pull/%s/head' % n for n in T1N + T2N])
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s: %d refs' % (lsr[0], now(), len(LS)))
for n in T1N: print('  refs/pull/%s/head %s' % (n, LS.get('refs/pull/%s/head' % n, 'ABSENT')))
P11BR = sorted(r for r in LS if r.startswith('refs/heads/feature/ks-1143-')); print('  KS-1143 branches at origin:', P11BR or 'NONE')
refspecs = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/pull/%s/head' % (n, n) for n in T1N + T2N]
if R.PR11_PENDING and P11BR: refspecs.append('+%s:refs/heads/pr11-expected' % P11BR[0])
rc, o, e = g('fetch', '--quiet', 'origin', *refspecs); print('fetch by ref FROM ORIGIN rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEVL = g('rev-parse', 'refs/heads/develop')[1]; print('origin develop at fetch (DEV_LAUNCH):', DEVL, '| ls-remote said', LS.get('refs/heads/develop'), '| == BASE:', DEVL == R.BASE)
hard(DEVL == LS.get('refs/heads/develop'), 'develop moved between the ls-remote and the fetch (re-run)')
def tree_of(c): return g('rev-parse', c + '^{tree}')[1]
hard(tree_of(R.BASE) == R.BASE_TREE, 'BASE tree != b4f2a8beaecd')
def lstree(tree, path):
    rc, o, e = g('ls-tree', tree, '--', path); return (o.split()[0], o.split()[2]) if o else ('ABSENT', 'ABSENT')
def cat(b): return subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True, env=ENV).stdout if b != 'ABSENT' else b''
def nlines(b): return cat(b).count(b'\n')
BT = tree_of(R.BASE)
def idx(name, base=R.BASE):
    env = dict(ENV, GIT_INDEX_FILE=Cdir + '/idx-' + name, GIT_WORK_TREE=WT); g('read-tree', base, env=env); return env
def blob_in(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
cenv = dict(ENV, GIT_AUTHOR_NAME='gate20T1-drafter', GIT_AUTHOR_EMAIL='drafter@scratch', GIT_COMMITTER_NAME='gate20T1-drafter', GIT_COMMITTER_EMAIL='drafter@scratch',
            GIT_AUTHOR_DATE='2026-09-23T00:00:00Z', GIT_COMMITTER_DATE='2026-09-23T00:00:00Z')
P11PATH = R.PRS['11']['files'][0]['path']
env11 = idx('pred11'); row11 = R.PRS['11']['canon'][0]; ap11 = g('apply', '--cached', R.canon_path(row11), env=env11); t11 = g('write-tree', env=env11)[1]
rc, P11, e = g('commit-tree', t11, '-p', R.BASE, '-m', 'scratch: PREDICTED PR 11 (KS-1143 GUARDMENTION-SELFTEST) from its canonical', env=cenv)
PRED11_BLOB = blob_in(env11, P11PATH)
print('PREDICTED PR 11: canonical apply rc %d -> tree %s | blob %s / %d lines (BASE %s) | scratch commit %s' % (ap11[0], t11[:12], PRED11_BLOB[:12], nlines(PRED11_BLOB), lstree(BT, P11PATH)[1][:12], P11[:9]))
hard(ap11[0] == 0, 'PR 11 canonical does not apply strict at BASE')
R.PRS['11']['files'][0]['blob12'] = PRED11_BLOB[:12]; R.PRS['11']['files'][0]['lines'] = nlines(PRED11_BLOB)
R.PRS['11']['files'][0]['dev_blob12'] = lstree(BT, P11PATH)[1][:12]; R.PRS['11']['files'][0]['dev_lines'] = nlines(lstree(BT, P11PATH)[1])
REF = {p: ('refs/pull/%s/head' % R.PRS[p]['n']) if R.PRS[p]['n'] else P11 for p in R.PUSH}
if R.PR11_PENDING:
    x = g('rev-parse', '--verify', '-q', 'refs/heads/pr11-expected')[1]
    print('PR 11 PENDING: every tree below uses the PREDICTED commit %s | a ks-1143 branch at origin: %s%s' % (P11[:9], x or 'ABSENT', (' parent %s, blob %s == predicted %s' % (g('rev-parse', x + '^')[1][:9], lstree(tree_of(x), P11PATH)[1][:12], lstree(tree_of(x), P11PATH)[1] == PRED11_BLOB)) if x else ''))
PARENT = {}
print('--- (a) THE HEADS (each read from the scratch clone fetched from origin)')
HEADTREE = {}; blobs40 = {}; modes = {}; ok_heads = 0
for p in R.PUSH:
    pr = R.PRS[p]; h = g('rev-parse', REF[p])[1]; par = g('rev-parse', h + '^')[1]; t = tree_of(h); HEADTREE[p] = t; PARENT[p] = par
    ns = g('diff-tree', '-r', '--name-status', par, h)[1].splitlines(); num = g('diff-tree', '-r', '--numstat', par, h)[1].splitlines()
    paths = sorted(l.split('\t')[1] for l in ns); want = sorted(f['path'] for f in pr['files'])
    adds = sum(int(l.split('\t')[0]) for l in num); dels = sum(int(l.split('\t')[1]) for l in num)
    okh = (h == pr['head']) if pr['head'] else None
    okp = par == R.BASE   # all SEVEN heads share BASE (Wednesday's 18:1x CORRECTION: PR 11 too — the seat cannot fetch)
    okt = t.startswith(pr['tree12']) if pr['tree12'] else (lstree(t, P11PATH)[1] == PRED11_BLOB)
    okf = paths == want; okn = (adds, dels) == (pr['adds'], pr['dels'])
    nc = g('rev-list', '--count', par + '..' + h)[1]
    print('  PR %-2s #%s %-8s %shead %s == READY %s | parent %s (== BASE %s; accepted %s) | commits %s | tree %s == READY %s | files == pinned %s %s | +%d/-%d == %s' % (p, pr['n'] or 'PENDING', pr['key'], '(PREDICTED) ' if not pr['head'] else '', h[:9], okh, par[:9], par == R.BASE, okp, nc, t[:12], okt, okf, '' if okf else (paths, want), adds, dels, okn))
    for f in pr['files']:
        m, b = lstree(t, f['path']); md, bd = lstree(BT, f['path']); blobs40[(p, f['path'])] = b; modes[f['path']] = (m, md)
        if f['dev_blob12'] and lstree(tree_of(par), f['path'])[1] != bd: print('     (the parent\'s blob %s differs from BASE\'s %s)' % (lstree(tree_of(par), f['path'])[1][:12], bd[:12]))
        st = [l.split('\t')[0] for l in ns if l.split('\t')[1] == f['path']]
        dv = ('%s == %s %s / %d lines' % (bd[:12], f['dev_blob12'], bd.startswith(f['dev_blob12']), nlines(bd))) if f['dev_blob12'] else ('%s / %d lines (pinned %s)' % (bd[:12], nlines(bd), 'NEW' if f['mode'] == 'new' else 'measure'))
        okb = b.startswith(f['blob12']) and (f['lines'] is None or nlines(b) == f['lines'])
        print('     %-92s %s blob %s == %s %s | lines %d (want %s) | mode %s (BASE %s) | BASE %s' % (f['path'], st, b[:12], f['blob12'], okb, nlines(b), f['lines'], m, md, dv))
        hard(okb, 'PR %s %s blob/lines' % (p, f['path']))
    if hard((okh is not False) and okp and okt and okf and okn and nc == '1', 'PR %s head shape' % p): ok_heads += 1
print('  heads fully agreeing (PR 11 PREDICTED while pending): %d/7 | MODES: %s' % (ok_heads, {k.split('/')[-1]: v for k, v in modes.items()}))
def merge(base, ours, theirs):
    rc, o, e = g('merge-tree', '--write-tree', '--merge-base=' + base, ours, theirs); return rc, o.splitlines()[0] if o else '', e
MB = {}
def chain(refs, start):
    cur = start
    for ref in refs:
        rc, t, e = merge(MB.get(ref, R.BASE), cur, ref)
        if rc != 0: return 'CONFLICT at %s: %s %s' % (ref, t[:12], e[:80])
        cur = t
    return cur
for p in R.PUSH: MB[REF[p]] = PARENT[p]
SIX = [p for p in R.PUSH if p != '11']
orders = {'seat order': list(R.PUSH), 'reverse': list(reversed(R.PUSH)), 'seed-20 shuffle': random.Random(20).sample(R.PUSH, len(R.PUSH))}
def auth_bytes(a, b):
    o = g('diff-tree', '-r', '--numstat', a, b, '--', R.AUTH_DIR)[1]; return o.splitlines() if o else []
print('--- (b) THE TREES over BASE', R.BASE[:9], '(REAL merge-tree --write-tree, chained; three orders)')
SUB = {}
for name, order in orders.items():
    SUB[name] = chain([REF[p] for p in order], R.BASE); print('  tier-1 sub-tree [%s] %s -> %s' % (name, ' '.join(order), SUB[name]))
A = SUB['seat order']; one = len(set(SUB.values())) == 1 and len(A) == 40
hard(one, 'tier-1 sub-tree not ONE tree in three orders')
print('  ONE tree (SEVEN PRs) in three orders: %s | %s | == the seat\'s READY 11 %s: %s' % (one, 'PREDICTED (PR 11 from its canonical)' if R.PR11_PENDING else 'MEASURED (seven real heads)', R.SEAT_T1SUB[:12], A == R.SEAT_T1SUB))
if not R.PR11_PENDING: hard(A == R.SEAT_T1SUB, 'the seven-PR sub-tree != READY 11 f85c25b427cd')
A6 = chain([REF[p] for p in SIX], R.BASE); A6r = chain([REF[p] for p in reversed(SIX)], R.BASE)
print('  CROSS-CHECK the SIX (PRs 3-10) over BASE: %s / reverse %s == the seat\'s READY 10 %s: %s' % (A6[:12], A6r[:12], R.SEAT_T1SUB_6[:12], A6 == A6r == R.SEAT_T1SUB_6))
hard(A6 == A6r == R.SEAT_T1SUB_6, 'the six-PR sub-tree != READY 10 655c450d8f3e')
ss = g('diff-tree', '-r', '--shortstat', R.BASE, A)[1].strip(); print('  shortstat:', ss, '| == the seven (the six READY 10 + PR 11 +5/-1):', ss == R.SEAT_T1SUB_SHORTSTAT); hard(ss == R.SEAT_T1SUB_SHORTSTAT, 'sub-tree shortstat')
ns = g('diff-tree', '-r', '--name-status', R.BASE, A)[1].splitlines(); print('  name-status: %d rows, A %d M %d | == round20T1 distinct: %s' % (len(ns), sum(1 for l in ns if l.startswith('A')), sum(1 for l in ns if l.startswith('M')), sorted(l.split('\t')[1] for l in ns) == R.distinct_paths()))
mism = sum(1 for p in R.PUSH for f in R.PRS[p]['files'] if lstree(A, f['path'])[1] != blobs40[(p, f['path'])]); hard(mism == 0, 'sub-tree path at a non-head blob')
ab = auth_bytes(R.BASE, A); hard(not ab, 'bytes under services/auth/ in the sub-tree'); print('  every path at its head blob: %s | services/auth/ numstat rows BASE..SUB: %d (control: the same diff over services/api-gateway/ gives %d rows)' % (mism == 0, len(ab), len((g('diff-tree', '-r', '--numstat', R.BASE, A, '--', R.D + 'services/api-gateway/')[1] or '').splitlines())))
t2_over = [q for q in R.T2_PATHS if lstree(A, q)[1] != lstree(BT, q)[1]]; tf_over = [q for q in R.TAMPER_FILES if lstree(A, q)[1] != lstree(BT, q)[1]]
print('  the tier-2 four paths changed by the sub-tree: %s | the tamper file changed: %s' % (t2_over or 'NONE', tf_over or 'NONE')); hard(not t2_over and not tf_over, 'sub-tree touches tier-2 / tamper')
T2REF = ['refs/pull/%s/head' % n for n in T2N]
for r_ in T2REF: MB[r_] = R.BASE
for n in T2N: hard(g('rev-parse', 'refs/pull/%s/head' % n)[1] == R.T2_PRS[n][1], 'tier-2 head #%s moved' % n)
t2sub = chain(T2REF, R.BASE); a10a = chain(T2REF, A6); a10b = chain([REF[p] for p in SIX], t2sub); a11 = chain([REF[p] for p in R.PUSH], t2sub)
print('  tier-2 four over BASE -> %s == the tier-2 END_TREE %s: %s | ALL-10 T1-then-T2 %s / T2-then-T1 %s == the seat %s: %s' % (t2sub[:12], R.T2_SUB[:12], t2sub == R.T2_SUB, a10a[:12], a10b[:12], R.SEAT_ALL10[:12], a10a == a10b == R.SEAT_ALL10))
hard(t2sub == R.T2_SUB and a10a == a10b == R.SEAT_ALL10, 'ALL-10 cross-check')
print('  ALL-11 (tier 2 + the seven) over BASE: %s (%s)' % (a11, 'PREDICTED' if R.PR11_PENDING else 'MEASURED'))
print('--- (c) THE DEVELOP AT THIS READ (DEV_LAUNCH %s)' % DEVL)
anc = sh(['git', '-C', CL, 'merge-base', '--is-ancestor', R.BASE, DEVL], env=ENV)[0]; hard(anc == 0, 'BASE is not an ancestor of develop (a rewrite?)')
behind = int(g('rev-list', '--count', R.BASE + '..' + DEVL)[1]); log = g('log', '--format=%H %an %ad %s', '--date=iso-strict', R.BASE + '..' + DEVL)[1]
print('  BASE ancestor of DEV_LAUNCH: %s | commits BASE..DEV_LAUNCH: %d (first-parent %s)' % (anc == 0, behind, g('rev-list', '--count', '--first-parent', R.BASE + '..' + DEVL)[1]))
for l in log.splitlines(): print('    ' + l[:160])
DT = tree_of(DEVL); moved = g('diff-tree', '-r', '--name-only', R.BASE, DEVL)[1].splitlines() if DEVL != R.BASE else []
print('  paths moved BASE..DEV_LAUNCH: %d %s' % (len(moved), moved[:12]))
ov1 = sorted(set(moved) & set(R.all_paths())); ovt = sorted(set(moved) & set(R.TAMPER_FILES)); abd = auth_bytes(R.BASE, DEVL)
print('  ∩ the 13 tier-1 paths: %s | ∩ the tamper file: %s | services/auth/ rows moved: %d (not a tier-1 fact, recorded)' % (ov1 or 'NONE', ovt or 'NONE', len(abd)))
hard(not ov1, 'the develop move touches a tier-1 path — re-predict by hand'); hard(not ovt, 'the develop move touches the tamper file')
judge = []
for q in moved:
    cur = lstree(DT, q)[1]
    if q in R.T2_BLOBS12: judge.append((q, 'LANDED tier-2' if cur.startswith(R.T2_BLOBS12[q]) else 'OTHER (tier-2 path, not the head blob)', cur[:12]))
    else: judge.append((q, 'NON-TIER-2 path', cur[:12]))
for j in judge: print('    %-80s %s %s' % j)
t2landed = sum(1 for j in judge if j[1] == 'LANDED tier-2'); others = [j for j in judge if j[1] != 'LANDED tier-2']
dev_is_t2 = DT == R.T2_SUB
print('  tier-2 paths LANDED on DEV_LAUNCH: %d/4 | other moved paths: %d | DEV_LAUNCH tree %s == the tier-2 END_TREE %s: %s' % (t2landed, len(others), DT[:12], R.T2_SUB[:12], dev_is_t2))
MERGED = {}
for p in R.PUSH:
    rc, t, e = merge(PARENT[p], DEVL, REF[p]); MERGED[p] = t if rc == 0 else 'CONFLICT'
    okp = all(lstree(t, f['path'])[1] == blobs40[(p, f['path'])] for f in R.PRS[p]['files']) if rc == 0 else False
    okm = all(lstree(t, q)[1] == lstree(DT, q)[1] for q in moved) if rc == 0 else False
    nsm = g('diff-tree', '-r', '--name-only', DEVL, t)[1].splitlines() if rc == 0 else []
    print('  PR %-2s #%s merged over DEV_LAUNCH rc %d -> %s | own paths at head blobs %s | moved paths at DEV_LAUNCH blobs %s | DEV_LAUNCH..merged paths == own %s' % (p, R.PRS[p]['n'] or 'PENDING', rc, t, okp, okm, sorted(nsm) == sorted(f['path'] for f in R.PRS[p]['files'])))
    hard(rc == 0 and okp and okm and sorted(nsm) == sorted(f['path'] for f in R.PRS[p]['files']), 'PR %s merged tree over DEV_LAUNCH' % p)
END = {}
for name, order in orders.items():
    END[name] = chain([REF[p] for p in order], DEVL); print('  END_TREE over DEV_LAUNCH [%s] -> %s' % (name, END[name]))
E = END['seat order']; hard(len(set(END.values())) == 1 and len(E) == 40, 'END_TREE not ONE tree in three orders')
E6 = chain([REF[p] for p in SIX], DEVL); print('  END over DEV_LAUNCH of the SIX only (cross-check): %s' % E6)
ess = g('diff-tree', '-r', '--shortstat', DEVL, E)[1].strip(); eab = auth_bytes(DEVL, E)
print('  END shortstat DEV_LAUNCH..END: %s == the sub-tree\'s %s | services/auth/ rows DEV_LAUNCH..END: %d' % (ess, ess == R.SEAT_T1SUB_SHORTSTAT, len(eab)))
hard(ess == R.SEAT_T1SUB_SHORTSTAT and not eab, 'END shortstat / auth bytes')
if dev_is_t2 and not R.PR11_PENDING: hard(E == R.SEAT_END_T2DEV, 'END over the tier-2 end != READY 11 073e658618cf'); print('  END over the tier-2 end == READY 11 %s: %s' % (R.SEAT_END_T2DEV[:12], E == R.SEAT_END_T2DEV))
if dev_is_t2: print('  CONTROL (DEV_LAUNCH tree == the tier-2 END_TREE): the SIX over it %s == the seat\'s ALL-10 %s: %s | the SEVEN over it %s == ALL-11 over BASE %s: %s' % (E6[:12], R.SEAT_ALL10[:12], E6 == R.SEAT_ALL10, E[:12], a11[:12], E == a11)); hard(E6 == R.SEAT_ALL10 and E == a11, 'END over the tier-2 end != ALL-10 / ALL-11')
elif DEVL == R.BASE: print('  CONTROL (develop still BASE): END_TREE %s == the sub-tree %s: %s' % (E[:12], A[:12], E == A)); hard(E == A, 'END over BASE != sub-tree')
else: print('  CONTROL: DEV_LAUNCH is neither BASE nor the tier-2 END_TREE — END_TREE is a NEW oid; no seat number to equal (measured only)')
print('--- (d) CANONICAL-PATCH IDENTITY at BASE (temp index per PR in the scratch clone; --cached; sections in order with their recorded opts)')
tree_ok = 0
for p in R.PUSH:
    pr = R.PRS[p]; env = idx('pr' + p)
    for i, row in enumerate(pr['canon']):
        label, rd, fn, sha16, opts, _ = row; patch = R.canon_path(row); ex = os.path.exists(patch)
        sha = hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?'; size = os.path.getsize(patch) if ex else -1
        envc = idx('chk-' + label, base=g('write-tree', env=env)[1])
        st = g('apply', '--cached', '--check', patch, env=envc); rv = g('apply', '--cached', '--check', '-R', patch, env=envc); rcn = g('apply', '--cached', '--check', '--recount', patch, env=envc)
        ap = g('apply', '--cached', *([opts] if opts else []), patch, env=env)
        print('  PR %-2s %-22s %-50s sha16 %s == pinned %s (%d B) | strict --check rc %d | -R rc %d | --recount rc %d | APPLY%s rc %d' % (p, label, rd + '/' + fn, sha, sha == sha16, size, st[0], rv[0], rcn[0], (' ' + opts) if opts else '', ap[0]))
        hard(sha == sha16 and ap[0] == 0, 'PR %s canonical %s sha/apply' % (p, label))
        if p == '10' and label == '1084-SIGTENANT-s2':
            mb = blob_in(env, R.GW + 'routes/proxy.ts'); print('     PR 10 INTERMEDIATE after stage 1: proxy.ts %s / %d lines == %s / %d: %s' % (mb[:12], nlines(mb), pr['mid'][0], pr['mid'][1], mb.startswith(pr['mid'][0]) and nlines(mb) == pr['mid'][1]))
            hard(mb.startswith(pr['mid'][0]) and nlines(mb) == pr['mid'][1], 'PR 10 intermediate blob')
    if 'canon_patch' in pr:
        for cp in [pr['canon_patch']] + ([pr['canon_patch2']] if 'canon_patch2' in pr else []):
            pp = R.LM + '/runs/' + cp[0] + '/out.md.checker/patch.diff'; ps = hashlib.sha256(open(pp, 'rb').read()).hexdigest()[:16]
            secs = sorted(x for x in os.listdir(os.path.dirname(pp)) if x in ('section_1.diff', 'section_2.diff'))
            catb = b''.join(open(os.path.join(os.path.dirname(pp), x), 'rb').read() for x in secs)
            print('     patch.diff %s sha16 %s == pinned %s %s | cat(%s) == patch.diff: %s' % (cp[0], ps, cp[1], ps == cp[1], '+'.join(secs), catb == open(pp, 'rb').read()))
    gen = [f for f in pr['files'] if f['kind'] == 'generated-spec']
    for f in gen:
        hb = blobs40[(p, f['path'])]; env2 = dict(env); g('update-index', '--add', '--cacheinfo', '100644,%s,%s' % (hb, f['path']), env=env2)
        dd = g('diff', '-U0', R.BASE, pr['head'], '--', f['path'])[1]
        pl = [l for l in dd.splitlines() if l.startswith('+') and not l.startswith('+++')]; ml = [l for l in dd.splitlines() if l.startswith('-') and not l.startswith('---')]
        print('     PR 6 GENERATED SPEC (not a canonical): head blob %s == READY %s %s | BASE %s | diff +%d/-%d: %s | %s' % (hb[:12], pr['spec_blob40'][:12], hb == pr['spec_blob40'], lstree(BT, f['path'])[1][:12], len(pl), len(ml), [x.strip() for x in ml], [x.strip() for x in pl]))
        hard(hb == pr['spec_blob40'], 'PR 6 spec blob != READY 6 834b0c3d2d2c')
        hard(len(pl) == 1 and len(ml) == 1 and ml[0].lstrip('-').strip() == 'required: false' and pl[0].lstrip('+').strip() == 'required: true', 'PR 6 spec diff is not exactly required: false -> true')
    if 'hunks' in pr:
        for hk, (fn_, sh16) in sorted(pr['hunks'].items()):
            hp = R.LM + '/runs/' + pr['canon'][0][1] + '/out.md.checker/' + fn_; hs = hashlib.sha256(open(hp, 'rb').read()).hexdigest()[:16]
            envh = idx('hunk-' + hk); aph = g('apply', '--cached', hp, env=envh); bh = blob_in(envh, P11PATH)
            print('     PR 11 SELF-TESTING SPLIT: %-5s hunk %s sha16 %s == pinned %s %s | strict apply at BASE rc %d -> blob %s / %d lines (the gate runs the suite on each: test-alone MUST red on W6, prod-alone green, both green)' % (hk, fn_, hs, sh16, hs == sh16, aph[0], bh[:12], nlines(bh)))
            hard(hs == sh16 and aph[0] == 0, 'PR 11 hunk %s' % hk)
    fin = all(blob_in(env, f['path']).startswith(f['blob12']) for f in pr['files'])
    t = g('write-tree', env=env)[1]
    if PARENT[p] != R.BASE:
        ok = all(blob_in(env, f['path']) == blobs40[(p, f['path'])] for f in pr['files']); print('     (PR %s parent %s != BASE: canonical-at-BASE blobs == head blobs %s — the tree comparison is by path)' % (p, PARENT[p][:9], ok))
    else: ok = t == HEADTREE[p]
    tree_ok += ok
    print('     final blobs == READY 12-hex: %s | write-tree %s == head tree %s: %s%s' % (fin, t[:12], HEADTREE[p][:12], ok, ' (canonical + the head\'s generated YAML)' if gen else ''))
    hard(fin and ok, 'PR %s canonical tree != head tree' % p)
print('  per-PR canonical trees == head trees: %d/7' % tree_ok)
envx = idx('ctrl'); ctl = g('apply', '--cached', '--check', Cdir + '/does-not-exist.diff', env=envx); print('  nonexistent-patch control rc', ctl[0], '(128 expected)')
print('--- (e) READS the gate leans on')
def grepc(rev, pat, path=None):
    a = ['grep', '-n', '-F', pat, rev] + (['--', path] if path else []); rc, o, e = g(*a); return [l.split(':', 1)[1] for l in o.splitlines()] if o else []
ra_b = grepc(R.BASE, 'rawAuthorization', R.D + 'services/'); ra_h = grepc(R.PRS['9']['head'], 'rawAuthorization', R.D + 'services/')
print('  PR 9: `git grep -n -F rawAuthorization` under services/ at BASE %d hits, at head %d hits:' % (len(ra_b), len(ra_h)))
for l in ra_h: print('    head: ' + l[:170])
nb = grepc(R.PRS['8']['head'], 'check-no-demo-mutation'); print('  PR 8: `git grep -n -F check-no-demo-mutation` at head: %d hits' % len(nb))
for l in nb: print('    ' + l[:170])
for rev, nm in ((R.BASE, 'BASE'), (DEVL, 'DEV_LAUNCH')):
    o = cat(lstree(tree_of(rev), R.TAMPER_FILES[0])[1]).decode('utf-8', 'replace').split('\n')
    print('  PR 3 tamper line %s:303 at %s: %s' % (R.TAMPER_FILES[0].split('/')[-3], nm, o[302].strip()[:150] if len(o) > 302 else 'ABSENT'))
print('--- RESULT: %d hard assertion(s) failed %s' % (len(FAIL), FAIL))
co_after = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects after:', co_after.replace('\n', ' '), '| byte-identical:', co_before == co_after)
NDT = os.path.join(G, 'newdev_tree.txt')
if FAIL:
    print('NOT writing newdev_tree.txt (the previous one, if any, is left as it was but is NOT this reading — fill / gen assert dev_launch == origin develop)')
    print('scratch clone', CL); print('done', now()); sys.exit(4)
if os.path.exists(NDT): shutil.copyfile(NDT, NDT + '.pre-' + now()[11:19].replace(':', ''))
with open(NDT, 'w') as f:
    f.write('pr11_pending %s\npr11_head %s\npr11_predicted_blob %s\nt1sub6 %s\n' % (R.PR11_PENDING, R.PRS['11']['head'] or 'PENDING', PRED11_BLOB, A6))
    f.write('base %s\nbase_tree %s\nt1sub %s\nt1sub_kind %s\ndev_launch %s\ndev_launch_tree %s\ndev_launch_is_t2end %s\nbehind %d\nt2_landed %d\nother_moved %d\nend_tree %s\nend_shortstat %s\n' % (
        R.BASE, R.BASE_TREE, A, 'PREDICTED' if R.PR11_PENDING else 'MEASURED', DEVL, DT, dev_is_t2, behind, t2landed, len(others), E, ess))
    f.write('all11_over_base %s\nend6 %s\ntree11 %s\n' % (a11, E6, HEADTREE['11']))
    for p in R.PUSH: f.write('merged_%s %s\n' % (R.PRS[p]['n'] or 'PR11PENDING', MERGED[p]))
    for p in R.PUSH: f.write('parent_%s %s\n' % (R.PRS[p]['n'] or 'PR11PENDING', PARENT[p]))
    for p in R.PUSH:
        for fl in R.PRS[p]['files']: f.write('blob %s %s %s\n' % (fl['path'], blobs40[(p, fl['path'])], modes[fl['path']][0]))
    for p in R.PUSH:
        for fl in R.PRS[p]['files']: f.write('baseblob %s %s\n' % (fl['path'], lstree(BT, fl['path'])[1]))
    f.write('read %s\n' % now())
open(os.path.join(G, 'devmove.txt'), 'w').write('develop move BASE %s .. DEV_LAUNCH %s (%d commits; read %s)\n%s\n' % (R.BASE, DEVL, behind, now(), log))
print('WROTE', NDT, 'and devmove.txt'); print('scratch clone', CL); print('done', now())
