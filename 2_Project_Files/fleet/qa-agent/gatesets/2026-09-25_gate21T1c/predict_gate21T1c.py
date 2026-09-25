#!/usr/bin/env python3
"""predict_gate21T1c.py — MEASURE the round-21 THIRD tier-1 batch (#1234 KS-1127+KS-1089+KS-1135, #1239 KS-1263) over origin develop AS READ NOW,
and write pins_gate21T1c.json beside this script. Never adopts a value from a mail.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, commit-tree,
read-tree / apply --cached / write-tree in a TEMP index) runs in a scratch clone under <scratchpad>/g21c_sp/clone — `git clone --shared` FROM the
checkout (objects borrowed read-only), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the
clone only, never printed). Nothing is written into the checkout.

REFUSES (rc 1) unless, over the develop just read:
  * each head's parent IS BASE and it is exactly 1 commit ahead of BASE; merge-base(develop, head) == BASE;
  * the develop move (BASE..develop) descends from BASE;
  * move ∩ #1234's own paths == EMPTY; move ∩ #1239's own paths == EXACTLY the two KNOWN overlaps (documents.ts via #1225 KS-1291, the ks1228 test via
    KS-1266 9e744421a) — any NEW overlap is re-predicted BY HAND, never here;
  * each PR merges clean (merge-tree rc 0); diff --name-only(develop, merged) == the PR's own paths; numstat(develop -> merged) == numstat(BASE -> head);
    for every NON-overlap path the merged blob == the head blob; for every OVERLAP path patch-id(BASE..head -- p) == patch-id(develop..merged -- p);
  * #1234 ∩ #1239 == EMPTY; END_TREE identical in both orders AND by a second instrument (apply --cached of each BASE..head onto develop's tree).
Usage: predict_gate21T1c.py <scratchpad dir under /private/tmp/claude-501/> [--develop <40-hex>]   (--develop: a TEST override for controls only)
"""
import json, os, subprocess, sys, datetime, tempfile

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
PRS = {
    '1234': {'key': 'KS-1127 + KS-1089 + KS-1135', 'ks': 'KS-1127', 'head': '6320a61d86b5d3fb9b693ea5fefb42050e1d2a43',
             'branch': 'refs/heads/feature/ks-1127-run-shell-suites-skip-tally-l4-skiptally-1', 'overlap': []},
    '1239': {'key': 'KS-1263', 'ks': 'KS-1263', 'head': '42c20e998a1a69887b8378968a8ff4f19106c24b',
             'branch': 'refs/heads/feature/ks-1263-share-transfer-transaction-l1-g-1',
             'overlap': ['Blockchain/Dev/services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts',
                         'Blockchain/Dev/services/originate/src/routes/documents.ts']},
}

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
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('predict_gate21T1c.py at', now(), '| scratchpad', SP)

# 1. ls-remote from the checkout (READ verb)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in PRS] + [PRS[n]['branch'] for n in PRS]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
lsd = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
DEV = DEV_OVERRIDE or lsd.get('refs/heads/develop')
print('ls-remote: develop %s%s' % (lsd.get('refs/heads/develop'), ' (OVERRIDDEN to %s for a control)' % DEV_OVERRIDE if DEV_OVERRIDE else ''))
for n, p in PRS.items():
    a, b = lsd.get('refs/pull/%s/head' % n), lsd.get(p['branch'])
    print('  #%s pull/head %s branch %s pinned %s' % (n, a, b, p['head']))
    if a != p['head'] or b != p['head']:
        die('#%s head moved or absent (pull %s, branch %s, pinned %s) — a new head needs a new READY, capture and a re-draft' % (n, a, b, p['head']))

# 2. scratch clone (write verbs ONLY here)
CL = os.path.join(SP, 'g21c_sp', 'clone')
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--shared', '--no-checkout', CHECKOUT, CL])
    run(['git', '-C', CL, 'remote', 'set-url', 'origin', ORIGIN])
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
need = [DEV, BASE] + [p['head'] for p in PRS.values()]
missing = [s for s in need if subprocess.run(['git', '-C', CL, 'cat-file', '-e', s + '^{commit}'], capture_output=True).returncode != 0]
if missing:
    print('fetching from origin into the scratch clone for', ' '.join(m[:9] for m in missing))
    run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '-C', CL, 'fetch', '-q', 'origin',
         '+refs/heads/develop:refs/g21c/develop', '+refs/pull/1234/head:refs/g21c/pr1234', '+refs/pull/1239/head:refs/g21c/pr1239'], env=env)
    for s in need:
        if subprocess.run(['git', '-C', CL, 'cat-file', '-e', s + '^{commit}'], capture_output=True).returncode != 0:
            die('object %s still missing after the fetch' % s)
g = lambda *a, **k: run(['git', '-C', CL] + list(a), **k)

# 3. develop move
if subprocess.run(['git', '-C', CL, 'merge-base', '--is-ancestor', BASE, DEV]).returncode != 0:
    die('BASE %s is not an ancestor of develop %s' % (BASE, DEV))
move_log = [l for l in g('log', '--format=%H %s', BASE + '..' + DEV).splitlines() if l]
move = sorted(x for x in g('diff', '--name-only', BASE, DEV).splitlines() if x)
print('develop %s is %d commits ahead of BASE; the move touches %d paths' % (DEV, len(move_log), len(move)))
out = {'measured_at': now(), 'base': BASE, 'base_tree': g('rev-parse', BASE + '^{tree}').strip(), 'develop': DEV,
       'develop_tree': g('rev-parse', DEV + '^{tree}').strip(), 'behind': len(move_log), 'move_log': move_log, 'move_paths': len(move), 'prs': {}}

# 4. per PR
own_all = {}
for n, p in PRS.items():
    h = p['head']
    par = g('rev-list', '--parents', '-n1', h).split()
    if par[1:] != [BASE]: die('#%s parent(s) %s != BASE' % (n, par[1:]))
    if g('rev-list', '--count', BASE + '..' + h).strip() != '1': die('#%s is not exactly 1 commit ahead of BASE' % n)
    mb = g('merge-base', DEV, h).strip()
    if mb != BASE: die('#%s merge-base(develop, head) %s != BASE' % (n, mb))
    own = sorted(x for x in g('diff', '--name-only', BASE, h).splitlines() if x)
    own_all[n] = own
    ov = sorted(set(own) & set(move))
    if ov != sorted(p['overlap']):
        die('#%s: the develop move touches %s of its own paths; the kit expects exactly %s — re-predict BY HAND' % (n, ov, p['overlap']))
    mt = g('merge-tree', '--write-tree', DEV, h, ok=(0, 1)).split('\n')[0].strip()
    if subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, h], capture_output=True).returncode != 0:
        die('#%s does NOT merge clean over develop %s' % (n, DEV))
    changed = sorted(x for x in g('diff', '--name-only', DEV, mt).splitlines() if x)
    if changed != own: die('#%s: diff(develop, merged) %s != its own paths %s' % (n, changed, own))
    ns_head = g('diff', '--numstat', BASE, h).strip(); ns_merged = g('diff', '--numstat', DEV, mt).strip()
    if ns_head != ns_merged: die('#%s numstat(develop->merged) != numstat(BASE->head)' % n)
    files = []
    for path in own:
        hb = g('rev-parse', '%s:%s' % (h, path)).strip(); mbb = g('rev-parse', '%s:%s' % (mt, path)).strip()
        mode = g('ls-tree', h, '--', path).split()[0]
        bb = subprocess.run(['git', '-C', CL, 'rev-parse', '%s:%s' % (BASE, path)], capture_output=True, text=True)
        bb = bb.stdout.strip() if bb.returncode == 0 else 'ABSENT'
        if path in p['overlap']:
            pid_h = g('patch-id', '--stable', inp=g('diff', BASE, h, '--', path)).split()[0]
            pid_m = g('patch-id', '--stable', inp=g('diff', DEV, mt, '--', path)).split()[0]
            if pid_h != pid_m: die('#%s %s: patch-id BASE..head %s != develop..merged %s' % (n, path, pid_h, pid_m))
            if hb == mbb: die('#%s %s is an overlap path but its merged blob == its head blob (the overlap is not what the kit thinks)' % (n, path))
            files.append({'path': path, 'mode': mode, 'head_blob': hb, 'merged_blob': mbb, 'base_blob': bb, 'overlap': True, 'patch_id': pid_h})
        else:
            if hb != mbb: die('#%s %s: merged blob %s != head blob %s' % (n, path, mbb, hb))
            files.append({'path': path, 'mode': mode, 'head_blob': hb, 'merged_blob': mbb, 'base_blob': bb, 'overlap': False})
    subj = g('log', '-1', '--format=%s', h).strip()
    out['prs'][n] = {'head': h, 'branch': p['branch'], 'key': p['key'], 'subject': subj, 'merged_tree': mt, 'numstat': ns_head,
                     'files': files, 'overlap': ov, 'shortstat': g('diff', '--shortstat', BASE, h).strip()}
    print('#%s ok: merged tree %s | %d paths | overlap with the move %d %s' % (n, mt, len(own), len(ov), ('(patch-id equal on each)' if ov else '')))

if set(own_all['1234']) & set(own_all['1239']): die('#1234 and #1239 share a path')

# 5. END_TREE, two orders + a second instrument
def merged_commit(parent, tree, other):
    return g('commit-tree', tree, '-p', parent, '-p', other, '-m', 'g21c predict (scratch)').strip()
a, b = PRS['1234']['head'], PRS['1239']['head']
t1 = out['prs']['1234']['merged_tree']; c1 = merged_commit(DEV, t1, a); e1 = g('merge-tree', '--write-tree', c1, b).split('\n')[0].strip()
t2 = out['prs']['1239']['merged_tree']; c2 = merged_commit(DEV, t2, b); e2 = g('merge-tree', '--write-tree', c2, a).split('\n')[0].strip()
if e1 != e2: die('END_TREE differs by order: %s vs %s' % (e1, e2))
idx = tempfile.mktemp(prefix='g21c_idx_', dir=os.path.join(SP, 'g21c_sp'))
ienv = dict(os.environ, GIT_INDEX_FILE=idx)
run(['git', '-C', CL, 'read-tree', DEV], env=ienv)
for h in (a, b):
    run(['git', '-C', CL, 'apply', '--cached'], env=ienv, inp=g('diff', '--binary', BASE, h))
e3 = run(['git', '-C', CL, 'write-tree'], env=ienv).strip()
os.remove(idx)
if e3 != e1: die('END_TREE by merge-tree %s != by apply --cached %s' % (e1, e3))
out['end_tree'] = e1
out['end_shortstat'] = g('diff', '--shortstat', DEV, e1).strip()
out['pairwise_disjoint'] = True
print('END_TREE %s (both orders + apply --cached agree) | %s' % (e1, out['end_shortstat']))
with open(os.path.join(GS, 'pins_gate21T1c.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1, sort_keys=True)
print('WROTE', os.path.join(GS, 'pins_gate21T1c.json'), 'at', now())
sys.exit(0)
