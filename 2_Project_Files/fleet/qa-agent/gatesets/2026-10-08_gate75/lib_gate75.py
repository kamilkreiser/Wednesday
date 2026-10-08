#!/usr/bin/env python3
"""lib_gate75.py — shared helper for the gate75 kit: ONE row (#1426 KS-1450, tier 2, a GUARD change) on base == develop
ddea005553bf at draft. Carried from lib_gate74.py and re-keyed by the gate75 drafter: G74_ -> G75_, gate74 -> gate75. composee5's h2
readers are NOT carried: #1426 adds no flow/cheat block, it inserts ONE clause into an existing line of each doc (c4 measures that by
bytes, not by headings).

  ROW / P              `--pr 1426` on the command line, else G75_ROW. There is NO default row.
  K                    the kit (kit.json beside this file; G75_KITJSON overrides it for self-tests and launcher arms only).
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath). GIT_SSH_COMMAND dropped.
  obj_at(repo,rev,p)   the object sha of a path at rev, or '' when ABSENT — via ls-tree, never `rev-parse rev:path`.
  gh_get / gh_job_log  read-only GitHub REST GETs; GH_TOKEN read BY NAME from the Secuura .env inside this helper, never printed. The
                       job-logs 302 is followed WITHOUT the Authorization header.
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G75_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'merge-tree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree', 'worktree', 'fetch'}
FORBIDDEN = os.environ.get('G75_FORBIDDEN_ROOT', K['forbidden_root'])
ROWS = K['rows']
BASE = K['base']


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def row_arg(required=True):
    r = opt(sys.argv, '--pr') or os.environ.get('G75_ROW')
    if r is None:
        if required: raise SystemExit('lib_gate75: REFUSED — no row (pass --pr <%s>); no default row' % '|'.join(ROWS))
        return None
    if r not in ROWS: raise SystemExit('lib_gate75: REFUSED — unknown row %r (kit rows %s)' % (r, list(ROWS)))
    return r


def _run(repo, args, env=None, inp=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate75: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate75: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate75: git %s rc %d: %s' % (' '.join(args)[:120], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0: raise SystemExit('lib_gate75: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def obj_at(repo, rev, path):
    f = git(repo, 'ls-tree', rev, '--', path).split()
    return f[2] if len(f) >= 3 and f[1] in ('blob', 'tree') else ''


def mode_at(repo, rev, path):
    f = git(repo, 'ls-tree', rev, '--', path).split()
    return f[0] if len(f) >= 3 else ''


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None, inp=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate75: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate75: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e, inp=inp)


def resolvable(repo, sha):
    return bool(sha) and re.fullmatch(r'[0-9a-f]{40}', sha or '') is not None and \
        _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def refuse_absent(repo, named):
    bad = [(n, s) for n, s in named if not resolvable(repo, s)]
    for n, s in bad:
        print('REFUSED BY NAME: %s %r is not a full 40-hex commit in %s — fetch it BY SHA into YOUR clone, then re-run' % (n, s, repo))
    return 2 if bad else 0


def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate75: %s not present in the Secuura .env (by name)' % name)


def gh_get(path):
    req = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                                 headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def gh_pages(path, key=None):
    out, page = [], 1
    while True:
        got = gh_get('%s%sper_page=100&page=%d' % (path, '&' if '?' in path else '?', page))
        items = got if isinstance(got, list) else got.get(key or 'jobs', got.get('workflow_runs', []))
        out += items
        if len(items) < 100 or page >= 10: return out
        page += 1


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


def gh_job_log(job_id):
    op = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request('https://api.github.com/repos/%s/actions/jobs/%s/logs' % (K['gh_repo'], job_id),
                                 headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    try:
        r = op.open(req, timeout=60); return r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308) or not e.headers.get('Location'): raise
        loc = e.headers['Location']
    return urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read().decode('utf-8', 'replace')


class Tally:
    def __init__(self): self.n = 0; self.fails = []; self.infos = []
    def check(self, cid, ok, msg):
        self.n += 1
        print('%s %s %s' % ('PASS' if ok else 'FAIL', cid, msg))
        if not ok: self.fails.append(cid)
        return ok
    def info(self, cid, msg):
        print('INFO %s %s' % (cid, msg)); self.infos.append(cid)
    def end(self):
        print('CHECKED %d' % self.n)
        print('%d FAIL%s' % (len(self.fails), (' (' + ' '.join(self.fails) + ')') if self.fails else ''))
        if self.n == 0:
            print('FAIL: 0 checked'); return 1
        return 1 if self.fails else 0
