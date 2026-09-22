#!/usr/bin/env python3
r"""predict_batch_scratch_gate18B.py — EVERY git WRITE verb of the gate18B drafter lives here, in ONE `git clone --shared --no-checkout` scratch clone
under the drafter's scratchpad (argv[1]) with a TEMP INDEX per step AND a TEMP OBJECT DIRECTORY (GIT_OBJECT_DIRECTORY inside the scratch dir; the
clone's own objects + the shared store reachable as alternates) — the Secuura checkout is only READ. THE CWD GUARD (Seat C 18th's S1: its
measure18.py run 1 ran `merge-tree` with cwd defaulted to the shared checkout and wrote 17 loose objects into the shared store; the seat's F1):
this script's FIRST act after the clone is to chdir INTO the scratch clone and ASSERT (i) os.getcwd() == the clone path, (ii) the clone path is
under argv[1] (the scratchpad), (iii) `git rev-parse --absolute-git-dir` from that cwd names the clone's .git (never the checkout's), (iv)
GIT_OBJECT_DIRECTORY is set for every write and points under the scratch dir — and REFUSES (rc 2) otherwise; every git call also passes `-C <clone>`.
`count-objects -v` on the checkout is read before and after and must be byte-identical (both copies saved beside the .out as
checkout_counts_predict_{before,after}.txt).
(a) CANONICAL-PATCH IDENTITY (strict this round — the seat's Q5; no `.opts` carries an option): each of the 8 apply units (6 run patches + KS-1265's
    two section files) applied `git apply --cached` into a temp index read from the PARENT 3916eacd1 — strict `--check` rc, `-R --check` rc,
    `--recount --check` rc quoted; the STRICT apply for real -> blob + line count == the head blob; the `--recount` apply -> the SAME blob (no
    truncation row this round: measured, not assumed); per-PR tree by write-tree == the head tree (KS-1265: test section then product AND the
    reverse; KS-1171: 8J-TSFIX then GUARD3S-TSFIX and the reverse); the all-7 (8 units) tree over PARENT in THREE orders == a36532029483…; read-tree
    back to PARENT == 4b573853be61…; a nonexistent-patch control rc 128.
(b) THE HEADS over PARENT: each head alone by REAL merge-tree --write-tree both orders == its head tree (fast-forward: parent IS PARENT); all seven
    chained in FOUR orders -> ONE tree == a36532029483…; every PR path in ALL carries its head blob; each single tree != ALL; numstat from an
    empty repo rc 128; the seat's octopus 5185c65cf read (its tree == ALL).
(c) THE #1036 MOVE and THE END_TREE over develop 8c2f7b3fd (THE LOAD-BEARING MEASUREMENT of this gate — the commission's item 3): `git diff
    --name-only 3916eacd1 8c2f7b3fd` (50 paths) saved to p1036_paths.out; ∩ the 9 PR paths = ∅ and ∩ the 4 tamper files = ∅ by set arithmetic;
    each head alone over develop by REAL 3-way merge-tree (base = PARENT) both orders -> ONE tree per PR (the per-PR MERGED tree the addendum
    must carry — NOT the head tree: develop moved); every one of its 9 (well, that PR's) paths at the head blob and every one of the 50 moved
    paths at develop's blob; all seven chained over develop in FOUR orders -> ONE sha = THE END_TREE; the 8 canonicals applied over develop in
    THREE orders -> the same sha; ALL_OVER_DEV != ALL_OVER_PARENT (by construction: the 50 moved paths); diff-tree ALL_OVER_PARENT..ALL_OVER_DEV
    name-only == exactly the 50 moved paths; ALL_OVER_DEV's 9 PR paths == the head blobs; ALL_OVER_DEV's 50 moved paths == develop's blobs.
(d) origin develop is RE-READ (`git ls-remote`, read-only in the checkout) — if it is no longer 8c2f7b3fd (Seat C 18th's six merges on a separate
    GO), the new tip is fetched BY SHA into THIS clone (never the checkout) over the checkout's own ssh road (its remote URL + repo-local
    core.sshCommand, read not printed) and (c) is repeated over it; newdev_tree.txt is written in either case (the generator reads it).
Usage: predict_batch_scratch_gate18B.py <scratchpad dir>. Derived from gatesets/2026-09-22_gate18C_seatC/predict_batch_scratch_gate18C.py."""
import glob, hashlib, os, random, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18B as R; S = os.path.abspath(sys.argv[1])
REPO = R.REPO; P = R.PARENT; PT = R.PARENT_TREE; DEV = R.DEV; DEV_TREE = R.DEV_TREE; SEAT_ALL = R.SEAT_ALL7
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate18B', now(), '| scratchpad', S)
assert os.path.isdir(S) and '/scratchpad' in S and not S.startswith(REPO), 'argv[1] must be the session scratchpad'
co_before = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; open(os.path.join(G, 'checkout_counts_predict_before.txt'), 'w').write(now() + '\n' + co_before + '\n')
print('checkout count-objects before:', co_before.replace('\n', ' '))
C = tempfile.mkdtemp(prefix='predict18B.', dir=S)
rc, o, e = sh(['git', 'clone', '--quiet', '--shared', '--no-checkout', REPO, C + '/clone']); print('clone rc=%d %s at %s' % (rc, e[:100], C))
if rc: sys.exit(1)
CL = C + '/clone'; OBJ = C + '/objtmp'; os.makedirs(OBJ, exist_ok=True)
# ---- THE CWD GUARD: a script has no memory of a sentence; it asserts its own cwd ----
os.chdir(CL)
cwd = os.getcwd()
gd = sh(['git', 'rev-parse', '--absolute-git-dir'])[1]   # deliberately WITHOUT -C: this is the reading a defaulted cwd would give
guard = dict(cwd_is_clone=(os.path.realpath(cwd) == os.path.realpath(CL)), clone_under_scratchpad=os.path.realpath(CL).startswith(os.path.realpath(S) + '/'),
             gitdir_is_clone=(os.path.realpath(gd) == os.path.realpath(CL + '/.git')), gitdir_not_checkout=(not os.path.realpath(gd).startswith(os.path.realpath(REPO))),
             objdir_under_scratch=os.path.realpath(OBJ).startswith(os.path.realpath(S) + '/'))
print('CWD GUARD:', guard)
if not all(guard.values()): print('REFUSING: the cwd / git-dir / object-dir guard failed — no write verb runs'); sys.exit(2)
BASE_ENV = dict(os.environ, GIT_OBJECT_DIRECTORY=OBJ, GIT_ALTERNATE_OBJECT_DIRECTORIES=CL + '/.git/objects')   # every new object lands in objtmp; reads chain objtmp -> the clone's objects -> (alternates) the shared store
def g(*a, env=None):
    e_ = env or BASE_ENV; assert e_.get('GIT_OBJECT_DIRECTORY', '').startswith(os.path.realpath(S)) or e_['GIT_OBJECT_DIRECTORY'].startswith(S), 'GIT_OBJECT_DIRECTORY not under the scratchpad'
    return sh(['git', '-C', CL] + list(a), env=e_)
print('temp object dir', OBJ, '| alternates chain: the clone objects ->', open(CL + '/.git/objects/info/alternates').read().strip()[:80])
print('PARENT tree:', g('rev-parse', P + '^{tree}')[1], '==', PT, g('rev-parse', P + '^{tree}')[1] == PT, '| develop tree:', g('rev-parse', DEV + '^{tree}')[1][:12], '==', DEV_TREE[:12], g('rev-parse', DEV + '^{tree}')[1] == DEV_TREE)
def idx(name, base=P):
    env = dict(BASE_ENV, GIT_INDEX_FILE=C + '/idx-' + name); g('read-tree', base, env=env); return env
def apply_check(env, patch, *flags): return g('apply', '--cached', '--check', *flags, patch, env=env)
def apply_real(env, patch, *flags): return g('apply', '--cached', *flags, patch, env=env)
def blob(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
def nlines(b):
    if b == 'ABSENT': return 0
    p = subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True, env=BASE_ENV); return p.stdout.count(b'\n')
print('--- (a) CANONICAL-PATCH IDENTITY at PARENT', P[:9], '(temp index per unit; --cached into the temp object dir; strict everywhere)')
for p in R.PUSH:
    pr = R.PRS[p]
    for f in pr['files']:
        for row in f['canon']:
            label, rd, fn, sha16, opts, adds, dels, hunk = row
            patch = R.canon_path(row); ex = os.path.exists(patch)
            env = idx('c-%s-%s' % (p, label))
            st = apply_check(env, patch); rv = apply_check(env, patch, '-R'); rcnt = apply_check(env, patch, '--recount')
            line = '  PR %-2s %-14s %-34s %-14s exists %s sha16 %s | strict --check rc %d %s | -R --check rc %d | --recount --check rc %d' % (
                p, label, rd, fn, ex, hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?', st[0], ('[' + (st[2].splitlines() or [''])[0][:60] + ']') if st[0] else '', rv[0], rcnt[0])
            envs = idx('s-%s-%s' % (p, label)); sa = apply_real(envs, patch); sb = blob(envs, f['path'])
            line += ' | STRICT APPLY rc %d -> blob %s / %d lines == head blob %s / %d: %s' % (sa[0], sb[:12], nlines(sb), f['blob'][:12], f['lines'], sb == f['blob'] and nlines(sb) == f['lines'])
            envr = idx('r-%s-%s' % (p, label)); ra = apply_real(envr, patch, '--recount'); rb = blob(envr, f['path'])
            line += ' | --recount APPLY rc %d -> blob %s == strict: %s (a no-op)' % (ra[0], rb[:12], rb == sb)
            print(line)
print('  CONTROL nonexistent patch: rc %d (want 128)' % apply_check(idx('ctrl-none'), C + '/nonexistent.diff')[0])
print('--- per-PR trees over PARENT by applying the canonicals (strict; KS-1265 test-then-product AND product-then-test; KS-1171 both orders)')
def apply_seq(env, seq):
    blobs = []
    for f, row in seq:
        rc, o, e = apply_real(env, R.canon_path(row))
        if rc: return 'APPLY FAIL %s rc %d %s' % (row[0], rc, e[:80]), blobs
        blobs.append((f['path'], blob(env, f['path'])))
    return g('write-tree', env=env)[1], blobs
PRTREE = {}
for p in R.PUSH:
    pr = R.PRS[p]; seq = [(f, row) for f in pr['files'] for row in f['canon']]
    env = idx('pr-' + p); t, bl = apply_seq(env, seq); PRTREE[p] = t
    ok_blobs = all(b == f['blob'] and nlines(b) == f['lines'] for f in pr['files'] for pth, b in bl if pth == f['path'])
    line = '  PR %-2s #%s %-8s tree %s == head tree %s: %s | final blobs == head + lines (%d files): %s' % (p, pr['n'], pr['key'], t[:12], pr['tree'][:12], t == pr['tree'], len(pr['files']), ok_blobs)
    if len(seq) > 1:
        env2 = idx('pr-' + p + '-rev'); t2, _ = apply_seq(env2, list(reversed(seq))); line += ' | REVERSE order tree %s same %s' % (t2[:12], t2 == t)
    print(line)
print('--- the all-7 (8 units) tree over PARENT by applying every canonical: forward, exact reverse, seed-18 shuffle')
allseq = [(f, row) for p in R.PUSH for f in R.PRS[p]['files'] for row in f['canon']]
orders = [('forward', allseq), ('reverse', list(reversed(allseq)))]
rnd = random.Random(18); sh18 = allseq[:]; rnd.shuffle(sh18); orders.append(('seed-18 shuffle', sh18))
alls = []
for name, seq in orders:
    env = idx('all-' + name.replace(' ', '')); t, bl = apply_seq(env, seq); alls.append(t); print('  %-16s -> %s' % (name, t))
print('  all three identical: %s | == the seat all-7 tree %s: %s' % (len(set(alls)) == 1, SEAT_ALL, alls[0] == SEAT_ALL))
ALL_P = alls[0]
if ALL_P == SEAT_ALL:
    print('  shortstat:', g('diff-tree', '-r', '--shortstat', P + '^{tree}', SEAT_ALL)[1], '(seat: %s)' % R.SEAT_ALL7_SHORTSTAT, '| name-status', sorted(l.split('\t')[0] for l in g('diff-tree', '-r', '--name-status', P + '^{tree}', SEAT_ALL)[1].splitlines()))
    print('  numstat:'); print(g('diff-tree', '-r', '--numstat', P + '^{tree}', SEAT_ALL)[1])
    for p in R.PUSH:
        for f in R.PRS[p]['files']:
            b = g('rev-parse', SEAT_ALL + ':' + f['path'])[1]; print('  ALL7:%-95s = %s == head blob %s' % (f['path'].replace(R.D, ''), b[:12], b == f['blob']))
env = idx('ctrl-parent'); wt = g('write-tree', env=env)[1]; print('  CONTROL read-tree back to PARENT -> %s == %s %s' % (wt, PT, wt == PT))
print('--- (b) THE HEADS from the captured READYs, REAL 3-way merges over PARENT')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(2), m.group(4))
present = [p for p in R.PUSH if p in READY]
print('heads from READYs (seat PR -> #PR key head):', {p: READY[p] for p in present})
H = {}
for p in present:
    h = READY[p][2]
    if h != R.PRS[p]['head']: print('PR', p, 'READY head', h[:9], '!= round18B', R.PRS[p]['head'][:9], '— REFUSING to use it'); continue
    if g('cat-file', '-e', h + '^{commit}')[0]: print('PR', p, h[:9], 'NOT in the object store — skipped'); continue
    H[p] = h
    a = g('merge-tree', '--write-tree', P, h); b = g('merge-tree', '--write-tree', h, P); ht = g('rev-parse', h + '^{tree}')[1]; par = g('rev-list', '--parents', '-n1', h)[1].split()[1:]
    print('PR %-2s #%s %s alone over PARENT: fwd=%s rc=%d rev-same=%s head^{tree}=%s fast-forward(fwd==head tree)=%s parent==PARENT %s | head tree == canonical-apply tree %s: %s' % (p, READY[p][0], h[:9], a[1][:12], a[0], a[1] == b[1], ht[:12], a[1] == ht, par == [P], PRTREE[p][:12], ht == PRTREE[p]))
present = [p for p in present if p in H]
def mk(tree, parent): return g('commit-tree', tree, '-p', parent, '-m', 'scratch')[1]
def chain(base, heads):
    cur = base; t = ''
    for h in heads:
        rc, t, e = g('merge-tree', '--write-tree', cur, h)
        if rc: return 'CONFLICT rc=%d at %s: %s' % (rc, h[:9], (t + ' ' + e)[:200])
        cur = mk(t, base)
    return t
orders_h = [present, list(reversed(present))]; rnd = random.Random(18)
for i in range(2):
    o = present[:]; rnd.shuffle(o); orders_h.append(o)
results = [chain(P, [H[p] for p in o]) for o in orders_h]
for o, t in zip(orders_h, results): print('order %-20s over PARENT: %s' % (' '.join(o), t))
ALLH = results[0]
print('all four orders identical:', len(set(results)) == 1, '| == the seat all-7 tree %s: %s (%d present)' % (SEAT_ALL, ALLH == SEAT_ALL, len(present)))
if 'CONFLICT' not in ALLH:
    mism = [(p, path) for p in present for path in g('diff', '--name-only', P, H[p])[1].splitlines() if g('rev-parse', ALLH + ':' + path)[1] != g('rev-parse', H[p] + ':' + path)[1]]
    print('every PR path in ALL(PARENT) carries its head blob: %s %s' % (not mism, mism or ''))
    for p in present: print('  PR %-2s head tree != ALL: %s' % (p, g('rev-parse', H[p] + '^{tree}')[1] != ALLH))
print('  the seat octopus %s in the shared store: %s | its tree == ALL: %s | parents %d' % (R.SEAT_OCTOPUS, g('cat-file', '-e', R.SEAT_OCTOPUS + '^{commit}')[0] == 0, g('rev-parse', R.SEAT_OCTOPUS + '^{tree}')[1] == ALLH, len(g('rev-list', '--parents', '-n1', R.SEAT_OCTOPUS)[1].split()) - 1))
# ---- (c) THE #1036 MOVE + THE END_TREE over develop ----
def predict_over(base, label):
    bt = g('rev-parse', base + '^{tree}')[1]
    mv = g('diff', '--name-only', P, base)[1].splitlines()
    open(os.path.join(G, 'p1036_paths%s.out' % label), 'w').write('# git diff --name-only %s %s  (%s)\n' % (P, base, now()) + '\n'.join(mv) + '\n')
    mine = set(R.all_paths()); tf = {x[0] for x in R.TAMPER_BLOBS}
    print('--- (c%s) THE MOVE %s -> %s: %d paths (saved p1036_paths%s.out) | shortstat %s | ∩ the 9 PR paths: %s | ∩ the 4 tamper files: %s | ∩ the lane package.json / lock files: %s' % (
        label, P[:9], base[:9], len(mv), label, g('diff', '--shortstat', P, base)[1], sorted(set(mv) & mine) or 'NONE (∅)', sorted(set(mv) & tf) or 'NONE (∅)',
        [x.replace(R.D, '') for x in mv if x in (R.OR + 'package.json', R.AN + 'package.json', R.AU + 'package.json', R.SH + 'package.json', R.OR + 'package-lock.json', R.AN + 'package-lock.json', R.AU + 'package-lock.json', R.SH + 'package-lock.json', R.D + 'package.json', R.D + 'package-lock.json')]))
    PR2 = {}
    for p in present:
        a = g('merge-tree', '--write-tree', base, H[p]); b = g('merge-tree', '--write-tree', H[p], base); PR2[p] = a[1]
        ok_paths = all(g('rev-parse', a[1] + ':' + f['path'])[1] == f['blob'] for f in R.PRS[p]['files'])
        ok_mv = all(g('rev-parse', a[1] + ':' + x)[1] == g('rev-parse', base + ':' + x)[1] for x in mv)
        print('  PR %-2s #%s head %s MERGED over %s (3-way, base %s): tree %s rc %d | both orders same %s | != head tree %s | its %d path(s) at the head blob(s): %s | the %d moved paths at %s\'s blobs: %s' % (
            p, READY[p][0], H[p][:9], base[:9], P[:9], a[1], a[0], a[1] == b[1], a[1] != R.PRS[p]['tree'], len(R.PRS[p]['files']), ok_paths, len(mv), base[:9], ok_mv))
    r2 = [chain(base, [H[p] for p in o]) for o in orders_h]
    for o, t in zip(orders_h, r2): print('  order %-20s over %s: %s' % (' '.join(o), base[:9], t))
    END = r2[0]; print('  all four orders identical: %s -> THE END_TREE over %s = %s' % (len(set(r2)) == 1, base[:9], END))
    alls2 = []
    for name, seq in orders:
        env = idx('all2%s-' % label + name.replace(' ', ''), base); t, _ = apply_seq(env, seq); alls2.append(t)
    print('  the 8 canonicals applied over %s in three orders: %s | identical %s | == the merged END_TREE: %s' % (base[:9], [x[:12] for x in alls2], len(set(alls2)) == 1, alls2[0] == END))
    if 'CONFLICT' not in END:
        dn = g('diff-tree', '-r', '--name-only', ALLH, END)[1].splitlines()
        print('  END_TREE != ALL_OVER_PARENT: %s | diff-tree ALL_OVER_PARENT..END_TREE name-only: %d paths == the moved set: %s' % (END != ALLH, len(dn), sorted(dn) == sorted(mv)))
        print('  END_TREE: the 9 PR paths at the head blobs: %s | the %d moved paths at %s\'s blobs: %s | shortstat vs %s: %s | shortstat vs PARENT: %s' % (
            all(g('rev-parse', END + ':' + f['path'])[1] == f['blob'] for p in present for f in R.PRS[p]['files']), len(mv), base[:9], all(g('rev-parse', END + ':' + x)[1] == g('rev-parse', base + ':' + x)[1] for x in mv),
            base[:9], g('diff-tree', '-r', '--shortstat', base + '^{tree}', END)[1], g('diff-tree', '-r', '--shortstat', P + '^{tree}', END)[1]))
        print('  a numstat of END_TREE OUTSIDE the temp objdir (the shared store; read-only) rc=%d (want 128 — nothing of this reached the shared store)' % sh(['git', '-C', REPO, 'diff-tree', '-r', '--numstat', base + '^{tree}', END])[0])
    return END, PR2, bt
END_DEV, PR2_DEV, DT = predict_over(DEV, '')
# ---- (d) origin develop NOW ----
CUR = sh(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'])[1].split()[0]
print('--- (d) origin develop NOW', CUR, now(), '| the pin', DEV[:9], '| moved since the pin:', CUR != DEV)
NEWT = PR2_DEV; ALL2 = END_DEV; CT = DT; DEV_NOW = DEV
if CUR != DEV:
    url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]; sshc = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
    rc, o, e = sh(['git', '-C', CL, '-c', 'core.sshCommand=' + sshc, 'fetch', '--quiet', url, CUR], env=BASE_ENV)
    print('fetch by SHA over ssh (the checkout remote URL + its repo-local core.sshCommand, read not printed) into the scratch clone temp object dir rc=%d %s | object present now: %s' % (rc, e[:120], g('cat-file', '-e', CUR + '^{commit}')[0] == 0))
    if g('cat-file', '-e', CUR + '^{commit}')[0] == 0:
        print('new develop tree', g('rev-parse', CUR + '^{tree}')[1], '| rev-list --count %s..%s = %s | first-parent %s | merge-base with PARENT = %s' % (DEV[:9], CUR[:9], g('rev-list', '--count', DEV + '..' + CUR)[1], g('rev-list', '--count', '--first-parent', DEV + '..' + CUR)[1], g('merge-base', P, CUR)[1][:12]))
        print('move 8c2f7b3fd -> new name-status:'); print(g('diff', '--name-status', DEV, CUR)[1])
        ALL2, NEWT, CT = predict_over(CUR, '_newdev'); DEV_NOW = CUR
open(os.path.join(G, 'newdev_tree.txt'), 'w').write('DEV_NOW %s\nTREE %s\nALL7_OVER_NEW %s\nALL7_OVER_PARENT %s\nALL7_OVER_8c2f7b3fd %s\n' % (DEV_NOW, CT, ALL2, ALLH, END_DEV) + '\n'.join('PR%s %s' % (p, NEWT.get(p, '?')) for p in R.PUSH) + '\n')
print('newdev_tree.txt written (DEV_NOW %s, ALL7_OVER_NEW %s, ALL7_OVER_PARENT %s)' % (DEV_NOW[:9], ALL2[:12], ALLH[:12]))
E = tempfile.mkdtemp(prefix='empty18B.', dir=S); subprocess.run(['git', '-C', E, 'init', '--quiet'])
print('control: numstat from an empty repo rc=%d (want 128)' % sh(['git', '-C', E, 'diff-tree', '-r', '--numstat', P + '^{tree}', SEAT_ALL])[0])
print('temp object dir objects written:', sum(len(fs) for _, _, fs in os.walk(OBJ)), '| the clone own objects dir (not the shared store):', sum(len(fs) for _, _, fs in os.walk(CL + '/.git/objects')))
co_after = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; open(os.path.join(G, 'checkout_counts_predict_after.txt'), 'w').write(now() + '\n' + co_after + '\n')
print('checkout count-objects after: ', co_after.replace('\n', ' '), '| byte-identical to before:', co_after == co_before)
print('checkout porcelain non-untracked (read):', sum(1 for l in sh(['git', '-C', REPO, 'status', '--porcelain'])[1].splitlines() if not l.startswith('??')), '| .git/worktrees:', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref:', len(sh(['git', '-C', REPO, 'for-each-ref'])[1].splitlines()))
print('scratch clone at', CL, '(left in the scratchpad, never deleted)'); print('done', now())
