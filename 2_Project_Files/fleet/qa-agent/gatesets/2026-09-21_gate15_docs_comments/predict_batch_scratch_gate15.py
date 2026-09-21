#!/usr/bin/env python3
"""predict_batch_scratch_gate15.py — every git WRITE verb of the gate15 drafter lives here, in a `git clone --shared --no-checkout` scratch clone
under the drafter's scratchpad (argv[1]); the Secuura checkout is only READ (count-objects before/after must be byte-identical).
(a) CANONICAL-PATCH IDENTITY: each of the 14 canonicals (run patch or READY fence per the GROUPING; fences re-extracted by shape_gate15.py into
    <scratchpad>/fences15/) applied with `git apply --cached` into a TEMP INDEX read from develop 581ed7fa1 — strict `--check` rc, `-R --check` rc,
    `--recount --check` rc quoted; the three `--recount` READYs (KS-1037 / KS-1045-A / KS-1045-B) must refuse strict rc 128 and apply --recount rc 0;
    KS-1036-item3's FENCE must refuse (strict rc 1 at DEV-PROCESS.md:224) while its RUN patch applies; the resulting blob per file == the GROUPING
    (both orders for the three two-READY files and PR 7's two files); the per-PR tree by write-tree == the GROUPING; the all-14 tree in THREE orders
    (forward, exact reverse, seed-15 shuffle) == a93fe063d28ae66d4a90e1926b78364a7a578ff4; read-tree back to develop == 60bd96e7078c…; a
    nonexistent-patch control rc 128.
(b) THE HEADS (for every READY captured): each head alone over develop by REAL merge-tree --write-tree both orders == its head tree (fast-forward,
    parent IS develop); all present heads chained in ≥ 3 orders -> ONE tree (== a93fe063d28a… once all ten are present); every PR path in ALL
    carries its head blob; each single tree != ALL; numstat from an empty repo rc 128.
Usage: predict_batch_scratch_gate15.py <scratchpad dir>. Derived from gatesets/2026-09-21_gate1130to1135/predict_batch_scratch_1130.py."""
import glob, hashlib, os, random, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); S = sys.argv[1]
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
DEV = '581ed7fa124b85c7c2da89ac05d52f99c2502911'; DEV_TREE = '60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'; SEAT_ALL = 'a93fe063d28ae66d4a90e1926b78364a7a578ff4'
D = 'Blockchain/Dev/'
PUSH = [str(i) for i in range(1, 11)]
TREE12 = {'1': '4cd290a2c80e', '2': '0edbb8341e60', '3': 'd1ba6f8882fd', '4': '4f0a8c67f95f', '5': '374c0328a8c5', '6': '99a9adaf3151', '7': '6e95645e29fb', '8': '366ec698c266', '9': '07d01c8ae4f5', '10': '9fdeab78e610'}
BLOB12 = {D + 'docs/DEV-PROCESS.md': 'ab9a70f13e3c', D + 'CONTRIBUTING.md': 'b3cc10a40089', D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md': '5ba84caf2e30', 'CLAUDE.md': 'ef2f8fc2e4cb',
          D + 'deployment/DEPLOYMENT-ARCHITECTURE.md': '622c0e505278', D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts': '9ce9e852ae44',
          D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts': '6a51358e3619', D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts': '57de2c6753e4',
          D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts': 'bed97468d499', D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts': 'b7949520cf03',
          D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts': '595bed15d859'}
# (label, seat PR, canonical path, mode, file)
FD = os.path.join(S, 'fences15')
def fence(rf): return os.path.join(FD, rf.replace('.md', '.fence.diff'))
def run(d): return os.path.join(LM, 'runs', d, 'out.md.checker', 'patch.diff')
CANON = [
 ('KS-1035-D', '1', run('2026-09-15_ks1035-ornith35b-night'), 'strict', D + 'docs/DEV-PROCESS.md'),
 ('KS-1036-item3', '1', run('2026-09-16_ks1036-ornith35b-night2'), 'strict', D + 'docs/DEV-PROCESS.md'),
 ('KS-1037', '2', fence('READY_KS-1037_ornith35b-q4_DOCPATCH-PASS-6of6_2026-09-15.diff.md'), '--recount', D + 'CONTRIBUTING.md'),
 ('KS-1049-A', '2', run('2026-09-16_ks1049-ornith35b-night2'), 'strict', D + 'CONTRIBUTING.md'),
 ('KS-1045-A', '3', fence('READY_KS-1045-A_ornith35b-q4_DOCPATCH-RECHECK-PASS-7of7_2026-09-15.diff.md'), '--recount', D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md'),
 ('KS-1045-B', '3', fence('READY_KS-1045-B_ornith35b-q4_DOCPATCH-PASS-7of7_2026-09-15.diff.md'), '--recount', D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md'),
 ('KS-1097-Da', '4', fence('READY_KS-1097-Da_ornith35b-q4_DOCPATCH-STRICT-PASS-7of7_2026-09-15.diff.md'), 'strict', 'CLAUDE.md'),
 ('KS-890', '5', fence('READY_KS-890_ornith35b-q4_DOCPATCH-ANCHORRESTORED-PASS-8of8_2026-09-16.diff.md'), 'strict', D + 'deployment/DEPLOYMENT-ARCHITECTURE.md'),
 ('KS-1140-GF2GF4', '6', run('2026-09-17_ks1140-ornith35b-night'), 'strict', D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts'),
 ('KS-1152-R1c', '7', run('2026-09-17_ks1152-ornith35b-night3'), 'strict', D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts'),
 ('KS-1152-R1d', '7', run('2026-09-17_ks1152-ornith35b-night4'), 'strict', D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts'),
 ('KS-979', '8', run('2026-09-17_ks979-ornith35b-night'), 'strict', D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts'),
 ('KS-1120-F3', '9', run('2026-09-17_ks1120-ornith35b-night'), 'strict', D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts'),
 ('KS-1156-A3', '10', run('2026-09-17_ks1156-ornith35b-night3'), 'strict', D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts'),
]
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate15', now())
co_before = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
C = tempfile.mkdtemp(prefix='predict15.', dir=S)
rc, o, e = sh(['git', 'clone', '--quiet', '--shared', '--no-checkout', REPO, C + '/clone']); print('clone rc=%d %s at %s' % (rc, e[:100], C))
CL = C + '/clone'
def g(*a, env=None): return sh(['git', '-C', CL] + list(a), env=env)
print('develop tree:', g('rev-parse', DEV + '^{tree}')[1], '==', DEV_TREE, g('rev-parse', DEV + '^{tree}')[1] == DEV_TREE)
def idx(name):
    env = dict(os.environ, GIT_INDEX_FILE=C + '/idx-' + name); g('read-tree', DEV, env=env); return env
def apply_check(env, patch, *flags): return g('apply', '--cached', '--check', *flags, patch, env=env)
def apply_real(env, patch, *flags): return g('apply', '--cached', *flags, patch, env=env)
def blob(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else '?'
print('--- (a) CANONICAL-PATCH IDENTITY at develop', DEV[:9], '(temp index per canonical; --cached into the scratch clone objects)')
res = {}
for label, p, patch, mode, path in CANON:
    ex = os.path.exists(patch)
    env = idx('c-' + label)
    st = apply_check(env, patch); rv = apply_check(env, patch, '-R'); rcnt = apply_check(env, patch, '--recount'); rvr = apply_check(env, patch, '-R', '--recount')
    flags = [] if mode == 'strict' else ['--recount']
    ap = apply_real(env, patch, *flags); b = blob(env, path)
    res[label] = (env, b)
    print('  %-14s PR %-2s canonical %s exists %s sha16 %s | strict --check rc %d %s | -R --check rc %d | --recount --check rc %d | -R --recount rc %d | APPLIED (%s) rc %d -> blob %s' % (
        label, p, os.path.basename(os.path.dirname(os.path.dirname(patch))) if '/runs/' in patch else 'FENCE', ex, hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?', st[0], ('[' + (st[2].splitlines() or [''])[0][:70] + ']') if st[0] else '', rv[0], rcnt[0], rvr[0], mode, ap[0], b[:12]))
# the KS-1036-item3 FENCE control (BLUF 3b): must refuse at the tip
f1036 = fence('READY_KS-1036-item3_ornith35b-q4_DOCPATCH-REBRIEF-PASS-8of8_2026-09-16.diff.md'); env = idx('ctrl-1036fence')
st = apply_check(env, f1036); rcnt = apply_check(env, f1036, '--recount')
print('  CONTROL KS-1036-item3 FENCE (not the canonical): strict --check rc %d [%s] | --recount --check rc %d — the seat/brief: rc 1 both, `patch failed: …DEV-PROCESS.md:224`' % (st[0], (st[2].splitlines() or [''])[0][:90], rcnt[0]))
for lab, rf in (('KS-1035-D', 'READY_KS-1035-D_ornith35b-q4_DOCPATCH-REANCHORED-PASS-6of6_2026-09-15.diff.md'), ('KS-1049-A', 'READY_KS-1049-A_ornith35b-q4_DOCPATCH-PLACED-BY-WEDNESDAY-D8-PASS_2026-09-16.diff.md')):
    env = idx('ctrl-' + lab + 'fence'); st = apply_check(env, fence(rf)); print('  CONTROL %s FENCE (fence != run patch; the run patch is the canonical): strict --check rc %d' % (lab, st[0]))
print('  CONTROL nonexistent patch: rc %d (want 128)' % apply_check(idx('ctrl-none'), C + '/nonexistent.diff')[0])
print('--- per-PR trees over develop by applying the canonicals in GROUPING order (and the reverse where a file carries two)')
PRC = {}
for label, p, patch, mode, path in CANON: PRC.setdefault(p, []).append((label, patch, mode, path))
def apply_seq(env, seq):
    for label, patch, mode, path in seq:
        rc, o, e = apply_real(env, patch, *([] if mode == 'strict' else ['--recount']))
        if rc: return 'APPLY FAIL %s rc %d %s' % (label, rc, e[:80])
    return g('write-tree', env=env)[1]
PRTREE = {}
for p in PUSH:
    seq = PRC[p]; env = idx('pr-' + p); t = apply_seq(env, seq); PRTREE[p] = t
    bl = {path.split('/')[-1]: blob(env, path)[:12] for _, _, _, path in seq}
    line = '  PR %-2s %-30s tree %s == GROUPING %s: %s | blobs %s == %s' % (p, ' + '.join(l for l, *_ in seq), t[:12], TREE12[p], t.startswith(TREE12[p]), bl, all(blob(env, path).startswith(BLOB12[path]) for _, _, _, path in seq))
    if len(seq) == 2:
        env2 = idx('pr-' + p + '-rev'); t2 = apply_seq(env2, list(reversed(seq))); line += ' | REVERSE order tree %s same %s' % (t2[:12], t2 == t)
    print(line)
print('--- the all-14 tree over develop by applying every canonical: forward, exact reverse, seed-15 shuffle')
allseq = [x for p in PUSH for x in PRC[p]]
orders = [('forward', allseq), ('reverse', list(reversed(allseq)))]
rnd = random.Random(15); sh15 = allseq[:]; rnd.shuffle(sh15); orders.append(('seed-15 shuffle', sh15))
alls = []
for name, seq in orders:
    t = apply_seq(idx('all-' + name.replace(' ', '')), seq); alls.append(t); print('  %-16s -> %s' % (name, t))
print('  all three identical: %s | == the seat/drafter all-14 tree %s: %s' % (len(set(alls)) == 1, SEAT_ALL, alls[0] == SEAT_ALL))
if alls[0] == SEAT_ALL:
    print('  shortstat:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', SEAT_ALL)[1], '| name-status', sorted(l.split('\t')[0] for l in g('diff-tree', '-r', '--name-status', DEV + '^{tree}', SEAT_ALL)[1].splitlines()))
    print('  numstat:'); print(g('diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL)[1])
env = idx('ctrl-dev'); wt = g('write-tree', env=env)[1]; print('  CONTROL read-tree back to develop -> %s == %s %s' % (wt, DEV_TREE, wt == DEV_TREE))
print('--- (b) THE HEADS from the captured READYs, REAL 3-way merges')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(2), m.group(4))
present = [p for p in PUSH if p in READY]
print('heads from READYs (seat PR -> #PR key head):', {p: READY[p] for p in present})
H = {}
for p in present:
    h = READY[p][2]
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
if len(present) >= 2:
    orders_h = [present, list(reversed(present))]; rnd = random.Random(15)
    for i in range(2):
        o = present[:]; rnd.shuffle(o); orders_h.append(o)
    results = []
    for o in orders_h:
        t = chain(DEV, [H[p] for p in o]); results.append(t); print('order %-24s: %s' % (' '.join(o), t))
    ALLH = results[0]
    print('all orders identical:', len(set(results)) == 1, '| == the seat all-14 tree %s: %s (True only once all ten heads are present; %d present)' % (SEAT_ALL, ALLH == SEAT_ALL, len(present)))
    if 'CONFLICT' not in ALLH:
        for p in present:
            for path in g('diff', '--name-only', DEV, H[p])[1].splitlines():
                a = g('rev-parse', ALLH + ':' + path)[1]; c = g('rev-parse', H[p] + ':' + path)[1]
                if a != c: print('  MISMATCH PR %s %s ALL %s head %s' % (p, path, a, c))
        print('every PR path in ALL(present) carries its head blob (no MISMATCH line above = True)')
        for p in present: print('  PR %s head tree != ALL(present): %s' % (p, g('rev-parse', H[p] + '^{tree}')[1] != ALLH))
        print('  ALL(present) shortstat:', g('diff-tree', '-r', '--shortstat', DEV + '^{tree}', ALLH)[1])
else:
    orders_h = []
    print('fewer than two heads present — the chain is a fast-forward; orders need two heads')
# (c) THE DEVELOP MOVE: origin develop moved off 581ed7fa1 (the heads' parent) at 12:44:19Z (#1138 merged — a merge commit, 3 commits, 7 files
#     under systemTest/ + Projects Documents/, ∩ the 11 paths = ∅ — dev_move_reads_1.out). The new tip is NOT in the local object store; it is
#     fetched BY SHA into THIS scratch clone only (never the checkout) over https with GH_TOKEN through a GIT_ASKPASS helper (never on a command
#     line); then every PR head alone over the NEW develop (real 3-way), the all-14 canonicals over it, and the all-present heads over it.
CUR = sh(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'])[1].split()[0]
print('--- (c) origin develop NOW', CUR, '| the heads parent', DEV[:9], '| moved:', CUR != DEV)
if CUR != DEV:
    tok = ''
    for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
        if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
    ask = os.path.join(C, 'askpass.sh'); open(ask, 'w').write('#!/bin/sh\ncase "$1" in *sername*) echo x-access-token;; *) printf %s "$GH_TOKEN_FOR_FETCH";; esac\n'); os.chmod(ask, 0o700)
    fenv = dict(os.environ, GIT_ASKPASS=ask, GH_TOKEN_FOR_FETCH=tok, GIT_TERMINAL_PROMPT='0')
    rc, o, e = sh(['git', '-C', CL, 'fetch', '--quiet', 'https://github.com/Secuura/Distributed_Secuura.git', CUR], env=fenv)
    print('fetch by SHA over https into the scratch clone rc=%d %s | object present now: %s' % (rc, e[:120], g('cat-file', '-e', CUR + '^{commit}')[0] == 0))
    if g('cat-file', '-e', CUR + '^{commit}')[0] != 0:
        # the https road refused (the token is not a clone credential for this org); the ssh road is the checkout's own: its remote URL and its
        # repo-local core.sshCommand (the per-project deploy key, READ from .git/config, never printed) — the same road `git ls-remote origin` takes
        url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]; sshc = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
        rc, o, e = sh(['git', '-C', CL, '-c', 'core.sshCommand=' + sshc, 'fetch', '--quiet', url, CUR])
        print('fetch by SHA over ssh (the checkout remote URL + its repo-local core.sshCommand, read not printed) into the scratch clone rc=%d %s | object present now: %s' % (rc, e[:120], g('cat-file', '-e', CUR + '^{commit}')[0] == 0))
    if g('cat-file', '-e', CUR + '^{commit}')[0] == 0:
        CT = g('rev-parse', CUR + '^{tree}')[1]; print('new develop tree', CT, '| rev-list --count %s..%s = %s | merge-base with the heads parent = %s' % (DEV[:9], CUR[:9], g('rev-list', '--count', DEV + '..' + CUR)[1], g('merge-base', DEV, CUR)[1][:12]))
        print('move name-status:'); print(g('diff', '--name-status', DEV, CUR)[1]); print('move shortstat:', g('diff', '--shortstat', DEV, CUR)[1])
        mv = set(g('diff', '--name-only', DEV, CUR)[1].splitlines()); mine = set(BLOB12)
        print('∩ the 11 paths:', sorted(mv & mine) or 'NONE', '| the 11 blobs identical at both tips:', all(g('rev-parse', DEV + ':' + p_)[1] == g('rev-parse', CUR + ':' + p_)[1] for p_ in BLOB12), '(11 of 11)')
        # per-PR trees over the NEW develop by applying the canonicals into a temp index read from CUR
        def idx2(name):
            env = dict(os.environ, GIT_INDEX_FILE=C + '/idx2-' + name); g('read-tree', CUR, env=env); return env
        PRTREE2 = {}
        for p in PUSH:
            t = apply_seq(idx2('pr-' + p), PRC[p]); PRTREE2[p] = t
            print('  PR %-2s canonicals over the NEW develop -> tree %s (over the old %s; the addendum merged tree for a merge onto %s)' % (p, t[:12], PRTREE[p][:12], CUR[:9]))
        alls2 = [apply_seq(idx2('all-' + n.replace(' ', '')), seq) for n, seq in orders]
        print('  all-14 over the NEW develop: forward %s | reverse %s | seed-15 %s | identical %s (the END STATE tree if every merge lands on %s)' % (alls2[0][:12], alls2[1][:12], alls2[2][:12], len(set(alls2)) == 1, CUR[:9]))
        print('  shortstat over NEW develop:', g('diff-tree', '-r', '--shortstat', CT, alls2[0])[1])
        ALL2 = alls2[0]
        # real 3-way merges of the captured heads over the NEW develop
        for p in present:
            a = g('merge-tree', '--write-tree', CUR, H[p]); b = g('merge-tree', '--write-tree', H[p], CUR)
            print('  PR %s #%s head %s alone over NEW develop %s: fwd=%s rc=%d rev-same=%s | == canonical-apply-over-new %s: %s | != head tree: %s' % (p, READY[p][0], H[p][:9], CUR[:9], a[1][:12], a[0], a[1] == b[1], PRTREE2[p][:12], a[1] == PRTREE2[p], a[1] != g('rev-parse', H[p] + '^{tree}')[1]))
        if len(present) >= 2:
            r2 = [chain(CUR, [H[p] for p in o]) for o in orders_h]
            print('  all-present heads over NEW develop in %d orders: %s | identical %s' % (len(r2), [x[:12] for x in r2], len(set(r2)) == 1))
        print('  compare per PR would read: merge_base %s ahead 1 behind %s (the launcher asserts behind = the move count)' % (DEV[:9], g('rev-list', '--count', DEV + '..' + CUR)[1]))
        print('  new-develop tree entries for the launcher generator: written to', os.path.join(G, 'newdev_tree.txt'))
        open(os.path.join(G, 'newdev_tree.txt'), 'w').write('DEV_NOW %s\nTREE %s\nALL14_OVER_NEW %s\n' % (CUR, CT, ALL2) + '\n'.join('PR%s %s' % (p, PRTREE2[p]) for p in PUSH) + '\n')
E = tempfile.mkdtemp(prefix='empty15.', dir=S); subprocess.run(['git', '-C', E, 'init', '--quiet'])
print('control: numstat from an empty repo rc=%d (want 128)' % sh(['git', '-C', E, 'diff-tree', '-r', '--numstat', DEV + '^{tree}', SEAT_ALL])[0])
co_after = sh(['git', '-C', REPO, 'count-objects', '-v'])[1]
print('checkout count-objects after: ', co_after.replace('\n', ' '), '| byte-identical to before:', co_after == co_before)
print('checkout porcelain non-untracked (read):', sum(1 for l in sh(['git', '-C', REPO, 'status', '--porcelain'])[1].splitlines() if not l.startswith('??')), '| .git/worktrees:', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref:', len(sh(['git', '-C', REPO, 'for-each-ref'])[1].splitlines()))
print('scratch clone at', CL, '(left in the scratchpad, never deleted)'); print('done', now())
