#!/usr/bin/env python3
"""predict_gate24T2b.py — MEASURE the round-24 SECOND tier-2 batch gate24T2b (#1249 KS-1144 STACKED on #1248, #1250 KS-1302 + KS-1303, #1251 KS-1147,
#1252 KS-1275 + KS-1299, #1253 KS-1297, #1254 KS-1155, #1255 KS-1301 — FROZEN at seven by the drafter at pin time (the two late adds by
Wednesday's messages; no Seat L5 widen item had a PR); three seats: L6, L5, B 28th) over origin develop
AS READ NOW, and write pins_gate24T2b.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index, hash-object for a simulation) runs in a scratch BARE clone under <scratchpad>/g24b_sp/clone.git
— `git clone --bare --no-local` FROM the checkout (a plain copy through upload-pack: NO alternates into the shared object store, which is only READ),
then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only, never printed). Nothing is
written into the checkout.

PARENTS (measured, not assumed): #1250, #1251, #1253, #1254 are ONE commit each on BASE 6e2a00bfed57; #1252 and #1255 are ONE commit each on develop
77c6426b96d9 (Seat B 28th branched after #1247); #1249 is ONE commit on #1248's head 2b4960172644 — #1248 is in the RUNNING gate24T2a batch (NOT graded here) and
is itself ONE commit on BASE. BASE-INVARIANT per PR (Wednesday's 04:35Z ANSWER `answer_seatB25_movedbase`), each over its GRADING BASE — develop for
six PRs, and for the stacked #1249 the commit develop + #1248 (merge-tree of develop and #1248's head): (1) diff(grading base, merged) == EXACTLY
the PR's own paths, each blob byte-equal to the head's blob; (2) numstat(grading base -> merged) == numstat(parent -> head); (3) the develop move since
the PR's parent ∩ the PR's OWN paths == EMPTY. #1249 over develop ALONE is ALSO measured: it carries #1248's commit, so its diff there is #1248 + #1249
combined — the reason #1249 merges only AFTER #1248. PAIRWISE the seven batch PRs' path sets are DISJOINT (hard); the ONE declared overlap is
#1248 ∩ #1249 == {ks781-p3-3-body-parser-order.test.ts} (merged-blob target: #1249's head blob). #1254 vs #1248/#1249/#1251 (all packages/shared):
path-disjoint (hard) — its coupling is by CONTENT (its derived list reads those files' bytes), measured in (n).
Python ports of the changed readers (cell 9's call-site predicate, the walker derivation, the yaml summarise() of preflight leg 8, the dedicated-verb
read) are READ instruments for PREDICTIONS only — never evidence; the gate measures through the real code.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in 1249..1254) builds develop + a FOREIGN edit of that PR's first own
file in the scratch clone and measures over it (a NEGATIVE CONTROL: must REFUSE); a simulation writes pins_gate24T2b.SIM-<mode>.json, never the pins.
Usage: predict_gate24T2b.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign1249|...|foreign1254]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6e2a00bfed577528de1ee02b41cb5a0e99172b35'
DEV_AT_DRAFT = '77c6426b96d9e48a758e68fa56e9138dc8509aa8'
H48 = '2b4960172644b5ef0414b94d46d11974012c2007'   # #1248's head as gate24T2a pinned it (14:52:19Z launch); #1249's parent
BR48 = 'refs/heads/feature/ks-1143-legf-gf2-callback-walk-l6-r24-1'
S = 'Blockchain/Dev/packages/shared/'
F48 = S + 'src/__tests__/ks781-p3-3-body-parser-order.test.ts'
PRS = {
    '1249': {'keys': ['KS-1144'], 'head': '6eb283d058184f1f0fabdc3c3184a817db4fb94b', 'parent': H48, 'seat': 'L6',
             'branch': 'refs/heads/feature/ks-1144-j2-positive-control-l6-r24-1', 'files': {F48: (81, 14)}},
    '1250': {'keys': ['KS-1302', 'KS-1303'], 'head': 'c78f4093fb531bceb94a8e9defb59350d8c60b73', 'parent': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-1302-runner-tmpdir-residue-and-orphan-pipe-l5-1',
             'files': {'Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh': (70, 0), 'Blockchain/Dev/scripts/run-shell-suites.sh': (49, 5)}},
    '1251': {'keys': ['KS-1147'], 'head': '8020adae99129f4b7194fef32f1ea5b762819d90', 'parent': BASE, 'seat': 'L6',
             'branch': 'refs/heads/feature/ks-1147-ks860-escaped-host-l6-r24-1',
             'files': {S + 'src/__tests__/ks860-test-listeners-bind-loopback.test.ts': (52, 1)}},
    '1252': {'keys': ['KS-1275', 'KS-1299'], 'head': 'ca7337fa04e04e5438bc79a5abe215424fcb33ef', 'parent': DEV_AT_DRAFT, 'seat': 'B 28th',
             'branch': 'refs/heads/feature/ks-1275-lifecycle-event-verb-list-points-at-the-enum-r24-b-1',
             'files': {'Blockchain/Dev/docs/openapi/secuura-api.yaml': (13, 6),
                       'Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts': (31, 5),
                       'Blockchain/Dev/services/originate/src/originate.openapi.ts': (12, 3)}},
    '1253': {'keys': ['KS-1297'], 'head': '6b88e4f03e82e3da0672efb1bb757ba5da912d6a', 'parent': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-1297-fixture-guard-anchor-and-two-gaps-l5-1',
             'files': {'Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh': (115, 3)}},
    '1254': {'keys': ['KS-1155'], 'head': 'da0c94968a7423c340b3a3b76244bda536d1f6d2', 'parent': BASE, 'seat': 'L6',
             'branch': 'refs/heads/feature/ks-1155-guard-timeout-budget-l6-r24-1',
             'files': {S + 'src/__tests__/support/walkTimeouts.setup.ts': (75, 0), S + 'src/__tests__/walkTimeouts.test.ts': (99, 0),
                       S + 'vitest.config.ts': (11, 0)}},
    '1255': {'keys': ['KS-1301'], 'head': '59245ff0b11c6b760ba5e2a9daedc5927e915e10', 'parent': DEV_AT_DRAFT, 'seat': 'B 28th',
             'branch': 'refs/heads/feature/ks-1301-presence-cells-for-sign-cert-and-sign-wallet-r24-c-1',
             'files': {'Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts': (23, 0)}},
}
ADDED = {S + 'src/__tests__/support/walkTimeouts.setup.ts', S + 'src/__tests__/walkTimeouts.test.ts'}
DECLARED_CONFIG = {S + 'vitest.config.ts': '1254'}   # the ONE config file in the batch, declared by #1254's own ticket (KS-1155 fix-shape 1)
H = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/'
PUSHLOG = {'1249': H + '2026-09-25_seatL6/raise/s-l6-ks1144-push.out', '1250': H + '2026-09-25_seatL5/raise/s-l5-ks1302-push.out',
           '1251': H + '2026-09-25_seatL6/raise/s-l6-ks1147-push.out', '1252': H + '2026-09-25_seatB-28th/raise/s-b28-prose-push.out',
           '1253': H + '2026-09-25_seatL5/raise/s-l5-ks1297-push.out', '1254': H + '2026-09-25_seatL6/raise/s-l6-ks1155-push.out',
           '1255': H + '2026-09-25_seatB-28th/raise/s-b28-cells-push.out'}
# the fleet STOP triple (+ run_shell_suites, which #1250 changes) each push must show, READ anchored to each suite's `=== …test.sh ===` header
WANT_STOP = {n: {'pre_push_hook_base': '28/0', 'fixture_guard': '10/0' if n == '1253' else '6/0', 'run_shell_suites': '55/0' if n == '1250' else '49/0',
                 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'} for n in PRS}
RECORD_OVERWRITTEN = {'1255'}   # measured at drafting: s-b28-cells-push.out was #1255's COMPLETE record at 15:10:16Z (predict_3.out); Seat B 28th's next push reused the name from 15:13:28Z (README §6)
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
def die(msg):
    print('REFUSING: ' + msg); sys.exit(1)
def run(args, cwd=None, env=None, inp=None, ok=(0,)):
    p = subprocess.run(args, cwd=cwd, env=env, input=inp, capture_output=True, text=True)
    if p.returncode not in ok:
        die('%s -> rc %d: %s' % (' '.join(args[:6]), p.returncode, (p.stderr or p.stdout).strip()[:400]))
    return p.stdout
if len(sys.argv) < 2 or not re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(sys.argv[1])) or not os.path.isdir(sys.argv[1]):
    die('argv[1] must be an existing scratchpad dir under /private/tmp/claude-501/')
SP = sys.argv[1]
SIM = sys.argv[sys.argv.index('--simulate') + 1] if '--simulate' in sys.argv else ''
if SIM not in ['', 'foreign1248', 'merged1248'] + ['foreign' + n for n in PRS]: die('unknown simulation ' + SIM)
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate24T2b.py at', now(), '| scratchpad', SP, '| SIMULATION:', SIM or 'none (the real read)')

print('--- (a) heads and develop: ls-remote (the checkout, READ) then a fetch FROM ORIGIN into the scratch clone')
refs = ['refs/heads/develop', 'refs/pull/1248/head', BR48] + ['refs/pull/%s/head' % n for n in PRS] + [PRS[n]['branch'] for n in PRS]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
print('  ls-remote at %s:' % now()); [print('    %s %s' % (v, k)) for k, v in lsd.items()]
CL = os.path.join(SP, 'g24b_sp', 'clone.git')
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL])
    run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g24b/develop', '+refs/pull/1248/head:refs/g24b/pr1248']
    + ['+refs/pull/%s/head:refs/g24b/pr%s' % (n, n) for n in PRS] + ['+%s:refs/g24b/br%s' % (PRS[n]['branch'], n) for n in PRS], env=env)
g = lambda *a, **k: run(['git', '--git-dir', CL] + list(a), **k)
DEV = g('rev-parse', 'refs/g24b/develop').strip()
hard(DEV == lsd.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
for n, p in PRS.items():
    h = g('rev-parse', 'refs/g24b/pr' + n).strip(); b = g('rev-parse', 'refs/g24b/br' + n).strip()
    hard(h == b == lsd.get('refs/pull/%s/head' % n) == lsd.get(p['branch']) == p['head'],
         '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (n, h))
h48 = g('rev-parse', 'refs/g24b/pr1248').strip()
hard(h48 == lsd.get('refs/pull/1248/head') == lsd.get(BR48) == H48,
     'STACK BASE: #1248 (gate24T2a, NOT graded here) refs/pull/1248/head == its branch == %s, the head gate24T2a pinned and #1249 sits on' % H48[:12])
REAL_DEV = DEV
CE = dict(env, GIT_AUTHOR_NAME='x', GIT_COMMITTER_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_EMAIL='x@x')
if SIM == 'merged1248':   # a POSITIVE simulation: #1248 squash-merged onto develop (one parent, as a squash lands) — the kit must re-pin cleanly over it
    t_ = g('merge-tree', '--write-tree', DEV, H48).split('\n')[0].strip()
    DEV = g('commit-tree', t_, '-p', DEV, '-m', 'SIMULATED squash of #1248 onto develop', env=CE).strip()
    print('  SIMULATED develop (merged1248): %s = the real develop %s + a SQUASH of #1248 — every check below is over the SIMULATION' % (DEV, REAL_DEV))
elif SIM:
    FP = F48 if SIM == 'foreign1248' else sorted(f for f in PRS[SIM[-4:]]['files'] if f not in ADDED)[0]
    idx = tempfile.mktemp(prefix='g24b_sim_', dir=os.path.dirname(CL)); ienv = dict(CE, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
    blob = g('cat-file', 'blob', DEV + ':' + FP) + '\n# a FOREIGN edit of this PR\'s own file (scratch only, never pushed)\n'
    bo = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=ienv, inp=blob).strip()
    run(['git', '--git-dir', CL, 'update-index', '--cacheinfo', '100644,%s,%s' % (bo, FP)], env=ienv)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
    DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + FP.rsplit('/', 1)[1], env=CE).strip()
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))

print('--- (b) ancestry, the stack, and the develop move')
for n, p in PRS.items():
    par = g('rev-list', '--parents', '-n1', p['head']).split()
    hard(par[1:] == [p['parent']] and g('rev-list', '--count', p['parent'] + '..' + p['head']).strip() == '1',
         '#%s: ONE commit, its parent == %s %s' % (n, {BASE: 'BASE', DEV_AT_DRAFT: 'develop-at-draft', H48: '#1248\'s head'}[p['parent']], p['parent'][:12]))
    hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', p['parent'], DEV]).returncode == 0 or p['parent'] == H48,
         '#%s: its parent %s is an ancestor of develop (or, for the stacked #1249, is #1248\'s head)' % (n, p['parent'][:12]))
par48 = g('rev-list', '--parents', '-n1', H48).split()
hard(par48[1:] == [BASE], 'STACK: #1248\'s head %s is ONE commit on BASE %s' % (H48[:12], BASE[:12]))
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode == 0, 'develop %s descends from BASE' % DEV[:12])
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
_b = lambda r: subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (r, F48)], capture_output=True, text=True).stdout.strip()
STACK_MODE = 'unmerged' if _b(DEV) == _b(BASE) else 'merged' if _b(DEV) == _b(H48) else 'FOREIGN'
print('  STACK MODE: %s (develop\'s %s blob %s; BASE %s; #1248 head %s)' % (STACK_MODE, F48.rsplit('/', 1)[1], _b(DEV)[:12], _b(BASE)[:12], _b(H48)[:12]))
print('  develop is %d commits ahead of BASE; the move touches %d paths:' % (len(move_log), len(move)))
for l in move_log: print('    ' + l)
for f in move: print('      moved path ' + f)
MOVE_SINCE = {}
for n, p in PRS.items():
    frm = BASE if p['parent'] == H48 else p['parent']
    allowed = {F48} if (n == '1249' and STACK_MODE == 'merged') else set()
    ms = sorted(x for x in g('diff', '--name-only', frm, DEV).splitlines() if x); MOVE_SINCE[n] = ms
    x = sorted(set(p['files']) & set(ms))
    hard(set(x) == allowed, '(3) BASE-INVARIANT: the develop move since #%s\'s parent (%s, %d paths) ∩ its OWN paths == %s (%s)' % (n, frm[:9], len(ms), sorted(allowed) or 'EMPTY', x))
if STACK_MODE == 'unmerged':
    x48 = sorted({F48} & set(move)); hard(not x48, '(3) STACK: #1248 NOT yet on develop, and the develop move ∩ #1248\'s path == EMPTY (%s)' % x48)
else:
    hard(STACK_MODE == 'merged', '(3) STACK: develop\'s blob of %s is BASE\'s (#1248 not merged) or #1248\'s head blob (#1248 SQUASHED byte-exact) — anything else is a FOREIGN move of #1249\'s path: re-predict BY HAND (mode %s)' % (F48.rsplit('/', 1)[1], STACK_MODE))
PAIR = {}
for a, b in itertools.combinations(PRS, 2):
    x = sorted(set(PRS[a]['files']) & set(PRS[b]['files'])); PAIR['%s^%s' % (a, b)] = x
    hard(not x, 'PAIRWISE path-disjoint: #%s ∩ #%s == EMPTY (%s)' % (a, b, x))
hard(sorted(set(PRS['1249']['files']) & {F48}) == [F48], 'DECLARED OVERLAP (the only one): #1248 ∩ #1249 == {%s}' % F48.rsplit('/', 1)[1])
for n in ('1249', '1251'):
    hard(not (set(PRS['1254']['files']) & (set(PRS[n]['files']) | {F48})), 'packages/shared: #1254 ∩ #%s (and #1248) == EMPTY — path-disjoint; coupling by CONTENT only, (n)' % n)
DIRS = sorted(set(f.rsplit('/', 1)[0] for n in PRS for f in PRS[n]['files']) | {F48.rsplit('/', 1)[0]})
print('  directory-level co-residence (not an overlap): %s' % [d for d in DIRS if sum(1 for n in PRS if any(f.rsplit('/', 1)[0] == d for f in PRS[n]['files'])) + (1 if d == F48.rsplit('/', 1)[0] else 0) > 1])

print('--- (c) per PR: numstat, blobs, modes; merge-tree over its GRADING BASE (develop; develop + #1248 for #1249) — checks (1) and (2)')
def mtree(a, b):
    r = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', a, b], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout.split('\n')[0].strip()
rc48, mt48 = mtree(DEV, H48) if STACK_MODE == 'unmerged' else (0, g('rev-parse', DEV + '^{tree}').strip())
hard(rc48 == 0, 'STACK: #1248 merges clean over develop (merge-tree rc %d) -> %s' % (rc48, mt48))
DEV48 = g('commit-tree', mt48, '-p', DEV, '-p', H48, '-m', 'g24b develop + #1248 (scratch only)', env=CE).strip() if (rc48 == 0 and STACK_MODE == 'unmerged') else DEV
print('  GRADING BASE for #1249: %s (%s, tree %s)' % (DEV48, 'a scratch commit: develop %s + #1248 %s' % (DEV[:9], H48[:9]) if STACK_MODE == 'unmerged' else 'develop itself: #1248 is already on it', mt48))
ns = lambda a, b: {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', a, b).strip().splitlines()}
out = {'measured_at': now(), 'simulation': SIM or 'none', 'stack_mode': STACK_MODE, 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move),
       'pairwise': PAIR, 'h1248': H48, 'dev48': DEV48, 'dev48_tree': mt48, 'prs': {}}
for n, p in PRS.items():
    h = p['head']; gb = DEV48 if n == '1249' else DEV
    nh = ns(p['parent'], h)
    hard(nh == p['files'], '#%s numstat parent..head == the pinned file set and counts (%d files)' % (n, len(p['files'])))
    rc, mt = mtree(gb, h)
    hard(rc == 0, '#%s merges clean over its grading base %s (merge-tree rc %d) -> %s' % (n, gb[:9], rc, mt))
    changed = sorted(x for x in g('diff', '--name-only', gb, mt).splitlines() if x) if rc == 0 else ['CONFLICT']
    hard(changed == sorted(p['files']), '(1) BASE-INVARIANT: diff(grading base, #%s merged) == EXACTLY its own paths (got %d)' % (n, len(changed)))
    hard(rc == 0 and ns(gb, mt) == nh, '(2) BASE-INVARIANT: numstat(grading base -> merged) == numstat(parent -> head) for #%s' % n)
    files = []
    for f in sorted(p['files']):
        lt = g('ls-tree', h, '--', f).split(); lp = g('ls-tree', p['parent'], '--', f).split(); ld = g('ls-tree', gb, '--', f).split()
        mb = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (mt, f)], capture_output=True, text=True).stdout.strip()
        hard(mb == lt[2], '(1) #%s merged blob == head blob %s: %s' % (n, lt[2], f))
        want_mode = '100755' if (lp and lp[0] == '100755') else '100644'
        hard(lt[0] == want_mode and (f in ADDED and not lp or (lp and lp[0] == lt[0])), '#%s %s mode %s at head (%s at parent) — unchanged' % (n, f.rsplit('/', 1)[1], lt[0], 'ABSENT' if not lp else lp[0]))
        hard((not lp and not ld) or (lp and ld and lp[2] == ld[2]), '#%s the grading base\'s blob of %s == the parent\'s (%s)' % (n, f.rsplit('/', 1)[1], lp[2][:12] if lp else 'ABSENT'))
        files.append({'path': f, 'mode': lt[0], 'head_blob': lt[2], 'parent_blob': lp[2] if lp else 'ABSENT', 'merged_blob': mb})
        print('    #%s %s %s (parent %s) +%d/-%d %s' % (n, lt[0], lt[2], lp[2][:12] if lp else 'ABSENT', p['files'][f][0], p['files'][f][1], f))
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json|vitest[^/]*\.config\.[tj]s|jest[^/]*\.config\.[tj]s|eslint\.config\.js|\.prettierignore|knip[^/]*)$', f)]
    hard(sorted(dep) == sorted(k for k, v in DECLARED_CONFIG.items() if v == n),
         '#%s: config files in the PR == the declared set %s (no package.json / lockfile / tsconfig / eslint / prettier / knip anywhere)' % (n, sorted(dep)))
    mb_ = BASE if p['parent'] in (BASE, H48) else p['parent']
    cmp_ = {'merge_base': mb_, 'ahead': int(g('rev-list', '--count', mb_ + '..' + h).strip()), 'behind': int(g('rev-list', '--count', mb_ + '..' + DEV).strip())}
    print('    #%s GitHub compare develop...head predicted: merge_base %s ahead %d behind %d' % (n, mb_[:12], cmp_['ahead'], cmp_['behind']))
    out['prs'][n] = {'compare': cmp_, 'head': h, 'parent': p['parent'], 'grading_base': gb, 'branch': p['branch'], 'keys': p['keys'], 'seat': p['seat'],
                     'subject': g('log', '-1', '--format=%s', h).strip(), 'merged_tree': mt, 'files': files,
                     'numstat': '%d/%d' % (sum(v[0] for v in p['files'].values()), sum(v[1] for v in p['files'].values())), 'nfiles': len(p['files'])}
rcA, mtA = mtree(DEV, PRS['1249']['head'])
nsA = ns(DEV, mtA) if rcA == 0 else {}
WANT_A = (178, 15) if STACK_MODE == 'unmerged' else (81, 14)
hard(rcA == 0 and sorted(nsA) == [F48] and nsA[F48] == WANT_A,
     'STACKED SIGNATURE: #1249 merged over develop ALONE: numstat %s == %s — %s' % (nsA, WANT_A, '#1248 + #1249 combined (GitHub\'s own 178/15): #1249 merges ONLY AFTER #1248' if STACK_MODE == 'unmerged' else '#1248 is already on develop, so #1249 alone is its own delta'))
out['r1249_alone'] = {'rc': rcA, 'tree': mtA, 'numstat': '%d/%d' % nsA.get(F48, (0, 0))}

print('--- (d) END_TREE: develop + #1248 + the seven, over SEVEN units (the stack unit S = #1248 then #1249); orders = every ORDERED PAIR of units merged first (the rest after, sorted), every rotation of the sorted order and of its reverse — prefix-memoised; + a second instrument')
# 7! = 5040 orders cost ~7 min per run (measured shape: ~13.7k merges); pairwise commutation (every ordered pair first) + every rotation both ways is the
# instrument here, and the second instrument (apply --cached) is order-free. The gate may run all 5040 in its own clone.
UNITS = {'S': ([H48] if STACK_MODE == 'unmerged' else []) + [PRS['1249']['head']]}; UNITS.update({n: [PRS[n]['head']] for n in PRS if n != '1249'})
def orders_for(us):
    us = sorted(us); o = []
    for a_, b_ in itertools.permutations(us, 2): o.append(tuple([a_, b_] + [u for u in us if u not in (a_, b_)]))
    for seq in (us, us[::-1]):
        for k in range(len(seq)): o.append(tuple(seq[k:] + seq[:k]))
    return sorted(set(o))
MEMO = {}
def chain(order, units, memo):
    memo.setdefault((), DEV)
    for k in range(1, len(order) + 1):
        pre = tuple(order[:k])
        if pre in memo: continue
        cur = memo[pre[:-1]]
        if cur.startswith('CONFLICT'): memo[pre] = cur; continue
        for hh in units[pre[-1]]:
            rc_, t_ = mtree(cur, hh)
            if rc_ != 0: cur = 'CONFLICT@' + pre[-1]; break
            cur = g('commit-tree', t_, '-p', cur, '-p', hh, '-m', 'g24b chain (scratch only)', env=CE).strip()
        memo[pre] = cur
    c = memo[tuple(order)]
    return c if c.startswith('CONFLICT') else g('rev-parse', c + '^{tree}').strip()
ORD = orders_for(UNITS)
ends = {','.join(o): chain(o, UNITS, MEMO) for o in ORD}
print('  %d orders (%d distinct prefixes merged; every ordered pair of the %d units first) -> %s' % (len(ends), len(MEMO) - 1, len(UNITS), sorted(set(ends.values()))))
e1 = list(ends.values())[0]
hard(len(set(ends.values())) == 1 and not e1.startswith('CONFLICT'), 'END_TREE identical in all %d orders' % len(ends))
def applied(base, diffs):
    idx = tempfile.mktemp(prefix='g24b_idx_', dir=os.path.dirname(CL)); ienv = dict(env, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=ienv); rcs = []
    for lab, a, b in diffs:
        ap = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached'], env=ienv, input=g('diff', '--binary', '--full-index', a, b), capture_output=True, text=True)
        rcs.append((lab, ap.returncode, ap.stderr.strip()[:120]))
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx); return t, rcs
DIFFS = ([('#1248', BASE, H48)] if STACK_MODE == 'unmerged' else []) + [('#1249', H48, PRS['1249']['head'])] + [('#' + n, PRS[n]['parent'], PRS[n]['head']) for n in PRS if n != '1249']
e3, rcs = applied(DEV, DIFFS)
for lab, rc_, err in rcs: hard(rc_ == 0, 'second instrument: apply --cached %s rc %d %s' % (lab, rc_, err))
hard(e3 == e1, 'second instrument (apply --cached, #1248 then #1249 then the rest) %s == END_TREE' % e3)
UNION = sorted(set(f for n in PRS for f in PRS[n]['files']) | {F48})
if e1.startswith('CONFLICT'):
    st = 'NONE (%s)' % e1; hard(False, 'END_TREE could not be built over this develop (%s)' % e1); e1 = e3
else:
    st = g('diff', '--shortstat', DEV, e1).strip(); print('  develop -> END_TREE:', st)
    hard(sorted(g('diff', '--name-only', DEV, e1).split()) == UNION, 'END_TREE diff vs develop == the union of the %d paths (#1248 + the seven)' % len(UNION))
    for n in PRS:
        for fe in out['prs'][n]['files']:
            eb = g('rev-parse', '%s:%s' % (e1, fe['path'])).strip()
            hard(eb == fe['head_blob'], 'END_TREE blob of %s == #%s head blob (the merged-blob target)' % (fe['path'].rsplit('/', 1)[1], n))
# the fallback END state if #1248 is NOT merged (a gate24T2a NO GO holds #1249 too): develop + the six non-stacked PRs
UN_NS = {n: [PRS[n]['head']] for n in PRS if n != '1249'}; MEMO_NS = {}
ns_ends = {','.join(o): chain(o, UN_NS, MEMO_NS) for o in orders_for(UN_NS)}
e_ns = sorted(set(ns_ends.values()))[0]
e_ns3, rcs_ns = applied(DEV, [d for d in DIFFS if d[0] not in ('#1248', '#1249')])
hard(len(set(ns_ends.values())) == 1 and not e_ns.startswith('CONFLICT') and e_ns3 == e_ns and all(r[1] == 0 for r in rcs_ns),
     'END_TREE_NOSTACK (develop + #1250 #1251 #1252 #1253 #1254 #1255 — for a #1248 NO GO, which holds #1249): %s, identical in %d orders and by apply --cached' % (e_ns, len(ns_ends)))
out['end_tree'] = e1; out['end_shortstat'] = st; out['union'] = UNION; out['end_tree_nostack'] = e_ns; out['end_orders'] = len(ends)

print('--- (e) #1249 KS-1144 (READ; stacked on #1248 — the gate grades it over develop + #1248)')
b49 = g('cat-file', 'blob', '%s:%s' % (PRS['1249']['head'], F48)); b48 = g('cat-file', 'blob', '%s:%s' % (H48, F48))
L49 = b49.split('\n'); ln = lambda L, s: [i + 1 for i, l in enumerate(L) if s in l]
LM49 = {'defaultShapesOf': ln(L49, 'const defaultShapesOf = (source: string): string[] => {'), 'J2': ln(L49, "it('J2 KS-900 — the real request-limits.ts has NO default FUNCTION export"),
        'J2_CONTROL_each': ln(L49, "])('J2 CONTROL KS-1144 — defaultShapesOf SEES $label'"), 'J2_CONTROL_all3': ln(L49, "it('J2 CONTROL KS-1144 — all three shapes at once"),
        'recorded_once': ln(L49, "'recorded once, not once per export site').toHaveLength(1)"), 'gf4_comment': ln(L49, 'KS-1144 GF-4 measured this assertion'),
        'toHaveLength3': ln(L49, 'expect(defaultShapesOf(src)).toHaveLength(3);')}
print('  line map at head: %s' % LM49)
hard(all(len(v) == 1 for v in LM49.values()), '#1249: defaultShapesOf, J2, the J2 CONTROL it.each, the all-three cell, the recorded-once line, the GF-4 comment and the length-3 assertion each occur ONCE')
cnt = lambda s: len(re.findall(r"(?m)^\s*it\(", s)) + len(re.findall(r"(?m)^\s*it\.each\(", s))
print('  it( + it.each( in the ks781 file: #1248 head %d -> #1249 head %d (the it.each carries THREE rows: +4 cells predicted, 930 -> 934 over #1248)' % (cnt(b48), cnt(b49)))
print('  LEAD LENGTH-ONLY (READ): the all-three cell asserts `.toHaveLength(3)` — the LABELS are not compared; a walk that reported one shape three times would pass it')
out['k1249'] = {'line_map': LM49}

print('--- (f) #1250 KS-1302 + KS-1303 (READ + the drafter\'s live trap probe, trapprobe_1.out: PREDICTION only)')
rh = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/run-shell-suites.sh' % PRS['1250']['head']); rb = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/run-shell-suites.sh' % BASE)
fn = rh[rh.find('rss_cleanup_tmpdir() {'):]; fn = fn[:fn.find('\n}\n') + 3]
hard('trap rss_cleanup_tmpdir EXIT INT TERM' in rh and 'trap ' not in re.sub(r'(?m)^\s*#.*$', '', rb), '#1250: the runner had NO trap at BASE; head installs `trap rss_cleanup_tmpdir EXIT INT TERM`')
hard('| tee "$rss_suite_log"' in rb and '| tee' not in re.sub(r'(?m)^\s*#.*$', '', rh) and 'bash "$REPO_ROOT/$rel" > "$rss_suite_log" 2>&1' in rh, '#1250: the `| tee` pipe is gone at head; the suite writes to its log file')
hard(bool(fn) and not re.search(r'(?m)^\s*(exit|kill)\b', fn), '#1250 LEAD TRAP-SWALLOWS-TERM (READ): rss_cleanup_tmpdir neither exits nor re-raises — a TERM/INT runs it and the runner CARRIES ON')
tb = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh' % BASE); th = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh' % PRS['1250']['head'])
cc = lambda s: len(re.findall(r'(?m)^\s*check ', s))
hard((cc(tb), cc(th)) == (49, 55), '#1250: `check` cells in run_shell_suites.test.sh BASE %d -> head %d (the fleet count run_shell_suites 49 -> 55)' % (cc(tb), cc(th)))
hard("[ \"$T1303_ELAPSED\" -lt 6 ]" in th, '#1250 LEAD TIMING-CELL (READ): the KS-1303 cell is a WALL-CLOCK cell (< 6 s) — the KS-1155 load class applies to it')
print('  no cell sends INT or TERM: %s (the seat disclosed it)' % (not re.search(r'kill\s+-(TERM|INT|15|2)\b', th)))
out['k1250'] = {'checks': [cc(tb), cc(th)]}

print('--- (g) #1251 KS-1147 (READ)')
kh = g('cat-file', 'blob', '%s:%s' % (PRS['1251']['head'], list(PRS['1251']['files'])[0])); kb = g('cat-file', 'blob', '%s:%s' % (BASE, list(PRS['1251']['files'])[0]))
NEW = r'''const host = /^\s*\\?(['"])127\.0\.0\.1\\?\1/.exec(rest);'''; OLD = r'''const host = /^\s*(['"])127\.0\.0\.1\1/.exec(rest);'''
hard(NEW in kh and OLD in kb and OLD not in kh, '#1251: the host regex gains an independent optional escape on each side (ONE product line)')
hx = re.compile(r"^\s*\\?(['\"])127\.0\.0\.1\\?\1"); ho = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
PR51 = [(lab, s, bool(ho.match(s)), bool(hx.match(s))) for lab, s in [('plain dq', ' "127.0.0.1")'), ('plain sq', " '127.0.0.1')"), ('escaped dq pair', ' \\"127.0.0.1\\")'),
        ('mismatched \\" ... "', ' \\"127.0.0.1")'), ('escaped wrong host', ' \\"0.0.0.0\\")'), ('escaped 127.0.0.10', ' \\"127.0.0.10\\")'), ('sq escaped', " \\'127.0.0.1\\')")]]
for r in PR51: print('    port %-22s %-22r BASE ok=%s HEAD ok=%s' % r)
out['k1251'] = {'rows': PR51}

print('--- (h) #1252 KS-1275 + KS-1299 (READ + a PyYAML port of preflight leg 8\'s summarise(): the legs-3/4/8-owed question)')
try:
    import yaml
    Y = 'Blockchain/Dev/docs/openapi/secuura-api.yaml'
    ld_ = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
    ya = yaml.load(g('cat-file', 'blob', '%s:%s' % (PRS['1252']['parent'], Y)), Loader=ld_); yb = yaml.load(g('cat-file', 'blob', '%s:%s' % (PRS['1252']['head'], Y)), Loader=ld_)
    M = ['get', 'put', 'post', 'delete', 'patch', 'head', 'options', 'trace']
    summ = lambda s: {'openapi': s.get('openapi'), 'version': (s.get('info') or {}).get('version'), 'paths': sorted(s.get('paths') or {}),
                      'ops': sum(1 for p in (s.get('paths') or {}) for m in M if (s['paths'][p] or {}).get(m))}
    sec = lambda s: {(p, m): json.dumps((s['paths'][p][m] or {}).get('security'), sort_keys=True) for p in (s.get('paths') or {}) for m in M if (s['paths'][p] or {}).get(m)}
    def strip_desc(o):
        if isinstance(o, dict): return {k: strip_desc(v) for k, v in o.items() if k != 'description'}
        if isinstance(o, list): return [strip_desc(v) for v in o]
        return o
    sa, sb = summ(ya), summ(yb)
    hard(sa == sb, '#1252 LEG-8 PORT: openapi / info.version / path set / operation count IDENTICAL develop -> head (%d paths, %d ops, version %s) — leg 8 compares ONLY these' % (len(sb['paths']), sb['ops'], sb['version']))
    hard(sec(ya) == sec(yb), '#1252 LEGS-3/4 PORT: every operation\'s `security` and the path set are IDENTICAL develop -> head — the inputs legs 3 and 4 read from the spec')
    hard(strip_desc(ya) == strip_desc(yb), '#1252: with every `description` removed the two specs are EQUAL — the yaml change is description-only')
    ded = sorted(set(p.rsplit('/', 1)[1] for p in (yb.get('paths') or {}) if re.fullmatch(r'/api/documents/\{id\}/[a-z-]+', p) and (yb['paths'][p] or {}).get('post')) - {'lifecycle-events'})
    lda = yb['components']['schemas']['LifecycleEventRequest']['properties']['action']['description']
    print('  dedicated POST /api/documents/{id}/<verb> routes in the head yaml: %s' % ded)
    print('  verbs named in the new description (substring, as the cell reads): %s | lifecycleActions.ts named %s | docs/VOCABULARY.md named %s' % ([v for v in ded if v in lda], 'lifecycleActions.ts' in lda, 'docs/VOCABULARY.md' in lda))
    print('  LEAD SUBSTRING-VERB (READ): the cell tests `description.includes(verb)` — a dedicated verb that is a substring of an ordinary word would red it (the safe direction)')
    out['k1252'] = {'summary_equal': sa == sb, 'dedicated': ded}
except ImportError as e:
    print('  PyYAML UNREAD (not a refusal; the gate measures): %s' % e); out['k1252'] = {'summary_equal': 'UNREAD'}
tt = g('cat-file', 'blob', '%s:Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts' % PRS['1252']['head'])
hard('DESCRIPTIONVERBLIST' not in re.sub(r'(?m)^\s*//.*$', '', tt) and tt.count("it('KS-1275 DESCRIPTIONPOINTSATSOURCE") == 1 and tt.count("it('KS-1275 EXCLUSIONHOLDS") == 1,
     '#1252: #1123\'s DESCRIPTIONVERBLIST cell is REPLACED by DESCRIPTIONPOINTSATSOURCE + EXCLUSIONHOLDS (one cell -> two: originate 869 -> 870)')
mig = subprocess.run(['git', '--git-dir', CL, 'diff', '--name-only', PRS['1252']['parent'], PRS['1252']['head'], '--', 'Blockchain/Dev/migrations', 'Blockchain/Dev/services/originate/migrations'], capture_output=True, text=True).stdout.split()
hard(not mig, '#1252 touches no migration (migrations/037 untouched, as the seat states)')

print('--- (i) #1253 KS-1297 (READ + a Python port of cell 9\'s call-site predicate: PREDICTION only)')
fg = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh' % PRS['1253']['head'])
fgb = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh' % BASE)
okc = lambda s: len(re.findall(r'(?m)^\s*ok "', s))
hard((okc(fgb), okc(fg)) == (6, 10), '#1253: `ok` cells in the fixture guard BASE %d -> head %d (the fleet count fixture_guard 6 -> 10)' % (okc(fgb), okc(fg)))
hard("C9_WRAPPED=\"$(grep -cE '(\\(|\\$\\(|\\|)[[:space:]]*build_fixture ' \"$SUBJ\")\"" in fg, '#1253: cell 9\'s predicate is the ERE `(\\(|\\$\\(|\\|)[[:space:]]*build_fixture ` (a PREFIX match only)')
subj = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh' % DEV)
TOT = re.compile(r'^[ \t]*build_fixture '); WR = re.compile(r'(\(|\$\(|\|)[ \t]*build_fixture ')
tot = sum(1 for l in subj.split('\n') if TOT.search(l)); wr = sum(1 for l in subj.split('\n') if WR.search(l))
hard((tot, wr) == (12, 0), '#1253 port over develop\'s subject: %d call sites, %d wrapped (the seat: 12 of 12 bare)' % (tot, wr))
SHAPES = [('bare (safe)', 'build_fixture "$WORK/c0" with-develop', False), ('|| true (safe)', 'build_fixture "$WORK/c0" with-develop || true', False),
          ('if (safe)', 'if build_fixture "$WORK/c0" with-develop; then :; fi', False), ('( bf ) subshell', '( build_fixture "$WORK/c0" with-develop )', True),
          ('x=$(bf)', 'x=$(build_fixture "$WORK/c0" with-develop)', True), ('bf | cat (the commit NAMES it)', 'build_fixture "$WORK/c0" with-develop | cat', True),
          ('bf & (background)', 'build_fixture "$WORK/c0" with-develop &', True), ('x=`bf` (backticks)', 'x=`build_fixture "$WORK/c0" with-develop`', True),
          ('( on its own line', '(\n  build_fixture "$WORK/c0" with-develop\n)', True), ('{ bf; } | cat', '{ build_fixture "$WORK/c0" with-develop; } | cat', True),
          ('false || bf (safe)', 'false || build_fixture "$WORK/c0" with-develop', False)]
PR53 = []
for lab, src, unsafe in SHAPES:
    flagged = sum(1 for l in src.split('\n') if WR.search(l)) > 0
    PR53.append({'shape': lab, 'unsafe': unsafe, 'flagged': flagged})
    print('    %-34s unsafe=%-5s cell-9 predicate flags=%-5s %s' % (lab, unsafe, flagged, '<-- WRONG READING' if flagged != unsafe else ''))
print('  PREDICTION (port): cell 9 MISSES %s and FLAGS the safe %s' % ([r['shape'] for r in PR53 if r['unsafe'] and not r['flagged']], [r['shape'] for r in PR53 if not r['unsafe'] and r['flagged']]))
out['k1253'] = {'shapes': PR53, 'callsites': [tot, wr]}

print('--- (n) #1254 KS-1155 (READ + a Python port of derivedTreeWalkers() over the head AND the END_TREE: PREDICTION only)')
st_ = g('cat-file', 'blob', '%s:%ssrc/__tests__/support/walkTimeouts.setup.ts' % (PRS['1254']['head'], S))
LIST = re.findall(r"^\s+'([^']+\.test\.ts)',$", st_[st_.find('TREE_WALKING_GUARDS'):st_.find('];', st_.find('TREE_WALKING_GUARDS'))], re.M)
MARK = ('readdirSync', 'DEV_ROOT', 'WALK_ROOTS')
def derived(rev):
    names = [x.rsplit('/', 1)[1] for x in g('ls-tree', '--name-only', rev, S + 'src/__tests__/').split() if x.endswith('.test.ts')]
    return sorted(n_ for n_ in names if n_ != 'walkTimeouts.test.ts' and any(m in g('cat-file', 'blob', '%s:%ssrc/__tests__/%s' % (rev, S, n_)) for m in MARK))
dh, de = derived(PRS['1254']['head']), derived(e1)
hard(dh == sorted(LIST) and len(LIST) == 7, '#1254 port: the derived walker set at head == TREE_WALKING_GUARDS (7): %s' % LIST)
hard(de == sorted(LIST), '#1254 port over the END_TREE (with #1248/#1249/#1251 in): derived == the list — the equality cell stays green after every sibling merges')
hard('vi.setConfig({ testTimeout: WALK_TIMEOUT_MS, hookTimeout: WALK_TIMEOUT_MS })' in st_ and "setupFiles: ['./src/__tests__/support/walkTimeouts.setup.ts']" in g('cat-file', 'blob', '%s:%svitest.config.ts' % (PRS['1254']['head'], S)),
     '#1254: the setup file raises testTimeout AND hookTimeout to 60 s via vi.setConfig; vitest.config.ts wires it through setupFiles')
nested = [x for x in g('ls-tree', '-r', '--name-only', e1, S + 'src/__tests__/').split() if x.endswith('.test.ts') and x.count('/') > (S + 'src/__tests__/').count('/')]
print('  LEAD NESTED (READ): *.test.ts BELOW src/__tests__/ (vitest includes them; the derivation does not look): %s' % (nested or 'NONE today'))
alt = [x for x in g('ls-tree', '--name-only', e1, S + 'src/__tests__/').split() if x.endswith('.test.ts') and x.rsplit('/', 1)[1] not in LIST
       and re.search(r'\b(readdir|opendirSync|opendir|globSync|walkSync|fg\.sync|fast-glob)\b', g('cat-file', 'blob', '%s:%s' % (e1, x)))]
print('  LEAD DERIVE-MARKERS (READ): non-listed test files that read directories through a NON-marker API: %s' % ([a.rsplit('/', 1)[1] for a in alt] or 'NONE today'))
print('  LEAD BUDGET-LEAK (UNREAD): whether vi.setConfig in a setupFile persists into the NEXT file of the same worker under --no-file-parallelism — the gate measures')
out['k1254'] = {'list': LIST, 'derived_head': dh, 'derived_end': de, 'nested': nested}

print('--- (o) #1255 KS-1301 (READ; test-only)')
F55 = list(PRS['1255']['files'])[0]
t55 = g('cat-file', 'blob', '%s:%s' % (PRS['1255']['head'], F55)); t55b = g('cat-file', 'blob', '%s:%s' % (PRS['1255']['parent'], F55))
hard(all('/__tests__/' in f for f in PRS['1255']['files']), '#1255 is TEST-ONLY: its one path is under originate/src/__tests__/ (routes/documents.ts is NOT in the PR)')
wr = re.findall(r"(?m)^  \['(/[a-z-]+)', `/api/documents/\$\{SOURCE_ID\}/", t55)
hard(wr == ['/version', '/sign-cert', '/sign-wallet'], '#1255: WRITERS carries exactly /version, /sign-cert, /sign-wallet (so PRESENCE_WRITERS == the two unpinned routes): %s' % wr)
hard("const PRESENCE_WRITERS = WRITERS.filter(([writer]) => writer !== '/version');" in t55 and t55.count("('RED KS-1301 a PRESENT %s documentType is refused") == 1 and t55.count("it('control - KS-1301 an ABSENT documentType is accepted") == 1,
     '#1255: ONE describe.each over PRESENCE_WRITERS: 3 it.each rows (null, \'\', false) + 1 control per route = 8 cells (originate 869 -> 877; the file 114 -> 122)')
docs = g('cat-file', 'blob', '%s:Blockchain/Dev/services/originate/src/routes/documents.ts' % DEV).split('\n')
GL = [i + 1 for i, l in enumerate(docs) if l.strip() == 'if (metadata.documentType !== undefined && metadata.documentType !== source.type) {']
print('  the relabel guard, byte-identical, in develop\'s routes/documents.ts at lines %s (/version, /sign-cert, /sign-wallet: the seat cites :2029 :2663 :2932)' % GL)
hard(len(GL) == 3, '#1255: the guard line occurs exactly THREE times in develop\'s documents.ts (a content tamper is ambiguous: tamper BY LINE with the other two asserted unmoved)')
out['k1255'] = {'guard_lines': GL, 'writers': wr}

print('--- (k) the fleet STOP count, READ ONLY from each PR\'s push log (anchored to each suite\'s `=== …test.sh ===` header; a NOT-FOUND control)')
def stopread(path):
    pl = open(path, encoding='utf-8', errors='replace').read()
    def after(hdr, pat=r'(\d+) passed, (\d+) failed'):
        i = pl.find(hdr); m_ = re.search(pat, pl[i:]) if i >= 0 else None
        return '%s/%s' % m_.groups() if m_ else 'NOT FOUND'
    return {'pre_push_hook_base': after('=== Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh ==='),
            'fixture_guard': after('=== Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh ==='),
            'run_shell_suites': after('=== Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh ===', r'run_shell_suites: (\d+) passed, (\d+) failed'),
            'shell_suites': (re.findall(r'shell suites: (\d+ passed, \d+ failed, \d+ skipped \(of \d+\))', pl) or ['NOT FOUND'])[-1],
            'preflight': (re.findall(r'PREFLIGHT [A-Z]+ — [^\n]*', pl) or ['NOT FOUND'])[-1], 'legs': (re.findall(r'  legs [0-9 ]+ — [^\n]*', pl) or ['NOT FOUND'])[-1],
            'fixture_build_failed': len(re.findall(r'(?m)^FIXTURE BUILD FAILED', pl)), 'control_absent_header': after('=== no_such_suite_g24b.test.sh ===')}
STOP = {}
for n in PRS:
    try:
        s_ = stopread(PUSHLOG[n]); STOP[n] = s_
        print('  #%s %s: %s' % (n, PUSHLOG[n].split('5_Project_History/')[1], s_))
        w = WANT_STOP[n]
        if n in RECORD_OVERWRITTEN:
            st0 = open(PUSHLOG[n].replace('.out', '.start'), encoding='utf-8', errors='replace').read().strip()
            print('  LEAD STOP-RECORD-OVERWRITTEN (READ): #%s\'s push log is now another push\'s (its .start reads %r; #1255\'s push ended 2026-09-25T15:04:49Z). The drafter READ #1255\'s own record COMPLETE at 15:10:16Z (predict_3.out: 28/0, 6/0, 49/0, 60 of 60, INCOMPLETE 12/15, legs 3 4 8) BEFORE the seat\'s next push reused the file name at 15:13:28Z — the gate cannot re-read it; not a refusal' % (n, st0))
            continue
        hard(all(s_[k] == w[k] for k in w) and s_['fixture_build_failed'] == 0 and s_['control_absent_header'] == 'NOT FOUND'
             and s_['preflight'].startswith('PREFLIGHT INCOMPLETE — 12/15') and s_['legs'].startswith('  legs 3 4 8 —'),
             '#%s push log: 28/0, fixture_guard %s, run_shell_suites %s, 60 of 60, INCOMPLETE 12/15 (legs 3 4 8), 0 FIXTURE BUILD FAILED (control NOT FOUND)' % (n, w['fixture_guard'], w['run_shell_suites']))
    except OSError as e:
        STOP[n] = {'error': str(e)}; print('  #%s push log UNREAD: %s (the gate reads it)' % (n, e))
out['stop'] = STOP

print('--- (l) branch names through the hyphenated-key scanner (own keys only) + the subjects vs MG-11')
for n, p in PRS.items():
    ks = sorted(set('KS-' + k for k in re.findall(r'(?i)\bks-(\d+)\b', p['branch'])))
    hard(bool(ks) and set(ks) <= set(p['keys']), '#%s branch keys %s ⊆ own %s' % (n, ks, p['keys']))
    body_ = g('log', '-1', '--format=%B', p['head']); fk = sorted(set(re.findall(r'\bKS-\d+', body_)) - set(p['keys']))
    out['prs'][n]['foreign_keys_in_body'] = fk
    print('    #%s commit body: own keys %s | FOREIGN hyphenated keys %s (a squash body must un-hyphenate them: MG-3) | Refs lines %s' % (n, sorted(set(re.findall(r'\bKS-\d+', body_)) & set(p['keys'])), fk or 'none', re.findall(r'(?m)^Refs .*$', body_)))
    sj = out['prs'][n]['subject']; print('    #%s commit subject %d chars%s: %s' % (n, len(sj), ' (> 92: MG-11 FAILS as a squash subject)' if len(sj) > 92 else '', sj))
print('--- (m) static reference counts (the gate MEASURES)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
nsuites = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots).splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
cnt_t = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', S + 'src/__tests__').splitlines() if f.endswith('.test.ts'))
out['suites'] = {'develop': nsuites(REAL_DEV), 'end': nsuites(e1)}; out['shared_files'] = {'develop': cnt_t(REAL_DEV), 'end': cnt_t(e1)}
print('  run-shell-suites.sh ROOTS `*.test.sh`: develop %d | END_TREE %d (no PR adds a suite FILE: the denominator stays 60)' % (out['suites']['develop'], out['suites']['end']))
print('  packages/shared *.test.ts: develop %d | END_TREE %d (seats: 928 develop; #1248 +2, #1249 +4, #1251 +2, #1254 +5 -> 941 predicted END; originate jest 869 -> 870 with #1252, -> 878 with #1255 too)' % (out['shared_files']['develop'], out['shared_files']['end']))
out['fail'] = len(FAIL)
name = 'pins_gate24T2b.json' if not SIM else 'pins_gate24T2b.SIM-%s.json' % SIM
with open(os.path.join(GS, name), 'w', encoding='utf-8') as f: json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, name), 'at', now()); print('HARD FAILS:', len(FAIL), FAIL)
sys.exit(1 if FAIL else 0)
