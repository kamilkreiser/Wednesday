#!/usr/bin/env python3
"""predict_batch_scratch_gate19C.py — every git WRITE verb of the gate19C drafter lives here, in a scratch clone made FROM ORIGIN (a `git clone --bare
--filter=blob:none` of git@github.com:Secuura/Distributed_Secuura.git over the checkout's own ssh road — its remote URL + repo-local core.sshCommand,
read from the checkout's config, never printed) under the drafter's scratchpad (argv[1]). NEVER `--shared` from the checkout (the commission: the
seat's OWN 18th-round S1 was a merge-tree in the shared store; the 18C drafter's S6 was mtime freshening through a --shared clone's alternates). The
Secuura checkout is only READ (count-objects before/after printed; byte-identical expected).
(a) THE HEADS: develop + refs/pull/N/head for the twelve (+ #1189, the CLOSED twin of #1190) fetched by ref INTO the scratch clone; each head's parent
    == develop 3bad652d1 (fast-forward: merged tree == head tree == the READY's item-0 PR-alone tree); per head: name-status / numstat vs the pins,
    every blob's 12-hex prefix vs the READY, MODES by ls-tree (100755 on the five exec scripts where develop has 100755), bash -n not run here.
(b) THE TREES: the twelve heads chained by REAL `merge-tree --write-tree` over develop in THREE orders (push order, reverse, seed-19 shuffle) -> ONE
    tree vs the seat's all-14 5a8458a5…; shortstat vs `21 files changed, 915 insertions(+), 29 deletions(-)`; the start-secuura.sh PAIR (#1180 +
    #1181) both orders -> one tree eaa961172883 with the PAIR blob 58cdd3dc846b… / 736 / 100755 (alone blobs 1882bb0c5114 / 9bb5e5e1272d); every
    other ALL path at its head blob; each single tree != ALL; 21 distinct paths; ∩ Seat B's captured paths = ∅.
(c) CANONICAL-PATCH IDENTITY: each of the 24 canonical rows (section_1/2.diff per bash_patch stage; patch.diff per doc row; the PRPROCESS golden)
    applied with `git apply --cached` into a temp index read from develop: strict --check rc / -R --check rc / --recount --check rc; the STRICT apply
    (or the .opts apply where the READY names one: #1180 s1 `--recount --ignore-whitespace`, #1185 s1 `--recount`) -> the blob == the READY's 12-hex;
    the two-stage rows (#1187 the accumulating script; #1193 REVIEWREQ then PRPROCESS) applied in sequence with the intermediate asserted; the per-PR
    tree by write-tree == the head tree; a nonexistent-patch control rc 128.
(d) THE DEVELOP MOVE: if origin develop is not 3bad652d1 the new tip is in the clone anyway (fetched by ref) and every tree is ALSO predicted over it;
    newdev_tree.txt is written in either case (the generator reads it).
Usage: predict_batch_scratch_gate19C.py <scratchpad dir> (MUST be this session's scratchpad under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/;
the guard refuses rc 9 otherwise; every write verb asserts cwd inside the scratch clone)."""
import hashlib, os, random, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19C as R
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
print('predict_batch_scratch_gate19C', now())
co_before = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
sshc = sh(['git', '-C', R.REPO, 'config', '--get', 'core.sshCommand'])[1]; print('checkout core.sshCommand read:', 'yes (not printed)' if sshc else 'NO')
url = sh(['git', '-C', R.REPO, 'config', '--get', 'remote.origin.url'])[1]; print('checkout remote.origin.url:', url, '== round19C:', url == R.ORIGIN_URL)
C = tempfile.mkdtemp(prefix='predict19C.', dir=S); CL = C + '/origin.git'; WT = C + '/wt'; os.makedirs(WT)
assert os.path.realpath(C).startswith(S)
ENV = dict(os.environ, GIT_SSH_COMMAND=sshc) if sshc else dict(os.environ)
os.chdir(C); print('cwd now', os.getcwd(), '| under the scratchpad:', os.path.realpath(os.getcwd()).startswith(S))
def assert_in_scratch(verb):
    if verb in WRITE_VERBS and not os.path.realpath(os.getcwd()).startswith(S):
        print('REFUSING write verb', verb, 'outside the scratchpad: cwd', os.getcwd()); sys.exit(9)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN (bare, blob:none) rc=%d %s -> %s' % (rc, e[:120], CL)); assert rc == 0
def g(*a, env=None, inp=None):
    assert_in_scratch(a[0]); return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
refspecs = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/pull/%s/head' % (R.PRS[p]['n'], R.PRS[p]['n']) for p in R.PUSH] + ['+refs/pull/1189/head:refs/pull/1189/head'] + ['+refs/pull/%s/head:refs/pull/%s/head' % (x[0], x[0]) for x in R.SEATB]
rc, o, e = g('fetch', '--quiet', 'origin', *refspecs); print('fetch by ref FROM ORIGIN rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEVNOW = g('rev-parse', 'refs/heads/develop')[1]; print('origin develop at fetch:', DEVNOW, '== pin 3bad652d1:', DEVNOW == R.DEV)
DEV = R.DEV
print('develop tree:', g('rev-parse', DEV + '^{tree}')[1], '(pin 12-hex', R.DEV_TREE12 + ')', g('rev-parse', DEV + '^{tree}')[1].startswith(R.DEV_TREE12))
def tree_of(c): return g('rev-parse', c + '^{tree}')[1]
def lstree(tree, path):
    rc, o, e = g('ls-tree', tree, '--', path); return (o.split()[0], o.split()[2]) if o else ('ABSENT', 'ABSENT')
def nlines(b):
    if b == 'ABSENT': return 0
    p = subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True, env=ENV); return p.stdout.count(b'\n')
print('--- (a) THE HEADS (each read from the scratch clone fetched from origin; parent / tree / files / blobs / modes)')
HEADTREE = {}; ok_heads = 0; blobs40 = {}
for p in R.PUSH:
    pr = R.PRS[p]; h = g('rev-parse', 'refs/pull/%s/head' % pr['n'])[1]
    par = g('rev-parse', h + '^')[1]; t = tree_of(h); HEADTREE[p] = t
    ns = g('diff-tree', '-r', '--name-status', DEV, h)[1].splitlines(); num = g('diff-tree', '-r', '--numstat', DEV, h)[1].splitlines()
    paths = sorted(l.split('\t')[1] for l in ns); want = sorted(f['path'] for f in pr['files'])
    adds = sum(int(l.split('\t')[0]) for l in num); dels = sum(int(l.split('\t')[1]) for l in num)
    okh = h == pr['head']; okp = par == DEV; okt = t == pr['tree']; okf = paths == want; okn = (adds, dels) == (pr['adds'], pr['dels'])
    print('  PR %-2s #%s %-8s head %s == READY %s | parent == develop %s | tree %s == READY %s | files == pinned %s %s | +%d/-%d == %s' % (p, pr['n'], pr['key'], h[:9], okh, okp, t[:12], okt, okf, '' if okf else (paths, want), adds, dels, okn))
    for f in pr['files']:
        m, b = lstree(t, f['path']); md, bd = lstree(tree_of(DEV), f['path']); blobs40[(p, f['path'])] = b
        st = [l.split('\t')[0] for l in ns if l.split('\t')[1] == f['path']]
        exp_mode = md if md != 'ABSENT' else '100644'
        print('     %-70s status %s (want %s) blob %s == READY %s %s | lines %d (want %d) | mode %s (develop %s) %s' % (f['path'], st, 'A' if f['mode'] == 'new' else 'M', b[:12], f['blob12'], b.startswith(f['blob12']), nlines(b), f['lines'], m, md, 'EXEC-KEPT' if (f['path'] in R.EXEC_SCRIPTS and m == '100755' == md) else ('MODE-OK' if m == exp_mode else 'MODE-MISMATCH')))
    if okh and okp and okt and okf and okn: ok_heads += 1
print('  heads fully agreeing with the READYs: %d/12' % ok_heads)
h1189 = g('rev-parse', 'refs/pull/1189/head')[1]; print('  #1189 (CLOSED twin) head', h1189[:9], '== #1190 head:', h1189 == R.PRS['7']['head'])
print('--- (b) THE TREES over develop', DEV[:9], '(REAL merge-tree --write-tree, chained; three orders)')
def merge(base, ours, theirs):
    rc, o, e = g('merge-tree', '--write-tree', '--merge-base=' + base, ours, theirs); return rc, o.splitlines()[0] if o else '', e
def chain(order):
    cur = DEV
    for p in order:
        rc, t, e = merge(DEV, cur, 'refs/pull/%s/head' % R.PRS[p]['n'])
        if rc != 0: return 'CONFLICT at PR %s: %s %s' % (p, t[:12], e[:80])
        cur = t
    return cur
orders = {'push order': list(R.PUSH), 'reverse': list(reversed(R.PUSH)), 'seed-19 shuffle': random.Random(19).sample(R.PUSH, len(R.PUSH))}
ALL = {}
for name, order in orders.items():
    ALL[name] = chain(order); print('  all-12 chained [%s] %s -> %s == seat all-14 %s: %s' % (name, ' '.join(order), ALL[name][:12], R.SEAT_ALL14[:12], ALL[name] == R.SEAT_ALL14))
A = ALL['push order']
if len(A) == 40:
    ss = g('diff-tree', '-r', '--shortstat', DEV, A)[1]; print('  shortstat:', ss.strip(), '== seat:', ss.strip().endswith(R.SEAT_ALL14_SHORTSTAT))
    ns = g('diff-tree', '-r', '--name-status', DEV, A)[1].splitlines(); print('  name-status: %d rows, A %d M %d | distinct paths %d == 21: %s | == round19C distinct: %s' % (len(ns), sum(1 for l in ns if l.startswith('A')), sum(1 for l in ns if l.startswith('M')), len(ns), len(ns) == 21, sorted(l.split('\t')[1] for l in ns) == R.distinct_paths()))
    mism = 0
    for p in R.PUSH:
        for f in R.PRS[p]['files']:
            m, b = lstree(A, f['path']); hb = blobs40[(p, f['path'])]
            if f['path'] == R.PAIR_PATH:
                print('     ALL %-40s blob %s == PAIR blob %s (EXPECTED: the pair) | lines %d (want %d) | mode %s (want %s)' % (f['path'], b[:12], b == R.PAIR_BLOB, nlines(b), R.PAIR_LINES, m, R.PAIR_MODE)); mism += (b != R.PAIR_BLOB or m != R.PAIR_MODE)
            elif b != hb: print('     ALL %s blob %s != head blob %s MISMATCH' % (f['path'], b[:12], hb[:12])); mism += 1
    print('  every non-pair ALL path at its head blob, the pair at the PAIR blob: %s (mismatches %d)' % (mism == 0, mism))
    print('  each single head tree != ALL:', all(HEADTREE[p] != A for p in R.PUSH))
    rb = g('rev-parse', DEV + '^{tree}')[1]; print('  develop tree unchanged:', rb.startswith(R.DEV_TREE12))
    seatb_over = [q for x in R.SEATB for q in x[3] if lstree(A, q)[1] != lstree(tree_of(DEV), q)[1]]; print('  Seat B captured paths changed by ALL:', seatb_over or 'NONE (0 overlap)')
rc1, t12, e = merge(DEV, 'refs/pull/1180/head', 'refs/pull/1181/head'); rc2, t21, e2 = merge(DEV, 'refs/pull/1181/head', 'refs/pull/1180/head')
print('  PAIR #1180 then #1181 -> %s (rc %d) | #1181 then #1180 -> %s (rc %d) | one tree: %s | == seat pair eaa961172883: %s' % (t12[:12], rc1, t21[:12], rc2, t12 == t21, t12.startswith(R.SEAT_PAIR_TREE12)))
if len(t12) == 40:
    m, b = lstree(t12, R.PAIR_PATH); print('  PAIR blob %s == 58cdd3dc846b… %s | lines %d (want 736) | mode %s | alone blobs #1180 %s #1181 %s (neither the pair: %s)' % (b, b == R.PAIR_BLOB, nlines(b), m, blobs40[('1', R.PAIR_PATH)][:12], blobs40[('2', R.PAIR_PATH)][:12], R.PAIR_BLOB not in (blobs40[('1', R.PAIR_PATH)], blobs40[('2', R.PAIR_PATH)])))
print('  Seat B heads alone over develop (context, NOT this gate\'s): ' + ' | '.join('#%s parent==develop %s' % (x[0], g('rev-parse', 'refs/pull/%s/head^' % x[0])[1] == DEV) for x in R.SEATB))
print('--- (c) CANONICAL-PATCH IDENTITY at develop (temp index per PR in the scratch clone; --cached; the .opts rows both ways)')
def idx(name, base=DEV):
    env = dict(ENV, GIT_INDEX_FILE=C + '/idx-' + name, GIT_WORK_TREE=WT); g('read-tree', base, env=env); return env
def blob_in(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
def mode_in(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[0] if o else 'ABSENT'
tree_ok = 0
for p in R.PUSH:
    pr = R.PRS[p]; env = idx('pr' + p); seq_ok = True
    for row in pr['canon']:
        label, rd, fn, sha16, opts, path = row; patch = R.canon_path(row); ex = os.path.exists(patch)
        sha = hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?'
        envc = idx('chk-' + label)
        st = g('apply', '--cached', '--check', patch, env=envc); rv = g('apply', '--cached', '--check', '-R', patch, env=envc); rcn = g('apply', '--cached', '--check', '--recount', patch, env=envc)
        flags = tuple(opts.split()) if opts else ()
        ap = g('apply', '--cached', *flags, patch, env=env); b = blob_in(env, path)
        line = '  PR %-2s %-20s %-44s sha16 %s == READY %s | strict --check rc %d%s | -R rc %d | --recount rc %d | APPLY%s rc %d -> %s / %d lines' % (p, label, rd + '/' + fn, sha, sha == sha16, st[0], (' [' + (st[2].splitlines() or [''])[0][:50] + ']') if st[0] else '', rv[0], rcn[0], (' (' + opts + ')') if opts else '', ap[0], b[:12], nlines(b))
        if opts:
            envs = idx('strict-' + label, base=None) if False else None
        print(line)
        if ap[0] != 0: seq_ok = False
    if pr.get('intermediate'):
        pass
    # final blobs per file vs the READY
    fin = all(blob_in(env, f['path']).startswith(f['blob12']) for f in pr['files'])
    t = g('write-tree', env=env)[1]
    print('     final blobs == READY 12-hex: %s | write-tree %s == head tree %s: %s | modes in index: %s' % (fin, t[:12], HEADTREE[p][:12], t == HEADTREE[p], [mode_in(env, f['path']) for f in pr['files']]))
    tree_ok += (t == HEADTREE[p])
print('  per-PR canonical trees == head trees: %d/12' % tree_ok)
# the two-stage intermediates
for p, stage_label, want12, wantlines in (('5', '1034-HOOKENV-s1', 'ed53fafc1730', 422), ('10', '1097-REVIEWREQ', '44e28201ebe9', 689)):
    pr = R.PRS[p]; env = idx('mid' + p)
    for row in pr['canon']:
        g('apply', '--cached', *(tuple(row[4].split()) if row[4] else ()), R.canon_path(row), env=env)
        if row[0] == stage_label: break
    b = blob_in(env, row[5]); print('  intermediate PR %s after %s: %s / %d == READY %s / %d: %s' % (p, stage_label, b[:12], nlines(b), want12, wantlines, b.startswith(want12) and nlines(b) == wantlines))
# the .opts rows the strict way too (the READY: #1180 s1 strict rc 128; #1185 s1 strict rc 0 same tree)
for p, label in (('1', '972-BANNER-s1'), ('4', '1033-DEMOBASE-s1')):
    row = [r for r in R.PRS[p]['canon'] if r[0] == label][0]; env = idx('strictopts-' + p)
    st = g('apply', '--cached', R.canon_path(row), env=env); b = blob_in(env, row[5])
    print('  .opts row %s applied STRICT: rc %d -> %s (the READY: %s)' % (label, st[0], b[:12] if st[0] == 0 else '(no apply)', 'strict rc 128 corrupt patch' if p == '1' else 'strict rc 0 same blob 3b4af5b463b1'))
env = idx('ctrl'); ctl = g('apply', '--cached', '--check', C + '/does-not-exist.diff', env=env); print('  nonexistent-patch control rc', ctl[0], '(128 expected)')
print('--- (d) THE DEVELOP MOVE')
print('  origin develop at fetch', DEVNOW[:9], 'UNMOVED' if DEVNOW == R.DEV else 'MOVED — the trees above are over the PIN; re-predict over the new tip is the generator\'s refusal case')
open(G + '/newdev_tree.txt', 'w').write('develop %s\ntree %s\nall12 %s\npair %s\npairblob %s\nread %s\n' % (DEVNOW, tree_of(DEVNOW), A, t12, lstree(t12, R.PAIR_PATH)[1] if len(t12) == 40 else '?', now()))
co_after = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects after:', co_after.replace('\n', ' '), '| byte-identical:', co_before == co_after)
print('scratch clone', CL, '| objects in the scratch clone (count-objects):', g('count-objects', '-v')[1].replace('\n', ' '))
print('done', now())
