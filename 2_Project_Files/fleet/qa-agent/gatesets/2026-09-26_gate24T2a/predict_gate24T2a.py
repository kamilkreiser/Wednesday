#!/usr/bin/env python3
"""predict_gate24T2a.py — MEASURE the round-24 FIRST tier-2 batch gate24T2a (#1243 KS-1117 + KS-1300 items 2-4, #1244 KS-1111, #1245 KS-1313,
#1248 KS-1143 GF-2 — WIDENED to four and FROZEN by Wednesday; one seat, Seat L6) over origin develop AS READ NOW, and write pins_gate24T2a.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index, hash-object for a simulation) runs in a scratch BARE clone under <scratchpad>/g24a_sp/clone.git
— `git clone --bare --no-local` FROM the checkout (a plain copy through upload-pack: NO alternates into the shared object store, which is only READ),
then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only, never printed). Nothing is
written into the checkout. The vitest 4.1.11 dist is READ from `npm pack vitest@<lockfile pin>` unpacked under <scratchpad>/g24a_sp/npm (a failed pack
prints UNREAD and is not a refusal).

BASE: all four heads are ONE commit each whose parent is BASE 6e2a00bfed57 (the develop every READY names). BASE-INVARIANT per PR (Wednesday's
04:35Z ANSWER `answer_seatB25_movedbase`): (1) diff(develop, merged) == EXACTLY the PR's own paths, each blob byte-equal to the head's blob; (2)
numstat(develop -> merged) == numstat(BASE -> head); (3) the develop move ∩ the PR's OWN paths == EMPTY. PAIRWISE the four PRs' path sets are
DISJOINT (measured here, hard): three sit under systemTest/performance, #1248 under Blockchain/Dev/packages/shared — NO declared overlap: ANY own-path overlap refuses, re-predict BY HAND.
#1241 (open, capped, unmerged, the older attempt on #1245's file) is NOT in the batch and NOT graded; its head is only READ and reported.
Python ports of three changed readers (parserImportSites, formatDockerArgsForLog, readSuiteCounts) are READ instruments for PREDICTIONS only —
never evidence; the gate measures through the real code.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign1243|foreign1244|foreign1245|foreign1248 builds develop + a FOREIGN edit of that PR's first own
file in the scratch clone and measures over it (a NEGATIVE CONTROL: must REFUSE); a simulation writes pins_gate24T2a.SIM-<mode>.json, never the pins.
Usage: predict_gate24T2a.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign1243|foreign1244|foreign1245|foreign1248]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, tarfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6e2a00bfed577528de1ee02b41cb5a0e99172b35'
P = 'systemTest/performance/'
H1241 = 'b4427d416592b40eb5ddb8727b2d6c31f3c7d067'
PRS = {
    '1243': {'keys': ['KS-1117', 'KS-1300'], 'head': '0c89e2b503d9333829c277c50ad3b1a33f03cb96',
             'branch': 'refs/heads/feature/ks-1117-readyaml-bom-strip-l6-r24-1',
             'files': {P + 'tests/unit/config/sheddingCeiling.test.ts': (88, 6), P + 'tests/unit/package_scripts.test.ts': (19, 4),
                       P + 'tests/unit/support/readYamlRouting.ts': (67, 0), P + 'tests/unit/utils/yamlRedaction.test.ts': (71, 0),
                       P + 'utils/yaml.ts': (10, 1)}},
    '1244': {'keys': ['KS-1111'], 'head': '146b620fda53f008b3384334a474b06a16235af3',
             'branch': 'refs/heads/feature/ks-1111-k6-echo-mask-lookbehind-l6-r24-1',
             'files': {P + 'runner/k6_docker.ts': (40, 8), P + 'tests/unit/runner/k6DockerRedaction.test.ts': (64, 0)}},
    '1245': {'keys': ['KS-1313'], 'head': '1700b5ae7dd56ad3e30602a40b20ae6469c35350',
             'branch': 'refs/heads/feature/ks-1313-readsuitecounts-label-set-l6-r24-1',
             'files': {P + 'tests/unit/utils/unitSuiteSlotIndependence.test.ts': (234, 4)}},
    '1248': {'keys': ['KS-1143'], 'head': '2b4960172644b5ef0414b94d46d11974012c2007',
             'branch': 'refs/heads/feature/ks-1143-legf-gf2-callback-walk-l6-r24-1',
             'files': {'Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts': (97, 1)}},
}
F48 = 'Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
L3C = 'a40cb9eea049'   # Seat L3's unpushed commit that #1248 cherry-picks (READ from the checkout's objects via the --no-local clone)
L6PUSH = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-25_seatL6/raise/'
SYSPERF = ('1243', '1244', '1245')
ADDED = {P + 'tests/unit/support/readYamlRouting.ts'}
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
if SIM not in ('', 'foreign1243', 'foreign1244', 'foreign1245', 'foreign1248'): die('unknown simulation ' + SIM)
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate24T2a.py at', now(), '| scratchpad', SP, '| SIMULATION:', SIM or 'none (the real read)')

print('--- (a) heads and develop: ls-remote (the checkout, READ) then a fetch FROM ORIGIN into the scratch clone')
refs = ['refs/heads/develop', 'refs/pull/1241/head'] + ['refs/pull/%s/head' % n for n in PRS] + [PRS[n]['branch'] for n in PRS]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
print('  ls-remote at %s:' % now()); [print('    %s %s' % (v, k)) for k, v in lsd.items()]
CL = os.path.join(SP, 'g24a_sp', 'clone.git')
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL])
    run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g24a/develop', '+refs/pull/1241/head:refs/g24a/pr1241']
    + ['+refs/pull/%s/head:refs/g24a/pr%s' % (n, n) for n in PRS] + ['+%s:refs/g24a/br%s' % (PRS[n]['branch'], n) for n in PRS], env=env)
g = lambda *a, **k: run(['git', '--git-dir', CL] + list(a), **k)
DEV = g('rev-parse', 'refs/g24a/develop').strip()
hard(DEV == lsd.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
for n, p in PRS.items():
    h = g('rev-parse', 'refs/g24a/pr' + n).strip(); b = g('rev-parse', 'refs/g24a/br' + n).strip()
    hard(h == b == lsd.get('refs/pull/%s/head' % n) == lsd.get(p['branch']) == p['head'],
         '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (n, h))
h41 = g('rev-parse', 'refs/g24a/pr1241').strip()
print('  #1241 (NOT in the batch, NOT graded) refs/pull/1241/head = %s (%s the head its gate graded)' % (h41, '==' if h41 == H1241 else 'MOVED from'))
REAL_DEV = DEV
CE = dict(env, GIT_AUTHOR_NAME='x', GIT_COMMITTER_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_EMAIL='x@x')
if SIM:
    FP = sorted(f for f in PRS[SIM[-4:]]['files'] if f not in ADDED)[0]
    idx = tempfile.mktemp(prefix='g24a_sim_', dir=os.path.dirname(CL)); ienv = dict(CE, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
    blob = g('cat-file', 'blob', DEV + ':' + FP) + '\n// a FOREIGN edit of this PR\'s own file (scratch only, never pushed)\n'
    bo = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=ienv, inp=blob).strip()
    run(['git', '--git-dir', CL, 'update-index', '--cacheinfo', '100644,%s,%s' % (bo, FP)], env=ienv)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
    DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + FP.rsplit('/', 1)[1], env=CE).strip()
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))

print('--- (b) ancestry and the develop move')
for n, p in PRS.items():
    par = g('rev-list', '--parents', '-n1', p['head']).split()
    hard(par[1:] == [BASE] and g('rev-list', '--count', BASE + '..' + p['head']).strip() == '1', '#%s: ONE commit, its parent == BASE %s' % (n, BASE[:12]))
    hard(g('merge-base', DEV, p['head']).strip() == BASE, '#%s: merge-base(develop, head) == BASE' % n)
hard(subprocess.run(['git', '--git-dir', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode == 0, 'develop %s descends from BASE' % DEV[:12])
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('  develop is %d commits ahead of BASE; the move touches %d paths:' % (len(move_log), len(move)))
for l in move_log: print('    ' + l)
for f in move: print('      moved path ' + f)
for n, p in PRS.items():
    x = sorted(set(p['files']) & set(move))
    hard(not x, '(3) BASE-INVARIANT: the develop move ∩ #%s\'s OWN paths == EMPTY (%s) — no declared overlap' % (n, x))
perf_moved = [f for f in move if f.startswith(P)]
print('  systemTest/performance paths in the move: %s' % (perf_moved or 'NONE'))
PAIR = {}
for a, b in itertools.combinations(PRS, 2):
    x = sorted(set(PRS[a]['files']) & set(PRS[b]['files'])); PAIR['%s^%s' % (a, b)] = x
    hard(not x, 'PAIRWISE path-disjoint: #%s ∩ #%s == EMPTY (%s)' % (a, b, x))
for n, p in PRS.items():
    if n in SYSPERF:
        hard(all(f.startswith(P) for f in p['files']) and not [f for f in p['files'] if f.startswith('Blockchain/Dev/')],
             '#%s: every path under systemTest/performance/, 0 under Blockchain/Dev/ (the pre-push preflight early return applies: NO 28/0 to claim)' % n)
    else:
        hard(all(f.startswith('Blockchain/Dev/packages/shared/') for f in p['files']),
             '#%s: every path under Blockchain/Dev/packages/shared/ (the pre-push hook RAN the preflight: the 28/0 claim is READ from the push log)' % n)
SHARED_DIRS = sorted(set(f.rsplit('/', 1)[0] for n in PRS for f in PRS[n]['files']))
print('  directories the batch touches: %s' % SHARED_DIRS)
print('  directory-level co-residence (not an overlap): %s' % sorted(set(
    d for d in SHARED_DIRS if sum(1 for n in PRS if any(f.rsplit('/', 1)[0] == d for f in PRS[n]['files'])) > 1)) or 'NONE')

print('--- (c) per PR: numstat, blobs, modes; merge-tree over the develop just read (checks (1) and (2))')
out = {'measured_at': now(), 'simulation': SIM or 'none', 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move),
       'perf_moved': perf_moved, 'pairwise': PAIR, 'h1241': h41, 'prs': {}}
for n, p in PRS.items():
    h = p['head']
    ns = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', BASE, h).strip().splitlines()}
    hard(ns == p['files'], '#%s numstat BASE..head == the pinned file set and counts (%d files)' % (n, len(p['files'])))
    mt_p = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', DEV, h], capture_output=True, text=True, env=env)
    mt = mt_p.stdout.split('\n')[0].strip()
    hard(mt_p.returncode == 0, '#%s merges clean over develop (merge-tree rc %d) -> %s' % (n, mt_p.returncode, mt))
    changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x) if mt_p.returncode == 0 else ['CONFLICT']
    hard(changed == sorted(p['files']), '(1) BASE-INVARIANT: diff(develop, #%s merged) == EXACTLY its own paths (got %d)' % (n, len(changed)))
    nsm = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in g('diff', '--numstat', DEV, mt).strip().splitlines()} if mt_p.returncode == 0 else {}
    hard(nsm == ns, '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(BASE -> head) for #%s' % n)
    files = []
    for f in sorted(p['files']):
        lt = g('ls-tree', h, '--', f).split(); lb = g('ls-tree', BASE, '--', f).split(); ld = g('ls-tree', DEV, '--', f).split()
        mb = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (mt, f)], capture_output=True, text=True).stdout.strip()
        hard(mb == lt[2], '(1) #%s merged blob == head blob %s: %s' % (n, lt[2], f))
        hard(lt[0] == '100644' and (f in ADDED and not lb or (lb and lb[0] == '100644')), '#%s %s mode 100644 at head (%s at BASE)' % (n, f, 'ABSENT' if not lb else lb[0]))
        hard((not lb and not ld) or (lb and ld and lb[2] == ld[2]), '#%s develop\'s blob of %s == BASE\'s (%s)' % (n, f.rsplit('/', 1)[1], lb[2][:12] if lb else 'ABSENT'))
        files.append({'path': f, 'mode': lt[0], 'head_blob': lt[2], 'base_blob': lb[2] if lb else 'ABSENT', 'merged_blob': mb})
        print('    #%s %s %s (BASE %s) +%d/-%d %s' % (n, lt[0], lt[2], lb[2][:12] if lb else 'ABSENT', p['files'][f][0], p['files'][f][1], f))
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json|vitest[^/]*\.config\.[tj]s|eslint\.config\.js|\.prettierignore|knip[^/]*)$', f)]
    hard(not dep, '#%s: NO package.json / lockfile / tsconfig / vitest / eslint / prettier / knip config in the PR' % n)
    tot = [sum(v[0] for v in p['files'].values()), sum(v[1] for v in p['files'].values())]
    out['prs'][n] = {'head': h, 'branch': p['branch'], 'keys': p['keys'], 'subject': g('log', '-1', '--format=%s', h).strip(), 'merged_tree': mt,
                     'files': files, 'numstat': '%d/%d' % tuple(tot), 'nfiles': len(p['files'])}

print('--- (d) END_TREE in all 24 orders + a second instrument (apply --cached of each BASE..head onto develop\'s tree in a TEMP index)')
def chain(order):
    cur = DEV
    for n in order:
        r = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', cur, PRS[n]['head']], capture_output=True, text=True, env=env)
        if r.returncode != 0: return 'CONFLICT@' + n
        cur = g('commit-tree', r.stdout.split('\n')[0].strip(), '-p', cur, '-p', PRS[n]['head'], '-m', 'g24a chain (scratch only)', env=CE).strip()
    ENDC.append(cur)
    return g('rev-parse', cur + '^{tree}').strip()
ENDC = []
ends = {','.join(o): chain(o) for o in itertools.permutations(sorted(PRS))}
print('  %d orders -> %s' % (len(ends), sorted(set(ends.values()))))
e1 = list(ends.values())[0]
hard(len(set(ends.values())) == 1 and not e1.startswith('CONFLICT'), 'END_TREE identical in all %d orders' % len(ends))
idx = tempfile.mktemp(prefix='g24a_idx_', dir=os.path.dirname(CL)); ienv = dict(env, GIT_INDEX_FILE=idx)
run(['git', '--git-dir', CL, 'read-tree', DEV], env=ienv)
for n in PRS:
    ap = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached'], env=ienv, input=g('diff', '--binary', '--full-index', BASE, PRS[n]['head']), capture_output=True, text=True)
    hard(ap.returncode == 0, 'second instrument: apply --cached #%s rc %d %s' % (n, ap.returncode, ap.stderr.strip()[:120]))
e3 = run(['git', '--git-dir', CL, 'write-tree'], env=ienv).strip(); os.remove(idx)
hard(e3 == e1, 'second instrument (apply --cached) %s == END_TREE' % e3)
UNION = sorted(f for n in PRS for f in PRS[n]['files'])
if e1.startswith('CONFLICT'):
    st = 'NONE (%s)' % e1; hard(False, 'END_TREE could not be built over this develop (%s)' % e1); e1 = e3
else:
    st = g('diff', '--shortstat', DEV, e1).strip(); print('  develop -> END_TREE:', st)
    hard(sorted(g('diff', '--name-only', DEV, e1).split()) == UNION, 'END_TREE diff vs develop == the union of the %d batch paths' % len(UNION))
    for n in PRS:
        for fe in out['prs'][n]['files']:
            eb = g('rev-parse', '%s:%s' % (e1, fe['path'])).strip()
            hard(eb == fe['head_blob'], 'END_TREE blob of %s == #%s head blob (the merged-blob target)' % (fe['path'].rsplit('/', 1)[1], n))
out['end_tree'] = e1; out['end_shortstat'] = st; out['union'] = UNION
r41 = subprocess.run(['git', '--git-dir', CL, 'merge-tree', '--write-tree', '--name-only', ENDC[0] if ENDC else DEV, H1241], capture_output=True, text=True, env=env)
print('  CONTEXT ONLY (#1241 is NOT graded): merge-tree(a commit whose tree is the END_TREE, #1241 head) rc %d — %s' % (r41.returncode, 'CONFLICTS (as expected: both rewrite the reader)' if r41.returncode == 1 else 'clean' if r41.returncode == 0 else 'error'))
out['r1241_over_end'] = r41.returncode

print('--- (e) #1243 KS-1117 + KS-1300 items 2-4 (READ + a Python port of parserImportSites: PREDICTION only)')
H43 = PRS['1243']['head']
yb = g('cat-file', 'blob', '%s:%sutils/yaml.ts' % (BASE, P)); yh = g('cat-file', 'blob', '%s:%sutils/yaml.ts' % (H43, P))
hard("const text = source.startsWith('\\uFEFF') ? source.slice(1) : source;" in yh and 'return loadYaml(text);' in yh and 'return loadYaml(source);' in yb,
     '#1243 yaml.ts: ONE leading U+FEFF stripped (startsWith + slice(1)), loadYaml(text) at head; loadYaml(source) at BASE')
yl = yh.split('\n'); print('  yaml.ts line map at head: strip %s | loadYaml(text) %s' % ([i + 1 for i, l in enumerate(yl) if "startsWith('\\uFEFF')" in l], [i + 1 for i, l in enumerate(yl) if 'loadYaml(text)' in l]))
rr = g('cat-file', 'blob', '%s:%stests/unit/support/readYamlRouting.ts' % (H43, P))
hard("export const PARSER_MODULE = ['js', 'yaml'].join('-');" in rr and 'js-yaml' not in rr, '#1243 readYamlRouting.ts assembles the specifier; the literal `js-yaml` occurs 0 times in it')
pats = [r'^\s*import\b[^\n]*[\'"`][^\'"`]*\bjs\-yaml\b', r'^\s*export\b[^\n]*\bfrom\b[^\n]*[\'"`][^\'"`]*\bjs\-yaml\b',
        r'\brequire\s*\(\s*[\'"`][^\'"`]*\bjs\-yaml\b', r'\bimport\s*\(\s*[\'"`][^\'"`]*\bjs\-yaml\b']
def sites(src): return [l.strip() for l in src.split('\n') if any(re.search(x, l) for x in pats)]
def old_sites(src): return [l for l in src.split('\n') if l.startswith('import') and 'js-yaml' in l]
PROBES = [('EVASIVE top-level static', "import { load } from 'js-yaml';", 1), ('EVASIVE indented', "    import { load } from 'js-yaml';", 1),
          ('EVASIVE re-export', "export { load } from 'js-yaml';", 1), ('EVASIVE require', "const { load } = require('js-yaml');", 1),
          ('EVASIVE dynamic', "const y = await import('js-yaml');", 1), ('EVASIVE dynamic indented', "        const y = await import('js-yaml');", 1),
          ('NON-HIT comment', "// we deliberately do not import js-yaml here", 0), ('NON-HIT string', "const label = 'parsed by js-yaml upstream';", 0),
          ('NON-HIT readYaml import', "import { readYaml } from '../../../utils/yaml.ts';", 0),
          ('LEAD multi-line static import (prettier wraps long lists)', "import {\n    load,\n    dump,\n} from 'js-yaml';", 1),
          ('LEAD multi-line re-export', "export {\n    load,\n} from 'js-yaml';", 1),
          ('LEAD `import * as yaml from` split over two lines', "import * as yaml from\n    'js-yaml';", 1),
          ('LEAD createRequire', "const load = createRequire(import.meta.url)('js-yaml').load;", 1),
          ('LEAD `import type` (no runtime load)', "import type { LoadOptions } from 'js-yaml';", 0),
          ('LEAD subpath', "import { load } from 'js-yaml/dist/js-yaml.mjs';", 1)]
PR43 = []
for lab, src, want in PROBES:
    got, old = len(sites(src)), len(old_sites(src)); PR43.append({'label': lab, 'want_hits': want, 'head': got, 'old': old})
    print('    %-58s want %d | head port %d | KS-1110 check %d%s' % (lab, want, got, old, '   <-- DIFFERS' if (got > 0) != (want > 0) else ''))
sc = g('cat-file', 'blob', '%s:%stests/unit/config/sheddingCeiling.test.ts' % (H43, P))
hard("mkdtempSync(join(perfRoot, '.ks1300-canary-'))" in sc and 'rmSync(dir, { recursive: true, force: true })' in sc,
     'LEAD (READ): the CANARY writes a scratch dir INSIDE the package root (perfRoot/.ks1300-canary-*) and removes it in finally')
ign = {f: subprocess.run(['git', '--git-dir', CL, 'cat-file', 'blob', '%s:%s%s' % (H43, P, f)], capture_output=True, text=True).stdout for f in ('.gitignore', '.prettierignore')}
print('  .ks1300-canary- named in the package .gitignore: %s | .prettierignore: %s (a killed run leaves the dir for format:check / eslint / git status to see)' % ('ks1300' in ign['.gitignore'], 'ks1300' in ign['.prettierignore']))
pj = json.loads(g('cat-file', 'blob', '%s:%spackage.json' % (H43, P)))
hard('tsx' in pj.get('devDependencies', {}), '#1243 the canary spawns node_modules/.bin/tsx — tsx is a devDependency (%s)' % pj.get('devDependencies', {}).get('tsx'))
hks = subprocess.run(['git', '--git-dir', CL, 'diff', '--name-only', BASE, H43, '--', '.githooks', 'Blockchain/Dev/scripts', '.github'], capture_output=True, text=True).stdout.split()
hard(not hks, '#1243 touches no hook / preflight / workflow — KS-1300 item 1 (READYAML-UNGATED) NOT built, as disclosed')
out['k1243'] = {'probes': PR43}

print('--- (f) #1244 KS-1111 (READ + a Python port of formatDockerArgsForLog at BASE and head: PREDICTION only)')
H44 = PRS['1244']['head']
kb = g('cat-file', 'blob', '%s:%srunner/k6_docker.ts' % (BASE, P)); kh = g('cat-file', 'blob', '%s:%srunner/k6_docker.ts' % (H44, P))
line = lambda s, k: [l for l in s.split('\n') if l.startswith(k)]
hard(line(kb, 'const SECRET_ENV_NAME') == line(kh, 'const SECRET_ENV_NAME') and len(line(kh, 'const SECRET_ENV_NAME')) == 1,
     '#1244: SECRET_ENV_NAME byte-identical BASE -> head (NO widening of the masked name set): %s' % line(kh, 'const SECRET_ENV_NAME'))
for k in ('const ENV_SHORT_FLAG_TWO_ARG', 'const ENV_SHORT_FLAG_ATTACHED', 'const REDACTED'):
    hard(line(kb, k) == line(kh, k), '#1244: %s byte-identical BASE -> head' % k)
SECRET = re.compile(r'PASSWORD|PASSWD|SECRET|TOKEN|MNEMONIC|(?:^|_)KEY$', re.I)
def mea(a):
    s = a.find('=')
    if s <= 0: return a
    return '%s=***' % a[:s] if SECRET.search(a[:s]) else a
def mas(a):
    m = re.match(r'^-([A-Za-df-z]*)e(.+)$', a, re.S)
    if not m: return a
    eq = '=' if m.group(2).startswith('=') else ''
    return '-%se%s%s' % (m.group(1), eq, mea(m.group(2)[len(eq):]))
def one(a): return '--env=' + mea(a[len('--env='):]) if a.startswith('--env=') else mas(a)
def fmt(argv, head):
    o = []
    for i, a in enumerate(argv):
        pv = argv[i - 1] if i > 0 else None
        if pv is not None and (pv == '--env' or re.match(r'^-[A-Za-z]*e$', pv)):
            m = mea(a); o.append((one(a) if m == a else m) if head else m); continue
        o.append(one(a))
    return ' '.join(o)
ROWS = [('seat L02', ['--label', '-one', '--env=ADMIN_PASSWORD=ks1111-l02-9b3e'], 'ks1111-l02-9b3e', 'masked'),
        ('seat L03', ['--label', '-qe', '-eKEY=ks1111-l03-4d71'], 'ks1111-l03-4d71', 'masked'),
        ('seat L08', ['-u', '-qe', '-e=DB_PASSWORD=ks1111-l08-c052'], 'ks1111-l08-c052', 'masked'),
        ('seat Q1', ['-Pe', 'API_KEY=ks1111-q1-77ac'], 'ks1111-q1-77ac', 'masked'), ('seat Q2', ['-diteADMIN_TOKEN=ks1111-q2-1fe8'], 'ks1111-q2-1fe8', 'masked'),
        ('seat accident cell', ['--label', '-qe', '-eADMIN_PASSWORD=ks1111-acc-3f08'], 'ks1111-acc-3f08', 'masked'),
        ('seat -l boundary cell', ['-l', 'ADMIN_PASSWORD=ks1111-q3-62ba'], 'ks1111-q3-62ba', 'clear'),
        ('LEAD unrowed L01 (secret name)', ['--label', '-e', '--env=ADMIN_PASSWORD=g-l01'], 'g-l01', 'masked'),
        ('LEAD unrowed L04 (KEY)', ['-e', '-e', '-eKEY=g-l04'], 'g-l04', 'masked'),
        ('LEAD unrowed L05 (KEY)', ['--label', '-one', '-qe=KEY=g-l05'], 'g-l05', 'masked'),
        ('LEAD unrowed L07 (secret name)', ['-a', '-e', '--env=ADMIN_PASSWORD=g-l07'], 'g-l07', 'masked'),
        ('control L06', ['--label', '-one', '-e', 'ADMIN_PASSWORD=g-l06'], 'g-l06', 'masked'),
        ('control bare -e NAME', ['-e', 'ADMIN_PASSWORD'], None, 'nothing to mask')]
PR44 = []
for lab, argv, val, want in ROWS:
    b, h = fmt(argv, False), fmt(argv, True)
    bs = 'n/a' if val is None else ('clear' if val in b else 'masked'); hs = 'n/a' if val is None else ('clear' if val in h else 'masked')
    PR44.append({'label': lab, 'argv': argv, 'base': bs, 'head': hs, 'want': want})
    print('    %-34s %-58s BASE %-7s HEAD %-7s want %s' % (lab, ' '.join(argv), bs, hs, want))
hard(all(r['head'] == r['want'] for r in PR44 if r['want'] in ('masked', 'clear')), '#1244 port: every row reads as wanted AT HEAD (PREDICTION)')
hard([r['label'] for r in PR44 if r['base'] == 'clear' and r['want'] == 'masked' and r['label'].startswith('seat')] == ['seat L02', 'seat L03', 'seat L08'],
     '#1244 port: at BASE exactly L02, L03, L08 print clear among the seat\'s rows (the seat\'s "L02, L03, L08 red") — PREDICTION')
print('  LEAD (port, PREDICTION): the unrowed siblings L01/L04/L05/L07, with a secret name, print CLEAR at BASE and are MASKED at head: %s' % [(r['label'], r['base'], r['head']) for r in PR44 if 'unrowed' in r['label']])
out['k1244'] = {'rows': PR44}

print('--- (g) #1245 KS-1313 (READ + a Python port of readSuiteCounts: PREDICTION only; the gate MEASURES through the real code)')
H45 = PRS['1245']['head']; F45 = P + 'tests/unit/utils/unitSuiteSlotIndependence.test.ts'
hb = g('cat-file', 'blob', '%s:%s' % (H45, F45)); db = g('cat-file', 'blob', '%s:%s' % (BASE, F45))
L = hb.split('\n'); ln = lambda s: [i + 1 for i, l in enumerate(L) if s in l]
LM = {'def': ln('export function readSuiteCounts('), 'ret103': ln("return { passed: counts.get('passed') ?? 0, failed: counts.get('failed') ?? 0 };"),
      'call': ln('const counts = readSuiteCounts(output);'), 'callret': [x for x in ln('    return counts;') if ln('const counts = readSuiteCounts(output);') and x > ln('const counts = readSuiteCounts(output);')[0]], 'lastLine': ln('function lastSummaryLine('),
      'labels': ln('const SUMMARY_LABELS ='), 'describe': ln("describe('KS-1313"), 'pin': ln("it('the call site still goes through readSuiteCounts'")}
print('  line map at head: %s' % LM)
hard(len(LM['def']) == 1 and len(LM['ret103']) == 1 and len(LM['call']) == 1 and len(LM['callret']) == 1, 'readSuiteCounts is EXPORTED, defined once; ONE return (the :103-equivalent) and ONE call in childSuiteCounts')
hard('const summary = /Tests' in db and "return { passed: Number(summary[2]), failed: Number(summary[1] ?? '0') };" in db and 'const summary = /Tests' not in hb,
     'develop\'s :99 inline regex + :103 reading exist at BASE and are GONE at head')
hard(db.count("it('") + db.count('it.each(') == 3, 'develop\'s file carries 3 cells (the slot-independence describe)')
dl = db.split('\n'); print('  develop :99/:103 at %s / %s' % ([i + 1 for i, l in enumerate(dl) if 'const summary = /Tests' in l], [i + 1 for i, l in enumerate(dl) if 'return { passed: Number(summary[2])' in l]))
m = re.search(r"describe\('unit-suite slot independence'.*?\n\}\);\n", hb, re.S); m0 = re.search(r"describe\('unit-suite slot independence'.*?\n\}\);\n", db, re.S)
hard(bool(m) and bool(m0) and m.group(0) == m0.group(0), 'the slot-independence describe (the :127/:262 matrix, item 1 / F4) is byte-identical develop -> head: the budget is untouched')
cfg = [g('rev-parse', '%s:%svitest.unit.config.ts' % (r, P)).strip() for r in (BASE, H45)]
hard(len(set(cfg)) == 1, 'vitest.unit.config.ts blob identical at BASE and head (%s)' % cfg[0][:12])
LABELS = ['failed', 'passed', 'expected fail', 'skipped', 'todo']
def rsc(o, variant='head'):
    o2 = re.sub(r'\x1b\[[0-9;]*m', '', o)
    tl = [l for l in o2.split('\n') if re.match(r'^\s*Tests\s+(.+?)\s*$', l)]
    if not tl: return None
    pick = tl[0] if variant == 'first' else tl[-1]
    line_ = re.match(r'^\s*Tests\s+(.+?)\s*$', pick).group(1)
    sp = re.match(r'^(.*\S)\s+\((\d+)\)$', line_)
    if not sp: return None
    c = {}
    for raw in sp.group(1).split('|'):
        seg = re.match(r'^(\d+) (.+)$', raw.strip())
        if not seg: return None
        if seg.group(2) not in LABELS or seg.group(2) in c:
            if variant != 'dupok' or seg.group(2) not in LABELS: return None
        c[seg.group(2)] = int(seg.group(1))
    if variant != 'nosum' and sum(c.values()) != int(sp.group(2)): return None
    r = {'passed': c.get('passed', 0), 'failed': c.get('failed', 0)}
    return {'passed': r['failed'], 'failed': r['passed']} if variant == 'swap' else r
def rsc_dev(o):
    m_ = re.search(r'Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)', o)
    return None if m_ is None else {'passed': int(m_.group(2)), 'failed': int(m_.group(1) or 0)}
# the drafter's OWN captures (liveshape_2.out; drafter_liveshape_g24a.sh; vitest 4.1.11 from an npm ci of the #1245 head's lockfile; piped;
# fixtures outside any package). S13/S14/S19 carry the Tests-shaped lines of stdout, then stderr, in the order childSuiteCounts concatenates them.
CAP = [('S01 fail-only', '      Tests  1 failed (1)', {'passed': 0, 'failed': 1}), ('S02 skip-only', '      Tests  1 skipped (1)', {'passed': 0, 'failed': 0}),
       ('S03 todo-only', '      Tests  1 todo (1)', {'passed': 0, 'failed': 0}), ('S04 expected-fail-only', '      Tests  1 expected fail (1)', {'passed': 0, 'failed': 0}),
       ('S05 expected-fail+pass', '      Tests  1 passed | 1 expected fail (2)', {'passed': 1, 'failed': 0}),
       ('S06 fail+pass+skip', '      Tests  1 failed | 1 passed | 1 skipped (3)', {'passed': 1, 'failed': 1}),
       ('S07 pass-only', '      Tests  1 passed (1)', {'passed': 1, 'failed': 0}),
       ('S08 multi-file', ' Test Files  1 failed | 1 passed (2)\n      Tests  1 failed | 1 passed | 1 skipped (3)', {'passed': 1, 'failed': 1}),
       ('S09 all-failed', '      Tests  3 failed (3)', {'passed': 0, 'failed': 3}),
       ('S10 every label', '      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (8)', {'passed': 2, 'failed': 2}),
       ('S11 orientation', '      Tests  2 failed | 3 passed (5)', {'passed': 3, 'failed': 2}),
       ('S12 beforeAll throws (Test Files 1 failed, rc 1)', ' Test Files  1 failed (1)\n      Tests  2 skipped (2)', {'passed': 0, 'failed': 0}),
       ('S13 lookalike console.log (stdout, BEFORE the summary)', '      Tests  5 passed (5)\n Test Files  1 failed (1)\n      Tests  1 failed | 1 passed (2)\n', {'passed': 1, 'failed': 1}),
       ('S14 lookalike console.error (stderr, AFTER the summary in stdout+stderr)', ' Test Files  1 failed (1)\n      Tests  1 failed | 1 passed (2)\n\nstderr | a.test.ts > logs\n      Tests  5 passed (5)\n', {'passed': 1, 'failed': 1}),
       ('S15 no tests', '      Tests  no tests', None), ('S16 ctx.skip() at runtime', '      Tests  1 passed | 1 skipped (2)', {'passed': 1, 'failed': 0}),
       ('S17 it.fails that passes (unexpected pass)', '      Tests  1 failed | 1 passed (2)', {'passed': 1, 'failed': 1}),
       ('S19 a failing string diff whose context line is Tests-shaped (stderr)', ' Test Files  1 failed (1)\n      Tests  1 failed | 1 passed (2)\n\n- Expected\n+ Received\n\n  a\n        Tests  9 passed (9)\n- c\n+ b\n', {'passed': 1, 'failed': 1})]
PRED45 = []
for lab, s, want in CAP:
    hd, dv = rsc(s), rsc_dev(s); PRED45.append({'shape': lab, 'want': want, 'head_port': hd, 'develop_port': dv})
    print('    %-72s want %-26s HEAD-port %-26s DEVELOP-port %s%s' % (lab, want, hd, dv, '   <-- HEAD WRONG' if hd != want else ''))
MAND = ['S01', 'S02', 'S03', 'S05', 'S06', 'S07', 'S08']
hard(all(r['head_port'] == r['want'] for r in PRED45 if r['shape'][:3] in MAND), 'PREDICTION (port): the head reads every MANDATED shape (fail-only, skip-only, todo-only, expected-fail+pass, fail+pass+skip, pass-only, multi-file) correctly')
wrong = [r['shape'] for r in PRED45 if r['head_port'] != r['want']]
print('  PREDICTION (port + the drafter\'s live captures, liveshape_lift_2.out): the head is WRONG on %s — the LAST-MATCH exposure: stderr follows stdout in `${stdout}\\n${stderr}`, so any Tests-shaped stderr line (console.error, a failing string diff) becomes the verdict' % wrong)
# tamper predictions: which KS-1313 cells red (by label) under each arm
CELLS = [('fail-only', '      Tests  1 failed (1)', {'passed': 0, 'failed': 1}), ('skip-only', '      Tests  1 skipped (1)', {'passed': 0, 'failed': 0}),
         ('todo-only', '      Tests  1 todo (1)', {'passed': 0, 'failed': 0}), ('expected-fail', '      Tests  1 expected fail (1)', {'passed': 0, 'failed': 0}),
         ('pass-only', '      Tests  1 passed (1)', {'passed': 1, 'failed': 0}), ('all-failed', '      Tests  3 failed (3)', {'passed': 0, 'failed': 3}),
         ('mixed', '      Tests  1 failed | 2 passed | 1 skipped | 1 todo (5)', {'passed': 2, 'failed': 1}),
         ('every label', '      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (8)', {'passed': 2, 'failed': 2}),
         ('LAST line', '      Tests  5 passed (5)\n\n      Tests  1 failed | 1 passed (2)', {'passed': 1, 'failed': 1}),
         ('null: no Tests line', 'some other output\n', None), ('null: no tests', '      Tests  no tests', None),
         ('null: sum != total', '      Tests  1 failed | 1 passed (5)', None), ('null: unknown label', '      Tests  1 flaky (1)', None),
         ('null: repeated label', '      Tests  1 passed | 1 passed (2)', None), ('null: repeat surviving sum', '      Tests  2 passed | 1 passed (1)', None),
         ('null: no count', '      Tests  passed (1)', None)]
def sumcell(fn): return fn(CELLS[7][1]) == {'passed': 2, 'failed': 2} and fn('      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (9)') is None
ARMS = {'HEAD': lambda o: rsc(o), 'R-D develop\'s :99/:103 reading in readSuiteCounts': rsc_dev, 'T-103 swap at :%s' % LM['ret103']: lambda o: rsc(o, 'swap'),
        'T-FIRST (seat T-2)': lambda o: rsc(o, 'first'), 'T-NOSUM (seat T-3)': lambda o: rsc(o, 'nosum'), 'T-DUPOK (seat T-5)': lambda o: rsc(o, 'dupok')}
TP = {}
for lab, fn in ARMS.items():
    red = [c for c, s, w in CELLS if fn(s) != w] + ([] if sumcell(fn) else ['the sum check is a real check'])
    TP[lab] = red; print('  PREDICTED (port) %-52s -> RED %s' % (lab, red or 'NONE'))
hard(TP['HEAD'] == [], 'the head reading satisfies every value cell under the port (the seat\'s green, reproduced statically)')
hard(len(TP['R-D develop\'s :99/:103 reading in readSuiteCounts']) >= 5, 'develop\'s reading reds at least five KS-1313 cells (RED at base is predictable)')
print('  T-CALL predictions (READ): (i) :%s back to develop\'s inline regex -> the call-site pin RED (its `toContain(\'readSuiteCounts(output)\')`), the reader cells GREEN;'
      ' (ii) :%s `return counts;` -> swapped -> the pin GREEN (the text is still there), the KS-1313 cells GREEN, ONLY the :262 matrix RED; (iii) a comment carrying'
      ' `readSuiteCounts(output)` beside an inline regex -> the pin GREEN (a SOURCE-TEXT pin, CALLSITE-SCRAPE)' % (LM['call'], LM['callret']))
out['k1245'] = {'line_map': LM, 'captures': PRED45, 'head_wrong': wrong, 'tamper_pred': TP}

print('--- (h) vitest 4.1.11 as pinned: the renderer of a PIPED run\'s final `Tests` line (READ from the npm tarball)')
lock = g('cat-file', 'blob', '%s:%spackage-lock.json' % (H45, P))
m = re.search(r'"node_modules/vitest": \{\s*"version": "([^"]+)"', lock); LV = m.group(1) if m else 'UNREAD'
hard(LV == '4.1.11', 'the package lockfile at the #1245 head pins vitest 4.1.11')
ND = os.path.join(SP, 'g24a_sp', 'npm'); PK = os.path.join(ND, 'package'); VREAD = {'version': 'UNREAD'}
try:
    if not os.path.isdir(PK):
        os.makedirs(ND, exist_ok=True)
        subprocess.run(['perl', '-e', 'alarm 120; exec @ARGV', 'npm', 'pack', 'vitest@' + LV, '--pack-destination', ND], capture_output=True, text=True, check=True)
        with tarfile.open(os.path.join(ND, 'vitest-%s.tgz' % LV)) as tf: tf.extractall(ND)
    VREAD['version'] = json.load(open(os.path.join(PK, 'package.json')))['version']
    ch = os.path.join(PK, 'dist', 'chunks'); src = {f: open(os.path.join(ch, f), encoding='utf-8', errors='replace').read() for f in os.listdir(ch) if f.endswith('.js')}
    ut = [f for f, s in src.items() if 'function getStateString(tasks' in s]
    if ut:
        us = src[ut[0]]; seg = us[us.index('function getStateString(tasks'):][:1600]
        VREAD.update({'utils_chunk': ut[0], 'every_segment_conditional': all(('%s ? ' % w) in seg for w in ('failed', 'passed', 'expectedFail', 'skipped', 'todo')),
                      'expected_fail_excluded_from_passed': 'Exclude expected failures from passed count' in seg, 'total_is_tasks_length': '` (${tasks.length})`' in seg,
                      'label_order': [w for w in ('failed`', 'passed`', 'expected fail`', 'skipped`', 'todo`') if w in seg]})
        for k in sorted(VREAD): print('  READ vitest: %s = %s' % (k, VREAD[k]))
except Exception as e:
    print('  vitest dist UNREAD (not a refusal; the gate measures at runtime): %s' % e)
out['vitest_lock'] = LV; out['vitest_read'] = VREAD

print('--- (k) #1248 KS-1143 GF-2 (READ; the gate re-runs L3\'s tamper matrix, T-2 FIRST)')
H48 = PRS['1248']['head']
b48 = g('cat-file', 'blob', '%s:%s' % (H48, F48)); d48 = g('cat-file', 'blob', '%s:%s' % (BASE, F48))
L48 = b48.split('\n'); ln48 = lambda s: [i + 1 for i, l in enumerate(L48) if s in l]
LM48 = {'continuations': ln48('const parserContinuations = (body: ts.Node): ts.Node[] => {'), 'filter_T2': ln48('if (ts.isArrowFunction(a) || ts.isFunctionExpression(a)) conts.push(a);'),
        'walk': ln48('for (const cont of parserContinuations(body)) walk(cont);'), 'W7': ln48("it('W7 KS-1143 GF-2"), 'W8': ln48("it('W8 KS-1143 GF-2 CONTROL"),
        'W2': ln48("it('W2 CONTROL"), 'W3': ln48("it('W3 CONTROL"), 'census': ln48("it('no service has grown an undeclared parser outside its entrypoint'"),
        'limit': ln48('DISCLOSED LIMIT, same direction as KS-1143')}
print('  line map at head: %s' % LM48)
hard(all(len(v) == 1 for v in LM48.values()), '#1248: the continuation walk, the T-2 filter line, the walk call, W2, W3, W7, W8, the LEG F census cell and the disclosed-limit comment each occur ONCE at head')
hard('      walk(body);' in d48.split('\n') and '      walk(body);' not in L48, '#1248: develop walked the WHOLE wrapper body (`walk(body);`); the head walks only the parser continuations')
lc = subprocess.run(['git', '--git-dir', CL, 'rev-parse', '--verify', '-q', L3C + '^{commit}'], capture_output=True, text=True).stdout.strip()
if lc:
    pid = lambda a, b: subprocess.run(['git', 'patch-id', '--stable'], input=g('diff', a, b), capture_output=True, text=True).stdout.split()[:1]
    same_pid = pid(lc + '^', lc) == pid(BASE, H48); same_blob = g('rev-parse', '%s:%s' % (lc, F48)).strip() == g('rev-parse', '%s:%s' % (H48, F48)).strip()
    par_blob = g('rev-parse', '%s^:%s' % (lc, F48)).strip() == g('rev-parse', '%s:%s' % (BASE, F48)).strip()
    hard(same_pid and same_blob, '#1248 is a FAITHFUL cherry-pick of L3\'s %s (%s): patch-id equal %s, file blob equal %s; L3\'s parent blob == develop\'s %s' % (L3C, lc, same_pid, same_blob, par_blob))
else:
    print('  L3\'s %s is NOT readable in this clone (a moved-kit clone may not carry it) — the cherry-pick faithfulness was measured at drafting (predict_2.out); the gate re-reads it' % L3C)
out['k1248'] = {'line_map': LM48, 'l3_commit': lc or 'UNREAD'}
try:
    pl = open(L6PUSH + 's-l6-ks1143-push.out', encoding='utf-8', errors='replace').read()
    def after(hdr):
        i = pl.find(hdr); m_ = re.search(r'(\d+) passed, (\d+) failed', pl[i:]) if i >= 0 else None
        return '%s/%s' % m_.groups() if m_ else 'NOT FOUND'
    stop = {'pre_push_hook_base': after('pre_push_hook_base.test.sh ==='), 'fixture_guard': after('pre_push_hook_base_fixture_guard.test.sh ==='),
            'shell_suites': (re.findall(r'shell suites: (\d+ passed, \d+ failed, \d+ skipped \(of \d+\))', pl) or ['NOT FOUND'])[-1],
            'preflight': (re.findall(r'PREFLIGHT [A-Z]+ — [^\n]*', pl) or ['NOT FOUND'])[-1], 'legs': (re.findall(r'  legs [0-9 ]+ — [^\n]*', pl) or ['NOT FOUND'])[-1],
            'fixture_build_failed': len(re.findall(r'(?m)^FIXTURE BUILD FAILED', pl)), 'control_absent_header': after('=== no_such_suite_g24a.test.sh ===')}
    print('  READ ONLY — #1248\'s push log (the seat record, anchored to each suite\'s `=== …test.sh ===` header): %s' % stop)
    hard(stop['pre_push_hook_base'] == '28/0' and stop['fixture_guard'] == '6/0' and stop['shell_suites'].startswith('60 passed, 0 failed') and stop['fixture_build_failed'] == 0
         and stop['control_absent_header'] == 'NOT FOUND', '#1248 push log: the fleet STOP count 28/0, 6/0, 60 of 60, 0 FIXTURE BUILD FAILED (anchored read; control header NOT FOUND)')
except OSError as e:
    stop = {'error': str(e)}; print('  the #1248 push log is UNREAD: %s (the gate reads it)' % e)
out['k1248']['push_log'] = stop

print('--- (i) branch names through the hyphenated-key scanner (own keys only)')
for n, p in PRS.items():
    ks = sorted(set('KS-' + k for k in re.findall(r'(?i)\bks-(\d+)\b', p['branch'])))
    hard(bool(ks) and set(ks) <= set(p['keys']), '#%s branch keys %s ⊆ own %s' % (n, ks, p['keys']))
print('--- (j) the fleet STOP count (static reference; #1248 is the only PR whose push ran the Blockchain/Dev preflight)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
def nsuites(rev): return sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots).splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
out['suites_dev'] = nsuites(REAL_DEV); out['suites_end'] = nsuites(e1)
print('  run-shell-suites.sh ROOTS `*.test.sh`: develop %d | END_TREE %d' % (out['suites_dev'], out['suites_end']))
UT = P + 'tests/unit'
cnt = lambda rev: sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', UT).splitlines() if f.endswith('.test.ts'))
out['unit_files'] = {'develop': cnt(REAL_DEV), 'end': cnt(e1)}
print('  systemTest/performance unit *.test.ts files: develop %d | END_TREE %d (the seats: 63 files; package counts predicted 1089 develop, +8 #1243, +7 #1244, +18 #1245 -> 1122 END; packages/shared 928 -> 930 with #1248; the gate MEASURES)' % (out['unit_files']['develop'], out['unit_files']['end']))
out['fail'] = len(FAIL)
name = 'pins_gate24T2a.json' if not SIM else 'pins_gate24T2a.SIM-%s.json' % SIM
with open(os.path.join(GS, name), 'w', encoding='utf-8') as f: json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, name), 'at', now()); print('HARD FAILS:', len(FAIL), FAIL)
sys.exit(1 if FAIL else 0)
