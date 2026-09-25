#!/usr/bin/env python3
"""predict_gate24T2d.py — MEASURE the round-24 CAP batch gate24T2d (#1250 KS-1302 + KS-1303 ROUND 2 OF 2, #1253 KS-1297 ROUND 2 OF 2 — both Seat L5,
both at THE CAP — #1262 KS-1310 + KS-1311, Seat B 28th, wrapped, and the four round-25 WIDENS #1263 KS-1140 (Seat L7) and #1264 KS-1281 (Seat L8), each
tier 3 comment-only, #1265 KS-1315 (Seat L7, tier 2, test-only, systemTest/performance) and #1266 KS-1120 (Seat L8, tier 2, test-only, vc-issuer),
each added by a Wednesday WIDEN message) over origin develop AS READ NOW, and write pins_gate24T2d.json beside this script. Never adopts a value from
a mail. FROZEN at SEVEN (Wednesday: "FREEZE at the next READY or at your pin"): at the re-pin 4 OPEN PRs sat on round-25 branches (#1263-#1266;
gh_read_4.out), all in the batch; the capture reads mail by message id only.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index, hash-object for a simulation) runs in a scratch BARE clone under <scratchpad>/g24d_sp/clone.git
— `git clone --bare --no-local` FROM the checkout (a plain copy through upload-pack: NO alternates into the shared object store), then a fetch FROM
ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only, never printed). Nothing is written into the
checkout.

SHAPE (measured, not assumed): #1250 is THREE commits on BASE 6e2a00bfed57 (round 1 c78f4093fb53, then R2 86ba93d25211, then R2b 2b8dcb824dd2), pushed
FAST-FORWARD (round 1 is an ancestor of the head); #1253 is TWO commits on BASE (round 1 6b88e4f03e82, then R2 91e066264004), fast-forward; #1262 is
ONE commit on develop fa25c9b10fb4 (#1248's squash); #1263, #1264, #1265 and #1266 are ONE commit each on develop 4db87c3e4b98. BASE-INVARIANT per PR over develop (Wednesday's 04:35Z ANSWER `answer_seatB25_movedbase`):
(1) diff(develop, merged) == EXACTLY the PR's own paths, each blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(parent ->
head); (3) the develop move since the PR's parent ∩ the PR's OWN paths == EMPTY. PAIRWISE the seven path sets are DISJOINT (hard); there is NO
declared overlap in this batch. The sibling kit gate24T2c's seven PRs are censused for path overlap too (READ; they may merge first).
Python ports of the changed readers (#1253's c9_scan whole-line whitelist) are READ instruments for PREDICTIONS only — never evidence; the gate
measures through the real code. The drafter's own runs of the REAL code (drafter_trapprobe_g24d.sh, drafter_readerprobe_g24d.sh,
drafter_maskprobe_g24d.sh) are PREDICTIONS too.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in 1250, 1253, 1262) builds develop + a FOREIGN edit of that PR's first
own file in the scratch clone and measures over it (a NEGATIVE CONTROL: must REFUSE); a simulation writes pins_gate24T2d.SIM-<mode>.json, never the pins.
Usage: predict_gate24T2d.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign1250|foreign1253|foreign1262|foreign1263|foreign1264|foreign1265|foreign1266]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6e2a00bfed577528de1ee02b41cb5a0e99172b35'
P62 = 'fa25c9b10fb44da6c848a6975d86ebfa523e8602'    # #1262's parent: develop at #1248's squash
RED62 = '33ccff807eb2'                              # the seat's Q6 red base for #1262: #1239's parent (resolved in full below)
P63 = '4db87c3e4b98b8e366c3dd60d5f399917bad5086'    # #1263's parent: develop at the first pin (#1255's squash)
KS879 = 'Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts'
VCR = 'Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts'
K6T = 'systemTest/performance/tests/unit/runner/k6DockerRedaction.test.ts'
VCT = 'Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts'
R1_50 = 'c78f4093fb531bceb94a8e9defb59350d8c60b73'; R1_53 = '6b88e4f03e82e3da0672efb1bb757ba5da912d6a'
RSS = 'Blockchain/Dev/scripts/run-shell-suites.sh'; RSST = 'Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh'
FG = 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh'; SUBJ = 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'
INT62 = 'Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts'
DOCS = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
PRS = {
    '1250': {'keys': ['KS-1302', 'KS-1303'], 'head': '2b8dcb824dd2c5cd4b92757934d7de9d28813a22', 'parent': BASE, 'seat': 'L5', 'round1': R1_50,
             'chain': [R1_50, '86ba93d2521139e0d3f4784517febf057665cd82', '2b8dcb824dd2c5cd4b92757934d7de9d28813a22'],
             'branch': 'refs/heads/feature/ks-1302-runner-tmpdir-residue-and-orphan-pipe-l5-1', 'files': {RSST: (166, 0), RSS: (82, 5)}},
    '1253': {'keys': ['KS-1297'], 'head': '91e066264004fdb22c67efb0c25fc44375ec6eac', 'parent': BASE, 'seat': 'L5', 'round1': R1_53,
             'chain': [R1_53, '91e066264004fdb22c67efb0c25fc44375ec6eac'],
             'branch': 'refs/heads/feature/ks-1297-fixture-guard-anchor-and-two-gaps-l5-1', 'files': {FG: (258, 3)}},
    '1262': {'keys': ['KS-1310', 'KS-1311'], 'head': '3b319485d1e3a58f30e4190a7898d7562cb80c3b', 'parent': P62, 'seat': 'B 28th', 'round1': None,
             'chain': ['3b319485d1e3a58f30e4190a7898d7562cb80c3b'],
             'branch': 'refs/heads/feature/ks-1310-transfer-custody-route-level-rollback-cell-r24-f-1', 'files': {INT62: (283, 1)}},
    '1263': {'keys': ['KS-1140'], 'head': '3c33f936fe3985ab40b72b78bda15a6959448e18', 'parent': P63, 'seat': 'L7', 'round1': None, 'tier': '3',
             'chain': ['3c33f936fe3985ab40b72b78bda15a6959448e18'],
             'branch': 'refs/heads/feature/ks-1140-ks879-docblock-figures-l7r25-1', 'files': {KS879: (25, 6)}},
    '1264': {'keys': ['KS-1281'], 'head': '2e95121dfc475a09c81d61d61f9a81148b6bb0b9', 'parent': P63, 'seat': 'L8', 'round1': None, 'tier': '3',
             'chain': ['2e95121dfc475a09c81d61d61f9a81148b6bb0b9'],
             'branch': 'refs/heads/feature/ks-1281-stale-autocreate-comment-l8r25-1', 'files': {VCR: (9, 4)}},
    '1265': {'keys': ['KS-1315'], 'head': '87ef6a1b088754ab773f541ddb273acce8dfab4f', 'parent': P63, 'seat': 'L7', 'round1': None, 'tier': '2',
             'chain': ['87ef6a1b088754ab773f541ddb273acce8dfab4f'],
             'branch': 'refs/heads/feature/ks-1315-k6-docker-redaction-sibling-rows-l7r25-1', 'files': {K6T: (35, 0)}},
    '1266': {'keys': ['KS-1120'], 'head': '952f4329de97cd7f94ab6363e670248c456d0a54', 'parent': P63, 'seat': 'L8', 'round1': None, 'tier': '2',
             'chain': ['952f4329de97cd7f94ab6363e670248c456d0a54'],
             'branch': 'refs/heads/feature/ks-1120-presentation-lookup-f1-f2-l8r25-2', 'files': {VCT: (54, 0)}},
}
SIB = {'1245': '65eb964271b0', '1256': '5a41ed7fea96', '1257': 'd1db0d41ac52', '1258': 'ff90fbf9d7e3', '1259': '8a2a28f50eb3', '1260': '62e69d23b250', '1261': 'eab8d7031b1b'}
H = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/'
PUSHLOG = {'1250': H + '2026-09-25_seatL5/raise/s-l5-ks1302-ff-push.out', '1253': H + '2026-09-25_seatL5/raise/s-l5-ks1297-ff-push.out',
           '1262': H + '2026-09-25_seatB-28th/raise/s-b28-int-push.out', '1263': H + '2026-09-26_seatL7/raise/s-l7-ks1140-3c33f936fe39-push.out',
           '1264': H + '2026-09-26_seatL8/raise/s-l8-ks1281-2e95121dfc475a09c81d61d61f9a81148b6bb0b9-push.out',
           '1265': H + '2026-09-26_seatL7/raise/s-l7-ks1315-87ef6a1b0887-push.out',
           '1266': H + '2026-09-26_seatL8/raise/s-l8-ks1120-952f4329de97cd7f94ab6363e670248c456d0a54-push.out'}
NO_PREFLIGHT = {'1265'}   # a repo-root systemTest/ push skips the 15-leg preflight entirely: its STOP count is NOT APPLICABLE (READ: the log carries only the format gate)
WANT_STOP = {'1250': {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '58/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'},
             '1253': {'pre_push_hook_base': '28/0', 'fixture_guard': '12/0', 'run_shell_suites': '49/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'},
             '1262': {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '49/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'},
             '1263': {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '49/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'},
             '1264': {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '49/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'},
             '1266': {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '49/0', 'shell_suites': '60 passed, 0 failed, 0 skipped (of 60)'}}
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
if SIM not in [''] + ['foreign' + n for n in PRS]: die('unknown simulation ' + SIM)
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate24T2d.py at', now(), '| scratchpad', SP, '| SIMULATION:', SIM or 'none (the real read)')

print('--- (a) heads and develop: ls-remote (the checkout, READ) then a fetch FROM ORIGIN into the scratch clone')
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in PRS] + [PRS[n]['branch'] for n in PRS] + ['refs/pull/%s/head' % n for n in SIB]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
print('  ls-remote at %s:' % now()); [print('    %s %s' % (v, k)) for k, v in lsd.items()]
CL = os.path.join(SP, 'g24d_sp', 'clone.git')
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL])
    run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g24d/develop']
    + ['+refs/pull/%s/head:refs/g24d/pr%s' % (n, n) for n in PRS] + ['+%s:refs/g24d/br%s' % (PRS[n]['branch'], n) for n in PRS]
    + ['+refs/pull/%s/head:refs/g24d/sib%s' % (n, n) for n in SIB if 'refs/pull/%s/head' % n in lsd], env=env)
g = lambda *a, **k: run(['git', '--git-dir', CL] + list(a), **k)
DEV = g('rev-parse', 'refs/g24d/develop').strip()
hard(DEV == lsd.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
for n, p in PRS.items():
    h = g('rev-parse', 'refs/g24d/pr' + n).strip(); b = g('rev-parse', 'refs/g24d/br' + n).strip()
    hard(h == b == lsd.get('refs/pull/%s/head' % n) == lsd.get(p['branch']) == p['head'],
         '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (n, h))
RED62F = g('rev-parse', RED62 + '^{commit}').strip()
REAL_DEV = DEV
CE = dict(env, GIT_AUTHOR_NAME='x', GIT_COMMITTER_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_EMAIL='x@x')
if SIM:
    FP = sorted(PRS[SIM[-4:]]['files'])[0]
    idx = tempfile.mktemp(prefix='g24d_sim_', dir=os.path.dirname(CL)); ienv = dict(CE, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
    blob = g('cat-file', 'blob', DEV + ':' + FP) + '\n# a FOREIGN edit of this PR\'s own file (scratch only, never pushed)\n'
    bo = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=ienv, inp=blob).strip()
    mode = g('ls-tree', DEV, '--', FP).split()[0]
    run(['git', '--git-dir', CL, 'update-index', '--cacheinfo', '%s,%s,%s' % (mode, bo, FP)], env=ienv)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
    DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + FP.rsplit('/', 1)[1], env=CE).strip()
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))

print('--- (b) ancestry: the commit CHAIN per PR (round 1 kept, fast-forward), and the develop move')
for n, p in PRS.items():
    chain = g('rev-list', '--reverse', '--topo-order', p['parent'] + '..' + p['head']).split()
    hard(chain == p['chain'], '#%s: the commits parent..head are EXACTLY %s (%d, in order)' % (n, [c[:12] for c in p['chain']], len(p['chain'])))
    single = all(len(g('rev-list', '--parents', '-n1', c).split()) == 2 for c in chain)
    hard(single, '#%s: every commit in the chain has ONE parent (no merge commit)' % n)
    if p['round1']:
        hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', p['round1'], p['head']]).returncode == 0,
             '#%s: the ROUND-1 head %s is an ancestor of the round-2 head — pushed FAST-FORWARD, no force' % (n, p['round1'][:12]))
    hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', p['parent'], DEV]).returncode == 0,
         '#%s: its parent %s is an ancestor of develop' % (n, p['parent'][:12]))
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', RED62F, BASE]).returncode == 0 and g('rev-parse', BASE + '^').strip() == RED62F,
     '#1262 red base %s is BASE^ (#1239\'s parent; #1239 is BASE %s)' % (RED62F[:12], BASE[:12]))
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('  develop is %d commits ahead of BASE; the move touches %d paths:' % (len(move_log), len(move)))
for l in move_log: print('    ' + l)
MOVE_SINCE = {}
for n, p in PRS.items():
    ms = sorted(x for x in g('diff', '--name-only', p['parent'], DEV).splitlines() if x); MOVE_SINCE[n] = ms
    x = sorted(set(p['files']) & set(ms))
    hard(not x, '(3) BASE-INVARIANT: the develop move since #%s\'s parent (%s, %d paths) ∩ its OWN paths == EMPTY (%s)' % (n, p['parent'][:9], len(ms), x))
PAIR = {}
for a, b in itertools.combinations(PRS, 2):
    x = sorted(set(PRS[a]['files']) & set(PRS[b]['files'])); PAIR['%s^%s' % (a, b)] = x
    hard(not x, 'PAIRWISE path-disjoint: #%s ∩ #%s == EMPTY (%s)' % (a, b, x))
print('  directory-level co-residence (not an overlap): scripts/__tests__/ holds #1250\'s suite and #1253\'s guard; #1250\'s runner RUNS #1253\'s guard at leg 14 (coupling by EXECUTION, not by path)')
SIBP = {}
for n in SIB:
    r = 'refs/g24d/sib' + n
    if subprocess.run(['git', '--git-dir', CL, 'rev-parse', '-q', '--verify', r], capture_output=True).returncode != 0:
        SIBP[n] = 'NOT FETCHED (closed or merged)'; continue
    mb = g('merge-base', DEV, r).strip(); SIBP[n] = sorted(x for x in g('diff', '--name-only', mb, r).splitlines() if x)
    inter = sorted(set(SIBP[n]) & set(f for q in PRS.values() for f in q['files']))
    print('  SIBLING gate24T2c #%s (%s): %d paths; ∩ this batch == %s' % (n, g('rev-parse', r).strip()[:12], len(SIBP[n]), inter or 'EMPTY'))
print('  SIBLING CONTENT COUPLINGS (READ): #1258 changes scripts/run-migrations.sh, which the gate\'s #1262 Postgres uses to migrate (use the GRADED tree\'s copy, say which); #1261\'s file comments on ks1263 still setting 127.0.0.1:1 (stale once #1262 merges)')

print('--- (c) per PR: numstat, blobs, modes; merge-tree over develop — checks (1) and (2)')
def mtree(a, b):
    r = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', a, b], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout.split('\n')[0].strip()
ns = lambda a, b: {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', a, b).strip().splitlines()}
out = {'measured_at': now(), 'simulation': SIM or 'none', 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move),
       'pairwise': PAIR, 'siblings': SIBP, 'red62': RED62F, 'prs': {}}
for n, p in PRS.items():
    h = p['head']
    nh = ns(p['parent'], h)
    hard(nh == p['files'], '#%s numstat parent..head == the pinned file set and counts (%d files)' % (n, len(p['files'])))
    rc, mt = mtree(DEV, h)
    hard(rc == 0, '#%s merges clean over develop %s (merge-tree rc %d) -> %s' % (n, DEV[:9], rc, mt))
    changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x) if rc == 0 else ['CONFLICT']
    hard(changed == sorted(p['files']), '(1) BASE-INVARIANT: diff(develop, #%s merged) == EXACTLY its own paths (got %d)' % (n, len(changed)))
    hard(rc == 0 and ns(DEV, mt) == nh, '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(parent -> head) for #%s' % n)
    files = []
    for f in sorted(p['files']):
        lt = g('ls-tree', h, '--', f).split(); lp = g('ls-tree', p['parent'], '--', f).split(); ld = g('ls-tree', DEV, '--', f).split()
        mb = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (mt, f)], capture_output=True, text=True).stdout.strip()
        hard(mb == lt[2], '(1) #%s merged blob == head blob %s: %s' % (n, lt[2], f))
        hard(bool(lp) and lp[0] == lt[0], '#%s %s mode %s at head (%s at parent) — unchanged' % (n, f.rsplit('/', 1)[1], lt[0], 'ABSENT' if not lp else lp[0]))
        hard(bool(lp) and bool(ld) and lp[2] == ld[2], '#%s develop\'s blob of %s == the parent\'s (%s)' % (n, f.rsplit('/', 1)[1], lp[2][:12] if lp else 'ABSENT'))
        r1 = g('ls-tree', p['round1'], '--', f).split()[2] if p['round1'] else None
        files.append({'path': f, 'mode': lt[0], 'head_blob': lt[2], 'parent_blob': lp[2] if lp else 'ABSENT', 'merged_blob': mb, 'round1_blob': r1})
        print('    #%s %s %s (parent %s%s) +%d/-%d %s' % (n, lt[0], lt[2], lp[2][:12] if lp else 'ABSENT', ', round 1 %s' % r1[:12] if r1 else '', p['files'][f][0], p['files'][f][1], f))
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json|vitest[^/]*\.config\.[tj]s|jest[^/]*\.config\.[tj]s|eslint\.config\.js|\.prettierignore|knip[^/]*)$', f)]
    hard(not dep, '#%s: NO config file in the PR (no package.json / lockfile / tsconfig / jest / vitest / eslint / prettier / knip) %s' % (n, dep))
    r2 = ns(p['round1'], h) if p['round1'] else {}
    if r2: print('    #%s ROUND-2 DELTA over round 1 %s: %s' % (n, p['round1'][:12], {k.rsplit('/', 1)[1]: v for k, v in r2.items()}))
    cmp_ = {'merge_base': p['parent'], 'ahead': int(g('rev-list', '--count', p['parent'] + '..' + h).strip()), 'behind': int(g('rev-list', '--count', p['parent'] + '..' + DEV).strip())}
    print('    #%s GitHub compare develop...head predicted: merge_base %s ahead %d behind %d' % (n, p['parent'][:12], cmp_['ahead'], cmp_['behind']))
    out['prs'][n] = {'compare': cmp_, 'head': h, 'parent': p['parent'], 'round1': p['round1'], 'chain': p['chain'], 'branch': p['branch'], 'keys': p['keys'], 'seat': p['seat'],
                     'subjects': [g('log', '-1', '--format=%s', c).strip() for c in p['chain']], 'merged_tree': mt, 'files': files,
                     'round2_delta': {k: '%d/%d' % v for k, v in r2.items()},
                     'numstat': '%d/%d' % (sum(v[0] for v in p['files'].values()), sum(v[1] for v in p['files'].values())), 'nfiles': len(p['files'])}

if SIM:
    print('SIMULATION %s: stops after (c) — HARD FAILS: %d %s' % (SIM, len(FAIL), FAIL))
    json.dump(dict(out, fail=len(FAIL)), open(os.path.join(GS, 'pins_gate24T2d.SIM-%s.json' % SIM), 'w'), indent=1, sort_keys=True)
    sys.exit(1 if FAIL else 0)
print('--- (d) END trees over SEVEN units: 7! = 5040 orders are too many to chain; instrument = every ORDERED PAIR merged first + every rotation of the sorted order and of its reverse (prefix-memoised) + a second instrument (apply --cached, order-free); for the four CAP VARIANTS of the GO subset (either L5 PR held)')
MEMO = {(): DEV}
def chain_tree(order):
    for k in range(1, len(order) + 1):
        pre = tuple(order[:k])
        if pre in MEMO: continue
        cur = MEMO[pre[:-1]]
        if cur.startswith('CONFLICT'): MEMO[pre] = cur; continue
        rc_, t_ = mtree(cur, PRS[pre[-1]]['head'])
        MEMO[pre] = 'CONFLICT@' + pre[-1] if rc_ != 0 else g('commit-tree', t_, '-p', cur, '-p', PRS[pre[-1]]['head'], '-m', 'g24d chain (scratch only)', env=CE).strip()
    c = MEMO[tuple(order)]
    return c if c.startswith('CONFLICT') else g('rev-parse', c + '^{tree}').strip()
def applied(base, ns_):
    idx = tempfile.mktemp(prefix='g24d_idx_', dir=os.path.dirname(CL)); ienv = dict(env, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=ienv); rcs = []
    for n in ns_:
        ap = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached'], env=ienv, input=g('diff', '--binary', '--full-index', PRS[n]['parent'], PRS[n]['head']), capture_output=True, text=True)
        rcs.append((n, ap.returncode, ap.stderr.strip()[:120]))
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx); return t, rcs
def orders_for(us):
    us = sorted(us); o = []
    for a_, b_ in itertools.permutations(us, 2): o.append(tuple([a_, b_] + [u for u in us if u not in (a_, b_)]))
    for seq in (us, us[::-1]):
        for k in range(len(seq)): o.append(tuple(seq[k:] + seq[:k]))
    return sorted(set(o))
SUBSETS = {}
NONCAP = [n for n in sorted(PRS) if n not in ('1250', '1253')]
for sub in [tuple(sorted(NONCAP + c)) for c in (['1250', '1253'], ['1253'], ['1250'], [])]:
    if True:
        ends = {','.join(o): chain_tree(o) for o in orders_for(sub)}
        e = sorted(set(ends.values()))
        t2, rcs = applied(DEV, sub)
        ok_ = len(e) == 1 and not e[0].startswith('CONFLICT') and t2 == e[0] and all(r[1] == 0 for r in rcs)
        hard(ok_, 'END over develop + {%s}: identical in all %d orders AND == apply --cached (%s)' % (' '.join('#' + s for s in sub), len(ends), e[0] if len(e) == 1 else e))
        SUBSETS['+'.join(sub)] = {'tree': e[0], 'orders': len(ends), 'shortstat': g('diff', '--shortstat', DEV, e[0]).strip() if not e[0].startswith('CONFLICT') else 'CONFLICT'}
        print('    develop + %-30s -> %s (%d orders; %s)' % ('+'.join(sub), e[0], len(ends), SUBSETS['+'.join(sub)]['shortstat']))
E1 = SUBSETS['+'.join(sorted(PRS))]['tree']
UNION = sorted(f for n in PRS for f in PRS[n]['files'])
hard(sorted(g('diff', '--name-only', DEV, E1).split()) == UNION, 'END_TREE diff vs develop == the union of the %d paths' % len(UNION))
for n in PRS:
    for fe in out['prs'][n]['files']:
        hard(g('rev-parse', '%s:%s' % (E1, fe['path'])).strip() == fe['head_blob'], 'END_TREE blob of %s == #%s head blob' % (fe['path'].rsplit('/', 1)[1], n))
out['end_tree'] = E1; out['end_shortstat'] = SUBSETS['+'.join(sorted(PRS))]['shortstat']; out['subsets'] = SUBSETS; out['union'] = UNION

print('--- (e) #1250 ROUND 2 (READ + the drafter\'s live probes trapprobe_1.out / maskprobe_1.out: PREDICTION only)')
rh = g('cat-file', 'blob', '%s:%s' % (PRS['1250']['head'], RSS)); r1 = g('cat-file', 'blob', '%s:%s' % (R1_50, RSS)); rb = g('cat-file', 'blob', '%s:%s' % (BASE, RSS))
strip = lambda s: re.sub(r'(?m)^\s*#.*$', '', s)
hard('trap rss_cleanup_tmpdir EXIT INT TERM' in r1 and 'trap rss_cleanup_tmpdir EXIT INT TERM' not in strip(rh), '#1250: round 1\'s single `trap rss_cleanup_tmpdir EXIT INT TERM` is GONE at head')
hard("trap rss_cleanup_tmpdir EXIT\n" in rh and "trap 'rss_on_signal INT' INT" in rh and "trap 'rss_on_signal TERM' TERM" in rh, '#1250: EXIT alone cleans; INT and TERM each go to rss_on_signal')
fn = rh[rh.find('rss_on_signal() {'):]; fn = fn[:fn.find('\n}\n') + 3]
hard('trap - EXIT INT TERM' in fn and 'kill -"$1" $$' in fn and 'kill -TERM "$rss_suite_pid"' in fn, '#1250: rss_on_signal cleans, removes its traps, TERMs the running suite BY PID, then RE-RAISES (`kill -"$1" $$`)')
hard('bash "$REPO_ROOT/$rel" > "$rss_suite_log" 2>&1 &' in rh and 'wait "$rss_suite_pid"' in rh, '#1250: each suite now runs BACKGROUND + `wait` (so a trapped signal interrupts at once)')
print('  LEAD RUNNER-MASKS-INT (READ + maskprobe_1.out): a suite started with `&` by a non-interactive shell gets SIGINT as SIG_IGN ON ENTRY — so EVERY suite the round-2 runner starts sees INT uninstallable (develop\'s foreground suite saw it installable). #1250\'s own INT arms therefore report UNREACHABLE under ANY run through the runner (leg 14, hook or not) — the PR\'s matrix attributes that to the hook')
print('  LEAD BG-STDIN (READ + maskprobe_1.out): a background suite\'s stdin is /dev/null (develop\'s inherited the runner\'s); a census of the 60 suites for a stdin read is owed')
print('  LEAD ORPHAN-ON-SIGNAL (trapprobe_1.out): rss_on_signal TERMs the suite\'s own bash only; a suite\'s background grandchild survives every signal arm on every runner (develop included) — pre-existing class; graded by reach (KS-1201: login_stub)')
th = g('cat-file', 'blob', '%s:%s' % (PRS['1250']['head'], RSST)); t1 = g('cat-file', 'blob', '%s:%s' % (R1_50, RSST)); tb = g('cat-file', 'blob', '%s:%s' % (BASE, RSST))
cc = lambda s: len(re.findall(r'(?m)^\s*check ', s))
print('  static `check ` lines: BASE %d | round 1 %d | head %d (the round-2 loop holds 3 check lines and runs 3 arms: runtime 55 + 3 = 58, the seat\'s count)' % (cc(tb), cc(t1), cc(th)))
hard((cc(tb), cc(t1)) == (49, 55), '#1250: BASE 49 and round-1 55 `check` lines (the gate24T2b counts)')
hard('for _sig_arm in "TERM pid" "INT pid" "INT group"; do' in th, '#1250: the round-2 cells loop over three arms: TERM pid, INT pid, INT group')
pidskip = th[th.find('if [ "$_s" = INT ] && [ "$_t" = pid ]; then'):][:400]
hard(pidskip.startswith('if [ "$_s" = INT ] && [ "$_t" = pid ]; then') and 'sig_installable' not in pidskip.split('elif')[0],
     '#1250 LEAD INT-PID-CONSTANT (READ): the INT-to-pid arm is UNREACHABLE by a CONSTANT branch — no probe runs for it, in any environment; it counts as a passed `check` (UNREACHABLE == UNREACHABLE)')
hard('set -m' in th[th.find('signal_run() {'):th.find('signal_run() {') + 1500], '#1250 LEAD RULE2-UNDER-SETM (READ): signal_run starts the runner under `set -m` — with job control ON bash does NOT ignore SIGINT in the background job; trapprobe_1.out: round 2 INT-to-pid under `set -m` rc 130, no further suite, no verdict, dir removed; round 1 and develop rc 0 + a green verdict (PREDICTION: the pid arm is REACHABLE and DISCRIMINATING in the harness\'s own shape)')
hard('[ "$T1303_ELAPSED" -lt 6 ]' in th, '#1250 N-1250-b TIMING-CELL (READ): the KS-1303 cell is still a `-lt 6` wall-clock cell — unfixed, disclosed by the seat')
out['k1250'] = {'checks_static': [cc(tb), cc(t1), cc(th)], 'runtime_declared': 58}

print('--- (f) #1253 ROUND 2 (READ + a Python port of c9_scan — PREDICTION; the drafter\'s REAL-guard run is readerprobe_1.out)')
fg = g('cat-file', 'blob', '%s:%s' % (PRS['1253']['head'], FG)); fg1 = g('cat-file', 'blob', '%s:%s' % (R1_53, FG)); fgb = g('cat-file', 'blob', '%s:%s' % (BASE, FG))
okc = lambda s: len(re.findall(r'(?m)^\s*ok "', s))
print('  static `ok "` lines: BASE %d | round 1 %d | head %d (the seat: 6 -> 10 -> 12)' % (okc(fgb), okc(fg1), okc(fg)))
hard((okc(fgb), okc(fg1), okc(fg)) == (6, 10, 12), '#1253: `ok` cells BASE 6 -> round 1 10 -> head 12 (fixture_guard 12/0 after merge)')
hard('c9_scan() {' in fg and "if (l !~ /^build_fixture \"[^\"]*\" [a-z-]+$/) { bad++; continue }" in fg, '#1253: cell 9 is now a WHOLE-LINE whitelist `^build_fixture "[^"]*" [a-z-]+$` + ONE line of context')
c10 = fg[fg.find('# CELL 10'):fg.find('# CELL 11')]
hard("C10_OR_FLAGGED=\"$(grep -cE '(\\(|\\$\\(|\\|)[[:space:]]*build_fixture ' \"$C10_OR\")\"" in c10 and 'c9_scan' not in c10,
     '#1253 LEAD STALE-CONTROL (READ): cell 10 still computes the ROUND-1 ERE, not c9_scan — its `ok` text ("cell 9\'s predicate ... does NOT fire on the measurably-safe `|| true` shape") describes a predicate that no longer exists')
c12 = fg[fg.find('# CELL 12'):]
hard('C12_DETAIL="$C12_DETAIL $_name=$([ "$_bare" -lt "$_occ" ] && echo not-bare || echo bare)"' in c12,
     '#1253 LEAD SAFE-SHAPES-FLAGGED (READ): cell 12 RECORDS the flag state of `|| true` / `false || bf` and asserts only their behaviour — it never asserts they are NOT flagged (the round-1 HOLD line required "each not flagged")')
def c9(src):
    L = src.split('\n'); occ = bad = 0
    for i, l in enumerate(L):
        if re.match(r'^[ \t]*#', l) or re.match(r'^[ \t]*build_fixture\(\)', l) or 'build_fixture' not in l: continue
        occ += 1
        if not re.match(r'^build_fixture "[^"]*" [a-z-]+$', l): bad += 1; continue
        prev = ''
        for j in range(i - 1, -1, -1):
            if re.match(r'^[ \t]*$', L[j]) or re.match(r'^[ \t]*#', L[j]): continue
            prev = L[j]; break
        if re.match(r'^[ \t]*[({][ \t]*$', prev) or re.search(r'(\||&&|\|\||\\)[ \t]*$', prev): bad += 1
    return occ, bad
subj = g('cat-file', 'blob', '%s:%s' % (DEV, SUBJ))
hard(c9(subj) == (12, 0), '#1253 port over develop\'s subject: %s occurrences:offending (the seat: 12 of 12 bare)' % (c9(subj),))
A = 'build_fixture "$WORK/c2" with-develop'
SHAPES = [('bare', A, False), ('bf | cat (named, round-1 commit)', A + ' | cat', True), ('{ bf; } | cat', '{ ' + A + '; } | cat', True), ('x=`bf`', 'x=`' + A + '`', True),
          ('( on its own line', '(\n' + A + '\n)', True), ('bf &', A + ' &\nwait', True), ('bf || true (named SAFE)', A + ' || true', False), ('false || bf (named SAFE)', 'false || ' + A, False),
          ('if bf; then (named SAFE, PR table)', 'if ' + A + '; then :; fi', False), ('bf && : (named SAFE, PR table)', A + ' && :', False),
          ('x=$( on the line above (cmd-sub class, named)', 'x=$(\n' + A + '\n)', True), ('( : noop on the line above', '( : noop\n' + A + '\n)', True),
          ('( two lines above (DECLARED boundary)', '(\n  : noop\n' + A + '\n)', True)]
PR53 = []
for lab, sh, unsafe in SHAPES:
    o, b = c9(subj.replace('\n' + A + '\n', '\n' + sh + '\n', 1)); flagged = b > 0
    PR53.append({'shape': lab, 'unsafe': unsafe, 'flagged': flagged})
    print('    %-48s unsafe=%-5s cell 9 flags=%-5s %s' % (lab, unsafe, flagged, '<-- WRONG READING' if flagged != unsafe else ''))
print('  PREDICTION (port; readerprobe_1.out agrees through the REAL guard): cell 9 FLAGS the named-safe %s and MISSES %s' % ([r['shape'] for r in PR53 if not r['unsafe'] and r['flagged']], [r['shape'] for r in PR53 if r['unsafe'] and not r['flagged']]))
out['k1253'] = {'shapes': PR53, 'ok_static': [okc(fgb), okc(fg1), okc(fg)]}

print('--- (g) #1262 KS-1310 + KS-1311 (READ: the DB cell\'s own guards; the red base)')
t62 = g('cat-file', 'blob', '%s:%s' % (PRS['1262']['head'], INT62))
hard("!(port >= 55410 && port <= 55419)" in t62 and "['127.0.0.1', 'localhost'].includes(dsn.hostname)" in t62, '#1262: the KS-1310 describe REFUSES unless DEFAULT_DB is 127.0.0.1/localhost on 55410-55419 (LEAD LOCALHOST-ALSO: `localhost` is admitted too)')
hard('const DEFAULT_DB = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;' in t62 and 'PLATFORM_DB' in t62 and 'PLATFORM_DB' not in t62[t62.find('CONDITION 4'):t62.find('CONDITION 4') + 900],
     '#1262 LEAD REFUSAL-SCOPE (READ): the refusal reads DEFAULT_DB only, inside the KS-1310 describe — the PLATFORM URL and the file\'s two earlier describes (DML) are not gated by it; the gate sets EVERY DB variable to its own :55419')
hard(t62.count('BEFORE UPDATE ON documents') == 1 and "WHEN (OLD.id = '${CUSTODY_DOC_UUID}'::uuid)" in t62 and 'expect(logged).toContain(FLIP_MSG);' in t62 and 'expect(await triggerRows()).toBe(0);' in t62,
     '#1262: ONE BEFORE UPDATE trigger on documents, scoped by WHEN to the cell\'s document; the route\'s logged error must carry FLIP_MSG; pg_trigger + pg_proc == 0 after')
hard(subprocess.run(['git', '--git-dir', CL, 'cat-file', '-e', '%s:%s' % (RED62F, INT62)], capture_output=True).returncode != 0, '#1262: the integration file is ABSENT at the red base %s (#1239 added it): the red arm plants the head file into that tree' % RED62F[:12])
wt = lambda rev: len(re.findall(r'\bwithTenant\(', g('cat-file', 'blob', '%s:%s' % (rev, DOCS))))
print('  withTenant( in routes/documents.ts: red base %s %d | BASE %d | develop %d (the seat: "0 withTenant calls" at the red base)' % (RED62F[:12], wt(RED62F), wt(BASE), wt(DEV)))
hard(wt(RED62F) == 0 and wt(DEV) > 0, '#1262: the red base has 0 withTenant( calls in documents.ts; develop has %d' % wt(DEV))
print('  LEAD OWNER-UNASSERTED-AT-BASE (READ b28-1310-BASE.out): the red stops at the custody count (:658); "the owner unflipped" is the NEXT expect (:659) and never ran at the red base — the gate measures it by a probe')
print('  LEAD MODE-F-NOT-RUN (READ): the seat ran MULTI_TENANCY_ENABLED=true only (KS-1305: no generated Prisma client in a fresh worktree) — declared scope')
out['k1262'] = {'red_base': RED62F, 'withtenant': [wt(RED62F), wt(BASE), wt(DEV)]}

print('--- (h) #1263 KS-1140 (TIER 3, comment-only: READ + a line-level port — the gate proves it through the TypeScript emit)')
d63 = g('diff', '-U0', P63, PRS['1263']['head'], '--', KS879)
chg = [l[1:] for l in d63.split('\n') if (l.startswith('+') or l.startswith('-')) and not l.startswith('+++') and not l.startswith('---')]
iscom = lambda s: bool(re.match(r'^\s*(\*|//|/\*)', s)) or s.strip() == ''
hard(len(chg) == 31 and all(iscom(s) for s in chg), '#1263: all %d changed lines in `git diff -U0` are comment lines (` *` / `//`) — the seat: 31 (a PORT; the gate proves it by the emit)' % len(chg))
b63 = g('cat-file', 'blob', '%s:%s' % (PRS['1263']['head'], KS879)); p63 = g('cat-file', 'blob', '%s:%s' % (P63, KS879))
strip_c = lambda s: re.sub(r'(?m)^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', s, flags=re.S))
hard(re.sub(r'\s+', '', strip_c(b63)) == re.sub(r'\s+', '', strip_c(p63)), '#1263 PORT: with /* */ and whole-line // comments stripped and whitespace removed, parent == head (the gate owes the real emit: `transpileModule` with removeComments)')
hard('toBeGreaterThan(1_000)' in b63 and 'toBeGreaterThan(5_000_000)' in b63, '#1263: the walk CONTROL floors (> 1_000 files, > 5_000_000 bytes) are present at head')
cb = lambda s: sum(1 for ch in s.encode('utf-8', 'surrogateescape') if (ch < 0x20 and ch not in (0x09, 0x0a, 0x0d)) or ch == 0x7f)
for n in PRS:
    for f in PRS[n]['files']:
        if f.endswith(('.ts', '.tsx', '.js', '.mjs', '.cjs')):
            hard(cb(g('cat-file', 'blob', '%s:%s' % (PRS[n]['head'], f))) == 0, 'ks879 COUPLING (READ port of rawControlBytes): #%s %s carries 0 raw control bytes — the ks879 walk over the END tree stays green' % (n, f.rsplit('/', 1)[1]))
print('  LEAD MAGIC-WORD-CLOSES (READ gh_read_2.out + linear_reads_2.out): #1263\'s PR body says "This does not close KS-1140\'s GF-1" — Linear parsed the magic word: the attachment is linkKind `closes`, not `contributes`, and the body\'s only Refs is inside backticks; a squash would close KS-1140 though the READY says the ticket stays In Progress')
print('  LEAD CENSUS-CLAIM (READ): the new comment asserts "1,429 files / 14,178,318 B" at 4db87c3e4b98, measured by the file\'s own sourceFiles on an extract — a prose claim no assertion reads; the gate may re-measure it through the real walk, never grade it as code')
out['k1263'] = {'changed_lines': len(chg)}

print('--- (h2) #1264 KS-1281 (TIER 3, comment-only, a PRODUCT file: READ + a line-level port — the gate proves it through the TypeScript emit)')
d64 = g('diff', '-U0', P63, PRS['1264']['head'], '--', VCR)
chg4 = [l[1:] for l in d64.split('\n') if (l.startswith('+') or l.startswith('-')) and not l.startswith('+++') and not l.startswith('---')]
hard(len(chg4) == 13 and all(iscom(s) for s in chg4), '#1264: all %d changed lines in `git diff -U0` are comment lines — a PORT; the gate proves it by the emit (the seat: EQUIVALENT, 6490 vs 6490 bytes)' % len(chg4))
b64 = g('cat-file', 'blob', '%s:%s' % (PRS['1264']['head'], VCR)); p64 = g('cat-file', 'blob', '%s:%s' % (P63, VCR))
hard(re.sub(r'\s+', '', strip_c(b64)) == re.sub(r'\s+', '', strip_c(p64)), '#1264 PORT: comment-stripped, whitespace removed, parent == head')
et = b64[b64.find('ensureTable'):]; et = et[:et.find('\n}\n') + 3] if '\n}\n' in et else et[:2000]
hard('CREATE TABLE' not in strip_c(b64).upper() or 'CREATE TABLE' not in strip_c(et).upper(), '#1264 COMMENT-CLAIMS (READ): ensureTable() issues no `CREATE TABLE` in code (the comment says "an existence check and issues no DDL")')
m001 = g('cat-file', 'blob', '%s:Blockchain/Dev/migrations/001_initial-schema.sql' % DEV); i03 = g('cat-file', 'blob', '%s:Blockchain/Dev/docker/init/03-service-tables.sql' % DEV)
hard('CREATE TABLE IF NOT EXISTS vc_credentials_store' in m001 and 'CREATE TABLE IF NOT EXISTS vc_credentials_store' in i03, '#1264 COMMENT-CLAIMS (READ): migrations/001_initial-schema.sql AND docker/init/03-service-tables.sql both create vc_credentials_store — the files the new comment names')
print('  LEAD COMMENT-CLAIMS (READ): "because the runtime role has no CREATE on schema `public`" is a claim about a DEPLOYED grant — UNMEASURED here (the seat names the Azure reach and the role check as UNMEASURED)')
out['k1264'] = {'changed_lines': len(chg4)}

print('--- (h3) #1265 KS-1315 and #1266 KS-1120 (READ; test-only; the gate re-runs the red proofs)')
k6 = g('cat-file', 'blob', '%s:systemTest/performance/runner/k6_docker.ts' % DEV)
T1 = 'return masked === arg ? maskOneArgumentForms(arg) : masked;'
hard(k6.count(T1) == 1, '#1265: the T-1 target (QA-961-1 fallthrough) occurs ONCE in develop\'s runner/k6_docker.ts — the tamper is `%s` -> `return masked;`' % T1)
t65 = g('cat-file', 'blob', '%s:%s' % (PRS['1265']['head'], K6T))
rows = re.findall(r"label: '[^']*\(QA-961-1 (L0[1457])\)'", t65)
hard(sorted(set(rows) & {'L01', 'L04', 'L05', 'L07'}) == ['L01', 'L04', 'L05', 'L07'] and "-eKEY=ks1315-l04-3a07" in t65, '#1265: the four new rows L05 / L07 / L04 / L01 are in the `masks $label` table; L04 is named `KEY` exactly (the naming arm: -eADMIN_PASSWORD is masked by accident)')
d66 = g('diff', '--name-only', P63, PRS['1266']['head'])
hard(d66.split() == [VCT], '#1266 is TEST-ONLY (one test file; routes/presentations.ts is NOT in the PR) — Wednesday\'s message called it "a PRODUCT change": the diff says test-only, tier 2')
t66 = g('cat-file', 'blob', '%s:%s' % (PRS['1266']['head'], VCT))
hard('storedId.startsWith(id)' in t66 or 'startsWith(' in t66, '#1266 X1 (F-1) asserts the id it sends is a PREFIX of the stored id (the cell cannot pass on a non-prefix)')
print('  #1266 X2 (F-2): the row is made memory-only by rejecting the INSERT (storePresentation\'s real catch); the seat\'s tamper script raise/tamper_ks1120.py (T4 startsWith scan re-inserted; T5 `return undefined` after the DB miss) — the gate re-runs both at head AND at develop without the cells (the seat: 131/0; T4 130/1 X1 only; T5 130/1 X2 only; develop 129/129 under both)')
out['k1265'] = {'rows': sorted(set(rows))}

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
            'fixture_build_failed': len(re.findall(r'(?m)^FIXTURE BUILD FAILED', pl)), 'control_absent_header': after('=== no_such_suite_g24d.test.sh ==='),
            'signal_env': re.findall(r'signal environment: [^)\n]*', pl), 'unreachable_cells': len(re.findall(r'UNREACHABLE here, measured', pl))}
STOP = {}
for n in PRS:
    try:
        s_ = stopread(PUSHLOG[n]); STOP[n] = s_
        st0 = open(PUSHLOG[n].replace('.out', '.start'), encoding='utf-8').read().strip(); en0 = open(PUSHLOG[n].replace('.out', '.end'), encoding='utf-8').read().strip()
        print('  #%s %s [%s .. %s]: %s' % (n, PUSHLOG[n].split('5_Project_History/')[1], st0, en0, s_))
        if n in NO_PREFLIGHT:
            pl_ = open(PUSHLOG[n], encoding='utf-8', errors='replace').read()
            hard('PREFLIGHT' not in pl_ and 'format:check OK' in pl_ and open(PUSHLOG[n].replace('.out', '.rc')).read().strip() == '0',
                 '#%s push log: NO preflight ran (a systemTest/ push), only the format gate — its fleet STOP count is NOT APPLICABLE' % n)
            continue
        w = WANT_STOP[n]
        hard(all(s_[k] == w[k] for k in w) and s_['fixture_build_failed'] == 0 and s_['control_absent_header'] == 'NOT FOUND'
             and s_['preflight'].startswith('PREFLIGHT INCOMPLETE — 12/15') and s_['legs'].startswith('  legs 3 4 8 —'),
             '#%s push log: 28/0, fixture_guard %s, run_shell_suites %s, 60 of 60, INCOMPLETE 12/15 (legs 3 4 8), 0 FIXTURE BUILD FAILED (control NOT FOUND)' % (n, w['fixture_guard'], w['run_shell_suites']))
    except OSError as e:
        STOP[n] = {'error': str(e)}; print('  #%s push log UNREAD: %s (the gate reads it)' % (n, e))
hard(STOP.get('1250', {}).get('signal_env') == ['signal environment: INT installable=no, TERM installable=yes'] and STOP['1250'].get('unreachable_cells') == 2,
     '#1250\'s own leg-14 run (in-hook): `INT installable=no` and 2 UNREACHABLE cells — so of its 58 in-hook passes, 2 assert nothing')
out['stop'] = STOP

print('--- (l) branch names through the hyphenated-key scanner (own keys only), every commit body, and the subjects vs MG-11')
for n, p in PRS.items():
    ks = sorted(set('KS-' + k for k in re.findall(r'(?i)\bks-(\d+)\b', p['branch'])))
    hard(bool(ks) and set(ks) <= set(p['keys']), '#%s branch keys %s ⊆ own %s' % (n, ks, p['keys']))
    fk = set()
    for c in p['chain']:
        body_ = g('log', '-1', '--format=%B', c); f_ = sorted(set(re.findall(r'\bKS-\d+', body_)) - set(p['keys'])); fk |= set(f_)
        sj = g('log', '-1', '--format=%s', c).strip()
        print('    #%s %s subject %d chars%s | FOREIGN hyphenated keys %s | Refs %s' % (n, c[:12], len(sj), ' (> 92)' if len(sj) > 92 else '', f_ or 'none', re.findall(r'(?m)^Refs .*$', body_)))
    out['prs'][n]['foreign_keys_in_commits'] = sorted(fk)
print('--- (m) static reference counts (the gate MEASURES)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
nsuites = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots).splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
out['suites'] = {'develop': nsuites(REAL_DEV), 'end': nsuites(E1)}
print('  run-shell-suites.sh ROOTS `*.test.sh`: develop %d | END_TREE %d (no PR adds a suite FILE: the denominator stays 60)' % (out['suites']['develop'], out['suites']['end']))
hard(out['suites'] == {'develop': 60, 'end': 60}, 'the shell-suite denominator is 60 at develop and at END')
itf = sorted(f.rsplit('/', 1)[1] for f in g('ls-tree', '-r', '--name-only', REAL_DEV, '--', 'Blockchain/Dev/services/originate/src').splitlines() if f.endswith('.integration.test.ts'))
print('  originate *.integration.test.ts at develop: %s (the gate runs ONLY ks1263; the others are censused, not run)' % itf)
out['fail'] = len(FAIL)
name = 'pins_gate24T2d.json' if not SIM else 'pins_gate24T2d.SIM-%s.json' % SIM
with open(os.path.join(GS, name), 'w', encoding='utf-8') as f: json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, name), 'at', now()); print('HARD FAILS:', len(FAIL), FAIL)
sys.exit(1 if FAIL else 0)
