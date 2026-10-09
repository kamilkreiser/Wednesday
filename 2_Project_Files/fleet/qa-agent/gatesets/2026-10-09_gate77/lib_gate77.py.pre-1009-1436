#!/usr/bin/env python3
"""lib_gate77.py — shared helper for the gate77 kit: SIX rows (Secuura/Blockchain #1429 #1430 #1431 #1432 #1433 #1434), each ONE commit on
the RAISE_BASE 0a6177ea5482, gated against a develop that has MOVED since they were cut (1e7f90e26137 = #1428 at draft; #1427 is GO'd and
will move it again). Carried from lib_gate76.py (git / wgit / readers / GH GETs / Tally) and widened by the gate77 drafter:
G76_ -> GATE77_, two rows -> six, plus the keep-both DOCS composer (block extraction, compose, read-back) used by c2_merge_gate77.py.

  ROW                  `--pr <n>` on the command line. There is NO default row (six rows make a default a trap).
  K                    the kit (kit.json beside this file; GATE77_KITJSON overrides it for self-tests and launcher arms ONLY).
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath). GIT_SSH_COMMAND dropped.
                       GATE77_FORBIDDEN_ROOT overrides the root for the self-test's refusal arm (a SCRATCH path, never a real sibling).
  READERS              flow numbers `<h2…>N.` (composee5's pinned reader) and cheat keys read ONE HEADING AT A TIME (gate76's reader).
  block_of / compose   the docs keep-both primitives: a row's doc change must be ONE pure insertion immediately before `</body>`.
  gh_get               read-only GitHub REST GETs; GH_TOKEN read BY NAME from the Secuura .env inside this helper, never printed.
"""
import difflib, hashlib, json, os, re, subprocess, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('GATE77_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref', 'interpret-trailers'}
WRITE_VERBS = {'merge-tree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree', 'worktree', 'fetch',
               'merge-file', 'init', 'add', 'commit', 'update-ref'}
FORBIDDEN = os.environ.get('GATE77_FORBIDDEN_ROOT', K['forbidden_root'])
DOCS = K['docs']
DOC_PATHS = [DOCS['flow'], DOCS['cheat']]
ROWS = K['rows']
RAISE_BASE = K['raise_base']


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def row_arg():
    r = opt(sys.argv, '--pr')
    if r is None: raise SystemExit('lib_gate77: REFUSED — no row (pass --pr <%s>); six rows, no default' % '|'.join(ROWS))
    if r not in ROWS: raise SystemExit('lib_gate77: REFUSED — unknown row %r (kit rows %s)' % (r, list(ROWS)))
    return r


def code_paths(R): return sorted(p for p in R['numstat'] if p not in DOC_PATHS)


# ---------------- composee5's flow reader, extracted, never re-typed (carried from lib_gate76) ----------------
def _load_flow_reader():
    rs = K['reader_source']; p = os.path.join(HERE, rs['copy'])
    raw = open(p, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
    if h != rs['sha256']:
        raise SystemExit('lib_gate77: REFUSED — %s sha256 %s != pinned %s' % (rs['copy'], h[:16], rs['sha256'][:16]))
    line = raw.decode('utf-8').split('\n')[rs['flow_num_line'] - 1]
    m = re.search(r"re\.findall\(r'(.+?)', \"\\n\"\.join\(lines\), (re\.S \| re\.I)\)", line)
    if not m: raise SystemExit('lib_gate77: REFUSED — %s:%d does not hold the expected re.findall reader' % (rs['copy'], rs['flow_num_line']))
    return re.compile(m.group(1), re.S | re.I)


FLOW_NUM_RX = _load_flow_reader()
H2_OPEN_RX = re.compile(r'<h2\b', re.I)
H2_WHOLE_RX = re.compile(r'<h2\b[^>]*>(.*?)</h2>', re.S | re.I)
DASH_KEY_RX = re.compile(r'(?:&mdash;|\u2014)\s*(KS-\d+)')
CLOSE_RX = re.compile(r'^\s*</body>\s*$')


def flow_nums(text): return [int(x) for x in FLOW_NUM_RX.findall(text)]


def cheat_keys(text):
    """ONE HEADING AT A TIME (gate76): each `<h2…>…</h2>` read alone, its key the LAST `— KS-n` inside it. Refuses a `<h2` opening that is not
    a whole heading, or a heading with no dash key (develop carries `— KS-1445 (with KS-1367)</h2>`, which a lazy whole-text reader straddles)."""
    ms = list(H2_WHOLE_RX.finditer(text))
    if len(ms) != len(H2_OPEN_RX.findall(text)):
        raise ValueError('cheat: %d `<h2` opening(s) but %d whole headings' % (len(H2_OPEN_RX.findall(text)), len(ms)))
    out = []
    for m in ms:
        ks = DASH_KEY_RX.findall(m.group(1))
        if not ks: raise ValueError('cheat: an <h2> carries no `— KS-n` key: %r' % m.group(1)[:80])
        out.append(ks[-1])
    return out


def seq_of(path, text): return flow_nums(text) if path == DOCS['flow'] else cheat_keys(text)


VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'col', 'area', 'base', 'wbr', 'source', 'track', 'embed', 'param'}
TAG_RX = re.compile(r'<(/?)([A-Za-z][A-Za-z0-9]*)(\s[^>]*)?>')


def tag_balance(text):
    """{tag: opens - closes} over every non-void tag, attribute-aware (`<code class=…>` counts as `<code`). Self-closing `<x/>` ignored."""
    bal = {}
    for m in TAG_RX.finditer(text):
        t = m.group(2).lower()
        if t in VOID or (m.group(3) or '').rstrip().endswith('/'): continue
        bal[t] = bal.get(t, 0) + (-1 if m.group(1) else 1)
    return {k: v for k, v in bal.items() if v}


def close_idx(lines):
    c = [i for i, l in enumerate(lines) if CLOSE_RX.match(l)]
    if len(c) != 1: raise ValueError('`</body>` matched %d line(s) (want 1)' % len(c))
    return c[0]


def block_of(base_text, head_text):
    """The row's doc change as ONE pure insertion IMMEDIATELY before `</body>`; returns the inserted lines (keepends). Raises otherwise."""
    a = base_text.splitlines(True); b = head_text.splitlines(True)
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert':
        raise ValueError('doc change is not ONE pure insertion: %s' % [(o[0], o[1], o[2], o[3], o[4]) for o in ops][:4])
    _, i1, _, j1, j2 = ops[0]
    blk = b[j1:j2]
    # difflib may slide an insertion across identical lines; re-anchor and REQUIRE it to sit right before </body>
    if a[:close_idx(a)] + blk + a[close_idx(a):] != b:
        raise ValueError('the insertion does not sit immediately before `</body>` (anchor at base line %d, close at %d)' % (i1 + 1, close_idx(a) + 1))
    return blk


def compose(cur_text, blk):
    a = cur_text.splitlines(True); c = close_idx(a)
    return ''.join(a[:c] + blk + a[c:])


# ---------------- git ----------------
def _run(repo, args, env=None, inp=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate77: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate77: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate77: git %s rc %d: %s' % (' '.join(args)[:120], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0: raise SystemExit('lib_gate77: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def obj_at(repo, rev, path):
    f = git(repo, 'ls-tree', rev, '--', path).split()
    return f[2] if len(f) >= 3 and f[1] in ('blob', 'tree') else ''


def mode_at(repo, rev, path):
    f = git(repo, 'ls-tree', rev, '--', path).split()
    return f[0] if len(f) >= 3 else ''


def changed_paths(repo, a, b):
    return sorted(l for l in git(repo, 'diff', '--name-only', '--no-renames', a, b).split('\n') if l)


def numstat(repo, a, b):
    out = {}
    for l in git(repo, 'diff', '--numstat', '--no-renames', a, b).split('\n'):
        if not l: continue
        x, y, p = l.split('\t', 2); out[p] = [int(x), int(y)]
    return out


def outside_forbidden(path):
    lex = os.path.abspath(path); real = os.path.realpath(path); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None, inp=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate77: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate77: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e, inp=inp)


def resolvable(repo, sha):
    return bool(sha) and re.fullmatch(r'[0-9a-f]{40}', sha or '') is not None and _run(repo, ['cat-file', '-e', sha + '^{commit}'])[0] == 0


def refuse_absent(repo, named):
    bad = [(n, s) for n, s in named if not resolvable(repo, s)]
    for n, s in bad:
        print('REFUSED BY NAME: %s %r is not a full 40-hex commit in %s — fetch it BY SHA into YOUR clone, then re-run' % (n, s, repo))
    return 2 if bad else 0


# ---------------- GitHub (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate77: %s not present in the Secuura .env (by name)' % name)


def gh_get(path):
    req = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                                 headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def gh_pages(path, key=None):
    out, page = [], 1
    while True:
        got = gh_get('%s%sper_page=100&page=%d' % (path, '&' if '?' in path else '?', page))
        items = got if isinstance(got, list) else got.get(key or 'workflow_runs', [])
        out += items
        if len(items) < 100 or page >= 10: return out
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
