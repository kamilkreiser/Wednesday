#!/usr/bin/env python3
"""predict_batch_scratch_gate19B.py — every git WRITE verb of the gate19B drafter lives here, in a scratch clone made FROM ORIGIN (a `git clone --bare
--filter=blob:none` of git@github.com:Secuura/Distributed_Secuura.git over the checkout's own ssh road — its remote URL + repo-local core.sshCommand,
read from the checkout's config, never printed) under the drafter's scratchpad (argv[1]). NEVER `--shared` from the checkout. The Secuura checkout
is only READ (count-objects before/after printed; byte-identical expected). The gate19C predict script re-keyed to Seat B 19th/20th's NINE.
(a) THE HEADS: develop + refs/pull/N/head for the nine (+ Seat C 19th's twelve, for the overlap) fetched by ref INTO the scratch clone; each head's
    parent == develop 3bad652d1 (fast-forward: merged tree == head tree == the READY's item-0 PR-alone tree; #1200's is the AMENDED tree d309bb90f69f);
    per head: name-status / numstat vs the pins, every blob's 12-hex prefix vs the READY (AT THE HEAD), lines, modes (100644 everywhere — no exec).
(b) THE TREES: the nine heads chained by REAL `merge-tree --write-tree` over develop in THREE orders (push order, reverse, seed-19 shuffle) -> ONE tree
    vs the seat's all-11 3df72c02d325…; shortstat vs `17 files changed, 642 insertions(+), 13 deletions(-)`; the security index.ts PAIR (#1198 + #1199)
    both orders -> one tree 64de96836e46 with the PAIR blob 2ad45cd8e555… / 1603 (alone blobs 7bdaa9cad257 / 5bf6fb62dba8); every other ALL path at its
    head blob; each single tree != ALL; 17 distinct paths; ∩ Seat C 19th's 21 paths = ∅ (Seat C's paths unchanged by ALL; ALL-of-C ∪ ALL-of-B chains
    in both orders -> ONE combined tree, the END STATE if both GOs land, stated for the merging seat).
(c) CANONICAL-PATCH IDENTITY: each of the 19 canonical rows applied with `git apply --cached` into a temp index read from develop: strict --check rc /
    -R --check rc / --recount --check rc; the .opts apply where the READY names one -> the blob == the READY's 12-hex; the two-stage rows (#1194 LOOSE
    then SIDEEFFECTS; #1198 CHECKKEYCP then SCOPETRIM) in sequence with the intermediate asserted; the per-PR write-tree == the head tree ×8 — and for
    #1200 (KS-1164) == the UNAMENDED tree 2a91afd2029e (the control), the head's test blob b4edbe5b0d12 vs the canonical 1d41e7033542 judged by THE
    INSTRUMENT: whitespace-stripped byte-stream equality (True expected; a one-byte control False; `git diff -w` recorded as NON-empty by construction);
    the all-11 over the UNAMENDED #1200 (a commit-tree in the scratch clone) -> 34728affba20 (the seat's item-0 control); a nonexistent-patch control rc 128.
(d) THE DEVELOP MOVE: if origin develop is not 3bad652d1 the new tip is in the clone anyway (fetched by ref); every tree is ALSO predicted over it;
    newdev_tree.txt is written in either case (the generator reads it).
Usage: predict_batch_scratch_gate19B.py <scratchpad dir> (MUST be this session's scratchpad under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/;
the guard refuses rc 9 otherwise; every write verb asserts cwd inside the scratch clone)."""
import hashlib, os, random, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19B as R
sys.path.insert(0, R.SIBLING_GATE_DIR); import round19C as C
SCRATCH_ROOT = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/'
S = os.path.realpath(sys.argv[1]) if len(sys.argv) > 1 else ''
if not (S.startswith(SCRATCH_ROOT) and '/scratchpad' in S and os.path.isdir(S)):
    print('REFUSING: argv[1] is not a scratchpad under', SCRATCH_ROOT, '->', S); sys.exit(9)
if os.path.realpath(R.REPO) in S or S.startswith(os.path.realpath(R.REPO)):
    print('REFUSING: the scratchpad is inside the Secuura checkout'); sys.exit(9)
WRITE_VERBS = {'apply', 'read-tree', 'write-tree', 'merge-tree', 'commit-tree', 'fetch', 'update-ref', 'update-index', 'hash-object', 'init', 'clone', 'worktree', 'checkout', 'merge', 'commit'}
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None, inp=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate19B', now())
co_before = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
sshc = sh(['git', '-C', R.REPO, 'config', '--get', 'core.sshCommand'])[1]; print('checkout core.sshCommand read:', 'yes (not printed)' if sshc else 'NO')
url = sh(['git', '-C', R.REPO, 'config', '--get', 'remote.origin.url'])[1]; print('checkout remote.origin.url:', url, '== round19B:', url == R.ORIGIN_URL)
Cdir = tempfile.mkdtemp(prefix='predict19B.', dir=S); CL = Cdir + '/origin.git'; WT = Cdir + '/wt'; os.makedirs(WT)
assert os.path.realpath(Cdir).startswith(S)
ENV = dict(os.environ, GIT_SSH_COMMAND=sshc) if sshc else dict(os.environ)
os.chdir(Cdir); print('cwd now', os.getcwd(), '| under the scratchpad:', os.path.realpath(os.getcwd()).startswith(S))
def assert_in_scratch(verb):
    if verb in WRITE_VERBS and not os.path.realpath(os.getcwd()).startswith(S):
        print('REFUSING write verb', verb, 'outside the scratchpad: cwd', os.getcwd()); sys.exit(9)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN (bare, blob:none) rc=%d %s -> %s' % (rc, e[:120], CL)); assert rc == 0
def g(*a, env=None, inp=None):
    assert_in_scratch(a[0]); return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
CPRS = [C.PRS[p]['n'] for p in C.PUSH]
refspecs = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/pull/%s/head' % (R.PRS[p]['n'], R.PRS[p]['n']) for p in R.PUSH] + ['+refs/pull/%s/head:refs/pull/%s/head' % (n, n) for n in CPRS]
rc, o, e = g('fetch', '--quiet', 'origin', *refspecs); print('fetch by ref FROM ORIGIN rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEVNOW = g('rev-parse', 'refs/heads/develop')[1]; print('origin develop at fetch:', DEVNOW, '== pin 3bad652d1:', DEVNOW == R.DEV)
DEV = R.DEV
print('develop tree:', g('rev-parse', DEV + '^{tree}')[1], '(pin 12-hex', R.DEV_TREE12 + ')', g('rev-parse', DEV + '^{tree}')[1].startswith(R.DEV_TREE12))
def tree_of(c): return g('rev-parse', c + '^{tree}')[1]
def lstree(tree, path):
    rc, o, e = g('ls-tree', tree, '--', path); return (o.split()[0], o.split()[2]) if o else ('ABSENT', 'ABSENT')
def cat(b):
    return subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True, env=ENV).stdout if b != 'ABSENT' else b''
def nlines(b): return cat(b).count(b'\n')
DEVTREE = tree_of(DEV)
print('--- (a) THE HEADS (each read from the scratch clone fetched from origin; parent / tree / files / blobs / modes)')
HEADTREE = {}; ok_heads = 0; blobs40 = {}
for p in R.PUSH:
    pr = R.PRS[p]; h = g('rev-parse', 'refs/pull/%s/head' % pr['n'])[1]
    par = g('rev-parse', h + '^')[1]; t = tree_of(h); HEADTREE[p] = t
    ns = g('diff-tree', '-r', '--name-status', DEV, h)[1].splitlines(); num = g('diff-tree', '-r', '--numstat', DEV, h)[1].splitlines()
    paths = sorted(l.split('\t')[1] for l in ns); want = sorted(f['path'] for f in pr['files'])
    adds = sum(int(l.split('\t')[0]) for l in num); dels = sum(int(l.split('\t')[1]) for l in num)
    okh = h == pr['head']; okp = par == DEV; okt = t == pr['tree']; okf = paths == want; okn = (adds, dels) == (pr['adds'], pr['dels'])
    ncommits = g('rev-list', '--count', DEV + '..' + h)[1]
    print('  PR %-2s #%s %-8s head %s == READY %s | parent == develop %s | commits %s | tree %s == READY %s | files == pinned %s %s | +%d/-%d == %s' % (p, pr['n'], pr['key'], h[:9], okh, okp, ncommits, t[:12], okt, okf, '' if okf else (paths, want), adds, dels, okn))
    for f in pr['files']:
        m, b = lstree(t, f['path']); md, bd = lstree(DEVTREE, f['path']); blobs40[(p, f['path'])] = b
        st = [l.split('\t')[0] for l in ns if l.split('\t')[1] == f['path']]
        print('     %-95s status %s (want %s) blob %s == READY %s %s | lines %d (want %d) | mode %s (develop %s) %s' % (f['path'], st, 'A' if f['mode'] == 'new' else 'M', b[:12], f['blob12'], b.startswith(f['blob12']), nlines(b), f['lines'], m, md, 'MODE-OK' if m == '100644' else 'MODE-UNEXPECTED'))
    if okh and okp and okt and okf and okn: ok_heads += 1
print('  heads fully agreeing with the READYs: %d/9' % ok_heads)
print('--- (b) THE TREES over develop', DEV[:9], '(REAL merge-tree --write-tree, chained; three orders)')
def merge(base, ours, theirs):
    rc, o, e = g('merge-tree', '--write-tree', '--merge-base=' + base, ours, theirs); return rc, o.splitlines()[0] if o else '', e
def chain(refs, start=DEV):
    cur = start
    for ref in refs:
        rc, t, e = merge(DEV, cur, ref)
        if rc != 0: return 'CONFLICT at %s: %s %s' % (ref, t[:12], e[:80])
        cur = t
    return cur
def pref(p): return 'refs/pull/%s/head' % R.PRS[p]['n']
orders = {'push order': list(R.PUSH), 'reverse': list(reversed(R.PUSH)), 'seed-19 shuffle': random.Random(19).sample(R.PUSH, len(R.PUSH))}
ALL = {}
for name, order in orders.items():
    ALL[name] = chain([pref(p) for p in order]); print('  all-11 chained [%s] %s -> %s == seat all-11 %s: %s' % (name, ' '.join(order), ALL[name][:12], R.SEAT_ALL11[:12], ALL[name] == R.SEAT_ALL11))
A = ALL['push order']
if len(A) == 40:
    ss = g('diff-tree', '-r', '--shortstat', DEV, A)[1]; print('  shortstat:', ss.strip(), '== seat:', ss.strip().endswith(R.SEAT_ALL11_SHORTSTAT))
    ns = g('diff-tree', '-r', '--name-status', DEV, A)[1].splitlines(); print('  name-status: %d rows, A %d M %d | distinct paths %d == 17: %s | == round19B distinct: %s' % (len(ns), sum(1 for l in ns if l.startswith('A')), sum(1 for l in ns if l.startswith('M')), len(ns), len(ns) == 17, sorted(l.split('\t')[1] for l in ns) == R.distinct_paths()))
    mism = 0
    for p in R.PUSH:
        for f in R.PRS[p]['files']:
            m, b = lstree(A, f['path']); hb = blobs40[(p, f['path'])]
            if f['path'] == R.PAIR_PATH:
                print('     ALL %-40s (#%s alone %s) blob %s == PAIR blob %s (EXPECTED: the pair) | lines %d (want %d) | mode %s' % (f['path'], R.PRS[p]['n'], hb[:12], b[:12], b == R.PAIR_BLOB, nlines(b), R.PAIR_LINES, m)); mism += (b != R.PAIR_BLOB)
            elif b != hb: print('     ALL %s blob %s != head blob %s MISMATCH' % (f['path'], b[:12], hb[:12])); mism += 1
    print('  every non-pair ALL path at its head blob, the pair at the PAIR blob: %s (mismatches %d)' % (mism == 0, mism))
    print('  each single head tree != ALL:', all(HEADTREE[p] != A for p in R.PUSH))
    print('  develop tree unchanged:', tree_of(DEV).startswith(R.DEV_TREE12))
    cpaths = C.distinct_paths(); seatc_over = [q for q in cpaths if lstree(A, q)[1] != lstree(DEVTREE, q)[1]]
    print('  Seat C 19th\'s %d paths changed by ALL: %s | B ∩ C paths: %s' % (len(cpaths), seatc_over or 'NONE (0 overlap)', sorted(set(R.distinct_paths()) & set(cpaths)) or 'NONE'))
rc1, t12, e = merge(DEV, pref('6'), pref('7')); rc2, t21, e2 = merge(DEV, pref('7'), pref('6'))
print('  PAIR #1198 then #1199 -> %s (rc %d) | #1199 then #1198 -> %s (rc %d) | one tree: %s | == seat pair 64de96836e46: %s' % (t12[:12], rc1, t21[:12], rc2, t12 == t21, t12.startswith(R.SEAT_PAIR_TREE12)))
if len(t12) == 40:
    m, b = lstree(t12, R.PAIR_PATH); a6 = blobs40[('6', R.PAIR_PATH)]; a7 = blobs40[('7', R.PAIR_PATH)]
    print('  PAIR blob %s == 2ad45cd8e555… %s | lines %d (want 1603) | mode %s | alone blobs #1198 %s (READY %s %s) #1199 %s (READY %s %s) | neither the pair: %s' % (b, b == R.PAIR_BLOB, nlines(b), m, a6[:12], R.PAIR_ALONE['1198'], a6.startswith(R.PAIR_ALONE['1198']), a7[:12], R.PAIR_ALONE['1199'], a7.startswith(R.PAIR_ALONE['1199']), R.PAIR_BLOB not in (a6, a7)))
    dv = lstree(DEVTREE, R.PAIR_PATH)[1]; print('  develop index.ts blob %s lines %d; #1198 alone lines %d; #1199 alone lines %d' % (dv[:12], nlines(dv), nlines(a6), nlines(a7)))
# the combined END STATE if BOTH GOs land (context for the merging seat): C's twelve then B's nine, and B then C
crefs = ['refs/pull/%s/head' % n for n in CPRS]; brefs = [pref(p) for p in R.PUSH]
cb = chain(crefs + brefs); bc = chain(brefs + crefs); c_alone = chain(crefs)
print('  Seat C 19th\'s twelve alone -> %s == gate19C\'s all-12 %s: %s' % (c_alone[:12], C.SEAT_ALL14[:12], c_alone == C.SEAT_ALL14))
print('  COMBINED (C twelve then B nine) -> %s | (B nine then C twelve) -> %s | one tree: %s  <- the END STATE over 3bad652d1 if gate19C\'s GO lands first: BASE moves to C\'s merge commit, the nine re-predicted over it must give THIS tree' % (cb[:12], bc[:12], cb == bc))
if len(cb) == 40: print('  combined shortstat:', g('diff-tree', '-r', '--shortstat', DEV, cb)[1].strip())
print('--- (c) CANONICAL-PATCH IDENTITY at develop (temp index per PR in the scratch clone; --cached; the .opts rows both ways)')
def idx(name, base=DEV):
    env = dict(ENV, GIT_INDEX_FILE=Cdir + '/idx-' + name, GIT_WORK_TREE=WT); g('read-tree', base, env=env); return env
def blob_in(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
tree_ok = 0; CANONTREE = {}
for p in R.PUSH:
    pr = R.PRS[p]; env = idx('pr' + p)
    for row in pr['canon']:
        label, rd, fn, sha16, opts, path = row; patch = R.canon_path(row); ex = os.path.exists(patch)
        sha = hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?'
        envc = idx('chk-' + label)
        st = g('apply', '--cached', '--check', patch, env=envc); rv = g('apply', '--cached', '--check', '-R', patch, env=envc); rcn = g('apply', '--cached', '--check', '--recount', patch, env=envc)
        flags = tuple(opts.split()) if opts else ()
        ap = g('apply', '--cached', *flags, patch, env=env); b = blob_in(env, path)
        print('  PR %-2s %-22s %-52s sha16 %s == READY %s | strict --check rc %d%s | -R rc %d | --recount rc %d | APPLY%s rc %d -> %s / %d lines' % (p, label, rd + '/' + fn, sha, sha == sha16, st[0], (' [' + (st[2].splitlines() or [''])[0][:50] + ']') if st[0] else '', rv[0], rcn[0], (' (' + opts + ')') if opts else '', ap[0], b[:12], nlines(b)))
        if pr.get('intermediate') and label in ('1229-LOOSE',):
            print('     intermediate after %s: %s / %d == READY %s / %d: %s' % (label, b[:12], nlines(b), pr['intermediate'][1], pr['intermediate'][2], b.startswith(pr['intermediate'][1]) and nlines(b) == pr['intermediate'][2]))
    fin = all(blob_in(env, f['path']).startswith(f.get('canon_blob12', f['blob12'])) for f in pr['files'])
    t = g('write-tree', env=env)[1]; CANONTREE[p] = t
    if p == '8':
        print('     final blobs == the CANONICAL 12-hex (report.ts %s; the test %s canonical): %s | write-tree %s == the UNAMENDED tree %s: %s | != the head tree %s (the AMENDED, by construction): %s' % (pr['files'][0]['blob12'], pr['files'][1]['canon_blob12'], fin, t[:12], pr['tree_unamended12'], t.startswith(pr['tree_unamended12']), HEADTREE[p][:12], t != HEADTREE[p]))
        tree_ok += t.startswith(pr['tree_unamended12'])
    else:
        print('     final blobs == READY 12-hex: %s | write-tree %s == head tree %s: %s' % (fin, t[:12], HEADTREE[p][:12], t == HEADTREE[p]))
        tree_ok += (t == HEADTREE[p])
print('  per-PR canonical trees == head trees (8) + #1200 == the unamended control (1): %d/9' % tree_ok)
print('--- (c2) THE KS-1164 AMENDMENT — the INSTRUMENT (whitespace-stripped byte-stream equality; NOT `git diff -w`)')
p8 = R.PRS['8']; tpath = p8['files'][1]['path']
env8 = idx('amend8'); [g('apply', '--cached', R.canon_path(row), env=env8) for row in p8['canon']]
canon_b = blob_in(env8, tpath); head_b = blobs40[('8', tpath)]
cb_bytes = cat(canon_b); hb_bytes = cat(head_b)
def strip_ws(x): return bytes(c for c in x if c not in b' \t\r\n')
eq = strip_ws(cb_bytes) == strip_ws(hb_bytes)
ctrl = strip_ws(cb_bytes) == strip_ws(hb_bytes[:100] + hb_bytes[101:]) if len(hb_bytes) > 101 else None
print('  canonical test blob %s / %d lines / %d B (READY canonical %s / %d) | head blob %s / %d lines / %d B (READY amended %s / %d)' % (canon_b[:12], nlines(canon_b), len(cb_bytes), p8['files'][1]['canon_blob12'], p8['files'][1]['canon_lines'], head_b[:12], nlines(head_b), len(hb_bytes), p8['files'][1]['blob12'], p8['files'][1]['lines']))
print('  INSTRUMENT: whitespace-stripped byte streams equal (every non-whitespace byte identical, in order): %s  <- WHITESPACE-ONLY %s' % (eq, 'CONFIRMED' if eq else 'REFUTED'))
print('  control: the same instrument with ONE byte (index 100, %r) removed from the head copy: %s (must be False)' % (hb_bytes[100:101], ctrl))
print('  non-whitespace byte count canonical %d / head %d | whitespace bytes canonical %d / head %d (delta %+d)' % (len(strip_ws(cb_bytes)), len(strip_ws(hb_bytes)), len(cb_bytes) - len(strip_ws(cb_bytes)), len(hb_bytes) - len(strip_ws(hb_bytes)), (len(hb_bytes) - len(strip_ws(hb_bytes))) - (len(cb_bytes) - len(strip_ws(cb_bytes)))))
open(Cdir + '/canon1164.ts', 'wb').write(cb_bytes); open(Cdir + '/head1164.ts', 'wb').write(hb_bytes)
dw = sh(['git', 'diff', '-w', '--no-index', '--stat', Cdir + '/canon1164.ts', Cdir + '/head1164.ts']); dwf = sh(['git', 'diff', '-w', '--no-index', Cdir + '/canon1164.ts', Cdir + '/head1164.ts'])
print('  `git diff -w --no-index` canonical vs head: rc %d, %d B of diff — NON-EMPTY by construction (LINE-based: a one-line -> four-line wrap is a line change to it); the seat\'s own record says the same. NOT the instrument.' % (dwf[0], len(dwf[1])))
# the all-11 over the UNAMENDED #1200: commit-tree the canonical tree in the scratch clone (a write verb, in the scratch clone only)
cenv = dict(ENV, GIT_AUTHOR_NAME='gate19B-drafter', GIT_AUTHOR_EMAIL='drafter@scratch', GIT_COMMITTER_NAME='gate19B-drafter', GIT_COMMITTER_EMAIL='drafter@scratch')
rc, c8, e = g('commit-tree', CANONTREE['8'], '-p', DEV, '-m', 'scratch: unamended KS-1164 control', env=cenv)
refs_un = [pref(p) if p != '8' else c8 for p in R.PUSH]; un = chain(refs_un)
print('  all-11 over the UNAMENDED #1200 (scratch commit %s of tree %s) -> %s == the seat\'s item-0 control 34728affba20: %s | != the amended all-11: %s' % (c8[:9], CANONTREE['8'][:12], un[:12], un.startswith(R.SEAT_ALL11_UNAMENDED12), un != A))
if len(un) == 40: print('  unamended shortstat:', g('diff-tree', '-r', '--shortstat', DEV, un)[1].strip(), '(the seat: 17 files +639/-13)')
# the .opts rows the strict way too
for p, label in (('1', '730-INGEST500-s1'), ('6', '974-CHECKKEYCP-s1'), ('6', '974-SCOPETRIM-s1')):
    row = [r for r in R.PRS[p]['canon'] if r[0] == label][0]; env = idx('strictopts-' + label)
    st = g('apply', '--cached', R.canon_path(row), env=env); b = blob_in(env, row[5])
    print('  .opts row %s applied STRICT: rc %d -> %s (the READY: strict rc 128)' % (label, st[0], b[:12] if st[0] == 0 else '(no apply)'))
env = idx('ctrl'); ctl = g('apply', '--cached', '--check', Cdir + '/does-not-exist.diff', env=env); print('  nonexistent-patch control rc', ctl[0], '(128 expected)')
print('--- (d) THE DEVELOP MOVE')
print('  origin develop at fetch', DEVNOW[:9], 'UNMOVED' if DEVNOW == R.DEV else 'MOVED — the trees above are over the PIN; re-predict over the new tip is the generator\'s refusal case')
open(G + '/newdev_tree.txt', 'w').write('develop %s\ntree %s\nall11 %s\npair %s\npairblob %s\ncombinedCB %s\nunamended %s\nread %s\n' % (DEVNOW, tree_of(DEVNOW), A, t12, lstree(t12, R.PAIR_PATH)[1] if len(t12) == 40 else '?', cb, un, now()))
co_after = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects after:', co_after.replace('\n', ' '), '| byte-identical:', co_before == co_after)
print('scratch clone', CL, '| objects in the scratch clone (count-objects):', g('count-objects', '-v')[1].replace('\n', ' '))
print('done', now())
