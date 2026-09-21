#!/usr/bin/env python3
"""predict_batch_scratch_gate16C.py — every git WRITE verb of the gate16C drafter lives here, in a `git clone --shared --no-checkout` scratch clone
under the drafter's scratchpad (argv[1]); the Secuura checkout is only READ (count-objects before/after must be byte-identical).
(a) CANONICAL-PATCH IDENTITY with the --recount class: each of the 14 run patches (round16C) applied with `git apply --cached` into a TEMP INDEX read
    from develop 64ab10513 — strict `--check` rc, `-R --check` rc, `--recount --check` rc, `-R --recount --check` rc quoted; then the STRICT apply for
    real on every NEW-file row beside the --recount apply: the three TRUNCATION rows (KS-1185-F4 97 vs 108 · KS-1188-F2 97 vs 122 · KS-1193-F1 124 vs
    153 — the seat's strict blobs 4f68a823f31f / 686a707056af / 610c209861d1) and the rc-128 row (KS-864-F1009b strict 128 `corrupt patch at line 10`,
    --recount rc 0); KS-910's two SECTION files strict (either order -> one tree) and its patch.diff (strict rc 1, --recount rc 1 — the brief);
    the per-PR tree by write-tree == the head tree (KS-1188 forward / reverse / seed-16 shuffle; KS-1193 both orders); the all-15 (twelve-PR) tree
    in THREE orders == 4817a9c2ea23…; read-tree back to develop == 87b4aa12d2eb…; a nonexistent-patch control rc 128; the thirteen-PR tree
    48528fa3c355… read in the shared store (if present) differs from the twelve-PR tree on exactly the HELD KS-1123 file.
(b) THE HEADS (for every READY captured): each head alone over develop by REAL merge-tree --write-tree both orders == its head tree (fast-forward,
    parent IS develop); all twelve heads chained in FOUR orders -> ONE tree == 4817a9c2ea23…; every PR path in ALL carries its head blob; each single
    tree != ALL; numstat from an empty repo rc 128.
(c) THE DEVELOP MOVE: if origin develop is not 64ab10513 the new tip is fetched BY SHA into THIS clone (never the checkout) over the checkout's own ssh
    road (its remote URL + repo-local core.sshCommand, read not printed — gate15's S1) and every tree is re-predicted over it; newdev_tree.txt is written
    in either case (the generator reads it).
Usage: predict_batch_scratch_gate16C.py <scratchpad dir>. Derived from gatesets/2026-09-22_gate16B_seatB/predict_batch_scratch_gate16B.py."""
import glob, hashlib, os, random, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16C as R; S = sys.argv[1]
REPO = R.REPO; DEV = R.DEV; DEV_TREE = R.DEV_TREE; SEAT_ALL = R.SEAT_ALL12
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate16C', now())
co_before = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
C = tempfile.mkdtemp(prefix='predict16C.', dir=S)
rc, o, e = sh(['git', 'clone', '--quiet', '--shared', '--no-checkout', REPO, C + '/clone']); print('clone rc=%d %s at %s' % (rc, e[:100], C))
CL = C + '/clone'
def g(*a, env=None): return sh(['git', '-C', CL] + list(a), env=env)
print('develop tree:', g('rev-parse', DEV + '^{tree}')[1], '==', DEV_TREE, g('rev-parse', DEV + '^{tree}')[1] == DEV_TREE)
def idx(name, base=DEV):
    env = dict(os.environ, GIT_INDEX_FILE=C + '/idx-' + name); g('read-tree', base, env=env); return env
def apply_check(env, patch, *flags): return g('apply', '--cached', '--check', *flags, patch, env=env)
def apply_real(env, patch, *flags): return g('apply', '--cached', *flags, patch, env=env)
def blob(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
def nlines(b):
    if b == 'ABSENT': return 0
    p = subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True); return p.stdout.count(b'\n')
def flags_for(row): return () if row[1].startswith('section_') else ('--recount',)
print('--- (a) CANONICAL-PATCH IDENTITY at develop', DEV[:9], '(temp index per canonical; --cached into the scratch clone objects; EVERY run patch --recount, the strict apply measured beside it; KS-910 sections strict)')
for p in R.PUSH:
    pr = R.PRS[p]
    for f in pr['files']:
        for row in f['canon']:
            label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip = row
            patch = R.canon_path(row); ex = os.path.exists(patch)
            env = idx('c-%s-%s' % (p, label))
            st = apply_check(env, patch); rv = apply_check(env, patch, '-R'); rcnt = apply_check(env, patch, '--recount'); rvr = apply_check(env, patch, '-R', '--recount')
            line = '  PR %-2s %-18s %-34s exists %s sha16 %s | strict --check rc %d %s | -R --check rc %d | --recount --check rc %d | -R --recount rc %d' % (
                p, label, rd, ex, hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?', st[0], ('[' + (st[2].splitlines() or [''])[0][:60] + ']') if st[0] else '', rv[0], rcnt[0], rvr[0])
            envs = idx('s-%s-%s' % (p, label)); sa = apply_real(envs, patch); sb = blob(envs, f['path'])
            envr = idx('r-%s-%s' % (p, label)); ra = apply_real(envr, patch, *flags_for(row)); rb = blob(envr, f['path'])
            line += ' | STRICT APPLY rc %d -> blob %s / %s lines | %s APPLY rc %d -> blob %s / %d lines (RECOUNT column %s / %d: %s)' % (
                sa[0], sb[:12], nlines(sb) if sb != 'ABSENT' else '-', 'RECOUNT' if flags_for(row) else 'SECTION', ra[0], rb[:12], nlines(rb), f['blob'][:12], f['lines'], rb == f['blob'] and nlines(rb) == f['lines'] if len(f['canon']) == 1 else 'n/a (one of %d rows)' % len(f['canon']))
            if sblob: line += ' | the seat STRICT blob %s / %d: %s' % (sblob, slines, sb.startswith(sblob) and nlines(sb) == slines)
            elif sa[0] == 0: line += ' | strict == recount: %s' % (sb == rb)
            print(line)
k910 = R.run_patch(R.KS910_RUN); e1 = idx('k910-patchdiff'); s910 = apply_check(e1, k910); r910 = apply_check(e1, k910, '--recount')
print('  KS-910 patch.diff (the READY fence, %s): strict --check rc %d %s | --recount --check rc %d %s (the brief: neither applies — the section files are the canonical)' % (R.KS910_FENCE16, s910[0], '[' + (s910[2].splitlines() or [''])[0][:70] + ']', r910[0], '[' + (r910[2].splitlines() or [''])[0][:70] + ']'))
print('  CONTROL nonexistent patch: rc %d (want 128)' % apply_check(idx('ctrl-none'), C + '/nonexistent.diff')[0])
print('--- per-PR trees over develop by applying the canonicals (run patches --recount, sections strict) in GROUPING order; multi-file PRs in every order')
def apply_seq(env, seq):
    blobs = []
    for f, row in seq:
        rc, o, e = apply_real(env, R.canon_path(row), *flags_for(row))
        if rc: return 'APPLY FAIL %s rc %d %s' % (row[0], rc, e[:80]), blobs
        blobs.append((f['path'].split('/')[-1], blob(env, f['path'])))
    return g('write-tree', env=env)[1], blobs
PRTREE = {}
for p in R.PUSH:
    pr = R.PRS[p]; seq = [(f, row) for f in pr['files'] for row in f['canon']]
    env = idx('pr-' + p); t, bl = apply_seq(env, seq); PRTREE[p] = t
    ok_blobs = all(b == f['blob'] and nlines(b) == f['lines'] for f in pr['files'] for n_, b in bl if n_ == f['path'].split('/')[-1])
    line = '  PR %-2s #%s %-8s tree %s == head tree %s: %s | final blobs == RECOUNT + lines (%d files): %s' % (p, pr['n'], pr['key'], t[:12], pr['tree'][:12], t == pr['tree'], len(pr['files']), ok_blobs)
    if len(seq) > 1:
        env2 = idx('pr-' + p + '-rev'); t2, _ = apply_seq(env2, list(reversed(seq)))
        line += '\n      REVERSE order tree %s same %s' % (t2[:12], t2 == t)
        if len(seq) > 2:
            rnd = random.Random(16); sq = seq[:]; rnd.shuffle(sq); env3 = idx('pr-' + p + '-shuf'); t3, _ = apply_seq(env3, sq)
            line += ' | seed-16 shuffle %s tree %s same %s' % ([x[1][0] for x in sq], t3[:12], t3 == t)
    print(line)
print('--- the all-15 (twelve-PR) tree over develop by applying every canonical: forward, exact reverse, seed-16 shuffle')
allseq = [(f, row) for p in R.PUSH for f in R.PRS[p]['files'] for row in f['canon']]
orders = [('forward', allseq), ('reverse', list(reversed(allseq)))]
rnd = random.Random(16); sh16 = allseq[:]; rnd.shuffle(sh16); orders.append(('seed-16 shuffle', sh16))
alls = []
for name, seq in orders:
    env = idx('all-' + name.replace(' ', '')); t, _ = apply_seq(env, seq); alls.append(t); print('  %-16s -> %s' % (name, t))
print('  all three identical: %s | == the seat twelve-PR tree %s: %s' % (len(set(alls)) == 1, SEAT_ALL, alls[0] == SEAT_ALL))
if alls[0] == SEAT_ALL:
    print('  shortstat:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', SEAT_ALL)[1], '| name-status', sorted(l.split('\t')[0] for l in g('diff-tree', '-r', '--name-status', DEV + '^{tree}', SEAT_ALL)[1].splitlines()))
    print('  numstat:'); print(g('diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL)[1])
    for p in R.PUSH:
        for f in R.PRS[p]['files']:
            b = g('rev-parse', SEAT_ALL + ':' + f['path'])[1]; print('  ALL12:%-70s = %s == RECOUNT %s' % (f['path'].split('/')[-1], b[:12], b == f['blob']))
    print('  the HELD KS-1123 file ABSENT in the twelve-PR tree:', g('cat-file', '-e', SEAT_ALL + ':' + R.HELD['file'])[0] != 0, '(want True)')
    if g('cat-file', '-e', R.SEAT_ALL13 + '^{tree}')[0] == 0:
        print('  the thirteen-PR batch tree %s IS in the shared store; diff vs the twelve-PR tree:' % R.SEAT_ALL13[:12], sorted(l.split('\t')[-1].split('/')[-1] for l in g('diff-tree', '-r', '--name-status', SEAT_ALL, R.SEAT_ALL13)[1].splitlines()), "(want exactly KS-1123's one file)", '| shortstat over develop:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', R.SEAT_ALL13)[1])
    else: print('  the thirteen-PR batch tree', R.SEAT_ALL13[:12], 'is NOT in the shared store (the seat built it in s-c16-batch — its objects may be local to that worktree; not read)')
env = idx('ctrl-dev'); wt = g('write-tree', env=env)[1]; print('  CONTROL read-tree back to develop -> %s == %s %s' % (wt, DEV_TREE, wt == DEV_TREE))
print('--- (b) THE HEADS from the captured READYs, REAL 3-way merges')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(2), m.group(4))
present = [p for p in R.PUSH if p in READY]
print('heads from READYs (seat PR -> #PR key head):', {p: READY[p] for p in present})
H = {}
for p in present:
    h = READY[p][2]
    if h != R.PRS[p]['head']: print('PR', p, 'READY head', h[:9], '!= round16C', R.PRS[p]['head'][:9], '— REFUSING to use it'); continue
    if g('cat-file', '-e', h + '^{commit}')[0]: print('PR', p, h[:9], 'NOT in the object store — skipped'); continue
    H[p] = h
    a = g('merge-tree', '--write-tree', DEV, h); b = g('merge-tree', '--write-tree', h, DEV); ht = g('rev-parse', h + '^{tree}')[1]; par = g('rev-list', '--parents', '-n1', h)[1].split()[1:]
    print('PR %-2s #%s %s alone over DEV %s: fwd=%s rc=%d rev-same=%s head^{tree}=%s fast-forward(fwd==head tree)=%s parent==DEV %s | head tree == canonical-apply tree %s: %s' % (p, READY[p][0], h[:9], DEV[:9], a[1][:12], a[0], a[1] == b[1], ht[:12], a[1] == ht, par == [DEV], PRTREE[p][:12], ht == PRTREE[p]))
present = [p for p in present if p in H]
def mk(tree, parent): return g('commit-tree', tree, '-p', parent, '-m', 'scratch')[1]
def chain(base, heads):
    cur = base; t = ''
    for h in heads:
        rc, t, e = g('merge-tree', '--write-tree', cur, h)
        if rc: return 'CONFLICT rc=%d at %s: %s' % (rc, h[:9], (t + ' ' + e)[:200])
        cur = mk(t, base)
    return t
orders_h = []
if len(present) >= 2:
    orders_h = [present, list(reversed(present))]; rnd = random.Random(16)
    for i in range(2):
        o = present[:]; rnd.shuffle(o); orders_h.append(o)
    results = []
    for o in orders_h:
        t = chain(DEV, [H[p] for p in o]); results.append(t); print('order %-36s: %s' % (' '.join(o), t))
    ALLH = results[0]
    print('all orders identical:', len(set(results)) == 1, '| == the seat twelve-PR tree %s: %s (%d present)' % (SEAT_ALL, ALLH == SEAT_ALL, len(present)))
    if 'CONFLICT' not in ALLH:
        for p in present:
            for path in g('diff', '--name-only', DEV, H[p])[1].splitlines():
                a = g('rev-parse', ALLH + ':' + path)[1]; c = g('rev-parse', H[p] + ':' + path)[1]
                if a != c: print('  MISMATCH PR %s %s ALL %s head %s' % (p, path, a, c))
        print('every PR path in ALL(present) carries its head blob (no MISMATCH line above = True)')
        for p in present: print('  PR %-2s head tree != ALL(present): %s' % (p, g('rev-parse', H[p] + '^{tree}')[1] != ALLH))
        print('  ALL(present) shortstat:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', ALLH)[1])
else: print('fewer than two heads present — the chain is a fast-forward; orders need two heads')
CUR = sh(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'])[1].split()[0]
print('--- (c) origin develop NOW', CUR, '| the heads parent', DEV[:9], '| moved:', CUR != DEV)
NEWT = {p: (PRTREE[p] if p in PRTREE else '?') for p in R.PUSH}; ALL2 = alls[0]; CT = DEV_TREE
if CUR != DEV:
    url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]; sshc = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
    rc, o, e = sh(['git', '-C', CL, '-c', 'core.sshCommand=' + sshc, 'fetch', '--quiet', url, CUR])
    print('fetch by SHA over ssh (the checkout remote URL + its repo-local core.sshCommand, read not printed) into the scratch clone rc=%d %s | object present now: %s' % (rc, e[:120], g('cat-file', '-e', CUR + '^{commit}')[0] == 0))
    if g('cat-file', '-e', CUR + '^{commit}')[0] == 0:
        CT = g('rev-parse', CUR + '^{tree}')[1]; print('new develop tree', CT, '| rev-list --count %s..%s = %s | merge-base with the heads parent = %s' % (DEV[:9], CUR[:9], g('rev-list', '--count', DEV + '..' + CUR)[1], g('merge-base', DEV, CUR)[1][:12]))
        print('move name-status:'); print(g('diff', '--name-status', DEV, CUR)[1]); print('move shortstat:', g('diff', '--shortstat', DEV, CUR)[1])
        mv = set(g('diff', '--name-only', DEV, CUR)[1].splitlines()); mine = set(R.all_paths()); tf = {x[0] for x in R.TAMPER_BLOBS}
        print('∩ the 16 paths:', sorted(mv & mine) or 'NONE', '| ∩ the 8 tamper files:', sorted(mv & tf) or 'NONE')
        PRTREE2 = {}
        for p in R.PUSH:
            env = idx('pr2-' + p, CUR); t, bl = apply_seq(env, [(f, row) for f in R.PRS[p]['files'] for row in f['canon']]); PRTREE2[p] = t
            print('  PR %-2s canonicals over the NEW develop -> tree %s (over the old %s)' % (p, t[:12], PRTREE[p][:12]))
        alls2 = []
        for name, seq in orders:
            env = idx('all2-' + name.replace(' ', ''), CUR); t, _ = apply_seq(env, seq); alls2.append(t)
        print('  all-15 over the NEW develop: %s | identical %s' % ([x[:12] for x in alls2], len(set(alls2)) == 1)); ALL2 = alls2[0]; NEWT = PRTREE2
        for p in present:
            a = g('merge-tree', '--write-tree', CUR, H[p]); b = g('merge-tree', '--write-tree', H[p], CUR)
            print('  PR %s head %s alone over NEW develop: fwd=%s rc=%d rev-same=%s | == canonical-apply-over-new %s: %s' % (p, H[p][:9], a[1][:12], a[0], a[1] == b[1], PRTREE2[p][:12], a[1] == PRTREE2[p]))
        if len(present) >= 2:
            r2 = [chain(CUR, [H[p] for p in o]) for o in orders_h]; print('  all-present heads over NEW develop in %d orders: %s | identical %s' % (len(r2), [x[:12] for x in r2], len(set(r2)) == 1))
        print('  compare per PR would read: merge_base %s ahead 1 behind %s' % (DEV[:9], g('rev-list', '--count', DEV + '..' + CUR)[1]))
open(os.path.join(G, 'newdev_tree.txt'), 'w').write('DEV_NOW %s\nTREE %s\nALL12_OVER_NEW %s\n' % (CUR, CT, ALL2) + '\n'.join('PR%s %s' % (p, NEWT[p]) for p in R.PUSH) + '\n')
print('newdev_tree.txt written (DEV_NOW %s, ALL12_OVER_NEW %s)' % (CUR[:9], ALL2[:12]))
E = tempfile.mkdtemp(prefix='empty16C.', dir=S); subprocess.run(['git', '-C', E, 'init', '--quiet'])
print('control: numstat from an empty repo rc=%d (want 128)' % sh(['git', '-C', E, 'diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL])[0])
co_after = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]
print('checkout count-objects after: ', co_after.replace('\n', ' '), '| byte-identical to before:', co_after == co_before)
print('checkout porcelain non-untracked (read):', sum(1 for l in sh(['git', '-C', REPO, 'status', '--porcelain'])[1].splitlines() if not l.startswith('??')), '| .git/worktrees:', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref:', len(sh(['git', '-C', REPO, 'for-each-ref'])[1].splitlines()))
print('scratch clone at', CL, '(left in the scratchpad, never deleted)'); print('done', now())
