#!/usr/bin/env python3
"""lib_gate54a.py — shared helpers for the gate54a check scripts (a NEW COPY of lib_gate54f.py, re-keyed). READ-ONLY git verbs only, and
NARROWER than gate54f's: exactly the seven the commission names (show, log, ls-tree, cat-file, ls-remote, rev-parse, diff). rev-list and
merge-base are NOT used: ahead / behind are counted with `git log --format=%H a..b`. Nothing here writes to a repository.
GitHub: read-only REST GETs; GH_TOKEN is read BY NAME from the Secuura .env and never printed. Imported by c1..c6 + the census; never run alone."""
import json, os, subprocess, datetime, time, urllib.request, urllib.error, sys

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'log', 'ls-tree', 'cat-file', 'ls-remote', 'rev-parse', 'diff'}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gate54a.git allows read verbs only (%s), got %r' % (sorted(READ_VERBS), a[0]))
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def has_commit(repo, rev):
    rc, _, _ = git(repo, 'cat-file', '-e', rev + '^{commit}', check=False)
    return rc == 0


def show(repo, sha, path):
    """the blob text at sha:path, resolved with cat-file -e first (rev-parse ECHOES an unresolved path); None when absent"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    return git(repo, 'show', '%s:%s' % (sha, path))


def count_range(repo, a, b):
    """number of commits in a..b, by `git log` (no rev-list)"""
    return len([l for l in git(repo, 'log', '--format=%H', '%s..%s' % (a, b)).splitlines() if l.strip()])


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
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:   # gate53's fix: a dropped connection is retried, not fatal
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
