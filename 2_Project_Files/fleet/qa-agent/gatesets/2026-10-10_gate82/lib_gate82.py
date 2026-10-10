#!/usr/bin/env python3
"""lib_gate82.py — shared helper for the gate82 kit (THREE PRs, one batch): #1447 (KS-1456 run-migrations.sh failed-run message, TIER 2), #1449 (KS-1417
env.example drops the dead API_GATEWAY_PORT, TIER 2) and #1448 (KS-1434 ApiKeyCreateRequest declares `rotate`, TIER 1 WEIGHT: the API-key surface).
Carried from lib_gate81.py (which came from lib_gate80.py); [g82] marks this kit's changes. The kit carries THREE PR records: K['prs'][<n>] and EACH PR
has its OWN base (K['prs'][n]['parents'][0]): #1447 and #1448 branch from develop 76b683c7dcd0, #1449 from f247ff85b612 (the cross-PR facts are
K['known_develop_overlap'] = the two shared docs; there is NO shared non-doc path, K['known_code_overlap'] is {}).

  K / PR(n)            the kit (kit.json beside this file; G82_KITJSON overrides it for the self-tests only) / one PR's record.
  req(A, name)         a REQUIRED argument: no default, ever (STANDING_LINES "inherited tools FAIL CLOSED on unset knobs").
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  blob(repo, rev, p)   blob id via `ls-tree` ('' for an ABSENT path) — never `rev-parse <sha>:<path>` (it ECHOES on an absent path).
  show(repo, rev, p)   the blob's text at rev ('' when absent).
  code_only(ts)        the TS source with comments replaced by spaces (newlines KEPT, so line numbers survive).
  span(src, anchor, end_rx)  [g82] (start, end) of the route handler that starts at the anchor (exactly once) .. the next match of end_rx.
  gh_get(path)         read-only GitHub REST GET; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear_issue(id)     read-only Linear GraphQL; LINEAR_API_KEY read BY NAME, never printed.
"""
import hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G82_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'archive', 'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout', 'merge-tree', 'read-tree', 'update-index', 'write-tree', 'hash-object', 'commit-tree'}   # [g82] + the temp-index / merge-tree verbs (clone-only)
FORBIDDEN = os.environ.get('G82_FORBIDDEN_ROOT', K['forbidden_root'])
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
        raise SystemExit('lib_gate82: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate82: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate82: git %s rc %d: %s' % (' '.join(args)[:200], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate82: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
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
        raise SystemExit('lib_gate82: REFUSED %s under %s (%s) — use YOUR scratch under /private/tmp' % (what, FORBIDDEN, path))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate82: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS:
        must_be_outside(repo, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e)


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def extract(repo, rev, paths, dest):
    """[g82] `git archive <rev> -- <paths> | tar -x -C dest`: a READ of the repo (archive writes nothing there); dest must be OUTSIDE the
    forbidden root. Returns the number of files extracted. Used for the shell legs (#1444) that need no node_modules."""
    must_be_outside(dest, 'extract'); os.makedirs(dest, exist_ok=True)
    a = subprocess.Popen(['git', '-C', repo, 'archive', rev, '--'] + list(paths), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t = subprocess.run(['tar', '-x', '-C', dest], stdin=a.stdout, capture_output=True); a.stdout.close(); err = a.stderr.read(); a.wait()
    if a.returncode or t.returncode:
        raise SystemExit('lib_gate82: extract %s rc %s/%s %s %s' % (rev[:12], a.returncode, t.returncode, err[:200], t.stderr[:200]))
    return sum(len(f) for _, _, f in os.walk(dest))


def sha256_16(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()[:16]


# ---------------- TypeScript ----------------
def code_only(src):
    """[g82] comments -> spaces (newlines kept). String / template literals are CODE and are kept verbatim; a `${…}` inside a
    template is tracked by brace depth so a `}` in the expression does not end it early. Regex literals ARE modelled [g82] by a previous-token
    heuristic (a `/` after an operator or opener); a mis-strip shows as a count change against the CONTROL counts printed beside every census."""
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
        if c == '/' and c2 not in ('//', '/*'):
            # [g82] REGEX LITERAL (gate80 did not model them; audit-export.ts line 60 has `/"/g` inside a template expression, which opened a phantom
            # string and kept every later comment un-blanked). A `/` is a regex start only when the previous significant char is an operator / opener.
            sig = ''.join(out).rstrip()[-1:]
            if sig == '' or sig in '(,=:[!&|?{};+-*%<>~^':
                j = i + 1; in_cls = False
                while j < n and src[j] != '\n':
                    ch_ = src[j]
                    if ch_ == '\\': j += 2; continue
                    if ch_ == '[': in_cls = True
                    elif ch_ == ']': in_cls = False
                    elif ch_ == '/' and not in_cls: break
                    j += 1
                if j < n and src[j] == '/':
                    j += 1
                    while j < n and src[j].isalpha(): j += 1
                    out.append(src[i:j]); i = j; continue
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


def span(src, anchor, end_rx):
    """[g82] the span of the route that begins at `anchor` (must occur EXACTLY once) up to the next match of end_rx after it."""
    if src.count(anchor) != 1:
        raise SystemExit('lib_gate82: route anchor %r occurs %d times (want 1)' % (anchor, src.count(anchor)))
    s0 = src.rfind('\n', 0, src.index(anchor)) + 1
    m = re.compile(end_rx, re.M).search(src, src.index(anchor) + len(anchor))
    return s0, (m.end() if m else len(src))


def PR(n):   # [g82] three kit PRs: 1447 1448 1449
    if str(n) not in K['prs']:
        raise SystemExit('lib_gate82: --pr %r is not one of the kit PRs %s' % (n, sorted(K['prs'])))
    return K['prs'][str(n)]


def doc_paths():
    return list(K['known_develop_overlap'])


def merge_order():
    return list(K['merge_order'])


def norm_lines(text):
    return [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n') if l.strip()]


# ---------------- GitHub / Linear (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate82: %s not present in the Secuura .env (by name)' % name)


def gh_get(path, raw=False):
    tok = env_value('GH_TOKEN')
    r = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                               headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json', 'User-Agent': 'gate82-qa'})
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
