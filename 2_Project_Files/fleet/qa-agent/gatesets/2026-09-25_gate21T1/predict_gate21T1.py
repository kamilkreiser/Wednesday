#!/usr/bin/env python3
"""predict_gate21T1.py <scratchpad> — the drafter's MEASUREMENTS for the round-21 tier-1 batch gate over #1213 KS-530, #1214 KS-528, #1216 KS-975,
#1217 KS-976. Every git WRITE verb (clone, fetch, merge-tree --write-tree, read-tree/apply/write-tree in a temp index) lives in a scratch bare clone
FROM ORIGIN under <scratchpad> (blob:none, over the checkout's own ssh road, read with `config --get` and never printed); the Secuura checkout is read
with `ls-remote` / `config --get` only. Measures: (a) develop + the four pull heads + branches at origin, two reads (ls-remote, then the fetch) that must
agree; (b) each head's parent == BASE, develop vs BASE (a move is judged by content against the 13 paths); (c) per-PR numstat == the pinned file set,
blobs + modes; (d) pairwise path disjointness; 0 bytes under services/auth/ with a control that can see a byte (services/security/); (e) per-PR merged
tree over the develop just read and the END_TREE of the four in THREE orders + an `apply --cached` second instrument; (f) #1214's audit-baseline edit
== exactly ONE removed member GHSA-jjmj-jmhj-qwj2, every other member byte-identical, the two 2026-10-02 react-router rows present; #1213 leaves the
baseline blob == BASE; (g) a per-lock package census (added / removed / version-changed; resolved/integrity moves on an UNCHANGED version; libc/os/cpu
counts); (h) #1216: principalScope lines in the diff (must be 0 changed) + the diff; (i) #1217: 'Key required' counts at BASE / head + the diff;
(j) the hyphenated-key scan on the four branch names. Writes pins_gate21T1.txt (key=value) beside itself. rc 0 only if every HARD assertion holds."""
import os, subprocess, sys, datetime, re, tempfile, json, random
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
D = 'Blockchain/Dev/'
PRS = [  # seat order: Seat B 25th READY 1, READY 2; Seat L2 READY 1, READY 2
    dict(n='1213', key='KS-530', head='f2751859c01565df066a3cdbe008e7360de4205a',
         br='refs/heads/feature/ks-530-hononode-server-v1-v2-major-bump-ghsa-frvp-originate-mcp-r21-patchline-1',
         files={D + 'services/mcp-server/package-lock.json': (3, 3), D + 'services/originate/package-lock.json': (3, 3), D + 'services/originate/package.json': (2, 1)}),
    dict(n='1214', key='KS-528', head='6fce4d0b188655a520e97447d3bfb1749d22a435',
         br='refs/heads/feature/ks-528-frontends-react-router-v6-v7-migration-3-moderate-client-r21-dompatch-1',
         files={D + 'frontend/admin/package-lock.json': (12, 12), D + 'frontend/issuer/package-lock.json': (12, 12), D + 'frontend/verifier/package-lock.json': (12, 12),
                D + 'package-lock.json': (12, 6), D + 'scripts/audit/audit-baseline.json': (0, 7)}),
    dict(n='1216', key='KS-975', head='c44b15dddaddac3dec1d4deff224efd01b7565f2',
         br='refs/heads/feature/ks-975-explicitscope-null-is-malformed-l2-scopenull-1',
         files={D + 'services/security/src/__tests__/ks975b-explicitscope-null-body-field-is-refused.test.ts': (65, 0), D + 'services/security/src/rateLimitScope.ts': (41, 2)}),
    dict(n='1217', key='KS-976', head='e83f344474028215ae827b2f74fd3a06566d4c23',
         br='refs/heads/feature/ks-976-reset-400-names-the-failing-field-l2-msg400-1',
         files={D + 'services/security/src/__tests__/ks976a-reset-400-names-the-failing-field.test.ts': (147, 0), D + 'services/security/src/index.ts': (6, 1),
                D + 'services/security/src/requestRefusal.ts': (55, 0)}),
]
BASELINE = D + 'scripts/audit/audit-baseline.json'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_gate21T1 start', now())
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
print('checkout remote.origin.url:', url, '| core.sshCommand present:', bool(ssh), '(value not printed)')
CL = tempfile.mkdtemp(prefix='g21clone_', dir=SP); os.rmdir(CL)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a, env=None, inp=None): return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % p['n'] for p in PRS] + [p['br'] for p in PRS]
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin'] + refs)
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
spec = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/g21/%s' % (p['n'], p['n']) for p in PRS] + ['+%s:refs/g21br/%s' % (p['br'], p['n']) for p in PRS]
rc, o, e = g('fetch', '--quiet', 'origin', *spec); print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]
print('--- (a) heads and develop (ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote' % DEV)
for p in PRS:
    h = g('rev-parse', 'refs/g21/' + p['n'])[1]; b = g('rev-parse', 'refs/g21br/' + p['n'])[1]
    hard(h == b == LS.get('refs/pull/%s/head' % p['n']) == LS.get(p['br']) == p['head'], '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (p['n'], h))
print('--- (b) ancestry and the develop reading')
for p in PRS:
    par = g('rev-list', '--parents', '-n', '1', p['head'])[1].split()[1:]
    hard(par == [BASE], '#%s: ONE commit, parent == BASE (%s)' % (p['n'], ','.join(x[:12] for x in par)))
ALL = sorted(set(f for p in PRS for f in p['files']))
if DEV == BASE:
    BEHIND = 0; print('  develop == BASE %s (0 commits ahead): every merge is a fast-forward-shaped squash' % BASE)
else:
    anc = g('merge-base', '--is-ancestor', BASE, DEV)[0] == 0; hard(anc, 'develop moved to a DESCENDANT of BASE')
    BEHIND = int(g('rev-list', '--count', BASE + '..' + DEV)[1]); mv = g('diff', '--name-only', BASE, DEV)[1].splitlines()
    print('  develop moved %d commits; %d paths changed' % (BEHIND, len(mv))); print('    ' + g('log', '--format=%H %s', BASE + '..' + DEV)[1].replace('\n', '\n    '))
    hard(not (set(ALL) & set(mv)), 'the develop move touches NONE of the batch paths (else re-predict BY HAND): %s' % sorted(set(ALL) & set(mv)))
with open(os.path.join(G, 'devlog_gate21T1.txt'), 'w') as f: f.write(g('log', '--format=%H %s', BASE + '..' + DEV)[1] + '\n')
DEVTREE = g('rev-parse', DEV + '^{tree}')[1]; BASETREE = g('rev-parse', BASE + '^{tree}')[1]
print('  develop tree', DEVTREE, '| BASE tree', BASETREE)
print('--- (c) per-PR numstat, blobs, modes')
BL = {}; BB = {}
for p in PRS:
    ns = g('diff', '--numstat', BASE, p['head'])[1]; rows = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in ns.splitlines()}
    print('  #%s %s: %d files +%d/-%d' % (p['n'], p['key'], len(rows), sum(a for a, _ in rows.values()), sum(d for _, d in rows.values())))
    hard(rows == p['files'], '#%s numstat == the pinned file set and counts' % p['n'])
    for f in sorted(p['files']):
        ls = g('ls-tree', p['head'], '--', f)[1].split(); BL[f] = (ls[2], ls[0])
        lb = g('ls-tree', BASE, '--', f)[1].split(); BB[f] = lb[2] if lb else 'ABSENT'
        print('    %s %s %s (BASE %s) %s' % (ls[0], ls[2], p['n'], BB[f][:12], f))
        hard(ls[0] == '100644', f + ' mode 100644 at head')
print('--- (d) disjointness, services/auth/')
for i, a in enumerate(PRS):
    for b in PRS[i + 1:]:
        x = set(a['files']) & set(b['files']); hard(not x, '#%s ∩ #%s = EMPTY (%s)' % (a['n'], b['n'], sorted(x)))
for p in PRS:
    au = g('diff', '--numstat', BASE, p['head'], '--', D + 'services/auth/')[1]; ct = g('diff', '--numstat', BASE, p['head'], '--', D + 'services/security/')[1]
    print('  #%s services/auth/ rows %d | control services/security/ rows %d' % (p['n'], len(au.splitlines()) if au else 0, len(ct.splitlines()) if ct else 0))
    hard(au == '', '#%s: 0 bytes under services/auth/' % p['n'])
hard(any(g('diff', '--numstat', BASE, p['head'], '--', D + 'services/security/')[1] for p in PRS), 'CONTROL: the same instrument SEES rows under services/security/ (#1216/#1217)')
print('--- (e) merged trees over the develop just read + END_TREE in three orders + a second instrument')
MT = {}
for p in PRS:
    r = g('merge-tree', '--write-tree', DEV, p['head']); t = r[1].splitlines()[0] if r[1] else ''
    ht = g('rev-parse', p['head'] + '^{tree}')[1]; MT[p['n']] = t
    print('  #%s merge-tree rc %d -> %s | head tree %s | equal %s' % (p['n'], r[0], t, ht, t == ht)); hard(r[0] == 0, '#%s merges clean over develop' % p['n'])
    if DEV == BASE: hard(t == ht, '#%s merged tree == head tree (develop == BASE)' % p['n'])
def chain(order):
    E = dict(ENV); E['GIT_AUTHOR_NAME'] = E['GIT_COMMITTER_NAME'] = 'x'; E['GIT_AUTHOR_EMAIL'] = E['GIT_COMMITTER_EMAIL'] = 'x@x'
    cur = DEV
    for n in order:
        h = [p['head'] for p in PRS if p['n'] == n][0]
        r = g('merge-tree', '--write-tree', cur, h)
        if r[0] != 0: return 'CONFLICT@' + n
        t = r[1].splitlines()[0]; cur = g('commit-tree', t, '-p', cur, '-p', h, '-m', 'g21 chain (scratch only)', env=E)[1]
    return g('rev-parse', cur + '^{tree}')[1]
orders = [[p['n'] for p in PRS]]; orders.append(list(reversed(orders[0]))); sh_ = list(orders[0]); random.Random(21).shuffle(sh_); orders.append(sh_)
ENDS = [chain(o) for o in orders]
for o, t in zip(orders, ENDS): print('  END_TREE order %s -> %s' % (','.join(o), t))
hard(len(set(ENDS)) == 1 and not ENDS[0].startswith('CONFLICT'), 'END_TREE identical in three orders')
END = ENDS[0]
idx = os.path.join(CL, 'g21.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '-C', CL, 'read-tree', DEVTREE], env=E2)
for p in PRS:
    patch = g('diff', '--binary', '--full-index', BASE, p['head'])[1] + '\n'
    ap = sh(['git', '-C', CL, 'apply', '--cached', '-'], env=E2, inp=patch); print('  apply --cached #%s rc %d %s' % (p['n'], ap[0], ap[2][:120]))
AT = sh(['git', '-C', CL, 'write-tree'], env=E2)[1]
hard(AT == END, 'second instrument (apply --cached of each BASE..head onto develop tree) == END_TREE: %s' % AT)
st = g('diff', '--shortstat', DEV, END)[1]; print('  develop -> END_TREE:', st)
for p in PRS:
    for f in p['files']: hard(g('rev-parse', END + ':' + f)[1] == BL[f][0], 'END_TREE %s == #%s head blob' % (f.split('/')[-1] if 'package' not in f else f[len(D):], p['n']))
print('--- (f) the audit baseline: #1214 removes EXACTLY one member; #1213 leaves it at BASE')
bj = json.loads(g('cat-file', 'blob', BASE + ':' + BASELINE)[1]); hj = json.loads(g('cat-file', 'blob', '6fce4d0b188655a520e97447d3bfb1749d22a435:' + BASELINE)[1])
ba, ha = bj['accepted'], hj['accepted']
removed = sorted(set(ba) - set(ha)); added = sorted(set(ha) - set(ba)); changed = sorted(k for k in set(ba) & set(ha) if ba[k] != ha[k])
print('  members BASE %d -> #1214 %d | removed %s | added %s | changed %s | $comment equal %s' % (len(ba), len(ha), removed, added, changed, bj.get('$comment') == hj.get('$comment')))
hard(removed == ['GHSA-jjmj-jmhj-qwj2'] and not added and not changed and bj.get('$comment') == hj.get('$comment'), '#1214 baseline edit == exactly the ONE member GHSA-jjmj-jmhj-qwj2 removed; every other member byte-equal as parsed')
print('  the removed member at BASE:', json.dumps(ba.get('GHSA-jjmj-jmhj-qwj2')))
for k in ('GHSA-wrjc-x8rr-h8h6', 'GHSA-337j-9hxr-rhxg'): hard(k in ha and ha[k].get('expires') == '2026-10-02', '%s still present, expires 2026-10-02' % k)
lap = sorted(k for k, v in ha.items() if str(v.get('expires', '')) <= '2026-09-30'); lapb = sorted(k for k, v in ba.items() if str(v.get('expires', '')) <= '2026-09-30')
print('  members with expires <= 2026-09-30: BASE %s -> #1214 %s' % (lapb, lap))
td = g('diff', '--numstat', BASE, '6fce4d0b188655a520e97447d3bfb1749d22a435', '--', BASELINE)[1]; print('  text numstat:', td); hard(td == '0\t7\t' + BASELINE, 'text diff 0/7 on the baseline')
hard(g('rev-parse', 'f2751859c01565df066a3cdbe008e7360de4205a:' + BASELINE)[1] == g('rev-parse', BASE + ':' + BASELINE)[1], '#1213: baseline blob == BASE (no baseline edit — the frvp re-date is NOT at this head)')
print('--- (g) lock census (packages map at BASE vs head)')
def lockmap(rev, f):
    r = g('cat-file', 'blob', rev + ':' + f); return json.loads(r[1])['packages'] if r[0] == 0 else {}
CENSUS = []
for p in PRS[:2]:
    for f in sorted(p['files']):
        if not f.endswith('package-lock.json'): continue
        a, b = lockmap(BASE, f), lockmap(p['head'], f)
        add = sorted(set(b) - set(a)); rem = sorted(set(a) - set(b))
        ver = sorted(k for k in set(a) & set(b) if a[k].get('version') != b[k].get('version'))
        other = sorted(k for k in set(a) & set(b) if a[k] != b[k] and k not in ver)
        ri = sorted(k for k in set(a) & set(b) if k not in ver and (a[k].get('resolved') != b[k].get('resolved') or a[k].get('integrity') != b[k].get('integrity')))
        def cnt(m, fld): return sum(1 for v in m.values() if fld in v)
        print('  #%s %s: entries %d -> %d | added %d removed %d version-changed %d %s | other-field-changed %d %s | resolved/integrity moved on an UNCHANGED version %d | libc %d->%d os %d->%d cpu %d->%d' % (
            p['n'], f[len(D):], len(a), len(b), len(add), len(rem), len(ver), ['%s %s->%s' % (k, a[k].get('version'), b[k].get('version')) for k in ver], len(other), other, len(ri),
            cnt(a, 'libc'), cnt(b, 'libc'), cnt(a, 'os'), cnt(b, 'os'), cnt(a, 'cpu'), cnt(b, 'cpu')))
        CENSUS.append('%s:%s:+%d/-%d/~%d' % (p['n'], f[len(D):], len(add), len(rem), len(ver)))
        hard(not add and not rem and not other and not ri, '#%s %s: nothing added / removed / other-field-changed; no resolved/integrity move outside a version change' % (p['n'], f[len(D):]))
        names = set(re.sub(r'^.*node_modules/', '', k) for k in ver)
        want = {'@hono/node-server'} if p['n'] == '1213' else {'react-router-dom', 'react-router', '@remix-run/router'}
        hard(names <= want, '#%s %s: every version-changed package is a named one %s (got %s)' % (p['n'], f[len(D):], sorted(want), sorted(names)))
print('  #1213 originate/package.json diff:'); print('    ' + g('diff', BASE, 'f2751859c01565df066a3cdbe008e7360de4205a', '--', D + 'services/originate/package.json')[1].replace('\n', '\n    '))
print('--- (h) #1216: principalScope must be byte-identical')
d16 = g('diff', '-U0', BASE, 'c44b15dddaddac3dec1d4deff224efd01b7565f2', '--', D + 'services/security/src/rateLimitScope.ts')[1]
chg = [l for l in d16.splitlines() if l[:1] in '+-' and not l.startswith(('+++', '---'))]
ps = [l for l in chg if 'principalScope' in l]
print('  changed lines %d; changed lines naming principalScope %d:' % (len(chg), len(ps))); [print('    ' + l[:160]) for l in ps]
def fn_body(rev, name):
    t = g('cat-file', 'blob', rev + ':' + D + 'services/security/src/rateLimitScope.ts')[1]
    m = re.search(r'(export\s+)?function\s+' + name + r'\b[\s\S]*?\n}\n', t); return m.group(0) if m else None
pb, ph = fn_body(BASE, 'principalScope'), fn_body('c44b15dddaddac3dec1d4deff224efd01b7565f2', 'principalScope')
print('  principalScope function text found BASE %s head %s; byte-identical %s' % (pb is not None, ph is not None, pb == ph))
hard(pb is not None and pb == ph, '#1216: the principalScope function text is byte-identical BASE -> head (instrument: regex over the blob; control: it FOUND the function at both)')
eb, eh = fn_body(BASE, 'explicitScope'), fn_body('c44b15dddaddac3dec1d4deff224efd01b7565f2', 'explicitScope')
hard(eb is not None and eh is not None and eb != eh, 'CONTROL: the same instrument sees explicitScope CHANGE')
print('  #1216 rateLimitScope.ts diff:'); print('    ' + g('diff', BASE, 'c44b15dddaddac3dec1d4deff224efd01b7565f2', '--', D + 'services/security/src/rateLimitScope.ts')[1].replace('\n', '\n    '))
print('--- (i) #1217: the /reset 400 message')
for rev, lab in ((BASE, 'BASE'), ('e83f344474028215ae827b2f74fd3a06566d4c23', '#1217')):
    gr = g('grep', '-n', '-F', 'Key required', rev, '--', D + 'services/security/')[1]
    print('  %s `Key required` hits under services/security/: %d' % (lab, len(gr.splitlines()) if gr else 0)); [print('    ' + l[:200]) for l in gr.splitlines()]
    gd = g('grep', '-n', '-F', 'Key required', rev, '--', D + 'docs/')[1]; print('  %s `Key required` under docs/: %d' % (lab, len(gd.splitlines()) if gd else 0))
print('  #1217 index.ts diff:'); print('    ' + g('diff', BASE, 'e83f344474028215ae827b2f74fd3a06566d4c23', '--', D + 'services/security/src/index.ts')[1].replace('\n', '\n    '))
print('--- (j) branch names through the hyphenated-key scanner (own key only)')
for p in PRS:
    ks = sorted(set(re.findall(r'(?i)\bks-(\d+)\b', p['br']))); hard(ks == [p['key'].split('-')[1]], '#%s branch keys %s == own %s' % (p['n'], ks, p['key']))
with open(os.path.join(G, 'pins_gate21T1.txt'), 'w') as f:
    for k, v in [('MEASURED_AT', now()), ('BASE', BASE), ('BASE_TREE', BASETREE), ('DEVELOP', DEV), ('DEVELOP_TREE', DEVTREE), ('BEHIND', BEHIND), ('END_TREE', END),
                 ('END_SHORTSTAT', st)] + [('HEAD_' + p['n'], p['head']) for p in PRS] + [('MERGED_' + n, t) for n, t in MT.items()] + \
                [('BLOB|' + f, '%s %s' % BL[f]) for f in ALL] + [('BASEBLOB|' + f, BB[f]) for f in ALL] + [('CENSUS', ' '.join(CENSUS)), ('FAIL', len(FAIL))]:
        f.write('%s=%s\n' % (k, v))
print('scratch clone', CL); print('HARD FAILS:', len(FAIL), FAIL); print('done', now())
sys.exit(1 if FAIL else 0)
