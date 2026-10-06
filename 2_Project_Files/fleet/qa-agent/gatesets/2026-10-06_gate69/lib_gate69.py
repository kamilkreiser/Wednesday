#!/usr/bin/env python3
"""lib_gate69.py — shared helper for the gate69 BATCH kit (#1395 KS-1305 + KS-1256 as a parameter, T1). Adapted from lib_gate68 (G69_ env names; scratch
defaults to <kit>/_scratch; every write verb is refused inside the forbidden root).

  K                  the kit (kit.json beside this file).
  git(repo, *args)   READ verbs only. Any other verb raises.
  wgit(repo, *args)  WRITE verbs ONLY in a repository OUTSIDE K['forbidden_root'] (lexical AND realpath).
  gh_get(path)       read-only GitHub REST GET of repos/<gh_repo>/<path>; GH_TOKEN read BY NAME from the Secuura .env, never printed.
  READERS            the NEWLINE-TOLERANT h2 readers, taken VERBATIM from Seat E 5th's composee5.py (copied beside this file as
                     composee5_copy.py, sha256 pinned in kit.json). The regexes are EXTRACTED from the copy at the pinned lines
                     (:66 flow numbers, :82 cheat keys) and the copy's hash is asserted at import: no third implementation.
"""
import hashlib, json, os, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('G69_SCRATCH', os.path.join(HERE, '_scratch'))
K = json.load(open(os.path.join(HERE, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'ls-files', 'log', 'diff', 'ls-tree', 'cat-file', 'rev-parse', 'ls-remote', 'merge-base', 'rev-list', 'config', 'grep', 'status', 'for-each-ref'}
WRITE_VERBS = {'merge-tree', 'hash-object', 'mktree', 'commit-tree', 'read-tree', 'update-index', 'write-tree', 'checkout', 'worktree'}
FORBIDDEN = os.environ.get('G69_FORBIDDEN_ROOT', K['forbidden_root'])


# ---------------- composee5's readers, extracted, never re-typed ----------------
def _load_readers():
    p = os.path.join(HERE, K['reader_source']['copy'])
    raw = open(p, 'rb').read()
    h = hashlib.sha256(raw).hexdigest()
    if h != K['reader_source']['sha256']:
        raise SystemExit('lib_gate69: REFUSED — composee5_copy.py sha256 %s != pinned %s (the reader source changed)' % (h[:16], K['reader_source']['sha256'][:16]))
    lines = raw.decode('utf-8').split('\n')
    out = {}
    for name, ln in (('flow_num', K['reader_source']['flow_num_line']), ('cheat_key', K['reader_source']['cheat_key_line'])):
        m = re.search(r"re\.findall\(r'(.+?)', \"\\n\"\.join\(lines\), (re\.S \| re\.I)\)", lines[ln - 1])
        if not m:
            raise SystemExit('lib_gate69: REFUSED — composee5_copy.py:%d does not hold the expected re.findall reader' % ln)
        out[name] = re.compile(m.group(1), re.S | re.I)
    return out


READERS = _load_readers()
FLOW_NUM_RX = READERS['flow_num']        # composee5.py:66   <h2[^>]*>\s*(\d+)\.          (re.S | re.I)
CHEAT_KEY_RX = READERS['cheat_key']      # composee5.py:82   <h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>   (re.S | re.I)
OLD_SAMELINE_RX = re.compile(K['old_sameline_rx'])   # the pre-#1390 per-LINE reader, kept only as the proof's negative arm
H2_OPEN_RX = re.compile(r'<h2\b', re.I)


def flow_nums(text):
    return [int(x) for x in FLOW_NUM_RX.findall(text)]


def flow_num_pos(text):
    """[(num, offset of `<h2`, line index of `<h2`)] with the composee5 :66 reader."""
    return [(int(m.group(1)), m.start(), text.count('\n', 0, m.start())) for m in FLOW_NUM_RX.finditer(text)]


def cheat_keys(text):
    return CHEAT_KEY_RX.findall(text)


def cheat_key_pos(text):
    """positions. REFUSES (ValueError) when `<h2` openings != keyed matches: the :82 reader's `.*?` under re.S would then straddle an
    unkeyed h2 and the match START would be the WRONG heading (gate67 D3, carried)."""
    ms = list(CHEAT_KEY_RX.finditer(text))
    if len(ms) != len(H2_OPEN_RX.findall(text)):
        raise ValueError('cheat: %d `<h2` opening(s) but %d keyed h2 match(es) — an unkeyed h2 would make the :82 reader straddle'
                         % (len(H2_OPEN_RX.findall(text)), len(ms)))
    return [(m.group(1), m.start(), text.count('\n', 0, m.start())) for m in ms]


def old_sameline_nums(text):
    return [int(m.group(1)) for l in text.split('\n') for m in [OLD_SAMELINE_RX.search(l)] if m]


def h2_open_count(text): return len(H2_OPEN_RX.findall(text))


def split_h2_count(text):
    return sum(1 for m in re.finditer(r'<h2\b[^>]*>.*?</h2\s*>', text, re.S | re.I) if '\n' in m.group(0))


# ---------------- git ----------------
def _run(repo, args, env=None):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(repo, *args, check=True):
    if not args or args[0] not in READ_VERBS:
        raise SystemExit('lib_gate69: REFUSED non-read git verb %r' % (args[:1],))
    if args[0] == 'config' and '--get' not in args:
        raise SystemExit('lib_gate69: REFUSED git config without --get')
    rc, o, e = _run(repo, args)
    if check and rc != 0:
        raise SystemExit('lib_gate69: git %s rc %d: %s' % (' '.join(args), rc, e.strip()[:300]))
    return o if check else (rc, o, e)


def outside_forbidden(repo):
    lex = os.path.abspath(repo); real = os.path.realpath(repo); f = FORBIDDEN.rstrip('/')
    return not (lex == f or lex.startswith(f + '/') or real == f or real.startswith(os.path.realpath(f) + '/'))


def wgit(repo, *args, env=None, input_bytes=None):
    if not args or args[0] not in WRITE_VERBS | READ_VERBS:
        raise SystemExit('lib_gate69: REFUSED git verb %r' % (args[:1],))
    if args[0] in WRITE_VERBS and not outside_forbidden(repo):
        raise SystemExit('lib_gate69: REFUSED write verb %s inside %s (repo %s) — use your OWN scratch clone' % (args[0], FORBIDDEN, repo))
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=e, input=input_bytes)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def resolvable(repo, sha):
    return bool(sha) and _run(repo, ['rev-parse', '--verify', '--quiet', sha + '^{commit}'])[0] == 0


def show(repo, rev, path):
    return git(repo, 'show', '%s:%s' % (rev, path))


# ---------------- GitHub (GET only) ----------------
def env_value(name):
    for line in open(K['secuura_env'], encoding='utf-8'):
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('lib_gate69: %s not present in the Secuura .env (by name)' % name)


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


# ---------------- gate69: the batch's PR specs ----------------
def spec(which, head=None, pr=None, branch=None):
    """The kit spec for PR 'A' or 'B' (or a sim PR key such as 'X1394'), with the head / PR number / branch filled from the arguments.
    PR B's number and branch are NOT in kit.json (unknown at drafting): pass them, or they stay None and every check that needs them
    says NOT RUN by name. The head defaults to head_expected (A) / head_standin (B) — the launch ALWAYS passes the head it re-read."""
    if which in K['prs']:
        s = dict(K['prs'][which])
    elif which in K.get('sim_prs', {}):
        s = dict(K['sim_prs'][which])
    else:
        raise SystemExit('lib_gate69: unknown PR key %r (want A, B or a sim_prs key)' % which)
    s['key'] = which
    s['head'] = head or os.environ.get('G69_HEAD_' + which) or s.get('head') or s.get('head_expected') or s.get('head_standin')
    if pr: s['pr'] = str(pr)
    if branch: s['branch'] = branch
    return s
