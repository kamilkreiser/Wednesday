#!/usr/bin/env python3
"""lib_gate70.py — shared helper for the gate70 kit (#1397 KS-1425, T1: in-range LOCK-ONLY refresh + 2 baseline rows).

  K                    the kit (kit.json beside this file; G70_KITJSON overrides it for the self-tests only).
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  gh_get(path)         read-only GitHub REST GET of repos/<gh_repo>/<path>; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  linear_issue(key)    read-only Linear GraphQL `issue(id)`; LINEAR_API_KEY read BY NAME, never printed.
  satisfies(v, range)  an INDEPENDENT node-semver subset (|| , hyphen, ^, ~, x/*, comparators) — NOT the repo's semver, so the
                       parent walk does not share the gate's own dependency. Self-tested in c2 --selftest against hand cases.
  resolve_path(pk, from_path, name)   npm's nearest-node_modules walk inside a lockfileVersion-3 `packages` map.
  detect_indent / roundtrip_exact     indent per FILE (D2), and the byte-exact json round-trip (proves no file was reformatted).
"""
import base64, hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('G70_SCRATCH', os.path.join(HERE, '_scratch'))
K = json.load(open(os.environ.get('G70_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'fetch', 'worktree', 'checkout', 'hash-object'}
FORBIDDEN = os.environ.get('G70_FORBIDDEN_ROOT', K['forbidden_root'])


# ---------------- git ----------------
def _run(repo, args, env=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate70: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate70: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate70: git %s rc %d: %s' % (' '.join(args), rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    """The blob's exact BYTES (no decode/re-encode): byte-equality claims are made on these."""
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate70: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate70: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate70: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
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
    """`node_modules/a/node_modules/@s/b` -> `@s/b`; a non-node_modules path (a workspace) -> None."""
    i = path.rfind('node_modules/')
    return path[i + len('node_modules/'):] if i >= 0 else None


def resolve_path(pk, from_path, name):
    """npm's lookup: from a package at `from_path`, the dependency `name` resolves to the NEAREST `<dir>/node_modules/<name>`
    walking up to the root. Returns the key in `pk` or None."""
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


# ---------------- an independent semver subset ----------------
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
    """one range token -> [(op, (maj,min,pat))]"""
    m = re.match(r'^(>=|<=|>|<|=|\^|~>?)?\s*(.*)$', tok.strip())
    op, rest = m.group(1) or '', m.group(2)
    n = _partial(rest)
    if op in ('', '=') and len(n) == 3:
        return [('=', tuple(n))]
    if op in ('', '=') and len(n) < 3:      # x-range
        if not n: return [('>=', (0, 0, 0))]
        lo = tuple(n + [0] * (3 - len(n))); hi = (n[0] + 1, 0, 0) if len(n) == 1 else (n[0], n[1] + 1, 0)
        return [('>=', lo), ('<', hi)]
    full = tuple(n + [0] * (3 - len(n)))
    if op in ('>=', '<=', '>', '<'):
        if op == '>' and len(n) < 3:  # >1.2 means >=1.3.0
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
        return False   # no prerelease is in this change set; refuse rather than guess node-semver's prerelease rule
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


def vlt(a, b): return _parse(a)[0] < _parse(b)[0]


# ---------------- registry ----------------
def sri_sha512(data): return 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode()


def http_get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'gate70-qa'}), timeout=timeout).read()


def bulk_advisories(payload):
    """POST registry.npmjs.org/-/npm/v1/security/advisories/bulk — a READ (the registry's own query endpoint)."""
    req = urllib.request.Request('https://registry.npmjs.org/-/npm/v1/security/advisories/bulk', data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json', 'User-Agent': 'gate70-qa'}, method='POST')
    return json.load(urllib.request.urlopen(req, timeout=60))


# ---------------- GitHub / Linear (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate70: %s not present in the Secuura .env (by name)' % name)


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


def linear_issue(key):
    q = 'query($id:String!){issue(id:$id){identifier title state{name type} updatedAt archivedAt}}'
    req = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': {'id': key}}).encode(),
                                 headers={'Content-Type': 'application/json', 'Authorization': env_value('LINEAR_API_KEY')}, method='POST')
    return json.load(urllib.request.urlopen(req, timeout=60))


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
