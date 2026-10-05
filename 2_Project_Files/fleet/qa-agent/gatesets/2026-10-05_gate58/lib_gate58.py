#!/usr/bin/env python3
"""lib_gate58.py — shared helpers for the gate58 check scripts (a NEW COPY of lib_gate54f.py plus gate56a's guard_out and a tiny semver
range reader). git() allows READ verbs only (show, ls-tree, rev-parse, cat-file, log, diff, rev-list, merge-base, ls-remote): nothing here
writes to a repository. Imported by c1..c6; never run on its own."""
import json, os, re, subprocess, datetime, difflib, urllib.request, urllib.error, time, sys

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'ls-tree', 'rev-parse', 'cat-file', 'log', 'diff', 'rev-list', 'merge-base', 'ls-remote'}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def opt_factory(A):
    return lambda n, d=None: A[A.index(n) + 1] if n in A and A.index(n) + 1 < len(A) else d


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gate58.git allows read verbs only, got %r' % a[0])
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def commit(repo, rev):
    rc, out, err = git(repo, 'rev-parse', '--verify', '--quiet', rev + '^{commit}', check=False)
    if rc:
        raise SystemExit('REFUSING: %s does not resolve to a commit in %s (fetch it into YOUR clone first)' % (rev, repo))
    return out.strip()


def show(repo, sha, path):
    """blob text at sha:path, resolved with cat-file -e first (rev-parse ECHOES an unresolved path)"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    return git(repo, 'show', '%s:%s' % (sha, path))


def blob(repo, sha, path):
    l = git(repo, 'ls-tree', sha, '--', path).strip()
    return l.split()[2] if l else None


def _under(p, root):
    p, root = os.path.normpath(p), os.path.normpath(root)
    return p == root or p.startswith(root + os.sep)


def forbidden_root():
    """kit forbidden_root; G58_FORBIDDEN_ROOT overrides it so a REFUSAL ARM can be driven with a path inside the drafter's/tester's scratch"""
    return os.environ.get('G58_FORBIDDEN_ROOT') or K['forbidden_root']


def guard_out(path, create=True):
    """refuse (SystemExit 2, NOTHING created) a path under the forbidden root unless under the QA reports root; lexical test FIRST, then the
    realpath of the nearest existing ancestor (a symlink cannot smuggle a write in), then mkdir"""
    lex = os.path.abspath(path); fr, rr = forbidden_root(), K['reports_root']
    if _under(lex, fr) and not _under(lex, rr):
        print('REFUSING: %s is inside %s but not under the QA reports root (nothing was created or run)' % (lex, fr)); raise SystemExit(2)
    anc = lex
    while not os.path.exists(anc):
        anc = os.path.dirname(anc)
    real = os.path.join(os.path.realpath(anc), os.path.relpath(lex, anc)) if anc != lex else os.path.realpath(lex)
    if _under(real, fr) and not _under(real, rr):
        print('REFUSING: %s resolves to %s inside %s (nothing was created or run)' % (lex, real, fr)); raise SystemExit(2)
    if create:
        os.makedirs(lex, exist_ok=True)
    return lex


def guard_worktree(path):
    """a directory the legs may RUN in: never under the forbidden root at all (not even the reports root), lexically AND by realpath"""
    lex = os.path.abspath(path); fr = forbidden_root()
    if _under(lex, fr) or _under(os.path.realpath(lex), fr):
        print('REFUSING: %s is under %s — run legs only in YOUR OWN worktree in your scratchpad, never the shared checkout or a builder\'s worktree (nothing was run)' % (lex, fr))
        raise SystemExit(2)
    return lex


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


def _depth(s):
    """net bracket depth of one line of pretty-printed JSON, IGNORING brackets inside strings"""
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


def block(text, key):
    ls = text.split('\n'); i = find_member(ls, key)
    if i is None:
        return None
    sp = member_span(ls, i)
    return '\n'.join(ls[sp[0]:sp[1] + 1]).rstrip(',') if sp else None


def opcodes(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False)
    return [op for op in sm.get_opcodes() if op[0] != 'equal']


# ---- a tiny semver range reader: enough for npm lock `dependencies` ranges (^ ~ >= > <= < = x, space-AND, ||, hyphen). NOT full semver:
# an unparseable range returns None and the caller reports it as UNPARSED (never as satisfied).
def _v(s):
    m = re.fullmatch(r'v?(\d+)(?:\.(\d+|x|\*))?(?:\.(\d+|x|\*))?(?:-([0-9A-Za-z.-]+))?(?:\+.*)?', s.strip())
    if not m: return None
    parts = [m.group(1), m.group(2), m.group(3)]
    return parts, m.group(4)


def _t(parts):
    return tuple(int(p) if p not in (None, 'x', '*') else 0 for p in parts)


def _cmp_set(rng):
    """one space-separated comparator set -> list of (op, tuple) or None"""
    rng = rng.strip()
    if rng in ('', '*', 'x', 'latest'):
        return []
    m = re.fullmatch(r'(\S+)\s+-\s+(\S+)', rng)
    if m:
        a, b = _v(m.group(1)), _v(m.group(2))
        return None if not a or not b else [('>=', _t(a[0])), ('<=', _t(b[0]))]
    out = []
    for tok in re.findall(r'(?:[<>]=?|=|\^|~)?\s*v?[0-9x*][^\s]*', rng):
        m = re.fullmatch(r'([<>]=?|=|\^|~)?\s*(.+)', tok)
        op, ver = m.group(1) or '', m.group(2); pv = _v(ver)
        if not pv: return None
        parts, pre = pv; t = _t(parts); wild = [p in (None, 'x', '*') for p in parts]
        if op == '^':
            if t[0] > 0 or wild[1]: up = (t[0] + 1, 0, 0)
            elif t[1] > 0 or wild[2]: up = (0, t[1] + 1, 0)
            else: up = (0, 0, t[2] + 1)
            out += [('>=', t), ('<', up)]
        elif op == '~':
            up = (t[0] + 1, 0, 0) if wild[1] else (t[0], t[1] + 1, 0)
            out += [('>=', t), ('<', up)]
        elif op in ('', '=') and any(wild):
            if wild[0]: continue
            up = (t[0] + 1, 0, 0) if wild[1] else (t[0], t[1] + 1, 0)
            out += [('>=', t), ('<', up)]
        else:
            out.append((op or '=', t))
    return out


def satisfies(version, rng):
    """True / False, or None when the range or version is not readable by this reader"""
    pv = _v(version)
    if not pv or pv[1]:
        return None
    v = _t(pv[0])
    any_ok = False
    for alt in rng.split('||'):
        cs = _cmp_set(alt)
        if cs is None:
            return None
        ok = all({'<': v < t, '<=': v <= t, '>': v > t, '>=': v >= t, '=': v == t}[op] for op, t in cs)
        any_ok |= ok
    return any_ok


class Checks:
    def __init__(self, quiet=False):
        self.res = []; self.tags = []; self.quiet = quiet

    def failed(self, prefix=''):
        return [t for t, ok in self.tags if not ok and t.startswith(prefix)]

    def chk(self, tag, ok, msg):
        self.res.append(bool(ok)); self.tags.append((tag, bool(ok)))
        if not self.quiet:
            print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
        return bool(ok)

    def nfail(self):
        return self.res.count(False)
