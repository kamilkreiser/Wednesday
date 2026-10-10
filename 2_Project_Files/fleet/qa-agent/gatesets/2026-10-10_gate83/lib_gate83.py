#!/usr/bin/env python3
"""lib_gate83.py — shared helper for the gate83 kit: ONE PR, #1450 (KS-1426, built by Seat F 10th, TIER 2 with both extra arms): lockfile-cleanroom.sh gains
`report_surface()`, which names the tracked package-lock.json files the preflight clean-room leg did not install (report-only, `return 0`).
Carried from lib_gate82.py; [g83] marks this kit's changes. The kit carries ONE gated PR record, K['prs']['1450'], and a roster of COMPANION PRs
K['companions'][<n>] (#1444 flow 50, #1447 flow 51, #1449 flow 52, #1448 flow 54): they are NOT gated here; they are the other writers of the two shared
platform-k docs, so the docs composition is proven against them (flow `53.` sits between them). The cross-PR facts: K['known_develop_overlap'] = the two shared docs;
K['known_code_overlap'] = {} (no non-doc path is shared).

  K / PR(n)            the kit (kit.json beside this file; G83_KITJSON overrides it for the self-tests only) / the ONE gated PR's record (a foreign number is refused).
  COMP(n)              a companion PR's record (composition only).
  req(A, name)         a REQUIRED argument: no default, ever (STANDING_LINES "inherited tools FAIL CLOSED on unset knobs").
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  blob(repo, rev, p)   blob id via `ls-tree` ('' for an ABSENT path) — never `rev-parse <sha>:<path>` (it ECHOES on an absent path).
  show(repo, rev, p)   the blob's text at rev ('' when absent).
  gh_get(path)         read-only GitHub REST GET; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear_issue(id)     read-only Linear GraphQL; LINEAR_API_KEY read BY NAME, never printed.
"""
import hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G83_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'archive', 'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout', 'merge-tree', 'read-tree', 'update-index', 'write-tree', 'hash-object', 'commit-tree'}   # [g83] + the temp-index / merge-tree verbs (clone-only)
FORBIDDEN = os.environ.get('G83_FORBIDDEN_ROOT', K['forbidden_root'])
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def req(A, k, hex40=False):
    v = opt(A, k)
    if v is None or v.startswith('--'):
        raise SystemExit('REFUSED: %s is REQUIRED (no default: a kit default is the drafter\'s pin, not your measurement)' % k)
    if hex40 and not HEX40.match(v):
        raise SystemExit('REFUSED: %s must be a FULL 40-hex sha, got %r' % (k, v))
    return v


# ---------------- git ----------------
def _run(repo, args, env=None):
    e = dict(env if env is not None else os.environ); e.pop('GIT_SSH_COMMAND', None)   # never an exported GIT_SSH_COMMAND
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=e)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate83: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate83: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate83: git %s rc %d: %s' % (' '.join(args)[:200], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate83: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def blob(repo, rev, path):
    out = git(repo, 'ls-tree', rev, '--', path).strip()
    if not out:
        return ''
    meta = out.split('\t')[0].split()
    return '%s %s' % (meta[0], meta[2])


def show(repo, rev, path):
    return git_bytes(repo, rev, path).decode('utf-8') if blob(repo, rev, path) else ''


def outside_forbidden(path):
    lex = os.path.abspath(path); real = os.path.realpath(path); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def must_be_outside(path, what):
    if not outside_forbidden(path):
        raise SystemExit('lib_gate83: REFUSED %s under %s (%s) — use YOUR scratch under /private/tmp' % (what, FORBIDDEN, path))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate83: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS:
        must_be_outside(repo, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e)


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def extract(repo, rev, paths, dest):
    """[g83] `git archive <rev> -- <paths> | tar -x -C dest`: a READ of the repo (archive writes nothing there); dest must be OUTSIDE the
    forbidden root. Returns the number of files extracted. Used for the shell legs (#1444) that need no node_modules."""
    must_be_outside(dest, 'extract'); os.makedirs(dest, exist_ok=True)
    a = subprocess.Popen(['git', '-C', repo, 'archive', rev, '--'] + list(paths), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t = subprocess.run(['tar', '-x', '-C', dest], stdin=a.stdout, capture_output=True); a.stdout.close(); err = a.stderr.read(); a.wait()
    if a.returncode or t.returncode:
        raise SystemExit('lib_gate83: extract %s rc %s/%s %s %s' % (rev[:12], a.returncode, t.returncode, err[:200], t.stderr[:200]))
    return sum(len(f) for _, _, f in os.walk(dest))


def sha256_16(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()[:16]


def PR(n):   # [g83] ONE gated PR: 1450
    if str(n) not in K['prs']:
        raise SystemExit('lib_gate83: --pr %r is not the kit PR %s' % (n, sorted(K['prs'])))
    return K['prs'][str(n)]


def COMP(n):   # [g83] a companion PR (composition only; never gated here)
    if str(n) not in K['companions']:
        raise SystemExit('lib_gate83: %r is not a kit companion PR %s' % (n, sorted(K['companions'])))
    return K['companions'][str(n)]


def doc_paths():
    return list(K['known_develop_overlap'])


def norm_lines(text):
    return [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n') if l.strip()]


# ---------------- GitHub / Linear (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate83: %s not present in the Secuura .env (by name)' % name)


def gh_get(path, raw=False):
    tok = env_value('GH_TOKEN')
    r = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                               headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json', 'User-Agent': 'gate83-qa'})
    data = urllib.request.urlopen(r, timeout=60).read()
    return data if raw else json.loads(data)


def gh_pages(path):
    out, page = [], 1
    while True:
        sep = '&' if '?' in path else '?'
        got = gh_get('%s%sper_page=100&page=%d' % (path, sep, page))
        out += got
        if len(got) < 100:
            return out
        page += 1


def linear(query, variables):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': variables}).encode(),
                               headers={'Content-Type': 'application/json', 'Authorization': env_value('LINEAR_API_KEY')}, method='POST')
    return json.load(urllib.request.urlopen(r, timeout=60))


def linear_issue(ident):
    q = ('query($id:String!){issue(id:$id){identifier title state{name type} updatedAt archivedAt '
         'comments{nodes{id createdAt updatedAt body}} attachments{nodes{id title url createdAt}}}}')
    r = linear(q, {'id': ident})
    return (r.get('data') or {}).get('issue'), r.get('errors')


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
