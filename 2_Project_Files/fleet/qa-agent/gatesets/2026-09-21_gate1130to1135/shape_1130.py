#!/usr/bin/env python3
"""shape_1130.py — READ-ONLY local object reads in the Secuura checkout (ls-remote, rev-list, rev-parse, diff --raw/--numstat, cat-file, show, ls-tree)
for every Seat B 14th PR whose READY has been captured (mail_seatB14_ready*_pr<N>_*.md, the head parsed from its first line "#<PR> at head <sha40>"),
plus the run-dir reads (canonical patches: bytes/sha256/hunks; tampers: from/to/reds from input.json, plant shas from .plant.out) and the `from`
counts at develop 9f0265eb0 (whole block by exact line-block AND raw substring; first line alone). Re-runnable: it reads whatever READYs exist.
No git write verb anywhere. Output: stdout (tee'd by the caller into shape_1130.out)."""
import glob, hashlib, json, os, re, subprocess, sys, itertools
G = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs'
DEV = '9f0265eb06ecf24d4de18149ce862ad2330a61ee'; DEV_TREE = '23d60cace7c37bc329ccc425e58659e950089a4d'; OLD = '7be81d5c9b109959b559e03652fb092c12de58e8'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('GIT-FAIL', a[:3], p.stderr.strip()[:200]); return ''
    return p.stdout
def blob(rev, path):
    p = git('rev-parse', '-q', '--verify', rev + ':' + path); return p.stdout.strip() if p.returncode == 0 else 'ABSENT'
def sha256(b): return hashlib.sha256(b).hexdigest()
print('shape_1130', now())
# 1. READYs -> (PR n, seat's PR number, key, head)
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB14_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', txt)
    if not m: print('READY parse FAIL', os.path.basename(f)); continue
    seatn, key, prn, head = m.groups()
    tree = re.search(r'Head tree ([0-9a-f]{40})', txt); br = re.search(r'branch\s*\n?\s*(feature/[^\n ,]+)', txt)
    READY[prn] = dict(seat_pr=seatn, key=key, head=head, tree=tree.group(1) if tree else '?', branch=(br.group(1) if br else '?'), file=os.path.basename(f))
    print('READY', os.path.basename(f), '-> seat PR', seatn, key, '#' + prn, 'head', head, 'tree', READY[prn]['tree'], 'branch', READY[prn]['branch'])
# 2. origin
lsr = out('ls-remote', 'origin', 'refs/heads/develop', *['refs/pull/%d/head' % n for n in range(1129, 1137)], 'refs/heads/feature/ks-1273-*', 'refs/heads/feature/ks-1135-*', 'refs/heads/feature/ks-958-*', 'refs/heads/feature/ks-880-*', 'refs/heads/feature/ks-887-*', 'refs/heads/feature/ks-1236-*', 'refs/heads/feature/ks-1006-*')
print('ls-remote', now()); print(lsr.rstrip())
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
print('origin develop', refs.get('refs/heads/develop'), '== pin', refs.get('refs/heads/develop') == DEV)
for prn, r in READY.items():
    ph = refs.get('refs/pull/%s/head' % prn); bh = refs.get('refs/heads/' + r['branch'])
    print('#%s pull/head %s branch %s READY %s -> %s' % (prn, ph, bh, r['head'], 'OK' if ph == r['head'] == bh else 'MISMATCH'))
# 3. local objects per landed head
dt = out('rev-parse', DEV + '^{tree}').strip(); print('develop tree', dt, dt == DEV_TREE)
CHANGED = {}; PERPR = {}
for prn, r in sorted(READY.items()):
    h = r['head']
    if git('cat-file', '-e', h + '^{commit}').returncode: print('#%s head %s NOT in local objects yet' % (prn, h[:9])); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    subj = out('log', '-1', '--format=%s', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', DEV, h).strip().splitlines()
    ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', DEV, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files[path] = ('ABSENT' if b1 == '0' * 40 else b1, b2, st, m2)
    print('#%s %s head %s parent==DEV %s | develop...head behind/ahead %s | tree %s == READY tree %s | subject %r (%d chars)' % (prn, r['key'], h[:9], par == [DEV], lr, t, t == r['tree'], subj, len(subj)))
    for p_, v in files.items():
        cnt = out('show', h + ':' + p_)
        print('   %s %s  %s -> %s  numstat +%s/-%s  mode %s  lines %d  bytes %d  sha256 %s  under __tests__/: %s' % (v[2], p_, v[0][:12], v[1], ns[p_][0], ns[p_][1], v[3], cnt.count('\n'), len(cnt.encode()), sha256(cnt.encode())[:16], '__tests__/' in p_))
    PERPR[prn] = files
    for p_, v in files.items(): CHANGED.setdefault(p_, []).append(prn)
print('union paths', len(CHANGED), '| pairwise overlaps', [(p_, v) for p_, v in CHANGED.items() if len(v) > 1] or 'NONE', '| pairs', len(list(itertools.combinations(PERPR, 2))))
# 4. target + tamper + sibling files at develop (and at OLD for the ks1194 pair)
D = 'Blockchain/Dev/'
PATHS = {'PR1 target': D + 'scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh', 'PR2 target': 'systemTest/__tests__/manifest_quarantine.test.sh',
         'PR6 target(product)': D + 'scripts/check-shared-relink.sh', 'PR6 new suite': D + 'scripts/__tests__/check_shared_relink_case.test.sh',
         'PR3+PR5 target': D + 'services/security/src/__tests__/ks869-connector-id-persisted.test.ts', 'PR4 target': D + 'services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts',
         'tamper PR1 job': 'Blockchain/Testing/jobs/04-container-trivy.sh', 'tamper PR2 manifest.ts': 'systemTest/fixtures/manifest.ts', 'tamper PR3/PR5 security index.ts': D + 'services/security/src/index.ts',
         'tamper PR4 users.ts': D + 'services/auth/src/routes/users.ts',
         'sib image_filter': D + 'scripts/__tests__/container_trivy_image_filter.test.sh', 'sib failed_scan_is_loud': D + 'scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh',
         'sib check_shared_relink.test.sh': D + 'scripts/__tests__/check_shared_relink.test.sh', 'sib tooling_tokens': D + 'scripts/__tests__/check_shared_relink_tooling_tokens.test.sh',
         'sib ks949 seed idempotence': D + 'scripts/__tests__/ks949_main_seed_idempotence.test.sh', 'sib preflight_deps': D + 'scripts/__tests__/preflight_deps.test.sh',
         'run-shell-suites.sh': D + 'scripts/run-shell-suites.sh', 'preflight.sh': D + 'scripts/preflight/preflight.sh', 'pre-push hook': '.githooks/pre-push',
         'security pkg': D + 'services/security/package.json', 'security vitest.config': D + 'services/security/vitest.config.ts', 'security tsconfig': D + 'services/security/tsconfig.json', 'security lock': D + 'services/security/package-lock.json',
         'auth pkg': D + 'services/auth/package.json', 'auth vitest.config': D + 'services/auth/vitest.config.ts', 'auth tsconfig': D + 'services/auth/tsconfig.json', 'auth lock': D + 'services/auth/package-lock.json', 'auth index.ts': D + 'services/auth/src/index.ts',
         'Dev package.json': D + 'package.json', 'Dev lock': D + 'package-lock.json', 'eslint.config.mjs': D + 'eslint.config.mjs', 'fix-libsodium': D + 'scripts/fix-libsodium-symlink.js', 'shared pkg': D + 'packages/shared/package.json'}
print('--- files at develop', DEV[:9], '(blob / lines / bytes / sha256 / mode) and at', OLD[:9], '; same at every landed head?')
for label, p_ in PATHS.items():
    b = blob(DEV, p_); bo = blob(OLD, p_)
    if b == 'ABSENT': print('  %-34s %-70s ABSENT at develop | at %s: %s' % (label, p_, OLD[:9], bo)); continue
    cnt = git('show', DEV + ':' + p_).stdout; mode = out('ls-tree', DEV, p_).split()[0]
    heads_same = {prn: blob(r['head'], p_) == b for prn, r in READY.items() if not git('cat-file', '-e', r['head']).returncode}
    print('  %-34s %-70s %s %5d %6d %s %s | at %s %s | same at heads %s' % (label, p_, b[:12], cnt.count('\n'), len(cnt.encode()), sha256(cnt.encode())[:12], mode, OLD[:9], 'SAME' if bo == b else bo[:12], heads_same))
# 5. run dirs: canonical patches + tampers + from counts at develop
RUNS = [('PR1', 'KS-1273', '2026-09-21_ks1273-ornith35b-night2', 'out.md.checker/patch.diff'), ('PR2', 'KS-1135', '2026-09-21_ks1135-ornith35b-night', 'out.md.checker/patch.diff'),
        ('PR6', 'KS-958', '2026-09-16_ks958-ornith35b-night2', 'recheck/out.md.checker/section_1.diff'), ('PR6', 'KS-958', '2026-09-16_ks958-ornith35b-night2', 'recheck/out.md.checker/section_2.diff'),
        ('PR3', 'KS-880', '2026-09-21_ks880-ornith35b-night2', 'out.md.checker/patch.diff'), ('PR5', 'KS-887', '2026-09-16_ks887-ornith35b-night2', 'out.md.checker/patch.diff'),
        ('PR4a', 'KS-1236', '2026-09-21_ks1236-ornith35b-night2', 'out.md.checker/patch.diff'), ('PR4b', 'KS-1006', '2026-09-21_ks1006-ornith35b-night2', 'out.md.checker/patch.diff')]
print('--- canonical patches')
for pr, key, run, rel in RUNS:
    p_ = os.path.join(LM, run, rel); b = open(p_, 'rb').read(); t = b.decode('utf-8', 'replace').splitlines()
    print('  %-4s %-7s %s/%s %5d B sha256 %s +++ %d - %d + %d lone+ %d hunks %s paths %s' % (pr, key, run, rel, len(b), sha256(b), sum(1 for l in t if l.startswith('+++')), sum(1 for l in t if l.startswith('-') and not l.startswith('---')), sum(1 for l in t if l.startswith('+') and not l.startswith('+++')), sum(1 for l in t if l == '+'), [l.split('@@')[1].strip() for l in t if l.startswith('@@')], [l[4:] for l in t if l.startswith('+++ ')]))
GOLD = {'PR1': 'runs/2026-09-21_gate1119rows-drafter-precheck/TRIVYYAMLEXITCODE/out.md.checker/patch.diff', 'PR2': 'runs/2026-09-21_gate1119rows-drafter-precheck/MANIFESTQUARANTINESTDERR/out.md.checker/patch.diff', 'PR3': 'runs/2026-09-21_gate1119rows-drafter-precheck/OTHERMAPPERDEFAULT/out.md.checker/patch.diff', 'PR4a': 'runs/2026-09-21_siblings-1236-1006-drafter/ALREADYPENDING/out.md.checker/patch.diff', 'PR4b': 'runs/2026-09-21_siblings-1236-1006-drafter/MFANOTENABLED/out.md.checker/patch.diff'}
for pr, rel in GOLD.items():
    p_ = os.path.join('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model', rel)
    print('  golden %-4s %s %s' % (pr, ('%d B sha256 %s' % (os.path.getsize(p_), sha256(open(p_, 'rb').read()))) if os.path.exists(p_) else 'ABSENT', rel))
print('--- tampers (input.json) and their from-counts at develop; plant shas from .plant.out')
for pr, key, run, rel in RUNS:
    if 'section' in rel or key in ('KS-958', 'KS-887'): continue
    ip = os.path.join(LM, run, 'input.json'); d = json.load(open(ip))
    print('  %s %s input.json tip %s test_file %s' % (pr, key, d.get('tip'), d.get('test_file')))
    for tp in d.get('tampers', []):
        cnt = git('show', DEV + ':' + tp['file']).stdout; lines = cnt.split('\n')
        frm = tp['from']; fl = frm.split('\n')
        block_line = sum(1 for i in range(len(lines) - len(fl) + 1) if lines[i:i + len(fl)] == fl); raw_c = cnt.count(frm); first_c = lines.count(fl[0])
        at = [i + 1 for i in range(len(lines) - len(fl) + 1) if lines[i:i + len(fl)] == fl]
        po = os.path.join(LM, run, 'out.md.checker', 'tamper_%s.plant.out' % tp['id']); plant = open(po).read().strip() if os.path.exists(po) else 'NO plant.out'
        vo = os.path.join(LM, run, 'out.md.checker', 'tamper_%s.verdict.out' % tp['id']); verd = open(vo).read().strip()[:160].replace('\n', ' | ') if os.path.exists(vo) else '-'
        print('    %-18s %s :%s  from-lines %d  block-count %d  raw-substring %d  first-line-alone %d  at %s  declared reds %d  | plant.out: %s | verdict: %s' % (tp['id'], tp['file'], tp['line'], len(fl), block_line, raw_c, first_c, at, len(tp.get('reds', [])), plant[:120], verd))
        for rd in tp.get('reds', []): print('        red: %s' % rd)
        print('        from: %r' % frm); print('        to:   %r' % tp['to'])
# KS-887 / KS-958 tamper sites from the brief (from-text copied from git show, asserted by count)
rel = git('show', DEV + ':' + D + 'scripts/check-shared-relink.sh').stdout.split('\n')
for needle in ['        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {', '        else if (L ~ /(^|[^A-Za-z0-9_.-])(node|nodejs|bun|deno)([0-9._-]|[^A-Za-z0-9_.-]|$)/) {']:
    print('  relink needle count %d at %s: %r' % (rel.count(needle), [i + 1 for i, l in enumerate(rel) if l == needle], needle[:60]))
print('  relink `tolower(L) ~` count at develop:', sum(1 for l in rel if 'tolower(L) ~' in l))
sec = git('show', DEV + ':' + D + 'services/security/src/index.ts').stdout.split('\n')
print('  security index.ts `         connector_id)` count %d at %s (KS-887 tamper site)' % (sec.count('         connector_id)'), [i + 1 for i, l in enumerate(sec) if l == '         connector_id)']))
print('  security index.ts `export function rowToApiKey(` at', [i + 1 for i, l in enumerate(sec) if l.startswith('export function rowToApiKey(')], '| `rowToAuditLog(` at', [i + 1 for i, l in enumerate(sec) if 'function rowToAuditLog(' in l])
print('  security index.ts `    name: r.name as string,` at', [i + 1 for i, l in enumerate(sec) if l == '    name: r.name as string,'], '| `    userId: (r.user_id as string) || undefined,` at', [i + 1 for i, l in enumerate(sec) if l == '    userId: (r.user_id as string) || undefined,'])
users = git('show', DEV + ':' + D + 'services/auth/src/routes/users.ts').stdout.split('\n')
print('  users.ts `    if (existingRequest) throw new BadRequestError(...already pending...)` at', [i + 1 for i, l in enumerate(users) if 'A verification request is already pending' in l and 'throw new BadRequestError' in l])
print('  users.ts `MFA is not enabled` throw at', [i + 1 for i, l in enumerate(users) if "throw new BadRequestError('MFA is not enabled')" in l], '| code.length !== 6 lines at', [i + 1 for i, l in enumerate(users) if 'code.length !== 6' in l])
job = git('show', DEV + ':Blockchain/Testing/jobs/04-container-trivy.sh').stdout.split('\n')
print('  job `--exit-code 0` lines at', [i + 1 for i, l in enumerate(job) if '--exit-code 0' in l], '| `--skip-db-update` at', [i + 1 for i, l in enumerate(job) if '--skip-db-update' in l], '| `# KS-1136:` at', [i + 1 for i, l in enumerate(job) if '# KS-1136:' in l])
man = git('show', DEV + ':systemTest/fixtures/manifest.ts').stdout.split('\n')
print('  manifest.ts `quarantineManifest(` signature at', [i + 1 for i, l in enumerate(man) if 'export function quarantineManifest(' in l], '| `const dir = path.dirname(target);` at', [i + 1 for i, l in enumerate(man) if l == '    const dir = path.dirname(target);'])
mq = git('show', DEV + ':systemTest/__tests__/manifest_quarantine.test.sh').stdout.split('\n')
print('  manifest_quarantine.test.sh `TMP="$(mktemp -d)"` at', [i + 1 for i, l in enumerate(mq) if l == 'TMP="$(mktemp -d)"'], '| `trap cleanup EXIT` at', [i + 1 for i, l in enumerate(mq) if l.strip() == 'trap cleanup EXIT'], '| cleanup() at', [i + 1 for i, l in enumerate(mq) if l.startswith('cleanup()')], '| `2>` redirect lines', sum(1 for l in mq if '2>' in l), '| npx tsx lines', sum(1 for l in mq if 'npx tsx' in l or 'npx --offline tsx' in l))
# pre-push hook trigger (READY 2's finding: no legs on a systemTest-only push)
hook = git('show', DEV + ':.githooks/pre-push').stdout.split('\n')
print('  .githooks/pre-push lines', len(hook), '| lines naming Blockchain/Dev:', [(i + 1, l.strip()[:110]) for i, l in enumerate(hook) if 'Blockchain/Dev' in l][:8])
# #1129 foreign head: what does it touch vs our paths?
h1129 = refs.get('refs/pull/1129/head')
if h1129 and not git('cat-file', '-e', h1129 + '^{commit}').returncode:
    mb = out('merge-base', DEV, h1129).strip(); lr = out('rev-list', '--left-right', '--count', DEV + '...' + h1129).split()
    names = out('diff', '--name-only', mb, h1129).strip().splitlines()
    print('  #1129 foreign head %s merge-base %s behind/ahead %s subject %r files %d: %s | ∩ our paths: %s' % (h1129[:9], mb[:9], lr, out('log', '-1', '--format=%s', h1129).strip()[:90], len(names), names[:12], sorted(set(names) & set(PATHS.values())) or 'NONE'))
else:
    print('  #1129 foreign head', h1129, 'NOT in local objects (a fetch is a write — left for the gate, which reads it via the files API)')
# checkout counts
print('--- checkout counts', now())
print('  porcelain non-untracked', git('status', '--porcelain').stdout.splitlines().__len__() - sum(1 for l in git('status', '--porcelain').stdout.splitlines() if l.startswith('??')), '| porcelain total', len(git('status', '--porcelain').stdout.splitlines()), '| worktrees', len(os.listdir(REPO + '/.git/worktrees')), '| for-each-ref', len(git('for-each-ref').stdout.splitlines()))
print('  ' + git('count-objects', '-v').stdout.replace('\n', ' '))
print('done', now())
