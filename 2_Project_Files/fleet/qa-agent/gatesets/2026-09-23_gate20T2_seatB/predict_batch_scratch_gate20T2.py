#!/usr/bin/env python3
"""predict_batch_scratch_gate20T2.py — every git WRITE verb of the gate20T2 drafter lives here, in a scratch clone made FROM ORIGIN (a `git clone --bare
--filter=blob:none` of git@github.com:Secuura/Distributed_Secuura.git over the checkout's own ssh road — its remote URL + repo-local core.sshCommand,
read from the checkout's config, never printed) under the drafter's scratchpad (argv[1]). NEVER `--shared` from the checkout. The Secuura checkout is
only READ (count-objects before/after printed; byte-identical expected). The gate19B predict script re-keyed to Seat B 21st's TIER-2 FOUR.
(a) THE HEADS: develop + refs/pull/N/head for seat PRs 1, 2, 4 (+ 5 once its READY names it; + the tier-1 PRs present at origin, for the overlap)
    fetched by ref INTO the scratch clone; each head's parent == develop 2bc5ccf63 (fast-forward: merged tree == head tree == the READY's PR-alone
    tree); per head: name-status / numstat vs the pins, every blob's 12-hex prefix vs the READY/brief (AT THE HEAD), lines, MODES (the two bash test
    files are read, not assumed — the STANDING_LINES 2026-09-22 disk-mode line).
    PR 5 PENDING (no READY yet): a PREDICTED PR-5 commit is built in the scratch clone from its canonical patch.diff over develop (commit-tree; a
    write verb in the scratch clone only) and every tree below uses it, labelled PREDICTED; if PR 5's head is also at origin under the expected
    branch, it is fetched and compared (tree == the predicted tree 8c02c7b62858 expected).
(b) THE TREES: the four heads chained by REAL `merge-tree --write-tree` over develop in THREE orders (push order, reverse, seed-20 shuffle) -> ONE
    tree = the TIER-2 SUB-TREE (the seat states it in READY 5); shortstat; 4 rows; every path at its head blob; each single tree != ALL; the tier-1
    paths (the brief's 12) untouched by ALL; the tier-1 heads at origin (today #1204 KS-851) ∩ ours = ∅ and T2-then-T1 == T1-then-T2.
(c) CANONICAL-PATCH IDENTITY: each canonical applied with `git apply --cached` into a temp index read from develop: strict --check rc / -R --check rc /
    --recount --check rc; APPLY -> the blob == the READY's 12-hex + lines; per-PR write-tree == the head tree ×4 (PR 5 == its predicted tree).
(c2) THE KS-1019 TOKEN INSTRUMENT — the comment_patch proof re-derived: the develop blob and the head blob of originate.openapi.ts through
    c4tokens_gate20T2.js (typescript 5.9.3, loaded READ-ONLY by absolute path from the checkout's node_modules) — SCANNER and PARSER-LEAVES counts and
    sha256s, before == after on each; the PLANTED-TOKEN control (one code token appended to the head copy) MUST move both streams; the PLANTED-COMMENT
    control MUST move neither; a line-diff of the two blobs printed (the one added line, its line number vs the ruling's :601).
(d) THE DEVELOP MOVE: if origin develop is not 2bc5ccf63 the new tip is in the clone anyway; newdev_tree.txt is written in either case.
Usage: predict_batch_scratch_gate20T2.py <scratchpad dir> (MUST be this session's scratchpad under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/;
the guard refuses rc 9 otherwise; every write verb asserts cwd inside the scratch clone)."""
import hashlib, json, os, random, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T2 as R
SCRATCH_ROOT = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/'
S = os.path.realpath(sys.argv[1]) if len(sys.argv) > 1 else ''
if not (S.startswith(os.path.realpath(SCRATCH_ROOT)) and '/scratchpad' in S and os.path.isdir(S)):
    print('REFUSING: argv[1] is not a scratchpad under', SCRATCH_ROOT, '->', S); sys.exit(9)
if S.startswith(os.path.realpath(R.REPO)):
    print('REFUSING: the scratchpad is inside the Secuura checkout'); sys.exit(9)
WRITE_VERBS = {'apply', 'read-tree', 'write-tree', 'merge-tree', 'commit-tree', 'fetch', 'update-ref', 'update-index', 'hash-object', 'init', 'clone', 'worktree', 'checkout', 'merge', 'commit'}
TSMOD = R.REPO + '/Blockchain/Dev/node_modules/typescript'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(args, cwd=None, env=None, inp=None):
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('predict_batch_scratch_gate20T2', now(), '| PR5_PENDING', R.PR5_PENDING, '| PR 5', R.PRS['5']['n'], R.PRS['5']['head'])
co_before = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects before:', co_before.replace('\n', ' '))
sshc = sh(['git', '-C', R.REPO, 'config', '--get', 'core.sshCommand'])[1]; print('checkout core.sshCommand read:', 'yes (not printed)' if sshc else 'NO')
url = sh(['git', '-C', R.REPO, 'config', '--get', 'remote.origin.url'])[1]; print('checkout remote.origin.url:', url, '== round20T2:', url == R.ORIGIN_URL)
Cdir = tempfile.mkdtemp(prefix='predict20T2.', dir=S); CL = Cdir + '/origin.git'; WT = Cdir + '/wt'; os.makedirs(WT)
ENV = dict(os.environ, GIT_SSH_COMMAND=sshc) if sshc else dict(os.environ)
os.chdir(Cdir); print('cwd now', os.getcwd(), '| under the scratchpad:', os.path.realpath(os.getcwd()).startswith(S))
def assert_in_scratch(verb):
    if verb in WRITE_VERBS and not os.path.realpath(os.getcwd()).startswith(S):
        print('REFUSING write verb', verb, 'outside the scratchpad: cwd', os.getcwd()); sys.exit(9)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN (bare, blob:none) rc=%d %s -> %s' % (rc, e[:120], CL)); assert rc == 0
def g(*a, env=None, inp=None):
    assert_in_scratch(a[0]); return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
# what exists at origin right now: the four (PR 5 by its READY's number, else by the EXPECTED branch), the tier-1 PR heads by number 1204..1215
lsr = sh(['git', '-C', R.REPO, 'ls-remote', 'origin', 'refs/heads/develop', R.PRS['5']['branch_expected']] + ['refs/pull/%d/head' % n for n in range(1202, 1216)])
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s: %d refs' % (lsr[0], now(), len(LS)))
T2N = [R.PRS[p]['n'] for p in R.PUSH if R.PRS[p]['n']]
T1N = sorted(r.split('/')[2] for r in LS if r.startswith('refs/pull/') and r.split('/')[2] not in T2N)
print('tier-2 PR numbers pinned:', T2N, '| other open pull heads 1202-1215 at origin (the tier-1 batch + anything else):', T1N)
refspecs = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/pull/%s/head' % (n, n) for n in T2N + T1N]
if R.PR5_PENDING and R.PRS['5']['branch_expected'] in LS: refspecs.append('+%s:refs/heads/pr5-expected' % R.PRS['5']['branch_expected'])
rc, o, e = g('fetch', '--quiet', 'origin', *refspecs); print('fetch by ref FROM ORIGIN rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEVNOW = g('rev-parse', 'refs/heads/develop')[1]; print('origin develop at fetch:', DEVNOW, '== pin 2bc5ccf63:', DEVNOW == R.DEV)
DEV = R.DEV
def tree_of(c): return g('rev-parse', c + '^{tree}')[1]
print('develop tree:', tree_of(DEV), '== pin', tree_of(DEV) == R.DEV_TREE)
def lstree(tree, path):
    rc, o, e = g('ls-tree', tree, '--', path); return (o.split()[0], o.split()[2]) if o else ('ABSENT', 'ABSENT')
def cat(b): return subprocess.run(['git', '-C', CL, 'cat-file', '-p', b], capture_output=True, env=ENV).stdout if b != 'ABSENT' else b''
def nlines(b): return cat(b).count(b'\n')
DEVTREE = tree_of(DEV)
def idx(name, base=DEV):
    env = dict(ENV, GIT_INDEX_FILE=Cdir + '/idx-' + name, GIT_WORK_TREE=WT); g('read-tree', base, env=env); return env
def blob_in(env, path):
    rc, o, e = g('ls-files', '-s', '--', path, env=env); return o.split()[1] if o else 'ABSENT'
cenv = dict(ENV, GIT_AUTHOR_NAME='gate20T2-drafter', GIT_AUTHOR_EMAIL='drafter@scratch', GIT_COMMITTER_NAME='gate20T2-drafter', GIT_COMMITTER_EMAIL='drafter@scratch',
            GIT_AUTHOR_DATE='2026-09-23T00:00:00Z', GIT_COMMITTER_DATE='2026-09-23T00:00:00Z')
# the PREDICTED PR 5 (always built — the control for the real head when it lands)
env5 = idx('pred5'); row5 = R.PRS['5']['canon'][0]; ap5 = g('apply', '--cached', R.canon_path(row5), env=env5); t5 = g('write-tree', env=env5)[1]
rc, P5, e = g('commit-tree', t5, '-p', DEV, '-m', 'scratch: PREDICTED PR 5 (KS-1139 ERREXITBEHAVIOUR) from its canonical', env=cenv)
print('PREDICTED PR 5: canonical apply rc %d -> tree %s (brief %s: %s) | scratch commit %s' % (ap5[0], t5[:12], R.PRS['5']['tree12'], t5.startswith(R.PRS['5']['tree12']), P5[:9]))
REF = {}
for p in R.PUSH:
    REF[p] = 'refs/pull/%s/head' % R.PRS[p]['n'] if R.PRS[p]['n'] else P5
if R.PR5_PENDING:
    x = g('rev-parse', '--verify', '-q', 'refs/heads/pr5-expected')[1]
    print('PR 5 PENDING: every tree below uses the PREDICTED commit %s | the expected branch at origin: %s%s' % (P5[:9], x or 'ABSENT', (' tree %s == predicted %s' % (tree_of(x)[:12], tree_of(x) == t5)) if x else ''))
print('--- (a) THE HEADS (each read from the scratch clone fetched from origin; parent / tree / files / blobs / modes)')
HEADTREE = {}; ok_heads = 0; blobs40 = {}; modes = {}
for p in R.PUSH:
    pr = R.PRS[p]; h = g('rev-parse', REF[p])[1]
    par = g('rev-parse', h + '^')[1]; t = tree_of(h); HEADTREE[p] = t
    ns = g('diff-tree', '-r', '--name-status', DEV, h)[1].splitlines(); num = g('diff-tree', '-r', '--numstat', DEV, h)[1].splitlines()
    paths = sorted(l.split('\t')[1] for l in ns); want = sorted(f['path'] for f in pr['files'])
    adds = sum(int(l.split('\t')[0]) for l in num); dels = sum(int(l.split('\t')[1]) for l in num)
    okh = (h == pr['head']) if pr['head'] else None; okp = par == DEV; okt = t.startswith(pr.get('tree') or pr.get('tree12')); okf = paths == want; okn = (adds, dels) == (pr['adds'], pr['dels'])
    ncommits = g('rev-list', '--count', DEV + '..' + h)[1]
    print('  PR %s #%s %-8s %s head %s == READY %s | parent == develop %s | commits %s | tree %s == READY/brief %s | files == pinned %s %s | +%d/-%d == %s' % (p, pr['n'] or 'PENDING', pr['key'], '(PREDICTED)' if not pr['head'] else '', h[:9], okh, okp, ncommits, t[:12], okt, okf, '' if okf else (paths, want), adds, dels, okn))
    for f in pr['files']:
        m, b = lstree(t, f['path']); md, bd = lstree(DEVTREE, f['path']); blobs40[(p, f['path'])] = b; modes[f['path']] = (m, md)
        st = [l.split('\t')[0] for l in ns if l.split('\t')[1] == f['path']]
        print('     %-80s status %s blob %s == %s %s | lines %d (want %d) | mode %s (develop %s; develop blob %s == %s %s / %d lines)' % (f['path'], st, b[:12], f['blob12'], b.startswith(f['blob12']), nlines(b), f['lines'], m, md, bd[:12], f['dev_blob12'], bd.startswith(f['dev_blob12']), nlines(bd)))
    if (okh is not False) and okp and okt and okf and okn: ok_heads += 1
print('  heads fully agreeing (PR 5 PREDICTED while pending): %d/4' % ok_heads)
print('  MODES: %s' % {k.split('/')[-1]: v for k, v in modes.items()})
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
orders = {'push order': list(R.PUSH), 'reverse': list(reversed(R.PUSH)), 'seed-20 shuffle': random.Random(20).sample(R.PUSH, len(R.PUSH))}
ALL = {}
for name, order in orders.items():
    ALL[name] = chain([REF[p] for p in order]); print('  tier-2 sub-tree chained [%s] %s -> %s' % (name, ' '.join(order), ALL[name]))
A = ALL['push order']; one = len(set(ALL.values())) == 1 and len(A) == 40
print('  ONE tree in three orders:', one, '| %s' % ('PREDICTED (PR 5 from its canonical)' if R.PR5_PENDING else 'MEASURED (four real heads)'))
if len(A) == 40:
    ss = g('diff-tree', '-r', '--shortstat', DEV, A)[1]; print('  shortstat:', ss.strip())
    ns = g('diff-tree', '-r', '--name-status', DEV, A)[1].splitlines(); print('  name-status: %d rows, A %d M %d | == round20T2 distinct: %s' % (len(ns), sum(1 for l in ns if l.startswith('A')), sum(1 for l in ns if l.startswith('M')), sorted(l.split('\t')[1] for l in ns) == R.distinct_paths()))
    mism = sum(1 for p in R.PUSH for f in R.PRS[p]['files'] if lstree(A, f['path'])[1] != blobs40[(p, f['path'])])
    print('  every ALL path at its head blob: %s (mismatches %d) | each single head tree != ALL: %s | develop tree unchanged: %s' % (mism == 0, mism, all(HEADTREE[p] != A for p in R.PUSH), tree_of(DEV) == R.DEV_TREE))
    t1_over = [q for q in R.TIER1_PATHS if lstree(A, q)[1] != lstree(DEVTREE, q)[1]]; tf_over = [q for q in R.TAMPER_FILES if lstree(A, q)[1] != lstree(DEVTREE, q)[1]]
    print('  the tier-1 batch\'s 12 paths changed by ALL: %s | the tamper files changed by ALL: %s' % (t1_over or 'NONE', tf_over or 'NONE'))
    for n in T1N:
        fp = g('diff-tree', '-r', '--name-only', DEV, 'refs/pull/%s/head' % n)[1].splitlines(); par = g('rev-parse', 'refs/pull/%s/head^' % n)[1]
        tb = chain(['refs/pull/%s/head' % n], start=A); bt = chain([REF[p] for p in R.PUSH], start=tree_of('refs/pull/%s/head' % n))
        print('  other pull #%s: parent == develop %s | files %s | ∩ tier-2 %s | ∈ the brief\'s tier-1 paths %s | T2-then-#%s %s == #%s-then-T2 %s: %s' % (n, par == DEV, [x.split('/')[-1] for x in fp], sorted(set(fp) & set(R.all_paths())) or 'NONE', all(x in R.TIER1_PATHS for x in fp), n, tb[:12], n, bt[:12], tb == bt))
print('--- (c) CANONICAL-PATCH IDENTITY at develop (temp index per PR in the scratch clone; --cached)')
tree_ok = 0
for p in R.PUSH:
    pr = R.PRS[p]; env = idx('pr' + p)
    for row in pr['canon']:
        label, rd, fn, sha16, opts, path = row; patch = R.canon_path(row); ex = os.path.exists(patch)
        sha = hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:16] if ex else '?'; size = os.path.getsize(patch) if ex else -1
        envc = idx('chk-' + label)
        st = g('apply', '--cached', '--check', patch, env=envc); rv = g('apply', '--cached', '--check', '-R', patch, env=envc); rcn = g('apply', '--cached', '--check', '--recount', patch, env=envc)
        ap = g('apply', '--cached', patch, env=env); b = blob_in(env, path)
        print('  PR %s %-22s %-52s sha16 %s == READY %s (%d B) | strict --check rc %d | -R rc %d | --recount rc %d | APPLY rc %d -> %s / %d lines' % (p, label, rd + '/' + fn, sha, sha == sha16, size, st[0], rv[0], rcn[0], ap[0], b[:12], nlines(b)))
    fin = all(blob_in(env, f['path']).startswith(f['blob12']) for f in pr['files'])
    t = g('write-tree', env=env)[1]
    print('     final blobs == READY 12-hex: %s | write-tree %s == head tree %s: %s' % (fin, t[:12], HEADTREE[p][:12], t == HEADTREE[p])); tree_ok += (t == HEADTREE[p])
print('  per-PR canonical trees == head trees: %d/4' % tree_ok)
env = idx('ctrl'); ctl = g('apply', '--cached', '--check', Cdir + '/does-not-exist.diff', env=env); print('  nonexistent-patch control rc', ctl[0], '(128 expected)')
print('--- (c2) THE KS-1019 TOKEN INSTRUMENT (comment_patch: token equivalence, BOTH tokenisations, with the planted controls)')
p2 = R.PRS['2']; path2 = p2['files'][0]['path']
bdev = lstree(DEVTREE, path2)[1]; bhead = blobs40[('2', path2)]
before = cat(bdev); after = cat(bhead)
open(Cdir + '/before.ts', 'wb').write(before); open(Cdir + '/after.ts', 'wb').write(after)
open(Cdir + '/after_plant_code.ts', 'wb').write(after + b'\nexport const __gate20T2_planted_token = 1;\n')
open(Cdir + '/after_plant_comment.ts', 'wb').write(after + b'\n// gate20T2 planted comment: no code token\n')
dl = sh(['diff', Cdir + '/before.ts', Cdir + '/after.ts']); print('  line diff develop -> head (rc %d):' % dl[0]); [print('    ' + x) for x in dl[1].splitlines()]
tsv = sh(['node', '-e', 'console.log(require(process.argv[1]).version)', TSMOD]); print('  typescript at', TSMOD, 'version', tsv[1], '(rc %d)' % tsv[0])
r = sh(['node', G + '/c4tokens_gate20T2.js', TSMOD, Cdir + '/before.ts', Cdir + '/after.ts', Cdir + '/after_plant_code.ts', Cdir + '/after_plant_comment.ts'])
print('  c4tokens_gate20T2.js rc', r[0], r[2][:200])
res = [json.loads(x) for x in r[1].splitlines()] if r[0] == 0 else []
for x in res: print('   ', os.path.basename(x['file']), 'scanner', x['scanner_n'], x['scanner_sha256'][:16], '| leaves', x['leaves_n'], x['leaves_sha256'][:16], '| ts', x['ts'])
if len(res) == 4:
    b_, a_, pc, pm = res
    print('  SCANNER before == after: %s (n %d == %d; the seat 17731) | LEAVES before == after: %s (n %d == %d; the checker 17679)' % (b_['scanner_sha256'] == a_['scanner_sha256'], b_['scanner_n'], a_['scanner_n'], b_['leaves_sha256'] == a_['leaves_sha256'], b_['leaves_n'], a_['leaves_n']))
    print('  PLANTED-TOKEN control FIRES (moves both): scanner %s (%d -> %d) leaves %s (%d -> %d) | PLANTED-COMMENT control is SILENT (moves neither): scanner %s leaves %s' % (
        pc['scanner_sha256'] != a_['scanner_sha256'], a_['scanner_n'], pc['scanner_n'], pc['leaves_sha256'] != a_['leaves_sha256'], a_['leaves_n'], pc['leaves_n'], pm['scanner_sha256'] == a_['scanner_sha256'], pm['leaves_sha256'] == a_['leaves_sha256']))
    json.dump(res, open(G + '/c4tokens_1.json', 'w'), indent=1)
print('--- (d) THE DEVELOP MOVE')
print('  origin develop at fetch', DEVNOW[:9], 'UNMOVED' if DEVNOW == R.DEV else 'MOVED — the trees above are over the PIN; re-predict over the new tip is the generator\'s refusal case')
open(G + '/newdev_tree.txt', 'w').write('develop %s\ntree %s\nt2sub %s\nt2sub_kind %s\npr5_predicted_tree %s\npr5_head %s\nread %s\n' % (DEVNOW, tree_of(DEVNOW), A, 'PREDICTED' if R.PR5_PENDING else 'MEASURED', t5, R.PRS['5']['head'] or 'PENDING', now()))
co_after = sh(['git', '-C', R.REPO, 'count-objects', '-v'])[1]; print('checkout count-objects after:', co_after.replace('\n', ' '), '| byte-identical:', co_before == co_after)
print('scratch clone', CL)
print('done', now())
