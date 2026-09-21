#!/usr/bin/env python3
"""predict_batch_scratch_1130.py — re-derive each Seat B 14th PR's merged tree over develop 9f0265eb0 (each head's parent IS develop: fast-forward,
merge-tree = head tree) and the all-N tree by REAL 3-way merges (merge-tree --write-tree chained through scratch commit-trees) in a --shared
--no-checkout scratch clone under the drafter's scratchpad; git write verbs THERE only — the Secuura checkout is only READ (count-objects before/after
must be byte-identical). Heads come from the captured READYs (mail_seatB14_ready*_pr<N>_*.md). Orders: the push order (1 2 6 3 5 4 as present), its
exact reverse, and four seeded shuffles; the PR 3 + PR 5 same-file pair both orders when both are present; controls: read-tree back to develop,
each single tree != ALL, every PR path in ALL carries its head blob (the shared ks869 file: the pair blob), numstat from an empty repo rc 128.
Usage: predict_batch_scratch_1130.py <scratchpad dir>. Derived from gatesets/2026-09-21_gate1119to1128/predict_batch_scratch.sh."""
import glob, os, random, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); S = sys.argv[1]
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '9f0265eb06ecf24d4de18149ce862ad2330a61ee'; DEV_TREE = '23d60cace7c37bc329ccc425e58659e950089a4d'
SEAT_ALL = '60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'; SEAT_PAIR35 = '9e5dec6aef2070de26d1450c961f531572ee8f57'; SEAT_PAIR35_BLOB = 'dcd3efaaf45a26bb4324b656ef62e79685462600'
SEAT_FOUR = '6eeef3623e8a71801a67e1fee10925abcee1cc72'
PUSH = ['1', '2', '6', '3', '5', '4']
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_1130', now())
co_before = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB14_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(2), m.group(4))
present = [p for p in PUSH if p in READY]
print('heads from READYs (seat PR -> #PR key head):', {p: READY[p] for p in present})
C = tempfile.mkdtemp(prefix='predict1130.', dir=S)
rc, o, e = sh(['git', 'clone', '--quiet', '--shared', '--no-checkout', REPO, C + '/clone']); print('clone rc=%d %s' % (rc, e[:100]))
def g(*a): return sh(['git', '-C', C + '/clone'] + list(a))
print('develop tree:', g('rev-parse', DEV + '^{tree}')[1], '==', DEV_TREE)
H = {p: READY[p][2] for p in present}
for p in present:
    h = H[p]
    if g('cat-file', '-e', h + '^{commit}')[0]: print('PR', p, h[:9], 'NOT in the object store — skipped'); present.remove(p); continue
    a = g('merge-tree', '--write-tree', DEV, h); b = g('merge-tree', '--write-tree', h, DEV); ht = g('rev-parse', h + '^{tree}')[1]
    print('PR %s #%s %s alone over DEV 9f0265eb0: fwd=%s rc=%d rev=%s rc=%d head^{tree}=%s fast-forward(fwd==head tree)=%s same-both-orders=%s' % (p, READY[p][0], h[:9], a[1], a[0], b[1], b[0], ht, a[1] == ht, a[1] == b[1]))
def mk(tree, parent): return g('commit-tree', tree, '-p', parent, '-m', 'scratch')[1]
def chain(base, heads):
    cur = base; t = ''
    for h in heads:
        rc, t, e = g('merge-tree', '--write-tree', cur, h)
        if rc: return 'CONFLICT rc=%d at %s: %s' % (rc, h[:9], (t + ' ' + e)[:200])
        cur = mk(t, base)
    return t
orders = [present, list(reversed(present))]
rnd = random.Random(1130)
for i in range(4):
    o = present[:]; rnd.shuffle(o)
    while o in orders and len(present) > 2: rnd.shuffle(o)
    orders.append(o)
print('--- all %d present over 9f0265eb0 (seat all-six tree %s; all-four %s)' % (len(present), SEAT_ALL, SEAT_FOUR))
results = []
for o in orders:
    t = chain(DEV, [H[p] for p in o]); results.append(t); print('order %-14s: %s' % (' '.join(o), t))
ALL = results[0]
print('all orders identical:', len(set(results)) == 1, '| == seat all-six %s: %s | == seat all-four %s: %s' % (SEAT_ALL, ALL == SEAT_ALL, SEAT_FOUR, ALL == SEAT_FOUR))
if '3' in present and '5' in present:
    p35 = chain(DEV, [H['3'], H['5']]); p53 = chain(DEV, [H['5'], H['3']])
    b35 = g('rev-parse', p35 + ':Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts')[1] if 'CONFLICT' not in p35 else '?'
    print('--- PR 3 + PR 5 (same file, disjoint hunks): 3->5 %s | 5->3 %s | same %s | == seat pair tree %s: %s | ks869 blob %s == seat pair blob %s: %s' % (p35, p53, p35 == p53, SEAT_PAIR35, p35 == SEAT_PAIR35, b35, SEAT_PAIR35_BLOB, b35 == SEAT_PAIR35_BLOB))
if all(p in present for p in ['1', '2', '3', '4']):
    f4 = chain(DEV, [H['1'], H['2'], H['3'], H['4']]); f4r = chain(DEV, [H['4'], H['3'], H['2'], H['1']])
    print('--- the FOUR (1 2 3 4) without the candidates: %s | reverse %s | == brief all-four %s: %s' % (f4, f4r, SEAT_FOUR, f4 == f4r == SEAT_FOUR))
env = dict(os.environ, GIT_INDEX_FILE=C + '/idx-dev'); subprocess.run(['git', '-C', C + '/clone', 'read-tree', DEV], env=env, capture_output=True)
wt = subprocess.run(['git', '-C', C + '/clone', 'write-tree'], env=env, capture_output=True, text=True).stdout.strip()
print('control read-tree back to 9f0265eb0 ->', wt, '==', DEV_TREE, wt == DEV_TREE)
if 'CONFLICT' not in ALL:
    print('--- ALL tree vs DEV numstat:'); print(g('diff-tree', '-r', '--numstat', DEV + '^{tree}', ALL)[1])
    ns = g('diff-tree', '-r', '--name-status', DEV + '^{tree}', ALL)[1].splitlines()
    print('count %d | name-status %s | shortstat: %s' % (len(ns), sorted(l.split('\t')[0] for l in ns), g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', ALL)[1]))
    shared = 'Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts'
    for p in present:
        for path in g('diff', '--name-only', DEV, H[p])[1].splitlines():
            a = g('rev-parse', ALL + ':' + path)[1]; c = g('rev-parse', H[p] + ':' + path)[1]
            if path == shared and '3' in present and '5' in present: print('  PR %s %s: ALL blob %s (the pair blob; head blob %s) == seat pair blob: %s' % (p, path.split('/')[-1], a[:12], c[:12], a == SEAT_PAIR35_BLOB))
            elif a != c: print('  MISMATCH PR %s %s ALL %s head %s' % (p, path, a, c))
    print('every single-owner PR path in ALL carries its head blob (no MISMATCH line above = True)')
    for p in present: print('  PR %s head tree != ALL: %s' % (p, g('rev-parse', H[p] + '^{tree}')[1] != ALL))
    E = tempfile.mkdtemp(prefix='empty1130.', dir=S); subprocess.run(['git', '-C', E, 'init', '--quiet'])
    print('control: numstat from an empty repo rc=%d (want 128)' % sh(['git', '-C', E, 'diff-tree', '-r', '--numstat', DEV + '^{tree}', ALL])[0])
co_after = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]
print('checkout count-objects after: ', co_after.replace('\n', ' '), '| byte-identical to before:', co_after == co_before)
print('checkout porcelain non-untracked (read):', sum(1 for l in sh(['git', '-C', REPO, 'status', '--porcelain'])[1].splitlines() if not l.startswith('??')), '| .git/worktrees:', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref:', len(sh(['git', '-C', REPO, 'for-each-ref'])[1].splitlines()))
print('scratch clone at', C, '(left in the scratchpad, never deleted)'); print('done', now())
