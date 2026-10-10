#!/usr/bin/env python3
"""c3_cells_gate84.py — the RUN instruments for gate84: #1450's shell suite (14 cells; arms: head, BASE planted, PREVIOUS head planted), the leg run ONLY with stubs (node / npm / git on a private PATH;
NO real npm ci, NO install of any lock), N-1450-1 re-measured (`hook`: a REAL linked-worktree push through a scratch pre-push hook and an inherited-GIT_DIR run, on /usr/bin/git AND Homebrew git),
the exit-code table (`exitcodes`: head vs previous head), the stub-git variants (`stubs`), the bash 3.2.57 empty-corpus abort and the empty-CHECKED guard on the EXTRACTED functions, the cwd question,
the sibling suite, the FIRST commit's payload applied from the Spark patch.diff, the real-tree surface COMPUTED (never run), the TAMPER rows (gate83's T1-T12 + the seat's mutants against the NEW script),
and the docs composition for the ONE PR (`compose`, `docs`: parent = merge-base(develop, head), the G83-1 fix). Every write path is checked lexically AND by realpath and refused under !CODING.
Ported from c3_cells_gate83.py; [g84] rebuilt. NO vitest, NO tsx, NO `npx`, NO npm of any kind. The ONLY git push this kit performs goes to a scratch BARE remote under the gate's scratch (asserted).

  shells   --clone CL --head H --base B --scratch S --out DIR   the new suite with the head product / the BASE product planted / the PREVIOUS head product planted (red cells named); `run-shell-suites.sh --list`
           base vs head; html_docs_matrix at the head tree; config hashes around every run. All in trees extracted with `git archive` OUTSIDE every git repo (asserted, with a control).
  hook     --clone CL --head H --base B --scratch S --out DIR   N-1450-1: the previous head's and the head's script, each in a scratch repo with a REAL pre-push hook and a REAL `git push` to a scratch bare
           remote, from the main checkout and from a linked worktree (and one with `git -c`, so GIT_CONFIG_PARAMETERS is exported), on /usr/bin/git AND Homebrew git; plus the inherited-GIT_DIR runs. node/npm STUBS only.
  exitcodes --clone CL --head H --base B --scratch S --out DIR  14 cases, the head script vs the PREVIOUS head script: exit code equal? output identical or different as predicted?
  payload  --clone CL --head H --base B --scratch S --out DIR   `git apply -p1` of the Spark patch.diff onto the BASE files (in a scratch tree outside every repo): the applied blobs vs the FIRST commit's.
  stubs    --clone CL --head H --base B --scratch S --out DIR   the leg (head, previous head, base) in a scratch repo under: no stub, S1 git fails on any call, S2 `--show-prefix` fails, S3 `ls-files` fails,
           TL `--show-toplevel` fails, ENV0 / ENV1 `--local-env-vars` prints nothing / fails, a real tree with no .git, the advisory-SKIP path; the zero-lock corpus on bash 3.2.57; the EXTRACTED functions with an
           empty CHECKED and an unguarded-expansion CONTROL. Each stub is shown to take effect (its call log).
  realtree --clone CL --head H --scratch S --out DIR   the surface COMPUTED on the real tree: the 45 tracked lock paths, `find` over the extracted lock files (35), and the EXTRACTED functions run in a scratch
           repo that tracks those 45 paths (MODELLED: the leg itself is not run on the real tree).
  cwd      --clone CL --head H --scratch S --out DIR   Q-CWD1426: the new suite from a non-repo cwd, from inside a scratch repo with .githooks (hooksPath unset), from a worktree of it, from a repo with another
           hooksPath value, with TMPDIR INSIDE the repo, and (INFO) with GIT_DIR inherited: outputs byte-compared; the .git/config of every repo hashed around every run (positive control, empty-hash guard).
  siblings --clone CL --head H --base B --scratch S --out DIR   preflight_deps.test.sh with the base script and with the head script (FULL outputs byte-compared); it plants a stub of the leg (its line 312).
  tamper   --pr 1450 --clone CL --head H --base B --scratch S --out DIR [--only T1,T2]   HEAD row (all green), CONTROL no-op row, then the rows: anchor EXACTLY ONCE, LANDED, run the suite, read
           which cells RED, RESTORE (sha). ALL-GREEN = a tamper no cell catches (a finding to rule).
  compose  --clone CL --head1450 H --base1450 B --develop D --scratch S --out DIR   the ONE PR in a TEMP INDEX over D (code-only tree = D + the PR's own non-doc paths), `git merge-tree --write-tree --name-only`
           of D with the head AND with the previous head (the predicted conflict set: exactly the two docs) and a clean control.
  docs     (same args)  the two docs: the fragment against merge-base(D, head) (`lib.docs_base`, NEVER head^), textual merge-file onto D, KEEP-BOTH SOLO onto D with the fragment COUNT of exactly 1 (and no flow number
           or heading duplicated), composed-minus-fragment == D byte for byte, html_docs_matrix on the composed tree, a DROP-A-BLOCK control and a DUPLICATE-A-BLOCK control that html_docs_matrix does not see
           (gate81 G81-2 / gate83 G83-1) but the COUNT does, and the wrong-parent controls (head^, develop given as the base) that REFUSE.
  --selftest   (refuses unless TMPDIR is a canonical directory outside every repo)
rc 0 / 1 (a FAIL: plant not landed, restore failed, a prediction DIFFERS, a composition that does not compose) / 2 refused. NOT RUN is reported by name and is never a pass."""
import difflib, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate84 import K, PR, git, git_bytes, blob, req, opt, wgit, must_be_outside, extract, resolvable, docs_base, exact_tail_insert, TAIL

HERE = os.path.dirname(os.path.abspath(__file__))
P50 = PR(1450)
DOCS = list(K['known_develop_overlap'])
SCRIPT, SUITE = P50['gate_script'], P50['suite']
EMPTY_SHA = 'e3b0c44298fc1c14'
CHECKOUT = K['checkout']
GENV = {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_AUTHOR_NAME': 'gate84', 'GIT_AUTHOR_EMAIL': 'x@x', 'GIT_COMMITTER_NAME': 'gate84', 'GIT_COMMITTER_EMAIL': 'x@x'}
REALGIT = '/usr/bin/git' if os.path.exists('/usr/bin/git') else shutil.which('git')
CELLRX = [(1, r'^FAIL: the leg does not name the locks outside its four directories'), (2, r"^FAIL: no 'surface: 3 of 6 tracked' line"), (3, r'^FAIL: CONTROL clean run'),
          (4, r'^FAIL: CONTROL one-directory run'), (5, r'^FAIL: CONTROL failing lock:'), (6, r'^FAIL: under an inherited GIT_DIR:'), (7, r'^FAIL: in a linked worktree \(gitdir'),
          (8, r'^FAIL: a failing --show-prefix:'), (9, r'^FAIL: a failing ls-files:'), (10, r'^FAIL: CONTROL heading/list:'), (11, r'^FAIL: CONTROL failing run:'),
          (12, r'^FAIL: CONTROL failing --show-toplevel:'), (13, r'^FAIL: an unusable local-variable list:'), (14, r'^FAIL: CONTROL no tracked locks:')]
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
    """[g84] a scratch tree inside a repo would put the suite's cwd / TMPDIR in someone's repo (gate82 H9); the gate's rule is a scratch OUTSIDE every repo."""
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


def cfmt(cells): return 'cells ' + (','.join(str(c) for c in sorted(cells)) or 'NONE')


def parse_surface(out):
    """-> dict(covered, total, outside_n, listed[], msg) from a leg's output, or None when there is no surface line. [g84] `msg` is the text after `surface: ` of any NON-number surface line
    ("not a git checkout ...", "git could not ... - cannot list ...", "git's list of repository-local variables is unusable - cannot list ...")."""
    m = re.search(r'(?m)^  surface: (\d+) of (\d+) tracked package-lock\.json file\(s\) were installed by this leg$', out)
    msg = re.search(r'(?m)^  surface: (?!\d)(.*)$', out)
    if not m and not msg: return None
    d = {'msg': msg.group(1).strip() if msg else None, 'covered': int(m.group(1)) if m else None, 'total': int(m.group(2)) if m else None, 'outside_n': None, 'listed': []}
    h = re.search(r'(?m)^  NOT installed by this leg \((\d+)\):$', out)
    if h:
        d['outside_n'] = int(h.group(1)); tail = out[h.end():].split('\n')
        for l in tail:
            if l.startswith('    ') and l.strip().endswith('package-lock.json'): d['listed'].append(l.strip())
            elif l.strip(): break
    return d


def sline(s):
    """a one-line rendering of a parse_surface result."""
    if s is None: return 'NO surface line'
    if s['covered'] is not None: return '%s of %s (heading %s, %d listed)' % (s['covered'], s['total'], s['outside_n'], len(s['listed']))
    return 'MSG[%s]' % s['msg'][:60]


# ---------------- the leg under stubs ----------------
def write_exec(path, text):
    w(path, text); os.chmod(path, 0o755)


def make_pathdir(d, node='24', git_mode=None, docker=None):
    """a private PATH directory: node answers `node` for any call; npm succeeds unless the cwd holds FAIL_ME; git_mode None = no git stub (real /usr/bin/git),
    'S1' fails on every call, 'S2' fails when an argument is --show-prefix, 'S3' ls-files, 'TL' --show-toplevel, 'ENV0' --local-env-vars prints nothing (rc 0), 'ENV1' --local-env-vars fails, 'LOG' only logs; docker None = absent, 'down' = exits 1."""
    must_be_outside(d, 'stub dir'); os.makedirs(d)
    write_exec(os.path.join(d, 'node'), '#!/bin/sh\necho %s\n' % node)
    write_exec(os.path.join(d, 'npm'), '#!/bin/sh\n[ -e FAIL_ME ] && exit 1\nexit 0\n')
    log = os.path.join(d, 'git.calls.log')
    if git_mode:
        body = {'S1': 'exit 1\n',
                'S2': 'for a in "$@"; do [ "$a" = "--show-prefix" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
                'S3': 'for a in "$@"; do [ "$a" = "ls-files" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
                'TL': 'for a in "$@"; do [ "$a" = "--show-toplevel" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
                'ENV0': 'for a in "$@"; do [ "$a" = "--local-env-vars" ] && exit 0; done\nexec %s "$@"\n' % REALGIT,
                'ENV1': 'for a in "$@"; do [ "$a" = "--local-env-vars" ] && exit 1; done\nexec %s "$@"\n' % REALGIT,
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
    br = Bracket(clone); stamp = '%d' % int(time.time()); prev = P50['prev_head']
    th = tree_for(clone, head, os.path.join(scratch, 'tree_head_' + stamp)); tb = tree_for(clone, base, os.path.join(scratch, 'tree_base_' + stamp))
    s_head, s_base, s_prev = git_bytes(clone, head, SCRIPT), git_bytes(clone, base, SCRIPT), git_bytes(clone, prev, SCRIPT)
    mode = os.stat(os.path.join(th, SCRIPT)).st_mode
    # PREDICTIONS (written from the reading of the suite and the script BEFORE any run; the F 11th READY states the same counts)
    arms = [('A', 'head script, head suite', s_head, (14, 0), 0, []),
            ('B', 'BASE script planted, head suite', s_base, (4, 10), 1, [1, 2, 6, 7, 8, 9, 10, 12, 13, 14]),
            ('C', 'PREVIOUS-head script (d1d8b91b7c1f, gate83\'s NO GO head) planted, head suite', s_prev, (9, 5), 1, [6, 7, 8, 9, 13])]
    for aid, lab, data, want, wrc, wred in arms:
        write_checked(th, SCRIPT, data); os.chmod(os.path.join(th, SCRIPT), mode)
        rc, o, e, to = run(['/bin/bash', os.path.join(th, SUITE)], cwd=scratch, env={'TMPDIR': tmp}, merge=True)
        c = pcounts(o); reds = red_cells(o); nfail = len(re.findall(r'(?m)^FAIL:', o)); npass = len(re.findall(r'(?m)^PASS:', o))
        w(os.path.join(out, 'shell1450_%s.out' % aid), o)
        ok = c == want and rc == wrc and reds == wred and (npass, nfail) == want
        print('%s ARM %s (%s): rc %d%s summary-line counts %s | own PASS/FAIL line count (%d, %d) | red %s | want %s rc %s red %s -> %s | output %d B sha256/16 %s | plant sha256/16 %s' % (
            now(), aid, lab, rc, ' TIMEOUT' if to else '', c, npass, nfail, cfmt(reds), want, wrc, cfmt(wred), 'MATCH' if ok else 'DIFFER', len(o.encode()), sha(o.encode())[:16], sha(data)[:16]))
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
    canon_tmp(scratch); sp = K['spark']['patch']; stamp = '%d' % int(time.time()); prev = P50['prev_head']
    if not os.path.isfile(sp): print('NOT RUN: %s is not readable' % sp); return 1
    d = os.path.join(scratch, 'payload_' + stamp); assert_not_in_repo(scratch, 'scratch')
    extract(clone, base, [SCRIPT], d)
    assert_not_in_repo(d, 'payload tree')
    rc, o, e, to = run(['git', 'apply', '--check', '-p1', sp], cwd=d); print('%s git apply --check -p1 patch.diff in %s (outside every repo): rc %d %s' % (now(), d, rc, (o + e).strip()[:120]))
    if rc: return 1
    rc, o, e, to = run(['git', 'apply', '-p1', sp], cwd=d); print('%s git apply -p1: rc %d %s' % (now(), rc, (o + e).strip()[:120]))
    if rc: return 1
    bs = open(os.path.join(d, SCRIPT), 'rb').read(); bt = open(os.path.join(d, SUITE), 'rb').read()
    ps, pt = git_bytes(clone, prev, SCRIPT), git_bytes(clone, prev, SUITE); hs, ht = git_bytes(clone, head, SCRIPT), git_bytes(clone, head, SUITE)
    print('%s applied script blob %s == the FIRST commit %s: %s | applied test blob %s == the first commit %s: %s | F 10th named 4948fe691609 / 5caa1b750fa3' % (
        now(), blob_id(bs)[:12], blob_id(ps)[:12], bs == ps, blob_id(bt)[:12], blob_id(pt)[:12], bt == pt))
    print('%s the HEAD blobs are %s / %s: they DIFFER from the payload (script differs: %s, test differs: %s) -> the second commit is the fix round, in NO payload (the PR body says so)' % (now(), blob_id(hs)[:12], blob_id(ht)[:12], bs != hs, bt != ht))
    if bs != ps or bt != pt or bs == hs or bt == ht: rc_all = 1
    rc2, o2, e2, to2 = run(['git', 'apply', '--check', '-p1', sp], cwd=d)
    print('%s CONTROL: the same patch applied a SECOND time must be refused (rc != 0): rc %d' % (now(), rc2))
    if rc2 == 0: rc_all = 1
    return rc_all


# ---------------- stubs (F1 / F2 / F5) ----------------
STUB_PREDICT = {   # PREDICTIONS for the HEAD script, written from the reading of the functions before any run
    'U':    dict(rc=0, covered=3, total=6, outside=3, msg=None),
    'S1':   dict(rc=0, covered=None, total=None, outside=None, msg="git's list of repository-local variables is unusable"),
    'S2':   dict(rc=0, covered=None, total=None, outside=None, msg="git could not report this directory's path"),
    'S3':   dict(rc=0, covered=None, total=None, outside=None, msg='git could not list the tracked package-lock.json files'),
    'TL':   dict(rc=0, covered=None, total=None, outside=None, msg='not a git checkout'),
    'ENV0': dict(rc=0, covered=None, total=None, outside=None, msg="git's list of repository-local variables is unusable"),
    'ENV1': dict(rc=0, covered=None, total=None, outside=None, msg="git's list of repository-local variables is unusable"),
    'R':    dict(rc=0, covered=None, total=None, outside=None, msg='not a git checkout'),
}
# what the PREVIOUS head (d1d8b91b7c1f, gate83's NO GO head) printed for the same variants (gate83 measured; the F 11th READY says the same)
PREV_PREDICT = {'U': '3 of 6', 'S1': 'not a git checkout', 'S2': '0 of 6', 'S3': '0 of 0', 'TL': 'not a git checkout', 'ENV0': '3 of 6', 'ENV1': '3 of 6', 'R': 'not a git checkout'}


def surface_key(s):
    if s is None: return 'NONE'
    return ('%s of %s' % (s['covered'], s['total'])) if s['covered'] is not None else s['msg']


def stubs_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); br = Bracket(clone); stamp = '%d' % int(time.time()); prev = P50['prev_head']
    s_head, s_base, s_prev = git_bytes(clone, head, SCRIPT), git_bytes(clone, base, SCRIPT), git_bytes(clone, prev, SCRIPT)
    print('%s shell: /bin/bash is %s; real git on the leg PATH: %s' % (now(), run(['/bin/bash', '--version'])[1].split('\n')[0], REALGIT))
    variants = [('U', None, True), ('S1', 'S1', True), ('S2', 'S2', True), ('S3', 'S3', True), ('TL', 'TL', True), ('ENV0', 'ENV0', True), ('ENV1', 'ENV1', True), ('R', None, False)]
    results = {}
    for tag, gm, init in variants:
        for which, sb in (('head', s_head), ('prev', s_prev), ('base', s_base)):
            root = os.path.join(scratch, 'leg_%s_%s_%s' % (tag, which, stamp)); sp = build_leg_repo(root, sb, init=init)
            pd, log = make_pathdir(os.path.join(scratch, 'path_%s_%s_%s' % (tag, which, stamp)), git_mode=gm or 'LOG')
            rc, o, to = run_leg(sp, pd, root)
            calls = [c for c in (open(log).read().split('\n') if os.path.exists(log) else []) if c]
            results[(tag, which)] = (rc, o, calls)
            w(os.path.join(out, 'leg_%s_%s.out' % (tag, which)), o)
    for tag, gm, init in variants:
        rc, o, calls = results[(tag, 'head')]; s = parse_surface(o); pr = STUB_PREDICT[tag]
        brc, bo, _ = results[(tag, 'base')]; prc, po, _ = results[(tag, 'prev')]; ps = parse_surface(po)
        got = dict(rc=rc, covered=s and s['covered'], total=s and s['total'], outside=s and s['outside_n'], msg=None)
        msg_ok = (pr['msg'] is None and (s is None or s['msg'] is None)) or (pr['msg'] is not None and bool(s and s['msg'] and s['msg'].startswith(pr['msg'])))
        match = got['rc'] == pr['rc'] and got['covered'] == pr['covered'] and got['total'] == pr['total'] and got['outside'] == pr['outside'] and msg_ok
        eff = ''
        if gm:
            hit = [c for c in calls if (gm == 'S2' and '--show-prefix' in c) or (gm == 'S3' and 'ls-files' in c) or (gm == 'TL' and '--show-toplevel' in c) or (gm in ('ENV0', 'ENV1') and '--local-env-vars' in c) or gm == 'S1']
            eff = ' | STUB TOOK EFFECT: %d logged git call(s) [%s], %d of them the failing one (%s)' % (len(calls), '; '.join(c[:28] for c in calls), len(hit), (hit or ['NONE'])[0][:50])
            if not hit: match = False
        pk = surface_key(ps); pwant = PREV_PREDICT[tag]; pmatch = (pk.startswith(pwant) if not pwant[0].isdigit() else pk == pwant)
        print('%s VARIANT %-4s HEAD: rc %d | %s | predicted %s -> %s%s | PREVIOUS head: rc %d, %s (predicted %s: %s) | base script: rc %d, surface %s | exit codes equal head/prev/base: %s' % (
            now(), tag, rc, sline(s), pr['msg'] or '%s of %s' % (pr['covered'], pr['total']), 'MATCH' if match else 'DIFFER', eff, prc, sline(ps), pwant, 'MATCH' if pmatch else 'DIFFER',
            brc, sline(parse_surface(bo)), rc == prc == brc))
        if not match or not pmatch or brc != rc or prc != rc or parse_surface(bo) is not None: rc_all = 1
    # the advisory SKIP path (a dev laptop with node < 24 and Docker down): the surface is NEVER printed there
    root = os.path.join(scratch, 'leg_skip_%s' % stamp); sp = build_leg_repo(root, s_head); pd, _ = make_pathdir(os.path.join(scratch, 'path_skip_%s' % stamp), node='18', docker='down')
    rc, o, to = run_leg(sp, pd, root); s = parse_surface(o); w(os.path.join(out, 'leg_advisory_skip.out'), o)
    print('%s ADVISORY-SKIP path (node stub answers 18, docker stub exits 1): rc %d | `SKIP (advisory)` printed: %s | surface lines: %s -> the surface is printed only on an all-OK run (c2 F3 measured the exit order)' % (now(), rc, 'SKIP (advisory)' in o, sline(s)))
    if not (rc == 0 and 'SKIP (advisory)' in o and s is None): rc_all = 1
    # F2: zero locks in the four directories, bash 3.2.57
    for which, sb in (('base', s_base), ('prev', s_prev), ('head', s_head)):
        root = os.path.join(scratch, 'leg_zero_%s_%s' % (which, stamp)); sp = build_leg_repo(root, sb, locks=False); pd, _ = make_pathdir(os.path.join(scratch, 'path_zero_%s_%s' % (which, stamp)))
        rc, o, to = run_leg(sp, pd, root); w(os.path.join(out, 'leg_zero_%s.out' % which), o)
        ub = 'unbound variable' in o; fn = 'DIRS[@]' in o
        print('%s F2 ZERO-LOCK corpus, %s script, /bin/bash 3.2.57, no arguments: rc %d | `unbound variable` %s | names DIRS[@] %s | surface lines %s | first line %r' % (
            now(), which, rc, ub, fn, sline(parse_surface(o)), (o.strip().split('\n') or [''])[0][:90]))
        if not (rc == 1 and ub and fn and parse_surface(o) is None): rc_all = 1
    hb = shutil.which('bash', path='/opt/homebrew/bin:/usr/local/bin')
    print('%s F2 on a bash >= 4: %s' % (now(), 'NOT RUN (no Homebrew bash on this host: /opt/homebrew/bin/bash absent)' if not hb else 'available at %s (NOT RUN by this kit)' % hb))
    # F2b: the EXTRACTED functions with an empty CHECKED, and the unguarded-expansion control. [g84] the guarded line lives in report_surface_lines, which the wrapper runs in a SUBSHELL:
    # an unbound-variable abort in the control therefore ends the subshell only and the wrapper still returns 0 (predicted: the control prints `unbound variable`, NO surface line, driver rc 0).
    src_h = s_head.decode()
    fn_lines, fn_wrap = function_text(src_h, 'report_surface_lines'), function_text(src_h, 'report_surface')
    root = os.path.join(scratch, 'leg_fn_%s' % stamp); build_leg_repo(root, s_head)
    devdir = os.path.join(root, 'Blockchain', 'Dev')
    guard = '${CHECKED[@]+"${CHECKED[@]}"}'
    for lab, lsrc in (('GUARDED (as committed)', fn_lines), ('CONTROL unguarded `"${CHECKED[@]}"`', fn_lines.replace(guard, '"${CHECKED[@]}"'))):
        if lab.startswith('CONTROL') and fn_lines.count(guard) != 1: print('FAIL the guard text occurs %d times' % fn_lines.count(guard)); rc_all = 1; continue
        if lab.startswith('CONTROL') and lsrc == fn_lines: print('FAIL the control plant did not land'); rc_all = 1; continue
        tg = lab[:5].strip().replace(' ', '_')
        drv = os.path.join(scratch, 'fn_driver_%s_%s.sh' % (tg, stamp))
        w(drv, 'set -uo pipefail\nCHECKED=()\n%s\n%s\ncd "%s"\nreport_surface\necho "report_surface rc=$?"\n' % (lsrc, fn_wrap, devdir))
        rc, o, to = run_leg(drv, make_pathdir(os.path.join(scratch, 'path_fn_%s_%s' % (tg, stamp)), git_mode='LOG')[0], scratch)
        s = parse_surface(o); ub = 'unbound variable' in o
        print('%s F2b EXTRACTED report_surface (wrapper) + report_surface_lines, EMPTY CHECKED, set -u, bash 3.2.57, %s: driver rc %d | surface %s | unbound variable: %s | tail %r' % (
            now(), lab, rc, sline(s), ub, o.strip().split('\n')[-1][:70]))
        if lab.startswith('GUARDED') and not (rc == 0 and s and s['covered'] == 0 and s['total'] == 6 and not ub and 'report_surface rc=0' in o): rc_all = 1
        if lab.startswith('CONTROL') and not (ub and s is None and 'report_surface rc=0' in o):
            rc_all = 1
        if lab.startswith('CONTROL'):
            print('      NOTE (measured): the wrapper\'s `return 0` after the subshell makes an unbound-variable crash of the body INVISIBLE to the leg\'s exit code (driver rc %d); only the missing surface line and the stderr text show it' % rc)
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- realtree (COMPUTED) ----------------
def realtree_cmd(clone, head, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); stamp = '%d' % int(time.time())
    names = [l for l in git(clone, 'ls-tree', '-r', '--name-only', head).split('\n') if l.endswith('package-lock.json')]
    tracked = len(names)
    lt = os.path.join(scratch, 'locks_%s' % stamp); extract(clone, head, names, lt); assert_not_in_repo(lt, 'lock tree')
    dev = os.path.join(lt, 'Blockchain', 'Dev')
    rc, o, e, to = run(['/usr/bin/find', 'services', 'packages', 'frontend', 'scripts', '-maxdepth', '2', '-name', 'package-lock.json'], cwd=dev)
    found = sorted(l for l in o.split('\n') if l.strip())
    print('%s REAL TREE (COMPUTED, the leg is NOT run on it): head %s tracks %d package-lock.json files (ls-tree; kit %d); the leg\'s `find services packages frontend scripts -maxdepth 2 -name package-lock.json` over those files reaches %d (kit %d); outside: %d (kit %d); find rc %d, stderr %r' % (
        now(), head[:12], tracked, P50['real_tree']['tracked_locks'], len(found), P50['real_tree']['find_reaches'], tracked - len(found), P50['real_tree']['listed'], rc, e[:80]))
    if tracked != P50['real_tree']['tracked_locks'] or len(found) != P50['real_tree']['find_reaches']: rc_all = 1
    emp = os.path.join(scratch, 'empty_%s' % stamp); os.makedirs(os.path.join(emp, 'services'))
    print('%s CONTROL: the same find over an empty services/ dir reads %d line(s) (must be 0)' % (now(), len([l for l in run(['/usr/bin/find', 'services', '-maxdepth', '2', '-name', 'package-lock.json'], cwd=emp)[1].split('\n') if l.strip()])))
    root = os.path.join(scratch, 'real45_%s' % stamp); os.makedirs(root)
    for n in names: w(os.path.join(root, n), b'{}\n')
    assert sh_git(['init', '-q', root])[0] == 0 and sh_git(['-C', root, 'add', '-A'])[0] == 0
    src_h = git_bytes(clone, head, SCRIPT).decode()
    fn_lines, fn_wrap = function_text(src_h, 'report_surface_lines'), function_text(src_h, 'report_surface')
    dirs = ' '.join('"%s"' % os.path.dirname(x) for x in found)
    drv = os.path.join(scratch, 'real45_driver_%s.sh' % stamp)
    w(drv, 'set -uo pipefail\nCHECKED=(%s)\n%s\n%s\ncd "%s"\nreport_surface\necho "report_surface rc=$?"\n' % (dirs, fn_lines, fn_wrap, os.path.join(root, 'Blockchain', 'Dev')))
    rc, o, to = run_leg(drv, make_pathdir(os.path.join(scratch, 'path_real45_%s' % stamp))[0], scratch); w(os.path.join(out, 'realtree_surface.out'), o)
    s = parse_surface(o)
    print('%s MODELLED output of the EXTRACTED report_surface over the 45 tracked paths with CHECKED = the 35 dirs (assumes all 35 pass): rc %d | %s' % (now(), rc, o.strip().replace('\n', ' | ')[:900]))
    want_out = sorted(set(names) - set('Blockchain/Dev/' + x for x in found))
    ok = s and s['covered'] == 35 and s['total'] == 45 and s['outside_n'] == 10 and sorted(s['listed']) == want_out
    print('%s PREDICTION `surface: 35 of 45` listing 10: %s | the 10 listed: %s' % (now(), 'MATCH' if ok else 'DIFFER', want_out))
    if not ok: rc_all = 1
    # the seat's FIELD evidence: the hook's own line on its real push, read from the raw log (read-only); the gate re-reads it
    for lab, fp in (('F 11th push of THIS head', P50['push_log_head']), ('F 10th push of the PREVIOUS head', P50['push_log_prev'])):
        if not os.path.isfile(fp): print('%s FIELD LOG %s: NOT READABLE here (%s): NOT RUN' % (now(), lab, fp)); continue
        txt = open(fp, encoding='utf-8', errors='replace').read(); ls = txt.split('\n')
        hits = [(i + 1, l.strip()) for i, l in enumerate(ls) if re.search(r'surface: \d+ of \d+|NOT installed by this leg|All \d+ standalone lock', l)]
        print('%s FIELD LOG %s (sha256/16 %s, %d B): %s' % (now(), lab, sha(txt.encode())[:16], len(txt.encode()), [(n, t[:80]) for n, t in hits[:4]]))
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
    rctl = make_repo(os.path.join(scratch, 'cwd_ctl_' + stamp), None); cfg = os.path.join(rctl, '.git', 'config'); c0 = cfg_hash(cfg)
    sh_git(['-C', rctl, 'config', 'core.hooksPath', 'zz']); c1 = cfg_hash(cfg)
    print('%s INSTRUMENT CONTROL: a direct `git config core.hooksPath zz` changes the hash %s -> %s (reads CHANGED: %s); the empty-string hash %s is refused' % (now(), c0, c1, c0 != c1, EMPTY_SHA))
    if c0 == c1: return 1
    try: cfg_hash(os.path.join(scratch, 'no-such-config')); print('FAIL the empty-hash guard did not fire'); return 1
    except SystemExit: print('  the empty-hash guard fired on an absent config (OK)')
    plain = os.path.join(scratch, 'cwd_plain_' + stamp); os.makedirs(plain); assert_not_in_repo(plain, 'plain cwd')
    r_unset = make_repo(os.path.join(scratch, 'cwd_unset_' + stamp), None); r_custom = make_repo(os.path.join(scratch, 'cwd_custom_' + stamp), 'custom/hooks'); r_tmp = make_repo(os.path.join(scratch, 'cwd_tmpin_' + stamp), None)
    wtp = os.path.join(scratch, 'cwd_wt_' + stamp); assert sh_git(['-C', r_unset, 'worktree', 'add', '-q', '--detach', wtp])[0] == 0
    arms = [('C0', 'cwd = a directory that is NOT in any repo', plain, None, tmp), ('C1', 'cwd = a scratch repo with .githooks, core.hooksPath UNSET', r_unset, r_unset, tmp),
            ('C2', 'cwd = a WORKTREE of that repo (the main repo\'s config is hashed)', wtp, r_unset, tmp), ('C3', 'cwd = a repo with core.hooksPath = custom/hooks', r_custom, r_custom, tmp),
            ('C4', 'cwd = a repo, and TMPDIR INSIDE it (the gate82 H9 shape)', r_tmp, r_tmp, os.path.join(r_tmp, 'tmp'))]
    outs = {}
    for aid, label, cwd, repo, td in arms:
        os.makedirs(td, exist_ok=True)
        before = cfg_hash(os.path.join(repo, '.git', 'config')) if repo else None
        st0 = sh_git(['-C', repo, 'status', '--porcelain'])[1] if repo else None
        rc, o, e, to = run(['/bin/bash', suite], cwd=cwd, env=dict(GENV, TMPDIR=td), merge=True)
        after = cfg_hash(os.path.join(repo, '.git', 'config')) if repo else None
        st1 = sh_git(['-C', repo, 'status', '--porcelain'])[1] if repo else None
        outs[aid] = (rc, o); w(os.path.join(out, 'cwd_%s.out' % aid), o)
        print('%s ARM %s %-70s rc %d counts %s | output %d B sha256/16 %s | repo .git/config %s -> %s : %s | repo `status --porcelain` %s -> %s' % (
            now(), aid, label, rc, pcounts(o), len(o.encode()), sha(o.encode())[:16], before, after, ('UNCHANGED' if before == after else 'CHANGED') if repo else 'n/a (no repo)', (st0 or '')[:30] or '(clean)', (st1 or '')[:30] or '(clean)'))
        if rc != 0 or pcounts(o) != (14, 0) or (repo and before != after) or st0 != st1: rc_all = 1
    same = len(set(sha(v[1].encode()) for v in outs.values())) == 1
    print('%s Q-CWD1426: FULL outputs of the 5 arms (stdout+stderr, rc folded) byte-identical: %s (%d distinct) | the F 11th READY reads 1,136 B from a non-repo dir and the worktree' % (now(), same, len(set(sha(v[1].encode()) for v in outs.values()))))
    if not same: rc_all = 1
    print('%s NOTE: this suite names neither bootstrap-env.sh nor env.example (c2 F7); it names core.hooksPath only as per-command `-c core.hooksPath=/dev/null` on its own scratch repo, so the gate82 H9 hazard (a TMPDIR inside a repo makes bootstrap-env.sh WRITE that repo\'s core.hooksPath) does not apply; the arms above MEASURE that rather than assume it.' % now())
    # C5 (INFO, not a pass/fail): the SUITE itself run with GIT_DIR inherited (as a hook would give it): is the suite hermetic? run-shell-suites.sh clears it (KS-1086) so the pre-push path is not affected.
    r_gd = make_repo(os.path.join(scratch, 'cwd_gd_' + stamp), None); gd_cfg = os.path.join(r_gd, '.git', 'config'); g0 = cfg_hash(gd_cfg); td = os.path.join(scratch, 'tmp_gd_' + stamp); os.makedirs(td)
    rc, o, e, to = run(['/bin/bash', suite], cwd=plain, env=dict(GENV, TMPDIR=td, GIT_DIR=os.path.join(r_gd, '.git')), merge=True); g1 = cfg_hash(gd_cfg); w(os.path.join(out, 'cwd_C5.out'), o)
    print('%s INFO C5 the suite run with GIT_DIR=<scratch repo>/.git inherited (cwd outside every repo): rc %d counts %s | that scratch repo\'s .git/config %s -> %s (%s) | output sha256/16 %s vs the clean arms\' %s -> %s' % (
        now(), rc, pcounts(o), g0, g1, 'UNCHANGED' if g0 == g1 else 'CHANGED', sha(o.encode())[:16], sha(outs['C0'][1].encode())[:16], 'same as C0' if o == outs['C0'][1] else 'DIFFERS from C0 (the suite is not hermetic against an inherited GIT_DIR; run-shell-suites.sh clears it, so the hook path is unaffected: a Polish note for the gate to rule)'))
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
    print('%s SIBLING base vs head: counts equal %s | FULL outputs byte-identical %s (%d differing line(s): %s) | READY: 56/0, weak' % (now(), pcounts(res['base'][1]) == pcounts(res['head'][1]), eq, len(dl), dl[:3]))
    if not eq or res['head'][0] != 0 or res['base'][0] != 0: rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- hook (N-1450-1 re-measured) and exitcodes ----------------
LOCAL_ENV = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_COMMON_DIR', 'GIT_PREFIX', 'GIT_CONFIG_PARAMETERS', 'GIT_CONFIG_COUNT', 'GIT_SSH_COMMAND')
IDENT = ['-c', 'user.name=gate84', '-c', 'user.email=x@x', '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null']
GITS = [('apple', '/usr/bin/git', '/usr/bin:/bin'), ('homebrew', '/opt/homebrew/bin/git', '/opt/homebrew/bin:/usr/bin:/bin')]
HOOK_TEXT = '''#!/bin/bash
# gate84 scratch pre-push hook: the two lines of the REAL .githooks/pre-push that matter (lines 281/283: `bash -c 'cd "$(git rev-parse --show-toplevel)" ...; cd Blockchain/Dev && bash scripts/preflight/...'`),
# with the leg called directly (no preflight) and the hook's inherited environment LOGGED. Writes only $HOOKLOG.
{
echo "HOOK-START"
echo "HOOK GIT_DIR=${GIT_DIR-unset}"
echo "HOOK GIT_WORK_TREE=${GIT_WORK_TREE-unset}"
echo "HOOK GIT_CONFIG_PARAMETERS=${GIT_CONFIG_PARAMETERS-unset}"
echo "HOOK PWD=$PWD"
echo "HOOK git=$(command -v git) $(git --version)"
( /bin/bash -c 'cd "$(git rev-parse --show-toplevel)" || exit 1; cd Blockchain/Dev && /bin/bash scripts/preflight/lockfile-cleanroom.sh' )
echo "HOOK-LEG-RC=$?"
} >> "$HOOKLOG" 2>&1
exit 0
'''


def ggit(gbin, args, cwd=None, env=None, timeout=120):
    e = dict(os.environ)
    for k in LOCAL_ENV: e.pop(k, None)
    e.update(GENV); e.update(env or {})
    p = subprocess.run([gbin] + list(args), capture_output=True, text=True, cwd=cwd, env=e, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def make_hook_repo(root, sb, gbin):
    """a scratch repo holding the leg + 6 tracked locks (3 inside the four directories), one commit, a scratch BARE remote, a REAL pre-push hook, and a linked worktree. -> dict."""
    must_be_outside(root, 'hook repo'); assert_not_in_repo(os.path.dirname(root), 'hook repo parent')
    sp = build_leg_repo(root, sb, init=False)
    for cmd in (['init', '-q', '-b', 'main', root], ['-C', root, 'add', '-A'], ['-C', root] + IDENT + ['commit', '-q', '-m', 'fixture']):
        rc, o, e = ggit(gbin, cmd)
        if rc: raise SystemExit('make_hook_repo: git %s rc %d %s' % (cmd[:3], rc, e[:200]))
    bare = root + '.remote.git'; must_be_outside(bare, 'bare remote')
    for cmd in (['init', '-q', '--bare', bare], ['-C', root, 'remote', 'add', 'origin', bare]):
        rc, o, e = ggit(gbin, cmd)
        if rc: raise SystemExit('make_hook_repo: git %s rc %d %s' % (cmd[:3], rc, e[:200]))
    hp = os.path.join(root, '.git', 'hooks', 'pre-push'); w(hp, HOOK_TEXT); os.chmod(hp, 0o755)
    wt = root + '.wt'; rc, o, e = ggit(gbin, ['-C', root, '-c', 'core.hooksPath=/dev/null', 'worktree', 'add', '--detach', '-q', wt])
    if rc: raise SystemExit('make_hook_repo: worktree add rc %d %s' % (rc, e[:200]))
    rc, gd, e = ggit(gbin, ['-C', wt, 'rev-parse', '--absolute-git-dir'])
    return {'root': root, 'bare': bare, 'wt': wt, 'wt_gitdir': gd.strip(), 'script': sp}


def parse_hook(log):
    d = {}
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_CONFIG_PARAMETERS', 'PWD', 'git'):
        m = re.search(r'(?m)^HOOK %s=(.*)$' % k, log); d[k] = m.group(1) if m else None
    m = re.search(r'(?m)^HOOK-LEG-RC=(\d+)$', log); d['leg_rc'] = int(m.group(1)) if m else None
    d['surface'] = parse_surface(log); d['fired'] = 'HOOK-START' in log
    return d


# PREDICTIONS (written before any run): (covered, total, listed) per script and shape
HOOK_PREDICT = {('prev', 'main'): (3, 6, 3), ('prev', 'wt'): (0, 6, 6), ('prev', 'wt_c'): (0, 6, 6), ('prev', 'gd_main'): (0, 6, 6), ('prev', 'gd_wt'): (0, 6, 6),
                ('head', 'main'): (3, 6, 3), ('head', 'wt'): (3, 6, 3), ('head', 'wt_c'): (3, 6, 3), ('head', 'gd_main'): (3, 6, 3), ('head', 'gd_wt'): (3, 6, 3)}


def hook_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); br = Bracket(clone); stamp = '%d' % int(time.time()); prev = P50['prev_head']
    scripts = [('prev', git_bytes(clone, prev, SCRIPT)), ('head', git_bytes(clone, head, SCRIPT))]
    ran = 0
    for gname, gbin, gpath in GITS:
        if not os.path.exists(gbin): print('%s GIT %s: %s ABSENT -> NOT RUN by name (never a pass)' % (now(), gname, gbin)); rc_all = 1; continue
        ver = ggit(gbin, ['--version'])[1].strip()
        print('%s ===== git %s = %s (%s); the hook\'s PATH puts the node/npm stubs first, then %s' % (now(), gname, gbin, ver, gpath))
        for sname, sb in scripts:
            tag = '%s_%s_%s' % (sname, gname, stamp)
            R = make_hook_repo(os.path.join(scratch, 'hook_' + tag), sb, gbin)
            assert R['wt_gitdir'].find('/worktrees/') > 0, R['wt_gitdir']
            pd, _ = make_pathdir(os.path.join(scratch, 'hookpath_' + tag))
            penv = {'PATH': pd + ':' + gpath}
            blob_ok = blob_id(open(R['script'], 'rb').read()) == blob_id(sb)
            shapes = [('main', R['root'], []), ('wt', R['wt'], []), ('wt_c', R['wt'], ['-c', 'gate84.probe=1'])]
            for shape, cwd, extra in shapes:
                log = os.path.join(scratch, 'hooklog_%s_%s' % (shape, tag)); br_name = 'push_%s' % shape
                rc, o, e = ggit(gbin, extra + ['-C', cwd, 'push', 'origin', 'HEAD:refs/heads/' + br_name], env=dict(penv, HOOKLOG=log))
                txt = open(log, encoding='utf-8', errors='replace').read() if os.path.exists(log) else ''
                h = parse_hook(txt); w(os.path.join(out, 'hook_%s_%s.log' % (shape, tag)), txt)
                landed = ggit(gbin, ['--git-dir', R['bare'], 'rev-parse', '--verify', '--quiet', 'refs/heads/' + br_name])[0] == 0
                s = h['surface']; got = (s['covered'], s['total'], len(s['listed'])) if s and s['covered'] is not None else None; want = HOOK_PREDICT[(sname, shape)]
                env_ok = (h['GIT_DIR'] == 'unset') if shape == 'main' else (h['GIT_DIR'] and '/worktrees/' in h['GIT_DIR'])
                cp_ok = (h['GIT_CONFIG_PARAMETERS'] not in (None, 'unset')) if shape == 'wt_c' else True
                ok = rc == 0 and landed and h['fired'] and h['leg_rc'] == 0 and got == want and env_ok and cp_ok and blob_ok
                if not ok: rc_all = 1
                ran += 1
                print('%s PUSH %-5s %-4s script %-4s via git %-8s (hook saw %s): push rc %d, ref landed in the scratch bare remote %s | hook fired %s | hook-logged GIT_DIR=%s%s GIT_CONFIG_PARAMETERS=%s | leg rc %s | %s | predicted %s -> %s%s' % (
                    now(), shape, '', sname, gname, (h['git'] or '?')[:40], rc, landed, h['fired'], (h['GIT_DIR'] or '?')[-44:], ' (env as expected: %s)' % env_ok, (h['GIT_CONFIG_PARAMETERS'] or '?')[:30], h['leg_rc'], sline(s), want, 'MATCH' if ok else 'DIFFER',
                    '' if blob_ok else ' | SCRIPT BLOB NOT THE ONE UNDER TEST'))
            # the inherited-GIT_DIR runs (no push): the leg run directly with GIT_DIR exported
            for shape, script_path, gd in (('gd_main', R['script'], os.path.join(R['root'], '.git')), ('gd_wt', os.path.join(R['wt'], 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh'), R['wt_gitdir'])):
                e2 = dict(GENV); e2.update({'PATH': pd + ':' + gpath, 'GIT_DIR': gd})
                rc, o, er, to = run(['/bin/bash', script_path], cwd=R['root'], env=e2, merge=True); s = parse_surface(o); w(os.path.join(out, 'hook_%s_%s.log' % (shape, tag)), o)
                got = (s['covered'], s['total'], len(s['listed'])) if s and s['covered'] is not None else None; want = HOOK_PREDICT[(sname, shape)]; ok = rc == 0 and got == want
                if not ok: rc_all = 1
                ran += 1
                print('%s INHERITED GIT_DIR %-7s script %-4s via git %-8s (GIT_DIR=%s): leg rc %d | %s | predicted %s -> %s' % (now(), shape, sname, gname, gd[-44:], rc, sline(s), want, 'MATCH' if ok else 'DIFFER'))
    print('%s hook instrument: %d scratch runs (real `git push` to scratch BARE remotes outside every repo, plus inherited-GIT_DIR runs); node/npm STUBS only; no npm, no network' % (now(), ran))
    if ran < 20: print('FAIL fewer runs than predicted (20): a git was NOT RUN'); rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


def case_run(scratch, stamp, tag, sb, kind, gbin='/usr/bin/git'):
    """one exit-code case -> (rc, output). Fresh scratch repo each time; node / npm stubs; git is the real /usr/bin/git unless the case stubs it."""
    root = os.path.join(scratch, 'case_%s_%s' % (kind, tag)); gm = None; env = {}; args = (); node, docker = '24', None
    if kind == 'nogit': sp = build_leg_repo(root, sb, init=False)
    elif kind == 'untracked':
        sp = build_leg_repo(root, sb, init=False); assert sh_git(['init', '-q', root])[0] == 0
    elif kind == 'WT':
        sp = build_leg_repo(root, sb, init=True)
        rc, o, e = ggit(gbin, ['-C', root] + IDENT + ['commit', '-q', '-m', 'fixture']); assert rc == 0, e
        wt = root + '.wt'; rc, o, e = ggit(gbin, ['-C', root, '-c', 'core.hooksPath=/dev/null', 'worktree', 'add', '--detach', '-q', wt]); assert rc == 0, e
        gd = ggit(gbin, ['-C', wt, 'rev-parse', '--absolute-git-dir'])[1].strip(); env = {'GIT_DIR': gd}; sp = os.path.join(wt, 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh')
    else: sp = build_leg_repo(root, sb, init=True)
    if kind == 'U': gm = 'LOG'
    elif kind in ('S1', 'S2', 'S3', 'TL', 'ENV0', 'ENV1'): gm = kind
    elif kind == 'GITDIR': env = {'GIT_DIR': os.path.join(root, '.git')}
    elif kind == 'failing': open(os.path.join(root, 'Blockchain/Dev/services/a/FAIL_ME'), 'w').write('x')
    elif kind == 'onedir': args = ('services/a',)
    elif kind == 'skip': node, docker = '18', 'down'
    pd, _ = make_pathdir(os.path.join(scratch, 'casepath_%s_%s' % (kind, tag)), node=node, git_mode=gm, docker=docker)
    rc, o, to = run_leg(sp, pd, root, args=args, env=env)
    return rc, o


CASES = ['U', 'GITDIR', 'WT', 'S1', 'S2', 'S3', 'TL', 'ENV0', 'ENV1', 'nogit', 'failing', 'onedir', 'untracked', 'skip']
# PREDICTED: the exit code of the head EQUALS the previous head's in every case (1 for `failing`, 0 elsewhere); the output is byte-identical in these 7 and different in the other 7
CASE_IDENTICAL = {'U', 'TL', 'nogit', 'failing', 'onedir', 'untracked', 'skip'}


def exitcodes_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); stamp = '%d' % int(time.time()); prev = P50['prev_head']; br = Bracket(clone)
    s_head, s_prev = git_bytes(clone, head, SCRIPT), git_bytes(clone, prev, SCRIPT)
    n_eq = 0; n_id = 0; n_df = 0
    for kind in CASES:
        rh, oh = case_run(scratch, stamp, 'head', s_head, kind); rp, op = case_run(scratch, stamp, 'prev', s_prev, kind)
        w(os.path.join(out, 'case_%s_head.out' % kind), oh); w(os.path.join(out, 'case_%s_prev.out' % kind), op)
        want_rc = 1 if kind == 'failing' else 0
        ident = oh == op; pred_ident = kind in CASE_IDENTICAL
        ok = rh == rp == want_rc and ident == pred_ident
        n_eq += 1 if rh == rp else 0; n_id += 1 if ident else 0; n_df += 0 if ident else 1
        print('%s CASE %-9s exit code head %d / previous head %d (equal: %s, want %d) | output %s (predicted %s) | head: %s | previous: %s -> %s' % (
            now(), kind, rh, rp, rh == rp, want_rc, 'IDENTICAL' if ident else 'DIFFERENT', 'identical' if pred_ident else 'different', sline(parse_surface(oh)), sline(parse_surface(op)), 'MATCH' if ok else 'DIFFER'))
        if not ok: rc_all = 1
    print('%s EXIT CODES: equal in %d of %d cases (the seat: 12 of 12 on its 12 cases); output byte-identical in %d, different in %d (the seat: 7 and 5 on its 12; the two extra cases here are S1 and the real linked worktree, both predicted different)' % (now(), n_eq, len(CASES), n_id, n_df))
    if n_eq != len(CASES): rc_all = 1
    if not br.close(): rc_all = 1
    return rc_all


# ---------------- tamper ----------------
T9_EDIT = ('not a git checkout - cannot list the tracked lockfiles this leg does not install"\n        return 0', 'not a git checkout - cannot list the tracked lockfiles this leg does not install"\n        return 1')
WRAP_RET = ('    )\n    return 0\n}\n\nFAILED=()', None)
FAILBLK = '    done\n    exit 1\nfi\n'
TAMPER = {
 '1450': dict(rows=[
    ('T1', 'the call is removed (the function is never reached)', [('if [ "$#" -eq 0 ]; then\n    report_surface\nfi\n', '')], [1, 2, 6, 7, 8, 9, 10, 12, 13, 14]),
    ('T2', 'the call is no longer guarded by `$# -eq 0`: it runs on a one-directory run too', [('if [ "$#" -eq 0 ]; then\n    report_surface\nfi\n', 'report_surface\n')], [4]),
    ('T3', 'the surface line is reworded (no "tracked package-lock.json file(s) were installed by this leg")', [('echo "  surface: $covered_n of $total tracked package-lock.json file(s) were installed by this leg"', 'echo "  surface: $covered_n of $total locks"')], [2, 6, 7, 14]),
    ('T4', 'the covered count is wrong (covered_n starts at 1: "4 of 6")', [('covered_n=0 total=0', 'covered_n=1 total=0')], [2, 6, 7, 14]),
    ('T5', 'the branches are swapped: the COVERED locks are listed and the outside ones counted as covered ("3 of 6" still reads right)',
     [('            covered_n=$((covered_n + 1))\n        else\n            outside=$((outside + 1))\n            lines="$lines    $lock"$\'\\n\'\n        fi',
       '            outside=$((outside + 1))\n            lines="$lines    $lock"$\'\\n\'\n        else\n            covered_n=$((covered_n + 1))\n        fi')], [1, 6, 7, 10]),
    ('T5b', 'the list names ALL six locks (covered ones too) under a heading that still says (3)', [('            covered_n=$((covered_n + 1))\n        else\n', '            covered_n=$((covered_n + 1)); lines="$lines    $lock"$\'\\n\'\n        else\n')], [6, 7, 10]),
    ('T6', 'the WRAPPER ends in `return 1` instead of `return 0` (the leg exits 1 on an all-OK run)', [('    )\n    return 0\n}\n\nFAILED=()', '    )\n    return 1\n}\n\nFAILED=()')], [3, 6, 7, 8, 9, 10, 12, 13, 14]),
    ('T7', 'WORDING: the heading line "NOT installed by this leg" is dropped (the paths are still listed)', [('        echo "  NOT installed by this leg ($outside):"\n', '')], [6, 7, 10]),
    ('T8', 'WRONG COUNT in the heading: "NOT installed by this leg (99):" (the surface line stays right)', [('echo "  NOT installed by this leg ($outside):"', 'echo "  NOT installed by this leg (99):"')], [6, 7, 10]),
    ('T9', 'gate83\'s T9 AS WRITTEN: the early return on a non-git checkout becomes `return 1` (the seat claims an EQUIVALENT MUTANT: the wrapper\'s `return 0` discards the body status)', [T9_EDIT], []),
    ('T9x', 'T9 AND the wrapper\'s `return 0` removed (the subshell status propagates: the seat says cell 12 fails)', [T9_EDIT, ('    )\n    return 0\n}\n\nFAILED=()', '    )\n}\n\nFAILED=()')], [12]),
    ('T10', 'the guard on CHECKED is removed (the unguarded expansion): a clean run with a non-empty CHECKED is unaffected on bash 3.2 (the seat SKIPPED this row)', [('${CHECKED[@]+"${CHECKED[@]}"}', '"${CHECKED[@]}"')], []),
    ('T11', 'the surface prints on a FAILING run too (a call before the failing exit)', [(FAILBLK, '    done\n    report_surface\n    exit 1\nfi\n')], [11]),
    ('T12', 'REGRESSION OF THE LEG ITSELF: the exit code of the failing path becomes `exit 0`', [(FAILBLK, '    done\n    exit 0\nfi\n')], [5, 11]),
    ('MT1', 'the seat\'s "env-not-cleared": the `unset "$v"` is neutralised (the local variables stay inherited)', [('unset "$v"\n', ': "$v"\n')], [6, 7]),
    ('MT2', 'the --show-prefix guard is made dead (`|| true; false && {`)', [('prefix="$(git rev-parse --show-prefix 2>/dev/null)" || {', 'prefix="$(git rev-parse --show-prefix 2>/dev/null)" || true; false && {')], [8]),
    ('MT3', 'the ls-files guard is made dead', [('listing="$(git -C "$top" ls-files \'*package-lock.json\' 2>/dev/null)" || {', 'listing="$(git -C "$top" ls-files \'*package-lock.json\' 2>/dev/null)" || true; false && {')], [9]),
    ('MT4', 'the --show-toplevel guard is made dead (the seat: cell 12 ALONE catches it)', [('top="$(git rev-parse --show-toplevel 2>/dev/null)" || {', 'top="$(git rev-parse --show-toplevel 2>/dev/null)" || true; false && {')], [12]),
    ('MT5', 'the "GIT_DIR must be among the names" check is made dead', [('if [ "$git_env_has_dir" -ne 1 ]; then', 'if false; then')], [13]),
    ('MT6', 'the empty-line skip (`[ -n "$lock" ] || continue`) is dropped', [('        [ -n "$lock" ] || continue   # KS-1426: a here-string of an empty listing yields one empty line\n', '')], [14]),
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
            elif edits == 'NOOP': new = head_src.rstrip('\n') + '\n# gate84-noop\n'
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
            good = c == (14, 0) and rc == 0; verdict = 'OK' if good else 'FAIL: %s rc %d' % (c, rc); rc_all |= 0 if good else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if c[1] == 0 else 'caught: %d failed (%s)' % (c[1], cfmt(reds))) + ' | kit-builder prediction %s: %s' % (cfmt(pred), 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-110s landed %s restored %s | rc %d counts %s | %s' % (now(), tid, name[:110], ok_land, back, rc, c, verdict))
        if not ok_land or not back: rc_all = 1
        if tid not in ('HEAD', 'CONTROL') and c is not None and sorted(pred) != reds: rc_all = 1
    return rc_all


# ---------------- docs / compose (ONE PR; the G83-1 fix: the base is merge-base(develop, head), never head^) ----------------
def insertion(basetxt, headtxt):
    la, lb = basetxt.split('\n'), headtxt.split('\n')
    ops = [x for x in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if x[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': raise SystemExit('not a pure insertion: %s' % ops[:3])
    _, i1, _, j1, j2 = ops[0]; return i1, lb[j1:j2]


def flow_numbers(txt): return [int(x) for x in re.findall(r'<h2>(\d+)\.', txt)]


def h2_counts(txt):
    c = {}
    for x in re.findall(r'<h2[^>]*>(.*?)</h2>', txt, re.S): c[x] = c.get(x, 0) + 1
    return c


def merge_file(cur, basef, other):
    rc, o, e, to = run(['git', 'merge-file', '-p', '-L', 'ours', '-L', 'base', '-L', 'theirs', cur, basef, other], timeout=60)
    return rc, o


def own_nondoc(clone, base, head):
    rc, o, e = cgit(clone, ['diff', '--name-only', base, head])
    if rc: raise SystemExit('git diff --name-only %s %s rc %d: %s (an unresolvable head / base can NOT read as "no paths")' % (base[:12], head[:12], rc, e.strip()[:120]))
    return sorted(x for x in o.decode().split('\n') if x and x not in DOCS)


def keep_both(devtxt, frag):
    """[g84] the keep-both onto the develop text: the fragment goes immediately before the closing `</body>\\n</html>\\n` (the exact tail), nowhere else."""
    if not devtxt.endswith(TAIL): raise SystemExit('the develop doc does not end with %r' % TAIL)
    return devtxt[:-len(TAIL)] + frag + TAIL


def compose_tree(clone, develop, head, base, scratch, tag):
    """a TEMP INDEX tree over DEVELOP: #1450's own non-doc paths from its head (each asserted UNCHANGED between base and develop, else the head blob would silently revert develop), the docs keep-both.
    -> dict(full, nodocs, docs). Writes objects into the KIT CLONE only."""
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
    for path in own_nondoc(clone, base, head):
        if blob(clone, base, path) and blob(clone, base, path) != blob(clone, develop, path): moved.append(path)
        m = [l.split()[0] for l in git(clone, 'ls-tree', head, '--', path).strip().split('\n') if l][0]
        put(path, git_bytes(clone, head, path), m)
    if moved: raise SystemExit('develop MOVED a path of the PR since its base: %s (the head blob would revert it)' % moved)
    docs_texts = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); ok, frag, why = exact_tail_insert(git_bytes(clone, base, d).decode('utf-8'), git_bytes(clone, head, d).decode('utf-8'))
        if not ok: raise SystemExit('%s: the head doc is not an exact tail insert against the base: %s' % (d, why))
        docs_texts[d] = keep_both(dv, frag); put(d, docs_texts[d].encode('utf-8'))
    rc, o, e = cgit(clone, ['write-tree'], env=env)
    if rc: raise SystemExit('write-tree: ' + e)
    full = o.decode().strip()
    for d in DOCS:
        bid = cgit(clone, ['rev-parse', '%s:%s' % (develop, d)])[1].decode().strip(); cgit(clone, ['update-index', '--cacheinfo', '100644,%s,%s' % (bid, d)], env=env)
    rc, o, e = cgit(clone, ['write-tree'], env=env); nodocs = o.decode().strip()
    return dict(full=full, nodocs=nodocs, docs=docs_texts)


def conflicts_of(clone, a, b):
    rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', a, b])
    lines = o.decode('utf-8', 'replace').strip().split('\n'); conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
    return rc, (lines[0] if lines else ''), sorted(set(conf)), e


def compose_cmd(clone, develop, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); os.makedirs(scratch, exist_ok=True); rc_all = 0; prev = P50['prev_head']
    try: mb, info = docs_base(clone, develop, head, base)
    except SystemExit as e: print('REFUSED: %s' % e); return 2
    print('%s docs parent: merge-base(develop %s, head %s) = %s == --base1450 %s ; head^ = %s (the previous head) is NOT used (G83-1) ; no companion in the batch' % (now(), develop[:12], head[:12], mb[:12], base[:12], info['head_parent'][:12]))
    try: t = compose_tree(clone, develop, head, base, scratch, 'SOLO')
    except SystemExit as e: print('FAIL compose: %s' % e); return 1
    print('  TEMP-INDEX TREE (develop + #1450): FULL %s | CODE-ONLY (docs reset to develop) %s' % (t['full'], t['nodocs']))
    want = sorted(own_nondoc(clone, base, head)); rc, o, e = cgit(clone, ['diff', '--name-only', develop, t['nodocs']]); got = sorted(x for x in o.decode().split('\n') if x)
    print('  develop..CODE-ONLY-tree paths == #1450\'s own non-doc paths: %s (%s)' % (got == want, got)); rc_all |= 0 if got == want else 1
    for p in want:
        a = cgit(clone, ['rev-parse', '%s:%s' % (t['nodocs'], p)])[1].decode().strip(); b = cgit(clone, ['rev-parse', '%s:%s' % (head, p)])[1].decode().strip()
        if a != b: print('  FAIL composed blob of %s != the head blob' % p); rc_all = 1
    rc, tree, conf, er = conflicts_of(clone, develop, head)
    print('  merge-tree --write-tree --name-only develop %s + HEAD %s: rc %d (1 = conflicts) tree %s | conflicted paths %s | PREDICTED exactly the two docs: %s' % (develop[:12], head[:12], rc, tree[:12], conf, 'MATCH' if conf == sorted(DOCS) and rc == 1 else 'DIFFER'))
    if not (rc == 1 and conf == sorted(DOCS)): rc_all = 1
    rc2, tree2, conf2, er2 = conflicts_of(clone, develop, prev)
    print('  merge-tree --write-tree --name-only develop + the PREVIOUS head %s: rc %d conflicted paths %s (the seat: the same two docs before AND after) -> %s' % (prev[:12], rc2, conf2, 'MATCH' if conf2 == sorted(DOCS) and rc2 == 1 else 'DIFFER'))
    if not (rc2 == 1 and conf2 == sorted(DOCS)): rc_all = 1
    rcc, treec, confc, erc = conflicts_of(clone, develop, base)
    print('  CONTROL merge-tree develop + the BASE (an ancestor of develop): rc %d conflicted paths %s -> the instrument reads a CLEAN merge as rc 0 / none: %s' % (rcc, confc or 'none', rcc == 0 and not confc))
    if not (rcc == 0 and not confc): rc_all = 1
    json.dump(dict(full=t['full'], nodocs=t['nodocs'], conflicts=conf), open(os.path.join(out, 'compose_trees.json'), 'w'), indent=1)
    return rc_all


def docs_cmd(clone, develop, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    assert_not_in_repo(scratch, 'scratch'); tmp = canon_tmp(scratch); prev = P50['prev_head']; D = K['docs_composition']
    try: mb, info = docs_base(clone, develop, head, base)
    except SystemExit as e: print('REFUSED: %s' % e); return 2
    print('%s docs parent: merge-base(develop %s, head %s) = %s (== --base1450 %s: %s); head^ = %s (the previous head) is NOT used; the fragment is extracted against the MERGE-BASE (G83-1)' % (now(), develop[:12], head[:12], mb[:12], base[:12], mb == base, info['head_parent'][:12]))
    texts = {}; frags = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); bt = git_bytes(clone, mb, d).decode('utf-8'); ht = git_bytes(clone, head, d).decode('utf-8'); pt = git_bytes(clone, prev, d).decode('utf-8'); nm = os.path.basename(d)
        ok, frag, why = exact_tail_insert(bt, ht); want = D['fragment_bytes'][d]
        if not ok: print('FAIL %s: not an exact tail insert against the merge-base: %s' % (nm, why)); return 1
        frags[d] = frag; fb = len(frag.encode('utf-8'))
        fnum = flow_numbers(dv)
        print('%s %s: fragment against the merge-base %d B (kit %d: %s) | develop flow numbers in DOCUMENT order, tail %s (max %s; next free by max+1 %s; kit tail at draft %s) | develop already holds the fragment: %s' % (
            now(), nm, fb, want, fb == want, fnum[-8:], max(fnum) if fnum else 'n/a', (max(fnum) + 1) if fnum else 'n/a', D['develop_tail_at_draft'] if d == DOCS[0] else 'n/a', frag in dv))
        if fb != want or frag in dv: rc_all = 1
        sd = os.path.join(scratch, 'docs_' + nm[:12]); os.makedirs(sd, exist_ok=True); w(os.path.join(sd, 'develop.html'), dv); w(os.path.join(sd, 'base.html'), bt); w(os.path.join(sd, 'head.html'), ht)
        rc, o = merge_file(os.path.join(sd, 'develop.html'), os.path.join(sd, 'base.html'), os.path.join(sd, 'head.html')); w(os.path.join(out, 'merge_alone_%s.txt' % nm[:10]), o)
        print('  #1450 alone onto develop, textual merge-file: %s hunk(s) (a conflict = develop has landed blocks at the SAME insertion point; expected 1 per doc, the PR reads dirty)' % (rc if rc >= 0 else 'ERR'))
        if rc != 1: rc_all = 1
        # wrong-parent CONTROLS: the instrument REFUSES them
        okp, _, whyp = exact_tail_insert(pt, ht); okd, _, whyd = exact_tail_insert(dv, ht)
        print('  CONTROL wrong parent head^ (%s): exact tail insert? %s (%s) | CONTROL develop given as the base: %s (%s) -> both must be REFUSED (False)' % (prev[:12], okp, whyp, okd, whyd))
        if okp or okd: rc_all = 1
        comp = keep_both(dv, frag); texts[d] = comp
        once = comp.count(frag) == 1 and dv.count(frag) == 0; minus = comp.replace(frag, '', 1) == dv
        cd = h2_counts(comp); dd = h2_counts(dv); extra = dict((k, cd.get(k, 0) - dd.get(k, 0)) for k in set(cd) | set(dd) if cd.get(k, 0) != dd.get(k, 0)); dup_h2 = sorted(k[:50] for k, v in cd.items() if v > dd.get(k, 0) and v > 1 and k in dd)
        fl = flow_numbers(comp); fl_extra = [n for n in set(fl) if fl.count(n) != flow_numbers(dv).count(n)]
        print('     KEEP-BOTH SOLO: fragment count WANT 1 -> %d (%s) | composed minus the fragment == develop byte for byte: %s | headings added vs develop: %s (want exactly the one new heading) | any pre-existing heading now duplicated: %s | flow numbers that changed count: %s (want [53] on the flow doc, [] on the cheat doc) | flow tail %s' % (
            comp.count(frag), once, minus, [k[:60] for k in extra], dup_h2 or 'none', sorted(fl_extra), fl[-7:] if d == DOCS[0] else 'n/a'))
        if not once or not minus or len(extra) != 1 or dup_h2 or (d == DOCS[0] and sorted(fl_extra) != [53]) or (d != DOCS[0] and fl_extra): rc_all = 1
        w(os.path.join(sd, 'composed.html'), comp)
    def small_tree(dest):
        if not os.path.exists(dest): extract(clone, develop, existing(clone, develop, SMALL_PATHS), dest)
        assert_not_in_repo(dest, 'matrix tree'); return dest
    mx = D['matrix_suite']; results = {}
    dup = dict((d, keep_both(keep_both(git_bytes(clone, develop, d).decode('utf-8'), frags[d]), frags[d])) for d in DOCS)
    for lab, kind in [('develop tree (control)', None), ('COMPOSED SOLO', 'C'), ('DROP-A-BLOCK control (no #1450 block)', 'DROP'), ('DUPLICATE-A-BLOCK control (#1450 block TWICE)', 'DUP')]:
        td = os.path.join(scratch, 'mx_' + re.sub(r'\W+', '_', lab)[:22]); small_tree(td)
        if kind:
            for d in DOCS:
                txt = texts[d] if kind == 'C' else (git_bytes(clone, develop, d).decode('utf-8') if kind == 'DROP' else dup[d]); w(os.path.join(td, d), txt)
        rc, o, e, to = run(['/bin/bash', os.path.join(td, mx)], cwd=td, env={'TMPDIR': tmp}, timeout=300, merge=True); c = pcounts(o); inval = 'is missing' in o
        w(os.path.join(out, 'matrix_%s.out' % re.sub(r'\W+', '_', lab)[:22]), o)
        print('%s html_docs_matrix on %-48s rc %d%s counts %s%s' % (now(), lab, rc, ' TIMEOUT' if to else '', c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
        results[lab] = (rc, c, inval)
        if inval: rc_all = 1
    if results['COMPOSED SOLO'][1] != (12, 0) or results['develop tree (control)'][1] != (12, 0): rc_all = 1
    f53 = frags[DOCS[0]]
    cnt_drop = git_bytes(clone, develop, DOCS[0]).decode('utf-8').count(f53); cnt_dup = dup[DOCS[0]].count(f53); cnt_ok = texts[DOCS[0]].count(f53)
    d_drop, d_dup = results['DROP-A-BLOCK control (no #1450 block)'], results['DUPLICATE-A-BLOCK control (#1450 block TWICE)']
    print('CONTROLS (gate81 G81-2 / gate83 G83-1): html_docs_matrix is BLIND to a dropped block (counts %s) and to a DUPLICATED block (counts %s) | the per-fragment COUNT reads composed %d, dropped %d, duplicated %d -> the COUNT %s' % (
        d_drop[1], d_dup[1], cnt_ok, cnt_drop, cnt_dup, 'CATCHES both' if (cnt_ok == 1 and cnt_drop == 0 and cnt_dup == 2) else 'DOES NOT CATCH'))
    if not (d_drop[1] == (12, 0) and d_dup[1] == (12, 0) and cnt_ok == 1 and cnt_drop == 0 and cnt_dup == 2): rc_all = 1
    return rc_all


# ---------------- selftest ----------------
def selftest():
    tmpd = os.environ.get('TMPDIR', '')
    if not tmpd or os.path.realpath(tmpd) != tmpd.rstrip('/') or in_repo(tmpd):
        print('REFUSED: the selftest runs only with TMPDIR set to a CANONICAL (realpath) directory outside every git repo; TMPDIR=%r (realpath %r, inside a repo: %s)' % (tmpd, os.path.realpath(tmpd) if tmpd else None, in_repo(tmpd) if tmpd and os.path.isdir(tmpd) else 'n/a')); return 2
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(os.path.realpath(tmpd) == tmpd.rstrip('/') and not in_repo(tmpd), 'TMPDIR %s is canonical (realpath equal) and NOT inside a repo' % tmpd)
    tmpd = tempfile.mkdtemp(prefix='g84st_', dir=tmpd)   # a fresh work dir per run (nothing is deleted; the TMPDIR keeps the residue)
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
    rep(pcounts('x\n  4 passed, 10 failed\n') == (4, 10) and pcounts('nothing') is None, 'pcounts reads "N passed, M failed" and nothing else')
    fl = "PASS: a\nFAIL: the leg does not name the locks outside its four directories: x\nFAIL: CONTROL failing lock: rc=0\nFAIL: CONTROL failing run: rc=0\nFAIL: CONTROL failing --show-toplevel: rc=1\nFAIL: in a linked worktree (gitdir 'x'): rc=0\n"
    rep(red_cells(fl) == [1, 5, 7, 11, 12] and red_cells('PASS: x\n') == [], 'red_cells maps FAIL lines of ALL 14 cells (incl. the three "CONTROL failing ..." texts apart) and reads nothing from PASS lines')
    rep(len(CELLRX) == 14 and [c for c, _ in CELLRX] == list(range(1, 15)), 'CELLRX covers cells 1..14')
    s = parse_surface('All 3 ...\n  surface: 0 of 6 tracked package-lock.json file(s) were installed by this leg\n  NOT installed by this leg (6):\n    a/package-lock.json\n    b/package-lock.json\n')
    rep(s and s['covered'] == 0 and s['total'] == 6 and s['outside_n'] == 6 and s['listed'] == ['a/package-lock.json', 'b/package-lock.json'] and s['msg'] is None, 'parse_surface reads the count, the heading and the listed paths')
    s = parse_surface('  surface: not a git checkout - cannot list the tracked lockfiles this leg does not install\n')
    rep(s and s['msg'].startswith('not a git checkout') and s['covered'] is None, 'parse_surface reads the not-a-git-checkout message')
    s = parse_surface("  surface: git's list of repository-local variables is unusable - cannot list the tracked lockfiles this leg does not install\n")
    rep(s and s['msg'].startswith("git's list of repository-local variables is unusable"), 'parse_surface reads the NEW unusable-variable-list message')
    s = parse_surface("  surface: git could not report this directory's path inside the checkout - cannot list the tracked lockfiles this leg does not install\n")
    rep(s and s['msg'].startswith('git could not report'), 'parse_surface reads the NEW --show-prefix message')
    rep(parse_surface('All 3 standalone lock(s) pass\n') is None, 'parse_surface returns None when there is no surface line')
    rep(surface_key(parse_surface('  surface: 3 of 6 tracked package-lock.json file(s) were installed by this leg\n')) == '3 of 6', 'surface_key renders "3 of 6"')
    r1 = keep_both('x\n' + TAIL, 'H53\n'); rep(r1 == 'x\nH53\n' + TAIL and r1.count('H53') == 1, 'keep_both: the fragment goes immediately before the exact closing tags, once')
    rep(keep_both('x\n' + TAIL, 'H53\n').count('H54') == 0, 'CONTROL: a composition keeping one block reads the others ABSENT (the count check can fail)')
    try: keep_both('no body', 'a\n'); rep(False, 'a doc with no closing tail was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a develop doc without the exact tail -> refused')
    ia, fa = insertion('x\n</body>\n', 'x\nH53\n</body>\n'); rep(ia == 1 and fa == ['H53'], 'insertion reads the block and its base position')
    try: insertion('x\n</body>\n', 'y\n</body>\n'); rep(False, 'a non-insertion was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a replaced base line is not a pure insertion -> refused')
    rep(flow_numbers('<h2>50. a</h2><h2>53. b</h2><h2>54. c</h2>') == [50, 53, 54], 'flow_numbers reads <h2>NN.</h2> headings')
    c1_ = h2_counts('<h2>50. a</h2><h2>50. a</h2><h2>b</h2>'); rep(c1_ == {'50. a': 2, 'b': 1}, 'h2_counts counts duplicated headings (the G83-1 symptom: a block present TWICE)')
    # the G83-1 fix: docs_base on a toy history: base B, develop D (child of B), branch H1 (child of B) then H2 (child of H1)
    toy = os.path.join(tmpd, 'toy_hist'); os.makedirs(toy); gi = lambda *a: cgit(toy, list(a), env={'GIT_AUTHOR_NAME': 'g', 'GIT_AUTHOR_EMAIL': 'x@x', 'GIT_COMMITTER_NAME': 'g', 'GIT_COMMITTER_EMAIL': 'x@x'})
    assert sh_git(['init', '-q', toy])[0] == 0
    def commit(msg, fname, content):
        open(os.path.join(toy, fname), 'w').write(content); gi('add', '-A'); gi('commit', '-q', '-m', msg); return gi('rev-parse', 'HEAD')[1].decode().strip()
    Bc = commit('base', 'f', 'b\n'); gi('checkout', '-q', '-b', 'br'); H1 = commit('h1', 'f', 'b\nh1\n'); H2 = commit('h2', 'f', 'b\nh2\n'); gi('checkout', '-q', Bc); gi('checkout', '-q', '-b', 'dv'); Dv = commit('dev', 'g', 'd\n')
    bb, inf = docs_base(toy, Dv, H2, Bc)
    rep(bb == Bc and bb != H1 and inf['head_parent'] == H1 and not inf['merge_base_is_head_parent'], '[g84] G83-1 FIX: docs_base picks the BRANCH POINT (merge-base), not head^ (H2^ = H1): base %s, head^ %s' % (bb[:8], H1[:8]))
    try: docs_base(toy, Dv, H2, H1); rep(False, 'a pinned base that is not the merge-base was ACCEPTED')
    except SystemExit as e: rep('pinned branch point' in str(e), '[g84] ARM: a pinned base that is NOT the merge-base (head^ given as the base) -> REFUSED, never guessed')
    try: docs_base(toy, Dv, Dv, None); rep(False, 'head == develop was ACCEPTED')
    except SystemExit as e: rep('ALREADY in develop' in str(e), '[g84] ARM: a head already in develop (merge-base == head) -> refused')
    try: docs_base(toy, '1' * 40, H2, None); rep(False, 'an unresolvable develop was ACCEPTED')
    except SystemExit: rep(True, '[g84] ARM: an unresolvable develop -> refused (never read as "not landed")')
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
    # the stub machinery on a toy leg: each stub changes what the toy sees, and the stub log shows it took effect
    toyleg = ('#!/bin/bash\nprefix="$(git rev-parse --show-prefix)"; echo "prefix=[$prefix]"\ntl="$(git rev-parse --show-toplevel)"; echo "tl=[${tl:+set}]"\nev="$(git rev-parse --local-env-vars | head -1)"; echo "ev=[$ev]"\n')
    root = os.path.join(tmpd, 'toy'); os.makedirs(os.path.join(root, 'sub')); open(os.path.join(root, 'sub', 'f'), 'w').write('x\n'); w(os.path.join(root, 'sub', 'toy.sh'), toyleg)
    assert sh_git(['init', '-q', root])[0] == 0
    outs = {}
    for gm in ('LOG', 'S1', 'S2', 'TL', 'ENV0', 'ENV1'):
        pdm, lgm = make_pathdir(os.path.join(tmpd, 'pd_' + gm), git_mode=gm); rcm, om, _ = run_leg(os.path.join(root, 'sub', 'toy.sh'), pdm, os.path.join(root, 'sub')); outs[gm] = (om, open(lgm).read())
    rep('prefix=[sub/]' in outs['LOG'][0] and 'tl=[set]' in outs['LOG'][0] and 'ev=[GIT_ALTERNATE_OBJECT_DIRECTORIES]' in outs['LOG'][0], 'stub LOG CONTROL: the real git answers prefix `sub/`, a toplevel and the first local-env name')
    rep('prefix=[]' in outs['S2'][0] and '--show-prefix' in outs['S2'][1] and 'tl=[set]' in outs['S2'][0], 'stub S2: --show-prefix reads EMPTY while the toplevel still answers, and the stub log shows the call')
    rep('tl=[]' in outs['TL'][0] and 'prefix=[sub/]' in outs['TL'][0] and '--show-toplevel' in outs['TL'][1], 'stub TL: --show-toplevel reads EMPTY while the prefix still answers, and the stub log shows the call')
    rep('ev=[]' in outs['ENV0'][0] and 'prefix=[sub/]' in outs['ENV0'][0] and '--local-env-vars' in outs['ENV0'][1] and 'ev=[]' in outs['ENV1'][0], 'stubs ENV0 / ENV1: --local-env-vars reads EMPTY (rc 0 / rc 1) while the prefix still answers, and the stub log shows the call')
    rep('prefix=[]' in outs['S1'][0] and 'tl=[]' in outs['S1'][0] and outs['S1'][1].strip() != '', 'stub S1: every git call fails (empty output) and is logged')
    fn = function_text('a\nfoo() {\n  :\n}\nb\n', 'foo'); rep(fn == 'foo() {\n  :\n}\n', 'function_text extracts one function')
    try: function_text('foo() {\n}\nfoo() {\n}\n', 'foo'); rep(False, 'a function defined twice was ACCEPTED')
    except SystemExit: rep(True, 'ARM: function_text refuses a function defined twice')
    sub_pd, _ = make_pathdir(os.path.join(tmpd, 'pdsub'), node='18', docker='down')
    rep(open(os.path.join(sub_pd, 'node')).read().strip().endswith('echo 18') and os.path.exists(os.path.join(sub_pd, 'docker')), 'make_pathdir: node answers 18 and docker is stubbed down for the advisory-SKIP arm')
    pd_ = os.path.join(tmpd, 'applytest'); os.makedirs(pd_); open(os.path.join(pd_, 'a.txt'), 'w').write('one\ntwo\n')
    pt = os.path.join(tmpd, 'p.diff'); open(pt, 'w').write('--- a/a.txt\n+++ b/a.txt\n@@ -1,2 +1,3 @@\n one\n+mid\n two\n')
    r1_ = run(['git', 'apply', '-p1', pt], cwd=pd_)[0]; r2_ = run(['git', 'apply', '--check', '-p1', pt], cwd=pd_)[0]
    rep(r1_ == 0 and r2_ != 0 and open(os.path.join(pd_, 'a.txt')).read() == 'one\nmid\ntwo\n', 'git apply outside a repo: the first application lands, a SECOND application is refused (the payload arm\'s control)')
    # [g84] the hook instrument's parts: the hook text is valid bash, parse_hook reads a log, the prediction table is complete
    hp = os.path.join(tmpd, 'hook_text.sh'); w(hp, HOOK_TEXT); rep(run(['/bin/bash', '-n', hp])[0] == 0, '[g84] HOOK_TEXT is valid bash (bash -n)')
    ph = parse_hook('HOOK-START\nHOOK GIT_DIR=/x/.git/worktrees/wt\nHOOK GIT_WORK_TREE=unset\nHOOK GIT_CONFIG_PARAMETERS=unset\nHOOK PWD=/x\nHOOK git=/usr/bin/git git version 2.50.1\n  surface: 0 of 6 tracked package-lock.json file(s) were installed by this leg\nHOOK-LEG-RC=0\n')
    rep(ph['fired'] and ph['GIT_DIR'] == '/x/.git/worktrees/wt' and ph['leg_rc'] == 0 and ph['surface']['covered'] == 0 and parse_hook('')['fired'] is False, '[g84] parse_hook reads the logged GIT_DIR, the leg rc and the surface line; an empty log reads NOT FIRED')
    rep(set(HOOK_PREDICT) == set((s_, h_) for s_ in ('prev', 'head') for h_ in ('main', 'wt', 'wt_c', 'gd_main', 'gd_wt')), '[g84] the hook prediction table covers 2 scripts x 5 shapes')
    rep(set(CASES) >= CASE_IDENTICAL and len(CASES) == 14 and len(CASE_IDENTICAL) == 7, '[g84] the exit-code case table: 14 cases, 7 predicted identical')
    for pr_, T in TAMPER.items():
        ok = all(len(rw) == 4 for rw in T['rows']); rep(ok, '#%s tamper table: %d rows, each (id, name, edits, predicted red cells)' % (pr_, len(T['rows'])))
    rep(len(TAMPER['1450']['rows']) == 20 and len(set(r[0] for r in TAMPER['1450']['rows'])) == 20, 'the tamper table is the declared size (20 rows, ids distinct)')
    rep(all(all(isinstance(c, int) and 1 <= c <= 14 for c in r[3]) for r in TAMPER['1450']['rows']), 'every predicted red cell is a cell number 1..14')
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
        if cmd == 'hook': return hook_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'exitcodes': return exitcodes_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'payload': return payload_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'stubs': return stubs_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'realtree': return realtree_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'cwd': return cwd_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'siblings': return siblings_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd in ('compose', 'docs'):
            cl = req(A, '--clone'); dev = req(A, '--develop', True)
            return (compose_cmd if cmd == 'compose' else docs_cmd)(cl, dev, req(A, '--head1450', True), req(A, '--base1450', True), req(A, '--scratch'), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
