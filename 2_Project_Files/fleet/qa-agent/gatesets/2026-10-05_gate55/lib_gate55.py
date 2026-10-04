#!/usr/bin/env python3
"""lib_gate55.py — shared helpers for the gate55 check scripts (a NEW COPY of lib_gate54a.py, re-keyed for KS-1015 / Seat B 58th's PR B).
READ-ONLY git verbs only: exactly show, log, ls-tree, cat-file, ls-remote, rev-parse, diff, grep. `git()` refuses any other verb BEFORE it
runs. ahead / behind are counted with `git log --format=%H a..b` (no rev-list, no merge-base). Nothing here writes to a repository.
GitHub: read-only REST GETs; GH_TOKEN is read BY NAME from the Secuura .env and never printed. `--offline-dir` replays (SIM fixtures) never
touch the network or the .env.
PATH GUARD (gate54a's lesson: its first guard ran `mkdir -p` BEFORE its prefix test and created an empty dir in the Secuura tree, and its
c5 `static` wrote into the kit dir, N-1374-5): `guard_out()` tests the LEXICAL absolute path first, then the realpath of the nearest existing
ancestor, and only then creates the directory. Nothing in this kit writes into the kit dir except fill_gate55.py (prompt / launcher / pins).
The forbidden root defaults to kit forbidden_root (/Volumes/DevMASTER/!CODING/); G55_FORBIDDEN_ROOT / G55_REPORTS_ROOT are CONTROLS-ONLY
overrides so a refusal arm can be exercised against a SCRATCH stand-in, never against a sibling of a real project path (the launcher refuses
a real launch with any G55_* set). Imported by every python tool in the kit; never run alone."""
import json, os, subprocess, datetime, time, urllib.request, urllib.error, sys, hashlib

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'log', 'ls-tree', 'cat-file', 'ls-remote', 'rev-parse', 'diff', 'grep'}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gate55.git allows read verbs only (%s), got %r' % (sorted(READ_VERBS), a[0]))
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def has_commit(repo, rev):
    rc, _, _ = git(repo, 'cat-file', '-e', rev + '^{commit}', check=False)
    return rc == 0


def blob_id(repo, sha, path):
    """the blob id at sha:path, resolved with cat-file -e first (rev-parse ECHOES an unresolved path); 'ABSENT' when absent"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return 'ABSENT'
    return git(repo, 'rev-parse', '%s:%s' % (sha, path)).strip()


def show(repo, sha, path):
    """the blob text at sha:path; None when absent (cat-file -e first)"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    return git(repo, 'show', '%s:%s' % (sha, path))


def count_range(repo, a, b):
    return len([l for l in git(repo, 'log', '--format=%H', '%s..%s' % (a, b)).splitlines() if l.strip()])


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def forbidden_root():
    return os.environ.get('G55_FORBIDDEN_ROOT') or K['forbidden_root']


def reports_root():
    return os.environ.get('G55_REPORTS_ROOT') or K['reports_root']


def _under(p, root):
    root = root.rstrip('/') + '/'
    return (p.rstrip('/') + '/').startswith(root)


def guard_out(path, create=True):
    """refuse (SystemExit 2, NOTHING created) an OUT inside the forbidden root unless it is under the QA reports root; lexical test FIRST,
    then the realpath of the nearest existing ancestor (a symlink cannot smuggle a write in), then mkdir"""
    lex = os.path.abspath(path)
    fr, rr = forbidden_root(), reports_root()
    if _under(lex, fr) and not _under(lex, rr):
        print('REFUSING: OUT %s is inside %s but not under the QA reports root (nothing was created)' % (lex, fr)); raise SystemExit(2)
    anc = lex
    while not os.path.exists(anc):
        anc = os.path.dirname(anc)
    real = os.path.join(os.path.realpath(anc), os.path.relpath(lex, anc)) if anc != lex else os.path.realpath(lex)
    if _under(real, fr) and not _under(real, rr):
        print('REFUSING: OUT %s resolves to %s inside %s (nothing was created)' % (lex, real, fr)); raise SystemExit(2)
    if create:
        os.makedirs(lex, exist_ok=True)
    return lex


def gh_token():
    tok = ''
    for l in open(K['secuura_env'], encoding='utf-8'):
        if l.startswith('GH_TOKEN='):
            tok = l.split('=', 1)[1].strip().strip('"').strip("'")
    return tok


class GH:
    """read-only GitHub access; offline=<dir> replays pulls.json / pr_<n>.json / files_<n>.json (SIM fixtures) with NO network"""
    def __init__(self, offline=None):
        self.off = offline; self.tok = None
        if not offline:
            self.tok = gh_token()
            if not self.tok:
                print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)

    def _file(self, name):
        p = os.path.join(self.off, name)
        if not os.path.isfile(p):
            print('OFFLINE fixture missing: %s' % p); raise SystemExit(3)
        return json.load(open(p, encoding='utf-8'))

    def get(self, u):
        if self.off:
            if u.startswith('pulls/') and u.count('/') == 1:
                return self._file('pr_%s.json' % u.split('/')[1])
            raise SystemExit('OFFLINE: no fixture route for %s' % u)
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
        if self.off:
            if u.startswith('pulls?state=open'):
                return self._file('pulls.json')
            if u.startswith('pulls/') and u.endswith('/files'):
                return self._file('files_%s.json' % u.split('/')[1])
            raise SystemExit('OFFLINE: no fixture route for %s' % u)
        out = []; pg = 1
        while True:
            b = self.get('%s%sper_page=100&page=%d' % (u, '&' if '?' in u else '?', pg)); out += b
            if len(b) < 100:
                return out
            pg += 1


class Checks:
    def __init__(self):
        self.res = []; self.tags = []

    def failed(self, prefix=''):
        return [t for t, ok in self.tags if not ok and t.startswith(prefix)]

    def chk(self, tag, ok, msg):
        self.res.append(bool(ok)); self.tags.append((tag, bool(ok))); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
        return bool(ok)

    def nfail(self):
        return self.res.count(False)
