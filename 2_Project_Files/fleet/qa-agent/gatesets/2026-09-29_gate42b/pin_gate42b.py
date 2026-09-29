#!/usr/bin/env python3
"""pin_gate42b.py — MEASURE the pins for the gate42b kit (kit.json beside this script) and write pins_gate42b.json.
Reads origin by `git ls-remote` (with the Secuura deploy key, in a scratch clone), fetches develop + refs/pull/<n>/head INTO THE SCRATCH CLONE ONLY
(<scratchpad>/g42b_sp/clone — built by `git clone --shared --no-checkout` from kit.json base_clone, or from the checkout, when absent), then:
  P1 head at branch == head at refs/pull/<n>/head (WHOLE-FIELD);         P2 merge-base(develop, head) and ahead/behind;
  P3 diff(merge-base...head) names == [kit path] and numstat == kit numstat; P4 merge-tree --write-tree develop head: CLEAN, END_TREE;
  P5 diff(develop, END) == [kit path] and END blob == head blob;          P6 if develop != the merge-base: the move must NOT touch the kit path.
Refuses rc 1 on any disagreement. --expect-head <sha>: also refuse unless the head equals it (the repin passes the launcher's pin).
Writes ONLY pins_gate42b.json beside this script and the scratch clone. Usage: pin_gate42b.py <scratchpad> [--expect-head <sha>]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
SP = sys.argv[1]; EXP = sys.argv[sys.argv.index('--expect-head') + 1] if '--expect-head' in sys.argv else None
CL = os.path.join(SP, 'g42b_sp', 'clone'); N = K['pr']; PATH = K['path']
SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
def git(*a, check=True):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if not os.path.isdir(CL):
    src = K['base_clone'] if os.path.isdir(K['base_clone']) else K['checkout']
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', src, CL], check=True)
    subprocess.run(['git', '-C', CL, 'remote', 'set-url', 'origin', 'git@github.com:Secuura/Distributed_Secuura.git'], check=True)
    print('built scratch clone %s (--shared from %s)' % (CL, src))
bad = []
ls = git('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % N, K['branch'])
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines()}
DEV, PH, BH = R.get('refs/heads/develop'), R.get('refs/pull/%s/head' % N), R.get(K['branch'])
print('ls-remote at %s: develop %s | pull/%s/head %s | branch %s' % (now(), DEV, N, PH, BH))
if not (PH and PH == BH): bad.append('P1 head at refs/pull/%s/head (%s) != at the branch (%s)' % (N, PH, BH))
if EXP and PH != EXP: bad.append('P1 head %s != the expected (pinned) head %s' % (PH, EXP))
git('fetch', '-q', 'origin', '+refs/heads/develop:refs/remotes/origin/develop', '+refs/pull/%s/head:refs/remotes/pr/%s' % (N, N))
if git('rev-parse', 'refs/remotes/origin/develop') != DEV or git('rev-parse', 'refs/remotes/pr/%s' % N) != PH: bad.append('fetched refs != ls-remote')
MB = git('merge-base', DEV, PH); ahead = int(git('rev-list', '--count', '%s..%s' % (MB, PH))); behind = int(git('rev-list', '--count', '%s..%s' % (MB, DEV)))
names = git('diff', '--name-only', MB, PH).splitlines(); ns = git('diff', '--numstat', MB, PH)
print('P2 merge-base %s | ahead %d | behind %d' % (MB, ahead, behind))
print('P3 files %s | numstat %r' % (names, ns))
if names != [PATH]: bad.append('P3 files %s != [%s]' % (names, PATH))
if ns != '%s\t%s' % (K['numstat'], PATH): bad.append('P3 numstat %r != %r' % (ns, K['numstat']))
mt = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', DEV, PH], capture_output=True, text=True)
END = mt.stdout.split('\n')[0].strip()
print('P4 merge-tree rc %d END_TREE %s' % (mt.returncode, END))
if mt.returncode != 0: bad.append('P4 merge-tree NOT clean (rc %d)' % mt.returncode)
d2 = git('diff', '--name-only', DEV, END).splitlines()
hb = git('rev-parse', '%s:%s' % (PH, PATH)); eb = git('rev-parse', '%s:%s' % (END, PATH)); db = git('rev-parse', '%s:%s' % (DEV, PATH)); mbb = git('rev-parse', '%s:%s' % (MB, PATH))
print('P5 diff(develop, END) %s | blob develop %s | merge-base %s | head %s | END %s' % (d2, db, mbb, hb, eb))
if d2 != [PATH] or eb != hb: bad.append('P5 diff(develop, END) %s or END blob %s != head blob %s' % (d2, eb, hb))
if DEV != MB:
    mv = git('diff', '--name-only', MB, DEV).splitlines()
    print('P6 develop moved since the merge-base: %d path(s); touches the kit path: %s' % (len(mv), PATH in mv))
    if PATH in mv: bad.append('P6 the develop move touches %s — a re-draft decides' % PATH)
else: print('P6 develop == the merge-base (no move)')
P = {'measured_at': now(), 'pr': N, 'branch': K['branch'], 'head': PH, 'develop': DEV, 'develop_tree': git('rev-parse', DEV + '^{tree}'), 'merge_base': MB,
     'ahead': ahead, 'behind': behind, 'files': names, 'numstat': K['numstat'], 'end_tree': END, 'blob_develop': db, 'blob_merge_base': mbb, 'blob_head': hb,
     'head_parent': git('rev-parse', PH + '^'), 'head_subject_commit': git('log', '-1', '--format=%s', PH)}
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + b) for b in bad]; raise SystemExit(1)
json.dump(P, open(os.path.join(G, 'pins_gate42b.json'), 'w'), indent=1)
print('PASS: pins_gate42b.json | head %s | develop %s | END_TREE %s' % (PH, DEV, END))
