#!/usr/bin/env python3
"""lib_gate59.py — shared helpers for the gate59 check scripts (a NEW COPY of lib_gate57.py: the git / guard / GH / Checks / run core).
  git()   READ verbs only (show, ls-tree, rev-parse, cat-file, log, diff, rev-list, merge-base, ls-remote, status).
  wgit()  WRITE verbs (checkout, commit-tree, merge-tree, hash-object, read-tree, update-index, write-tree, worktree) ONLY in a repository /
          worktree whose path is NOT under kit forbidden_root (lexically AND by realpath): your scratch clone. The Secuura checkout can never
          be written through this lib.
  move_out()  shutil.move, never os.replace (gate57's G57-KIT-1: os.replace across volumes raised EXDEV mid-run).
Imported by c1..c6 and the census; never run on its own."""
import json, os, re, subprocess, datetime, difflib, urllib.request, urllib.error, time, sys, hashlib, shutil

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'ls-tree', 'rev-parse', 'cat-file', 'log', 'diff', 'rev-list', 'merge-base', 'ls-remote', 'status', 'grep'}
WRITE_VERBS = {'checkout', 'commit-tree', 'merge-tree', 'hash-object', 'read-tree', 'update-index', 'write-tree', 'worktree'}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def opt_factory(A):
    return lambda n, d=None: A[A.index(n) + 1] if n in A and A.index(n) + 1 < len(A) else d


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gate59.git allows read verbs only, got %r' % a[0])
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def _under(p, root):
    p, root = os.path.normpath(p), os.path.normpath(root)
    return p == root or p.startswith(root + os.sep)


def forbidden_root():
    """kit forbidden_root; G59_FORBIDDEN_ROOT overrides it ONLY so a REFUSAL ARM can be driven with a scratch path"""
    return os.environ.get('G59_FORBIDDEN_ROOT') or K['forbidden_root']


def guard_scratch(path, what='repository'):
    """a repo / worktree that may be WRITTEN or RUN in: never under the forbidden root, lexically AND by realpath (SystemExit 2, nothing run)"""
    lex = os.path.abspath(path); fr = forbidden_root()
    if _under(lex, fr) or _under(os.path.realpath(lex), fr):
        print('REFUSING: %s %s is under %s — write / run only in YOUR OWN scratch clone or worktree, never the shared checkout or a builder worktree (nothing was run)' % (what, lex, fr))
        raise SystemExit(2)
    return lex


def guard_out(path, create=True):
    """an output dir: refuse a path under the forbidden root unless under the QA reports root; lexical first, then realpath of the nearest
    existing ancestor; then mkdir"""
    lex = os.path.abspath(path); fr, rr = forbidden_root(), K['reports_root']
    if _under(lex, fr) and not _under(lex, rr):
        print('REFUSING: %s is inside %s but not under the QA reports root (nothing was created or run)' % (lex, fr)); raise SystemExit(2)
    anc = lex
    while not os.path.exists(anc):
        anc = os.path.dirname(anc)
    real = os.path.join(os.path.realpath(anc), os.path.relpath(lex, anc)) if anc != lex else os.path.realpath(lex)
    if _under(real, fr) and not _under(real, rr):
        print('REFUSING: %s resolves to %s inside %s (nothing was created or run)' % (lex, real, fr)); raise SystemExit(2)
    if create:
        os.makedirs(lex, exist_ok=True)
    return lex


def wgit(repo, *a, check=True, env=None, inp=None):
    if a[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('REFUSING: lib_gate59.wgit verb %r not allowed' % a[0])
    guard_scratch(repo)
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True, env=e, input=inp)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def has_commit(repo, sha):
    return git(repo, 'cat-file', '-e', sha + '^{commit}', check=False)[0] == 0


def show(repo, sha, path):
    """blob text at sha:path, resolved with cat-file -e first (rev-parse ECHOES an unresolved path); None when absent"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    r = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (sha, path)], capture_output=True)
    return r.stdout.decode('utf-8')


def blob(repo, sha, path):
    l = git(repo, 'ls-tree', sha, '--', path).strip()
    return l.split()[2] if l else None


def tree(repo, rev):
    return git(repo, 'rev-parse', rev + '^{tree}').strip()


def sha256(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()


def move_out(src, dst_dir, name=None):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name or os.path.basename(src))
    shutil.move(src, dst)
    return dst


def gh_token():
    tok = ''
    for l in open(K['secuura_env'], encoding='utf-8'):
        if l.startswith('GH_TOKEN='):
            tok = l.split('=', 1)[1].strip().strip('"').strip("'")
    return tok


class GH:
    """read-only GitHub REST GETs; offline=<dir> replays <dir>/<url with /?&= -> __>.json fixtures (SIM, never evidence)"""
    def __init__(self, offline=None):
        self.off = offline; self.tok = None if offline else gh_token()
        if not offline and not self.tok:
            print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)

    def get(self, u):
        if self.off:
            f = os.path.join(self.off, re.sub(r'[/?&=]', '__', u) + '.json')
            if not os.path.isfile(f):
                print('OFFLINE fixture missing: %s' % f); raise SystemExit(3)
            return json.load(open(f))
        for i in range(4):
            try:
                return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], u),
                    headers={'Authorization': 'Bearer ' + self.tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
            except urllib.error.HTTPError as e:
                if e.code < 500 or i == 3:
                    print('API %s HTTP %d' % (u, e.code)); raise SystemExit(3)
            except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
                if i == 3:
                    print('API %s unreachable: %s' % (u, e)); raise SystemExit(3)
                print('RETRY %s: %s' % (u, e), file=sys.stderr)
            time.sleep(10)

    def pages(self, u):
        out = []; pg = 1
        while True:
            b = self.get('%s%sper_page=100&page=%d' % (u, '&' if '?' in u else '?', pg)); out += b
            if len(b) < 100:
                return out
            pg += 1


def ls_remote(refs):
    """ONE `git ls-remote` READ from the Secuura checkout (its own origin + sshCommand); returns {ref: sha}"""
    r = subprocess.run(['git', '-C', K['checkout'], 'ls-remote', 'origin'] + list(refs), capture_output=True, text=True)
    if r.returncode:
        print('REFUSING: ls-remote rc %d: %s' % (r.returncode, r.stderr.strip()[:200])); raise SystemExit(3)
    return {l.split()[1]: l.split()[0] for l in r.stdout.splitlines() if l.strip()}


def opcodes(a_lines, b_lines):
    return [op for op in difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False).get_opcodes() if op[0] != 'equal']


class Checks:
    def __init__(self, quiet=False):
        self.res = []; self.tags = []; self.quiet = quiet

    def failed(self, prefix=''):
        return [t for t, ok in self.tags if not ok and t.startswith(prefix)]

    def chk(self, tag, ok, msg):
        self.res.append(bool(ok)); self.tags.append((tag, bool(ok)))
        if not self.quiet:
            print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
        return bool(ok)

    def nfail(self):
        return self.res.count(False)


def run(cmd, cwd, out_prefix, env=None, timeout=3600):
    """run a command in a GUARDED scratch cwd; stdout / stderr / rc to SEPARATE files (out_prefix.out/.err/.rc); returns (rc, out, err)"""
    guard_scratch(cwd, 'cwd')
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=e, timeout=timeout)
    if out_prefix:
        open(out_prefix + '.out', 'w').write(r.stdout); open(out_prefix + '.err', 'w').write(r.stderr); open(out_prefix + '.rc', 'w').write('%d\n' % r.returncode)
    return r.returncode, r.stdout, r.stderr


def selftest_arm(state, name, fn, want, show_on_miss=True):
    """drive ONE self-test arm: want None == the arm must PASS (positive control); want '<tag prefix>' == it must FAIL on that check (tamper).
    state is a dict {'ok': n, 'n': n} updated in place."""
    import io, contextlib
    buf = io.StringIO(); C = Checks()
    try:
        with contextlib.redirect_stdout(buf):
            fn(C)
    except SystemExit as e:
        C.chk('CRASH', False, 'SystemExit %s' % e)
    f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
    state['n'] += 1; state['ok'] += good
    print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
    if not good and show_on_miss:
        print(buf.getvalue()[:1500])
    return good
