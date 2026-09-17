#!/usr/bin/env python3
"""redraft_setup_1035.py — the RE-DRAFTER's substrate for #1035 (KS-1204) (shape: drafter_setup_1035.py of the dead drafter; re-pointed at the CURRENT develop).
The dead drafter's clone (/private/tmp/claude-501/drafter1035/…) is outside this session's scratch: it is READ for comparison only, never reused for runs.
clone --shared --no-checkout into a fresh mktemp -d under the session scratchpad gate1035/; worktrees IN THE CLONE: head 4b1fb0621, dev = develop 3961c2add
(READ by ls-remote), merged = commit-tree(merge-tree --write-tree head x 3961c2add, parents head + develop) — a commit object IN THE CLONE ONLY, so a worktree
can hold it. Asserts: head's one parent 732c13459 = merge-base(head, 3961c2add); 732c13459..3961c2add touches no api-gateway / shared / eslint / Settings.tsx /
mcp-server path; merged api-gateway + shared + frontend/admin + mcp-server subtrees = head's; develop..head = the 2 PR files; merged vs develop = the 2 PR files.
Worktrees get NO node_modules here (farm_1035 does it, per ENTRY, with the vitest 4.1.11 overlay). Never rm. The Secuura checkout: read-only readings BEFORE/AFTER."""
import subprocess, os, tempfile, datetime, json, hashlib, sys
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8f7ffae4-dc85-433a-8a53-4d87581eb627/scratchpad/gate1035'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1035'
HEAD = '4b1fb0621e58ff00bba096751130bc6e53df4714'; BASE = '732c13459d76f5b05ade94bb91de7e47585b0e7d'
DEV = 'Blockchain/Dev'; G = DEV + '/services/api-gateway'
VER = G + '/src/routes/verification.ts'; TEST = G + '/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def run(c, cwd=None, env=None):
    p = subprocess.run(c, cwd=cwd, capture_output=True, text=True, env=env); return p.returncode, p.stdout, p.stderr
def checkout_reading(tag):
    wts = len(os.listdir(REPO + '/.git/worktrees'))
    rc, o, e = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    refs = len(run(['git', '-C', REPO, 'for-each-ref'])[1].splitlines())
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    br = run(['git', '-C', REPO, 'branch', '--show-current'])[1].strip()
    vd = REPO + '/' + G + '/node_modules/.vite'
    vite = sorted(os.listdir(vd)) if os.path.isdir(vd) else 'ABSENT'
    ls = run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1035/head'])[1].split('\n')
    r = dict(worktrees=wts, porcelain=len(o.splitlines()), refs=refs, config=cfg, branch=br, gateway_vite=vite, ls_remote=[x.split('\t')[::-1] for x in ls if x])
    P('source checkout', tag, now(), r, '| status stderr', repr(e.strip()[:200])); return r
P('redraft_setup_1035', now())
before = checkout_reading('BEFORE')
cur_dev = dict((b, a) for b, a in before['ls_remote'])['refs/heads/develop']; pr_head = dict((b, a) for b, a in before['ls_remote'])['refs/pull/1035/head']
P('origin develop', cur_dev, '| refs/pull/1035/head', pr_head, '== pin', pr_head == HEAD)
assert pr_head == HEAD, 'HEAD MOVED — STOP'
os.makedirs(SCR, exist_ok=True)
W = tempfile.mkdtemp(prefix='gate1035_redraft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
for k, v in (('head', HEAD), ('base', BASE), ('develop', cur_dev)):
    P('object', k, v[:9], run(['git', '-C', C, 'cat-file', '-t', v])[1].strip(), '| parents', [x[:9] for x in run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', v])[1].split()[1:]], '| tree', run(['git', '-C', C, 'rev-parse', v + '^{tree}'])[1].strip())
parents = run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', HEAD])[1].split()[1:]
mb = run(['git', '-C', C, 'merge-base', HEAD, cur_dev])[1].strip()
P('head parents', [p[:9] for p in parents], '| one parent = 732c13459:', parents == [BASE], '| merge-base(head, develop)', mb[:9], '= 732c13459:', mb == BASE)
dd = run(['git', '-C', C, 'diff', '--name-only', BASE, cur_dev])[1].split('\n'); dd = [x for x in dd if x]
WATCH = (G + '/', DEV + '/packages/shared/', DEV + '/eslint.config.mjs', DEV + '/frontend/admin/', DEV + '/services/mcp-server/')
P('develop delta 732c13459..%s: %d files %s | on a watched path: %s' % (cur_dev[:9], len(dd), dd, [x for x in dd if x.startswith(WATCH)]))
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', HEAD, cur_dev])
mt = o.strip().split('\n')[0]; P('merge-tree --write-tree (IN THE CLONE) head x develop rc', rc, 'tree', mt, '| conflicts/extra lines', o.strip().split('\n')[1:][:6], e.strip()[:200]); assert rc == 0
env = dict(os.environ, GIT_AUTHOR_NAME='qa1035-redrafter', GIT_AUTHOR_EMAIL='qa@invalid', GIT_COMMITTER_NAME='qa1035-redrafter', GIT_COMMITTER_EMAIL='qa@invalid', GIT_AUTHOR_DATE='2026-09-18T00:00:00Z', GIT_COMMITTER_DATE='2026-09-18T00:00:00Z')
rc, o, e = run(['git', '-C', C, 'commit-tree', mt, '-p', HEAD, '-p', cur_dev, '-m', 'qa1035 merged tree (clone only)'], env=env); MC = o.strip(); P('commit-tree (clone only) rc', rc, MC, e.strip()[:200]); assert rc == 0
for sub in (G, DEV + '/packages/shared', DEV + '/frontend/admin', DEV + '/services/mcp-server', DEV + '/eslint.config.mjs', DEV + '/package-lock.json'):
    vals = {k: run(['git', '-C', C, 'rev-parse', v + ':' + sub])[1].strip()[:9] for k, v in (('base', BASE), ('develop', cur_dev), ('head', HEAD), ('merged', MC))}
    P('subtree', sub.replace(DEV + '/', ''), vals, '| merged == head:', vals['merged'] == vals['head'], '| develop == base:', vals['develop'] == vals['base'])
dh = sorted(x for x in run(['git', '-C', C, 'diff', '--name-only', cur_dev, MC])[1].split('\n') if x); P('develop..merged files == the 2 PR files:', dh == sorted([VER, TEST]), dh)
bh = sorted(x for x in run(['git', '-C', C, 'diff', '--name-only', BASE, HEAD])[1].split('\n') if x); P('732c13459..head files == the 2 PR files:', bh == sorted([VER, TEST]), '| numstat', run(['git', '-C', C, 'diff', '--numstat', BASE, HEAD])[1].strip().replace('\n', ' | '))
pid = lambda a, b: run(['bash', '-c', 'git -C "$0" diff "$1" "$2" | git patch-id --stable', C, a, b])[1].split(' ')[0][:12]
P('patch-id 732c13459..head', pid(BASE, HEAD), '| develop..merged', pid(cur_dev, MC), '| equal', pid(BASE, HEAD) == pid(cur_dev, MC), '| control develop..head', pid(cur_dev, HEAD))
for p in (VER, TEST):
    P('blob', p.split('/')[-1], {k: (run(['git', '-C', C, 'rev-parse', '--verify', '-q', v + ':' + p])[1].strip()[:9] or 'ABSENT') for k, v in (('base', BASE), ('develop', cur_dev), ('head', HEAD), ('merged', MC))})
trees = {}
for name, sha in (('head', HEAD), ('dev', cur_dev), ('merged', MC)):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, sha]); assert rc == 0, e; trees[name] = wt
    P('worktree', name, sha[:9], 'porcelain', len(run(['git', '-C', wt, 'status', '--porcelain'])[1].splitlines()))
after = checkout_reading('AFTER')
P('checkout bounds equal (porcelain, worktrees, branch, config):', (before['porcelain'], before['worktrees'], before['branch'], before['config']) == (after['porcelain'], after['worktrees'], after['branch'], after['config']))
json.dump({'W': W, 'C': C, 'trees': trees, 'sha': {'head': HEAD, 'dev': cur_dev, 'merged': MC, 'base': BASE}, 'merged_tree': mt}, open(GS + '/out/r2/paths.json', 'w'), indent=1)
P('redraft_setup_1035 end', now())
