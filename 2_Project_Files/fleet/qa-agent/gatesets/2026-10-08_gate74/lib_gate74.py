#!/usr/bin/env python3
"""lib_gate74.py — shared helper for the gate74 kit: ONE row (#1423 KS-1164, tier 2) on base b280b74ff07b; develop eae08a3f441c at draft.
  Carried from lib_gate73.py (gate73, four rows) and re-keyed by the gate74 drafter: G73_ -> G74_, gate73 -> gate74, the row prose below.

  ROW / P              `--pr 1423` on the command line, else G74_ROW. There is NO default row even with ONE member: a script that
                       needs one and gets none REFUSES (a default is a value nobody passed; gate73's rule carried unchanged).
  K                    the kit (kit.json beside this file; G74_KITJSON overrides it for the self-tests and launcher arms only).
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath). GIT_SSH_COMMAND is dropped.
  obj_at(repo,rev,p)   the object sha of a path (blob OR tree) at rev, or '' when ABSENT — read with ls-tree, never `rev-parse rev:path`
                       (that ECHOES the argument for an absent path: STANDING_LINES 2026-09-27 / 2026-10-07).
  READERS              composee5's newline-tolerant h2 readers, EXTRACTED from composee5_copy.py at its pinned lines (sha256 asserted),
                       the cheat reader WIDENED to `&mdash;` OR U+2014 by ONE asserted substitution (base b280b74f carries both forms,
                       inherited from gate73's #1407 (`&mdash;`) and #1408 (U+2014) blocks; #1423's block writes U+2014).
  gh_get / gh_job_log  read-only GitHub REST GETs; GH_TOKEN read BY NAME from the Secuura .env inside this helper, never printed. The
                       job-logs 302 is followed WITHOUT the Authorization header (STANDING_LINES 2026-10-06, Seat E 8th).
"""
import hashlib, json, os, re, subprocess, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.environ.get('G74_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref', 'archive'}
WRITE_VERBS = {'merge-tree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree', 'worktree', 'fetch'}
FORBIDDEN = os.environ.get('G74_FORBIDDEN_ROOT', K['forbidden_root'])
D = K['docs']
ROWS = K['rows']
BASE = K['base']


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def row_arg(required=True):
    r = opt(sys.argv, '--pr') or os.environ.get('G74_ROW')
    if r is None:
        if required: raise SystemExit('lib_gate74: REFUSED — no row (pass --pr <%s>); no default row' % '|'.join(ROWS))
        return None
    if r not in ROWS: raise SystemExit('lib_gate74: REFUSED — unknown row %r (kit rows %s)' % (r, list(ROWS)))
    return r


def code_paths(R): return sorted(p for p in R['numstat'] if not p.startswith('Projects Documents/'))


# ---------------- composee5's readers, extracted, never re-typed ----------------
def _load_readers():
    rs = K['reader_source']; p = os.path.join(HERE, rs['copy'])
    raw = open(p, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
    if h != rs['sha256']:
        raise SystemExit('lib_gate74: REFUSED — %s sha256 %s != pinned %s' % (rs['copy'], h[:16], rs['sha256'][:16]))
    lines = raw.decode('utf-8').split('\n'); out = {}
    for name, ln in (('flow_num', rs['flow_num_line']), ('cheat_key', rs['cheat_key_line'])):
        m = re.search(r"re\.findall\(r'(.+?)', \"\\n\"\.join\(lines\), (re\.S \| re\.I)\)", lines[ln - 1])
        if not m: raise SystemExit('lib_gate74: REFUSED — %s:%d does not hold the expected re.findall reader' % (rs['copy'], ln))
        out[name] = re.compile(m.group(1), re.S | re.I)
    return out


READERS = _load_readers()
FLOW_NUM_RX = READERS['flow_num']
CHEAT_KEY_RX_PINNED = READERS['cheat_key']
if CHEAT_KEY_RX_PINNED.pattern.count('&mdash;') != 1:
    raise SystemExit('lib_gate74: REFUSED — the pinned cheat reader no longer carries exactly one `&mdash;` to widen')
CHEAT_KEY_RX = re.compile(CHEAT_KEY_RX_PINNED.pattern.replace('&mdash;', '(?:&mdash;|\u2014)'), re.S | re.I)
CLOSE_RX = re.compile(D['close_tag_rx'])
OLD_SAMELINE_RX = re.compile(K['old_sameline_rx'])
H2_OPEN_RX = re.compile(r'<h2\b', re.I)


def flow_nums(text): return [int(x) for x in FLOW_NUM_RX.findall(text)]
def flow_num_pos(text): return [(int(m.group(1)), text.count('\n', 0, m.start())) for m in FLOW_NUM_RX.finditer(text)]
def old_sameline_nums(text): return [int(m.group(1)) for l in text.split('\n') for m in [OLD_SAMELINE_RX.search(l)] if m]
def h2_open_count(text): return len(H2_OPEN_RX.findall(text))


def cheat_key_pos(text):
    """[(key, line of `<h2`)]. REFUSES when `<h2` openings != keyed matches (a lazy `.*?` would straddle an unkeyed h2 — gate67 D3)."""
    ms = list(CHEAT_KEY_RX.finditer(text))
    if len(ms) != h2_open_count(text):
        raise ValueError('cheat: %d `<h2` opening(s) but %d keyed h2 match(es)' % (h2_open_count(text), len(ms)))
    return [(m.group(1), text.count('\n', 0, m.start())) for m in ms]


def cheat_keys(text): return [k for k, _ in cheat_key_pos(text)]
def cheat_keys_pinned(text): return CHEAT_KEY_RX_PINNED.findall(text)


def close_idx(lines):
    c = [i for i, l in enumerate(lines) if CLOSE_RX.match(l)]
    if len(c) != 1: raise ValueError('close tag %r matched %d line(s) (want 1)' % (D['close_tag_rx'], len(c)))
    return c[0]


# ---------------- git ----------------
def _run(repo, args, env=None, inp=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate74: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate74: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate74: git %s rc %d: %s' % (' '.join(args)[:120], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0: raise SystemExit('lib_gate74: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
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
        raise SystemExit('lib_gate74: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate74: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
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


# ---------------- GitHub (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate74: %s not present in the Secuura .env (by name)' % name)


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
