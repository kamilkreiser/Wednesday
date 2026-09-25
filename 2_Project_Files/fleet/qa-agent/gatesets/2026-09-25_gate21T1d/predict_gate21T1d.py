#!/usr/bin/env python3
"""predict_gate21T1d.py — MEASURE the tier-1 ROUND-2 gate of #1239 KS-1263 (head c8e1875c2, Seat B 27th) over origin develop AS READ NOW, and write
pins_gate21T1d.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, read-tree /
apply --cached / write-tree in a TEMP index) runs in a scratch clone under <scratchpad>/g21T1d_sp/clone — `git clone --shared` FROM the checkout
(objects borrowed read-only; the DRAFTER's instrument only — the gate itself clones from origin), then a fetch FROM ORIGIN into THAT clone (the
checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only, never printed). Nothing is written into the checkout.

REFUSES (rc 1) unless, over the develop just read:
  * the head is at its branch AND refs/pull/1239/head; head^ == the round-1 head R1 (42c20e998) and R1^ == BASE (6ab9d5021): 2 commits over BASE,
    a FAST-FORWARD of round 1 (the seat's claim, measured);
  * the round-2 delta R1..head touches EXACTLY the two TEST paths (ks1228, ks1263) — no product path, so no new surface (legs 3/4/8 not owed);
    documents.ts and shareRepo.ts blobs at head == at R1;
  * BASE is an ancestor of develop; merge-base(develop, head) == BASE;
  * move (BASE..develop) ∩ #1239's own paths == EXACTLY the two KNOWN overlaps (documents.ts, the ks1228 test) — any NEW overlap is re-predicted BY
    HAND, never here; the move touches NONE of the cell's reach: services/originate/src/db.ts, services/originate/src/repositories/shareRepo.ts,
    packages/shared/src/db/ (substrate paths it DOES touch — migrations, docker/init*, run-migrations.sh, originate package files — are REPORTED);
  * THE REGION CHECK: every BASE-side hunk of BASE..develop on documents.ts lies OUTSIDE the /:id/share and /:id/transfer-custody handler spans at
    BASE, AND each handler's text at BASE == at develop (byte-equal), AND each handler's text in the MERGED tree == at the head;
  * the PR merges clean (merge-tree rc 0); diff --name-only(develop, merged) == own paths; numstat(develop -> merged) == numstat(BASE -> head); every
    NON-overlap merged blob == the head blob; every OVERLAP path's patch-id(BASE..head -- p) == patch-id(develop..merged -- p);
  * END_TREE (== the merged tree, one PR) equals a second instrument: apply --cached of BASE..head onto develop's tree in a temp index.
Usage: predict_gate21T1d.py <scratchpad dir under /private/tmp/claude-501/> [--develop <40-hex>] [--pretend-hunk <BASE line>]
  (--develop and --pretend-hunk are TEST overrides for controls only: an older develop; a synthetic BASE-side hunk injected into the region check)
"""
import json, os, re, subprocess, sys, datetime, tempfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
R1 = '42c20e998a1a69887b8378968a8ff4f19106c24b'
HEAD = 'c8e1875c21e994a746e36c8b8efec8de1d9dbc98'
BRANCH = 'refs/heads/feature/ks-1263-share-transfer-transaction-l1-g-1'
O = 'Blockchain/Dev/services/originate/'
DOCS = O + 'src/routes/documents.ts'
KS1228 = O + 'src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts'
KS1263 = O + 'src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts'
OVERLAP = sorted([KS1228, DOCS])
R2_DELTA = sorted([KS1228, KS1263])
PRODUCT = [DOCS, O + 'src/repositories/shareRepo.ts']
REACH_FORBIDDEN = [O + 'src/db.ts', O + 'src/repositories/shareRepo.ts', 'Blockchain/Dev/packages/shared/src/db/']
SUBSTRATE = ['Blockchain/Dev/migrations/', 'Blockchain/Dev/docker/init/', 'Blockchain/Dev/docker/init-platform/', 'Blockchain/Dev/scripts/run-migrations.sh',
             O + 'package.json', O + 'package-lock.json', O + 'jest.integration.config.js', 'Blockchain/Dev/package-lock.json', 'Blockchain/Dev/prisma/']
HANDLERS = ["'/:id/share',", "'/:id/transfer-custody',"]

def die(msg):
    print('REFUSING: ' + msg); sys.exit(1)

def run(args, cwd=None, env=None, inp=None, ok=(0,)):
    p = subprocess.run(args, cwd=cwd, env=env, input=inp, capture_output=True, text=True)
    if p.returncode not in ok:
        die('%s -> rc %d: %s' % (' '.join(args[:6]), p.returncode, (p.stderr or p.stdout).strip()[:400]))
    return p.stdout

if len(sys.argv) < 2 or not sys.argv[1].startswith('/private/tmp/claude-501/') or not os.path.isdir(sys.argv[1]):
    die('argv[1] must be an existing scratchpad dir under /private/tmp/claude-501/')
SP = sys.argv[1]
DEV_OVERRIDE = sys.argv[sys.argv.index('--develop') + 1] if '--develop' in sys.argv else None
PRETEND = int(sys.argv[sys.argv.index('--pretend-hunk') + 1]) if '--pretend-hunk' in sys.argv else None
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate21T1d.py at', now(), '| scratchpad', SP)

# 1. ls-remote from the checkout (READ verb)
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1239/head', BRANCH])
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
DEV = DEV_OVERRIDE or lsd.get('refs/heads/develop')
print('ls-remote: develop %s%s' % (lsd.get('refs/heads/develop'), ' (OVERRIDDEN to %s for a control)' % DEV_OVERRIDE if DEV_OVERRIDE else ''))
a, b = lsd.get('refs/pull/1239/head'), lsd.get(BRANCH)
print('  #1239 pull/head %s branch %s pinned %s' % (a, b, HEAD))
if a != HEAD or b != HEAD:
    die('#1239 head moved or absent (pull %s, branch %s, pinned %s) — a new head needs a new READY, capture and a re-draft' % (a, b, HEAD))

# 2. scratch clone (write verbs ONLY here)
CL = os.path.join(SP, 'g21T1d_sp', 'clone')
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--shared', '--no-checkout', CHECKOUT, CL])
    run(['git', '-C', CL, 'remote', 'set-url', 'origin', ORIGIN])
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
need = [DEV, BASE, R1, HEAD]
missing = [s for s in need if subprocess.run(['git', '-C', CL, 'cat-file', '-e', s + '^{commit}'], capture_output=True).returncode != 0]
if missing:
    print('fetching from origin into the scratch clone for', ' '.join(m[:9] for m in missing))
    run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '-C', CL, 'fetch', '-q', 'origin',
         '+refs/heads/develop:refs/g21T1d/develop', '+refs/pull/1239/head:refs/g21T1d/pr1239'], env=env)
    for s in need:
        if subprocess.run(['git', '-C', CL, 'cat-file', '-e', s + '^{commit}'], capture_output=True).returncode != 0:
            die('object %s still missing after the fetch' % s)
g = lambda *a, **k: run(['git', '-C', CL] + list(a), **k)

# 3. the head's shape: a fast-forward of round 1, test-only delta
if g('rev-list', '--parents', '-n1', HEAD).split()[1:] != [R1]: die('head^ != the round-1 head %s' % R1)
if g('rev-list', '--parents', '-n1', R1).split()[1:] != [BASE]: die('R1^ != BASE')
if g('rev-list', '--count', BASE + '..' + HEAD).strip() != '2': die('the head is not exactly 2 commits over BASE')
r2 = sorted(x for x in g('diff', '--name-only', R1, HEAD).splitlines() if x)
if r2 != R2_DELTA: die('the round-2 delta R1..head touches %s, the kit expects exactly %s (test-only)' % (r2, R2_DELTA))
for p in PRODUCT:
    if g('rev-parse', '%s:%s' % (R1, p)).strip() != g('rev-parse', '%s:%s' % (HEAD, p)).strip(): die('product blob %s differs between R1 and head' % p)
r2_numstat = g('diff', '--numstat', R1, HEAD).strip()
print('head %s = R1 %s + 1 commit (test-only: %s); product blobs unchanged since round 1' % (HEAD[:9], R1[:9], ', '.join(os.path.basename(x) for x in r2)))

# 4. develop move
if subprocess.run(['git', '-C', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode != 0:
    die('BASE %s is not an ancestor of develop %s' % (BASE, DEV))
mb = g('merge-base', DEV, HEAD).strip()
if mb != BASE: die('merge-base(develop, head) %s != BASE' % mb)
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('develop %s is %d commits ahead of BASE; the move touches %d paths' % (DEV, len(move_log), len(move)))
own = sorted(x for x in g('diff', '--name-only', BASE, HEAD).splitlines() if x)
ov = sorted(set(own) & set(move))
if ov != OVERLAP: die('the develop move touches %s of #1239\'s own paths; the kit expects exactly %s — re-predict BY HAND' % (ov, OVERLAP))
bad = [m for m in move for f in REACH_FORBIDDEN if m == f or (f.endswith('/') and m.startswith(f))]
if bad: die('the develop move touches the cell\'s reach %s — re-predict BY HAND' % bad)
subst = [m for m in move for f in SUBSTRATE if m == f or (f.endswith('/') and m.startswith(f))]
subst_log = {m: [l[:9] for l in g('log', '--format=%H', BASE + '..' + DEV, '--', m).splitlines() if l] for m in subst}
print('substrate paths the move touches (REPORTED, not refused): %s' % (subst_log or 'none'))
docs_move_commits = [l for l in g('log', '--format=%h %s', BASE + '..' + DEV, '--', DOCS).splitlines() if l]
print('commits on documents.ts in the move: %s' % docs_move_commits)

# 5. THE REGION CHECK
def spans(rev):
    lines = g('show', '%s:%s' % (rev, DOCS)).split('\n')
    decl = [i for i, l in enumerate(lines) if l.startswith('documentsRouter.')]
    out = {}
    for h in HANDLERS:
        hit = [i for i, l in enumerate(lines) if l.strip() == h]
        if len(hit) != 1: die('%s: %d lines equal %r (want 1)' % (rev[:9], len(hit), h))
        start = max(d for d in decl if d < hit[0])
        nxt = [d for d in decl if d > hit[0]]
        end = (nxt[0] - 1) if nxt else len(lines) - 1
        out[h] = (start + 1, end + 1, '\n'.join(lines[start:end + 1]))   # 1-based inclusive
    return out
sb, sd, sh = spans(BASE), spans(DEV), spans(HEAD)
hunks = []
for l in g('diff', '-U0', BASE, DEV, '--', DOCS).splitlines():
    m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+', l)
    if m:
        s, c = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        hunks.append((s, s + max(c, 1) - 1))
if PRETEND is not None:
    hunks.append((PRETEND, PRETEND)); print('  (CONTROL: a synthetic BASE-side hunk at line %d injected)' % PRETEND)
region = {}
for h, (s0, e0, txt) in sb.items():
    inter = [x for x in hunks if not (x[1] < s0 or x[0] > e0)]
    region[h] = {'base_span': [s0, e0], 'develop_span': list(sd[h][:2]), 'head_span': list(sh[h][:2]), 'hunks_inside': inter}
    print('  %-26s BASE %d-%d | develop %d-%d | head %d-%d | move hunks inside: %s' % (h, s0, e0, sd[h][0], sd[h][1], sh[h][0], sh[h][1], inter or 'none'))
    if inter: die('a develop-move hunk %s falls INSIDE the %s handler at BASE (%d-%d) — the region the cell reaches moved: re-predict BY HAND' % (inter, h, s0, e0))
    if txt != sd[h][2]: die('the %s handler text differs between BASE and develop' % h)
print('move hunks on documents.ts (BASE side): %s — none inside either handler; both handler texts byte-equal BASE == develop' % hunks)

# 6. the merge
mt = g('merge-tree', '--write-tree', DEV, HEAD, ok=(0, 1)).split('\n')[0].strip()
if subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, HEAD], capture_output=True).returncode != 0:
    die('#1239 does NOT merge clean over develop %s' % DEV)
changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x)
if changed != own: die('diff(develop, merged) %s != own paths %s' % (changed, own))
ns_head = g('diff', '--numstat', BASE, HEAD).strip(); ns_merged = g('diff', '--numstat', DEV, mt).strip()
if ns_head != ns_merged: die('numstat(develop->merged) != numstat(BASE->head)')
files = []
for path in own:
    hb = g('rev-parse', '%s:%s' % (HEAD, path)).strip(); mbb = g('rev-parse', '%s:%s' % (mt, path)).strip()
    mode = g('ls-tree', HEAD, '--', path).split()[0]
    bb = subprocess.run(['git', '-C', CL, 'rev-parse', '%s:%s' % (BASE, path)], capture_output=True, text=True)
    bb = bb.stdout.strip() if bb.returncode == 0 else 'ABSENT'
    db_ = subprocess.run(['git', '-C', CL, 'rev-parse', '%s:%s' % (DEV, path)], capture_output=True, text=True)
    db_ = db_.stdout.strip() if db_.returncode == 0 else 'ABSENT'
    if path in OVERLAP:
        pid_h = g('patch-id', '--stable', inp=g('diff', BASE, HEAD, '--', path)).split()[0]
        pid_m = g('patch-id', '--stable', inp=g('diff', DEV, mt, '--', path)).split()[0]
        if pid_h != pid_m: die('%s: patch-id BASE..head %s != develop..merged %s' % (path, pid_h, pid_m))
        if hb == mbb: die('%s is an overlap path but its merged blob == its head blob' % path)
        files.append({'path': path, 'mode': mode, 'head_blob': hb, 'merged_blob': mbb, 'base_blob': bb, 'develop_blob': db_, 'overlap': True, 'patch_id': pid_h})
    else:
        if hb != mbb: die('%s: merged blob %s != head blob %s' % (path, mbb, hb))
        files.append({'path': path, 'mode': mode, 'head_blob': hb, 'merged_blob': mbb, 'base_blob': bb, 'develop_blob': db_, 'overlap': False})
mcommit = g('commit-tree', mt, '-p', DEV, '-p', HEAD, '-m', 'g21T1d predict (scratch)').strip()
smerged = spans(mcommit)
for h in HANDLERS:
    if smerged[h][2] != sh[h][2]: die('the %s handler text in the MERGED tree != at the head' % h)
    region[h]['merged_span'] = list(smerged[h][:2])
print('#1239 merges clean over %s: merged tree %s | %d paths | overlap %d (patch-id equal on each) | both handlers in the merged tree == the head\'s' % (DEV[:9], mt, len(own), len(ov)))

# 7. END_TREE, a second instrument
idx = tempfile.mktemp(prefix='g21T1d_idx_', dir=os.path.join(SP, 'g21T1d_sp'))
ienv = dict(os.environ, GIT_INDEX_FILE=idx)
run(['git', '-C', CL, 'read-tree', DEV], env=ienv)
run(['git', '-C', CL, 'apply', '--cached'], env=ienv, inp=g('diff', '--binary', BASE, HEAD))
e3 = run(['git', '-C', CL, 'write-tree'], env=ienv).strip()
os.remove(idx)
if e3 != mt: die('END_TREE by merge-tree %s != by apply --cached %s' % (mt, e3))
out = {'measured_at': now(), 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'r1': R1, 'head': HEAD, 'branch': BRANCH,
       'develop': DEV, 'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move),
       'r2_delta': r2, 'r2_numstat': r2_numstat, 'subject': g('log', '-1', '--format=%s', HEAD).strip(), 'merged_tree': mt, 'end_tree': mt,
       'numstat': ns_head, 'shortstat': g('diff', '--shortstat', BASE, HEAD).strip(), 'end_shortstat': g('diff', '--shortstat', DEV, mt).strip(),
       'files': files, 'overlap': ov, 'substrate_touched': subst_log, 'docs_move_commits': docs_move_commits, 'docs_move_hunks': hunks, 'region': region}
print('END_TREE %s (merge-tree == apply --cached) | %s' % (mt, out['end_shortstat']))
if PRETEND is not None or DEV_OVERRIDE:
    print('CONTROL RUN — pins NOT written'); sys.exit(0)
with open(os.path.join(GS, 'pins_gate21T1d.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, 'pins_gate21T1d.json'), 'at', now())
sys.exit(0)
