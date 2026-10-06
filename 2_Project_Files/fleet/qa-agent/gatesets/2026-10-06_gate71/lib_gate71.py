#!/usr/bin/env python3
"""lib_gate71.py — shared helper for the gate71 kit. WIDENED 2026-10-07 to TWO ROWS: #1404 (KS-1436, T2, job 06 stderr to its own file,
#1398's merge condition, merges FIRST) and #1398 (KS-1136, T1: an unparseable security artefact must not read as a clean scan).

  ROW / P              the PR row: `--pr <1404|1398>` on the command line, else G71_ROW, else 1398 WITH A STDERR NOTE (never silent).
                       P = K['rows'][ROW]. Every script prints its row in its first line.

  K                    the kit (kit.json beside this file; G71_KITJSON overrides it for the self-tests only).
  git(repo, *args)     READ verbs only. Any other verb raises.
  wgit(repo, *args)    WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath). GIT_SSH_COMMAND is dropped.
  resolvable / absent_objects   an object that is not a commit in the repo is REFUSED BY NAME (rc 2), never read as "different".
  READERS              the NEWLINE-TOLERANT h2 readers, EXTRACTED from composee5_copy.py at its pinned lines (:66 flow, :82 cheat); the copy's
                       sha256 is asserted at import (no third implementation). The OLD same-line reader exists only as a proof's negative arm.
  gh_get / gh_pages    read-only GitHub REST GETs (X6). GH_TOKEN read BY NAME from the Secuura .env inside this helper, never printed.
  gh_job_log(job_id)   the job-logs endpoint 302s to a signed URL: the redirect is followed WITHOUT the Authorization header (a reader
                       that follows it with the header, or swallows the error, returns a placeholder and every needle reads 0).
"""
import hashlib, json, os, re, subprocess, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('G71_SCRATCH', os.path.join(HERE, '_scratch'))
K = json.load(open(os.environ.get('G71_KITJSON', os.path.join(HERE, 'kit.json')), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config',
              'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'merge-tree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree', 'worktree', 'fetch'}
FORBIDDEN = os.environ.get('G71_FORBIDDEN_ROOT', K['forbidden_root'])
D = K['docs']


def _row():
    a = sys.argv
    if '--pr' in a and a.index('--pr') + 1 < len(a): r = a[a.index('--pr') + 1]
    elif os.environ.get('G71_ROW'): r = os.environ['G71_ROW']
    else:
        r = '1398'; sys.stderr.write('lib_gate71: NOTE row defaulted to 1398 (pass --pr <1404|1398>)\n')
    if r not in K['rows']: raise SystemExit('lib_gate71: REFUSED — unknown row %r (kit rows %s)' % (r, list(K['rows'])))
    return r


ROW = _row()
P = K['rows'][ROW]


# ---------------- composee5's readers, extracted, never re-typed ----------------
def _load_readers():
    rs = K['reader_source']; p = os.path.join(HERE, rs['copy'])
    raw = open(p, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
    if h != rs['sha256']:
        raise SystemExit('lib_gate71: REFUSED — %s sha256 %s != pinned %s (the reader source changed)' % (rs['copy'], h[:16], rs['sha256'][:16]))
    lines = raw.decode('utf-8').split('\n'); out = {}
    for name, ln in (('flow_num', rs['flow_num_line']), ('cheat_key', rs['cheat_key_line'])):
        m = re.search(r"re\.findall\(r'(.+?)', \"\\n\"\.join\(lines\), (re\.S \| re\.I)\)", lines[ln - 1])
        if not m:
            raise SystemExit('lib_gate71: REFUSED — %s:%d does not hold the expected re.findall reader' % (rs['copy'], ln))
        out[name] = re.compile(m.group(1), re.S | re.I)
    return out


READERS = _load_readers()
FLOW_NUM_RX = READERS['flow_num']        # <h2[^>]*>\s*(\d+)\.                    (re.S | re.I)
CHEAT_KEY_RX_PINNED = READERS['cheat_key']   # <h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>  (re.S | re.I) — BLIND on develop after #1402
if CHEAT_KEY_RX_PINNED.pattern.count('&mdash;') != 1:
    raise SystemExit('lib_gate71: REFUSED — the pinned cheat reader no longer carries exactly one `&mdash;` to widen')
# WIDENED 2026-10-07: #1402 rewrote the cheat sheet with the CHARACTER U+2014 where the pinned reader wants the ENTITY `&mdash;`, so the
# pinned reader reads 0 keys on develop. The widened reader is DERIVED from the pinned one (one substitution, asserted), never re-typed.
CHEAT_KEY_RX = re.compile(CHEAT_KEY_RX_PINNED.pattern.replace('&mdash;', '(?:&mdash;|\u2014)'), re.S | re.I)
CLOSE_RX = re.compile(D['close_tag_rx'])
OLD_SAMELINE_RX = re.compile(K['old_sameline_rx'])
H2_OPEN_RX = re.compile(r'<h2\b', re.I)


def flow_nums(text): return [int(x) for x in FLOW_NUM_RX.findall(text)]
def flow_num_pos(text): return [(int(m.group(1)), text.count('\n', 0, m.start())) for m in FLOW_NUM_RX.finditer(text)]
def old_sameline_nums(text): return [int(m.group(1)) for l in text.split('\n') for m in [OLD_SAMELINE_RX.search(l)] if m]
def h2_open_count(text): return len(H2_OPEN_RX.findall(text))


def cheat_key_pos(text):
    """[(key, line of `<h2`)]. REFUSES when `<h2` openings != keyed matches (the lazy `.*?` would straddle an unkeyed h2 — gate67 D3)."""
    ms = list(CHEAT_KEY_RX.finditer(text))
    if len(ms) != h2_open_count(text):
        raise ValueError('cheat: %d `<h2` opening(s) but %d keyed h2 match(es)' % (h2_open_count(text), len(ms)))
    return [(m.group(1), text.count('\n', 0, m.start())) for m in ms]


def cheat_keys(text): return [k for k, _ in cheat_key_pos(text)]
def cheat_keys_pinned(text): return CHEAT_KEY_RX_PINNED.findall(text)


def close_idx(lines):
    """the index of the ONE `</body>` line (any indentation: base `  </body>`, develop `</body>`), else ValueError."""
    c = [i for i, l in enumerate(lines) if CLOSE_RX.match(l)]
    if len(c) != 1: raise ValueError('close tag %r matched %d line(s) (want 1)' % (D['close_tag_rx'], len(c)))
    return c[0]


# ---------------- git ----------------
def _run(repo, args, env=None, inp=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate71: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate71: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate71: git %s rc %d: %s' % (' '.join(args)[:120], rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def git_bytes(repo, rev, path):
    """the blob's exact BYTES: byte-equality claims are made on these, never on a decoded/re-encoded copy."""
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('lib_gate71: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def blob_at(repo, rev, path):
    """the blob sha of `path` at `rev`, or '' when the path is ABSENT there. Read with ls-tree: `rev-parse <rev>:<absent path>` can echo
    the argument itself on stdout (STANDING_LINES 2026-09-27), so two absences would compare as two DIFFERENT 'shas'."""
    f = git(repo, 'ls-tree', rev, '--', path).split()
    return f[2] if len(f) >= 3 and f[1] == 'blob' else ''


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None, inp=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate71: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate71: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    return _run(repo, args, env=e, inp=inp)


def resolvable(repo, sha):
    return bool(sha) and re.fullmatch(r'[0-9a-f]{40}', sha or '') is not None and \
        _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def absent_objects(repo, named):
    """[(name, sha)] of every NAMED sha that is not a full 40-hex commit in `repo`. A rev-parse of an absent object can hand back the
    argument itself (STANDING_LINES 2026-09-27), so absence is decided by `--verify ^{commit}`, never by comparing output."""
    return [(n, s) for n, s in named if not resolvable(repo, s)]


def refuse_absent(repo, named):
    bad = absent_objects(repo, named)
    for n, s in bad:
        print('REFUSED BY NAME: %s %r is not a commit in %s — fetch it BY SHA into YOUR clone (X7), then re-run' % (n, s, repo))
    return 2 if bad else 0


# ---------------- GitHub (GET / read-only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate71: %s not present in the Secuura .env (by name)' % name)


def gh_get(path):
    req = urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], path),
                                 headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def gh_pages(path):
    out, page = [], 1
    while True:
        got = gh_get('%s%sper_page=100&page=%d' % (path, '&' if '?' in path else '?', page))
        items = got if isinstance(got, list) else got.get('jobs', got.get('workflow_runs', []))
        out += items
        if len(items) < 100:
            return out
        page += 1


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


def gh_job_log(job_id):
    """text of a job log. Step 1 WITH auth, redirects NOT followed; step 2 the Location WITHOUT the Authorization header."""
    op = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request('https://api.github.com/repos/%s/actions/jobs/%s/logs' % (K['gh_repo'], job_id),
                                 headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    try:
        r = op.open(req, timeout=60); return r.read().decode('utf-8', 'replace')     # a 200 without redirect (rare)
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308) or not e.headers.get('Location'):
            raise
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


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
