#!/usr/bin/env python3
"""predict_gate24T2c.py — MEASURE the round-24 THIRD tier-2 batch gate24T2c (#1245 KS-1313 ROUND 2 OF 2 — THE CAP ROUND, #1256 KS-1159, #1257 KS-1201,
#1258 KS-1296, #1259 KS-906, #1260 KS-1139, #1261 KS-1293 — FROZEN at seven; Seats L6, L5, B 28th) over origin develop AS READ NOW, and write
pins_gate24T2c.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index, hash-object for a simulation) runs in a scratch BARE clone under <scratchpad>/g24c_sp/clone.git
— `git clone --bare --no-local` FROM the checkout (NO alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as
GIT_SSH_COMMAND for the clone only, never printed). Nothing is written into the checkout.

PARENTS (measured, not assumed): #1245 is TWO commits on BASE 6e2a00bfed57 (round 1 1700b5ae7dd5, then round 2 65eb964271b0); #1257, #1258, #1259,
#1260 are ONE commit each on BASE; #1256 is ONE commit on develop 77c6426b96d9; #1261 is ONE commit on develop fa25c9b10fb4. BASE-INVARIANT per PR
(Wednesday's 04:35Z ANSWER `answer_seatB25_movedbase`) over develop: (1) diff(develop, merged) == EXACTLY the PR's own paths at the head's blobs;
(2) numstat(develop -> merged) == numstat(parent -> head); (3) the develop move since the PR's parent ∩ its OWN paths == EMPTY. THERE IS NO DECLARED
OVERLAP. PAIRWISE the seven path sets are DISJOINT (hard), AND the seven ∩ the RUNNING sibling batch gate24T2b's seven (+ #1248's path) == EMPTY
(hard): so a gate24T2b squash is a develop move that touches none of this batch's paths and the repin re-derives over it (control P-T2Bm).
Ports of changed readers (#1256's guard, #1261's CONFIGPINNED) and the drafter's live probe of #1245 (drafter_liveshape_g24c.py) are PREDICTIONS only.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the seven) builds develop + a FOREIGN edit of that PR's own file (NEGATIVE:
must REFUSE); --simulate mergedT2b builds develop + a squash of each of gate24T2b's seven heads (POSITIVE: must re-pin, and the fleet STOP read from
that develop moves to fixture_guard 10 / run_shell_suites 55). A simulation writes pins_gate24T2c.SIM-<mode>.json, never the pins.
Usage: predict_gate24T2c.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign1245|...|foreign1261|mergedT2b]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6e2a00bfed577528de1ee02b41cb5a0e99172b35'
DEV77 = '77c6426b96d9e48a758e68fa56e9138dc8509aa8'
DEVFA = 'fa25c9b10fb44da6c848a6975d86ebfa523e8602'
R1_1245 = '1700b5ae7dd56ad3e30602a40b20ae6469c35350'   # #1245 round 1 (gate24T2a NO GO B-1245-1); round 2 sits on it
P = 'systemTest/performance/'
F45 = P + 'tests/unit/utils/unitSuiteSlotIndependence.test.ts'; C45 = P + 'tests/unit/support/capturedChildOutput.ts'
O = 'Blockchain/Dev/services/originate/src/__tests__/'
PRS = {
    '1245': {'keys': ['KS-1313'], 'head': '65eb964271b0d6895e90fe8f5ffcbbbb9a484050', 'chain': [R1_1245], 'base': BASE, 'seat': 'L6',
             'branch': 'refs/heads/feature/ks-1313-readsuitecounts-label-set-l6-r24-1', 'files': {C45: (42, 0), F45: (346, 6)}},
    '1256': {'keys': ['KS-1159'], 'head': '5a41ed7fea96ab77ed1dc263ae0c7d25c9846440', 'chain': [], 'base': DEV77, 'seat': 'B 28th',
             'branch': 'refs/heads/feature/ks-1159-ks1061-guard-blind-spots-r24-d-1', 'files': {O + 'ks1061-shared-mock-completeness.test.ts': (29, 8)}},
    '1257': {'keys': ['KS-1201'], 'head': 'd1db0d41ac52359c231cd22abf11124204645d97', 'chain': [], 'base': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-1201-login-stub-parent-shell-l5-1', 'files': {'systemTest/__tests__/bootstrap_login_diagnosis.test.sh': (64, 8)}},
    '1258': {'keys': ['KS-1296'], 'head': 'ff90fbf9d7e351104404e3eaad505a673e656c1e', 'chain': [], 'base': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-1296-pg-isready-missing-binary-l5-1',
             'files': {'Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh': (77, 2), 'Blockchain/Dev/scripts/run-migrations.sh': (24, 0)}},
    '1259': {'keys': ['KS-906'], 'head': '8a2a28f50eb3453db7284da0f098f6a819d40145', 'chain': [], 'base': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-906-case6-inert-cd-l5-1', 'files': {'Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh': (31, 3)}},
    '1260': {'keys': ['KS-1139'], 'head': '62e69d23b2507780316f1930123c7d57ebba3ae2', 'chain': [], 'base': BASE, 'seat': 'L5',
             'branch': 'refs/heads/feature/ks-1139-sync-secrets-arith-errexit-l5-1', 'files': {'Blockchain/Dev/deployment/azure/sync-secrets.sh': (8, 8)}},
    '1261': {'keys': ['KS-1293'], 'head': 'eab8d7031b1b19071a66715ca0aabd9c5cb29c6d', 'chain': [], 'base': DEVFA, 'seat': 'B 28th',
             'branch': 'refs/heads/feature/ks-1293-pin-originate-suite-hermeticity-r24-e-1', 'files': {O + 'ks1293-originate-suite-is-hermetic.test.ts': (157, 0)}},
}
ADDED = {C45, O + 'ks1293-originate-suite-is-hermetic.test.ts'}
DECLARED_CONFIG = {}   # no config file in this batch
# the RUNNING sibling batch gate24T2b (launched 16:18:43Z over fa25c9b1): heads + own paths, as its pins_gate24T2b.json read at 16:2xZ (READ); #1248 is
# already squashed onto fa25c9b1 (its path is listed so a foreign move of it would still be seen)
T2B = {'1249': ('6eb283d058184f1f0fabdc3c3184a817db4fb94b', ['Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts']),
       '1250': ('c78f4093fb531bceb94a8e9defb59350d8c60b73', ['Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh', 'Blockchain/Dev/scripts/run-shell-suites.sh']),
       '1251': ('8020adae99129f4b7194fef32f1ea5b762819d90', ['Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts']),
       '1252': ('ca7337fa04e04e5438bc79a5abe215424fcb33ef', ['Blockchain/Dev/docs/openapi/secuura-api.yaml', O + 'ks978-published-contract-organizationuuid.test.ts', 'Blockchain/Dev/services/originate/src/originate.openapi.ts']),
       '1253': ('6b88e4f03e82e3da0672efb1bb757ba5da912d6a', ['Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh']),
       '1254': ('da0c94968a7423c340b3a3b76244bda536d1f6d2', ['Blockchain/Dev/packages/shared/src/__tests__/support/walkTimeouts.setup.ts', 'Blockchain/Dev/packages/shared/src/__tests__/walkTimeouts.test.ts', 'Blockchain/Dev/packages/shared/vitest.config.ts']),
       '1255': ('59245ff0b11c6b760ba5e2a9daedc5927e915e10', [O + 'ks1213-a-derived-writer-relabel-is-refused.test.ts'])}
T2B_ALSO = ['Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts']   # #1248 (already on develop)
H = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/'
PUSHLOG = {'1245': (H + '2026-09-25_seatL6/raise/s-l6-ks1313-ff-push.out', 'format-gate'),
           '1256': (H + '2026-09-25_seatB-28th/raise/s-b28-cells-push.out', 'overwritten'),
           '1257': (H + '2026-09-25_seatL5/raise/s-l5-ks1201-push.out', 'early-return'),
           '1258': (H + '2026-09-25_seatL5/raise/s-l5-ks1296-push.out', 'preflight'),
           '1259': (H + '2026-09-25_seatL5/raise/s-l5-ks906-push.out', 'preflight'),
           '1260': (H + '2026-09-25_seatL5/raise/s-l5-ks1139-push.out', 'preflight'),
           '1261': (H + '2026-09-25_seatB-28th/raise/s-b28-cells-push.out', 'preflight')}
SUITE = {'pre_push_hook_base': ('=== Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh ===', r'(\d+) passed, (\d+) failed'),
         'fixture_guard': ('=== Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh ===', r'(\d+) passed, (\d+) failed'),
         'run_shell_suites': ('=== Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh ===', r'run_shell_suites: (\d+) passed, (\d+) failed'),
         'run_migrations_failure_exit_code': ('=== Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh ===', r'run_migrations_failure_exit_code: (\d+) passed, (\d+) failed'),
         'no_tracked_credentials_root': ('=== Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh ===', r'(\d+) passed, (\d+) failed'),
         'bootstrap_login_diagnosis': ('=== systemTest/__tests__/bootstrap_login_diagnosis.test.sh ===', r'bootstrap_login_diagnosis\.test\.sh: (\d+) passed, (\d+) failed')}
BASE_WANT = {'pre_push_hook_base': '28/0', 'fixture_guard': '6/0', 'run_shell_suites': '49/0', 'run_migrations_failure_exit_code': '5/0',
             'no_tracked_credentials_root': '15/0', 'bootstrap_login_diagnosis': '16/0'}
WANT_STOP = {n: dict(BASE_WANT) for n in PRS}
WANT_STOP['1258']['run_migrations_failure_exit_code'] = '7/0'; WANT_STOP['1259']['no_tracked_credentials_root'] = '16/0'
# #1256's push record (s-b28-cells-push.out, .start 2026-09-25T15:13:28Z) was OVERWRITTEN by #1261's push from 15:50:24Z. The only surviving reads are
# gate24T2b's drafter's predict_5/6/7.out (15:23Z / 15:29Z / 15:46Z), which read that file under the label #1255 (their own overwritten record):
T2B_KIT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2b/'
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
if SIM not in ['', 'mergedT2b'] + ['foreign' + n for n in PRS]: die('unknown simulation ' + SIM)
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate24T2c.py at', now(), '| scratchpad', SP, '| SIMULATION:', SIM or 'none (the real read)')

print('--- (a) heads and develop: ls-remote (the checkout, READ) then a fetch FROM ORIGIN into the scratch clone')
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in PRS] + [PRS[n]['branch'] for n in PRS] + ['refs/pull/%s/head' % n for n in T2B]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
print('  ls-remote at %s:' % now()); [print('    %s %s' % (v, k)) for k, v in lsd.items()]
CL = os.path.join(SP, 'g24c_sp', 'clone.git')
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL])
    run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g24c/develop']
    + ['+refs/pull/%s/head:refs/g24c/pr%s' % (n, n) for n in list(PRS) + list(T2B)] + ['+%s:refs/g24c/br%s' % (PRS[n]['branch'], n) for n in PRS], env=env)
g = lambda *a, **k: run(['git', '--git-dir', CL] + list(a), **k)
DEV = g('rev-parse', 'refs/g24c/develop').strip()
hard(DEV == lsd.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
for n, p in PRS.items():
    h = g('rev-parse', 'refs/g24c/pr' + n).strip(); b = g('rev-parse', 'refs/g24c/br' + n).strip()
    hard(h == b == lsd.get('refs/pull/%s/head' % n) == lsd.get(p['branch']) == p['head'],
         '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (n, h))
for n, (h, _) in T2B.items():
    print('  sibling gate24T2b #%s refs/pull/%s/head %s (%s)' % (n, n, (lsd.get('refs/pull/%s/head' % n) or 'ABSENT')[:12], 'the pin' if lsd.get('refs/pull/%s/head' % n) == h else 'MOVED since its pin — context only'))
REAL_DEV = DEV
CE = dict(env, GIT_AUTHOR_NAME='x', GIT_COMMITTER_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_EMAIL='x@x')
def mtree(a, b):
    r = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', a, b], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout.split('\n')[0].strip()
if SIM == 'mergedT2b':   # a POSITIVE simulation: gate24T2b's seven squash-merged onto develop, one parent each (as a squash lands)
    for n, (h, _) in T2B.items():
        rc_, t_ = mtree(DEV, h)
        if rc_ != 0: die('SIMULATION: gate24T2b #%s does not merge over %s' % (n, DEV[:12]))
        DEV = g('commit-tree', t_, '-p', DEV, '-m', 'SIMULATED squash of gate24T2b #%s' % n, env=CE).strip()
    print('  SIMULATED develop (mergedT2b): %s = the real develop %s + squashes of gate24T2b #1249..#1255 — every check below is over the SIMULATION' % (DEV, REAL_DEV))
elif SIM:
    nn = SIM[-4:]; own = sorted(PRS[nn]['files']); FP = ([f for f in own if f not in ADDED] or own)[0]
    idx = tempfile.mktemp(prefix='g24c_sim_', dir=os.path.dirname(CL)); ienv = dict(CE, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
    ex = subprocess.run(['git', '--git-dir', CL, 'cat-file', 'blob', DEV + ':' + FP], capture_output=True, text=True)
    blob = (ex.stdout if ex.returncode == 0 else '') + '\n# a FOREIGN edit of this PR\'s own file (scratch only, never pushed)\n'
    bo = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=ienv, inp=blob).strip()
    run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (bo, FP)], env=ienv)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
    DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + FP.rsplit('/', 1)[1], env=CE).strip()
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))

print('--- (b) ancestry and the develop move')
for n, p in PRS.items():
    chain = p['chain'] + [p['head']]; prev = p['base']; ok = True
    for c in chain:
        par = g('rev-list', '--parents', '-n1', c).split(); ok = ok and par[1:] == [prev]; prev = c
    hard(ok and g('rev-list', '--count', p['base'] + '..' + p['head']).strip() == str(len(chain)),
         '#%s: %d commit(s) on %s %s%s' % (n, len(chain), {BASE: 'BASE', DEV77: 'develop 77c6426b9', DEVFA: 'develop fa25c9b1'}[p['base']], p['base'][:12], ' (round 1 %s, then round 2)' % R1_1245[:12] if p['chain'] else ''))
    hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', p['base'], DEV]).returncode == 0,
         '#%s: its base %s is an ancestor of develop' % (n, p['base'][:12]))
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode == 0, 'develop %s descends from BASE' % DEV[:12])
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('  develop is %d commits ahead of BASE; the move touches %d paths:' % (len(move_log), len(move)))
for l in move_log: print('    ' + l)
for f in move: print('      moved path ' + f)
MOVE_SINCE = {}
for n, p in PRS.items():
    ms = sorted(x for x in g('diff', '--name-only', p['base'], DEV).splitlines() if x); MOVE_SINCE[n] = ms
    x = sorted(set(p['files']) & set(ms))
    hard(not x, '(3) BASE-INVARIANT: the develop move since #%s\'s base (%s, %d paths) ∩ its OWN paths == EMPTY (%s) — no declared overlap in this batch' % (n, p['base'][:9], len(ms), x))
PAIR = {}
for a, b in itertools.combinations(PRS, 2):
    x = sorted(set(PRS[a]['files']) & set(PRS[b]['files'])); PAIR['%s^%s' % (a, b)] = x
    hard(not x, 'PAIRWISE path-disjoint: #%s ∩ #%s == EMPTY (%s)' % (a, b, x))
OURS = set(f for n in PRS for f in PRS[n]['files']); THEIRS = set(f for n in T2B for f in T2B[n][1]) | set(T2B_ALSO)
hard(not (OURS & THEIRS), 'SIBLING BATCH: this batch\'s %d paths ∩ gate24T2b\'s %d (+ #1248\'s) == EMPTY — a gate24T2b squash never touches an own path here (%s)' % (len(OURS), len(THEIRS), sorted(OURS & THEIRS)))
DIRS = {}
for f in OURS | THEIRS: DIRS.setdefault(f.rsplit('/', 1)[0], set()).add(f)
print('  directory-level co-residence (not an overlap; CONTENT coupling is measured in (f)/(k)): %s' % {d: len(v) for d, v in DIRS.items() if len(v) > 1})

print('--- (c) per PR: numstat, blobs, modes; merge-tree over develop — checks (1) and (2)')
ns = lambda a, b: {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', a, b).strip().splitlines()}
out = {'measured_at': now(), 'simulation': SIM or 'none', 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move), 'pairwise': PAIR, 'prs': {}}
for n, p in PRS.items():
    h = p['head']; nh = ns(p['base'], h)
    hard(nh == p['files'], '#%s numstat base..head == the pinned file set and counts (%d files)' % (n, len(p['files'])))
    rc, mt = mtree(DEV, h)
    hard(rc == 0, '#%s merges clean over develop %s (merge-tree rc %d) -> %s' % (n, DEV[:9], rc, mt))
    changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x) if rc == 0 else ['CONFLICT']
    hard(changed == sorted(p['files']), '(1) BASE-INVARIANT: diff(develop, #%s merged) == EXACTLY its own paths (got %d)' % (n, len(changed)))
    hard(rc == 0 and ns(DEV, mt) == nh, '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(base -> head) for #%s' % n)
    files = []
    for f in sorted(p['files']):
        lt = g('ls-tree', h, '--', f).split(); lp = g('ls-tree', p['base'], '--', f).split(); ld = g('ls-tree', DEV, '--', f).split()
        mb = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (mt, f)], capture_output=True, text=True).stdout.strip()
        hard(mb == lt[2], '(1) #%s merged blob == head blob %s: %s' % (n, lt[2], f))
        want_mode = '100755' if (lp and lp[0] == '100755') else '100644'
        hard(lt[0] == want_mode and (f in ADDED and not lp or (lp and lp[0] == lt[0])), '#%s %s mode %s at head (%s at base) — unchanged' % (n, f.rsplit('/', 1)[1], lt[0], 'ABSENT' if not lp else lp[0]))
        hard((not lp and not ld) or (lp and ld and lp[2] == ld[2]), '#%s develop\'s blob of %s == the base\'s (%s)' % (n, f.rsplit('/', 1)[1], lp[2][:12] if lp else 'ABSENT'))
        files.append({'path': f, 'mode': lt[0], 'head_blob': lt[2], 'parent_blob': lp[2] if lp else 'ABSENT', 'merged_blob': mb})
        print('    #%s %s %s (base %s) +%d/-%d %s' % (n, lt[0], lt[2], lp[2][:12] if lp else 'ABSENT', p['files'][f][0], p['files'][f][1], f))
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json|vitest[^/]*\.config\.[tj]s|jest[^/]*\.config\.[tj]s|eslint\.config\.[cm]?js|\.prettierignore|knip[^/]*)$', f)]
    hard(not dep, '#%s: no config file in the PR (no package.json / lockfile / tsconfig / vitest / jest / eslint / prettier / knip): %s' % (n, dep))
    cmp_ = {'merge_base': p['base'], 'ahead': int(g('rev-list', '--count', p['base'] + '..' + h).strip()), 'behind': int(g('rev-list', '--count', p['base'] + '..' + DEV).strip())}
    print('    #%s GitHub compare develop...head predicted: merge_base %s ahead %d behind %d' % (n, p['base'][:12], cmp_['ahead'], cmp_['behind']))
    out['prs'][n] = {'compare': cmp_, 'head': h, 'parent': p['base'], 'chain': p['chain'], 'branch': p['branch'], 'keys': p['keys'], 'seat': p['seat'],
                     'subject': g('log', '-1', '--format=%s', h).strip(), 'merged_tree': mt, 'files': files,
                     'numstat': '%d/%d' % (sum(v[0] for v in p['files'].values()), sum(v[1] for v in p['files'].values())), 'nfiles': len(p['files'])}
r2 = ns(R1_1245, PRS['1245']['head'])
print('  #1245 ROUND-2 DELTA (round 1 %s -> round 2 head): %s' % (R1_1245[:12], r2))
out['r2_1245'] = {k.rsplit('/', 1)[1]: '%d/%d' % v for k, v in r2.items()}

print('--- (d) END_TREE: develop + the seven, over SEVEN units; orders = every ORDERED PAIR merged first (the rest after, sorted), every rotation of the sorted order and of its reverse — prefix-memoised; + a second instrument')
UNITS = {n: [PRS[n]['head']] for n in PRS}
def orders_for(us):
    us = sorted(us); o = []
    for a_, b_ in itertools.permutations(us, 2): o.append(tuple([a_, b_] + [u for u in us if u not in (a_, b_)]))
    for seq in (us, us[::-1]):
        for k in range(len(seq)): o.append(tuple(seq[k:] + seq[:k]))
    return sorted(set(o))
def chain(order, units, memo, start):
    memo.setdefault((), start)
    for k in range(1, len(order) + 1):
        pre = tuple(order[:k])
        if pre in memo: continue
        cur = memo[pre[:-1]]
        if cur.startswith('CONFLICT'): memo[pre] = cur; continue
        for hh in units[pre[-1]]:
            rc_, t_ = mtree(cur, hh)
            if rc_ != 0: cur = 'CONFLICT@' + pre[-1]; break
            cur = g('commit-tree', t_, '-p', cur, '-p', hh, '-m', 'g24c chain (scratch only)', env=CE).strip()
        memo[pre] = cur
    c = memo[tuple(order)]
    return c if c.startswith('CONFLICT') else g('rev-parse', c + '^{tree}').strip()
MEMO = {}
ends = {','.join(o): chain(o, UNITS, MEMO, DEV) for o in orders_for(UNITS)}
print('  %d orders (%d distinct prefixes merged) -> %s' % (len(ends), len(MEMO) - 1, sorted(set(ends.values()))))
e1 = sorted(set(ends.values()))[0]
hard(len(set(ends.values())) == 1 and not e1.startswith('CONFLICT'), 'END_TREE identical in all %d orders' % len(ends))
def applied(base, diffs):
    idx = tempfile.mktemp(prefix='g24c_idx_', dir=os.path.dirname(CL)); ienv = dict(env, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=ienv); rcs = []
    for lab, a, b in diffs:
        ap = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached'], env=ienv, input=g('diff', '--binary', '--full-index', a, b), capture_output=True, text=True)
        rcs.append((lab, ap.returncode, ap.stderr.strip()[:120]))
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx); return t, rcs
DIFFS = [('#' + n, PRS[n]['base'], PRS[n]['head']) for n in PRS]
e3, rcs = applied(DEV, DIFFS)
for lab, rc_, err in rcs: hard(rc_ == 0, 'second instrument: apply --cached %s rc %d %s' % (lab, rc_, err))
hard(e3 == e1, 'second instrument (apply --cached of each base..head onto develop\'s tree) %s == END_TREE' % e3)
UNION = sorted(OURS)
if e1.startswith('CONFLICT'):
    st = 'NONE (%s)' % e1; hard(False, 'END_TREE could not be built over this develop (%s)' % e1); e1 = e3
else:
    st = g('diff', '--shortstat', DEV, e1).strip(); print('  develop -> END_TREE:', st)
    hard(sorted(g('diff', '--name-only', DEV, e1).split()) == UNION, 'END_TREE diff vs develop == the union of the %d paths' % len(UNION))
    for n in PRS:
        for fe in out['prs'][n]['files']:
            hard(g('rev-parse', '%s:%s' % (e1, fe['path'])).strip() == fe['head_blob'], 'END_TREE blob of %s == #%s head blob' % (fe['path'].rsplit('/', 1)[1], n))
# THE CAP: a #1245 NO GO ships NOTHING of #1245 — the END state without it
UN6 = {n: [PRS[n]['head']] for n in PRS if n != '1245'}; MEMO6 = {}
e6s = {','.join(o): chain(o, UN6, MEMO6, DEV) for o in orders_for(UN6)}; e6 = sorted(set(e6s.values()))[0]
e63, rcs6 = applied(DEV, [d for d in DIFFS if d[0] != '#1245'])
hard(len(set(e6s.values())) == 1 and not e6.startswith('CONFLICT') and e63 == e6 and all(r[1] == 0 for r in rcs6),
     'END_TREE_NO1245 (develop + the six, for the CAP: a #1245 NO GO ships nothing): %s, identical in %d orders and by apply --cached' % (e6, len(e6s)))
out['end_tree'] = e1; out['end_shortstat'] = st; out['union'] = UNION; out['end_tree_no1245'] = e6; out['end_orders'] = len(ends); out['end_orders_no1245'] = len(e6s)
# forward look (INFO, not pinned): the END if gate24T2b's seven land first
cur = DEV; okT = True
if SIM != 'mergedT2b':
    for n, (h, _) in T2B.items():
        rc_, t_ = mtree(cur, h)
        if rc_ != 0: okT = False; break
        cur = g('commit-tree', t_, '-p', cur, '-m', 'g24c T2B squash (scratch)', env=CE).strip()
    eT, rcsT = applied(g('rev-parse', cur + '^{tree}').strip() if okT else DEV, DIFFS)
    hard(okT and all(r[1] == 0 for r in rcsT), 'FORWARD LOOK: gate24T2b\'s seven squashed first, then this batch by apply --cached: clean (END over T2B %s — INFO, not pinned)' % eT)
    out['end_over_t2b'] = eT

print('--- (e) #1245 KS-1313 ROUND 2 (READ + the drafter\'s live probe drafter_liveshape_g24c.py: PREDICTION only)')
b45 = g('cat-file', 'blob', '%s:%s' % (PRS['1245']['head'], F45)); b45r1 = g('cat-file', 'blob', '%s:%s' % (R1_1245, F45)); b45d = g('cat-file', 'blob', '%s:%s' % (BASE, F45))
L45 = b45.split('\n'); ln = lambda L, s: [i + 1 for i, l in enumerate(L) if s in l]
LM45 = {'readChildOutput': ln(L45, 'export function readChildOutput(output: string): SuiteCounts | null {'), 'readSuiteCounts': ln(L45, 'export function readSuiteCounts(output: string): SuiteCounts | null {'),
        'TEST_FILES_LINE': ln(L45, "const TEST_FILES_LINE = ' Test Files ';"), 'anchor_includes': ln(L45, "if ((lines[i] ?? '').includes(TEST_FILES_LINE)) {"),
        'call_site': ln(L45, 'const counts = readChildOutput(result.stdout);'), 'childSuiteCounts': ln(L45, 'function childSuiteCounts(vars: Record<string, string>): SuiteCounts {'),
        'spawn_timeout': ln(L45, "{ env, cwd: PACKAGE_ROOT, encoding: 'utf8', timeout: 180_000 },"), 'whole_run_each': ln(L45, "])('KS-1313 whole-run: readChildOutput reads $label', ({ text, want }) => {"),
        'E5_cell': ln(L45, "it('KS-1313 E5: a failing child whose stderr carries a lookalike reports the FAILURE, not a clean run', () => {"),
        'anchor_control': ln(L45, "it('KS-1313 the anchor is what does it: without a Test Files block there is nothing to vouch for', () => {"),
        'callsite_cell': ln(L45, "it('the call site still goes through readChildOutput — behaviourally, not by reading the source', () => {"),
        'S10_row_3_2': ln(L45, "{ label: 'S10 stdout — the ticket mixed line', text: S10_STDOUT, want: { passed: 3, failed: 2 } },"),
        'matrix': ln(L45, "it('the slot-sensitive files pass identically from a shell on NO slot and on every slot — the measured regression', () => {")}
print('  line map at head: %s' % LM45)
hard(all(len(v) == 1 for v in LM45.values()), '#1245: readChildOutput, readSuiteCounts, the anchor, the stdout-only call site, the whole-run it.each, E5, the anchor control, the call-site cell, the {3,2} row and the :262 matrix each occur ONCE')
fnb = b45[b45.find('function childSuiteCounts('):]; fnb = fnb[:fnb.find('\n}\n') + 3]
hard('readSuiteCounts(output)' not in fnb and '${result.stdout}\\n${result.stderr}`.slice(-1500)' in fnb, '#1245: childSuiteCounts reads result.stdout ALONE; stderr is joined only into the thrown message tail')
unchk = [k for k in ('result.error', 'result.signal', 'result.status') if k not in fnb]
print('  LEAD KILLED-AFTER-LOOKALIKE (READ): childSuiteCounts never consults %s — a child killed by spawnSync\'s 180 s timeout returns its partial stdout and is READ as if it finished' % unchk)
cb = b45[b45.find("it('the call site still goes through readChildOutput"):]; cb = cb[:cb.find('\n    });\n') + 8]
hard(not re.search(r'(?<!function )\bchildSuiteCounts\(', cb) and "own.indexOf('function childSuiteCounts(')" in cb and 'readChildOutput(S17_STDOUT)' in cb and "toContain('readChildOutput(result.stdout)')" in cb,
     '#1245 LEAD CALLSITE-STILL-TEXT (READ): the "behavioural" call-site cell calls readChildOutput on a CONSTANT and never enters childSuiteCounts; the only call-site reach is the source-text toContain — T-CALL (iii) (an inline reading + a comment `// readChildOutput(result.stdout)`) is PREDICTED GREEN')
mb_ = lambda s: s[s.find("it('the slot-sensitive files pass identically"):s.find('\n});\n', s.find("it('the slot-sensitive files pass identically"))]
hard(mb_(b45) == mb_(b45d) == mb_(b45r1), '#1245: the :262 matrix block is byte-identical BASE -> round 1 -> round 2 (the budget stays out of scope)')
cnt = lambda s: len(re.findall(r"(?m)^\s*it\(", s)) + len(re.findall(r"(?m)^\s*it\.each\(", s))
print('  it( + it.each( in the file: BASE %d -> round 1 %d -> round 2 %d' % (cnt(b45d), cnt(b45r1), cnt(b45)))
cap = g('cat-file', 'blob', '%s:%s' % (PRS['1245']['head'], C45))
exp_ = re.findall(r'(?m)^export const (\w+) =', cap)
hard(exp_ == ['S17_STDOUT', 'S17_STDERR', 'S18_STDOUT', 'S18_STDERR', 'S19_STDOUT', 'S10_STDOUT'], '#1245: capturedChildOutput.ts exports exactly the six captured streams %s' % exp_)
print('  NOTE (READ): every captured constant embeds the seat\'s session scratchpad path (%d occurrences of /private/tmp/claude-501/) — a committed fixture carrying a machine path' % cap.count('/private/tmp/claude-501/'))
LS = os.path.join(GS, '_sp', 'live2', 'results.json')
if os.path.exists(LS):
    R = json.load(open(LS))
    print('  DRAFTER LIVE PROBE (%s, PREDICTION): stdout-only (the product path) WRONG on %s; JOINED (the seat\'s named claim) WRONG on %s' % (
        LS, [r['shape'] for r in R if r['stdoutOnly'] != 'PASS'], [r['shape'] for r in R if r['joined'] != 'PASS']))
    out['live'] = {'stdout_wrong': [r['shape'] for r in R if r['stdoutOnly'] != 'PASS'], 'joined_wrong': [r['shape'] for r in R if r['joined'] != 'PASS'], 'n': len(R)}
else:
    print('  DRAFTER LIVE PROBE: results absent at this home (%s) — UNREAD, not a refusal (the gate measures)' % LS); out['live'] = {'n': 0}
out['k1245'] = {'line_map': LM45, 'unchecked': unchk}

print('--- (f) #1256 KS-1159 (READ + a Python port of the ks1061 guard, old and new, over develop, the head and the END_TREE: PREDICTION only)')
g56 = g('cat-file', 'blob', '%s:%sks1061-shared-mock-completeness.test.ts' % (PRS['1256']['head'], O))
NEW_ROOT = re.compile(r'''jest\.(?:mock|doMock)\(\s*['"]@secuura/shared['"]\s*,''')
NEW_VIA = re.compile(r'''jest\.(?:mock|doMock)\(\s*['"]@secuura/shared['"]\s*,\s*\(\)\s*=>\s*\n?\s*require\(\s*['"](?:\.\.?/)+helpers/sharedModuleMock['"]\s*\)\.makeSharedMock\(''')
OLD_ROOT = re.compile(r"jest\.mock\(\s*'@secuura/shared'\s*,"); OLD_VIA = re.compile(r"jest\.mock\(\s*'@secuura/shared'\s*,\s*\(\)\s*=>\s*\n?\s*require\('\./helpers/sharedModuleMock'\)\.makeSharedMock\(")
hard(r"const ROOT_MOCK = /jest\.(?:mock|doMock)\(\s*['" + '"' + r"]@secuura\/shared['" + '"' + r"]\s*,/g;" in g56 and 'fs.readdirSync(dir, { withFileTypes: true })' in g56,
     '#1256: ROOT_MOCK widened to mock|doMock and either quote; the walk is recursive (withFileTypes)')
def guard(rev, root, via, recursive):
    fl = [x for x in g('ls-tree', '-r', '--name-only', rev, O).split() if x.endswith('.test.ts') and (recursive or x.count('/') == O.count('/'))]
    tot, off = 0, []
    for f in fl:
        s_ = g('cat-file', 'blob', '%s:%s' % (rev, f)); d_, v_ = len(root.findall(s_)), len(via.findall(s_)); tot += d_
        if d_ != v_: off.append('%s (%d/%d)' % (f.rsplit('/', 1)[1], d_, v_))
    return tot, off, len(fl)
for lab, rev in (('develop', DEV), ('#1256 head', PRS['1256']['head']), ('END_TREE', e1)):
    tn, on, fn_ = guard(rev, NEW_ROOT, NEW_VIA, True); to, oo, fo = guard(rev, OLD_ROOT, OLD_VIA, False)
    print('    port over %-10s NEW guard: %d files, %d factories, offenders %s | OLD guard: %d files, %d factories, offenders %s' % (lab, fn_, tn, on or 'none', fo, to, oo or 'none'))
    if lab != 'develop': hard(not on and tn >= 10, '#1256 port over %s: the NEW guard finds %d factories (>= 10) and NO offender — the widened readers stay green over the tree (incl. #1261\'s new file)' % (lab, tn))
out['k1256'] = {'factories_end': guard(e1, NEW_ROOT, NEW_VIA, True)[0]}
print('  LEAD SELF-SCAN (READ, the seat names it): the guard reads its own source; a doc comment spelling the offending shape reds it — the gate plants one in a COPY and confirms')

print('--- (g) #1257 KS-1201 (READ)')
s57 = g('cat-file', 'blob', '%s:systemTest/__tests__/bootstrap_login_diagnosis.test.sh' % PRS['1257']['head']); s57b = g('cat-file', 'blob', '%s:systemTest/__tests__/bootstrap_login_diagnosis.test.sh' % BASE)
nc = lambda s: re.sub(r'(?m)^\s*#.*$', '', s)
hard('$(start_stub' in nc(s57b) and '$(start_stub' not in nc(s57) and len(re.findall(r'(?m)^start_stub (429|401|503|200) \|\| exit 2$', s57)) == 5,
     '#1257: every `port="$(start_stub N)"` is gone from code lines; five parent-shell `start_stub N || exit 2` calls (4 cells + the KS-1201 control)')
hard('case "$cmd" in *"$STUB"*)' in s57 and 'pgrep' not in nc(s57), '#1257: count_my_stubs selects by the stub\'s ABSOLUTE path, never pgrep / basename')
okc = lambda s: len(re.findall(r'(?m)(^|[;&|] |then |else )\s*ok "', s))
print('  static `ok "` call sites BASE %d -> head %d (the seat: 16 -> 18 at run time)' % (okc(s57b), okc(s57)))
print('  NOTE (READ): the suite sits in systemTest/__tests__ — a run-shell-suites ROOT: one of the 60, NOT in the STOP triple; the push took the hook\'s early return (0 of 15 legs)')

print('--- (h) #1258 KS-1296 (READ)')
m58 = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/run-migrations.sh' % PRS['1258']['head']); t58 = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh' % PRS['1258']['head'])
t58b = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh' % BASE)
hard('#   4  — pg_isready is not installed' in m58 and m58.count('exit 4') == 1 and m58.find('command -v pg_isready') < m58.find('echo "Waiting for PostgreSQL to be ready..."'),
     '#1258: exit 4 documented in the exit-code table, raised ONCE, and the binary check precedes the wait')
hard('EXPECTED_CELLS=4' in t58b and 'EXPECTED_CELLS=6' in t58, '#1258: EXPECTED_CELLS 4 -> 6 (the completeness guard; the suite prints 5 -> 7 passed)')
print('  NOTE (READ): cell 5\'s red at BASE burns MAX_RETRIES=30 x RETRY_INTERVAL=2 (~61 s, the seat); pg_isready is ABSENT on this box (/usr/bin, /opt/homebrew/bin: ls rc 1 at drafting) so cell 5\'s precondition holds here; the DB_URL names localhost:5432 but every cell stubs psql/pg_isready — NO cell reaches :5432 (READ)')

print('--- (i) #1259 KS-906 (READ)')
t59 = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh' % PRS['1259']['head']); t59b = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh' % BASE)
hard('res=$(cd /tmp && run_check)' in t59b and 'res=$(cd /tmp && run_check)' not in t59 and 'c6b_from_tmp="$(cd /tmp && run_check)"' in t59 and 'c6b_from_repo="$(cd "$HERE" && run_check)"' in t59,
     '#1259: CASE 6\'s inert `cd /tmp` dropped; CASE 6b asks from /tmp AND from $HERE (inside the checkout)')
print('  static `ok "` call sites BASE %d -> head %d (the seat: 15 -> 16)' % (okc(t59b), okc(t59)))

print('--- (j) #1260 KS-1139 (READ ONLY — the gate NEVER executes sync-secrets.sh and NEVER runs az)')
d60 = g('diff', '-U0', BASE, PRS['1260']['head'], '--', 'Blockchain/Dev/deployment/azure/sync-secrets.sh')
minus = [l[1:] for l in d60.splitlines() if l.startswith('-') and not l.startswith('---')]; plus = [l[1:] for l in d60.splitlines() if l.startswith('+') and not l.startswith('+++')]
pairs_ok = len(minus) == len(plus) == 8 and all(re.fullmatch(r'(\s*)\(\((SKIPPED|GENERATED|UPDATED)\+\+\)\)', a) and b == '%s%s=$((%s + 1))' % (re.match(r'\s*', a).group(0), re.search(r'\((\w+)\+\+', a).group(1), re.search(r'\((\w+)\+\+', a).group(1)) for a, b in zip(minus, plus))
hard(pairs_ok, '#1260: EXACTLY 8 changed lines, each `((X++))` -> `X=$((X + 1))` for SKIPPED / GENERATED / UPDATED, indentation kept')
s60 = g('cat-file', 'blob', '%s:Blockchain/Dev/deployment/azure/sync-secrets.sh' % PRS['1260']['head'])
CELL4 = re.compile(r'^[ \t]*\(\([A-Za-z_][A-Za-z_0-9]*(\+\+|--)\)\)[ \t]*$', re.M)
hard(len(CELL4.findall(s60)) == 0 and 'set -euo pipefail' in s60, '#1260: the CELL 4 census regex reads 0 in sync-secrets.sh at head (8 at BASE); `set -euo pipefail` present')
cen = {}
for rev_lab, rev in (('BASE', BASE), ('END_TREE', e1)):
    c_ = {}
    for f in g('ls-tree', '-r', '--name-only', rev).split():
        if f.endswith('.sh'):
            k = len(CELL4.findall(g('cat-file', 'blob', '%s:%s' % (rev, f))))
            if k: c_[f] = k
    cen[rev_lab] = c_
print('  KS-1139 CENSUS (the ticket\'s CELL 4 regex over every tracked *.sh): BASE %s | END_TREE %s' % (cen['BASE'], cen['END_TREE']))
hard(set(cen['END_TREE']) <= {'Blockchain/Dev/scripts/validate-env.sh'} and 'systemTest/schemathesis/validate-lint.sh' not in cen['BASE'],
     'KS-1139 census: validate-lint.sh x2 already reads 0 at BASE (fixed by #1192 4ff8247fe, 2026-09-22); at the END_TREE only validate-env.sh x3 remains — the ticket\'s own "NOT defects" row')
print('  LEAD KS1139-CLOSES? (READ): the ticket names 10 sites (sync-secrets.sh x8 + validate-lint.sh x2); #1192 took the 2, #1260 takes the 8 — the gate RULES whether #1260\'s delivered scope closes KS-1139 (the errexit DEATH itself stays UNREPRODUCED-ON-THIS-HOST)')
print('  NOTE (READ): the errexit DEATH is UNREPRODUCED-ON-THIS-HOST (only /bin/bash 3.2.57; no /opt/homebrew/bin/bash, no /usr/local/bin/bash at drafting)')
out['k1260'] = {'census': cen}

print('--- (k) #1261 KS-1293 (READ + a Python port of CONFIGPINNED\'s anchoringBases() over the head, the END_TREE and the END over gate24T2b: PREDICTION only)')
F61 = O + 'ks1293-originate-suite-is-hermetic.test.ts'; t61 = g('cat-file', 'blob', '%s:%s' % (PRS['1261']['head'], F61))
BAD = {1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 37, 42, 43, 53, 69, 77, 79, 87, 95, 101, 102, 103, 104, 109, 110, 111, 113, 115, 117, 119, 123, 135, 137, 139, 143, 161, 179, 389, 427, 465,
       512, 513, 514, 515, 526, 530, 531, 532, 540, 548, 554, 556, 563, 587, 601, 636, 989, 990, 993, 995, 1719, 1720, 1723, 2049, 3659, 4045, 4190, 5060, 5061, 6000, 6566, 6665, 6666, 6667, 6668,
       6669, 6679, 6697, 10080}
def configpinned(rev):
    pinned, off = 0, []
    for f in [x for x in g('ls-tree', '--name-only', rev, O).split() if x.endswith('.test.ts') and not x.endswith('.integration.test.ts')]:
        s_ = g('cat-file', 'blob', '%s:%s' % (rev, f))
        if 'ANCHORING_SERVICE_URL' not in s_: continue
        bases = [m.group(1) for m in re.finditer(r'''ANCHORING_SERVICE_URL\s*=\s*['"]([^'"]+)['"]''', s_)]
        for m in re.finditer(r'ANCHORING_SERVICE_URL\s*=\s*([A-Z][A-Z0-9_]*)\s*;', s_):
            d = re.search(r'''const\s+%s\s*=\s*['"]([^'"]+)['"]''' % m.group(1), s_)
            if d: bases.append(d.group(1))
        if not bases: off.append('%s: mentions, assigns no literal' % f.rsplit('/', 1)[1]); continue
        for b_ in bases:
            pinned += 1; mm = re.match(r'https?://([^:/]+)(?::(\d+))?', b_)
            if not mm or mm.group(1) != '127.0.0.1' or int(mm.group(2) or 80) in BAD: off.append('%s: %s' % (f.rsplit('/', 1)[1], b_))
    return pinned, off
for lab, rev in (('#1261 head', PRS['1261']['head']), ('END_TREE', e1)) + ((('END over gate24T2b', eT),) if 'eT' in dir() and okT else ()):
    pn, of = configpinned(rev)
    print('    port over %-18s CONFIGPINNED: %d bases pinned, offenders %s' % (lab, pn, of or 'none'))
    hard(pn >= 8 and not of, '#1261 port over %s: >= 8 bases, no offender (with #1256\'s and, where present, #1252/#1255\'s bytes in)' % lab)
hard('revert one file\'s env line and the suite stays green' in t61, '#1261: its own header NAMES the regression shape the cells exist to catch — "revert one file\'s env line and the suite stays green"')
# THE NAMED SHAPE through the port: delete each subject file's env-assignment line(s) and re-read CONFIGPINNED (a file that no longer mentions the key is SKIPPED)
def bases_of(s_):
    b_ = [m.group(1) for m in re.finditer(r'''ANCHORING_SERVICE_URL\s*=\s*['"]([^'"]+)['"]''', s_)]
    for m in re.finditer(r'ANCHORING_SERVICE_URL\s*=\s*([A-Z][A-Z0-9_]*)\s*;', s_):
        d = re.search(r'''const\s+%s\s*=\s*['"]([^'"]+)['"]''' % m.group(1), s_)
        if d: b_.append(d.group(1))
    return b_
subj61 = {}
for f in [x for x in g('ls-tree', '--name-only', PRS['1261']['head'], O).split() if x.endswith('.test.ts') and not x.endswith('.integration.test.ts')]:
    s_ = g('cat-file', 'blob', '%s:%s' % (PRS['1261']['head'], f))
    if 'ANCHORING_SERVICE_URL' in s_: subj61[f] = s_
tot61 = sum(len(bases_of(s_)) for s_ in subj61.values()); REV = []
for f, s_ in sorted(subj61.items()):
    L_ = s_.split('\n'); asg = [i for i, l in enumerate(L_) if re.search(r'ANCHORING_SERVICE_URL\s*=', l) and not l.strip().startswith(('//', '*'))]
    rv = '\n'.join(l for i, l in enumerate(L_) if i not in asg); still = 'ANCHORING_SERVICE_URL' in rv
    after = tot61 - len(bases_of(s_)) + (len(bases_of(rv)) if still else 0)
    red = (still and not bases_of(rv)) or after < 8
    REV.append({'file': f.rsplit('/', 1)[1], 'lines': [i + 1 for i in asg], 'still_mentions': still, 'pinned_after': after, 'configpinned': 'RED' if red else 'GREEN'})
    print('    port REVERT %-60s env line(s) %s -> still mentions the key %-5s pinned %d -> %s' % (f.rsplit('/', 1)[1], [i + 1 for i in asg], still, after, 'RED' if red else 'GREEN — the revert is INVISIBLE'))
print('  LEAD REVERT-SKIPS (port, PREDICTION): %d subjects, %d bases, floor 8 — reverting the env line of %s leaves CONFIGPINNED GREEN (the file stops mentioning the key and is skipped; the floor absorbs it): THE NAMED SHAPE, read WRONG' % (len(subj61), tot61, [r['file'] for r in REV if r['configpinned'] == 'GREEN']))
out['k1261_revert'] = REV
integ = g('cat-file', 'blob', '%s:%sks1263-multi-write-rolls-back.integration.test.ts' % (DEV, O))
print('  #1261 NOT-COVERED claim (READ): ks1263-multi-write-rolls-back.integration.test.ts on develop sets %s' % re.findall(r'''ANCHORING_SERVICE_URL[^\n]*''', integ)[:2])
hard("await expect(fetch(new URL('/healthz', 'http://anchoring:4005'))).rejects.toThrow();" in t61 and 'return real(...args);' in t61,
     '#1261 LEAD NODNS-EGRESS (READ): the NODNS positive-control arm fetches the PRODUCT DEFAULT http://anchoring:4005 through the REAL resolver (the spy passes through) — every originate run makes an off-host DNS query, and where `anchoring` resolves, a real HTTP request; the gate MEASURES this before running #1261\'s suite')
out['k1261'] = {'pinned_end': configpinned(e1)[0]}

print('--- (l) the fleet STOP count, READ ONLY from each PR\'s push log (anchored to each suite\'s `=== …test.sh ===` header; a NOT-FOUND control)')
def stopread(path):
    pl = open(path, encoding='utf-8', errors='replace').read()
    def after(hdr, pat):
        i = pl.find(hdr); m_ = re.search(pat, pl[i:]) if i >= 0 else None
        return '%s/%s' % m_.groups() if m_ else 'NOT FOUND'
    r = {k: after(h_, p_) for k, (h_, p_) in SUITE.items()}
    r.update({'shell_suites': (re.findall(r'shell suites: (\d+ passed, \d+ failed, \d+ skipped \(of \d+\))', pl) or ['NOT FOUND'])[-1],
              'preflight': (re.findall(r'PREFLIGHT [A-Z]+ — [^\n]*', pl) or ['NOT FOUND'])[-1], 'legs': (re.findall(r'  legs [0-9 ]+ — [^\n]*', pl) or ['NOT FOUND'])[-1],
              'fixture_build_failed': len(re.findall(r'(?m)^FIXTURE BUILD FAILED', pl)), 'control_absent_header': after('=== no_such_suite_g24c.test.sh ===', r'(\d+) passed, (\d+) failed'),
              'suite_headers': len(re.findall(r'(?m)^=== .*\.test\.sh ===$', pl)), 'format_gate': (re.findall(r'\[format-gate\] \d+ package\(s\) checked[^\n]*', pl) or ['none'])[-1],
              'branches': sorted(set(re.findall(r'feature/ks-\d+[a-z0-9-]*', pl)))})
    return r
STOP = {}
for n in PRS:
    path, kind = PUSHLOG[n]
    try:
        s_ = stopread(path); STOP[n] = dict(s_, kind=kind, start=open(path.replace('.out', '.start')).read().strip(), end=open(path.replace('.out', '.end')).read().strip())
        print('  #%s %s [%s] %s -> %s: %s' % (n, path.split('5_Project_History/')[1], kind, STOP[n]['start'], STOP[n]['end'], {k: v for k, v in s_.items() if v not in ('NOT FOUND', 0, 'none', [])} or s_))
        own_br = PRS[n]['branch'].replace('refs/heads/', '')
        if kind == 'overwritten':
            hard(own_br not in s_['branches'], '#%s: its push record %s now holds ANOTHER push (%s) — LEAD STOP-RECORD-OVERWRITTEN (the gate cannot re-read #%s\'s own record)' % (n, path.rsplit('/', 1)[1], s_['branches'], n))
            ev = [l for f_ in ('predict_5.out', 'predict_6.out', 'predict_7.out') if os.path.exists(T2B_KIT + f_) for l in open(T2B_KIT + f_, encoding='utf-8') if 's-b28-cells-push.out: {' in l]
            print('    the only surviving reads (gate24T2b drafter, predict_5/6/7.out, labelled #1255, .start 15:13:28Z = #1256\'s push window by timing; branch NOT recorded by that instrument): %d lines, e.g. %s' % (len(ev), ev[-1].strip()[:400] if ev else 'NONE FOUND'))
            continue
        hard(own_br in s_['branches'], '#%s push log names its own branch %s' % (n, own_br))
        if kind == 'format-gate':
            hard(s_['suite_headers'] == 0 and s_['preflight'] == 'NOT FOUND' and '1 package(s) checked, 0 skipped, 0 failed' in s_['format_gate'], '#%s push: format gate only, 0 suite headers, NO preflight (systemTest/performance path) — no STOP count to claim' % n)
        elif kind == 'early-return':
            hard(s_['suite_headers'] == 0 and s_['preflight'] == 'NOT FOUND', '#%s push: the hook took its EARLY RETURN — 0 suite headers, no preflight line (0 of 15 legs, by design) — no STOP count to claim' % n)
        else:
            w = WANT_STOP[n]
            hard(all(s_[k] == w[k] for k in w) and s_['shell_suites'] == '60 passed, 0 failed, 0 skipped (of 60)' and s_['fixture_build_failed'] == 0 and s_['control_absent_header'] == 'NOT FOUND'
                 and s_['preflight'].startswith('PREFLIGHT INCOMPLETE — 12/15') and s_['legs'].startswith('  legs 3 4 8 —'),
                 '#%s push log: 28/0, fixture_guard 6/0, run_shell_suites 49/0, run_migrations %s, no_tracked_credentials_root %s, bootstrap %s, 60 of 60, INCOMPLETE 12/15 (legs 3 4 8), 0 FIXTURE BUILD FAILED (control NOT FOUND)' % (n, w['run_migrations_failure_exit_code'], w['no_tracked_credentials_root'], w['bootstrap_login_diagnosis']))
    except OSError as e:
        STOP[n] = {'error': str(e)}; print('  #%s push log UNREAD: %s (the gate reads it)' % (n, e))
out['stop'] = STOP
tb = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh' % DEV); fg = g('cat-file', 'blob', '%s:Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh' % DEV)
SAD = {'run_shell_suites': len(re.findall(r'(?m)^\s*check ', tb)), 'fixture_guard': len(re.findall(r'(?m)^\s*ok "', fg))}
print('  FLEET STOP AT THIS DEVELOP (static cell census of develop %s; 49 / 6 before gate24T2b\'s #1250 / #1253 squash, 55 / 10 after): run_shell_suites %d, fixture_guard %d' % (DEV[:12], SAD['run_shell_suites'], SAD['fixture_guard']))
hard(SAD['run_shell_suites'] in (49, 55) and SAD['fixture_guard'] in (6, 10), 'the fleet STOP counts on this develop are one of the two known states (49|55, 6|10) — anything else is re-derived by hand')
out['stop_at_develop'] = SAD

print('--- (m) branch names through the hyphenated-key scanner (own keys only) + the subjects vs MG-11 + foreign keys per commit body (MG-3)')
for n, p in PRS.items():
    ks = sorted(set('KS-' + k for k in re.findall(r'(?i)\bks-(\d+)\b', p['branch'])))
    hard(bool(ks) and set(ks) <= set(p['keys']), '#%s branch keys %s ⊆ own %s' % (n, ks, p['keys']))
    fk = set(); refs_ = []
    for c in p['chain'] + [p['head']]:
        body_ = g('log', '-1', '--format=%B', c); fk |= set(re.findall(r'\bKS-\d+', body_)) - set(p['keys']); refs_ += re.findall(r'(?m)^Refs .*$', body_)
    out['prs'][n]['foreign_keys_in_body'] = sorted(fk)
    print('    #%s commit bodies: FOREIGN hyphenated keys %s (a squash body must un-hyphenate them: MG-3) | Refs lines %s' % (n, sorted(fk) or 'none', refs_))
    sj = out['prs'][n]['subject']; print('    #%s head commit subject %d chars%s: %s' % (n, len(sj), ' (> 92: MG-11 FAILS as a squash subject)' if len(sj) > 92 else '', sj))
print('--- (n) static reference counts (the gate MEASURES)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
nsuites = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots).splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
cnt_o = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', O).splitlines() if f.endswith('.test.ts') and not f.endswith('.integration.test.ts'))
cnt_p = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', P + 'tests/unit').splitlines() if f.endswith('.test.ts'))
out['suites'] = {'develop': nsuites(DEV), 'end': nsuites(e1)}; out['originate_files'] = {'develop': cnt_o(DEV), 'end': cnt_o(e1)}; out['perf_files'] = {'develop': cnt_p(DEV), 'end': cnt_p(e1)}
print('  run-shell-suites.sh ROOTS `*.test.sh`: develop %d | END_TREE %d (no PR adds a suite FILE: the denominator stays 60)' % (out['suites']['develop'], out['suites']['end']))
print('  originate unit *.test.ts (non-integration): develop %d | END_TREE %d (+1: #1261; the seat: 74 -> 75 suites, 869 -> 871 cells)' % (out['originate_files']['develop'], out['originate_files']['end']))
print('  systemTest/performance tests/unit *.test.ts: develop %d | END_TREE %d (#1245 adds a SUPPORT module, not a test file: 63 files; the seat 1089 -> 1115)' % (out['perf_files']['develop'], out['perf_files']['end']))
hard(out['suites']['end'] == out['suites']['develop'] == 60, 'the shell-suite denominator is 60 on develop AND on the END_TREE')
out['fail'] = len(FAIL)
name = 'pins_gate24T2c.json' if not SIM else 'pins_gate24T2c.SIM-%s.json' % SIM
with open(os.path.join(GS, name), 'w', encoding='utf-8') as f: json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, name), 'at', now()); print('HARD FAILS:', len(FAIL), FAIL)
sys.exit(1 if FAIL else 0)
