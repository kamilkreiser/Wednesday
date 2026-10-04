#!/usr/bin/env python3
"""lib_gateD2.py — shared helpers for the gateD2 check scripts (a NEW COPY of lib_gate54a.py + gate54f's JSON-block helpers, re-keyed).
READ-ONLY git verbs only: exactly show, log, ls-tree, cat-file, ls-remote, rev-parse, diff. rev-list / merge-base are NOT used (ahead / behind
are counted with `git log --format=%H a..b`). Nothing here writes to a repository.
GitHub: read-only REST GETs; GH_TOKEN is read BY NAME from the Secuura .env and never printed.
safe_out(path): the WRITE GUARD every gateD2 script uses before it creates anything: the LEXICAL absolute path must lie under this kit dir,
/private/tmp/claude-501/, or the QA reports root — tested BEFORE any mkdir (gate54a's refusal arm created `Secuura/x` because its mkdir ran
first; this order is the fix). Imported by every gateD2 script; never run alone."""
import json, os, subprocess, datetime, time, urllib.request, urllib.error, sys, difflib

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'log', 'ls-tree', 'cat-file', 'ls-remote', 'rev-parse', 'diff'}
WRITE_ROOTS = (G + '/', '/private/tmp/claude-501/', K['reports_root'] + '/')


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def safe_out(p, create=True):
    """refuse (SystemExit 2) unless the lexical abspath is under a WRITE_ROOT; only THEN mkdir. Returns the abspath."""
    a = os.path.abspath(p)
    if not any((a + '/').startswith(r) for r in WRITE_ROOTS):
        print('REFUSING: output path %s is outside %s (nothing was created)' % (a, list(WRITE_ROOTS))); raise SystemExit(2)
    if create:
        os.makedirs(a, exist_ok=True)
        r = os.path.realpath(a)
        if not any((r + '/').startswith(x) or (r + '/').startswith(os.path.realpath(x.rstrip('/')) + '/') for x in WRITE_ROOTS):
            print('REFUSING: output path %s resolves to %s, outside the write roots' % (a, r)); raise SystemExit(2)
    return a


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gateD2.git allows read verbs only (%s), got %r' % (sorted(READ_VERBS), a[0]))
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def has_commit(repo, rev):
    rc, _, _ = git(repo, 'cat-file', '-e', rev + '^{commit}', check=False)
    return rc == 0


def commit(repo, rev):
    rc, out, _ = git(repo, 'rev-parse', '--verify', '--quiet', rev + '^{commit}', check=False)
    if rc:
        raise SystemExit('REFUSING: %s does not resolve to a commit in %s (fetch it into YOUR clone first)' % (rev, repo))
    return out.strip()


def show(repo, sha, path):
    """blob text at sha:path, resolved with cat-file -e first (rev-parse ECHOES an unresolved path); None when absent"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    return git(repo, 'show', '%s:%s' % (sha, path))


def blob(repo, sha, path):
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    return git(repo, 'rev-parse', '%s:%s' % (sha, path)).strip() if rc == 0 else None


def count_range(repo, a, b):
    return len([l for l in git(repo, 'log', '--format=%H', '%s..%s' % (a, b)).splitlines() if l.strip()])


def code_lines(text):
    """TS/JS source with // and /* */ comments blanked (line numbers kept) — for 'in CODE' regexes"""
    out = []; inblk = False
    for l in (text or '').split('\n'):
        s = ''; i = 0; q = None
        while i < len(l):
            c = l[i]
            if inblk:
                if l.startswith('*/', i): inblk = False; i += 2; continue
                i += 1; continue
            if q:
                s += c
                if c == '\\' and i + 1 < len(l): s += l[i + 1]; i += 2; continue
                if c == q: q = None
                i += 1; continue
            if c in '\'"`': q = c; s += c; i += 1; continue
            if l.startswith('//', i): break
            if l.startswith('/*', i): inblk = True; i += 2; continue
            s += c; i += 1
        out.append(s)
    return '\n'.join(out)


# ---------- gate54f's pretty-printed-JSON block helpers ----------
def _depth(s):
    d = 0; ins = False; esc = False
    for ch in s:
        if ins:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': ins = False
        elif ch == '"': ins = True
        elif ch in '{[': d += 1
        elif ch in '}]': d -= 1
    return d


def member_span(lines, start):
    depth = 0
    for j in range(start, len(lines)):
        depth += _depth(lines[j])
        if depth == 0:
            return start, j
    return None


def find_member(lines, key):
    want = '"%s": {' % key
    st = [i for i, l in enumerate(lines) if l.strip() == want]
    return st[0] if len(st) == 1 else None


def opcodes(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False)
    return [op for op in sm.get_opcodes() if op[0] != 'equal']


# ---------- GitHub ----------
def gh_token():
    tok = ''
    for l in open(K['secuura_env'], encoding='utf-8'):
        if l.startswith('GH_TOKEN='):
            tok = l.split('=', 1)[1].strip().strip('"').strip("'")
    return tok


def gh_get(u, tok):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], u),
                headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3:
                print('API %s HTTP %d' % (u, e.code)); raise SystemExit(3)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if i == 3:
                print('API %s unreachable: %s' % (u, e)); raise SystemExit(3)
            print('RETRY %s: %s' % (u, e), file=sys.stderr)
        time.sleep(10)


def gh_pages(u, tok):
    out = []; pg = 1
    while True:
        b = gh_get('%s%sper_page=100&page=%d' % (u, '&' if '?' in u else '?', pg), tok); out += b
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
