#!/usr/bin/env python3
"""predict_gate21T2e.py — MEASURE the round-21 tier-2 gate gate21T2e (#1241 KS-1226 item 2, ROUND 2 OF 2; Seat B 27th) over origin develop AS READ
NOW, and write pins_gate21T2e.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index, hash-object for a simulation) runs in a scratch BARE clone under <scratchpad>/g21e_sp/clone.git
— `git clone --bare --no-local` FROM the checkout (a plain copy through upload-pack: NO alternates into the shared object store, which is only READ),
then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only, never printed). Nothing is
written into the checkout. The vitest 4.1.11 dist is READ from `npm pack vitest@<lockfile pin>` unpacked under <scratchpad>/g21e_sp/npm (never the
checkout's stale node_modules, which hold 4.1.9); a failed pack prints UNREAD and is not a refusal (the gate measures the shape at runtime anyway).

BASE-INVARIANT (Wednesday's 04:35Z ANSWER `answer_seatB25_movedbase`): the PR was cut from the OLD develop aa600af94 (BASE); round 2 is a
FAST-FORWARD of the round-1 head e2d0518df (TWO commits over BASE, squashed as ONE). (1) diff(develop, merged) == EXACTLY the PR's own path, its blob
byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(BASE -> head); (3) the develop move ∩ the PR's OWN path == EMPTY. NO declared
overlap — ANY own-path overlap refuses, re-predict BY HAND.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign1241 builds develop + a FOREIGN edit of the PR's own file in the scratch clone and
measures over it (a NEGATIVE CONTROL: must REFUSE); a simulation writes pins_gate21T2e.SIM-foreign1241.json, never the real pins.
Usage: predict_gate21T2e.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign1241]
"""
import json, os, re, subprocess, sys, datetime, tempfile, tarfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = 'aa600af94d69ad59db279d32cbbd7596931a739b'
R1HEAD = 'e2d0518df40228f0a183bc4223c7a6840821253e'
DEV_R1 = 'e68e2f0e837df86da527d775a3a49c631b0f5b17'   # the develop round 1 graded over (report.md BASE_GO)
F = 'systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts'
PR = {'n': '1241', 'key': 'KS-1226', 'head': 'b4427d416592b40eb5ddb8727b2d6c31f3c7d067', 'files': {F: (123, 3)},
      'branch': 'refs/heads/feature/ks-1226-unitsuiteslotindependence-summary-regex-returns-null-on-skipped-r22-skippedsummary-1'}
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
if SIM not in ('', 'foreign1241'): die('unknown simulation ' + SIM)
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate21T2e.py at', now(), '| scratchpad', SP, '| SIMULATION:', SIM or 'none (the real read)')

print('--- (a) head and develop: ls-remote (the checkout, READ) then a fetch FROM ORIGIN into the scratch clone')
refs = ['refs/heads/develop', 'refs/pull/1241/head', PR['branch']]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
print('  ls-remote at %s:' % now()); [print('    %s %s' % (v, k)) for k, v in lsd.items()]
CL = os.path.join(SP, 'g21e_sp', 'clone.git')
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL])
    run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g21e/develop',
     '+refs/pull/1241/head:refs/g21e/pr1241', '+%s:refs/g21e/br1241' % PR['branch']], env=env)
g = lambda *a, **k: run(['git', '--git-dir', CL] + list(a), **k)
DEV = g('rev-parse', 'refs/g21e/develop').strip()
hard(DEV == lsd.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
h = g('rev-parse', 'refs/g21e/pr1241').strip(); b = g('rev-parse', 'refs/g21e/br1241').strip()
hard(h == b == lsd.get('refs/pull/1241/head') == lsd.get(PR['branch']) == PR['head'], '#1241 head %s == pull head == branch (ls-remote AND fetch) == the pin' % h)
REAL_DEV = DEV
CE = dict(env, GIT_AUTHOR_NAME='x', GIT_COMMITTER_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_EMAIL='x@x')
if SIM:
    idx = tempfile.mktemp(prefix='g21e_sim_', dir=os.path.dirname(CL)); ienv = dict(CE, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
    blob = g('cat-file', 'blob', DEV + ':' + F) + '\n// a FOREIGN edit of this PR\'s own file (scratch only, never pushed)\n'
    bo = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=ienv, inp=blob).strip()
    run(['git', '--git-dir', CL, 'update-index', '--cacheinfo', '100644,%s,%s' % (bo, F)], env=ienv)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
    DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + F.rsplit('/', 1)[1], env=CE).strip()
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))

print('--- (b) ancestry (round 2 is a FAST-FORWARD of round 1) and the develop move')
H = PR['head']
hard(g('rev-list', '--parents', '-n1', H).split()[1:] == [R1HEAD], '#1241 head\'s parent == the round-1 head %s (fast-forward, no force)' % R1HEAD[:12])
hard(g('rev-list', '--parents', '-n1', R1HEAD).split()[1:] == [BASE], 'the round-1 head\'s parent == BASE %s' % BASE[:12])
hard(g('rev-list', '--count', BASE + '..' + H).strip() == '2', '#1241: exactly TWO commits over BASE (squashed as ONE)')
hard(g('merge-base', DEV, H).strip() == BASE, '#1241: merge-base(develop, head) == BASE')
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode == 0, 'develop %s descends from BASE' % DEV[:12])
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', R1HEAD, DEV]).returncode != 0, 'the round-1 head is NOT on develop (round 1 shipped nothing)')
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('  develop is %d commits ahead of BASE; the move touches %d paths:' % (len(move_log), len(move)))
for l in move_log: print('    ' + l)
for f in move: print('      moved path ' + f)
x = sorted(set(PR['files']) & set(move))
hard(not x, '(3) BASE-INVARIANT: the develop move ∩ #1241\'s OWN path == EMPTY (%s) — no declared overlap' % x)
since_r1 = [l for l in g('log', '--format=%H %s', DEV_R1 + '..' + DEV).splitlines() if l] if subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', DEV_R1, DEV]).returncode == 0 else ['(round-1 develop is NOT an ancestor)']
perf_since = sorted(x for x in g('diff', '--name-only', DEV_R1, DEV, '--', 'systemTest/performance').splitlines() if x) if not since_r1[0].startswith('(') else ['UNKNOWN']
print('  since round 1\'s develop %s: %d commits %s; systemTest/performance paths moved since: %s' % (DEV_R1[:9], len(since_r1), since_r1, perf_since or 'NONE'))

print('--- (c) numstat, blob, mode; merge-tree over the develop just read (checks (1) and (2)); END_TREE (== the merged tree, one PR) + a second instrument')
ns = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', BASE, H).strip().splitlines()}
hard(ns == PR['files'], '#1241 numstat BASE..head == the pinned file set and counts %s (got %s)' % (PR['files'], ns))
mt_p = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', DEV, H], capture_output=True, text=True, env=env)
mt = mt_p.stdout.split('\n')[0].strip()
hard(mt_p.returncode == 0, '#1241 merges clean over develop (merge-tree rc %d) -> %s' % (mt_p.returncode, mt))
changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x) if mt_p.returncode == 0 else ['CONFLICT']
hard(changed == sorted(PR['files']), '(1) BASE-INVARIANT: diff(develop, merged) == EXACTLY its own path (got %s)' % changed)
nsm = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', DEV, mt).strip().splitlines()} if mt_p.returncode == 0 else {}
hard(nsm == ns, '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(BASE -> head)')
lt = g('ls-tree', H, '--', F).split(); lb = g('ls-tree', BASE, '--', F).split(); l1 = g('ls-tree', R1HEAD, '--', F).split()
mb = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (mt, F)], capture_output=True, text=True).stdout.strip()
ld = g('ls-tree', DEV, '--', F).split()
hard(mb == lt[2], '(1) merged blob == head blob %s' % lt[2])
hard(lt[0] == '100644' and lb and lb[0] == '100644', 'mode 100644 at head, unchanged from BASE')
hard(bool(ld) and ld[2] == lb[2], 'develop\'s blob of the file == BASE\'s %s (develop never took round 1)' % lb[2][:12])
print('    head %s | round-1 %s | BASE %s | develop %s | merged %s' % (lt[2], l1[2], lb[2], ld[2] if ld else 'ABSENT', mb))
dep = [f for f in PR['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json|vitest[^/]*\.config\.[tj]s)$', f)]
hard(not dep, '#1241: NO package.json / lockfile / tsconfig / vitest config in the PR')
hard(not [f for f in PR['files'] if f.startswith('Blockchain/Dev/')], '#1241 touches 0 paths under Blockchain/Dev/ — the pre-push hook\'s preflight early return applies (NO 28/0 to claim)')
e1 = mt
idx = tempfile.mktemp(prefix='g21e_idx_', dir=os.path.dirname(CL)); ienv = dict(env, GIT_INDEX_FILE=idx)
run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
ap = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached'], env=ienv, input=g('diff', '--binary', '--full-index', BASE, H), capture_output=True, text=True)
hard(ap.returncode == 0, 'second instrument: apply --cached BASE..head onto develop rc %d %s' % (ap.returncode, ap.stderr.strip()[:120]))
e3 = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
hard(e3 == e1, 'second instrument (apply --cached) %s == END_TREE (the merged tree) %s' % (e3, e1))
st = g('diff', '--shortstat', DEV, e1).strip() if mt_p.returncode == 0 else 'NONE (CONFLICT)'
print('  develop -> END_TREE:', st)
out = {'measured_at': now(), 'simulation': SIM or 'none', 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move),
       'since_r1': since_r1, 'perf_since_r1': perf_since, 'end_tree': e1, 'end_shortstat': st,
       'pr': {'head': H, 'r1head': R1HEAD, 'branch': PR['branch'], 'key': PR['key'], 'subject': g('log', '-1', '--format=%s', H).strip(),
              'merged_tree': mt, 'path': F, 'mode': lt[0], 'head_blob': lt[2], 'r1_blob': l1[2], 'base_blob': lb[2], 'merged_blob': mb, 'numstat': '123/3'}}

print('--- (d) item 1 (the :127 budget) is OUT of scope: the matrix cell and the unit config are byte-identical BASE -> head')
hb = g('cat-file', 'blob', '%s:%s' % (H, F)); bb = g('cat-file', 'blob', '%s:%s' % (BASE, F)); r1b = g('cat-file', 'blob', '%s:%s' % (R1HEAD, F))
def matrix(src):
    i = src.find("    it('the slot-sensitive files pass identically"); j = src.find('\n    });\n', i)
    return src[i:j] if i >= 0 and j > i else None
hard(matrix(hb) is not None and matrix(hb) == matrix(bb), 'the matrix cell (`the slot-sensitive files pass identically …`) is byte-identical at BASE and head (item 1 untouched)')
cfg = [g('rev-parse', '%s:systemTest/performance/vitest.unit.config.ts' % r).strip() for r in (BASE, H, DEV)]
hard(len(set(cfg)) == 1, 'systemTest/performance/vitest.unit.config.ts blob identical at BASE, head and develop (%s)' % cfg[0][:12])
hard(hb.count('SLOT_SENSITIVE_FILES') >= 2 and hb[hb.find('const SLOT_SENSITIVE_FILES'):hb.find('];', hb.find('const SLOT_SENSITIVE_FILES'))] == bb[bb.find('const SLOT_SENSITIVE_FILES'):bb.find('];', bb.find('const SLOT_SENSITIVE_FILES'))],
     'SLOT_SENSITIVE_FILES list byte-identical BASE -> head')

print('--- (e) the head file: the reader, its binding, the cells (READ; the gate MEASURES)')
L = hb.split('\n'); ln = lambda s: [i + 1 for i, l in enumerate(L) if s in l]
print('  line map at head: readSuiteCounts def %s | its return %s | the call in childSuiteCounts %s | `return summary;` %s | KS-1226 describe %s' % (
    ln('function readSuiteCounts('), ln("return { passed: counts.get('passed')"), ln('const summary = readSuiteCounts(output);'), ln('    return summary;'), ln("describe('KS-1226")))
hard(len(ln('function readSuiteCounts(')) == 1 and not ln('export function readSuiteCounts'), 'readSuiteCounts is defined ONCE and is NOT exported (module-private: the gate reaches it by an in-file probe, never a lift)')
hard(len(ln('const summary = readSuiteCounts(output);')) == 1, 'childSuiteCounts calls readSuiteCounts exactly once')
hard(not [l for l in L if l.strip().startswith('const summary = /')] and 'shippedSummaryRegexBody' not in hb and 'readSummary(' not in hb, 'round 1\'s source scrape (a code line starting `const summary = /`, shippedSummaryRegexBody) and readSummary are GONE at head (a comment at :206 still names the old anchor)')
hard("return { passed: Number(summary[2]), failed: Number(summary[1] ?? '0') };" in r1b and "return { passed: Number(summary[2])" not in hb, 'round 1\'s :103 reading exists at the round-1 head and is gone at head (its successor is readSuiteCounts\' return)')
print('  round-1 :103 line at the round-1 head: %s' % [i + 1 for i, l in enumerate(r1b.split('\n')) if 'return { passed: Number(summary[2])' in l])

def read_head(o, swap=False):
    m = re.search(r'^[^\S\n]*Tests[^\S\n]+(.+?)[^\S\n]*\((\d+)\)[^\S\n]*$', o, re.M)
    if m is None: return None
    c = {}
    for seg in m.group(1).split('|'):
        pm = re.match(r'^\s*(\d+)\s+(\S.*?)\s*$', seg)
        if pm is None: return None
        c[pm.group(2)] = int(pm.group(1))
    if 'passed' not in c: return None
    r = {'passed': c.get('passed', 0), 'failed': c.get('failed', 0)}
    return {'passed': r['failed'], 'failed': r['passed']} if swap else r
def read_rx(rx):
    def f(o):
        m = re.search(rx, o); return None if m is None else {'passed': int(m.group(2)), 'failed': int(m.group(1) or 0)}
    return f
RX_BASE = r'Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)'
RX_R1 = r'Tests\s+(?:(\d+) failed \| )?(?:\d+ skipped \| )?(\d+) passed \((\d+)\)'
hard(('const summary = /%s/.exec(output);' % RX_BASE) in bb and ('const summary = /%s/.exec(output);' % RX_R1) in r1b, 'the BASE and round-1 :99 literals, as pinned here, are byte-present in their blobs')
C2 = '\n'.join([' Test Files  1 failed | 1 passed (2)', '      Tests  1 failed | 1 passed | 1 skipped (3)', '   Start at  10:00:00'])
CELLS = [('R1', 'Tests  1 failed | 1 passed | 1 skipped (3)', {'passed': 1, 'failed': 1}), ('R2', 'Tests  1 passed | 1 skipped (2)', {'passed': 1, 'failed': 0}),
         ('R3', 'Tests  1 passed | 1 todo (2)', {'passed': 1, 'failed': 0}), ('R4', 'Tests  1 passed | 1 expected fail (2)', {'passed': 1, 'failed': 0}),
         ('C1', 'Tests  1 passed (1)', {'passed': 1, 'failed': 0}), ('C2', C2, {'passed': 1, 'failed': 1}), ('C3', 'Tests  245 passed', None),
         ('C4', 'Tests  1 passed | wat (2)', None), ('C5', 'Tests  3 banana (3)', None)]
for cid, s, _ in CELLS:
    hard(("readSuiteCounts('%s')" % s) in hb or (cid == 'C2' and all(("'%s'," % x) in hb for x in s.split('\n'))), 'cell %s literal byte-present in the head file' % cid)
hard(ln("it('KS-1226 C6") != [], 'cell C6 (typeof readSuiteCounts === function) present — it grades nothing about the call site')
ARMS = [('HEAD', read_head), ('R-A round-1 reading (the :99 R1 literal + :103) in readSuiteCounts', read_rx(RX_R1)),
        ('R-D develop/BASE reading in readSuiteCounts', read_rx(RX_BASE)), ('R-B passed<->failed swapped in readSuiteCounts\' return (:93)', lambda o: read_head(o, True))]
PRED = {}
for lab, fn in ARMS:
    red = [cid for cid, s, want in CELLS if fn(s) != want]
    PRED[lab] = red; print('  PREDICTED (READ ONLY instrument, a Python port of each reading) %-62s -> RED %s (of 10; C6 always green)' % (lab, red or 'NONE'))
hard(PRED['HEAD'] == [], 'the head reading satisfies all 9 value cells under this instrument (the seat\'s green, reproduced statically)')
hard(bool(PRED[ARMS[1][0]]) and bool(PRED[ARMS[2][0]]), 'the round-1 and develop readings each red at least one cell (the red proof is predictable)')
SHAPES = [('seat-captured: fail+pass+skip', '      Tests  1 failed | 1 passed | 1 skipped (3)'), ('seat-captured: pass+skip', '      Tests  1 passed | 1 skipped (2)'),
          ('seat-captured: pass+todo', '      Tests  1 passed | 1 todo (2)'), ('seat-captured: pass+expected fail', '      Tests  1 passed | 1 expected fail (2)'),
          ('seat-captured: pass-only', '      Tests  1 passed (1)'),
          ('PREDICTED from the READ renderer (NOT captured): fail-only', '      Tests  1 failed (1)'),
          ('PREDICTED (NOT captured): skip-only', '      Tests  2 skipped (2)'), ('PREDICTED (NOT captured): todo-only', '      Tests  1 todo (1)'),
          ('PREDICTED (NOT captured): multi-file', ' Test Files  1 failed | 1 passed (2)\n      Tests  1 failed | 1 passed | 1 skipped (3)'),
          ('PREDICTED (NOT captured): 2 failed | 3 passed (orientation)', '      Tests  2 failed | 3 passed (5)'),
          ('PREDICTED (NOT captured): zero tests', '      Tests  no tests')]
TABLE = []
for lab, s in SHAPES:
    r = (lab, s, read_rx(RX_BASE)(s), read_rx(RX_R1)(s), read_head(s)); TABLE.append(r)
    print('    %-62s %-58r BASE %-28s R1 %-28s HEAD %s' % (lab, s, r[2], r[3], r[4]))
print('  PREDICTION (READ ONLY): on the fail-only shape the HEAD reader returns %s (no `passed` segment -> null by design); the gate MEASURES whether vitest 4.1.11 prints that shape' % read_head('      Tests  1 failed (1)'))

print('--- (f) vitest 4.1.11 as pinned: which renderer prints the final `Tests` line on a PIPED (non-TTY) run (READ from the npm tarball)')
lock = g('cat-file', 'blob', '%s:systemTest/performance/package-lock.json' % H)
m = re.search(r'"node_modules/vitest": \{\s*"version": "([^"]+)"', lock); LV = m.group(1) if m else 'UNREAD'
hard(LV == '4.1.11', 'the package lockfile at the head pins vitest 4.1.11')
ND = os.path.join(SP, 'g21e_sp', 'npm'); PK = os.path.join(ND, 'package')
VREAD = {'version': 'UNREAD'}
try:
    if not os.path.isdir(PK):
        os.makedirs(ND, exist_ok=True)
        subprocess.run(['perl', '-e', 'alarm 120; exec @ARGV', 'npm', 'pack', 'vitest@' + LV, '--pack-destination', ND], capture_output=True, text=True, check=True)
        with tarfile.open(os.path.join(ND, 'vitest-%s.tgz' % LV)) as tf: tf.extractall(ND)
    VREAD['version'] = json.load(open(os.path.join(PK, 'package.json')))['version']
    ch = os.path.join(PK, 'dist', 'chunks'); src = {f: open(os.path.join(ch, f), encoding='utf-8', errors='replace').read() for f in os.listdir(ch) if f.endswith('.js')}
    ut = [f for f, s in src.items() if 'function getStateString(tasks' in s]; ix = [f for f, s in src.items() if 'function getStateString(entry' in s]
    if ut and ix:
        us, xs = src[ut[0]], src[ix[0]]
        useg = us[us.index('function getStateString(tasks'):][:1600]; xseg = xs[xs.index('function getStateString(entry'):][:700]
        VREAD.update({'utils_chunk': ut[0], 'utils_passed_conditional': 'passed ? c.bold(c.green(`${passed} passed`)) : null' in useg,
                      'index_chunk': ix[0], 'index_passed_unconditional': 'c.bold(c.green(`${entry.passed} passed`)),' in xseg,
                      'final_summary_uses_utils': 'this.log(padSummaryTitle("Tests"), getStateString$1(tests));' in xs and 'as getStateString$1' in xs,
                      'nontty_disables_summary_window': 'if (!this.isTTY) this.options.summary = false;' in xs,
                      'isTTY_def': [l.strip() for l in open(os.path.join(ch, [f for f, s in src.items() if 'const isTTY =' in s][0]), encoding='utf-8') if 'const isTTY =' in l]})
        for k in ('utils_chunk', 'utils_passed_conditional', 'index_chunk', 'index_passed_unconditional', 'final_summary_uses_utils', 'nontty_disables_summary_window', 'isTTY_def'):
            print('  READ vitest %s: %s = %s' % (VREAD['version'], k, VREAD[k]))
        if VREAD['utils_passed_conditional'] and VREAD['final_summary_uses_utils'] and VREAD['nontty_disables_summary_window']:
            print('  LEAD (READ ONLY, strong): a PIPED run prints its final `Tests` line from %s:getStateString, where `passed` is CONDITIONAL; the renderer the head\'s'
                  ' comment quotes (%s:getStateString(entry), `passed` unconditional) is the SummaryReporter window, which DefaultReporter never builds when stdout is not a TTY.'
                  ' So a fail-only child prints `Tests  N failed (N)` and the head reader returns null there (predicted; the gate MEASURES).' % (ut[0], ix[0]))
except Exception as e:
    print('  vitest dist UNREAD (not a refusal; the gate measures at runtime): %s' % e)
out['k1226'] = {'shapes': [{'label': a, 'line': b, 'base': c, 'r1': d, 'head': e} for a, b, c, d, e in TABLE], 'pred_red': PRED, 'vitest_lock': LV, 'vitest_read': VREAD}

print('--- (g) branch name through the hyphenated-key scanner (own key only)')
ks = sorted(set(re.findall(r'(?i)\bks-(\d+)\b', PR['branch']))); hard(ks == ['1226'], '#1241 branch keys %s == own KS-1226' % ks)
print('--- (h) the fleet STOP count (static, reference only — #1241 has no Blockchain/Dev leg to claim)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
def nsuites(rev): return sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots).splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
out['suites_dev'] = nsuites(REAL_DEV); print('  run-shell-suites.sh ROOTS `*.test.sh` at develop: %d (END_TREE %d)' % (out['suites_dev'], nsuites(e1)))
out['fail'] = len(FAIL)
name = 'pins_gate21T2e.json' if not SIM else 'pins_gate21T2e.SIM-%s.json' % SIM
with open(os.path.join(GS, name), 'w', encoding='utf-8') as f: json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, name), 'at', now()); print('HARD FAILS:', len(FAIL), FAIL)
sys.exit(1 if FAIL else 0)
