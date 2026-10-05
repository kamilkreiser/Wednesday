#!/usr/bin/env python3
"""c5_prtext_gate64.py — C5 PR TEXT for #1389 (KS-1330). KS-1330 is the ticket this PR serves; whether it moves to Done is Wednesday's.

  --fetch <dir>   read-only GitHub GET of pulls/1389 (GH_TOKEN by name, never printed); writes <dir>/pr1389_body.md and
                  <dir>/pr1389_meta.json; then judges them.
  --body <file> --title <text> [--message <file>]   judge offline (the self-test fixtures use this).
  T1  exactly ONE `Refs KS-1330` in the body (markdown emphasis allowed) and the ticket URL https://linear.app/secuura/issue/KS-1330
  T2  CLOSING WORDS: 0 Linear magic-word references (close/fix/resolve/complete… then a hyphenated KS key in the same sentence —
      Linear does NOT parse negation, so "does not close KS-1302" COUNTS) in title, body AND commit message; 0 GitHub `<kw> #n`
  T3  the only hyphenated KS key in title + body is KS-1330 (KS 1302 / 1303 / 1325 de-hyphenated)
  T4  title == the kit subject (75 chars), <= 92, no `(#`
  T5  NOT COVERED stated: no live sweep; the PTY / foreground INT harness is KS 1325's; KS 1302 / KS 1303 residue not closed;
      #1250 not touched (its disposition not decided here); NO new pre-push leg
  T6  0 Co-Authored-By lines in the body (a squash may carry the body into the landed message)
  T7  the two re-landed blob ids the body credits == the kit's #1250 round-2 blobs, in full (runner 8eef1c4877b3, test 9c4a87f0a97c)
  T8  Q-DOC (b) stated, not skipped: "No block in either platform-k HTML doc", the skill blob == kit eaf43dfd4d98, and both §4 quotes
  INFO every figure the body states (54/7, 61/0, 61 -> 60, 67/0/0, the coupling table, kill_to_exit, inode/rdev, the grep claim,
       leg 14) printed for the gate to compare with C3 / C4 / the census; and the commit message's coupling sentence (STALE if not 0)
--selftest  synthetic bodies in <G64_SCRATCH>/fixtures: T0 a clean body passes; every arm must FAIL its named check.
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, Tally, gh_get, SCRATCH

CLOSE_RX = re.compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', re.I)
GHCLOSE_RX = re.compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', re.I)
KEY_RX = re.compile(r'\bKS-\d+\b')
QDOC = ['No block in either platform-k HTML doc', '"Test change" means backend unit, integration, *or* systemTest',
        '**say so explicitly and why**']


def judge(title, body, message, t):
    refs = re.findall(r'\bRefs\W{0,4}KS-1330\b', body)
    t.check('T1', len(refs) == 1 and K['ticket_url'] in body, '`Refs KS-1330` %d (want 1); ticket URL present %s' % (len(refs), K['ticket_url'] in body))
    hits = []
    for where, txt in (('title', title), ('body', body), ('message', message or '')):
        hits += ['%s: %r' % (where, m.group(0)[:90]) for m in CLOSE_RX.finditer(txt)]
        hits += ['%s: %r' % (where, m.group(0)) for m in GHCLOSE_RX.finditer(txt)]
    t.check('T2', not hits, 'closing references %d %s' % (len(hits), hits))
    keys = sorted(set(KEY_RX.findall(title + '\n' + body)))
    t.check('T3', keys == ['KS-1330'], 'hyphenated keys in title+body %s (want only KS-1330)' % keys)
    t.check('T4', title == K['subject'] and len(title) <= K['subject_max'] and '(#' not in title, 'title %r %d chars (want the kit subject, <= %d, no "(#")' % (
        title, len(title), K['subject_max']))
    need = {'no live sweep': bool(re.search(r'no live sweep', body, re.I)),
            'PTY / foreground INT is KS 1325': bool(re.search(r'KS 1325', body)),
            'KS 1302 / KS 1303 not closed': bool(re.search(r'KS 1302 and KS 1303[^.]{0,80}not closed', body)),
            '#1250 not touched': bool(re.search(r'#1250[^.\n]{0,40}(not touched|stays open)', body, re.I)),
            'no new pre-push leg': bool(re.search(r'no new\W{0,4}pre-push leg', body, re.I))}
    miss = [k for k, v in need.items() if not v]
    t.check('T5', not miss, 'NOT-COVERED statements missing %s' % miss)
    co = len(re.findall(r'(?im)^co-authored-by:', body))
    t.check('T6', co == 0, 'Co-Authored-By lines in body %d' % co)
    want = set(K['r2_blobs'].values()); got = set(re.findall(r'\b[0-9a-f]{40}\b', body)) - {K['head'], K['skill_blob']}
    t.check('T7', want <= got and not (got - want), 'full 40-hex ids credited %s; the kit r2 blobs %s present %s; others %s' % (
        sorted(x[:12] for x in got), sorted(x[:12] for x in want), want <= got, sorted(x[:12] for x in got - want)))
    q = [s for s in QDOC if s not in body]
    t.check('T8', not q and K['skill_blob'] in body, 'Q-DOC (b) statements missing %s; skill blob %s present %s' % (q, K['skill_blob'][:12], K['skill_blob'] in body))
    for lbl, rx in (('develop runner', r'develop\'s runner[^\n]{0,40}?\d+ passed / \d+ failed'), ('head', r'this head \d+ passed / \d+ failed'),
                    ('tamper total', r'total\s+\d+\s*(->|→)\s*\d+'), ('whole runner', r'shell suites: \d+ passed, \d+ failed, \d+ skipped \(of \d+\)'),
                    ('read head', r'`read` as a command head \| \*\*\d+\*\*'), ('trap INT', r'suites trapping INT \| \d+'),
                    ('also TERM/EXIT', r'\*\*\d+ of \d+\*\*'), ('kill_to_exit', r'kill_to_exit=\d+s[^\n]{0,40}'),
                    ('inode', r'inode \d+ and rdev [\d,]+|inode \d+'), ('grep claim', r'\*\*0 hits\*\*[^\n]{0,120}'), ('leg 14', r'come back \d+/\d+/\d+')):
        m = re.search(rx, body, re.I)
        t.info('FIG', '%s: %s' % (lbl, repr(m.group(0)[:160]) if m else 'ABSENT'))
    st = re.search(r'(\d+) use `read`', message or '')
    t.info('MSG', 'commit message coupling sentence: %s' % (repr(st.group(0)) + ' — STALE vs the body\'s 0 (lands only if the squash body carries the message)' if st else 'none'))


def selftest():
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    r, tt = K['r2_blobs'][K['runner']], K['r2_blobs'][K['test']]
    good = ('Refs KS-1330\n\n%s\n\n#1250 stays open and is not touched; blobs `%s` and `%s` re-landed.\n\n'
            '**No block in either platform-k HTML doc.** Skill blob `%s`:\n> "Test change" means backend unit, integration, *or* systemTest.\n'
            '> **say so explicitly and why**\n\nThis PR adds **no new pre-push leg**.\n\n## Not covered\nNo live sweep. A PTY harness is KS 1325. '
            'The residue items KS 1302 and KS 1303 own are not closed by this PR.\n' % (K['ticket_url'], r, tt, K['skill_blob']))
    open(os.path.join(fx, 'c5_good_body.md'), 'w').write(good)
    def run(title, body, msg=''):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(title, body, msg, t)
        return t
    t0 = run(K['subject'], good); ok = int(not t0.fails and t0.n == 8); total = 1
    print('SELFTEST %s T0 clean synthetic body (fixtures/c5_good_body.md): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    arms = [('Refs removed', None, good.replace('Refs KS-1330\n', ''), '', ['T1']),
            ('a second bold Refs', None, '**Refs KS-1330**\n' + good, '', ['T1']),
            ('URL removed', None, good.replace(K['ticket_url'], 'the ticket'), '', ['T1']),
            ('NEGATED "does not close KS-1302" in the body', None, good + 'This does not close KS-1302.\n', '', ['T2', 'T3']),
            ('"does not close KS-1330" in the commit message', None, good, 'x\n\nThis does not close KS-1330.\n', ['T2']),
            ('"fixes #1250"', None, good + 'fixes #1250\n', '', ['T2']),
            ('KS-1325 hyphenated', None, good.replace('KS 1325', 'KS-1325'), '', ['T3']),
            ('title with (#1389)', K['subject'] + ' (#1389)', good, '', ['T4']),
            ('title 93 chars', 'K' * 93, good, '', ['T4']),
            ('live sweep statement removed', None, good.replace('No live sweep. ', ''), '', ['T5']),
            ('#1250 untouched statement removed', None, good.replace('stays open and is not touched', 'is upstream'), '', ['T5']),
            ('"no new pre-push leg" removed', None, good.replace('**no new pre-push leg**', 'a tweak'), '', ['T5']),
            ('Co-Authored-By', None, good + 'Co-Authored-By: X <x@invalid>\n', '', ['T6']),
            ('a wrong runner blob credited', None, good.replace(r, '0' * 40), '', ['T7']),
            ('an extra 40-hex id', None, good + 'tree %s\n' % ('a' * 40), '', ['T7']),
            ('Q-DOC (b) sentence removed', None, good.replace('No block in either platform-k HTML doc', 'docs later'), '', ['T8']),
            ('skill blob id dropped', None, good.replace(K['skill_blob'], 'the skill'), '', ['T8'])]
    for name, title, body, msg, want in arms:
        assert body != good or msg or title, 'tamper did not land: ' + name
        p = os.path.join(fx, 'c5_arm_%02d.md' % total); open(p, 'w').write(body)
        t = run(title or K['subject'], body, msg); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (fixture %s): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    msg = open(opt('--message'), encoding='utf-8').read() if opt('--message') else ''
    if opt('--fetch'):
        d = opt('--fetch'); os.makedirs(d, exist_ok=True)
        p = gh_get('pulls/' + K['pr'])
        body = p.get('body') or ''; title = p['title']
        open(os.path.join(d, 'pr%s_body.md' % K['pr']), 'w', encoding='utf-8').write(body)
        meta = {'title': title, 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'], 'base_sha': p['base']['sha'],
                'state': p['state'], 'merged': p.get('merged'), 'draft': p.get('draft'), 'body_bytes': len(body.encode()), 'updated_at': p.get('updated_at')}
        json.dump(meta, open(os.path.join(d, 'pr%s_meta.json' % K['pr']), 'w'), indent=1)
        print('API #%s head %s branch %s base %s (%s) state %s merged %s body %d bytes updated %s' % (K['pr'], meta['head'], meta['branch'], meta['base'],
              meta['base_sha'][:12], meta['state'], meta['merged'], meta['body_bytes'], meta['updated_at']))
    else:
        body = open(opt('--body'), encoding='utf-8').read(); title = opt('--title', K['subject'])
    t = Tally(); judge(title, body, msg, t); raise SystemExit(t.end())
