#!/usr/bin/env python3
"""lib_gate85.py — shared helper for the gate85 kit: ONE PR, #1453 (KS-1432), TIER 1 (census) proposed by the builder; THE GATE DECIDES THE TIER. Ported from lib_gate85.py;
[g85] marks this kit's changes. The kit carries ONE gated PR record, K['prs']['1453'], and NO companion (K['companions'] == {}).

#1453 is ONE commit directly on develop (head^ == the base == develop at the draft), so the gate84 two-commit machinery (prev_head, head^ != base) is gone; `docs_base` is kept
(G83-1 / G84: the ONE place a docs instrument gets its parent = merge-base(develop, head), never a kit-pinned parent taken on trust) and still refuses a merge-base that is not the pinned
branch point. [g85] new here: `run()` (a subprocess with a REQUIRED cwd, a canonical TMPDIR assertion, no shell), `blob_of_bytes()` (git's blob id of bytes, no repo needed).

  K / PR(n)            the kit (kit.json beside this file; G85_KITJSON overrides it for the self-tests only) / the ONE gated PR's record (a foreign number is refused).
  req(A, name)         a REQUIRED argument: no default, ever (STANDING_LINES "inherited tools FAIL CLOSED on unset knobs").
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  blob(repo, rev, p)   blob id via `ls-tree` ('' for an ABSENT path) — never `rev-parse <sha>:<path>` (it ECHOES on an absent path).
  show(repo, rev, p)   the blob's text at rev ('' when absent).
  docs_base(...)       merge-base(develop, head), asserted == the pinned branch point; returns (base, info). The docs instruments call ONLY this.
  gh_get(path)         read-only GitHub REST GET; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear_issue(id)     read-only Linear GraphQL; LINEAR_API_KEY read BY NAME, never printed.
"""
import hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G85_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'archive', 'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout', 'merge-tree', 'read-tree', 'update-index', 'write-tree', 'hash-object', 'commit-tree'}   # [g85] + the temp-index / merge-tree verbs (clone-only)
FORBIDDEN = os.environ.get('G85_FORBIDDEN_ROOT', K['forbidden_root'])
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
        raise SystemExit('lib_gate85: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate85: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate85: git %s rc %d: %s' % (' '.join(args)[:200], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate85: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
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
        raise SystemExit('lib_gate85: REFUSED %s under %s (%s) — use YOUR scratch under /private/tmp' % (what, FORBIDDEN, path))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate85: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS:
        must_be_outside(repo, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e)


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def extract(repo, rev, paths, dest):
    """[g85] `git archive <rev> -- <paths> | tar -x -C dest`: a READ of the repo (archive writes nothing there); dest must be OUTSIDE the
    forbidden root. Returns the number of files extracted."""
    must_be_outside(dest, 'extract'); os.makedirs(dest, exist_ok=True)
    a = subprocess.Popen(['git', '-C', repo, 'archive', rev, '--'] + list(paths), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t = subprocess.run(['tar', '-x', '-C', dest], stdin=a.stdout, capture_output=True); a.stdout.close(); err = a.stderr.read(); a.wait()
    if a.returncode or t.returncode:
        raise SystemExit('lib_gate85: extract %s rc %s/%s %s %s' % (rev[:12], a.returncode, t.returncode, err[:200], t.stderr[:200]))
    return sum(len(f) for _, _, f in os.walk(dest))


def sha256_16(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()[:16]


def docs_base(repo, develop, head, pinned_base=None):
    """[g85] THE G83-1 FIX. The base a docs fragment is extracted against = merge-base(develop, head). Never head^ and never a kit-pinned parent taken on trust.
    -> (base, info). Refuses: an unresolvable sha, no merge-base, a merge-base == head (the head is already in develop: nothing to compose), and a merge-base that differs
    from `pinned_base` (the branch point the caller was handed: a mismatch means develop merged the branch or the pin is stale)."""
    for lab, s in (('develop', develop), ('head', head)):
        if not resolvable(repo, s): raise SystemExit('docs_base: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (lab, s, repo))
    rc, o, e = _run(repo, ['merge-base', develop, head])
    base = o.strip()
    if rc != 0 or not HEX40.match(base): raise SystemExit('docs_base: no merge-base(%s, %s): rc %d %s' % (develop[:12], head[:12], rc, e.strip()[:120]))
    if base == head: raise SystemExit('docs_base: merge-base == head: the head %s is ALREADY in develop %s (nothing to compose)' % (head[:12], develop[:12]))
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    if pinned_base and base != pinned_base:
        raise SystemExit('docs_base: merge-base(develop %s, head %s) = %s != the pinned branch point %s (develop merged the branch, or the pin is stale): REFUSED, never guessed' % (develop[:12], head[:12], base[:12], pinned_base[:12]))
    return base, {'merge_base': base, 'head_parent': (par or [''])[0], 'merge_base_is_head_parent': bool(par) and par[0] == base, 'parents': par}


def blob_of_bytes(b):
    """[g85] git's blob id of `b` (sha1 over `blob <len>\\0` + bytes) computed in-process: needs no repository, so a scratch tree outside every repo can be identified by blob."""
    if isinstance(b, str): b = b.encode('utf-8')
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def canonical_tmp(path):
    """[g85] True iff `path` is a realpath (no symlink component) that sits under /private/tmp/claude-501/ and under NO git repository (no .git on any parent)."""
    real = os.path.realpath(path)
    if real != os.path.abspath(path) or not real.startswith('/private/tmp/claude-501/'): return False
    d = real
    while d != '/':
        if os.path.exists(os.path.join(d, '.git')): return False
        d = os.path.dirname(d)
    return True


def run(cmd, cwd, env=None, timeout=900):
    """[g85] subprocess without a shell; the cwd is REQUIRED and must exist and sit outside the forbidden root. -> (rc, stdout, stderr)."""
    must_be_outside(cwd, 'run in')
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(list(cmd), cwd=cwd, capture_output=True, env=e, timeout=timeout)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


TAIL = '</body>\n</html>\n'


def exact_tail_insert(base, head):
    """[g85] head == base_prefix + FRAGMENT + TAIL where base == base_prefix + TAIL (TAIL = `</body>\\n</html>\\n`). -> (ok, fragment, why). A replaced base line, a second insertion elsewhere,
    a changed tail, an empty fragment all return ok False. The gate83 `pure_insertion` (difflib opcodes) is blind to WHERE the single insert sits; this one pins it before the closing tags."""
    if not base.endswith(TAIL) or not head.endswith(TAIL): return False, '', 'a doc does not end with %r' % TAIL
    pre = base[:-len(TAIL)]
    if not head.startswith(pre): return False, '', 'the head doc does not start with the whole base prefix (a base byte changed, or a second edit elsewhere)'
    frag = head[len(pre):-len(TAIL)]
    if not frag: return False, '', 'empty fragment'
    return True, frag, 'ok'


def tag_deltas(fragment):
    """[g85] open-minus-close counts of the paired HTML tags in a fragment (non-void tags only). A balanced fragment reads all zeros."""
    out = {}
    for tg in ('table', 'thead', 'tbody', 'tr', 'td', 'th', 'div', 'ul', 'ol', 'li', 'pre', 'code', 'p', 'h2', 'h3', 'h4', 'details', 'summary', 'span', 'section', 'strong', 'em', 'a'):
        o = len(re.findall(r'<%s(?=[\s>])' % tg, fragment)); c = len(re.findall(r'</%s>' % tg, fragment))
        if o or c: out[tg] = o - c
    return out



def PR(n):   # [g85] ONE gated PR: 1453
    if str(n) not in K['prs']:
        raise SystemExit('lib_gate85: --pr %r is not the kit PR %s' % (n, sorted(K['prs'])))
    return K['prs'][str(n)]


def COMP(n):   # [g85] kept for shape: K['companions'] is EMPTY in this kit, so every call refuses
    if str(n) not in K['companions']:
        raise SystemExit('lib_gate85: %r is not a kit companion PR %s' % (n, sorted(K['companions'])))
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
    raise SystemExit('lib_gate85: %s not present in the Secuura .env (by name)' % name)


def gh_get(path, raw=False):
    tok = env_value('GH_TOKEN')
    r = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                               headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json', 'User-Agent': 'gate85-qa'})
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
