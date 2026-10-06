#!/usr/bin/env python3
"""lib_gate72.py — shared helper for the gate72 kit (#1406 KS-1437, T1: in-range LOCK-ONLY refresh, 5 locks, 0 baseline rows).
Carried from lib_gate70.py; changes are marked [g72].

  K                    the kit (kit.json beside this file; G72_KITJSON overrides it for the self-tests only).
  req(A, name)         [g72] a REQUIRED argument: no default, ever (STANDING_LINES "inherited tools FAIL CLOSED on unset knobs").
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  blob(repo, rev, p)   [g72] blob id via `ls-tree` (empty string for an ABSENT path) — never `rev-parse <sha>:<path>`, which ECHOES
                       its argument on an absent path (STANDING_LINES, Seat R 5th 2026-10-07).
  gh_get(path)         read-only GitHub REST GET; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear(query, vars)  read-only Linear GraphQL; LINEAR_API_KEY read BY NAME, never printed.
  satisfies(v, range)  an INDEPENDENT node-semver subset (NOT the repo's semver). Self-tested in c2 --selftest.
  resolve_path / parents_of           npm's nearest-node_modules walk inside a lockfileVersion-3 `packages` map.
  detect_indent / roundtrip_exact     indent per FILE, and the byte-exact json round-trip.
  leaf_diff(a, b)      [g72] every changed LEAF path between two json values, with key-ORDER changes reported as their own kind.
"""
import base64, hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G72_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout', 'hash-object'}
FORBIDDEN = os.environ.get('G72_FORBIDDEN_ROOT', K['forbidden_root'])
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def req(A, k, hex40=False):
    """[g72] a REQUIRED argument. Missing -> SystemExit rc 2 naming it. hex40 -> must be a full 40-hex sha."""
    v = opt(A, k)
    if v is None or v.startswith('--'):
        raise SystemExit('REFUSED: %s is REQUIRED (no default: a kit default is the drafter\'s pin, not your measurement)' % k)
    if hex40 and not HEX40.match(v):
        raise SystemExit('REFUSED: %s must be a FULL 40-hex sha, got %r' % (k, v))
    return v


# ---------------- git ----------------
def _run(repo, args, env=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate72: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate72: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate72: git %s rc %d: %s' % (' '.join(args), rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    """The blob's exact BYTES (no decode/re-encode): byte-equality claims are made on these."""
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate72: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def blob(repo, rev, path):
    """[g72] '<mode> <blob>' of path at rev via ls-tree; '' when the path is ABSENT (a third state, never a sha echo)."""
    out = git(repo, 'ls-tree', rev, '--', path).strip()
    if not out:
        return ''
    meta = out.split('\t')[0].split()
    return '%s %s' % (meta[0], meta[2])


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate72: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate72: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e)


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def tracked_locks(repo, rev):
    return sorted(l for l in git(repo, 'ls-tree', '-r', '--name-only', rev).split('\n') if l.endswith('package-lock.json'))


def in_scope(lock):
    """The leg-6 + leg-7 corpus: every tracked lock except the OUT_OF_SCOPE_LOCKS (mobile, KS-769)."""
    return not any(lock == d + '/package-lock.json' for d in K['out_of_scope_lock_dirs'])


# ---------------- lockfiles ----------------
def detect_indent(text):
    m = re.search(r'\n( +)"', text)
    return len(m.group(1)) if m else None


def roundtrip_exact(raw):
    """True iff json.dumps(json.loads(raw), indent=<detected>) + '\\n' reproduces the file byte for byte."""
    t = raw.decode('utf-8'); n = detect_indent(t)
    return n is not None and (json.dumps(json.loads(t), indent=n, ensure_ascii=False) + '\n').encode('utf-8') == raw, n


def pkg_name(path):
    i = path.rfind('node_modules/')
    return path[i + len('node_modules/'):] if i >= 0 else None


def resolve_path(pk, from_path, name):
    p = from_path
    while True:
        cand = (p + '/node_modules/' + name) if p else ('node_modules/' + name)
        if cand in pk:
            return cand
        if not p:
            return None
        p = p.rsplit('/', 1)[0] if '/' in p else ''


DEP_FIELDS = ('dependencies', 'optionalDependencies', 'peerDependencies', 'devDependencies')


def parents_of(pk, target):
    """Every entry P (the root '' included) declaring `name` whose resolution lands on `target`, with the declared range(s).
    devDependencies count only for the root and for workspace (non-node_modules) entries, as npm installs them."""
    name = pkg_name(target); out = []
    for p, e in pk.items():
        if e.get('link'):
            continue
        for f in DEP_FIELDS:
            if f == 'devDependencies' and pkg_name(p) is not None:
                continue
            r = (e.get(f) or {}).get(name)
            if r is not None and resolve_path(pk, p, name) == target:
                out.append((p, f, r))
    return out


def leaf_diff(a, b, path=''):
    """[g72] [(kind, path, old, new)] kind in change / add / remove / order. Dicts recurse; lists compare whole."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        common_a = [k for k in a if k in b]; common_b = [k for k in b if k in a]
        if common_a != common_b:
            out.append(('order', path or '<top>', list(a), list(b)))
        for k in a:
            p = '%s/%s' % (path, k) if path else k
            if k not in b: out.append(('remove', p, a[k], None))
            else: out += leaf_diff(a[k], b[k], p)
        for k in b:
            if k not in a: out.append(('add', '%s/%s' % (path, k) if path else k, None, b[k]))
        return out
    return [] if a == b else [('change', path, a, b)]


# ---------------- an independent semver subset (carried from lib_gate70 unchanged) ----------------
def _parse(v):
    m = re.match(r'^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?$', v.strip())
    if not m:
        raise ValueError('not a version: %r' % v)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))), m.group(4)


def _partial(s):
    s = s.strip().lstrip('v=')
    parts = s.split('.') if s not in ('', '*', 'x', 'X') else []
    nums = []
    for x in parts[:3]:
        x = x.split('-')[0]
        if x in ('*', 'x', 'X'):
            break
        nums.append(int(x))
    return nums


def _cmp(a, b): return (a > b) - (a < b)


def _expand(tok):
    m = re.match(r'^(>=|<=|>|<|=|\^|~>?)?\s*(.*)$', tok.strip())
    op, rest = m.group(1) or '', m.group(2)
    n = _partial(rest)
    if op in ('', '=') and len(n) == 3:
        return [('=', tuple(n))]
    if op in ('', '=') and len(n) < 3:
        if not n: return [('>=', (0, 0, 0))]
        lo = tuple(n + [0] * (3 - len(n))); hi = (n[0] + 1, 0, 0) if len(n) == 1 else (n[0], n[1] + 1, 0)
        return [('>=', lo), ('<', hi)]
    full = tuple(n + [0] * (3 - len(n)))
    if op in ('>=', '<=', '>', '<'):
        if op == '>' and len(n) < 3:
            return [('>=', (n[0] + 1, 0, 0) if len(n) == 1 else (n[0], n[1] + 1, 0))]
        if op == '<=' and len(n) < 3:
            return [('<', (n[0] + 1, 0, 0) if len(n) == 1 else (n[0], n[1] + 1, 0))]
        return [(op, full)]
    if op.startswith('~'):
        hi = (n[0] + 1, 0, 0) if len(n) == 1 else (n[0], n[1] + 1, 0)
        return [('>=', full), ('<', hi)]
    if op == '^':
        if n[0] > 0 or len(n) == 1: hi = (n[0] + 1, 0, 0)
        elif len(n) == 2 or n[1] > 0: hi = (0, n[1] + 1, 0)
        else: hi = (0, 0, n[2] + 1)
        return [('>=', full), ('<', hi)]
    raise ValueError('unsupported token %r' % tok)


def satisfies(version, rng):
    v, pre = _parse(version)
    if pre:
        return False
    for alt in rng.split('||'):
        alt = alt.strip()
        hm = re.match(r'^(\S+)\s+-\s+(\S+)$', alt)
        if hm:
            comps = [('>=', tuple(_partial(hm.group(1)) + [0] * (3 - len(_partial(hm.group(1))))))] + \
                    [c for c in _expand('<=' + hm.group(2))]
        else:
            alt = re.sub(r'(>=|<=|>|<|=|\^|~>?)\s+', r'\1', alt)
            comps = [c for t in alt.split() for c in _expand(t)] if alt else [('>=', (0, 0, 0))]
        ok = True
        for op, b in comps:
            c = _cmp(v, b)
            ok &= {'=': c == 0, '>=': c >= 0, '<=': c <= 0, '>': c > 0, '<': c < 0}[op]
        if ok:
            return True
    return False


# ---------------- registry ----------------
def sri_sha512(data): return 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode()


def http_get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'gate72-qa'}), timeout=timeout).read()


def packument(name):
    return json.loads(http_get('https://registry.npmjs.org/%s' % name.replace('/', '%2F') if name.startswith('@') else 'https://registry.npmjs.org/%s' % name))


def tgz_url(name, ver): return 'https://registry.npmjs.org/%s/-/%s-%s.tgz' % (name, name.split('/')[-1], ver)


def bulk_advisories(payload):
    """POST registry.npmjs.org/-/npm/v1/security/advisories/bulk — a READ (leg 7's own instrument, audit-locks.mjs)."""
    req_ = urllib.request.Request('https://registry.npmjs.org/-/npm/v1/security/advisories/bulk', data=json.dumps(payload).encode(),
                                  headers={'Content-Type': 'application/json', 'User-Agent': 'gate72-qa'}, method='POST')
    return json.load(urllib.request.urlopen(req_, timeout=60))


def ids_of(resp):
    out = {}
    for pkg, advs in resp.items():
        for a in advs:
            gid = a.get('github_advisory_id') or (a.get('url') or '').rsplit('/', 1)[-1]
            out[gid] = (pkg, a.get('severity'), a.get('vulnerable_versions'))
    return out


# ---------------- GitHub / Linear (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate72: %s not present in the Secuura .env (by name)' % name)


def gh_get(path, raw=False):
    tok = env_value('GH_TOKEN')
    r = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                               headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'})
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
