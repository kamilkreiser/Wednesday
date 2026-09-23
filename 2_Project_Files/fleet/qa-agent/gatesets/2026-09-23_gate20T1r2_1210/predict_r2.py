#!/usr/bin/env python3
"""predict_r2.py <scratchpad> — the #1210 round-2 re-gate's MEASUREMENTS. Every git WRITE verb lives in a scratch clone FROM ORIGIN under <scratchpad>
(bare, blob:none, over the checkout's own ssh road); the Secuura checkout is read with `ls-remote` / `config --get` only.
Measures: develop + #1210's head + #1212's head at origin (ls-remote AND the fetch, must agree); the head's ancestry (r2 head -> r1 head -> BASE);
BASE..develop; the compare shape; the per-file numstat of BASE..head and of the round-2 delta; services/auth/ bytes (control: api-gateway rows);
the merged tree over the develop just read in TWO instruments (merge-tree --write-tree both orders; apply --cached of BASE..head onto develop's tree
in a temp index) + the seat's 0c834769 as a third reading; LEG D's hunk ranges vs #1212's in BASE coordinates (disjoint) with a CONTROL THAT FIRES
(a synthetic commit on the head editing a #1212-hunk line must CONFLICT under the same merge-tree); the moved sites read back from index.ts; the
LEG D pin strings at head; the head blobs. Writes pins_r2.txt (key=value) beside itself. rc 0 only if every hard assertion holds."""
import os, subprocess, sys, datetime, re, tempfile
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '2bc5ccf63b8c40911afb568b03cace066238ffcf'
R1 = '231ab8b5c898488b40ffe0c3672116b4bf5c80f7'
H1212 = 'ebb5d85ee0ed7ea524c686c87d504d5fa114962b'
BR = 'refs/heads/feature/ks-1239-r-1-the-indexts347-rawauthorization-capture-is-dead-code-0-r16b-rawauthdead-1'
SHARED = 'Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
INDEX = 'Blockchain/Dev/services/api-gateway/src/index.ts'
TEST = 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts'
SEAT_MERGED = '0c834769ecf99f9563105f0b1a48a6c7371955b2'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_r2 start', now())
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
print('checkout remote.origin.url:', url)
CL = tempfile.mkdtemp(prefix='r2clone_', dir=SP)
os.rmdir(CL)   # an empty dir we just made; clone wants to create it
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a): return sh(['git', '-C', CL] + list(a), env=ENV)
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', BR, 'refs/pull/1210/head', 'refs/pull/1212/head'])
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
rc, o, e = g('fetch', '--quiet', 'origin', '+refs/heads/develop:refs/heads/develop', '+refs/pull/1210/head:refs/r2/head', '+refs/pull/1212/head:refs/r2/h1212', '+%s:refs/r2/branch' % BR)
print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]; HEAD = g('rev-parse', 'refs/r2/head')[1]; BRH = g('rev-parse', 'refs/r2/branch')[1]
print('--- (a) heads and develop (two reads: ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote %s' % (DEV, LS.get('refs/heads/develop')))
hard(HEAD == LS.get('refs/pull/1210/head') == LS.get(BR) == BRH, '#1210 head %s == pull/1210/head == branch (ls-remote and fetch)' % HEAD)
hard(g('rev-parse', 'refs/r2/h1212')[1] == H1212, '#1212 head at origin still %s' % H1212)
print('--- (b) ancestry')
par = g('rev-parse', HEAD + '^')[1]; par2 = g('rev-parse', R1 + '^')[1]
hard(par == R1, 'head parent == round-1 head %s (fast-forward)' % R1)
hard(par2 == BASE, 'round-1 head parent == BASE %s' % BASE)
mb = g('merge-base', DEV, HEAD)[1]; hard(mb == BASE, 'merge-base(develop, head) %s == BASE' % mb)
ahead = int(g('rev-list', '--count', DEV + '..' + HEAD)[1]); behind = int(g('rev-list', '--count', HEAD + '..' + DEV)[1])
print('  compare develop...head: ahead %d behind %d' % (ahead, behind)); hard(ahead == 2, 'ahead == 2 (r1 + r2 commits)')
print('  BASE..develop:'); print('    ' + g('log', '--format=%H %s', BASE + '..' + DEV)[1].replace('\n', '\n    '))
DEVTREE = g('rev-parse', DEV + '^{tree}')[1]; print('  develop tree', DEVTREE)
DEV0 = 'dd8f99cc75b9b753172a40379eaab2b6c1026180'   # the develop the commission and READY r2 name (six tier-1 merged)
if DEV != DEV0:
    anc = g('merge-base', '--is-ancestor', DEV0, DEV)[0] == 0
    hard(anc, 'develop moved past %s: it is a DESCENDANT (else re-predict by hand)' % DEV0)
    mv = g('diff', '--name-only', DEV0, DEV)[1].splitlines() if anc else []
    print('  develop move %s..%s touches %d paths' % (DEV0[:12], DEV[:12], len(mv)))
    hard(not ({SHARED, INDEX, TEST} & set(mv)), 'the further develop move touches none of #1210\'s 3 paths (else re-predict BY HAND)')
else:
    print('  develop == %s (the commission\'s / READY r2\'s develop)' % DEV0)
with open(os.path.join(G, 'devlog_r2.txt'), 'w') as f: f.write(g('log', '--format=%H %s', BASE + '..' + DEV)[1] + '\n')
print('--- (c) numstat')
ns = g('diff', '--numstat', BASE, HEAD)[1]; print('  BASE..head:\n    ' + ns.replace('\n', '\n    '))
rows = [l.split('\t') for l in ns.splitlines()]
hard(sorted(r[2] for r in rows) == sorted([SHARED, INDEX, TEST]), 'BASE..head touches exactly the 3 declared paths')
d = {r[2]: (r[0], r[1]) for r in rows}
hard(d.get(INDEX) == ('0', '18'), 'index.ts +0/-18'); hard(d.get(SHARED) == ('17', '8'), 'shared test +17/-8')
ns2 = g('diff', '--numstat', R1, HEAD)[1]; print('  round-2 delta r1..head:\n    ' + ns2.replace('\n', '\n    '))
hard(ns2 == '17\t8\t' + SHARED, 'the round-2 delta is ONLY the shared file +17/-8')
auth = g('diff', '--numstat', BASE, HEAD, '--', 'Blockchain/Dev/services/auth/')[1]; ctl = g('diff', '--numstat', BASE, HEAD, '--', 'Blockchain/Dev/services/api-gateway/')[1]
hard(auth == '' and len(ctl.splitlines()) == 2, 'services/auth/ rows 0 (control: services/api-gateway/ rows %d, want 2)' % len(ctl.splitlines()))
print('--- (d) blobs at head')
BL = {}
for p in (INDEX, TEST, SHARED):
    ls = g('ls-tree', HEAD, '--', p)[1]; BL[p] = ls.split()[2]; print('   ', ls)
    hard(ls.split()[0] == '100644', p + ' mode 100644')
print('--- (e) merged tree over the develop just read — two instruments + the seat')
m1 = g('merge-tree', '--write-tree', DEV, HEAD); m2 = g('merge-tree', '--write-tree', HEAD, DEV)
MT1 = m1[1].splitlines()[0] if m1[1] else ''; MT2 = m2[1].splitlines()[0] if m2[1] else ''
print('  merge-tree develop,head rc %d -> %s | head,develop rc %d -> %s' % (m1[0], MT1, m2[0], MT2))
idx = os.path.join(CL, 'r2.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '-C', CL, 'read-tree', DEVTREE], env=E2)
patch = g('diff', '--binary', '--full-index', BASE, HEAD)[1] + '\n'
ap = sh(['git', '-C', CL, 'apply', '--cached', '-'], env=E2, inp=patch); AT = sh(['git', '-C', CL, 'write-tree'], env=E2)[1]
print('  apply --cached BASE..head onto develop tree rc %d %s -> %s' % (ap[0], ap[2][:200], AT))
hard(m1[0] == 0 and m2[0] == 0 and MT1 == MT2 == AT, 'merged tree identical in both merge-tree orders and the apply instrument: %s' % MT1)
print('  seat READY r2 merged tree %s == ours: %s' % (SEAT_MERGED, MT1 == SEAT_MERGED))
MERGED = MT1
for p in (INDEX, TEST, SHARED):
    b = g('rev-parse', MERGED + ':' + p)[1]; print('   merged %s %s == head blob: %s' % (b[:12], p.split('/')[-1], b == BL[p]))
hard(g('rev-parse', MERGED + ':' + SHARED)[1] != BL[SHARED], 'the merged shared file != the head blob (it carries #1212 too, as it must)')
mdiff = g('diff', '--stat', DEV, MERGED)[1].splitlines()[-1]; print('  develop -> merged:', mdiff)
print('--- (f) LEG D vs #1212 in the same file — hunk ranges in BASE coordinates')
def hunks(a, b):
    out = g('diff', '-U0', a, b, '--', SHARED)[1]
    return [(int(m.group(1)), int(m.group(2) or 1)) for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? ', out, re.M)]
HL = hunks(BASE, HEAD); HK = hunks(BASE, H1212)
print('  #1210 hunks (old start,len):', HL); print('  #1212 hunks (old start,len):', HK)
def span(h): return (h[0], h[0] + max(h[1], 1) - 1)
over = [(a, b) for a in HL for b in HK if not (span(a)[1] + 3 < span(b)[0] or span(b)[1] + 3 < span(a)[0])]
hard(not over, 'disjoint with 3 lines of context margin (overlaps: %s)' % over)
# CONTROL: a synthetic commit on #1210's head that edits the first line of #1212's first hunk must CONFLICT under the same merge-tree
# (fixed after run 1: #1212's hunk start is a BASE line number; at #1210's head it sits lower by #1210's net +9 above it — run 1 edited
#  head:2327, a DIFFERENT line, and its 'control' did not fire. Map the BASE line into head coordinates and assert the text is identical.)
bl = HK[0][0]; btxt = g('cat-file', 'blob', BASE + ':' + SHARED)[1].split('\n'); txt = g('cat-file', 'blob', HEAD + ':' + SHARED)[1].split('\n')
net = sum(1 for _ in [])
nd = g('diff', '-U0', BASE, HEAD, '--', SHARED)[1]
for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', nd, re.M):
    os_, ol, ns_, nl = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
    if os_ + max(ol, 1) - 1 < bl: net += nl - ol
ln = bl + net
print('  control: #1212 hunk at BASE:%d -> head:%d (net %+d above it); BASE text %r' % (bl, ln, net, btxt[bl - 1][:100]))
hard(txt[ln - 1] == btxt[bl - 1], 'control target mapped: head:%d text == BASE:%d text' % (ln, bl))
k12 = g('diff', '-U0', BASE, H1212, '--', SHARED)[1]; print('  #1212 rewrote at that hunk:\n    ' + '\n    '.join(l for l in k12.splitlines() if l[:1] in '+-' and not l.startswith(('+++', '---')))[:600])
txt[ln - 1] = txt[ln - 1] + ' // r2-control'
bh = sh(['git', '-C', CL, 'hash-object', '-w', '--stdin'], env=ENV, inp='\n'.join(txt) + '\n')[1]
sh(['git', '-C', CL, 'read-tree', HEAD], env=E2); sh(['git', '-C', CL, 'update-index', '--cacheinfo', '100644,%s,%s' % (bh, SHARED)], env=E2)
ct = sh(['git', '-C', CL, 'write-tree'], env=E2)[1]
cc = sh(['git', '-C', CL, 'commit-tree', ct, '-p', HEAD, '-m', 'r2 control (scratch only)'], env=dict(E2, GIT_AUTHOR_NAME='x', GIT_AUTHOR_EMAIL='x@x', GIT_COMMITTER_NAME='x', GIT_COMMITTER_EMAIL='x@x'))[1]
mc = g('merge-tree', '--write-tree', '--name-only', DEV, cc)
print('  control merge-tree rc %d; output tail: %s' % (mc[0], mc[1].splitlines()[-2:] if mc[1] else ''))
hard(mc[0] == 1, 'CONTROL FIRES: an edit on a #1212-hunk line CONFLICTS (rc 1) under the same instrument')
print('--- (g) the moved sites, read back from index.ts (BASE line -> head line), by TEXT')
bi = g('cat-file', 'blob', BASE + ':' + INDEX)[1].split('\n'); hi = g('cat-file', 'blob', HEAD + ':' + INDEX)[1].split('\n')
print('  index.ts lines BASE %d -> head %d' % (len(bi), len(hi)))
for a, b in ((845, 827), (858, 840), (891, 873)):
    print('   %d: %s\n   %d: %s' % (a, bi[a - 1].strip()[:110], b, hi[b - 1].strip()[:110]))
    hard(bi[a - 1] == hi[b - 1] and 'mockBodyParser' in hi[b - 1], 'BASE:%d == head:%d byte-identical and carries mockBodyParser' % (a, b))
hs = g('cat-file', 'blob', HEAD + ':' + SHARED)[1]
print('  LEG D pin strings at head:')
for m in re.finditer(r'^.*(index\.ts:\d+ express\.json|toContain\(\d+\)).*$', hs, re.M): print('    ' + m.group(0).strip()[:140])
old_live = [l for l in re.findall(r'^.*\b(845|858|891)\b.*$', hs, re.M)]
print('  lines at head still naming 845/858/891:', len(re.findall(r'^.*\b(?:845|858|891)\b.*$', hs, re.M)))
for l in re.findall(r'^.*\b(?:845|858|891)\b.*$', hs, re.M): print('    ' + l.strip()[:160])
print('--- (h) the round-2 delta on the shared file, verbatim (for the scope grade)')
print(g('diff', R1, HEAD, '--', SHARED)[1])
print('--- (i) other packages/shared tests naming api-gateway index.ts by line (CROSSLANE-READERS) at the merged tree')
gr = g('grep', '-n', '-E', r"index\.ts:[0-9]+", MERGED, '--', 'Blockchain/Dev/packages/shared/src/__tests__/')[1]
files = sorted(set(l.split(':')[1] for l in gr.splitlines())); print('  files:', files, '| lines:', len(gr.splitlines()))
with open(os.path.join(G, 'pins_r2.txt'), 'w') as f:
    for k, v in (('MEASURED_AT', now()), ('BASE', BASE), ('R1', R1), ('HEAD', HEAD), ('DEVELOP', DEV), ('DEVELOP_TREE', DEVTREE), ('BEHIND', behind),
                 ('MERGED_TREE', MERGED), ('SEAT_MERGED_EQUAL', MT1 == SEAT_MERGED), ('BLOB_INDEX', BL[INDEX]), ('BLOB_TEST', BL[TEST]), ('BLOB_SHARED', BL[SHARED]),
                 ('HUNKS_1210', HL), ('HUNKS_1212', HK), ('FAIL', len(FAIL))):
        f.write('%s=%s\n' % (k, v))
print('scratch clone', CL); print('HARD FAILS:', len(FAIL), FAIL); print('done', now())
sys.exit(1 if FAIL else 0)
