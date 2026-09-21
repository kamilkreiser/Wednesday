#!/usr/bin/env python3
"""predict_batch_scratch_gate16B.py — every git WRITE verb of the gate16B drafter lives here, in a `git clone --shared --no-checkout` scratch clone
under the drafter's scratchpad (argv[1]); the Secuura checkout is only READ (count-objects before/after must be byte-identical).
(a) CANONICAL-PATCH IDENTITY with the --recount class: each of the 12 canonicals (the run patches — round16B) applied with `git apply --cached` into a
    TEMP INDEX read from develop 64ab10513 — strict `--check` rc, `-R --check` rc, `--recount --check` rc, `-R --recount --check` rc quoted; then the
    STRICT apply for real on the four TRUNCATION rows (KS-928 / KS-1133-B / KS-1181-F3 / KS-975-ITEM1: rc 0 and a SHORT file — the seat's F3 blobs
    e76b3e90db28 / e9dc6e3899f0 / 6250385ee49e / 1fcffe443b5c) beside the --recount apply (the RECOUNT blob == the head blob); the rc-128 row (KS-1158-R3:
    strict 128 `corrupt patch at line 100`, --recount rc 0); the five KS-1229 stages in forward / reverse / seed-16 shuffle -> ONE blob bbfcd0f98923 / 309
    lines with the four intermediate blobs; the per-PR tree by write-tree == the head tree; the all-12 tree in THREE orders == c54c1ae73ba3…; read-tree
    back to develop == 87b4aa12d2eb…; a nonexistent-patch control rc 128.
(b) THE HEADS (for every READY captured): each head alone over develop by REAL merge-tree --write-tree both orders == its head tree (fast-forward,
    parent IS develop); all eight heads chained in FOUR orders -> ONE tree == c54c1ae73ba3…; every PR path in ALL carries its head blob; each single
    tree != ALL; numstat from an empty repo rc 128.
(c) THE DEVELOP MOVE: if origin develop is not 64ab10513 the new tip is fetched BY SHA into THIS clone (never the checkout) over the checkout's own ssh
    road (its remote URL + repo-local core.sshCommand, read not printed — gate15's S1) and every tree is re-predicted over it; newdev_tree.txt is written
    in either case (the generator reads it).
Usage: predict_batch_scratch_gate16B.py <scratchpad dir>. Derived from gatesets/2026-09-21_gate15_docs_comments/predict_batch_scratch_gate15.py."""
import glob, hashlib, os, random, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16B as R; S = sys.argv[1]
REPO = R.REPO; DEV = R.DEV; DEV_TREE = R.DEV_TREE; SEAT_ALL = R.SEAT_ALL8
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate16B', now())
co_before = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
C = tempfile.mkdtemp(prefix='predict16B.', dir=S)
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
def lines_of(b): return g('cat-file', '-p', b)[1].count('\n') + (0 if g('cat-file', '-p', b)[1] == '' else 1) if b != 'ABSENT' else 0
def nlines(b):
    p = subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True); return p.stdout.count(b'\n')
print('--- (a) CANONICAL-PATCH IDENTITY at develop', DEV[:9], '(temp index per canonical; --cached into the scratch clone objects; EVERY apply --recount, the strict apply measured beside it)')
for p in R.PUSH:
    pr = R.PRS[p]
    for label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip in pr['canon']:
        patch = R.run_patch(rd); ex = os.path.exists(patch)
        env = idx('c-%s-%s' % (p, label))
        st = apply_check(env, patch); rv = apply_check(env, patch, '-R'); rcnt = apply_check(env, patch, '--recount'); rvr = apply_check(env, patch, '-R', '--recount')
        line = '  PR %-2s %-12s run %-34s exists %s sha16 %s | strict --check rc %d %s | -R --check rc %d | --recount --check rc %d | -R --recount rc %d' % (
            p, label, rd, ex, hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?', st[0], ('[' + (st[2].splitlines() or [''])[0][:60] + ']') if st[0] else '', rv[0], rcnt[0], rvr[0])
        if pr['mode'] == 'new':
            envs = idx('s-%s-%s' % (p, label)); sa = apply_real(envs, patch); sb = blob(envs, pr['file'])
            envr = idx('r-%s-%s' % (p, label)); ra = apply_real(envr, patch, '--recount'); rb = blob(envr, pr['file'])
            line += ' | STRICT APPLY rc %d -> blob %s / %s lines | RECOUNT APPLY rc %d -> blob %s / %d lines (RECOUNT column %s / %d: %s)' % (
                sa[0], sb[:12], nlines(sb) if sb != 'ABSENT' else '-', ra[0], rb[:12], nlines(rb) if rb != 'ABSENT' else 0, pr['blob'][:12], pr['lines'], rb == pr['blob'] and nlines(rb) == pr['lines'])
            if sblob: line += ' | the seat F3 STRICT blob %s / %d: %s' % (sblob, slines, sb.startswith(sblob) and nlines(sb) == slines)
            elif sa[0] == 0: line += ' | strict == recount: %s' % (sb == rb)
        print(line)
print('  CONTROL nonexistent patch: rc %d (want 128)' % apply_check(idx('ctrl-none'), C + '/nonexistent.diff')[0])
print('--- per-PR trees over develop by applying the canonicals --recount in GROUPING order (PR 5: forward, reverse, seed-16 shuffle)')
def apply_seq(env, seq, path):
    blobs = []
    for label, rd, *_ in seq:
        rc, o, e = apply_real(env, R.run_patch(rd), '--recount')
        if rc: return 'APPLY FAIL %s rc %d %s' % (label, rc, e[:80]), blobs
        blobs.append(blob(env, path))
    return g('write-tree', env=env)[1], blobs
PRTREE = {}
for p in R.PUSH:
    pr = R.PRS[p]; env = idx('pr-' + p); t, bl = apply_seq(env, pr['canon'], pr['file']); PRTREE[p] = t
    line = '  PR %-2s #%s %-16s tree %s == head tree %s: %s | final blob %s == RECOUNT %s: %s | lines %d (want %d)' % (p, pr['n'], pr['key'], t[:12], pr['tree'][:12], t == pr['tree'], bl[-1][:12], pr['blob'][:12], bl[-1] == pr['blob'], nlines(bl[-1]), pr['lines'])
    if len(pr['canon']) > 1:
        line += '\n      stage blobs %s == the READY\'s %s: %s' % ([b[:12] for b in bl], [b[:12] for b in pr['stage_blobs']], bl == pr['stage_blobs'])
        env2 = idx('pr-' + p + '-rev'); t2, bl2 = apply_seq(env2, list(reversed(pr['canon'])), pr['file'])
        rnd = random.Random(16); sq = pr['canon'][:]; rnd.shuffle(sq); env3 = idx('pr-' + p + '-shuf'); t3, bl3 = apply_seq(env3, sq, pr['file'])
        line += '\n      REVERSE order tree %s same %s | seed-16 shuffle %s tree %s same %s' % (t2[:12], t2 == t, [x[0] for x in sq], t3[:12], t3 == t)
    print(line)
print('--- the all-12 tree over develop by applying every canonical --recount: forward, exact reverse, seed-16 shuffle')
allseq = [(p, c) for p in R.PUSH for c in R.PRS[p]['canon']]
orders = [('forward', allseq), ('reverse', list(reversed(allseq)))]
rnd = random.Random(16); sh16 = allseq[:]; rnd.shuffle(sh16); orders.append(('seed-16 shuffle', sh16))
alls = []
for name, seq in orders:
    env = idx('all-' + name.replace(' ', ''))
    bad = None
    for p, (label, rd, *_) in seq:
        rc, o, e = apply_real(env, R.run_patch(rd), '--recount')
        if rc: bad = 'APPLY FAIL %s/%s rc %d %s' % (p, label, rc, e[:80]); break
    t = bad or g('write-tree', env=env)[1]; alls.append(t); print('  %-16s -> %s' % (name, t))
print('  all three identical: %s | == the seat eight-PR tree %s: %s' % (len(set(alls)) == 1, SEAT_ALL, alls[0] == SEAT_ALL))
if alls[0] == SEAT_ALL:
    print('  shortstat:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', SEAT_ALL)[1], '| name-status', sorted(l.split('\t')[0] for l in g('diff-tree', '-r', '--name-status', DEV + '^{tree}', SEAT_ALL)[1].splitlines()))
    print('  numstat:'); print(g('diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL)[1])
    for p in R.PUSH:
        b = g('rev-parse', SEAT_ALL + ':' + R.PRS[p]['file'])[1]; print('  ALL8:%s = %s == RECOUNT %s' % (R.PRS[p]['file'].split('/')[-1], b[:12], b == R.PRS[p]['blob']))
    print('  the HELD KS-1171 files ABSENT in the eight-PR tree:', [g('cat-file', '-e', SEAT_ALL + ':' + f)[0] != 0 for f in R.HELD['files']], '(want [True, True])')
    if g('cat-file', '-e', R.SEAT_ALL9 + '^{tree}')[0] == 0:
        print('  the nine-PR octopus tree %s IS in the shared store; diff vs the eight-PR tree:' % R.SEAT_ALL9[:12], sorted(l.split('\t')[-1] for l in g('diff-tree', '-r', '--name-status', SEAT_ALL, R.SEAT_ALL9)[1].splitlines()), '(want exactly KS-1171\'s two anchoring files)')
    else: print('  the nine-PR octopus tree', R.SEAT_ALL9[:12], 'is NOT in the shared store (the seat built it in s-b16-batch — its objects may be local to that worktree; not read)')
env = idx('ctrl-dev'); wt = g('write-tree', env=env)[1]; print('  CONTROL read-tree back to develop -> %s == %s %s' % (wt, DEV_TREE, wt == DEV_TREE))
print('--- (b) THE HEADS from the captured READYs, REAL 3-way merges')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(2), m.group(4))
present = [p for p in R.PUSH if p in READY]
print('heads from READYs (seat PR -> #PR key head):', {p: READY[p] for p in present})
H = {}
for p in present:
    h = READY[p][2]
    if h != R.PRS[p]['head']: print('PR', p, 'READY head', h[:9], '!= round16B', R.PRS[p]['head'][:9], '— REFUSING to use it'); continue
    if g('cat-file', '-e', h + '^{commit}')[0]: print('PR', p, h[:9], 'NOT in the object store — skipped'); continue
    H[p] = h
    a = g('merge-tree', '--write-tree', DEV, h); b = g('merge-tree', '--write-tree', h, DEV); ht = g('rev-parse', h + '^{tree}')[1]; par = g('rev-list', '--parents', '-n1', h)[1].split()[1:]
    print('PR %s #%s %s alone over DEV %s: fwd=%s rc=%d rev-same=%s head^{tree}=%s fast-forward(fwd==head tree)=%s parent==DEV %s | head tree == canonical-apply tree %s: %s' % (p, READY[p][0], h[:9], DEV[:9], a[1][:12], a[0], a[1] == b[1], ht[:12], a[1] == ht, par == [DEV], PRTREE[p][:12], ht == PRTREE[p]))
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
        t = chain(DEV, [H[p] for p in o]); results.append(t); print('order %-24s: %s' % (' '.join(o), t))
    ALLH = results[0]
    print('all orders identical:', len(set(results)) == 1, '| == the seat eight-PR tree %s: %s (%d present)' % (SEAT_ALL, ALLH == SEAT_ALL, len(present)))
    if 'CONFLICT' not in ALLH:
        for p in present:
            for path in g('diff', '--name-only', DEV, H[p])[1].splitlines():
                a = g('rev-parse', ALLH + ':' + path)[1]; c = g('rev-parse', H[p] + ':' + path)[1]
                if a != c: print('  MISMATCH PR %s %s ALL %s head %s' % (p, path, a, c))
        print('every PR path in ALL(present) carries its head blob (no MISMATCH line above = True)')
        for p in present: print('  PR %s head tree != ALL(present): %s' % (p, g('rev-parse', H[p] + '^{tree}')[1] != ALLH))
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
        mv = set(g('diff', '--name-only', DEV, CUR)[1].splitlines()); mine = {R.PRS[p]['file'] for p in R.PUSH}; tf = {x[0] for x in R.TAMPER_BLOBS}
        print('∩ the 8 paths:', sorted(mv & mine) or 'NONE', '| ∩ the 9 tamper files:', sorted(mv & tf) or 'NONE')
        PRTREE2 = {}
        for p in R.PUSH:
            env = idx('pr2-' + p, CUR); t, bl = apply_seq(env, R.PRS[p]['canon'], R.PRS[p]['file']); PRTREE2[p] = t
            print('  PR %-2s canonicals over the NEW develop -> tree %s (over the old %s)' % (p, t[:12], PRTREE[p][:12]))
        alls2 = []
        for name, seq in orders:
            env = idx('all2-' + name.replace(' ', ''), CUR)
            for p, (label, rd, *_) in seq: apply_real(env, R.run_patch(rd), '--recount')
            alls2.append(g('write-tree', env=env)[1])
        print('  all-12 over the NEW develop: %s | identical %s' % ([x[:12] for x in alls2], len(set(alls2)) == 1)); ALL2 = alls2[0]; NEWT = PRTREE2
        for p in present:
            a = g('merge-tree', '--write-tree', CUR, H[p]); b = g('merge-tree', '--write-tree', H[p], CUR)
            print('  PR %s head %s alone over NEW develop: fwd=%s rc=%d rev-same=%s | == canonical-apply-over-new %s: %s' % (p, H[p][:9], a[1][:12], a[0], a[1] == b[1], PRTREE2[p][:12], a[1] == PRTREE2[p]))
        if len(present) >= 2:
            r2 = [chain(CUR, [H[p] for p in o]) for o in orders_h]; print('  all-present heads over NEW develop in %d orders: %s | identical %s' % (len(r2), [x[:12] for x in r2], len(set(r2)) == 1))
        print('  compare per PR would read: merge_base %s ahead 1 behind %s' % (DEV[:9], g('rev-list', '--count', DEV + '..' + CUR)[1]))
open(os.path.join(G, 'newdev_tree.txt'), 'w').write('DEV_NOW %s\nTREE %s\nALL8_OVER_NEW %s\n' % (CUR, CT, ALL2) + '\n'.join('PR%s %s' % (p, NEWT[p]) for p in R.PUSH) + '\n')
print('newdev_tree.txt written (DEV_NOW %s, ALL8_OVER_NEW %s)' % (CUR[:9], ALL2[:12]))
E = tempfile.mkdtemp(prefix='empty16B.', dir=S); subprocess.run(['git', '-C', E, 'init', '--quiet'])
print('control: numstat from an empty repo rc=%d (want 128)' % sh(['git', '-C', E, 'diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL])[0])
co_after = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]
print('checkout count-objects after: ', co_after.replace('\n', ' '), '| byte-identical to before:', co_after == co_before)
print('checkout porcelain non-untracked (read):', sum(1 for l in sh(['git', '-C', REPO, 'status', '--porcelain'])[1].splitlines() if not l.startswith('??')), '| .git/worktrees:', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref:', len(sh(['git', '-C', REPO, 'for-each-ref'])[1].splitlines()))
print('scratch clone at', CL, '(left in the scratchpad, never deleted)'); print('done', now())
