#!/usr/bin/env python3
"""lib_gate64.py — shared helper for the gate64 kit (#1389, KS-1330, T2). Derived from lib_gate62 (G64_ env names; adds the read verb ls-files and the write verb worktree, the latter refused inside the forbidden root like every write verb).

  K            the kit (kit.json beside this file).
  git(repo, *args)   READ verbs only (READ_VERBS). Any other verb raises — the kit never writes a repository it did not create.
  wgit(repo, *args)  WRITE verbs (WRITE_VERBS) ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath). Used by
               c4 predict / its self-test in the GATE's (or the drafter's) own scratch clone; refuses the shared checkout.
  gh_get(path)  read-only GitHub REST GET of repos/<gh_repo>/<path>; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  out(...)     print helper; every checker prints `CHECKED <n>` and a `<n> FAIL` line.
"""
import json, os, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('G64_SCRATCH', HERE)   # where self-test fixtures / SIM indexes go: the gate sets this to ITS scratch
K = json.load(open(os.path.join(HERE, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config'}
WRITE_VERBS = {'merge-tree', 'worktree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree'}
FORBIDDEN = os.environ.get('G64_FORBIDDEN_ROOT', K['forbidden_root'])


def _run(repo, args, env=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate64: REFUSED non-read git verb %r (read verbs only: %s)' % (args[:1], sorted(READ_VERBS)))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate64: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate64: git %s rc %d: %s' % (' '.join(args), rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None, input_bytes=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate64: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate64: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=e, input=input_bytes)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def blob(repo, rev, path):
    return git(repo, 'show', '%s:%s' % (rev, path))


def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate64: %s not present in the Secuura .env (by name)' % name)


def gh_get(path):
    tok = env_value('GH_TOKEN')
    req = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                                 headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def gh_pages(path):
    out, page = [], 1
    while True:
        sep = '&' if '?' in path else '?'
        got = gh_get('%s%sper_page=100&page=%d' % (path, sep, page))
        out += got
        if len(got) < 100:
            return out
        page += 1


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
