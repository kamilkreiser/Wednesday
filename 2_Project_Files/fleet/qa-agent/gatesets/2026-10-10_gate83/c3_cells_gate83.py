#!/usr/bin/env python3
"""c3_cells_gate83.py — the RUN instruments for gate83: #1450's shell suite (arms, base vs head), the leg run ONLY with stubs (node / npm / git on a private PATH; NO real npm ci, NO
install of any lock), the three stub-git variants + a real no-.git run (finding F1), the bash 3.2.57 empty-corpus abort (F2) and the empty-CHECKED guard on the EXTRACTED function,
the cwd question (Q-CWD1426), the sibling suite, the payload applied from the Spark patch.diff, the real-tree surface COMPUTED (never run), tamper rows, and the COMPOSITION of the
two shared platform-k HTML docs against the OTHER writers of them (#1444 flow 50, #1447 flow 51, #1449 flow 52, #1448 flow 54) around #1450's flow 53. Every write path is
checked lexically AND by realpath and refused under !CODING. Carried in shape from c3_cells_gate82.py; [g83] rebuilt. NO vitest, NO tsx, NO `npx`, NO npm of any kind.

  shells   --clone CL --head H --base B --scratch S --out DIR   the new suite with the head product / the BASE product planted (red cells named); `run-shell-suites.sh --list` base vs head;
           html_docs_matrix at the head tree; config hashes around every run. All in trees extracted with `git archive` OUTSIDE every git repo (asserted, with a control).
  payload  --clone CL --head H --base B --scratch S --out DIR   `git apply -p1` of the Spark patch.diff onto the BASE files (in a scratch tree outside every repo): the applied blobs vs the head's.
  stubs    --clone CL --head H --base B --scratch S --out DIR   F1 / F2 / F5: the leg (head AND base script) in a scratch repo under: no stub, S1 git fails on any call, S2 `--show-prefix` fails,
           S3 `ls-files` fails, a real tree with no .git, the advisory-SKIP path (node 18 + docker down); the zero-lock corpus on bash 3.2.57; the EXTRACTED report_surface with an empty CHECKED
           and an unguarded-expansion CONTROL. Each stub is shown to take effect (its call log). Exit codes compared with the unstubbed run.
  realtree --clone CL --head H --scratch S --out DIR   the surface COMPUTED on the real tree: the 45 tracked lock paths, `find` over the extracted lock files (35), and the EXTRACTED report_surface run
           in a scratch repo that tracks those 45 paths (MODELLED: the leg itself is not run on the real tree).
  cwd      --clone CL --head H --scratch S --out DIR   Q-CWD1426: the new suite from a non-repo cwd, from inside a scratch repo with .githooks (hooksPath unset), from a worktree of it, from a repo
           with another hooksPath value, and with TMPDIR INSIDE the repo: outputs byte-compared; the .git/config of every repo hashed around every run (positive control, empty-hash guard).
  siblings --clone CL --head H --base B --scratch S --out DIR   preflight_deps.test.sh with the base script and with the head script (FULL outputs byte-compared); it plants a stub of the leg (its line 312).
  tamper   --pr 1450 --clone CL --head H --base B --scratch S --out DIR [--only T1,T2]   HEAD row (all green), CONTROL no-op row, then the rows: anchor EXACTLY ONCE, LANDED, run the suite, read
           which cells RED, RESTORE (sha). ALL-GREEN = a tamper no cell catches (a finding to rule).
  compose  --clone CL --head1450 H --base1450 B --develop D --comp-head-1444 H ... --scratch S --out DIR   the five PRs in a TEMP INDEX over D in orders A / B / C (code-only tree identical and equal
           to D + each PR's own non-doc paths), `git merge-tree --write-tree` per pair and per PR onto D.
  docs     (same args)  the two docs: each fragment against its PR's OWN base, textual merge-file of each PR alone onto D, KEEP-BOTH onto D in A / B / C and #1450 solo, a fragment COUNT of exactly 1,
           composed-minus-fragments == D byte for byte, html_docs_matrix on every composed tree, and a DROP-A-BLOCK control that html_docs_matrix does not see (gate81 G81-2) but the COUNT does.
  --selftest   (refuses unless TMPDIR is a canonical directory outside every repo)
rc 0 / 1 (a FAIL: plant not landed, restore failed, a prediction DIFFERS, a composition that does not compose) / 2 refused. NOT RUN is reported by name and is never a pass."""
import difflib, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate83 import K, PR, COMP, git, git_bytes, blob, req, opt, wgit, must_be_outside, extract, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
P50 = PR(1450)
DOCS = list(K['known_develop_overlap'])
SCRIPT, SUITE = P50['gate_script'], P50['suite']
EMPTY_SHA = 'e3b0c44298fc1c14'
CHECKOUT = K['checkout']
GENV = {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_AUTHOR_NAME': 'gate83', 'GIT_AUTHOR_EMAIL': 'x@x', 'GIT_COMMITTER_NAME': 'gate83', 'GIT_COMMITTER_EMAIL': 'x@x'}
REALGIT = '/usr/bin/git' if os.path.exists('/usr/bin/git') else shutil.which('git')
CELLRX = [('cell 1', r'^FAIL: the leg does not name the locks outside its four directories'), ('cell 2', r"^FAIL: no 'surface: 3 of 6 tracked' line"),
          ('cell 3', r'^FAIL: CONTROL clean run'), ('cell 4', r'^FAIL: CONTROL one-directory run'), ('cell 5', r'^FAIL: CONTROL failing lock')]
SURFACE_2 = 'surface: 3 of 6 tracked package-lock.json file(s) were installed by this leg'


def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
def blob_id(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


# ---------------- paths / repos ----------------
def in_repo(path):
    """True when `path` lies inside ANY git work tree (git rev-parse --show-toplevel succeeds there)."""
    d = path if os.path.isdir(path) else os.path.dirname(path)
    while d and not os.path.isdir(d): d = os.path.dirname(d)
    e = dict(os.environ); e.pop('GIT_DIR', None); e.pop('GIT_WORK_TREE', None)
    return subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, env=e).returncode == 0


def assert_not_in_repo(path, what):
    """[g83] a scratch tree inside a repo would put the suite's cwd / TMPDIR in someone's repo (gate82 H9); the gate's rule is a scratch OUTSIDE every repo."""
    if in_repo(path): raise SystemExit('REFUSED: %s %s is inside a git repository — use a scratch under /private/tmp outside every repo' % (what, path))


def canon_tmp(scratch):
    """a realpath-canonical TMPDIR under `scratch`, outside every repo and under !CODING never."""
    must_be_outside(scratch, 'scratch'); real = os.path.realpath(scratch)
    if real != os.path.abspath(scratch): raise SystemExit('REFUSED: scratch %s is not canonical (realpath %s): pass the realpath' % (scratch, real))
    assert_not_in_repo(real, 'scratch'); t = os.path.join(real, 'tmp'); os.makedirs(t, exist_ok=True); return t


def w(path, data):
    must_be_outside(path, 'write'); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))


def write_checked(root, rel, data):
    p = os.path.join(root, rel); must_be_outside(p, 'write'); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(data)
    if sha(open(p, 'rb').read()) != sha(data): raise SystemExit('PLANT NOT LANDED: %s' % rel)
    return p


def run(cmd, cwd=None, env=None, timeout=300, stdin=None, merge=False):
    """-> (rc, out, err, timed_out). The child runs in its OWN process group; a timeout kills the group. merge=True folds stderr into stdout (the test's own `2>&1`)."""
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.Popen(cmd, cwd=cwd, env=e, stdin=(subprocess.PIPE if stdin is not None else subprocess.DEVNULL), stdout=subprocess.PIPE,
                         stderr=(subprocess.STDOUT if merge else subprocess.PIPE), start_new_session=True)
    try:
        o, er = p.communicate(input=(stdin.encode() if stdin is not None else None), timeout=timeout); to = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); o, er = p.communicate(); to = True
    return p.returncode, o.decode('utf-8', 'replace'), (er or b'').decode('utf-8', 'replace'), to


def cgit(clone, args, env=None, inp=None):
    """plumbing in the KIT CLONE only (refuses a clone under !CODING); never the shared checkout."""
    must_be_outside(clone, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True, env=e, input=inp)
    return p.returncode, p.stdout, p.stderr.decode('utf-8', 'replace')


def sh_git(args, cwd=None):
    e = dict(os.environ); e.update(GENV); e.pop('GIT_DIR', None); e.pop('GIT_WORK_TREE', None); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['git'] + list(args), capture_output=True, text=True, cwd=cwd, env=e); return p.returncode, p.stdout.strip(), p.stderr.strip()


def apply_edits(src, edits):
    """returns the tampered text; refuses unless each anchor occurs EXACTLY ONCE in the (progressively edited) file."""
    out = src
    for a, b in edits:
        n = out.count(a)
        if n != 1: raise SystemExit('ANCHOR %r occurs %d time(s) (want 1) — the tamper is NOT applied' % (a[:70], n))
        out = out.replace(a, b)
    return out


def landed(before, after, edits):
    return sha(before.encode()) != sha(after.encode()) and all(b in after for _, b in edits if b)


def existing(clone, rev, cands):
    return [c for c in cands if git(clone, 'ls-tree', rev, '--', c).strip()]


SMALL_PATHS = ['Blockchain/Dev/scripts', 'systemTest/__tests__', '.githooks'] + DOCS
DEV_PATHS = ['Blockchain/Dev', 'systemTest/__tests__', 'systemTest/scripts', 'systemTest/slot-target.sh', 'systemTest/run-in-slot.sh', '.githooks', '.github', 'observability', 'Projects Documents']


def tree_for(clone, rev, dest, paths=None):
    """extract the paths the shell legs need into `dest` (NOT inside a repo)."""
    assert_not_in_repo(os.path.dirname(dest.rstrip('/')) or dest, 'tree parent')
    if os.path.exists(dest): raise SystemExit('REFUSED: %s exists (a fresh tree each time)' % dest)
    extract(clone, rev, existing(clone, rev, paths or SMALL_PATHS), dest)
    assert_not_in_repo(dest, 'extracted tree')
    return dest


def cfg_hash(path):
    b = open(path, 'rb').read() if os.path.isfile(path) else b''
    h = hashlib.sha256(b).hexdigest()[:16]
    if h == EMPTY_SHA or not b: raise SystemExit('REFUSED: the config at %s is empty or absent (hash %s is the EMPTY-string hash: a check on it could not fail)' % (path, h))
    return h


def wed_config():
    gd = subprocess.run(['git', '-C', HERE, 'rev-parse', '--git-common-dir'], capture_output=True, text=True).stdout.strip()
    gd = gd if os.path.isabs(gd) else os.path.join(HERE, gd)
    return os.path.join(os.path.realpath(gd), 'config')


def kit_clone_config(clone):
    return os.path.join(clone, '.git', 'config') if os.path.isdir(os.path.join(clone, '.git')) else os.path.join(clone, 'config')


def shared_config():
    return os.path.join(CHECKOUT, '.git', 'config')


class Bracket:
    """the .git/config hashes of the shared checkout, the repo that CONTAINS this kit and the kit clone, taken before and after a leg of work."""
    def __init__(self, clone):
        self.cfgs = [('shared checkout', shared_config()), ('repo containing this kit', wed_config()), ('kit clone', kit_clone_config(clone))]
        self.before = dict((n, cfg_hash(p)) for n, p in self.cfgs)
    def close(self):
        after = dict((n, cfg_hash(p)) for n, p in self.cfgs)
        same = after == self.before
        print('CONFIG HASHES (sha256/16) %s : %s' % ('; '.join('%s %s -> %s' % (n, self.before[n], after[n]) for n, _ in self.cfgs), 'ALL UNCHANGED' if same else 'CHANGED'))
        return same


def pcounts(text):
    m = re.search(r'(\d+) passed, (\d+) failed', text); return (int(m.group(1)), int(m.group(2))) if m else None


def red_cells(out):
    return sorted(c for c, rx in CELLRX if re.search(rx, out, re.M))


def parse_surface(out):
    """-> dict(covered, total, outside_n, listed[], msg) from a leg's output, or None when there is no surface line."""
    m = re.search(r'(?m)^  surface: (\d+) of (\d+) tracked package-lock\.json file\(s\) were installed by this leg$', out)
    msg = re.search(r'(?m)^  surface: not a git checkout.*$', out)
    if not m and not msg: return None
    d = {'msg': msg.group(0).strip() if msg else None, 'covered': int(m.group(1)) if m else None, 'total': int(m.group(2)) if m else None, 'outside_n': None, 'listed': []}
    h = re.search(r'(?m)^  NOT installed by this leg \((\d+)\):$', out)
    if h:
        d['outside_n'] = int(h.group(1)); tail = out[h.end():].split('\n')
        for l in tail:
            if l.startswith('    ') and l.strip().endswith('package-lock.json'): d['listed'].append(l.strip())
            elif l.strip(): break
    return d


# ---------------- the leg under stubs ----------------
def write_exec(path, text):
    w(path, text); os.chmod(path, 0o755)


def make_pathdir(d, node='24', git_mode=None, docker=None):
    """a private PATH directory: node answers `node` for any call; npm succeeds unless the cwd holds FAIL_ME; git_mode None = no git stub (real /usr/bin/git),
    'S1' fails on every call, 'S2' fails when an argument is --show-prefix, 'S3' fails when an argument is ls-files, 'LOG' only logs; docker None = absent, 'down' = exits 1."""
    must_be_outside(d, 'stub dir'); os.makedirs(d)
    write_exec(os.path.join(d, 'node'), '#!/bin/sh\necho %s\n' % node)
    write_exec(os.path.join(d, 'npm'), '#!/bin/sh\n[ -e FAIL_ME ] && exit 1\nexit 0\n')
    log = os.path.join(d, 'git.calls.log')
    if git_mode:
        body = {'S1': 'exit 1\n',
                'S2': 'for a in "$@"; do [ "$a" = "--show-prefix" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
                'S3': 'for a in "$@"; do [ "$a" = "ls-files" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
                'LOG': 'exec %s "$@"\n' % REALGIT}[git_mode]
        write_exec(os.path.join(d, 'git'), '#!/bin/sh\necho "$*" >> "%s"\n%s' % (log, body))
    if docker: write_exec(os.path.join(d, 'docker'), '#!/bin/sh\nexit 1\n')
    return d, log


def build_leg_repo(root, script_bytes, init=True, locks=True):
    """the test's scratch layout: three locks inside the leg's four directories, three outside; `init` makes it a git repo and tracks everything."""
    must_be_outside(root, 'leg repo'); dev = os.path.join(root, 'Blockchain', 'Dev')
    for d in ('scripts/preflight', 'services/a', 'packages/p', 'frontend', 'connectors/wa'): os.makedirs(os.path.join(dev, d), exist_ok=True)
    os.makedirs(os.path.join(root, 'systemTest', 'akto'), exist_ok=True)
    sp = os.path.join(dev, 'scripts', 'preflight', 'lockfile-cleanroom.sh'); w(sp, script_bytes)
    w(os.path.join(dev, 'frontend', '.keep'), b'')
    if locks:
        for l in (os.path.join(dev, 'services', 'a'), os.path.join(dev, 'packages', 'p'), os.path.join(dev, 'scripts', 'preflight'), os.path.join(dev, 'connectors', 'wa'), dev, os.path.join(root, 'systemTest', 'akto')):
            w(os.path.join(l, 'package-lock.json'), b'{}\n')
    if init:
        assert sh_git(['init', '-q', root])[0] == 0 and sh_git(['-C', root, 'add', '-A'])[0] == 0
    return sp


def run_leg(script, pathdir, cwd, args=(), env=None, bash='/bin/bash', timeout=120):
    e = {'PATH': pathdir + ':/usr/bin:/bin'}; e.update(GENV); e.update(env or {})
    rc, o, er, to = run([bash, script] + list(args), cwd=cwd, env=e, timeout=timeout, merge=True)
    return rc, o, to


def function_text(src, name):
    ls = src.split('\n'); s = [i for i, l in enumerate(ls) if l.startswith(name + '() {')]
    if len(s) != 1: raise SystemExit('function %s defined %d times' % (name, len(s)))
    e = next(i for i in range(s[0] + 1, len(ls)) if ls[i] == '}')
    return '\n'.join(ls[s[0]:e + 1]) + '\n'


# ---------------- shells ----------------
def shells_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch)
    ctl = in_repo(HERE)
    print('%s scratch %s is canonical and NOT inside a repo (asserted); CONTROL: the kit dir %s IS inside a repo: %s' % (now(), scratch, HERE, ctl))
    if not ctl: print('FAIL the in-repo control did not fire'); return 1
    br = Bracket(clone); stamp = '%d' % int(time.time())
    th = tree_for(clone, head, os.path.join(scratch, 'tree_head_' + stamp)); tb = tree_for(clone, base, os.path.join(scratch, 'tree_base_' + stamp))
    s_head, s_base = git_bytes(clone, head, SCRIPT), git_bytes(clone, base, SCRIPT)
    mode = os.stat(os.path.join(th, SCRIPT)).st_mode
    arms = [('A', 'head script, head suite', s_head, (5, 0), 0, []), ('B', 'BASE script planted, head suite', s_base, (3, 2), 1, ['cell 1', 'cell 2'])]
    for aid, lab, data, want, wrc, wred in arms:
        write_checked(th, SCRIPT, data); os.chmod(os.path.join(th, SCRIPT), mode)
        rc, o, e, to = run(['/bin/bash', os.path.join(th, SUITE)], cwd=scratch, env={'TMPDIR': tmp}, merge=True)
        c = pcounts(o); reds = red_cells(o); nfail = len(re.findall(r'(?m)^FAIL:', o)); npass = len(re.findall(r'(?m)^PASS:', o))
        w(os.path.join(out, 'shell1450_%s.out' % aid), o)
        ok = c == want and rc == wrc and reds == wred and (npass, nfail) == want
        print('%s ARM %s (%s): rc %d%s summary-line counts %s | own PASS/FAIL line count (%d, %d) | red cells %s | want %s rc %s red %s -> %s | output %d B sha256/16 %s | plant sha256/16 %s' % (
            now(), aid, lab, rc, ' TIMEOUT' if to else '', c, npass, nfail, reds, want, wrc, wred, 'MATCH' if ok else 'DIFFER', len(o.encode()), sha(o.encode())[:16], sha(data)[:16]))
        if not ok: rc_all = 1
    write_checked(th, SCRIPT, s_head); os.chmod(os.path.join(th, SCRIPT), mode)
    back = sha(open(os.path.join(th, SCRIPT), 'rb').read()) == sha(s_head)
    print('%s restored the head script by sha: %s (blob %s)' % (now(), back, blob_id(s_head)[:12]))
    if not back: rc_all = 1
    lists = {}
    for lab, tr in (('base', tb), ('head', th)):
        rc, o, e, to = run(['/bin/bash', os.path.join(tr, 'Blockchain/Dev/scripts/run-shell-suites.sh'), '--list'], cwd=scratch, env={'TMPDIR': tmp})
        ls = [l for l in o.split('\n') if l.strip()]; lists[lab] = ls
        print('%s run-shell-suites.sh --list at the %s tree: rc %d, %d line(s) (PR body: 74 -> 75; the new suite listed: %s)' % (now(), lab, rc, len(ls), os.path.basename(SUITE) in o))
        w(os.path.join(out, 'list_%s.txt' % lab), o)
    added = sorted(set(lists['head']) - set(lists['base'])); removed = sorted(set(lists['base']) - set(lists['head']))
    print('%s --list head minus base: +%s -%s' % (now(), [os.path.basename(x) for x in added], removed))
    if not (len(lists['base']) == 74 and len(lists['head']) == 75 and len(added) == 1 and not removed): rc_all = 1
    rc, o, e, to = run(['/bin/bash', os.path.join(th, K['docs_composition']['matrix_suite'])], cwd=scratch, env={'TMPDIR': tmp}, merge=True)
    inval = 'is missing' in o; c = pcounts(o)
    print('%s html_docs_matrix at the head tree: rc %d counts %s (PR body: 12/0)%s' % (now(), rc, c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
    w(os.path.join(out, 'matrix_head.out'), o)
    if inval or c != (12, 0): rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- payload ----------------
def payload_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    canon_tmp(scratch); sp = K['spark']['patch']; stamp = '%d' % int(time.time())
    if not os.path.isfile(sp): print('NOT RUN: %s is not readable' % sp); return 1
    d = os.path.join(scratch, 'payload_' + stamp); assert_not_in_repo(scratch, 'scratch')
    extract(clone, base, [SCRIPT], d)
    assert_not_in_repo(d, 'payload tree')
    rc, o, e, to = run(['git', 'apply', '--check', '-p1', sp], cwd=d); print('%s git apply --check -p1 patch.diff in %s (outside every repo): rc %d %s' % (now(), d, rc, (o + e).strip()[:120]))
    if rc: return 1
    rc, o, e, to = run(['git', 'apply', '-p1', sp], cwd=d); print('%s git apply -p1: rc %d %s' % (now(), rc, (o + e).strip()[:120]))
    if rc: return 1
    bs = open(os.path.join(d, SCRIPT), 'rb').read(); bt = open(os.path.join(d, SUITE), 'rb').read()
    hs, ht = git_bytes(clone, head, SCRIPT), git_bytes(clone, head, SUITE)
    print('%s applied script blob %s == head %s: %s | applied test blob %s == head %s: %s | the READY names 4948fe691609 / 5caa1b750fa3' % (
        now(), blob_id(bs)[:12], blob_id(hs)[:12], bs == hs, blob_id(bt)[:12], blob_id(ht)[:12], bt == ht))
    if bs != hs or bt != ht: rc_all = 1
    rc2, o2, e2, to2 = run(['git', 'apply', '--check', '-p1', sp], cwd=d)
    print('%s CONTROL: the same patch applied a SECOND time must be refused (rc != 0): rc %d' % (now(), rc2))
    if rc2 == 0: rc_all = 1
    ts = git_bytes(clone, head, SUITE).decode().split('\n')
    return rc_all


# ---------------- stubs (F1 / F2 / F5) ----------------
STUB_PREDICT = {   # kit-builder PREDICTIONS, written from the reading of the function before any run (F 10th's STATUS/READY give the same numbers)
    'U':  dict(rc=0, covered=3, total=6, outside=3, msg=False),
    'S1': dict(rc=0, covered=None, total=None, outside=None, msg=True),
    'S2': dict(rc=0, covered=0, total=6, outside=6, msg=False),
    'S3': dict(rc=0, covered=0, total=0, outside=None, msg=False),
    'R':  dict(rc=0, covered=None, total=None, outside=None, msg=True),
}


def stubs_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); br = Bracket(clone); stamp = '%d' % int(time.time())
    s_head, s_base = git_bytes(clone, head, SCRIPT), git_bytes(clone, base, SCRIPT)
    print('%s shell: /bin/bash is %s; real git on the leg PATH: %s' % (now(), run(['/bin/bash', '--version'])[1].split('\n')[0], REALGIT))
    variants = [('U', None, True), ('S1', 'S1', True), ('S2', 'S2', True), ('S3', 'S3', True), ('R', None, False)]
    results = {}
    for tag, gm, init in variants:
        for which, sb in (('head', s_head), ('base', s_base)):
            root = os.path.join(scratch, 'leg_%s_%s_%s' % (tag, which, stamp)); sp = build_leg_repo(root, sb, init=init)
            pd, log = make_pathdir(os.path.join(scratch, 'path_%s_%s_%s' % (tag, which, stamp)), git_mode=gm or ('LOG' if which == 'head' else None))
            rc, o, to = run_leg(sp, pd, root)
            calls = open(log).read().split('\n') if os.path.exists(log) else []
            calls = [c for c in calls if c]
            results[(tag, which)] = (rc, o, calls)
            w(os.path.join(out, 'leg_%s_%s.out' % (tag, which)), o)
    for tag, gm, init in variants:
        rc, o, calls = results[(tag, 'head')]; s = parse_surface(o); pr = STUB_PREDICT[tag]
        brc, bo, bcalls = results[(tag, 'base')]
        got = dict(rc=rc, covered=s and s['covered'], total=s and s['total'], outside=s and s['outside_n'], msg=bool(s and s['msg']))
        match = got == pr
        eff = ''
        if gm:
            hit = [c for c in calls if (gm == 'S2' and '--show-prefix' in c) or (gm == 'S3' and 'ls-files' in c) or gm == 'S1']
            eff = ' | STUB TOOK EFFECT: %d logged git call(s), %d of them the failing one (%s)' % (len(calls), len(hit), (hit or ['NONE'])[0][:50])
            if not hit: match = False
        base_surface = parse_surface(bo)
        print('%s VARIANT %-2s head: rc %d (unstubbed rc %d) | surface line: %s | listed %s%s | predicted %s -> %s | base script: rc %d, surface lines %s | exit code equals the unstubbed run: %s' % (
            now(), tag, rc, results[('U', 'head')][0], (('%s of %s' % (s['covered'], s['total'])) if s and s['covered'] is not None else (s['msg'] if s else 'NONE')),
            (s['listed'] if s else []), eff, pr, 'MATCH' if match else 'DIFFER', brc, base_surface, rc == results[('U', 'head')][0] and brc == rc))
        if not match or brc != rc or base_surface is not None: rc_all = 1
        if tag in ('S2', 'S3'):
            print('      F1 FINDING (measured): with git PARTLY failing the leg exits %d and prints `%s` while the truth is %s: a WRONG NUMBER on a screen that exists to be honest; the three stub variants and the no-.git run all exit like the unstubbed run' % (
                rc, ('surface: %s of %s' % (s['covered'], s['total'])) if s else '??', 'surface: 3 of 6, 3 listed'))
    # the advisory SKIP path (a dev laptop with node < 24 and Docker down): the surface is NEVER printed there
    root = os.path.join(scratch, 'leg_skip_%s' % stamp); sp = build_leg_repo(root, s_head); pd, _ = make_pathdir(os.path.join(scratch, 'path_skip_%s' % stamp), node='18', docker='down')
    rc, o, to = run_leg(sp, pd, root); s = parse_surface(o); w(os.path.join(out, 'leg_advisory_skip.out'), o)
    print('%s ADVISORY-SKIP path (node stub answers 18, docker stub exits 1): rc %d | `SKIP (advisory)` printed: %s | surface lines: %s -> the surface is printed only on an all-OK run (c2 F3 measured the exit order)' % (now(), rc, 'SKIP (advisory)' in o, s))
    if not (rc == 0 and 'SKIP (advisory)' in o and s is None): rc_all = 1
    # F2: zero locks in the four directories, bash 3.2.57
    for which, sb in (('base', s_base), ('head', s_head)):
        root = os.path.join(scratch, 'leg_zero_%s_%s' % (which, stamp)); sp = build_leg_repo(root, sb, locks=False); pd, _ = make_pathdir(os.path.join(scratch, 'path_zero_%s_%s' % (which, stamp)))
        rc, o, to = run_leg(sp, pd, root); w(os.path.join(out, 'leg_zero_%s.out' % which), o)
        ub = 'unbound variable' in o; fn = 'DIRS[@]' in o
        print('%s F2 ZERO-LOCK corpus, %s script, /bin/bash 3.2.57, no arguments: rc %d | `unbound variable` %s | names DIRS[@] %s | surface lines %s | first line %r' % (
            now(), which, rc, ub, fn, parse_surface(o), (o.strip().split('\n') or [''])[0][:90]))
        if not (rc == 1 and ub and fn and parse_surface(o) is None): rc_all = 1
    hb = shutil.which('bash', path='/opt/homebrew/bin:/usr/local/bin')
    print('%s F2 on a bash >= 4: %s' % (now(), 'NOT RUN (no Homebrew bash on this host: /opt/homebrew/bin/bash absent)' if not hb else 'available at %s (NOT RUN by this kit)' % hb))
    # F2b: the EXTRACTED function with an empty CHECKED, and the unguarded-expansion control
    fn_src = function_text(s_head.decode(), 'report_surface')
    root = os.path.join(scratch, 'leg_fn_%s' % stamp); build_leg_repo(root, s_head)
    devdir = os.path.join(root, 'Blockchain', 'Dev')
    guard = '${CHECKED[@]+"${CHECKED[@]}"}'
    for lab, src in (('GUARDED (as committed)', fn_src), ('CONTROL unguarded `"${CHECKED[@]}"`', fn_src.replace(guard, '"${CHECKED[@]}"'))):
        if lab.startswith('CONTROL') and fn_src.count(guard) != 1: print('FAIL the guard text occurs %d times' % fn_src.count(guard)); rc_all = 1; continue
        if lab.startswith('CONTROL') and src == fn_src: print('FAIL the control plant did not land'); rc_all = 1; continue
        drv = os.path.join(scratch, 'fn_driver_%s_%s.sh' % (lab[:5].strip().replace(' ', '_'), stamp))
        w(drv, 'set -uo pipefail\nCHECKED=()\n%s\ncd "%s"\nreport_surface\necho "report_surface rc=$?"\n' % (src, devdir))
        rc, o, to = run_leg(drv, make_pathdir(os.path.join(scratch, 'path_fn_%s_%s' % (lab[:5].strip().replace(' ', '_'), stamp)), git_mode='LOG')[0], scratch)
        s = parse_surface(o); ub = 'unbound variable' in o
        print('%s F2b EXTRACTED report_surface, EMPTY CHECKED, set -u, bash 3.2.57, %s: driver rc %d | surface %s | unbound variable: %s | tail %r' % (
            now(), lab, rc, ('%s of %s' % (s['covered'], s['total'])) if s and s['covered'] is not None else s, ub, o.strip().split('\n')[-1][:70]))
        if lab.startswith('GUARDED') and not (rc == 0 and s and s['covered'] == 0 and s['total'] == 6 and not ub and 'report_surface rc=0' in o): rc_all = 1
        if lab.startswith('CONTROL') and not (rc != 0 and ub): rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- realtree (COMPUTED) ----------------
def realtree_cmd(clone, head, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); stamp = '%d' % int(time.time())
    names = [l for l in git(clone, 'ls-tree', '-r', '--name-only', head).split('\n') if l.endswith('package-lock.json')]
    tracked = len(names)
    # the leg's own discovery, run by `find` over the EXTRACTED lock files (tracked files only: node_modules locks are untracked, and maxdepth 2 never reaches them)
    lt = os.path.join(scratch, 'locks_%s' % stamp); extract(clone, head, names, lt); assert_not_in_repo(lt, 'lock tree')
    dev = os.path.join(lt, 'Blockchain', 'Dev')
    rc, o, e, to = run(['/usr/bin/find', 'services', 'packages', 'frontend', 'scripts', '-maxdepth', '2', '-name', 'package-lock.json'], cwd=dev)
    found = sorted(l for l in o.split('\n') if l.strip())
    print('%s REAL TREE (COMPUTED, the leg is NOT run on it): head %s tracks %d package-lock.json files (ls-tree; kit %d); the leg\'s `find services packages frontend scripts -maxdepth 2 -name package-lock.json` over those files reaches %d (kit %d); outside: %d (kit %d); find rc %d, stderr %r' % (
        now(), head[:12], tracked, P50['real_tree']['tracked_locks'], len(found), P50['real_tree']['find_reaches'], tracked - len(found), P50['real_tree']['listed'], rc, e[:80]))
    if tracked != P50['real_tree']['tracked_locks'] or len(found) != P50['real_tree']['find_reaches']: rc_all = 1
    # CONTROL: the same find over a dir with no locks reads 0
    emp = os.path.join(scratch, 'empty_%s' % stamp); os.makedirs(os.path.join(emp, 'services'))
    print('%s CONTROL: the same find over an empty services/ dir reads %d line(s) (must be 0)' % (now(), len([l for l in run(['/usr/bin/find', 'services', '-maxdepth', '2', '-name', 'package-lock.json'], cwd=emp)[1].split('\n') if l.strip()])))
    # MODELLED run: the EXTRACTED report_surface in a scratch repo that TRACKS those 45 paths, CHECKED = the 35 dirs
    root = os.path.join(scratch, 'real45_%s' % stamp); os.makedirs(root)
    for n in names: w(os.path.join(root, n), b'{}\n')
    assert sh_git(['init', '-q', root])[0] == 0 and sh_git(['-C', root, 'add', '-A'])[0] == 0
    fn_src = function_text(git_bytes(clone, head, SCRIPT).decode(), 'report_surface')
    dirs = ' '.join('"%s"' % os.path.dirname(x) for x in found)
    drv = os.path.join(scratch, 'real45_driver_%s.sh' % stamp)
    w(drv, 'set -uo pipefail\nCHECKED=(%s)\n%s\ncd "%s"\nreport_surface\necho "report_surface rc=$?"\n' % (dirs, fn_src, os.path.join(root, 'Blockchain', 'Dev')))
    rc, o, to = run_leg(drv, make_pathdir(os.path.join(scratch, 'path_real45_%s' % stamp))[0], scratch); w(os.path.join(out, 'realtree_surface.out'), o)
    s = parse_surface(o)
    print('%s MODELLED output of report_surface over the 45 tracked paths with CHECKED = the 35 dirs (assumes all 35 pass): rc %d | %s' % (now(), rc, o.strip().replace('\n', ' | ')[:900]))
    want_out = sorted(set(names) - set('Blockchain/Dev/' + x for x in found))
    ok = s and s['covered'] == 35 and s['total'] == 45 and s['outside_n'] == 10 and sorted(s['listed']) == want_out
    print('%s PREDICTION `surface: 35 of 45` listing 10: %s | the 10 listed: %s' % (now(), 'MATCH' if ok else 'DIFFER', want_out))
    if not ok: rc_all = 1
    return rc_all


# ---------------- cwd (Q-CWD1426) ----------------
def make_repo(path, hooks, with_hooks_dir=True):
    must_be_outside(path, 'repo'); os.makedirs(path)
    assert sh_git(['init', '-q', path])[0] == 0
    if with_hooks_dir:
        os.makedirs(os.path.join(path, '.githooks')); open(os.path.join(path, '.githooks', '.keep'), 'w').write('x\n')
    open(os.path.join(path, 'f'), 'w').write('x\n')
    assert sh_git(['-C', path, 'add', '-A'])[0] == 0 and sh_git(['-C', path, 'commit', '-q', '-m', 'init'])[0] == 0
    if hooks is not None: assert sh_git(['-C', path, 'config', 'core.hooksPath', hooks])[0] == 0
    return path


def cwd_cmd(clone, head, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); br = Bracket(clone); stamp = '%d' % int(time.time())
    th = tree_for(clone, head, os.path.join(scratch, 'cwd_tree_' + stamp)); suite = os.path.join(th, SUITE)
    # instrument controls
    rctl = make_repo(os.path.join(scratch, 'cwd_ctl_' + stamp), None); cfg = os.path.join(rctl, '.git', 'config'); c0 = cfg_hash(cfg)
    sh_git(['-C', rctl, 'config', 'core.hooksPath', 'zz']); c1 = cfg_hash(cfg)
    print('%s INSTRUMENT CONTROL: a direct `git config core.hooksPath zz` changes the hash %s -> %s (reads CHANGED: %s); the empty-string hash %s is refused' % (now(), c0, c1, c0 != c1, EMPTY_SHA))
    if c0 == c1: return 1
    try: cfg_hash(os.path.join(scratch, 'no-such-config')); print('FAIL the empty-hash guard did not fire'); return 1
    except SystemExit: print('  the empty-hash guard fired on an absent config (OK)')
    plain = os.path.join(scratch, 'cwd_plain_' + stamp); os.makedirs(plain); assert_not_in_repo(plain, 'plain cwd')
    arms = []
    r_unset = make_repo(os.path.join(scratch, 'cwd_unset_' + stamp), None); r_custom = make_repo(os.path.join(scratch, 'cwd_custom_' + stamp), 'custom/hooks'); r_tmp = make_repo(os.path.join(scratch, 'cwd_tmpin_' + stamp), None)
    wtp = os.path.join(scratch, 'cwd_wt_' + stamp); assert sh_git(['-C', r_unset, 'worktree', 'add', '-q', '--detach', wtp])[0] == 0
    arms = [('C0', 'cwd = a directory that is NOT in any repo', plain, None, tmp), ('C1', 'cwd = a scratch repo with .githooks, core.hooksPath UNSET', r_unset, r_unset, tmp),
            ('C2', 'cwd = a WORKTREE of that repo (the main repo\'s config is hashed)', wtp, r_unset, tmp), ('C3', 'cwd = a repo with core.hooksPath = custom/hooks', r_custom, r_custom, tmp),
            ('C4', 'cwd = a repo, and TMPDIR INSIDE it (the F 10th UNMEASURED case; gate82 H9 shape)', r_tmp, r_tmp, os.path.join(r_tmp, 'tmp'))]
    outs = {}
    for aid, label, cwd, repo, td in arms:
        os.makedirs(td, exist_ok=True)
        before = cfg_hash(os.path.join(repo, '.git', 'config')) if repo else None
        st0 = sh_git(['-C', repo, 'status', '--porcelain'])[1] if repo else None
        rc, o, e, to = run(['/bin/bash', suite], cwd=cwd, env=dict(GENV, TMPDIR=td), merge=True)
        after = cfg_hash(os.path.join(repo, '.git', 'config')) if repo else None
        st1 = sh_git(['-C', repo, 'status', '--porcelain'])[1] if repo else None
        outs[aid] = (rc, o); w(os.path.join(out, 'cwd_%s.out' % aid), o)
        print('%s ARM %s %-86s rc %d counts %s | output %d B sha256/16 %s | repo .git/config %s -> %s : %s | repo `status --porcelain` %s -> %s' % (
            now(), aid, label, rc, pcounts(o), len(o.encode()), sha(o.encode())[:16], before, after, ('UNCHANGED' if before == after else 'CHANGED') if repo else 'n/a (no repo)', (st0 or '')[:30] or '(clean)', (st1 or '')[:30] or '(clean)'))
        if rc != 0 or pcounts(o) != (5, 0) or (repo and before != after) or st0 != st1: rc_all = 1
    same = len(set(sha(v[1].encode()) for v in outs.values())) == 1
    print('%s Q-CWD1426: FULL outputs of the 5 arms (stdout+stderr, rc folded) byte-identical: %s (%d distinct) | the F 10th READY reads 506 B red / 404 B green from a non-repo cwd and the worktree' % (now(), same, len(set(sha(v[1].encode()) for v in outs.values()))))
    if not same: rc_all = 1
    print('%s NOTE: this suite names neither bootstrap-env.sh nor env.example nor hooksPath (c2 F7), so the gate82 H9 hazard (a TMPDIR inside a repo makes bootstrap-env.sh WRITE that repo\'s core.hooksPath) does not apply to it; the arms above MEASURE that rather than assume it.' % now())
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- siblings ----------------
def siblings_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); br = Bracket(clone); stamp = '%d' % int(time.time())
    td = tree_for(clone, head, os.path.join(scratch, 'sib_tree_' + stamp), DEV_PATHS)
    sib = P50['siblings'][0]; s_head, s_base = git_bytes(clone, head, SCRIPT), git_bytes(clone, base, SCRIPT)
    st = git_bytes(clone, head, sib).decode()
    plants = [l.strip() for l in st.split('\n') if 'lockfile-cleanroom.sh' in l]
    print('%s the sibling %s mentions the leg on %d line(s): %s -> it PLANTS a stub of the leg (`exit 0`) rather than running the changed code: WEAK EVIDENCE, said before any count' % (now(), os.path.basename(sib), len(plants), [p[:100] for p in plants]))
    if not (len(plants) == 1 and 'exit 0' in plants[0] and '> "$dev/scripts/preflight/lockfile-cleanroom.sh"' in plants[0]): rc_all = 1
    res = {}
    for lab, data in (('base', s_base), ('head', s_head)):
        write_checked(td, SCRIPT, data)
        rc, o, e, to = run(['/bin/bash', os.path.join(td, sib)], cwd=scratch, env={'TMPDIR': tmp}, timeout=600, merge=True)
        res[lab] = (rc, o); w(os.path.join(out, 'sibling_%s.out' % lab), o)
        print('%s SIBLING %-4s %s: rc %d%s counts %s | FULL output %d B sha256/16 %s | script blob %s' % (now(), lab, os.path.basename(sib), rc, ' TIMEOUT' if to else '', pcounts(o) or re.findall(r'(\d+) passed, (\d+) failed', o)[-1:], len(o.encode()), sha(o.encode())[:16], blob_id(data)[:12]))
    write_checked(td, SCRIPT, s_head)
    eq = res['base'][1] == res['head'][1]
    dl = [l for l in difflib.unified_diff(res['base'][1].split('\n'), res['head'][1].split('\n'), lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
    print('%s SIBLING base vs head: counts equal %s | FULL outputs byte-identical %s (%d differing line(s): %s) | READY: 56/0 before and after, identical output' % (now(), pcounts(res['base'][1]) == pcounts(res['head'][1]), eq, len(dl), dl[:3]))
    if not eq or res['head'][0] != 0 or res['base'][0] != 0: rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- tamper ----------------
H_CALL = '    report_surface\n'
TAMPER = {
 '1450': dict(rows=[
    ('T1', 'the call is removed (the function is never reached)', [('if [ "$#" -eq 0 ]; then\n    report_surface\nfi\n', '')], ['cell 1', 'cell 2']),
    ('T2', 'the call is no longer guarded by `$# -eq 0`: it runs on a one-directory run too', [('if [ "$#" -eq 0 ]; then\n    report_surface\nfi\n', 'report_surface\n')], ['cell 4']),
    ('T3', 'the surface line is reworded (no "tracked package-lock.json file(s) were installed by this leg")', [('echo "  surface: $covered_n of $total tracked package-lock.json file(s) were installed by this leg"', 'echo "  surface: $covered_n of $total locks"')], ['cell 2']),
    ('T4', 'the covered count is wrong (covered_n starts at 1: "4 of 6")', [('covered_n=0 total=0', 'covered_n=1 total=0')], ['cell 2']),
    ('T5', 'the branches are swapped: the COVERED locks are listed and the outside ones counted as covered ("3 of 6" still reads right)', [('            covered_n=$((covered_n + 1))\n        else\n            outside=$((outside + 1))\n            lines="$lines    $lock"$\'\\n\'', '            outside=$((outside + 1))\n            lines="$lines    $lock"$\'\\n\'\n        else\n            covered_n=$((covered_n + 1))')], ['cell 1']),
    ('T5b', 'the list names ALL six locks (covered ones too) under a heading that still says (3)', [('            covered_n=$((covered_n + 1))\n        else\n', '            covered_n=$((covered_n + 1)); lines="$lines    $lock"$\'\\n\'\n        else\n')], []),
    ('T6', 'the function ends in `return 1` instead of `return 0` (the leg exits 1 on an all-OK run)', [('    return 0\n}\n\nFAILED=()', '    return 1\n}\n\nFAILED=()')], ['cell 3']),
    ('T7', 'WORDING: the heading line "NOT installed by this leg" is dropped (the paths are still listed)', [('        echo "  NOT installed by this leg ($outside):"\n', '')], []),
    ('T8', 'WRONG COUNT in the heading: "NOT installed by this leg (99):" (the surface line stays right)', [('echo "  NOT installed by this leg ($outside):"', 'echo "  NOT installed by this leg (99):"')], []),
    ('T9', 'the early return on a non-git checkout becomes `return 1` (the leg exits 1 when it is not in a git checkout; no cell runs a non-git tree)', [('cannot list the tracked lockfiles this leg does not install"\n        return 0', 'cannot list the tracked lockfiles this leg does not install"\n        return 1')], []),
    ('T10', 'the guard on CHECKED is removed (the unguarded expansion): a clean run with a non-empty CHECKED is unaffected on bash 3.2', [('${CHECKED[@]+"${CHECKED[@]}"}', '"${CHECKED[@]}"')], []),
    ('T11', 'the surface prints on a FAILING run too (a call before the failing exit; cell 5 greps only the FAIL line and the absence of the pass line)', [('    done\n    exit 1\nfi\n', '    done\n    report_surface\n    exit 1\nfi\n')], []),
    ('T12', 'REGRESSION OF THE LEG ITSELF: the exit code of the failing path becomes `exit 0` (cell 5 must catch it)', [('    done\n    exit 1\nfi\n', '    done\n    exit 0\nfi\n')], ['cell 5']),
 ]),
}


def tamper_cmd(pr, clone, head, base, scratch, out, only):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    if pr not in TAMPER: raise SystemExit('REFUSED: --pr %r has no tamper table (1450)' % pr)
    tmp = canon_tmp(scratch); stamp = '%d' % int(time.time()); th = tree_for(clone, head, os.path.join(scratch, 'tm_tree_%s' % stamp))
    head_src = git_bytes(clone, head, SCRIPT).decode('utf-8'); mode = os.stat(os.path.join(th, SCRIPT)).st_mode
    rows = [('HEAD', 'no change (all green)', None, []), ('CONTROL', 'a no-op comment appended (all green)', 'NOOP', [])] + list(TAMPER[pr]['rows'])
    for tid, name, edits, pred in rows:
        if only and tid not in only and tid not in ('HEAD', 'CONTROL'): continue
        try:
            if edits is None: new = head_src
            elif edits == 'NOOP': new = head_src.rstrip('\n') + '\n# gate83-noop\n'
            else: new = apply_edits(head_src, edits)
        except SystemExit as e:
            print('%s %-8s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        ok_land = (new == head_src) if edits is None else (new != head_src and (edits == 'NOOP' or landed(head_src, new, edits)))
        write_checked(th, SCRIPT, new.encode('utf-8')); os.chmod(os.path.join(th, SCRIPT), mode)
        rc, o, e, to = run(['/bin/bash', os.path.join(th, SUITE)], cwd=scratch, env={'TMPDIR': tmp}, merge=True)
        c = pcounts(o); reds = red_cells(o)
        write_checked(th, SCRIPT, head_src.encode('utf-8')); back = sha(open(os.path.join(th, SCRIPT), 'rb').read()) == sha(head_src.encode())
        w(os.path.join(out, 'tamper_%s_%s.out' % (pr, tid)), o)
        if c is None: verdict = 'TAMPER-INVALID (no count: the suite did not run)'; rc_all = 1
        elif tid in ('HEAD', 'CONTROL'):
            good = c == (5, 0) and rc == 0; verdict = 'OK' if good else 'FAIL: %s rc %d' % (c, rc); rc_all |= 0 if good else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if c[1] == 0 else 'caught: %d failed (%s)' % (c[1], reds)) + ' | kit-builder prediction %s: %s' % (pred or 'ALL-GREEN', 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-110s landed %s restored %s | rc %d counts %s | %s' % (now(), tid, name[:110], ok_land, back, rc, c, verdict))
        if not ok_land or not back: rc_all = 1
        if tid not in ('HEAD', 'CONTROL') and c is not None and sorted(pred) != reds: rc_all = 1
    return rc_all


# ---------------- docs / compose (five PRs) ----------------
def insertion(basetxt, headtxt):
    la, lb = basetxt.split('\n'), headtxt.split('\n')
    ops = [x for x in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if x[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': raise SystemExit('not a pure insertion: %s' % ops[:3])
    _, i1, _, j1, j2 = ops[0]; return i1, lb[j1:j2]


def compose_keep_both(devtxt, frags):
    """frags: [fragment_lines] IN THE ORDER TO PLACE THEM; all are inserted immediately before the LAST `</body>` of `devtxt` (the develop the gate reads)."""
    la = devtxt.split('\n'); idx = [i for i, l in enumerate(la) if l.strip() == '</body>']
    if not idx: raise SystemExit('no </body> line in the develop doc')
    i = idx[-1]; return '\n'.join(la[:i] + [l for f in frags for l in f] + la[i:])


def flow_numbers(txt): return [int(x) for x in re.findall(r'<h2>(\d+)\.', txt)]


def merge_file(cur, basef, other):
    rc, o, e, to = run(['git', 'merge-file', '-p', '-L', 'ours', '-L', 'base', '-L', 'theirs', cur, basef, other], timeout=60)
    return rc, o


def all_prs(): return ['1450'] + sorted(K['companions'])


def pr_heads(A):
    h = {'1450': req(A, '--head1450', True)}
    for n in sorted(K['companions']): h[n] = req(A, '--comp-head-' + n, True)
    return h


def pr_bases(clone, develop, heads, base1450):
    """each PR's OWN base: #1450 the pinned parent; a companion its parent, or merge-base(develop, head) when the head merged develop in (#1444)."""
    b = {'1450': base1450}
    for n in sorted(K['companions']):
        c = COMP(n)
        if c['base_kind'].startswith('merge-base'):
            rc, o, e = cgit(clone, ['merge-base', develop, heads[n]]); b[n] = o.decode().strip()
            if rc or not b[n]: raise SystemExit('merge-base(develop, #%s head) failed: %s' % (n, e))
        else:
            b[n] = c['parents'][0]
    return b


def landed_set(clone, develop, heads, bases):
    """[g83] a COMPANION whose docs fragment is ALREADY in the develop doc has LANDED (a squash): composing its head again would put the block in twice. -> sorted list of ids.
    #1444 landed during the kit build (develop 40ed3573b491, the squash `KS-937: ...`). #1450 itself must NOT be landed (refused)."""
    d0 = git_bytes(clone, develop, DOCS[0]).decode('utf-8'); out = []
    for n in sorted(heads):
        for lab, sha_ in (('head', heads[n]), ('base', bases[n])):
            if not resolvable(clone, sha_): raise SystemExit('REFUSED: #%s %s %s is not in %s (fetch it BY SHA into YOUR clone): an unresolvable sha is never read as "not landed"' % (n, lab, sha_, clone))
        try: frag = insertion(git_bytes(clone, bases[n], DOCS[0]).decode('utf-8'), git_bytes(clone, heads[n], DOCS[0]).decode('utf-8'))[1]
        except SystemExit: continue   # present but NOT a pure insertion: cannot have landed as this block
        if '\n'.join(frag) in d0:
            if n == '1450': raise SystemExit('REFUSED: #1450\'s own docs fragment is ALREADY in develop %s (it has landed: nothing to gate)' % develop[:12])
            out.append(n)
    return out


def own_nondoc(clone, base, head):
    rc, o, e = cgit(clone, ['diff', '--name-only', base, head])
    if rc: raise SystemExit('git diff --name-only %s %s rc %d: %s (an unresolvable head / base can NOT read as "no paths")' % (base[:12], head[:12], rc, e.strip()[:120]))
    return sorted(x for x in o.decode().split('\n') if x and x not in DOCS)


def compose_tree(clone, develop, heads, bases, order, scratch, tag):
    """a TEMP INDEX tree of the whole composition in `order` over DEVELOP: every PR's own non-doc paths from its head (each asserted UNCHANGED between the PR's base and develop, else the
    head's blob would silently revert develop), the docs keep-both in `order`. -> dict(full, nodocs, docs). Writes objects into the KIT CLONE only."""
    idx = os.path.join(scratch, 'idx_%s_%d' % (tag, int(time.time() * 1000))); env = {'GIT_INDEX_FILE': idx}; must_be_outside(idx, 'temp index')
    rc, o, e = cgit(clone, ['read-tree', develop], env=env)
    if rc: raise SystemExit('read-tree: ' + e)
    def put(path, data, mode='100644'):
        rc, o, e = cgit(clone, ['hash-object', '-w', '--stdin'], inp=data)
        if rc: raise SystemExit('hash-object: ' + e)
        bid = o.decode().strip(); rc, o, e = cgit(clone, ['update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, bid, path)], env=env)
        if rc: raise SystemExit('update-index: ' + e)
        return bid
    moved = []
    for n in order:
        for path in own_nondoc(clone, bases[n], heads[n]):
            if blob(clone, bases[n], path) and blob(clone, bases[n], path) != blob(clone, develop, path): moved.append((n, path))
            m = [l.split()[0] for l in git(clone, 'ls-tree', heads[n], '--', path).strip().split('\n') if l][0]
            put(path, git_bytes(clone, heads[n], path), m)
    if moved: raise SystemExit('develop MOVED a path of a PR since its base: %s (the head blob would revert it)' % moved)
    docs_texts = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8')
        fr = [insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))[1] for n in order]
        docs_texts[d] = compose_keep_both(dv, fr); put(d, docs_texts[d].encode('utf-8'))
    rc, o, e = cgit(clone, ['write-tree'], env=env)
    if rc: raise SystemExit('write-tree: ' + e)
    full = o.decode().strip()
    for d in DOCS:
        bid = cgit(clone, ['rev-parse', '%s:%s' % (develop, d)])[1].decode().strip(); cgit(clone, ['update-index', '--cacheinfo', '100644,%s,%s' % (bid, d)], env=env)
    rc, o, e = cgit(clone, ['write-tree'], env=env); nodocs = o.decode().strip()
    return dict(full=full, nodocs=nodocs, docs=docs_texts)


def compose_cmd(clone, develop, heads, bases, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); os.makedirs(scratch, exist_ok=True); rc_all = 0
    landed = landed_set(clone, develop, heads, bases); live = [n for n in all_prs() if n not in landed]
    print('%s LANDED companions (their docs fragment is already in develop %s; excluded from the orders, NOT counted as composed): %s | live PRs %s' % (now(), develop[:12], landed or 'NONE', live))
    print('%s COMPOSITION over develop %s: #1450 and the four companions (%s): the code paths are DISJOINT (c1 companions P13); the proof: a temp-index tree per order, the code-only tree identical across orders and equal to develop + each PR\'s own non-doc paths; bases %s' % (
        now(), develop[:12], ', '.join('#' + n for n in sorted(K['companions'])), dict((n, b[:12]) for n, b in bases.items())))
    trees = {}
    for tag in ('A', 'B', 'C'):
        order = [n for n in K['compose_orders'][tag] if n not in landed]
        try:
            t = compose_tree(clone, develop, heads, bases, order, scratch, tag); trees[tag] = t
            print('  TEMP-INDEX TREE order %s (%s): FULL %s | CODE-ONLY (docs reset to develop) %s' % (tag, ' -> '.join('#' + n for n in order), t['full'], t['nodocs']))
        except SystemExit as e:
            print('  TEMP-INDEX TREE order %s: %s' % (tag, e)); rc_all = 1
    if len(trees) == 3:
        same = len({t['nodocs'] for t in trees.values()}) == 1; nfull = len({t['full'] for t in trees.values()})
        print('  CODE-ONLY tree IDENTICAL across orders A / B / C: %s (%s) | FULL trees differ only by the docs order: %d distinct of 3' % (same, trees['A']['nodocs'][:12], nfull)); rc_all |= 0 if same else 1
        want = sorted(set(p for n in live for p in own_nondoc(clone, bases[n], heads[n])))
        rc, o, e = cgit(clone, ['diff', '--name-only', develop, trees['A']['nodocs']])
        got = sorted(x for x in o.decode().split('\n') if x)
        print('  develop..CODE-ONLY-tree paths == the union of the five PRs\' own non-doc paths: %s (%d paths) %s' % (got == want, len(got), '' if got == want else sorted(set(got) ^ set(want))))
        rc_all |= 0 if got == want else 1
        for n in live:
            for p in own_nondoc(clone, bases[n], heads[n]):
                a = cgit(clone, ['rev-parse', '%s:%s' % (trees['A']['nodocs'], p)])[1].decode().strip(); b = cgit(clone, ['rev-parse', '%s:%s' % (heads[n], p)])[1].decode().strip()
                if a != b: print('  FAIL composed blob of %s != #%s head blob' % (p, n)); rc_all = 1
        print('  every PR path of the CODE-ONLY tree == that PR\'s head blob (checked for %d paths)' % sum(len(own_nondoc(clone, bases[n], heads[n])) for n in all_prs()))
        json.dump(dict((k, dict(full=v['full'], nodocs=v['nodocs'])) for k, v in trees.items()), open(os.path.join(out, 'compose_trees.json'), 'w'), indent=1)
    ns = sorted(heads)
    for i, a in enumerate(ns):
        for b in ns[i + 1:]:
            if '1450' not in (a, b) or a in landed or b in landed: continue
            rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', heads[a], heads[b]])
            lines = o.decode('utf-8', 'replace').strip().split('\n'); tree = lines[0] if lines else ''
            conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
            print('  merge-tree --write-tree #%s + #%s (merge base computed by git): rc %d (1 = conflicts; anything else is an ERROR) tree %s | conflicted paths %s' % (a, b, rc, tree[:12], sorted(set(conf)) or 'none'))
            if rc not in (0, 1): rc_all = 1
    for n in ns:
        if n in landed: print('  merge-tree develop + #%s: SKIPPED (LANDED: its change is already in develop)' % n); continue
        rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', develop, heads[n]])
        lines = o.decode('utf-8', 'replace').strip().split('\n'); conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
        print('  merge-tree --write-tree develop %s + #%s: rc %d tree %s | conflicted paths %s' % (develop[:12], n, rc, (lines[0] if lines else '')[:12], sorted(set(conf)) or 'none'))
        if rc not in (0, 1): rc_all = 1
        if n == '1450' and sorted(set(conf)) != sorted(DOCS): print('  FAIL #1450 onto develop must conflict in EXACTLY the two docs (the seat measured the same); got %s' % sorted(set(conf))); rc_all = 1
    return rc_all


def docs_cmd(clone, develop, heads, bases, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    assert_not_in_repo(scratch, 'scratch'); tmp = canon_tmp(scratch)
    landed = landed_set(clone, develop, heads, bases)
    print('%s LANDED companions (docs fragment already in develop %s; excluded from every order): %s' % (now(), develop[:12], landed or 'NONE'))
    orders = [(t, [n for n in K['compose_orders'][t] if n not in landed]) for t in ('A', 'B', 'C')] + [('SOLO', ['1450'])]; texts = {}
    D = K['docs_composition']
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); nm = os.path.basename(d)
        ins = dict((n, insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))) for n in heads)
        fn = flow_numbers(dv)
        print('%s %s: insertion position per PR against ITS OWN base (line) %s | each directly before </body> | fragment bytes %s | develop flow numbers in DOCUMENT order, tail %s (max %s; next free by max+1 %s)%s' % (
            now(), nm, dict((n, v[0] + 1) for n, v in ins.items()), dict((n, len('\n'.join(v[1]).encode()) + 1) for n, v in ins.items()), fn[-6:], max(fn) if fn else 'n/a', (max(fn) + 1) if fn else 'n/a',
            '' if d != DOCS[0] else ' | kit tail at draft %s' % D['develop_tail_at_draft']))
        sd = os.path.join(scratch, 'docs_' + nm[:12]); os.makedirs(sd, exist_ok=True); w(os.path.join(sd, 'develop.html'), dv)
        for n in heads:
            w(os.path.join(sd, 'base_%s.html' % n), git_bytes(clone, bases[n], d)); w(os.path.join(sd, 'head_%s.html' % n), git_bytes(clone, heads[n], d))
        for n in sorted(heads):   # each PR ALONE onto develop (a textual merge of its change onto the develop the gate reads)
            if n in landed: print('  #%s alone onto develop: SKIPPED (LANDED)' % n); continue
            rc, o = merge_file(os.path.join(sd, 'develop.html'), os.path.join(sd, 'base_%s.html' % n), os.path.join(sd, 'head_%s.html' % n)); w(os.path.join(out, 'merge_alone_%s_%s.txt' % (nm[:10], n)), o)
            print('  #%s alone onto develop, textual merge-file: %s hunk(s) (a conflict means develop has a block at the SAME insertion line; #%s\'s base is %s)' % (n, rc if rc >= 0 else 'ERR', n, bases[n][:12]))
            if n == '1450' and rc != 1: print('  FAIL #1450 alone must conflict by exactly 1 hunk per doc (the PR reads dirty); got %s' % rc); rc_all = 1
        for tag, order in orders:
            frs = [ins[n][1] for n in order]; res = compose_keep_both(dv, frs); texts[(tag, d)] = res
            w(os.path.join(sd, 'composed_%s.html' % tag), res)
            counts = dict((n, res.count('\n'.join(ins[n][1]))) for n in order)
            h2 = dict((n, len([l for l in ins[n][1] if '<h2' in l])) for n in order)
            minus = res
            for n in order: minus = minus.replace('\n'.join(ins[n][1]) + '\n', '', 1)
            fnum = flow_numbers(res) if d == DOCS[0] else None
            once = all(c == 1 for c in counts.values()); equal_dev = (minus == dv)
            print('     KEEP-BOTH %-4s (%s): fragment counts WANT 1 each %s -> %s | composed minus the fragments == develop byte for byte: %s | h2 per fragment %s%s' % (
                tag, ' -> '.join('#' + n for n in order), counts, once, equal_dev, h2, (' | flow numbers in file order (tail) %s' % fnum[-7:]) if fnum else ''))
            if not once or not equal_dev: rc_all = 1
            if d == DOCS[0]:
                wantf = [D['flow_numbers'][n] for n in order]; tail = [x for x in fnum if x in wantf]
                print('     placement order %s -> file order of those flow numbers %s : %s' % (wantf, tail, 'MATCH' if tail == wantf else 'DIFFER')); rc_all |= 0 if tail == wantf else 1
    def small_tree(dest):
        if not os.path.exists(dest): extract(clone, develop, existing(clone, develop, SMALL_PATHS), dest)
        assert_not_in_repo(dest, 'matrix tree'); return dest
    mx = D['matrix_suite']; results = {}
    drop = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); ins = dict((n, insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))) for n in heads)
        drop[d] = (compose_keep_both(dv, [ins[n][1] for n in K['compose_orders']['A'] if n != '1450' and n not in landed]), ins['1450'][1])
    for lab, comp in [('develop tree (control)', None)] + [('COMPOSED order %s' % t, t) for t, _ in orders] + [('DROP-A-BLOCK control (no #1450)', 'DROP')]:
        td = os.path.join(scratch, 'mx_' + re.sub(r'\W+', '_', lab)[:22]); small_tree(td)
        if comp:
            for d in DOCS: w(os.path.join(td, d), drop[d][0] if comp == 'DROP' else texts[(comp, d)])
        rc, o, e, to = run(['/bin/bash', os.path.join(td, mx)], cwd=td, env={'TMPDIR': tmp}, timeout=300, merge=True); c = pcounts(o); inval = 'is missing' in o
        w(os.path.join(out, 'matrix_%s.out' % re.sub(r'\W+', '_', lab)[:22]), o)
        print('%s html_docs_matrix on %-36s rc %d%s counts %s%s' % (now(), lab, rc, ' TIMEOUT' if to else '', c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
        results[lab] = (rc, c, inval)
        if inval: rc_all = 1
    ok_orders = [lab for lab, (rc, c, inv) in results.items() if lab.startswith('COMPOSED') and rc == 0 and c and c[1] == 0 and not inv]
    print('COMPOSED orders with html_docs_matrix 0 failed: %s (PASS condition: order A + at least ONE other)' % ok_orders)
    if 'COMPOSED order A' not in ok_orders or len(ok_orders) < 2: rc_all = 1
    dk = results['DROP-A-BLOCK control (no #1450)']
    frag50 = '\n'.join(drop[DOCS[0]][1]); cnt = drop[DOCS[0]][0].count(frag50)
    print('CONTROL: a composition WITHOUT #1450: html_docs_matrix rc %d counts %s (gate81 G81-2: the matrix does NOT detect a dropped block) | the COUNT check (fragment of #1450 present once) reads %d and the flow number 53 is present: %s -> the count check %s' % (
        dk[0], dk[1], cnt, 53 in flow_numbers(drop[DOCS[0]][0]), 'CATCHES the drop' if cnt != 1 and 53 not in flow_numbers(drop[DOCS[0]][0]) else 'DOES NOT CATCH THE DROP'))
    rc_all |= 0 if (cnt != 1 and 53 not in flow_numbers(drop[DOCS[0]][0]) and dk[1] == (12, 0)) else 1
    return rc_all


# ---------------- selftest ----------------
def selftest():
    tmpd = os.environ.get('TMPDIR', '')
    if not tmpd or os.path.realpath(tmpd) != tmpd.rstrip('/') or in_repo(tmpd):
        print('REFUSED: the selftest runs only with TMPDIR set to a CANONICAL (realpath) directory outside every git repo; TMPDIR=%r (realpath %r, inside a repo: %s)' % (tmpd, os.path.realpath(tmpd) if tmpd else None, in_repo(tmpd) if tmpd and os.path.isdir(tmpd) else 'n/a')); return 2
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(os.path.realpath(tmpd) == tmpd.rstrip('/') and not in_repo(tmpd), 'TMPDIR %s is canonical (realpath equal) and NOT inside a repo' % tmpd)
    tmpd = tempfile.mkdtemp(prefix='g83st_', dir=tmpd)   # a fresh work dir per run (nothing is deleted; the TMPDIR keeps the residue)
    rep(in_repo(HERE), 'CONTROL: the kit directory IS inside a repo (in_repo fires)')
    try: assert_not_in_repo(HERE, 'x'); rep(False, 'assert_not_in_repo accepted the kit dir')
    except SystemExit: rep(True, 'ARM: assert_not_in_repo refuses a path inside a repo')
    try: canon_tmp('/Volumes/DevMASTER/!CODING/zz'); rep(False, 'canon_tmp accepted a !CODING path')
    except SystemExit: rep(True, 'ARM: canon_tmp refuses a scratch under !CODING')
    try: apply_edits('a b a', [('a', 'x')]); rep(False, 'a 2-occurrence anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor occurring twice -> refused (tamper not applied)')
    try: apply_edits('a b', [('zz', 'x')]); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor absent -> refused')
    t = apply_edits('one two', [('two', 'TWO')]); rep(t == 'one TWO' and landed('one two', t, [('two', 'TWO')]), 'a single-occurrence edit applies and reads LANDED')
    rep(not landed('x', 'x', [('a', 'b')]), 'PLANTED no-change reads NOT LANDED')
    rep(pcounts('x\n  4 passed, 0 failed\n') == (4, 0) and pcounts('nothing') is None, 'pcounts reads "N passed, M failed" and nothing else')
    rep(red_cells("PASS: a\nFAIL: the leg does not name the locks outside its four directories: x\nFAIL: CONTROL failing lock: rc=0") == ['cell 1', 'cell 5'] and red_cells('PASS: x\n') == [], 'red_cells maps FAIL lines to cells and reads nothing from PASS lines')
    s = parse_surface('All 3 ...\n  surface: 0 of 6 tracked package-lock.json file(s) were installed by this leg\n  NOT installed by this leg (6):\n    a/package-lock.json\n    b/package-lock.json\n')
    rep(s and s['covered'] == 0 and s['total'] == 6 and s['outside_n'] == 6 and s['listed'] == ['a/package-lock.json', 'b/package-lock.json'], 'parse_surface reads the count, the heading and the listed paths')
    rep(parse_surface('  surface: not a git checkout - cannot list the tracked lockfiles this leg does not install\n')['msg'] and parse_surface('All 3 standalone lock(s) pass\n') is None, 'parse_surface reads the not-a-git-checkout message and returns None when there is no surface line')
    dev = 'x\n</body>\n'
    r1 = compose_keep_both(dev, [['H50'], ['H51'], ['H52'], ['H53'], ['H54']]); rep(r1 == 'x\nH50\nH51\nH52\nH53\nH54\n</body>\n', 'compose_keep_both: five fragments go before </body> in the given order, each present once')
    rep(compose_keep_both(dev, [['H54'], ['H53']]) == 'x\nH54\nH53\n</body>\n', 'compose_keep_both: the REVERSE placement is a different, equally complete text')
    rep(compose_keep_both(dev, [['H51']]).count('H53') == 0, 'CONTROL: a composition keeping one block reads the others ABSENT (the count check can fail)')
    try: compose_keep_both('no body', [['a']]); rep(False, 'a doc with no </body> was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a develop doc with no </body> -> refused')
    ia, fa = insertion('x\n</body>\n', 'x\nH53\n</body>\n'); rep(ia == 1 and fa == ['H53'], 'insertion reads the block and its base position')
    try: insertion('x\n</body>\n', 'y\n</body>\n'); rep(False, 'a non-insertion was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a replaced base line is not a pure insertion -> refused')
    rep(flow_numbers('<h2>50. a</h2><h2>53. b</h2><h2>54. c</h2>') == [50, 53, 54], 'flow_numbers reads <h2>NN.</h2> headings')
    d = os.path.join(tmpd, 'selftest_a'); os.makedirs(d, exist_ok=True)
    for n, tx in (('x', 'one\ntwo\nthree\n'), ('y', 'one\ntwo\nthree\nfour\n'), ('z', 'zero\ntwo\nthree\n'), ('q', 'one\nTWO\nthree\n'), ('r', 'one\ntwo!\nthree\n')): open(os.path.join(d, n), 'w').write(tx)
    rc, o = merge_file(os.path.join(d, 'y'), os.path.join(d, 'x'), os.path.join(d, 'z')); rep(rc == 0 and o.startswith('zero') and o.rstrip().endswith('four'), 'merge_file: a clean 3-way merge reads rc 0')
    rc, o = merge_file(os.path.join(d, 'q'), os.path.join(d, 'x'), os.path.join(d, 'r')); rep(rc == 1 and ('<' * 7 + ' ours') in o, 'merge_file: PLANTED same-line edits read rc 1 with a conflict marker (the instrument can see a conflict)')
    rc, o, e, to = run(['sh', '-c', 'cat >/dev/null'], timeout=2, stdin=None); rep(rc == 0 and not to, 'run(): a child with stdin /dev/null returns')
    pre = time.time(); rc, o, e, to = run(['sh', '-c', 'sleep 30'], timeout=1); rep(to and time.time() - pre < 6, 'run(): a hanging child is killed by process group at the timeout (TIMEOUT reported)')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/x/y', 'write'); rep(False, 'a write under !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a write path under !CODING -> refused (lexical)')
    try: extract('/nonexistent-repo', 'abc', ['x'], '/Volumes/DevMASTER/!CODING/zz'); rep(False, 'extract into !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: extract into a !CODING dest -> refused before any write')
    try: cgit('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', ['write-tree']); rep(False, 'plumbing in the shared checkout was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a plumbing write verb against a clone under !CODING (the shared checkout) -> refused before it runs')
    try: cfg_hash(os.path.join(tmpd, 'absent-config')); rep(False, 'cfg_hash accepted an absent config')
    except SystemExit: rep(True, 'ARM: cfg_hash refuses an absent / empty config (the EMPTY-string hash e3b0c44298fc1c14 can never be a measurement)')
    r0 = make_repo(os.path.join(tmpd, 'selftest_repo_unset'), None); r1 = make_repo(os.path.join(tmpd, 'selftest_repo_set'), '.githooks')
    rep(sh_git(['-C', r0, 'config', 'core.hooksPath'])[1] == '' and sh_git(['-C', r1, 'config', 'core.hooksPath'])[1] == '.githooks' and os.path.isdir(os.path.join(r0, '.githooks')), 'make_repo: an UNSET repo and an already-`.githooks` repo, both with a .githooks directory')
    h0 = cfg_hash(os.path.join(r0, '.git', 'config')); sh_git(['-C', r0, 'config', 'core.hooksPath', 'zz']); rep(cfg_hash(os.path.join(r0, '.git', 'config')) != h0, 'cfg_hash: a direct config change reads CHANGED (the positive control of the cwd arms)')
    rep(in_repo(r0) and not in_repo(tmpd), 'in_repo: a scratch repo reads inside, the canonical TMPDIR reads outside')
    # the stub machinery on a toy leg: S2 changes a number, the stub log shows it took effect, the unstubbed run is the control
    toy = ('#!/bin/bash\nprefix="$(git rev-parse --show-prefix)"\necho "prefix=[$prefix]"\n')
    root = os.path.join(tmpd, 'toy'); os.makedirs(os.path.join(root, 'sub')); open(os.path.join(root, 'sub', 'f'), 'w').write('x\n'); w(os.path.join(root, 'sub', 'toy.sh'), toy)
    assert sh_git(['init', '-q', root])[0] == 0
    pd0, log0 = make_pathdir(os.path.join(tmpd, 'pd0'), git_mode='LOG'); pd2, log2 = make_pathdir(os.path.join(tmpd, 'pd2'), git_mode='S2')
    rc0, o0, _ = run_leg(os.path.join(root, 'sub', 'toy.sh'), pd0, os.path.join(root, 'sub')); rc2, o2, _ = run_leg(os.path.join(root, 'sub', 'toy.sh'), pd2, os.path.join(root, 'sub'))
    rep('prefix=[sub/]' in o0 and 'prefix=[]' in o2 and '--show-prefix' in open(log2).read() and '--show-prefix' in open(log0).read(), 'stub S2 CONTROL: --show-prefix reads `sub/` unstubbed and EMPTY under S2, and both calls are in the stub log (the stub is shown to take effect)')
    pd1, log1 = make_pathdir(os.path.join(tmpd, 'pd1'), git_mode='S1'); rc1, o1, _ = run_leg(os.path.join(root, 'sub', 'toy.sh'), pd1, os.path.join(root, 'sub'))
    rep('prefix=[]' in o1 and open(log1).read().strip() != '', 'stub S1 CONTROL: every git call fails (empty output) and is logged')
    fn = function_text('a\nfoo() {\n  :\n}\nb\n', 'foo'); rep(fn == 'foo() {\n  :\n}\n', 'function_text extracts one function')
    try: function_text('foo() {\n}\nfoo() {\n}\n', 'foo'); rep(False, 'a function defined twice was ACCEPTED')
    except SystemExit: rep(True, 'ARM: function_text refuses a function defined twice')
    sub_pd, _ = make_pathdir(os.path.join(tmpd, 'pdsub'), node='18', docker='down')
    rep(open(os.path.join(sub_pd, 'node')).read().strip().endswith('echo 18') and os.path.exists(os.path.join(sub_pd, 'docker')), 'make_pathdir: node answers 18 and docker is stubbed down for the advisory-SKIP arm')
    # git apply outside a repo refuses a second application (the payload control)
    pd_ = os.path.join(tmpd, 'applytest'); os.makedirs(pd_); open(os.path.join(pd_, 'a.txt'), 'w').write('one\ntwo\n')
    pt = os.path.join(tmpd, 'p.diff'); open(pt, 'w').write('--- a/a.txt\n+++ b/a.txt\n@@ -1,2 +1,3 @@\n one\n+mid\n two\n')
    r1_ = run(['git', 'apply', '-p1', pt], cwd=pd_)[0]; r2_ = run(['git', 'apply', '--check', '-p1', pt], cwd=pd_)[0]
    rep(r1_ == 0 and r2_ != 0 and open(os.path.join(pd_, 'a.txt')).read() == 'one\nmid\ntwo\n', 'git apply outside a repo: the first application lands, a SECOND application is refused (the payload arm\'s control)')
    for pr_, T in TAMPER.items():
        ok = all(len(rw) == 4 for rw in T['rows']); rep(ok, '#%s tamper table: %d rows, each (id, name, edits, predicted reds)' % (pr_, len(T['rows'])))
    rep(len(TAMPER['1450']['rows']) == 13, 'the tamper table is the declared size (13)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        cmd = A[0]
        if cmd == 'tamper':
            pr = req(A, '--pr'); only = (opt(A, '--only') or '').split(',') if opt(A, '--only') else None
            return tamper_cmd(pr, req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'), only)
        if cmd == 'shells': return shells_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'payload': return payload_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'stubs': return stubs_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'realtree': return realtree_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'cwd': return cwd_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'siblings': return siblings_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd in ('compose', 'docs'):
            cl = req(A, '--clone'); dev = req(A, '--develop', True); heads = pr_heads(A)
            bases = pr_bases(cl, dev, heads, req(A, '--base1450', True))
            return (compose_cmd if cmd == 'compose' else docs_cmd)(cl, dev, heads, bases, req(A, '--scratch'), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
