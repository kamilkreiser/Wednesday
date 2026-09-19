#!/usr/bin/env python3
"""measure_scratch.py — the drafter's independent reads for #1097-#1099, WITHOUT any git write: develop blobs are read with `git cat-file blob`
(a read) from the Secuura checkout and written as PLAIN FILES into a fresh mktemp dir under the session scratchpad (not a repo); `git apply`
(patch mode, cwd = that dir, strict: no --recount, no fuzz, no whitespace option) applies the canonical patch.diff files; `git hash-object`
(no -w) hashes each result. Measures: (1) the ks1215 file under EVERY non-empty subset and EVERY order of N95-1 / N96-1a / N96-1b (15 orders);
(2) canonical identity of #1097 / #1098 / #1099 head blobs; (3) reverse and crossed controls; (4) all 17 tampers re-planted from each run's
input.json on develop's blob: `from` occurrence count (whole-line for single-line froms, whole-block for the 4-line GUARD froms), the landed
line, the plant sha256 (vs the checker's tamper_<ID>.plant.out) and the pre-plant byte count; (5) the whole-line count of `    requireSuperAdmin,`
and its line numbers. Nothing is deleted."""
import hashlib, itertools, json, os, re, subprocess, sys, tempfile
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd1ce61d-09bc-4b11-b5ed-43cb67420198/scratchpad'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
DEV = 'c87458bdd8a9dd5ae3a082612e467cda5539aebc'
A = 'Blockchain/Dev/services/api-gateway/'
F1215 = A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
F1230 = A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts'
F1062 = A + 'src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts'
HEAD = {1097: 'f5364217952c1cb4d3755fbf8604b3edde124c42', 1098: 'efce14bed4a8adda15bca124fa60ae7d894fa6a6', 1099: 'b68aaf9b4581e67369be33d8ebcf4d61886c039b'}
RUN = {'N92-1': '2026-09-20_ks1230-ornith35b-night', 'N93-1': '2026-09-20_ks1062-ornith35b-night2', 'N95-1': '2026-09-20_ks1238-ornith35b-night3',
       'N96-1a': '2026-09-20_ks1282-ornith35b-night2', 'N96-1b': '2026-09-20_ks1282-ornith35b-night3'}
READY = {('N95-1',): 'f9bff1b332af', ('N96-1a',): '63d5c6876d82', ('N96-1b',): '7c56fdbdcfde', ('N95-1', 'N96-1a'): '86d7faeae0e3',
         ('N95-1', 'N96-1b'): 'f47c8eadf237', ('N96-1a', 'N96-1b'): '6292bafe5906', ('N95-1', 'N96-1a', 'N96-1b'): 'fe235c8aa1d85d28d73a4853890c840bd59e0a7a'}
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, **k)
def blob(rev, p): return sh('git', '-C', REPO, 'cat-file', 'blob', rev + ':' + p).stdout
def rp(x): return sh('git', '-C', REPO, 'rev-parse', '--verify', '-q', x, text=True).stdout.strip()
print('measure_scratch', sh('date', '+%Y-%m-%d %H:%M:%S %Z', text=True).stdout.strip(), '| git', sh('git', '--version', text=True).stdout.split()[2])
X = tempfile.mkdtemp(prefix='meas1097-', dir=SCRATCH); print('scratch (plain files, not a repo; left in place):', X)
bad = []; k = 0
def apply_seq(path, names, extra=()):
    global k; k += 1; W = os.path.join(X, 'w%03d' % k); os.makedirs(os.path.dirname(os.path.join(W, path)))
    open(os.path.join(W, path), 'wb').write(blob(DEV, path))
    for nm in names:
        r = sh('git', 'apply', *extra, RUNS + RUN[nm] + '/out.md.checker/patch.diff', cwd=W, text=True)
        if r.returncode: return None, r.returncode
    return sh('git', 'hash-object', os.path.join(W, path), text=True).stdout.strip(), 0
for nm in RUN:
    ck = RUNS + RUN[nm] + '/out.md.checker/'
    opts = [f for f in os.listdir(ck) if f.endswith('.opts') or re.match(r'section_\d+\.diff$', f)]
    tip = json.load(open(RUNS + RUN[nm] + '/input.json'))['tip']
    d = open(ck + 'patch.diff').read()
    print('  %-6s %s patch.diff sha256 %s  +%d/-%d  +++ headers %d  opts/section files %s  input.json tip == develop %s' % (nm, RUN[nm], hashlib.sha256(d.encode()).hexdigest()[:12],
          sum(1 for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')), sum(1 for l in d.splitlines() if l.startswith('-') and not l.startswith('---')),
          d.count('\n+++ ') + d.startswith('+++ '), opts, tip == DEV))
    if opts or tip != DEV: bad.append(('run shape', nm))
# (1) the ks1215 file: every subset, every order
three = ('N95-1', 'N96-1a', 'N96-1b'); dist = {}
for r_ in (1, 2, 3):
    for sub in itertools.combinations(three, r_):
        got = set()
        for order in itertools.permutations(sub):
            b, rc = apply_seq(F1215, order); got.add(b)
            print('  ks1215 [%s] -> %s rc %d' % (' then '.join(order), b, rc))
        ok = len(got) == 1 and next(iter(got)) is not None and next(iter(got)).startswith(READY[sub])
        print('    subset %s: %d distinct result(s), = READY %s: %s' % ('+'.join(sub), len(got), READY[sub], ok)); dist[sub] = got
        if not ok: bad.append(('order', sub))
h1099 = rp(HEAD[1099] + ':' + F1215); print('  #1099 head blob', h1099, '== all-three-orders blob:', {h1099} == dist[three])
if {h1099} != dist[three]: bad.append('1099 canonical')
# (2) #1097 / #1098 canonical
for n, f, nm in ((1097, F1230, 'N92-1'), (1098, F1062, 'N93-1')):
    b, rc = apply_seq(f, [nm]); hb = rp(HEAD[n] + ':' + f)
    print('  #%d canonical %s -> %s == head blob %s: %s' % (n, nm, b, hb, b == hb))
    if b != hb: bad.append(('canonical', n))
# (3) controls: reverse onto develop refuses; crossed (N92-1 into the ks1062 file's develop blob) refuses
for nm, f in (('N92-1', F1230), ('N93-1', F1062), ('N95-1', F1215), ('N96-1a', F1215), ('N96-1b', F1215)):
    b, rc = apply_seq(f, [nm], ('--reverse',)); print('  CONTROL %s --reverse onto develop blob: rc %d (want non-zero)' % (nm, rc))
    if rc == 0: bad.append(('reverse applied', nm))
k += 1; W = os.path.join(X, 'crossed'); os.makedirs(os.path.dirname(os.path.join(W, F1062))); open(os.path.join(W, F1062), 'wb').write(blob(DEV, F1062))
r = sh('git', 'apply', '--check', RUNS + RUN['N92-1'] + '/out.md.checker/patch.diff', cwd=W, text=True)
print('  CONTROL crossed: N92-1 patch into the ks1062 develop blob refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append('crossed')
# (4) the 17 tampers
for nm in RUN:
    j = json.load(open(RUNS + RUN[nm] + '/input.json'))
    for t in j['tampers']:
        path = t['file'] if t['file'].startswith('Blockchain/') else A + t['file'].split('api-gateway/')[-1]
        src = blob(DEV, path).decode(); fr = t['from']; to = t['to']
        lines = src.split('\n')
        if '\n' in fr:
            n_ = src.count(fr); kind = 'block'
        else:
            n_ = sum(1 for l in lines if l == fr); kind = 'whole-line'
        sub_only = sum(1 for l in lines if fr.split('\n')[0] in l and l != fr.split('\n')[0])
        idx = src.find(fr); landed = src.count('\n', 0, idx) + 1
        out = src.replace(fr, to, 1)
        sha = hashlib.sha256(out.encode()).hexdigest()
        rec = open(RUNS + RUN[nm] + '/out.md.checker/tamper_%s.plant.out' % t['id']).read()
        want = re.search(r'sha256 ([0-9a-f]{12})', rec).group(1); pre = int(re.search(r'\((\d+) ->', rec).group(1))
        ok = n_ == 1 and sha.startswith(want) and pre == len(src.encode()) and landed == int(t['line'])
        print('  %-6s %-18s %s:%d %s x%d (first-line substring-only lines %d) landed %d plant sha256 %s == checker %s: %s | pre-plant bytes %d == %d | reds %s'
              % (nm, t['id'], path.split('/')[-1], t['line'], kind, n_, sub_only, landed, sha[:12], want, ok, len(src.encode()), pre, t['reds']))
        if not ok: bad.append(('tamper', t['id']))
# (5) the bare guard line
pl = blob(DEV, A + 'src/routes/platform.ts').decode().split('\n')
g = [i + 1 for i, l in enumerate(pl) if l == '    requireSuperAdmin,']
print('  platform.ts `    requireSuperAdmin,` whole-line x%d at %s' % (len(g), g))
for p in ('src/routes/admin.ts', 'src/routes/platform.ts', 'src/startup-migrations.ts'):
    print('  develop sha256 %s %s' % (p.split('/')[-1], hashlib.sha256(blob(DEV, A + p)).hexdigest()[:12]))
print('ALL OK' if not bad else 'DISAGREES %r' % bad)
sys.exit(1 if bad else 0)
