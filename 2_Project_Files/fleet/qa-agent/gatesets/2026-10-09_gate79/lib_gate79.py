#!/usr/bin/env python3
"""lib_gate79.py — shared helper for the gate79 kit (#1437 KS-1402, T1: originate resolves a transfer-custody holder email itself).
Carried from lib_gate78.py; [g79] marks this kit's changes. The lock / semver / registry core is DROPPED (no lock is touched by #1437);
[g79] ADDS a TypeScript comment stripper (code_only) that respects '…', "…" and `…` literals (a `//` inside a string or a template is
CODE), the transfer-custody handler extractor, and the K-seat tool-copy helper.

  K                    the kit (kit.json beside this file; G79_KITJSON overrides it for the self-tests only).
  req(A, name)         a REQUIRED argument: no default, ever (STANDING_LINES "inherited tools FAIL CLOSED on unset knobs").
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  blob(repo, rev, p)   blob id via `ls-tree` ('' for an ABSENT path) — never `rev-parse <sha>:<path>` (it ECHOES on an absent path).
  show(repo, rev, p)   the blob's text at rev ('' when absent).
  code_only(ts)        [g79] the TS source with comments replaced by spaces (newlines KEPT, so line numbers survive).
  handler(ts)          [g79] (start, end) char span of the transfer-custody handler: from the route anchor to the next top-level
                       `documentsRouter.` / `publicDocumentsRouter.` / `export ` at column 0.
  block(ts, hs, he)    [g79] (start, end) of the email-resolution block inside the handler (kit resolution_block start .. end).
  gh_get(path)         read-only GitHub REST GET; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear_issue(id)     read-only Linear GraphQL; LINEAR_API_KEY read BY NAME, never printed.
"""
import hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G79_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout'}
FORBIDDEN = os.environ.get('G79_FORBIDDEN_ROOT', K['forbidden_root'])
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
        raise SystemExit('lib_gate79: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate79: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate79: git %s rc %d: %s' % (' '.join(args)[:200], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate79: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
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
        raise SystemExit('lib_gate79: REFUSED %s under %s (%s) — use YOUR scratch under /private/tmp' % (what, FORBIDDEN, path))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate79: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS:
        must_be_outside(repo, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e)


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def sha256_16(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()[:16]


# ---------------- TypeScript ----------------
def code_only(src):
    """[g79] comments -> spaces (newlines kept). String / template literals are CODE and are kept verbatim; a `${…}` inside a
    template is tracked by brace depth so a `}` in the expression does not end it early. Regex literals are not modelled: the
    files this kit reads carry none on the lines it measures (the self-test pins that), and a mis-strip shows as a count change
    against the CONTROL counts printed beside every census."""
    out = []; i = 0; n = len(src); stack = []   # stack of '`' (template) / '{' (expr inside a template)
    while i < n:
        c = src[i]; c2 = src[i:i + 2]
        in_tpl = bool(stack) and stack[-1] == '`'
        if in_tpl:
            if c == '\\': out.append(src[i:i + 2]); i += 2; continue
            if c == '`': stack.pop(); out.append(c); i += 1; continue
            if c2 == '${': stack.append('{'); out.append(c2); i += 2; continue
            out.append(c); i += 1; continue
        if c2 == '//':
            j = src.find('\n', i); j = n if j < 0 else j
            out.append(' ' * (j - i)); i = j; continue
        if c2 == '/*':
            j = src.find('*/', i + 2); j = n if j < 0 else j + 2
            out.append(re.sub(r'[^\n]', ' ', src[i:j])); i = j; continue
        if c in ('"', "'"):
            j = i + 1
            while j < n and src[j] != c and src[j] != '\n':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1; continue
        if c == '`': stack.append('`'); out.append(c); i += 1; continue
        if c == '{' and stack: stack.append('{')
        if c == '}' and stack and stack[-1] == '{': stack.pop()
        out.append(c); i += 1
    return ''.join(out)


def handler(src):
    """[g79] the transfer-custody handler span. Refuses (SystemExit) unless the route anchor occurs exactly once."""
    a = K['route_anchor']
    if src.count(a) != 1:
        raise SystemExit('lib_gate79: route anchor %r occurs %d times (want 1)' % (a, src.count(a)))
    s = src.rfind('\ndocumentsRouter.post(', 0, src.index(a)) + 1
    m = re.compile(r'^(documentsRouter\.|publicDocumentsRouter\.|export |/\*\*)', re.M).search(src, src.index(a))
    return s, (m.start() if m else len(src))


def block(src, hs, he):
    """[g79] the email-resolution block span inside the handler: resolution_block.start .. the line before .end."""
    st, en = K['resolution_block']['start'], K['resolution_block']['end']
    i = src.find(st, hs, he)
    if i < 0 or src.find(st, i + 1, he) >= 0:
        raise SystemExit('lib_gate79: resolution block start %r not exactly once in the handler' % st)
    j = src.find(en, i, he)
    if j < 0:
        raise SystemExit('lib_gate79: resolution block end %r not found after its start' % en)
    return src.rfind('\n', 0, i) + 1, src.rfind('\n', 0, j) + 1


def norm_lines(text):
    return [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n') if l.strip()]


# ---------------- GitHub / Linear (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate79: %s not present in the Secuura .env (by name)' % name)


def gh_get(path, raw=False):
    tok = env_value('GH_TOKEN')
    r = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                               headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json', 'User-Agent': 'gate79-qa'})
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
