#!/usr/bin/env python3
"""measure_scratch.py — drafter's own measurement for the #1100 + #1101 batch, READ-ONLY against the Secuura checkout (cat-file / hash-object only;
no git write verb there). In a PLAIN scratch dir (not a repo) it re-applies each canonical patch.diff STRICT onto develop's blob and hashes the
result; re-plants each of the four tampers by TEXT from the develop blob and hashes the plant; re-reads platform.ts:64 / :67 / :68 and admin.ts:1132
at develop; and re-reads db.retry.test.ts's blob at develop and at each head. Prints ALL OK / rc on the caller's line."""
import hashlib, os, re, subprocess, sys, tempfile
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = 'e470198783bcb1ef0eac94780f87579974051423'
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = os.environ['SCRATCHDIR']
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()
bad = []
def chk(label, got, want):
    ok = got == want
    print('  %-62s %s | want %s: %s' % (label, got, want, ok))
    if not ok: bad.append((label, got, want))

KS1230 = A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts'
KS1215 = A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
ADMIN = A + 'src/routes/admin.ts'; PLAT = A + 'src/routes/platform.ts'
DBRETRY = A + 'src/__tests__/db.retry.test.ts'
PRS = [(1100, '99ce89e741e6c3cad7457af7c91fb6fea86acdff', KS1230, '2026-09-20_ks1230-ornith35b-night2', 'N97-1', '893879a1995031a13d4a1969d24f3aa0c60e5d21'),
       (1101, 'dc40087e756c598ca8b2957da7fbf1ec01945df8', KS1215, '2026-09-20_ks1282-ornith35b-night4', 'N99-1', '50298953359ead9f947ac9f20f455a529dd2543a')]
X = tempfile.mkdtemp(prefix='meas1100-', dir=SCRATCH)
print('scratch (plain files, not a repo):', X)

print('1. CANONICAL-PATCH IDENTITY (develop blob as a plain file; git apply strict; git hash-object without -w)')
for n, h, path, run, name, headblob in PRS:
    W = os.path.join(X, 'canon-%d' % n); os.makedirs(os.path.join(W, os.path.dirname(path)), exist_ok=True)
    open(os.path.join(W, path), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + path))
    patch = RUNS + run + '/out.md.checker/patch.diff'
    r = subprocess.run(['git', 'apply', patch], cwd=W, capture_output=True, text=True)
    got = subprocess.run(['git', 'hash-object', os.path.join(W, path)], capture_output=True, text=True).stdout.strip()
    print('  #%d %s apply rc %d %s' % (n, name, r.returncode, r.stderr.strip()[:100]))
    chk('#%d %s over develop -> blob' % (n, name), got, headblob)
    chk('#%d head blob in the repo' % n, rp(h + ':' + path), headblob)
    print('    patch sha256 %s' % hashlib.sha256(open(patch, 'rb').read()).hexdigest()[:12],
          '| + lines %d | - lines %d' % (sum(1 for l in open(patch) if l.startswith('+') and not l.startswith('+++')),
                                          sum(1 for l in open(patch) if l.startswith('-') and not l.startswith('---'))))
    # control: reverse onto the develop blob must refuse
    W2 = os.path.join(X, 'rev-%d' % n); os.makedirs(os.path.join(W2, os.path.dirname(path)), exist_ok=True)
    open(os.path.join(W2, path), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + path))
    rr = subprocess.run(['git', 'apply', '--reverse', '--check', patch], cwd=W2, capture_output=True, text=True)
    print('  CONTROL #%d %s --reverse onto the develop blob refuses: rc %d (want non-zero)' % (n, name, rr.returncode))
    if rr.returncode == 0: bad.append(('reverse control applied', n))
# control: crossed patch
W3 = os.path.join(X, 'crossed'); os.makedirs(os.path.join(W3, os.path.dirname(KS1230)), exist_ok=True)
open(os.path.join(W3, KS1230), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + KS1230))
rc3 = subprocess.run(['git', 'apply', '--check', RUNS + '2026-09-20_ks1282-ornith35b-night4/out.md.checker/patch.diff'], cwd=W3, capture_output=True, text=True).returncode
print('  CONTROL crossed: N99-1 into the ks1230 develop blob refuses: rc %d (want non-zero)' % rc3)
if rc3 == 0: bad.append(('crossed control applied',))

print('2. THE FOUR TAMPER PLANTS, re-planted by TEXT from the DEVELOP blob (each ALONE, never stacked)')
TAMPERS = [('LASTOF2NULLMIXED', ADMIN, 1132, '2026-09-20_ks1230-ornith35b-night2'),
           ('LASTOF4NULL',      ADMIN, 1132, '2026-09-20_ks1230-ornith35b-night2'),
           ('SUPERROLESWIDEN',  PLAT,   64,  '2026-09-20_ks1282-ornith35b-night4'),
           ('SUPERADMITSANYUSER', PLAT, 68,  '2026-09-20_ks1282-ornith35b-night4')]
import json
srcs = {}
for p in (ADMIN, PLAT):
    raw = gitb('cat-file', 'blob', DEV + ':' + p)
    srcs[p] = raw
    print('  %s at develop: blob %s sha256 %s bytes %d' % (p.split('/')[-1], rp(DEV + ':' + p), hashlib.sha256(raw).hexdigest()[:12], len(raw)))
for tid, path, line, run in TAMPERS:
    inp = json.load(open(RUNS + run + '/input.json'))
    t = [x for x in inp['tampers'] if x['id'] == tid][0]
    raw = srcs[path]; txt = raw.decode('utf-8')
    lines = txt.split('\n')
    whole = sum(1 for l in lines if l == t['from'])
    subs = txt.count(t['from'])
    landed = [i + 1 for i, l in enumerate(lines) if l == t['from']]
    planted = txt.replace(t['from'], t['to'], 1) if whole == 1 else None
    # plant by exact whole-line replacement at its single occurrence
    if whole == 1:
        i = landed[0] - 1; lines2 = list(lines); lines2[i] = t['to']
        planted = '\n'.join(lines2)
    psha = hashlib.sha256(planted.encode()).hexdigest()[:12] if planted else None
    # the checker's own recorded plant sha, if its plant.out carries one
    po = open(RUNS + run + '/out.md.checker/tamper_%s.plant.out' % tid).read()
    m = re.search(r'([0-9a-f]{64})', po)
    print('  %-18s %s:%d | whole-line matches %d (raw substring %d) landed %s | plant sha256 %s | bytes %d -> %d | checker plant.out sha %s'
          % (tid, path.split('/')[-1], line, whole, subs, landed, psha, len(raw), len(planted.encode()) if planted else -1, (m.group(1)[:12] if m else '(none in plant.out)')))
    if whole != 1 or subs != 1: bad.append(('from match count', tid, whole, subs))
    if landed != [line]: bad.append(('landed line', tid, landed, line))
    if m and m.group(1)[:12] != psha: bad.append(('plant sha != checker', tid, psha, m.group(1)[:12]))
    print('     verdict.out tail:', open(RUNS + run + '/out.md.checker/tamper_%s.verdict.out' % tid).read().strip().splitlines()[-1][:150])

print('3. THE :67 -> :68 CORRECTION, re-read at develop (Wednesday brief said :67; the seat says :68)')
pl = srcs[PLAT].decode('utf-8').split('\n')
for ln in (64, 66, 67, 68, 69):
    print('  platform.ts:%d %r' % (ln, pl[ln - 1]))
chk('platform.ts:67 is the const user line', pl[66], '  const user = req.user;')
chk('platform.ts:68 is the guard line', pl[67], '  if (!user || !SUPER_ROLES.includes(user.role)) {')
chk('platform.ts:64 is the SUPER_ROLES line', pl[63], "const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];")
ad = srcs[ADMIN].decode('utf-8').split('\n')
print('  admin.ts:1132 %r' % ad[1131])
chk('admin.ts:1132 is the KS-1230 continue line', ad[1131], '        if (types === undefined || types === null) continue;')
print('  bare "    requireSuperAdmin," whole-line count in platform.ts: %d' % sum(1 for l in pl if l == '    requireSuperAdmin,'))

print('4. THE FINDING FILE db.retry.test.ts — blob at develop and at each head (the seat says byte-identical)')
b0 = rp(DEV + ':' + DBRETRY)
chk('db.retry.test.ts at develop', b0, '5933da41ed3dcf37f415000c4da4a717ea8d7eba')
for n, h, *_ in PRS:
    chk('db.retry.test.ts at #%d head' % n, rp(h + ':' + DBRETRY), b0)
for n, h, path, run, name, hb in PRS:
    p = open(RUNS + run + '/out.md.checker/patch.diff').read()
    print('  "db.retry" occurrences in %s patch.diff: %d (want 0)' % (name, p.count('db.retry')))
    if p.count('db.retry'): bad.append(('patch names db.retry', name))

print('ALL OK' if not bad else ('DISAGREED: %r' % (bad,)))
sys.exit(0 if not bad else 1)
