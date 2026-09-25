#!/usr/bin/env python3
"""predict_gate21T2b.py <scratchpad> — the drafter's MEASUREMENTS for the round-21 SECOND tier-2 batch gate over #1225 KS-1291, #1227 KS-1252+KS-1253,
#1229 KS-865+KS-808(3), #1231 KS-1281, #1232 KS-1128 (FROZEN at five). Every git WRITE verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree/apply/write-tree in a temp index) lives in a scratch bare clone FROM ORIGIN under <scratchpad> (blob:none, over the checkout's own ssh road,
read with `config --get` and never printed); the Secuura checkout is read with `ls-remote` / `config --get` only. Derived from gate21T2's
predict_gate21T2.py, re-keyed; the merge checks are BASE-INVARIANT (Wednesday 04:35Z / 05:02Z): develop has moved 4 commits past every PR's base.
Measures: (a) develop + the five pull heads + branches, ls-remote then the fetch, must agree; (b) ancestry: #1225/#1231/#1232 ONE commit on BASE,
#1227 and #1229 TWO commits, linear; (c) per-PR numstat == the pinned file set, blobs + modes; product/script/test classification; (d) pairwise
disjointness across the five AND against develop's move BASE..develop; (e) per-PR merged tree over the CURRENT develop + the BASE-INVARIANT check
(diff develop..merged == the PR's own paths, each blob == the head blob), END_TREE in three orders + an `apply --cached` second instrument;
(f)-(k) per-PR reads (the diffs, the sites, the text-pinned readers, the substrate sources); (j) the hyphenated-key scan on the branch names.
Writes pins_gate21T2b.txt (key=value) + devlog_gate21T2b.txt beside itself. rc 0 only if every HARD assertion holds."""
import os, subprocess, sys, datetime, re, tempfile, random
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
D = 'Blockchain/Dev/'
PRS = [
    dict(n='1225', key='KS-1291', keys={'KS-1291'}, head='120420a2e7b1a0d10dd41ee4320f7e88bc1529c6', commits=1,
         br='refs/heads/feature/ks-1291-dead-post-save-issuername-guard-l1-j-1',
         files={D + 'services/originate/src/routes/documents.ts': (8, 11)}),
    dict(n='1227', key='KS-1252', keys={'KS-1252', 'KS-1253'}, head='69a72726e8eee0711a56b782d04936bf647e9160', commits=2, mid='582ab9e5e7dfb554558cd13930c4185a922ad9cb',
         br='refs/heads/feature/ks-1252-spec-example-guard-e7-ulid-ish-prefix-l4-e7prefix-1',
         files={D + 'scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh': (175, 0), D + 'scripts/spec-examples/check/contract.mjs': (18, 2)}),
    dict(n='1229', key='KS-865', keys={'KS-865', 'KS-808'}, head='ed85bd81d0acb137c89e1257d05ef9c72855086b', commits=2, mid='099f9fb6b2e96b7d8d36babe184f4a3b81ac2dde',
         br='refs/heads/feature/ks-865-check-no-latest-tags-silently-skips-l4-examinedcount-1',
         files={D + 'scripts/__tests__/check_no_latest_tags.test.sh': (161, 0), D + 'scripts/check-no-latest-tags.sh': (19, 2), D + 'scripts/run-migrations.sh': (10, 3)}),
    dict(n='1231', key='KS-1281', keys={'KS-1281'}, head='bd1d2daec2bf1b934437eae19c6239fe257305a6', commits=1,
         br='refs/heads/feature/ks-1281-vc-issuer-boot-warns-could-not-ensure-vc_credentials_store-r21-existencecheck-1',
         files={D + 'services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts': (46, 0), D + 'services/vc-issuer/src/repositories/credentialRepo.ts': (3, 7)}),
    dict(n='1232', key='KS-1128', keys={'KS-1128'}, head='ec0d7efcf682112639505cf45baec71b899b665f', commits=1,
         br='refs/heads/feature/ks-1128-the-platform-tenant-seeds-catch-logs-platform-tenant-seed-r21-seedwarn-1',
         files={D + 'services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts': (80, 0), D + 'services/api-gateway/src/startup-migrations.ts': (3, 1)}),
]
P = {p['n']: p for p in PRS}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_gate21T2b start', now())
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'): ENV.pop(k, None)
print('checkout remote.origin.url:', url, '| core.sshCommand present:', bool(ssh), '(value not printed)')
CL = tempfile.mkdtemp(prefix='g21T2bclone_', dir=SP); os.rmdir(CL)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a, env=None, inp=None): return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % p['n'] for p in PRS] + [p['br'] for p in PRS]
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin'] + refs)
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
spec = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/g21b/%s' % (p['n'], p['n']) for p in PRS] + ['+%s:refs/g21bbr/%s' % (p['br'], p['n']) for p in PRS]
rc, o, e = g('fetch', '--quiet', 'origin', *spec); print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]
print('--- (a) heads and develop (ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote' % DEV)
for p in PRS:
    h = g('rev-parse', 'refs/g21b/' + p['n'])[1]; b = g('rev-parse', 'refs/g21bbr/' + p['n'])[1]
    hard(h == b == LS.get('refs/pull/%s/head' % p['n']) == LS.get(p['br']) == p['head'], '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (p['n'], h))
print('--- (b) ancestry')
for p in PRS:
    revs = g('rev-list', '--parents', BASE + '..' + p['head'])[1].splitlines()
    hard(len(revs) == p['commits'], '#%s: %d commit(s) over BASE (measured %d)' % (p['n'], p['commits'], len(revs)))
    if p['commits'] == 1: hard(revs[0].split()[1:] == [BASE], '#%s: parent == BASE' % p['n'])
    else: hard(revs[0].split() == [p['head'], p['mid']] and revs[1].split() == [p['mid'], BASE], '#%s: head %s -> %s -> BASE (linear, no merge commit)' % (p['n'], p['head'][:9], p['mid'][:9]))
    hard(g('merge-base', DEV, p['head'])[1] == BASE, '#%s: merge-base(develop, head) == BASE' % p['n'])
    for c in reversed(revs): print('    ' + g('log', '-1', '--format=%h %s', c.split()[0])[1])
print('--- (b2) develop\'s move since BASE')
hard(g('merge-base', '--is-ancestor', BASE, DEV)[0] == 0, 'develop %s descends from BASE' % DEV[:12])
BEHIND = int(g('rev-list', '--count', BASE + '..' + DEV)[1]); MV = g('diff', '--name-only', BASE, DEV)[1].splitlines()
LOG = g('log', '--format=%H %s', BASE + '..' + DEV)[1]
print('  develop is %d commits past BASE; %d paths changed:' % (BEHIND, len(MV))); print('    ' + LOG.replace('\n', '\n    '))
for f in MV: print('      moved: ' + f)
with open(os.path.join(G, 'devlog_gate21T2b.txt'), 'w') as f: f.write(LOG + '\n')
ALL = sorted(set(f for p in PRS for f in p['files']))
hard(not (set(ALL) & set(MV)), "develop's move BASE..develop touches NONE of the batch's %d paths: %s" % (len(ALL), sorted(set(ALL) & set(MV))))
DEVTREE = g('rev-parse', DEV + '^{tree}')[1]; BASETREE = g('rev-parse', BASE + '^{tree}')[1]
print('  develop tree', DEVTREE, '| BASE tree', BASETREE)
print('--- (c) per-PR numstat, blobs, modes, class')
BL = {}; BB = {}
def cls(f):
    if '/__tests__/' in f: return 'TEST'
    if f.startswith(D + 'scripts/'): return 'SCRIPT'
    return 'PRODUCT'
for p in PRS:
    ns = g('diff', '--numstat', BASE, p['head'])[1]; rows = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in ns.splitlines()}
    print('  #%s %s: %d files +%d/-%d' % (p['n'], p['key'], len(rows), sum(a for a, _ in rows.values()), sum(d for _, d in rows.values())))
    hard(rows == p['files'], '#%s numstat == the pinned file set and counts' % p['n'])
    for f in sorted(p['files']):
        ls = g('ls-tree', p['head'], '--', f)[1].split(); BL[f] = (ls[2], ls[0])
        lb = g('ls-tree', BASE, '--', f)[1].split(); BB[f] = lb[2] if lb else 'ABSENT'
        print('    %s %s %s %-7s (BASE %s %s) %s' % (ls[0], ls[2], p['n'], cls(f), lb[0] if lb else '', BB[f][:12], f))
        if lb: hard(ls[0] == lb[0], '%s mode %s at head == BASE mode' % (f[len(D):], ls[0]))
# the two NEW shell suites: mode vs their siblings at BASE (run-shell-suites.sh runs them; the sibling mode is the convention)
sib = [l.split() for l in g('ls-tree', BASE, D + 'scripts/__tests__/')[1].splitlines()]
sibsh = [(x[0], x[3]) for x in sib if x[3].endswith('.test.sh')]
modes = {}
for m, _ in sibsh: modes[m] = modes.get(m, 0) + 1
print('  scripts/__tests__/*.test.sh at BASE: %d files, modes %s' % (len(sibsh), modes))
for f in (D + 'scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh', D + 'scripts/__tests__/check_no_latest_tags.test.sh'):
    print('  NEW %s mode %s (BASE majority %s)' % (f.split('/')[-1], BL[f][1], max(modes, key=modes.get)))
print('  PRODUCT paths:', [f for f in ALL if cls(f) == 'PRODUCT']); print('  SCRIPT paths:', [f for f in ALL if cls(f) == 'SCRIPT'])
hard([f for f in ALL if cls(f) == 'PRODUCT'] == [D + 'services/api-gateway/src/startup-migrations.ts', D + 'services/originate/src/routes/documents.ts', D + 'services/vc-issuer/src/repositories/credentialRepo.ts'],
     'the PRODUCT paths are exactly #1232 startup-migrations.ts, #1225 documents.ts, #1231 credentialRepo.ts')
print('--- (d) disjointness (pairwise across the five; vs develop\'s move above)')
for i, a in enumerate(PRS):
    for b in PRS[i + 1:]:
        x = set(a['files']) & set(b['files']); hard(not x, '#%s ∩ #%s = EMPTY (%s)' % (a['n'], b['n'], sorted(x)))
print('  distinct paths:', len(ALL))
print('--- (e) merged trees over the CURRENT develop, the BASE-INVARIANT check, END_TREE')
MT = {}
for p in PRS:
    r = g('merge-tree', '--write-tree', DEV, p['head']); t = r[1].splitlines()[0] if r[1] else ''
    MT[p['n']] = t; hard(r[0] == 0, '#%s merges clean over develop %s -> merged tree %s' % (p['n'], DEV[:12], t))
    dn = sorted(g('diff', '--name-only', DEV, t)[1].splitlines())
    hard(dn == sorted(p['files']), '#%s BASE-INVARIANT: diff develop..merged == its own %d path(s) %s' % (p['n'], len(p['files']), dn))
    for f in p['files']: hard(g('rev-parse', t + ':' + f)[1] == BL[f][0], '#%s merged blob %s == head blob %s' % (p['n'], f.split('/')[-1], BL[f][0][:12]))
def chain(order):
    E = dict(ENV); E['GIT_AUTHOR_NAME'] = E['GIT_COMMITTER_NAME'] = 'x'; E['GIT_AUTHOR_EMAIL'] = E['GIT_COMMITTER_EMAIL'] = 'x@x'
    cur = DEV
    for n in order:
        r = g('merge-tree', '--write-tree', cur, P[n]['head'])
        if r[0] != 0: return 'CONFLICT@' + n
        t = r[1].splitlines()[0]; cur = g('commit-tree', t, '-p', cur, '-p', P[n]['head'], '-m', 'g21T2b chain (scratch only)', env=E)[1]
    return g('rev-parse', cur + '^{tree}')[1]
orders = [[p['n'] for p in PRS]]; orders.append(list(reversed(orders[0]))); sh_ = list(orders[0]); random.Random(21).shuffle(sh_); orders.append(sh_)
ENDS = [chain(o) for o in orders]
for o, t in zip(orders, ENDS): print('  END_TREE order %s -> %s' % (','.join(o), t))
hard(len(set(ENDS)) == 1 and not ENDS[0].startswith('CONFLICT'), 'END_TREE identical in three orders')
END = ENDS[0]
idx = os.path.join(CL, 'g21T2b.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '-C', CL, 'read-tree', DEVTREE], env=E2)
for p in PRS:
    # RAW stdout (never .strip()): stripping a trailing blank context line corrupts the patch (gate21T2 predict_1's bug)
    patch = subprocess.run(['git', '-C', CL, 'diff', '--binary', '--full-index', BASE, p['head']], capture_output=True, text=True, env=ENV).stdout
    ap = sh(['git', '-C', CL, 'apply', '--cached', '-'], env=E2, inp=patch); print('  apply --cached #%s rc %d %s' % (p['n'], ap[0], ap[2][:120]))
    hard(ap[0] == 0, '#%s applies to develop\'s tree by patch' % p['n'])
AT = sh(['git', '-C', CL, 'write-tree'], env=E2)[1]
hard(AT == END, 'second instrument (apply --cached of each BASE..head onto develop tree) == END_TREE: %s' % AT)
st = g('diff', '--shortstat', DEV, END)[1]; print('  develop -> END_TREE:', st)
hard(sorted(g('diff', '--name-only', DEV, END)[1].splitlines()) == ALL, 'END_TREE BASE-INVARIANT: diff develop..END == the %d batch paths exactly' % len(ALL))
for p in PRS:
    for f in p['files']: hard(g('rev-parse', END + ':' + f)[1] == BL[f][0], 'END_TREE %s == #%s head blob' % (f.split('/')[-1], p['n']))
def blob(rev, f):
    r = subprocess.run(['git', '-C', CL, 'cat-file', 'blob', rev + ':' + f], capture_output=True, text=True, env=ENV); return r.stdout if r.returncode == 0 else None
def gg(rev, pat, *paths, flags=('-n',)):
    r = g('grep', *flags, '-E', pat, rev, '--', *paths); return [l.split(':', 1)[1] for l in r[1].splitlines()] if r[1] else []
def show_diff(n, f): print('    ' + g('diff', BASE, P[n]['head'], '--', f)[1].replace('\n', '\n    '))
print('--- (f) #1225 KS-1291: the removed post-save guard, the surviving early guard, #1174, the witness cell, the route')
DOC = D + 'services/originate/src/routes/documents.ts'
show_diff('1225', DOC)
b0 = blob(BASE, DOC).splitlines(); b1 = blob(P['1225']['head'], DOC).splitlines()
print('  BASE issuerName lines:', [(i + 1, l.strip()[:120]) for i, l in enumerate(b0) if 'issuerName' in l])
print('  head issuerName lines:', [(i + 1, l.strip()[:120]) for i, l in enumerate(b1) if 'issuerName' in l])
print('  BASE `saveDocument(` lines:', [i + 1 for i, l in enumerate(b0) if 'saveDocument(' in l], '| head:', [i + 1 for i, l in enumerate(b1) if 'saveDocument(' in l])
print('  BASE `@` guard lines (includes(\'@\')):', [(i + 1, l.strip()[:100]) for i, l in enumerate(b0) if "includes('@')" in l or 'includes("@")' in l])
print('  head `@` guard lines:', [(i + 1, l.strip()[:100]) for i, l in enumerate(b1) if "includes('@')" in l or 'includes("@")' in l])
print('  BASE route registrations naming documents in this file:', [(i + 1, l.strip()[:100]) for i, l in enumerate(b0) if re.search(r"router\.(post|get|put|patch|delete)\(", l)][:12])
c1174 = g('log', '--format=%H %s', '--grep=#1174', BASE)[1]; print('  commits at BASE whose message names #1174:', c1174[:400])
if c1174:
    body = g('log', '-1', '--format=%B', c1174.split()[0])[1]; print('  its message lines naming unreachable/later cleanup:', [l.strip()[:160] for l in body.splitlines() if 'unreachable' in l or 'cleanup' in l])
w = g('grep', '-l', '-E', 'E-01', BASE, '--', D + 'services/originate/src/__tests__/')[1]; print('  originate test files naming E-01 at BASE:', [x.split(':', 1)[1][len(D):] for x in w.splitlines()])
tr = g('grep', '-l', '-E', r'routes/documents(\.ts)?', BASE, '--', D + 'services/', D + 'packages/', D + 'scripts/')[1]
print('  files at BASE that NAME routes/documents (text readers / importers):', len(tr.splitlines()) if tr else 0)
for x in tr.splitlines()[:40]: print('    ' + x.split(':', 1)[1][len(D):])
rd = [x for x in (tr.splitlines() if tr else []) if 'readFileSync' in (blob(BASE, x.split(':', 1)[1]) or '')]
print('  of those, files that also call readFileSync (candidate TEXT-pinned readers):', [x.split(':', 1)[1][len(D):] for x in rd])
SPEC = D + 'docs/openapi/secuura-api.yaml'
spec0 = blob(BASE, SPEC) or ''
print('  served-spec reach: `/api/documents:` path keys in secuura-api.yaml at BASE: %d | `/api/documents` any: %d | control `/api/anchors`: %d' % (spec0.count('/api/documents:'), spec0.count('/api/documents'), spec0.count('/api/anchors')))
print('--- (g) #1227 KS-1252+KS-1253: contract.mjs, the ks256 rows, the importers, leg 14\'s discovery')
CON = D + 'scripts/spec-examples/check/contract.mjs'
show_diff('1227', CON)
print('  mid-commit 582ab9e5e diff (KS-1252 only), numstat:', g('diff', '--numstat', BASE, P['1227']['mid'])[1])
c1 = blob(P['1227']['head'], CON)
print('  head lines naming BENIGN_SHAPES / PREFIXED_UUID_RE / ULID:', [(i + 1, l.strip()[:150]) for i, l in enumerate(c1.splitlines()) if re.search(r'BENIGN_SHAPES|PREFIXED_UUID_RE|ULID|DENY|EXACT', l)][:20])
K256 = D + 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts'
k = blob(BASE, K256) or ''
print('  ks256 at BASE: present %s | lines naming len12: %s | lines naming \'credit\': %s' % (bool(k), [(i + 1, l.strip()[:120]) for i, l in enumerate(k.splitlines()) if 'len12' in l], [(i + 1, l.strip()[:120]) for i, l in enumerate(k.splitlines()) if "'credit'" in l]))
hard(bool(k) and any('len12' in l for l in k.splitlines()) and any("'credit'" in l for l in k.splitlines()), 'ks256 at BASE carries the len12 and credit rows (#1227\'s collateral pair)')
imp = g('grep', '-l', 'spec-examples/check/contract', BASE, '--', D)[1]; print('  files at BASE importing/naming spec-examples/check/contract:', [x.split(':', 1)[1][len(D):] for x in imp.splitlines()] if imp else [])
RSS = D + 'scripts/run-shell-suites.sh'
rss = blob(BASE, RSS) or ''
print('  run-shell-suites.sh discovery lines:', [(i + 1, l.strip()[:140]) for i, l in enumerate(rss.splitlines()) if re.search(r'\*\.test\.sh|__tests__|find |for .* in', l)][:10])
print('  shell suites (scripts/__tests__/*.test.sh) at BASE %d -> #1227 head %d -> #1229 head %d -> END_TREE %d' % tuple(
    len([l for l in g('ls-tree', '--name-only', r, D + 'scripts/__tests__/')[1].splitlines() if l.endswith('.test.sh')]) for r in (BASE, P['1227']['head'], P['1229']['head'], END)))
print('--- (h) #1229 KS-865 + KS-808(3): the two scripts, deploy-staging.yml, BACKLOG.md, exit 3')
NLT = D + 'scripts/check-no-latest-tags.sh'; RM = D + 'scripts/run-migrations.sh'
show_diff('1229', NLT); show_diff('1229', RM)
print('  mid-commit 099f9fb6b numstat:', g('diff', '--numstat', BASE, P['1229']['mid'])[1])
ds = [l for l in g('ls-tree', '-r', '--name-only', BASE)[1].splitlines() if l.endswith('deploy-staging.yml')]
ci = [l for l in g('ls-tree', '-r', '--name-only', BASE)[1].splitlines() if l.endswith('.github/workflows/ci.yml')]
print('  `deploy-staging.yml` anywhere in BASE tree: %d %s | CONTROL `.github/workflows/ci.yml`: %d %s' % (len(ds), ds, len(ci), ci))
hard(len(ds) == 0 and len(ci) >= 1, '#1229: deploy-staging.yml absent at BASE, and the same instrument finds ci.yml')
def noncomment_nonecho(a, b, f):
    out = []
    for l in g('diff', '-U0', a, b, '--', f)[1].splitlines():
        if l[:1] in '+-' and not l.startswith(('+++', '---')):
            s = l[1:].strip()
            if s and not s.startswith('#') and not re.match(r'^(echo|printf)\b', s) and not re.match(r'^"[^"]*"\s*(>&2)?$', s): out.append(l)
    return out
nr = noncomment_nonecho(BASE, P['1229']['head'], RM); nc = noncomment_nonecho(BASE, P['1229']['head'], NLT)
print('  run-migrations.sh changed lines that are neither comment nor echo/printf: %d %s | CONTROL check-no-latest-tags.sh: %d' % (len(nr), nr, len(nc)))
hard(len(nc) > 0, '#1229 instrument CONTROL: sees code lines in check-no-latest-tags.sh')
r0 = blob(BASE, RM); r1 = blob(P['1229']['head'], RM)
print('  run-migrations.sh `exit 3` BASE %d head %d | `BACKLOG` BASE %d head %d | echo lines naming BACKLOG BASE %d head %d | KS-1031 head %d | KS-808 head %d' % (
    r0.count('exit 3'), r1.count('exit 3'), r0.count('BACKLOG'), r1.count('BACKLOG'),
    len([l for l in r0.splitlines() if 'BACKLOG' in l and 'echo' in l]), len([l for l in r1.splitlines() if 'BACKLOG' in l and 'echo' in l]), r1.count('KS-1031'), r1.count('KS-808')))
hard(g('diff', '--quiet', BASE, P['1229']['head'], '--', D + 'BACKLOG.md', 'BACKLOG.md')[0] == 0, '#1229: BACKLOG.md untouched (both roots)')
n1 = blob(P['1229']['head'], NLT)
print('  check-no-latest-tags.sh head CHECK_FILES region:'); 
m = re.search(r'CHECK_FILES=\((.*?)\)', n1, re.S); print('    ' + (m.group(0).replace('\n', '\n    ') if m else 'NOT FOUND'))
m0 = re.search(r'CHECK_FILES=\((.*?)\)', blob(BASE, NLT), re.S); print('  BASE CHECK_FILES:'); print('    ' + (m0.group(0).replace('\n', '\n    ') if m0 else 'NOT FOUND'))
if m:
    for e in re.findall(r'"?([^\s"()]+)"?', m.group(1)):
        if e.startswith('#'): continue
        print('    entry %-60s at BASE under Blockchain/Dev: %s' % (e, bool(g('ls-tree', BASE, '--', D + e)[1])))
print('--- (i) #1231 KS-1281: credentialRepo, the substrate sources for vc_credentials_store, provisionAppRole, the memory fallback')
CR = D + 'services/vc-issuer/src/repositories/credentialRepo.ts'
show_diff('1231', CR)
cr1 = blob(P['1231']['head'], CR)
print('  head lines naming memory / fallback / SELECT / CREATE:', [(i + 1, l.strip()[:130]) for i, l in enumerate(cr1.splitlines()) if re.search(r'(?i)memory|fallback|SELECT 1|CREATE', l)][:16])
vs = g('grep', '-n', 'vc_credentials_store', BASE, '--', D)[1]
print('  `vc_credentials_store` at BASE (every source that names it):')
for x in vs.splitlines(): print('    ' + x.split(':', 1)[1][len(D):][:200])
vsr = g('grep', '-n', 'vc_credentials_store', BASE, '--', '.', ':!' + D)[1]
print('  ... outside Blockchain/Dev: %d' % (len(vsr.splitlines()) if vsr else 0))
pa = g('grep', '-n', '-E', 'provisionAppRole|GRANT SELECT|ALTER DEFAULT PRIVILEGES', BASE, '--', D)[1]
print('  provisionAppRole / GRANT SELECT / ALTER DEFAULT PRIVILEGES at BASE:')
for x in pa.splitlines()[:30]: print('    ' + x.split(':', 1)[1][len(D):][:200])
crt = g('grep', '-l', 'credentialRepo', BASE, '--', D + 'services/vc-issuer/')[1]; print('  vc-issuer files naming credentialRepo at BASE:', [x.split(':', 1)[1][len(D):] for x in crt.splitlines()] if crt else [])
print('--- (k) #1232 KS-1128: the seed catch, the :1142 inner catch, the three text-pinned readers, the siblings')
SM = D + 'services/api-gateway/src/startup-migrations.ts'
show_diff('1232', SM)
s0 = blob(BASE, SM).splitlines(); s1 = blob(P['1232']['head'], SM).splitlines()
print('  BASE catch lines 1130-1150:'); [print('    %d: %s' % (i + 1, s0[i][:150])) for i in range(1129, min(1150, len(s0)))]
print('  head catch lines 1130-1152:'); [print('    %d: %s' % (i + 1, s1[i][:150])) for i in range(1129, min(1152, len(s1)))]
print('  lines naming `Platform tenant seed` BASE:', [(i + 1, l.strip()[:150]) for i, l in enumerate(s0) if 'Platform tenant seed' in l], '| head:', [(i + 1, l.strip()[:150]) for i, l in enumerate(s1) if 'Platform tenant seed' in l])
print('  lines naming `Main tenant seed`/main-DB arm at head:', [(i + 1, l.strip()[:150]) for i, l in enumerate(s1) if re.search(r'(?i)tenant seed', l)][:8])
READERS = [D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts', D + 'services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts', D + 'scripts/__tests__/ks949_main_seed_idempotence.test.sh']
for rf in READERS:
    t = blob(BASE, rf) or ''
    print('  reader %s present %s; its lines naming startup-migrations: %s' % (rf[len(D):], bool(t), [(i + 1, l.strip()[:140]) for i, l in enumerate(t.splitlines()) if 'startup-migrations' in l][:5]))
allr = g('grep', '-l', 'startup-migrations', BASE, '--', D)[1]; print('  every file at BASE naming startup-migrations:', [x.split(':', 1)[1][len(D):] for x in allr.splitlines()] if allr else [])
sib = [l for l in g('ls-tree', '--name-only', BASE, D + 'services/api-gateway/src/__tests__/')[1].splitlines() if re.search(r'ks1062|ks1125|ks1272', l)]; print('  sibling suites ks1062/ks1125/ks1272 at BASE:', sib)
t1128 = blob(P['1232']['head'], D + 'services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts')
print('  ks1128 test: it( %d, test( %d, `:5432` %d, `.invalid` %d, createRequire %d, WARN-ish lines %s' % (len(re.findall(r'\bit\(', t1128)), len(re.findall(r'\btest\(', t1128)), t1128.count(':5432'), t1128.count('.invalid'), t1128.count('createRequire'), [l.strip()[:120] for l in t1128.splitlines() if 'FAILED' in l][:4]))
print('--- (l) develop\'s four new commits vs the five PRs\' test/lane readers (does the move touch anything the PRs\' suites READ?)')
for f in MV:
    hits = [n for n in P if any(f.split('/')[-1] in (blob(P[n]['head'], x) or '') for x in P[n]['files'] if '/__tests__/' in x)]
    print('  moved %-90s named by a batch test file: %s' % (f[len(D):] if f.startswith(D) else f, hits))
print('--- (j) hyphenated-key scan on the branch names (own keys only)')
for p in PRS:
    ks = sorted(set(m.upper() for m in re.findall(r'(?i)\bks-\d+', p['br'])))
    print('  #%s %s -> %s' % (p['n'], p['br'], ks)); hard(set(ks) <= p['keys'] and p['key'] in ks, '#%s branch carries its own key(s) only' % p['n'])
print('--- summary')
PINS = dict(MEASURED_AT=now(), BASE=BASE, BASE_TREE=BASETREE, DEVELOP=DEV, DEVELOP_TREE=DEVTREE, BEHIND=str(BEHIND), MOVED_N=str(len(MV)), END_TREE=END, END_SHORTSTAT=st)
for p in PRS: PINS['HEAD_' + p['n']] = p['head']; PINS['MERGED_' + p['n']] = MT[p['n']]
for f in ALL: PINS['BLOB|' + f] = '%s %s' % BL[f]
for f in ALL: PINS['BASEBLOB|' + f] = BB[f]
PINS['FAIL'] = str(len(FAIL))
with open(os.path.join(G, 'pins_gate21T2b.txt'), 'w') as f:
    for k, v in PINS.items(): f.write('%s=%s\n' % (k, v))
print('pins written; FAIL', len(FAIL), FAIL); print('scratch clone (kept, never deleted):', CL)
sys.exit(1 if FAIL else 0)
